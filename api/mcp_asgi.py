"""ASGI middleware: Streamable HTTP transport for MCP at POST /api/v1/mcp."""

from __future__ import annotations

import logging
from asgiref.sync import sync_to_async
from mcp.server.streamable_http import MCP_SESSION_ID_HEADER
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.responses import JSONResponse

from api.mcp_auth import resolve_streamable_authorization

logger = logging.getLogger(__name__)

MCP_PATH = "/api/v1/mcp"


def _get_header(scope, name: str) -> str:
    name_bytes = name.lower().encode()
    for key, value in scope.get("headers", []):
        if key.lower() == name_bytes:
            return value.decode()
    return ""


def _www_authenticate_header() -> str:
    from django.conf import settings as dj_settings

    base = (getattr(dj_settings, "SHOPIFY_APP_URL", None) or dj_settings.WAGTAILADMIN_BASE_URL or "").rstrip("/")
    metadata = f"{base}/.well-known/oauth-protected-resource" if base else "/.well-known/oauth-protected-resource"
    return f'Bearer realm="mcp", resource_metadata="{metadata}"'


async def _authenticate_scope(scope) -> tuple[bool, str]:
    from api.auth import ApiKeyAuth
    from api.mcp import get_mcp_server

    auth = ApiKeyAuth()
    mcp = get_mcp_server()
    session_id = _get_header(scope, MCP_SESSION_ID_HEADER)
    stored = mcp._streamable_session_auth.get(session_id, "") if session_id else ""
    resolved = await sync_to_async(
        resolve_streamable_authorization,
        thread_sensitive=True,
    )(
        request_authorization=_get_header(scope, "authorization"),
        stored_session_authorization=stored,
        fallback_authorization=mcp.default_auth_header,
        authenticate_token=auth._authenticate_token,
    )
    return bool(resolved), resolved


class MCPStreamableHTTPMiddleware:
    """Route Streamable HTTP MCP requests before Django; keep SSE on GET without session id."""

    def __init__(self, app):
        self.app = app
        self._session_manager: StreamableHTTPSessionManager | None = None
        self._run_cm = None

    def _is_streamable_http_request(self, scope) -> bool:
        if scope["type"] != "http":
            return False
        path = scope.get("path", "")
        if path not in (MCP_PATH, f"{MCP_PATH}/"):
            return False
        method = scope.get("method", "GET")
        if method in ("POST", "DELETE"):
            return True
        if method == "GET" and _get_header(scope, MCP_SESSION_ID_HEADER):
            return True
        return False

    async def __call__(self, scope, receive, send):
        if scope["type"] == "lifespan":
            await self._handle_lifespan(scope, receive, send)
            return

        if self._is_streamable_http_request(scope):
            await self._handle_streamable(scope, receive, send)
            return

        await self.app(scope, receive, send)

    async def _handle_lifespan(self, scope, receive, send):
        while True:
            message = await receive()
            if message["type"] == "lifespan.startup":
                try:
                    await self._start_session_manager()
                    await send({"type": "lifespan.startup.complete"})
                except Exception:
                    logger.exception("MCP Streamable HTTP session manager startup failed")
                    await send({"type": "lifespan.startup.failed"})
            elif message["type"] == "lifespan.shutdown":
                await self._stop_session_manager()
                await send({"type": "lifespan.shutdown.complete"})
                return

    async def _start_session_manager(self):
        if self._session_manager is not None:
            return

        from api.mcp import get_mcp_server

        self._session_manager = StreamableHTTPSessionManager(
            app=get_mcp_server().server,
            stateless=False,
            json_response=False,
        )
        self._run_cm = self._session_manager.run()
        await self._run_cm.__aenter__()

    async def _stop_session_manager(self):
        if self._run_cm is not None:
            await self._run_cm.__aexit__(None, None, None)
            self._run_cm = None
        self._session_manager = None

    async def _handle_streamable(self, scope, receive, send):
        ok, auth_header = await _authenticate_scope(scope)

        if not ok:
            response = JSONResponse(
                {"detail": "Unauthorized"},
                status_code=401,
                headers={"WWW-Authenticate": _www_authenticate_header()},
            )
            await response(scope, receive, send)
            return

        from api.mcp import get_mcp_server, streamable_request_authorization

        mcp = get_mcp_server()
        session_id = _get_header(scope, MCP_SESSION_ID_HEADER)
        if session_id:
            mcp.set_streamable_session_auth(session_id, auth_header)
        auth_token = streamable_request_authorization.set(auth_header)

        if self._session_manager is None:
            await self._start_session_manager()

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                for key, value in message.get("headers", []):
                    if key.lower() == b"mcp-session-id":
                        mcp.set_streamable_session_auth(value.decode(), auth_header)
            await send(message)

        mcp._active_streamable_session_id = session_id or None
        try:
            assert self._session_manager is not None
            await self._session_manager.handle_request(scope, receive, send_wrapper)
        finally:
            streamable_request_authorization.reset(auth_token)
            mcp._active_streamable_session_id = None

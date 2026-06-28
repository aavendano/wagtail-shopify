import asyncio
import json
import logging
import time
from typing import Any
from uuid import UUID, uuid4

import anyio
import mcp.types as types
from django.conf import settings
from django.http import HttpRequest, JsonResponse
from mcp.shared.message import SessionMessage
from ninja import Body, NinjaAPI, Path, Router
from ninja_mcp import NinjaMCP
from ninja_mcp.transport.sse import DjangoSseServerTransport

logger = logging.getLogger(__name__)

_DEBUG_LOG_PATH = "/home/alejandro/apps/wagtail-shopify/.cursor/debug-4100ed.log"
_DEBUG_SESSION_ID = "4100ed"


def _agent_debug_log(*, hypothesis_id: str, location: str, message: str, data: dict | None = None) -> None:
    # #region agent log
    try:
        payload = {
            "sessionId": _DEBUG_SESSION_ID,
            "runId": "pre-fix",
            "hypothesisId": hypothesis_id,
            "location": location,
            "message": message,
            "data": data or {},
            "timestamp": int(time.time() * 1000),
        }
        with open(_DEBUG_LOG_PATH, "a", encoding="utf-8") as log_file:
            log_file.write(json.dumps(payload) + "\n")
    except OSError:
        pass
    # #endregion


class AuthForwardingSseTransport(DjangoSseServerTransport):
    """SSE transport that stores Authorization per session for internal API calls."""

    def __init__(self, endpoint: str, server, mcp: "WagtailShopifyMCP") -> None:
        super().__init__(endpoint, server)
        self._mcp = mcp
        self._session_auth: dict[UUID, str] = {}

    @staticmethod
    def _serialize_sse_payload(message) -> str:
        if isinstance(message, SessionMessage):
            return message.message.model_dump_json(by_alias=True, exclude_none=True)
        return message.model_dump_json()

    async def handle_post_message(self, session_id: UUID, message: types.JSONRPCMessage):
        writer = self._read_stream_writers.get(session_id)
        # #region agent log
        _agent_debug_log(
            hypothesis_id="H4",
            location="api/mcp.py:handle_post_message",
            message="MCP POST message received",
            data={
                "session_id": str(session_id),
                "session_found": writer is not None,
                "active_sessions": len(self._read_stream_writers),
                "method": getattr(message, "method", None),
            },
        )
        # #endregion
        if not writer:
            return JsonResponse({"error": "Could not find session"}, status=404)

        # django-ninja-mcp sends bare JSONRPCMessage; MCP session expects SessionMessage.
        asyncio.create_task(writer.send(SessionMessage(message=message)))
        return JsonResponse({"status": "Accepted"}, status=202)

    def connect_sse(self, request: HttpRequest):
        logger.debug("Setting up SSE connection with auth forwarding")

        session_id = uuid4()
        request_auth = request.META.get("HTTP_AUTHORIZATION", "")
        fallback_auth = self._mcp.default_auth_header
        auth_header = request_auth or fallback_auth
        # #region agent log
        _agent_debug_log(
            hypothesis_id="H1",
            location="api/mcp.py:connect_sse",
            message="MCP SSE connection opened",
            data={
                "session_id": str(session_id),
                "has_request_auth": bool(request_auth),
                "uses_fallback_auth": bool(not request_auth and fallback_auth),
                "auth_scheme": request_auth.split(" ", 1)[0] if request_auth else None,
                "user_agent": request.META.get("HTTP_USER_AGENT", "")[:80],
            },
        )
        # #endregion
        self._session_auth[session_id] = auth_header

        read_stream_writer, read_stream = anyio.create_memory_object_stream(0)
        write_stream, write_stream_reader = anyio.create_memory_object_stream(0)
        self._read_stream_writers[session_id] = read_stream_writer

        async def sse_writer():
            try:
                yield f"event: endpoint\ndata: {session_id}\n\n"
                async with write_stream_reader:
                    async for message in write_stream_reader:
                        payload = self._serialize_sse_payload(message)
                        yield f"event: message\ndata: {payload}\n\n"
            except Exception as exc:
                logger.error("Error in SSE writer: %s", exc)
            finally:
                self._session_auth.pop(session_id, None)
                if session_id in self._read_stream_writers:
                    del self._read_stream_writers[session_id]

        async def run_mcp_server():
            self._mcp._active_session_id = session_id
            try:
                await self._server.run(
                    read_stream,
                    write_stream,
                    self._server.create_initialization_options(),
                )
            finally:
                self._mcp._active_session_id = None
                self._session_auth.pop(session_id, None)
                if session_id in self._write_tasks:
                    self._write_tasks[session_id].cancel()
                    del self._write_tasks[session_id]
                await write_stream.aclose()
                await read_stream.aclose()

        asyncio.create_task(run_mcp_server())
        return sse_writer()


class WagtailShopifyMCP(NinjaMCP):
    def __init__(self, *args, **kwargs):
        self._active_session_id: UUID | None = None
        super().__init__(*args, **kwargs)

    @property
    def default_auth_header(self) -> str:
        key = getattr(settings, "MCP_DEFAULT_API_KEY", "")
        return f"Bearer {key}" if key else ""

    def mount(self, router: NinjaAPI | Router | None = None, mount_path: str = "/mcp") -> None:
        if not mount_path.startswith("/"):
            mount_path = f"/{mount_path}"
        if mount_path.endswith("/"):
            mount_path = mount_path[:-1]

        if router is None:
            router = self.ninja

        self.sse_transport = AuthForwardingSseTransport(
            f"{mount_path}/messages/",
            self.server,
            self,
        )

        @router.event_source(mount_path, include_in_schema=False, operation_id="mcp_connection")
        async def handle_mcp_connection(request):
            """Handle SSE connection for MCP clients."""
            async for event in self.sse_transport.connect_sse(request):
                yield event

        @router.post(
            "/{session_id}",
            include_in_schema=False,
            response=dict[str, Any],
            operation_id="mcp_messages",
        )
        async def handle_post_message(
            request,
            session_id: Path[UUID],
            message: Body[types.JSONRPCMessage],
        ):
            """Handle POST messages from MCP clients."""
            return await self.sse_transport.handle_post_message(session_id, message)

        logger.info("MCP server listening at %s", mount_path)

    async def _request(self, client, method, url, query, headers, body):
        headers = dict(headers)
        auth_header = ""
        session_id = self._active_session_id
        if session_id and self.sse_transport:
            auth_header = self.sse_transport._session_auth.get(session_id, "")
        if not auth_header:
            auth_header = self.default_auth_header
        if auth_header and "Authorization" not in headers:
            headers["Authorization"] = auth_header
        return await super()._request(client, method, url, query, headers, body)


_mcp_server: WagtailShopifyMCP | None = None


def get_mcp_server() -> WagtailShopifyMCP:
    if _mcp_server is None:
        raise RuntimeError("MCP server not initialized; import api.main first")
    return _mcp_server


def setup_mcp(api, description: str) -> WagtailShopifyMCP:
    global _mcp_server
    if _mcp_server is not None:
        return _mcp_server

    mcp_server = WagtailShopifyMCP(
        ninja=api,
        base_url=settings.MCP_BASE_URL,
        name="Wagtail-Shopify Content API",
        description=description,
        describe_all_responses=True,
        exclude_operations=["mcp_connection", "mcp_messages"],
    )
    mcp_server.mount(api, mount_path="/mcp")
    _mcp_server = mcp_server
    return mcp_server

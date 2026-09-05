"""RFC 7591 Dynamic Client Registration for MCP OAuth clients.

Each successful POST /register creates a new public Application (PKCE, no
secret). Redirect URIs must be Cursor/Claude callbacks or localhost loopback.
Legacy shared apps named PLT-CMS are not reused.
"""

from __future__ import annotations

import json
import uuid
from urllib.parse import urlparse

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.models import Application

MCP_REDIRECT_ALLOWLIST = {
    "https://www.cursor.com/agents/mcp/oauth/callback",
    "https://cursor.com/agents/mcp/oauth/callback",
    "https://claude.ai/api/mcp/auth_callback",
    "cursor://anysphere.cursor-mcp/oauth/callback",
    "http://localhost:8787/callback",
    "http://127.0.0.1:8787/callback",
}

_LOOPBACK_HOSTS = {"localhost", "127.0.0.1", "[::1]"}
_LOOPBACK_PATHS = {"/callback", "/oauth/callback"}


def is_allowed_redirect_uri(uri: str) -> bool:
    if not uri or uri in MCP_REDIRECT_ALLOWLIST:
        return bool(uri) and uri in MCP_REDIRECT_ALLOWLIST
    parsed = urlparse(uri)
    if parsed.scheme == "http" and parsed.hostname in _LOOPBACK_HOSTS:
        if parsed.path.rstrip("/") in {p.rstrip("/") for p in _LOOPBACK_PATHS} or parsed.path in _LOOPBACK_PATHS:
            return not parsed.query and not parsed.fragment
    return False


def _cors(response):
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Authorization, Content-Type, MCP-Protocol-Version"
    return response


def _error(status, code, description):
    return _cors(JsonResponse({"error": code, "error_description": description}, status=status))


def _create_mcp_application(*, redirect_uris: list[str], client_name: str) -> Application:
    """Create one public Application per DCR request (RFC 7591)."""
    name = (client_name or "").strip() or f"mcp-{uuid.uuid4().hex[:8]}"
    app = Application(
        name=name[:255],
        client_type=Application.CLIENT_PUBLIC,
        authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        hash_client_secret=False,
        client_secret="",
        redirect_uris=" ".join(sorted(set(redirect_uris))),
    )
    app.save()
    return app


@method_decorator(csrf_exempt, name="dispatch")
class OAuthDynamicClientRegistrationView(View):
    """Open registration for public MCP clients (PKCE, no client secret)."""

    http_method_names = ["post", "options"]

    def options(self, request, *args, **kwargs):
        return _cors(JsonResponse({}))

    def post(self, request, *args, **kwargs):
        try:
            payload = json.loads(request.body.decode() or "{}")
        except (UnicodeDecodeError, json.JSONDecodeError):
            return _error(400, "invalid_client_metadata", "Request body must be JSON.")

        raw_uris = payload.get("redirect_uris") or []
        if isinstance(raw_uris, str):
            raw_uris = [raw_uris]
        if not isinstance(raw_uris, list) or not raw_uris:
            return _error(400, "invalid_redirect_uri", "redirect_uris is required.")

        uris = [str(uri).strip() for uri in raw_uris if str(uri).strip()]
        if not uris or any(not is_allowed_redirect_uri(uri) for uri in uris):
            return _error(
                400,
                "invalid_redirect_uri",
                "redirect_uris must be Cursor/Claude MCP callbacks or localhost loopback.",
            )

        client_name = str(payload.get("client_name") or "").strip()
        app = _create_mcp_application(redirect_uris=uris, client_name=client_name)
        issued_at = int(app.created.timestamp()) if app.created else None
        body = {
            "client_id": app.client_id,
            "client_id_issued_at": issued_at,
            "client_name": app.name,
            "redirect_uris": uris,
            "grant_types": ["authorization_code", "refresh_token"],
            "response_types": ["code"],
            "token_endpoint_auth_method": "none",
            "scope": "mcp",
        }
        return _cors(JsonResponse(body, status=201))

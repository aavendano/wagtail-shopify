import api.ninja_compat  # noqa: F401 — must run before any ninja import

from datetime import timedelta
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from django.test import TestCase, override_settings
from django.utils import timezone
from ninja.openapi import get_schema
from ninja.testing import TestClient
from oauth2_provider.models import AccessToken, Application

from api.main import api
from api.mcp import WagtailShopifyMCP, get_mcp_server
from api.models import ApiKey


def _auth_headers(key: str) -> dict:
    return {"Authorization": f"Bearer {key}"}


def _openapi_operation_ids():
    schema = get_schema(api=api, path_prefix="")
    operation_ids = set()
    for path_item in schema.get("paths", {}).values():
        for method, operation in path_item.items():
            if method in ("get", "post", "put", "patch", "delete"):
                op_id = operation.get("operationId")
                if op_id:
                    operation_ids.add(op_id)
    return operation_ids


class McpToolGenerationTests(TestCase):
    def test_mcp_tool_count_matches_openapi_operations(self):
        mcp_server = get_mcp_server()
        openapi_ops = _openapi_operation_ids()
        mcp_tool_names = {tool.name for tool in mcp_server.tools}
        self.assertEqual(mcp_tool_names, openapi_ops)
        self.assertGreaterEqual(len(mcp_tool_names), 41)
        self.assertIn("list_products", mcp_tool_names)
        self.assertIn("push_location", mcp_tool_names)
        self.assertIn("push_glossary_term", mcp_tool_names)
        self.assertNotIn("mcp_connection", mcp_tool_names)


class McpAuthForwardingTests(TestCase):
    @override_settings(MCP_DEFAULT_API_KEY="fallback-key")
    async def test_request_uses_session_authorization_header(self):
        mcp_server = WagtailShopifyMCP(
            ninja=api,
            base_url="http://testserver/api/v1",
            http_client=AsyncMock(),
        )
        session_id = uuid4()
        mcp_server.sse_transport = MagicMock()
        mcp_server.sse_transport._session_auth = {
            session_id: "Bearer session-key",
        }
        mcp_server._active_session_id = session_id

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mcp_server._http_client.get = AsyncMock(return_value=mock_response)

        await mcp_server._request(
            mcp_server._http_client,
            "get",
            "http://testserver/api/v1/products/",
            {},
            {},
            None,
        )

        _, kwargs = mcp_server._http_client.get.call_args
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer session-key")

    @override_settings(MCP_DEFAULT_API_KEY="fallback-key")
    async def test_request_falls_back_to_mcp_default_api_key(self):
        mcp_server = WagtailShopifyMCP(
            ninja=api,
            base_url="http://testserver/api/v1",
            http_client=AsyncMock(),
        )
        mcp_server._active_session_id = None

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mcp_server._http_client.get = AsyncMock(return_value=mock_response)

        await mcp_server._request(
            mcp_server._http_client,
            "get",
            "http://testserver/api/v1/products/",
            {},
            {},
            None,
        )

        _, kwargs = mcp_server._http_client.get.call_args
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer fallback-key")

    @override_settings(MCP_DEFAULT_API_KEY="fallback-key")
    async def test_request_uses_streamable_contextvar_authorization(self):
        from api.mcp import streamable_request_authorization

        mcp_server = WagtailShopifyMCP(
            ninja=api,
            base_url="http://testserver/api/v1",
            http_client=AsyncMock(),
        )
        mcp_server._active_session_id = None
        mcp_server._active_streamable_session_id = None

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mcp_server._http_client.get = AsyncMock(return_value=mock_response)

        token = streamable_request_authorization.set("Bearer context-key")
        try:
            await mcp_server._request(
                mcp_server._http_client,
                "get",
                "http://testserver/api/v1/products/",
                {},
                {},
                None,
            )
        finally:
            streamable_request_authorization.reset(token)

        _, kwargs = mcp_server._http_client.get.call_args
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer context-key")


class StreamableAuthResolutionTests(TestCase):
    def test_prefers_valid_request_bearer_over_session_and_fallback(self):
        from api.mcp_auth import resolve_streamable_authorization

        resolved = resolve_streamable_authorization(
            request_authorization="Bearer request-key",
            stored_session_authorization="Bearer session-key",
            fallback_authorization="Bearer fallback-key",
            authenticate_token=lambda token: token == "request-key",
        )
        self.assertEqual(resolved, "Bearer request-key")

    def test_skips_invalid_request_bearer_and_uses_session(self):
        from api.mcp_auth import resolve_streamable_authorization

        resolved = resolve_streamable_authorization(
            request_authorization="Bearer expired-oauth",
            stored_session_authorization="Bearer session-key",
            fallback_authorization="Bearer fallback-key",
            authenticate_token=lambda token: token == "session-key",
        )
        self.assertEqual(resolved, "Bearer session-key")

    def test_ignores_unvalidated_fallback(self):
        from api.mcp_auth import resolve_streamable_authorization

        resolved = resolve_streamable_authorization(
            request_authorization="",
            stored_session_authorization="",
            fallback_authorization="Bearer not-in-database",
            authenticate_token=lambda token: False,
        )
        self.assertEqual(resolved, "")


@override_settings(
    SHOPIFY_APP_URL="https://cms.aadigitalbusiness.com",
    WAGTAILADMIN_BASE_URL="https://cms.aadigitalbusiness.com",
    MCP_DEFAULT_API_KEY="",
)
class StreamableWwwAuthenticateTests(TestCase):
    def test_unauthenticated_streamable_post_includes_www_authenticate(self):
        from asgiref.sync import async_to_sync

        from api.mcp_asgi import MCPStreamableHTTPMiddleware

        async def dummy_app(scope, receive, send):
            raise AssertionError("unauthenticated Streamable request must not reach Django")

        middleware = MCPStreamableHTTPMiddleware(dummy_app)

        async def run():
            status = {}
            headers = {}

            async def receive():
                return {"type": "http.request", "body": b"{}", "more_body": False}

            async def send(message):
                if message["type"] == "http.response.start":
                    status["code"] = message["status"]
                    headers.update(
                        {
                            key.decode().lower(): value.decode()
                            for key, value in message.get("headers", [])
                        }
                    )

            scope = {
                "type": "http",
                "asgi": {"version": "3.0"},
                "http_version": "1.1",
                "method": "POST",
                "scheme": "https",
                "path": "/api/v1/mcp",
                "raw_path": b"/api/v1/mcp",
                "query_string": b"",
                "headers": [(b"content-type", b"application/json")],
                "client": ("127.0.0.1", 50000),
                "server": ("cms.aadigitalbusiness.com", 443),
            }
            await middleware(scope, receive, send)
            return status.get("code"), headers

        code, headers = async_to_sync(run)()
        self.assertEqual(code, 401)
        www = headers.get("www-authenticate", "")
        self.assertIn('Bearer realm="mcp"', www)
        self.assertIn(
            'resource_metadata="https://cms.aadigitalbusiness.com/.well-known/oauth-protected-resource"',
            www,
        )

    def test_authenticate_token_accepts_active_api_key(self):
        from api.auth import ApiKeyAuth

        key = ApiKey.objects.create(name="streamable-key")
        auth = ApiKeyAuth()
        self.assertIsNotNone(auth._authenticate_token(key.key))
        self.assertIsNone(auth._authenticate_token("missing-key"))


class McpEndpointAuthTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)
        self.key = ApiKey.objects.create(name="mcp-agent")
        self.oauth_app = Application.objects.create(
            name="mcp-client",
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris="http://localhost/callback",
        )

    def _create_access_token(self, token: str, scope: str = "mcp", expired: bool = False):
        expires = timezone.now() + timedelta(hours=1)
        if expired:
            expires = timezone.now() - timedelta(minutes=1)
        return AccessToken.objects.create(
            application=self.oauth_app,
            token=token,
            expires=expires,
            scope=scope,
        )

    def test_mcp_sse_requires_api_key(self):
        response = self.client.get("/mcp")
        self.assertEqual(response.status_code, 401)

    def test_mcp_sse_route_is_registered(self):
        response = self.client.get("/mcp", headers=_auth_headers(self.key.key))
        self.assertNotEqual(response.status_code, 404)

    def test_mcp_sse_accepts_oauth_access_token_with_mcp_scope(self):
        token = self._create_access_token("valid-oauth-token", scope="mcp")

        response = self.client.get("/mcp", headers=_auth_headers(token.token))

        self.assertNotEqual(response.status_code, 401)

    def test_mcp_sse_rejects_oauth_access_token_without_mcp_scope(self):
        token = self._create_access_token("wrong-scope-token", scope="read write")

        response = self.client.get("/mcp", headers=_auth_headers(token.token))

        self.assertEqual(response.status_code, 401)

    def test_mcp_sse_rejects_expired_oauth_access_token(self):
        token = self._create_access_token("expired-oauth-token", expired=True)

        response = self.client.get("/mcp", headers=_auth_headers(token.token))

        self.assertEqual(response.status_code, 401)

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

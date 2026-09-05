from django.test import Client, SimpleTestCase, TestCase, override_settings

from api.oauth_registration import is_allowed_redirect_uri


class RedirectAllowlistTests(SimpleTestCase):
    def test_allows_cursor_and_loopback_callbacks(self):
        self.assertTrue(is_allowed_redirect_uri("https://www.cursor.com/agents/mcp/oauth/callback"))
        self.assertTrue(is_allowed_redirect_uri("http://localhost:8787/callback"))
        self.assertTrue(is_allowed_redirect_uri("http://127.0.0.1:9999/callback"))
        self.assertFalse(is_allowed_redirect_uri("https://evil.example/callback"))


@override_settings(
    SHOPIFY_APP_URL="https://cms.aadigitalbusiness.com",
    WAGTAILADMIN_BASE_URL="https://cms.aadigitalbusiness.com",
)
class OAuthRootRouteTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST="cms.aadigitalbusiness.com")

    def test_authorize_root_redirects_unauthenticated_users_to_login(self):
        response = self.client.get(
            "/authorize",
            {
                "response_type": "code",
                "client_id": "test-client",
                "redirect_uri": "https://claude.ai/api/mcp/auth_callback",
                "code_challenge": "challenge",
                "code_challenge_method": "S256",
                "state": "xyz",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin-django/login/", response["Location"])
        self.assertIn("/authorize", response["Location"])

    def test_token_root_accepts_post(self):
        response = self.client.post(
            "/token",
            {
                "grant_type": "authorization_code",
                "code": "invalid",
                "redirect_uri": "https://claude.ai/api/mcp/auth_callback",
                "client_id": "missing",
                "client_secret": "missing",
            },
        )

        self.assertIn(response.status_code, (400, 401))

    def test_oauth_authorization_server_metadata(self):
        response = self.client.get("/.well-known/oauth-authorization-server")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["authorization_endpoint"], "https://cms.aadigitalbusiness.com/authorize")
        self.assertEqual(payload["token_endpoint"], "https://cms.aadigitalbusiness.com/token")
        self.assertIn("S256", payload["code_challenge_methods_supported"])
        self.assertEqual(payload["registration_endpoint"], "https://cms.aadigitalbusiness.com/register")
        self.assertEqual(payload["token_endpoint_auth_methods_supported"], ["none"])

    def test_oauth_protected_resource_metadata(self):
        response = self.client.get("/.well-known/oauth-protected-resource")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["resource"], "https://cms.aadigitalbusiness.com/api/v1/mcp")
        self.assertEqual(payload["authorization_servers"], ["https://cms.aadigitalbusiness.com"])

    def test_dynamic_client_registration_returns_public_client(self):
        from oauth2_provider.models import Application

        response = self.client.post(
            "/register",
            data={
                "redirect_uris": [
                    "https://www.cursor.com/agents/mcp/oauth/callback",
                    "http://localhost:8787/callback",
                ],
                "client_name": "Cursor",
                "token_endpoint_auth_method": "none",
                "grant_types": ["authorization_code"],
                "response_types": ["code"],
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        payload = response.json()
        self.assertEqual(payload["token_endpoint_auth_method"], "none")
        self.assertEqual(payload["client_name"], "Cursor")
        self.assertTrue(payload["client_id"])
        app = Application.objects.get(client_id=payload["client_id"])
        self.assertEqual(app.client_type, Application.CLIENT_PUBLIC)
        self.assertEqual(app.name, "Cursor")
        self.assertIn("https://www.cursor.com/agents/mcp/oauth/callback", app.redirect_uris)
        # Only requested URIs — not the full allowlist dumped onto one shared app.
        self.assertNotIn("https://claude.ai/api/mcp/auth_callback", app.redirect_uris)

    def test_dynamic_client_registration_creates_distinct_clients(self):
        from oauth2_provider.models import Application

        cursor = self.client.post(
            "/register",
            data={
                "redirect_uris": ["https://www.cursor.com/agents/mcp/oauth/callback"],
                "client_name": "Cursor",
                "token_endpoint_auth_method": "none",
            },
            content_type="application/json",
        )
        claude = self.client.post(
            "/register",
            data={
                "redirect_uris": ["https://claude.ai/api/mcp/auth_callback"],
                "client_name": "Claude",
                "token_endpoint_auth_method": "none",
            },
            content_type="application/json",
        )

        self.assertEqual(cursor.status_code, 201)
        self.assertEqual(claude.status_code, 201)
        cursor_id = cursor.json()["client_id"]
        claude_id = claude.json()["client_id"]
        self.assertNotEqual(cursor_id, claude_id)
        self.assertEqual(Application.objects.filter(name="PLT-CMS").count(), 0)
        cursor_app = Application.objects.get(client_id=cursor_id)
        claude_app = Application.objects.get(client_id=claude_id)
        self.assertNotIn("https://claude.ai/api/mcp/auth_callback", cursor_app.redirect_uris)
        self.assertNotIn("https://www.cursor.com/agents/mcp/oauth/callback", claude_app.redirect_uris)

    def test_dynamic_client_registration_rejects_unknown_redirect(self):
        response = self.client.post(
            "/register",
            data={
                "redirect_uris": ["https://evil.example/steal"],
                "token_endpoint_auth_method": "none",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "invalid_redirect_uri")

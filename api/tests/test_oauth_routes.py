from django.test import Client, TestCase, override_settings


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

    def test_oauth_protected_resource_metadata(self):
        response = self.client.get("/.well-known/oauth-protected-resource")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["resource"], "https://cms.aadigitalbusiness.com/api/v1/mcp")
        self.assertEqual(payload["authorization_servers"], ["https://cms.aadigitalbusiness.com"])

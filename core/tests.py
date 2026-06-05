from django.test import TestCase, override_settings
from django.urls import reverse
from types import SimpleNamespace
from unittest.mock import patch

from .embedded_redirects import (
    validate_parent_redirect_url,
    validate_relative_app_path,
)
from .forms import ShopConfigForm
from .models import ShopConfig


class ShopConfigFormTests(TestCase):
    def test_accepts_valid_myshopify_domain(self):
        with patch.object(ShopConfigForm, "validate_unique", return_value=None):
            form = ShopConfigForm(data={"shop": "test-shop.myshopify.com"})
            self.assertTrue(form.is_valid())
            self.assertEqual(form.cleaned_data["shop"], "test-shop.myshopify.com")

    def test_normalizes_shop_domain_to_lowercase_and_strips_spaces(self):
        with patch.object(ShopConfigForm, "validate_unique", return_value=None):
            form = ShopConfigForm(data={"shop": "  Test-Shop.MYSHOPIFY.COM  "})
            self.assertTrue(form.is_valid())
            self.assertEqual(form.cleaned_data["shop"], "test-shop.myshopify.com")

    def test_rejects_domain_without_myshopify_suffix(self):
        with patch.object(ShopConfigForm, "validate_unique", return_value=None):
            form = ShopConfigForm(data={"shop": "test-shop.com"})
            self.assertFalse(form.is_valid())
            self.assertIn("shop", form.errors)

    def test_rejects_domain_with_invalid_characters(self):
        with patch.object(ShopConfigForm, "validate_unique", return_value=None):
            form = ShopConfigForm(data={"shop": "test_shop.myshopify.com"})
            self.assertFalse(form.is_valid())
            self.assertIn("shop", form.errors)


class PublicEntryViewTests(TestCase):
    def test_renders_landing_even_when_shop_exists(self):
        response = self.client.get(
            f"{reverse('core:install')}?shop=test-shop.myshopify.com&hmac=abc123"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'action="/auth/login"')

    def test_renders_landing_with_auth_login_form_without_shop(self):
        response = self.client.get(reverse("core:install"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'action="/auth/login"')
        self.assertContains(response, 'name="shop"')
        self.assertContains(response, 'placeholder="my-shop-domain.myshopify.com"')

    @patch("core.mixins.get_shopify_app")
    def test_app_route_still_works(self, mocked_get_shopify_app):
        mocked_get_shopify_app.return_value.verify_app_home_req.return_value = SimpleNamespace(
            ok=True,
            response=SimpleNamespace(headers={}),
        )
        response = self.client.get("/app/")

        self.assertEqual(response.status_code, 200)


@override_settings(SHOPIFY_API_KEY="test-client-id")
class AuthLoginViewTests(TestCase):
    def test_get_without_shop_renders_form(self):
        response = self.client.get(reverse("core:auth-login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'action="/auth/login"')

    def test_get_with_valid_shop_keeps_form_flow(self):
        response = self.client.get(
            f"{reverse('core:auth-login')}?shop=valid-shop.myshopify.com"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'action="/auth/login"')

    def test_post_with_invalid_shop_renders_form_with_error(self):
        response = self.client.post(reverse("core:auth-login"), data={"shop": "invalid.com"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Shop domain must match *.myshopify.com.")

    def test_post_with_valid_shop_redirects_to_shopify_install(self):
        response = self.client.post(
            reverse("core:auth-login"),
            data={"shop": "  Valid-Shop.MYSHOPIFY.COM  "},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "https://admin.shopify.com/store/valid-shop/oauth/install?client_id=test-client-id",
        )


class HomeViewAuthTests(TestCase):
    @patch("core.mixins.get_shopify_app")
    def test_home_view_uses_expected_patch_id_token_path(self, mocked_get_shopify_app):
        mocked_get_shopify_app.return_value.verify_app_home_req.return_value = SimpleNamespace(
            ok=True,
            response=SimpleNamespace(headers={}),
        )

        self.client.get("/app/?shop=test-shop.myshopify.com")

        mocked_get_shopify_app.return_value.verify_app_home_req.assert_called_once()
        _, kwargs = mocked_get_shopify_app.return_value.verify_app_home_req.call_args
        self.assertEqual(kwargs["app_home_patch_id_token_path"], "/core/auth/patch-id-token")

    @patch("core.mixins.get_shopify_app")
    def test_document_request_valid_renders_page_and_copies_headers(self, mocked_get_shopify_app):
        mocked_get_shopify_app.return_value.verify_app_home_req.return_value = SimpleNamespace(
            ok=True,
            response=SimpleNamespace(
                headers={
                    "Content-Security-Policy": "frame-ancestors https://shop.myshopify.com;",
                }
            ),
        )

        response = self.client.get("/app/?shop=test-shop.myshopify.com")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Content-Security-Policy", response)

    @patch("core.mixins.get_shopify_app")
    def test_document_request_without_id_token_redirects_to_patch_route(
        self, mocked_get_shopify_app
    ):
        mocked_get_shopify_app.return_value.verify_app_home_req.return_value = SimpleNamespace(
            ok=False,
            response=SimpleNamespace(
                status=302,
                body="",
                headers={
                    "Location": "/core/auth/patch-id-token?shop=test-shop.myshopify.com"
                },
            ),
        )

        response = self.client.get("/app/?shop=test-shop.myshopify.com")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["Location"], "/core/auth/patch-id-token?shop=test-shop.myshopify.com"
        )

    @patch("core.mixins.get_shopify_app")
    def test_fetch_request_with_invalid_token_returns_unauthorized(
        self, mocked_get_shopify_app
    ):
        mocked_get_shopify_app.return_value.verify_app_home_req.return_value = SimpleNamespace(
            ok=False,
            response=SimpleNamespace(
                status=401,
                body="Unauthorized",
                headers={"X-Shopify-Retry-Invalid-Session-Request": "1"},
            ),
        )

        response = self.client.get(
            "/app/?shop=test-shop.myshopify.com",
            HTTP_AUTHORIZATION="Bearer invalid-token",
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response["X-Shopify-Retry-Invalid-Session-Request"], "1")

    @patch("core.mixins.get_shopify_app")
    def test_fetch_request_with_valid_token_returns_ok(self, mocked_get_shopify_app):
        mocked_get_shopify_app.return_value.verify_app_home_req.return_value = SimpleNamespace(
            ok=True,
            response=SimpleNamespace(headers={}),
        )

        response = self.client.get(
            "/app/?shop=test-shop.myshopify.com",
            HTTP_AUTHORIZATION="Bearer valid-token",
        )

        self.assertEqual(response.status_code, 200)

    @patch("shopify_requests.graphql_client.raw_admin_graphql")
    @patch("core.mixins.get_shopify_app")
    def test_home_graphql_failure_returns_sdk_http_response(
        self, mocked_get_shopify_app, mock_raw_gql
    ):
        ShopConfig.objects.create(
            shop="test-shop",
            is_online=False,
            access_token="tok",
        )
        mocked_get_shopify_app.return_value.verify_app_home_req.return_value = SimpleNamespace(
            ok=True,
            shop="test-shop",
            new_id_token_response=SimpleNamespace(status=401, body="", headers={}),
            response=SimpleNamespace(headers={}),
        )
        mock_raw_gql.return_value = SimpleNamespace(
            ok=False,
            shop="test-shop",
            data=None,
            log=SimpleNamespace(code="unauthorized", detail=""),
            response=SimpleNamespace(
                status=401,
                body="Unauthorized",
                headers={"X-Shopify-Retry-Invalid-Session-Request": "1"},
            ),
        )

        response = self.client.get("/app/?shop=test-shop.myshopify.com")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response["X-Shopify-Retry-Invalid-Session-Request"], "1")
        record = ShopConfig.objects.get(shop="test-shop")
        self.assertIsNone(record.access_token)


class AuthPatchIdTokenViewTests(TestCase):
    @patch("core.views.get_shopify_app")
    def test_patch_id_token_route_returns_sdk_response(self, mocked_get_shopify_app):
        mocked_get_shopify_app.return_value.app_home_patch_id_token.return_value = (
            SimpleNamespace(
                ok=False,
                response=SimpleNamespace(
                    status=302,
                    body="",
                    headers={"Location": "/app/?shopify-reload=%2Fapp%2F"},
                ),
                log=SimpleNamespace(code="redirect_to_patch_id_token_page", detail="redirect"),
            )
        )

        response = self.client.get("/core/auth/patch-id-token?shop=test-shop.myshopify.com")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/app/?shopify-reload=%2Fapp%2F")


class TokenLifecycleTests(TestCase):
    @patch("shopify_requests.graphql_client.raw_admin_graphql")
    @patch("core.mixins.get_shopify_app")
    def test_exchange_persists_offline_token_data(
        self, mocked_get_shopify_app, mock_raw_gql
    ):
        mock_raw_gql.return_value = SimpleNamespace(
            ok=True,
            shop="test-shop",
            data={"shop": {"id": "gid://shopify/Shop/1"}},
            extensions=None,
            log=SimpleNamespace(code="success", detail="ok"),
            response=SimpleNamespace(status=200, body="", headers={}),
        )
        mocked_get_shopify_app.return_value.verify_app_home_req.return_value = SimpleNamespace(
            ok=True,
            shop="test-shop",
            id_token=SimpleNamespace(
                exchangeable=True,
                token="jwt-token",
                claims={"dest": "https://test-shop.myshopify.com"},
            ),
            new_id_token_response=SimpleNamespace(status=401, body="", headers={}),
            response=SimpleNamespace(headers={}),
        )
        mocked_get_shopify_app.return_value.exchange_using_token_exchange.return_value = (
            SimpleNamespace(
                ok=True,
                access_token=SimpleNamespace(
                    access_mode="offline",
                    shop="test-shop",
                    token="new-access-token",
                    scope="write_products",
                    expires="2027-01-01T00:00:00Z",
                    refresh_token="refresh-token",
                    refresh_token_expires="2027-02-01T00:00:00Z",
                ),
                log=SimpleNamespace(code="success", detail="ok"),
            )
        )

        response = self.client.get("/app/?shop=test-shop.myshopify.com")

        self.assertEqual(response.status_code, 200)
        record = ShopConfig.objects.get(shop="test-shop")
        self.assertFalse(record.is_online)
        self.assertEqual(record.access_token, "new-access-token")
        self.assertEqual(record.scope, "write_products")
        self.assertEqual(record.refresh_token, "refresh-token")
        mocked_get_shopify_app.return_value.exchange_using_token_exchange.assert_called_once()

    @patch("shopify_requests.graphql_client.raw_admin_graphql")
    @patch("core.mixins.get_shopify_app")
    def test_refresh_updates_existing_token(self, mocked_get_shopify_app, mock_raw_gql):
        mock_raw_gql.return_value = SimpleNamespace(
            ok=True,
            shop="test-shop",
            data={"shop": {"id": "gid://shopify/Shop/1"}},
            extensions=None,
            log=SimpleNamespace(code="success", detail="ok"),
            response=SimpleNamespace(status=200, body="", headers={}),
        )
        ShopConfig.objects.create(
            shop="test-shop",
            is_online=False,
            access_token="stale-token",
            refresh_token="refresh-token",
        )
        mocked_get_shopify_app.return_value.verify_app_home_req.return_value = SimpleNamespace(
            ok=True,
            shop="test-shop",
            id_token=SimpleNamespace(
                exchangeable=True,
                token="jwt-token",
                claims={"dest": "https://test-shop.myshopify.com"},
            ),
            new_id_token_response=SimpleNamespace(status=401, body="", headers={}),
            response=SimpleNamespace(headers={}),
        )
        mocked_get_shopify_app.return_value.refresh_token_exchanged_access_token.return_value = (
            SimpleNamespace(
                ok=True,
                access_token=SimpleNamespace(
                    access_mode="offline",
                    shop="test-shop",
                    token="fresh-token",
                    scope="write_products",
                    expires="2027-03-01T00:00:00Z",
                    refresh_token="new-refresh-token",
                    refresh_token_expires="2027-04-01T00:00:00Z",
                ),
                log=SimpleNamespace(code="success", detail="ok"),
            )
        )

        response = self.client.get("/app/?shop=test-shop.myshopify.com")

        self.assertEqual(response.status_code, 200)
        record = ShopConfig.objects.get(shop="test-shop")
        self.assertEqual(record.access_token, "fresh-token")
        self.assertEqual(record.refresh_token, "new-refresh-token")
        mocked_get_shopify_app.return_value.refresh_token_exchanged_access_token.assert_called_once()
        mocked_get_shopify_app.return_value.exchange_using_token_exchange.assert_not_called()

    @patch("core.mixins.get_shopify_app")
    def test_refresh_failure_clears_tokens_and_returns_sdk_response(
        self, mocked_get_shopify_app
    ):
        ShopConfig.objects.create(
            shop="test-shop",
            is_online=False,
            access_token="stale-token",
            refresh_token="refresh-token",
        )
        mocked_get_shopify_app.return_value.verify_app_home_req.return_value = SimpleNamespace(
            ok=True,
            shop="test-shop",
            id_token=SimpleNamespace(
                exchangeable=True,
                token="jwt-token",
                claims={"dest": "https://test-shop.myshopify.com"},
            ),
            new_id_token_response=SimpleNamespace(status=401, body="", headers={}),
            response=SimpleNamespace(headers={}),
        )
        mocked_get_shopify_app.return_value.refresh_token_exchanged_access_token.return_value = (
            SimpleNamespace(
                ok=False,
                log=SimpleNamespace(code="invalid_subject_token", detail="invalid"),
                response=SimpleNamespace(
                    status=401,
                    body="Unauthorized",
                    headers={"X-Shopify-Retry-Invalid-Session-Request": "1"},
                ),
            )
        )

        response = self.client.get("/app/?shop=test-shop.myshopify.com")

        self.assertEqual(response.status_code, 401)
        record = ShopConfig.objects.get(shop="test-shop")
        self.assertIsNone(record.access_token)
        self.assertIsNone(record.refresh_token)


class EmbeddedRedirectValidationTests(TestCase):
    def test_validate_relative_rejects_protocol_relative(self):
        self.assertIsNotNone(validate_relative_app_path("//evil.com/x"))

    def test_validate_relative_accepts_app_path(self):
        self.assertIsNone(validate_relative_app_path("/app/extra"))

    @override_settings(SHOPIFY_APP_URL="https://trusted.example.com")
    def test_validate_parent_allows_configured_app_host(self):
        self.assertIsNone(
            validate_parent_redirect_url("https://trusted.example.com/settings")
        )

    @override_settings(SHOPIFY_APP_URL="https://trusted.example.com")
    def test_validate_parent_rejects_unknown_host(self):
        self.assertIsNotNone(
            validate_parent_redirect_url("https://malicious.example.net/phish")
        )


class EmbeddedRedirectViewTests(TestCase):
    @patch("core.mixins.get_shopify_app")
    def test_in_app_verify_failed_returns_sdk_response(self, mock_gs):
        mock_gs.return_value.verify_app_home_req.return_value = SimpleNamespace(
            ok=False,
            response=SimpleNamespace(
                status=302,
                body="",
                headers={"Location": "/core/auth/patch-id-token"},
            ),
            log=SimpleNamespace(code="redirect_to_patch_id_token_page", detail=""),
        )

        response = self.client.get(
            f"{reverse('core:auth-embedded-redirect')}?next=/app/extra"
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/core/auth/patch-id-token")

    @patch("core.mixins.get_shopify_app")
    def test_in_app_calls_sdk_with_next_and_shop(self, mock_gs):
        mock_app = mock_gs.return_value
        mock_app.verify_app_home_req.return_value = SimpleNamespace(
            ok=True,
            shop="test-shop",
            response=SimpleNamespace(headers={}),
            log=SimpleNamespace(code="verified", detail=""),
        )
        mock_app.app_home_redirect.return_value = SimpleNamespace(
            ok=True,
            response=SimpleNamespace(
                status=302,
                body="",
                headers={"Location": "/app/extra"},
            ),
            log=SimpleNamespace(code="app_home_redirect_success", detail=""),
        )

        response = self.client.get(
            f"{reverse('core:auth-embedded-redirect')}?next=/app/extra"
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/app/extra")
        mock_app.app_home_redirect.assert_called_once()
        self.assertEqual(
            mock_app.app_home_redirect.call_args[0][1], "/app/extra"
        )
        self.assertEqual(
            mock_app.app_home_redirect.call_args[0][2], "test-shop"
        )

    @patch("core.mixins.get_shopify_app")
    def test_in_app_invalid_next_returns_400_before_sdk_redirect(self, mock_gs):
        mock_gs.return_value.verify_app_home_req.return_value = SimpleNamespace(
            ok=True,
            shop="test-shop",
            response=SimpleNamespace(headers={}),
            log=SimpleNamespace(code="verified", detail=""),
        )

        response = self.client.get(
            f"{reverse('core:auth-embedded-redirect')}?next=//evil.com"
        )

        self.assertEqual(response.status_code, 400)
        mock_gs.return_value.app_home_redirect.assert_not_called()

    @override_settings(SHOPIFY_APP_URL="https://trusted.example.com")
    @patch("core.mixins.get_shopify_app")
    def test_parent_allowed_url_calls_sdk(self, mock_gs):
        mock_app = mock_gs.return_value
        mock_app.verify_app_home_req.return_value = SimpleNamespace(
            ok=True,
            shop="test-shop",
            response=SimpleNamespace(headers={}),
            log=SimpleNamespace(code="verified", detail=""),
        )
        mock_app.app_home_parent_redirect.return_value = SimpleNamespace(
            ok=True,
            response=SimpleNamespace(
                status=200,
                body="<html>ok</html>",
                headers={"Content-Type": "text/html"},
            ),
            log=SimpleNamespace(code="app_home_parent_redirect_success", detail=""),
        )

        target = "https://trusted.example.com/out"
        response = self.client.get(
            reverse("core:auth-embedded-parent-redirect"),
            {"url": target},
        )

        self.assertEqual(response.status_code, 200)
        mock_app.app_home_parent_redirect.assert_called_once()
        self.assertEqual(
            mock_app.app_home_parent_redirect.call_args[0][1], target
        )
        self.assertEqual(
            mock_app.app_home_parent_redirect.call_args[0][2], "test-shop"
        )

    @override_settings(SHOPIFY_APP_URL="https://trusted.example.com")
    @patch("core.mixins.get_shopify_app")
    def test_parent_disallowed_host_returns_400(self, mock_gs):
        mock_gs.return_value.verify_app_home_req.return_value = SimpleNamespace(
            ok=True,
            shop="test-shop",
            response=SimpleNamespace(headers={}),
            log=SimpleNamespace(code="verified", detail=""),
        )

        response = self.client.get(
            reverse("core:auth-embedded-parent-redirect"),
            {"url": "https://evil.example/not-allowed"},
        )

        self.assertEqual(response.status_code, 400)
        mock_gs.return_value.app_home_parent_redirect.assert_not_called()

    @override_settings(SHOPIFY_APP_URL="https://trusted.example.com")
    @patch("core.mixins.get_shopify_app")
    def test_parent_invalid_target_returns_400(self, mock_gs):
        mock_gs.return_value.verify_app_home_req.return_value = SimpleNamespace(
            ok=True,
            shop="test-shop",
            response=SimpleNamespace(headers={}),
            log=SimpleNamespace(code="verified", detail=""),
        )

        response = self.client.get(
            reverse("core:auth-embedded-parent-redirect"),
            {
                "url": "https://trusted.example.com/ok",
                "target": "_self",
            },
        )

        self.assertEqual(response.status_code, 400)
        mock_gs.return_value.app_home_parent_redirect.assert_not_called()

from types import SimpleNamespace
from unittest.mock import patch

from django.test import TestCase

from core.models import ShopConfig


class WebhookUninstalledTests(TestCase):
    @patch("webhooks.views.get_shopify_app")
    def test_invalid_hmac_returns_sdk_response(self, mock_get_app):
        mock_get_app.return_value.verify_webhook_req.return_value = SimpleNamespace(
            ok=False,
            response=SimpleNamespace(status=401, body="Unauthorized", headers={}),
            log=SimpleNamespace(code="invalid_hmac", detail="bad signature"),
        )

        response = self.client.post(
            "/webhooks/app/uninstalled",
            data=b"{}",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content.decode(), "Unauthorized")

    @patch("webhooks.views.get_shopify_app")
    def test_uninstalled_deletes_shop_config_by_short_shop(self, mock_get_app):
        ShopConfig.objects.create(shop="demo", is_online=False, access_token="tok")
        mock_get_app.return_value.verify_webhook_req.return_value = SimpleNamespace(
            ok=True,
            shop="demo.myshopify.com",
            response=SimpleNamespace(status=200, body="", headers={}),
            log=SimpleNamespace(code="verified", detail="ok"),
        )

        response = self.client.post(
            "/webhooks/app/uninstalled",
            data=b'{"id": 1}',
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(ShopConfig.objects.filter(shop="demo").exists())

    @patch("webhooks.views.get_shopify_app")
    def test_uninstalled_deletes_shop_config_by_full_domain_row(self, mock_get_app):
        ShopConfig.objects.create(
            shop="demo.myshopify.com", is_online=False, access_token="tok"
        )
        mock_get_app.return_value.verify_webhook_req.return_value = SimpleNamespace(
            ok=True,
            shop="demo.myshopify.com",
            response=SimpleNamespace(status=200, body="", headers={}),
            log=SimpleNamespace(code="verified", detail="ok"),
        )

        response = self.client.post(
            "/webhooks/app/uninstalled",
            data=b"{}",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(ShopConfig.objects.exists())


class WebhookScopesUpdateTests(TestCase):
    @patch("webhooks.views.get_shopify_app")
    def test_scopes_update_ok_returns_200(self, mock_get_app):
        mock_get_app.return_value.verify_webhook_req.return_value = SimpleNamespace(
            ok=True,
            shop="demo.myshopify.com",
            response=SimpleNamespace(status=200, body="", headers={}),
            log=SimpleNamespace(code="verified", detail="ok"),
        )

        response = self.client.post(
            "/webhooks/app/scopes_update",
            data=b'{"current":["read_products"]}',
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

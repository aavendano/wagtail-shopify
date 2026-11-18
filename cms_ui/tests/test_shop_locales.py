from unittest.mock import patch

from django.test import TestCase, override_settings

from core.models import ShopConfig
from cms_ui.shop_locales import (
    _parse_shop_locales,
    fetch_shop_spa_locales,
)


class ShopLocalesParseTests(TestCase):
    def test_only_mapped_and_published(self):
        payload = _parse_shop_locales(
            {
                "shopLocales": [
                    {"locale": "en", "primary": True, "published": True, "name": "English"},
                    {"locale": "es", "primary": False, "published": True, "name": "Spanish"},
                    {"locale": "ja", "primary": False, "published": True, "name": "Japanese"},
                ]
            }
        )
        codes = {row["code"] for row in payload["availableLocales"]}
        self.assertEqual(codes, {"en-US", "es-US"})
        self.assertEqual(payload["primaryLocale"], "en-US")


@override_settings(LANGUAGE_CODE="en-US")
class ShopLocalesFetchTests(TestCase):
    def setUp(self):
        self.config = ShopConfig.objects.create(
            shop="test-shop.myshopify.com",
            access_token="tok",
        )

    @patch("cms_ui.shop_locales.execute_admin_graphql")
    def test_fetch_caches_two_locales(self, mock_graphql):
        mock_graphql.return_value = type(
            "R",
            (),
            {
                "ok": True,
                "data": {
                    "shopLocales": [
                        {"locale": "en", "primary": True, "published": True, "name": "English"},
                        {"locale": "es", "primary": False, "published": True, "name": "Español"},
                    ]
                },
                "error_code": None,
                "log_detail": "",
            },
        )()

        payload = fetch_shop_spa_locales(force_refresh=True)
        self.assertEqual(len(payload["availableLocales"]), 2)
        self.assertEqual(payload["primaryLocale"], "en-US")
        self.config.refresh_from_db()
        self.assertEqual(len(self.config.cached_spa_locales), 2)
        mock_graphql.assert_called_once()

    @patch("cms_ui.shop_locales.execute_admin_graphql")
    def test_api_failure_uses_stale_cache(self, mock_graphql):
        self.config.cached_spa_locales = [
            {"code": "en-US", "label": "English (United States)", "primary": True},
        ]
        self.config.cached_spa_primary_locale = "en-US"
        self.config.save()
        mock_graphql.return_value = type(
            "R",
            (),
            {
                "ok": False,
                "data": None,
                "error_code": "throttled",
                "log_detail": "slow down",
            },
        )()

        payload = fetch_shop_spa_locales(force_refresh=True)
        self.assertEqual(payload["source"], "stale_cache")
        self.assertEqual(payload["primaryLocale"], "en-US")

    @patch("cms_ui.shop_locales.execute_admin_graphql")
    def test_api_failure_without_cache_falls_back(self, mock_graphql):
        mock_graphql.return_value = type(
            "R",
            (),
            {"ok": False, "data": None, "error_code": "error", "log_detail": "boom"},
        )()
        payload = fetch_shop_spa_locales(force_refresh=True)
        self.assertEqual(payload["source"], "fallback")
        self.assertIn(
            "en-US",
            [row["code"] for row in payload["availableLocales"]],
        )

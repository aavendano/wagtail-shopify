from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings

from cms_ui.models import CmsSpaMount, default_cms_layout

User = get_user_model()


def _shop_locales_stub():
    return {
        "primaryLocale": "es-US",
        "availableLocales": [
            {"code": "en-US", "label": "English (United States)", "primary": False},
            {"code": "es-US", "label": "Spanish (United States)", "primary": True},
        ],
        "source": "shop",
    }


@override_settings(SHOPIFY_API_KEY="test-key", SHOPIFY_API_SECRET="test-secret")
class CmsSpaLocaleBootstrapTests(TestCase):
    def setUp(self):
        CmsSpaMount.objects.create(
            slug="cms",
            title="Merchant CMS",
            url_prefix="cms",
            layout=default_cms_layout(),
        )
        self.user = User.objects.create_user(
            username="editor",
            password="pass",
            is_staff=True,
        )

    @patch("cms_ui.models.fetch_shop_spa_locales", return_value=_shop_locales_stub())
    def test_bootstrap_includes_store_locales(self, _mock):
        client = Client()
        client.force_login(self.user)
        response = client.get("/cms/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"primaryLocale": "es-US"')
        self.assertContains(response, '"availableLocales"')
        self.assertContains(response, '"setLanguageUrl"')

    @patch("cms_ui.spa_locale.fetch_shop_spa_locales", return_value=_shop_locales_stub())
    @patch("cms_ui.models.fetch_shop_spa_locales", return_value=_shop_locales_stub())
    def test_default_language_is_shop_primary_without_cookie(self, _m1, _m2):
        client = Client()
        client.force_login(self.user)
        response = client.get("/cms/")
        self.assertIn(b'"language": "es-US"', response.content)

    @patch("cms_ui.spa_locale.fetch_shop_spa_locales", return_value=_shop_locales_stub())
    @patch("cms_ui.models.fetch_shop_spa_locales", return_value=_shop_locales_stub())
    def test_user_cookie_overrides_primary(self, _m1, _m2):
        client = Client()
        client.cookies["cms_ui_locale"] = "en-US"
        client.force_login(self.user)
        response = client.get("/cms/")
        self.assertContains(response, '"language": "en-US"')

    @patch("cms_ui.views.fetch_shop_spa_locales", return_value=_shop_locales_stub())
    def test_set_language_persists_cookie(self, _mock):
        client = Client()
        client.force_login(self.user)
        response = client.post(
            "/cms/set-language/",
            data='{"language": "es-US"}',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.cookies["cms_ui_locale"].value, "es-US")

    @patch("cms_ui.views.fetch_shop_spa_locales", return_value=_shop_locales_stub())
    def test_set_language_rejects_disabled_locale(self, _mock):
        client = Client()
        client.force_login(self.user)
        response = client.post(
            "/cms/set-language/",
            data='{"language": "fr-CA"}',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

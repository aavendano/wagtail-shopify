from django.test import SimpleTestCase

from cms_ui.locale_mapping import shopify_locale_to_wagtail


class LocaleMappingTests(SimpleTestCase):
    def test_iso639_maps_to_wagtail(self):
        self.assertEqual(shopify_locale_to_wagtail("en"), "en-US")
        self.assertEqual(shopify_locale_to_wagtail("es"), "es-US")
        self.assertEqual(shopify_locale_to_wagtail("fr"), "fr-CA")

    def test_regional_tags(self):
        self.assertEqual(shopify_locale_to_wagtail("en-CA"), "en-CA")
        self.assertEqual(shopify_locale_to_wagtail("es-US"), "es-US")

    def test_unknown_returns_none(self):
        self.assertIsNone(shopify_locale_to_wagtail("de"))

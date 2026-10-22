from django.test import SimpleTestCase

from shopify_content.shopify_languages import (
    shopify_country,
    shopify_language,
    shopify_market,
    shopify_translation_language,
)
from shopify_content.sync.outbound import _wagtail_locale_to_shopify


class ShopifyLanguagesTests(SimpleTestCase):
    """Shopify languages are en (primary), es and fr; markets are ca and usa."""

    def test_language_is_the_shopify_language_not_the_market_locale(self):
        self.assertEqual(
            {code: shopify_language(code) for code in ('en-US', 'es-US', 'en-CA', 'fr-CA')},
            {'en-US': 'en', 'es-US': 'es', 'en-CA': 'en', 'fr-CA': 'fr'},
        )

    def test_market_and_country(self):
        self.assertEqual(shopify_market('en-US'), 'usa')
        self.assertEqual(shopify_market('fr-CA'), 'ca')
        self.assertEqual(shopify_country('es-US'), 'United States')
        self.assertEqual(shopify_country('en-CA'), 'Canada')
        self.assertIsNone(shopify_market('de-DE'))

    def test_only_es_and_fr_are_translations(self):
        self.assertIsNone(shopify_translation_language('en-US'), 'primary language')
        self.assertIsNone(shopify_translation_language('en-CA'), 'shares the primary language')
        self.assertEqual(shopify_translation_language('es-US'), 'es')
        self.assertEqual(shopify_translation_language('fr-CA'), 'fr')

    def test_translations_register_uses_shopify_languages(self):
        self.assertEqual(_wagtail_locale_to_shopify('fr-CA'), 'fr', 'not the invalid "fr-CA"')
        self.assertIsNone(_wagtail_locale_to_shopify('en-CA'), 'not the invalid "en-CA"')
        self.assertEqual(_wagtail_locale_to_shopify('es-US'), 'es')
        self.assertIsNone(_wagtail_locale_to_shopify('en-US'))

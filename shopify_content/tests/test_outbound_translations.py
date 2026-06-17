import uuid
from unittest.mock import patch

from django.test import TestCase
from wagtail.models import Locale, Page

from core.models import ShopConfig
from shopify_content.models import ProductPage, ShopifyRootPage
from shopify_content.sync.outbound import (
    PRIMARY_LOCALE,
    _resolve_primary_page,
    sync_product_page,
)
from shopify_requests.graphql_service import AdminGraphqlResult


def _graphql_ok(shop, data):
    return AdminGraphqlResult(
        ok=True,
        shop=shop,
        data=data,
        extensions=None,
        error_code=None,
        log_detail='',
        reauthorization_required=False,
        retryable=False,
        raw=None,
    )


class OutboundPrimaryLocaleTests(TestCase):
    def setUp(self):
        ShopConfig.objects.create(shop='test-shop.myshopify.com', access_token='tok')
        self.en_locale = Locale.get_default()
        self.es_locale, _ = Locale.objects.get_or_create(language_code='es-US')

        home = Page.objects.first()
        if home is None:
            home = Page.add_root(
                instance=Page(title='Home', slug='home', locale=self.en_locale),
            )
        self.parent = ShopifyRootPage(title='Root', slug='root', locale=self.en_locale)
        home.add_child(instance=self.parent)
        self.parent.save_revision().publish()

        self.translation_key = uuid.uuid4()
        self.shopify_id = 'gid://shopify/Product/999'

        self.en_product = ProductPage(
            title='English Title',
            slug='product-en',
            locale=self.en_locale,
            translation_key=self.translation_key,
            shopify_id=self.shopify_id,
            sync_enabled=True,
        )
        self.parent.add_child(instance=self.en_product)
        self.en_product.save_revision().publish()

        self.es_product = ProductPage(
            title='Título Español',
            slug='product-es',
            locale=self.es_locale,
            translation_key=self.translation_key,
            shopify_id=self.shopify_id,
            sync_enabled=True,
        )
        self.parent.add_child(instance=self.es_product)
        self.es_product.save_revision().publish()

    def test_resolve_primary_page_from_translation(self):
        primary = _resolve_primary_page(self.es_product.specific)
        self.assertEqual(primary.pk, self.en_product.pk)
        self.assertEqual(primary.title, 'English Title')

    def test_resolve_primary_page_when_already_primary(self):
        primary = _resolve_primary_page(self.en_product.specific)
        self.assertEqual(primary.pk, self.en_product.pk)

    def test_resolve_primary_page_fallback_without_en_us_sibling(self):
        solo_key = uuid.uuid4()
        solo_es = ProductPage(
            title='Solo ES',
            slug='solo-es',
            locale=self.es_locale,
            translation_key=solo_key,
            shopify_id='gid://shopify/Product/1000',
            sync_enabled=True,
        )
        self.parent.add_child(instance=solo_es)
        solo_es.save_revision().publish()

        primary = _resolve_primary_page(solo_es.specific)
        self.assertEqual(primary.pk, solo_es.pk)
        self.assertEqual(primary.title, 'Solo ES')

    @patch('shopify_content.sync.outbound.execute_admin_graphql')
    def test_sync_from_es_us_pushes_en_us_primary_and_registers_es(self, mock_graphql):
        product_updates = []
        translation_calls = []

        def side_effect(query, shop, variables=None, **kwargs):
            if 'productUpdate' in query:
                product_updates.append(variables)
                return _graphql_ok(shop, {'productUpdate': {'userErrors': []}})
            if 'translationsRegister' in query:
                translation_calls.append(variables)
                return _graphql_ok(shop, {'translationsRegister': {'userErrors': []}})
            if 'metafieldsSet' in query:
                return _graphql_ok(shop, {'metafieldsSet': {'userErrors': []}})
            raise AssertionError(f'Unexpected GraphQL query: {query[:80]}')

        mock_graphql.side_effect = side_effect

        success = sync_product_page(self.es_product.specific)

        self.assertTrue(success)
        self.assertEqual(len(product_updates), 1)
        self.assertEqual(product_updates[0]['input']['title'], 'English Title')
        self.assertNotEqual(product_updates[0]['input']['title'], 'Título Español')

        self.assertEqual(len(translation_calls), 1)
        translations = translation_calls[0]['translations']
        self.assertEqual(len(translations), 1)
        self.assertEqual(translations[0]['locale'], 'es')
        self.assertEqual(translations[0]['key'], 'title')
        self.assertEqual(translations[0]['value'], 'Título Español')

    @patch('shopify_content.sync.outbound.execute_admin_graphql')
    def test_sync_from_en_us_registers_sibling_locales(self, mock_graphql):
        translation_calls = []

        def side_effect(query, shop, variables=None, **kwargs):
            if 'productUpdate' in query:
                return _graphql_ok(shop, {'productUpdate': {'userErrors': []}})
            if 'translationsRegister' in query:
                translation_calls.append(variables)
                return _graphql_ok(shop, {'translationsRegister': {'userErrors': []}})
            if 'metafieldsSet' in query:
                return _graphql_ok(shop, {'metafieldsSet': {'userErrors': []}})
            raise AssertionError(f'Unexpected GraphQL query: {query[:80]}')

        mock_graphql.side_effect = side_effect

        success = sync_product_page(self.en_product.specific)

        self.assertTrue(success)
        self.assertEqual(len(translation_calls), 1)
        locales = {t['locale'] for t in translation_calls[0]['translations']}
        self.assertIn('es', locales)
        self.assertNotIn(PRIMARY_LOCALE, locales)

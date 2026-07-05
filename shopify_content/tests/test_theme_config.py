import json
from unittest.mock import patch

from django.test import TestCase
from wagtail.models import Locale, Page

from core.models import ShopConfig
from shopify_content.models import CollectionPage, ProductPage, ShopifyRootPage
from shopify_content.sync.outbound import sync_collection_page, sync_product_page
from shopify_content.sync.theme_config import collect_theme_config_metafield_inputs


class ThemeConfigTests(TestCase):
    def test_collect_theme_config_metafield_inputs(self):
        page = ProductPage(theme_config={
            'metafields': [
                {
                    'namespace': 'custom',
                    'key': 'hero_blocks',
                    'type': 'json',
                    'value': '{"blocks":[]}',
                },
            ],
        })
        inputs = collect_theme_config_metafield_inputs(page, 'gid://shopify/Product/1')

        self.assertEqual(len(inputs), 1)
        self.assertEqual(inputs[0]['ownerId'], 'gid://shopify/Product/1')
        self.assertEqual(inputs[0]['key'], 'hero_blocks')
        self.assertEqual(inputs[0]['type'], 'json')

    def test_collect_skips_invalid_entries(self):
        page = ProductPage(theme_config={'metafields': [{'key': ''}, {'value': 'x'}]})
        self.assertEqual(collect_theme_config_metafield_inputs(page, 'gid://1'), [])


class SyncThemeConfigTests(TestCase):
    def setUp(self):
        ShopConfig.objects.create(shop='test-shop.myshopify.com', access_token='tok')
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.root = ShopifyRootPage(title='Root', slug='root', locale=locale)
        home.add_child(instance=self.root)
        self.root.save_revision().publish()

    @patch('shopify_content.sync.outbound._register_shopify_translations')
    @patch('shopify_content.sync.outbound._push_hreflang_metafields', return_value=None)
    @patch('shopify_content.sync.outbound._push_native_reference_metafields', return_value=True)
    @patch('shopify_content.sync.outbound._push_internal_links_metafield', return_value=True)
    @patch('shopify_content.sync.outbound._push_faq_metafield', return_value=True)
    @patch('shopify_content.sync.outbound._push_metafields', return_value=True)
    @patch('shopify_content.sync.outbound.execute_admin_graphql')
    def test_sync_product_page_pushes_theme_config(
        self, mock_graphql, mock_push, *_mocks,
    ):
        mock_graphql.return_value.ok = True
        mock_graphql.return_value.data = {'productUpdate': {'userErrors': []}}

        product = ProductPage(
            title='Widget',
            slug='widget',
            handle='widget',
            shopify_id='gid://shopify/Product/100',
            sync_enabled=True,
            theme_config={
                'metafields': [
                    {
                        'key': 'theme_layout',
                        'type': 'single_line_text_field',
                        'value': 'wide',
                    },
                ],
            },
            locale=Locale.get_default(),
        )
        self.root.add_child(instance=product)
        product.save_revision().publish()

        sync_product_page(product)

        self.assertGreaterEqual(mock_push.call_count, 2)
        theme_call = mock_push.call_args_list[-1]
        inputs = theme_call.args[1]
        self.assertEqual(inputs[0]['key'], 'theme_layout')
        self.assertEqual(inputs[0]['value'], 'wide')

    @patch('shopify_content.sync.outbound._register_shopify_translations')
    @patch('shopify_content.sync.outbound._push_hreflang_metafields', return_value=None)
    @patch('shopify_content.sync.outbound._push_native_reference_metafields', return_value=True)
    @patch('shopify_content.sync.outbound._push_internal_links_metafield', return_value=True)
    @patch('shopify_content.sync.outbound._push_faq_metafield', return_value=True)
    @patch('shopify_content.sync.outbound._push_metafields', return_value=True)
    @patch('shopify_content.sync.outbound.execute_admin_graphql')
    def test_sync_collection_page_pushes_theme_config(
        self, mock_graphql, mock_push, *_mocks,
    ):
        mock_graphql.return_value.ok = True
        mock_graphql.return_value.data = {'collectionUpdate': {'userErrors': []}}

        collection = CollectionPage(
            title='Summer',
            slug='summer',
            handle='summer',
            shopify_id='gid://shopify/Collection/200',
            sync_enabled=True,
            theme_config={
                'metafields': [
                    {
                        'key': 'banner_json',
                        'type': 'json',
                        'value': json.dumps({'title': 'Sale'}),
                    },
                ],
            },
            locale=Locale.get_default(),
        )
        self.root.add_child(instance=collection)
        collection.save_revision().publish()

        sync_collection_page(collection)

        theme_call = mock_push.call_args_list[-1]
        inputs = theme_call.args[1]
        self.assertEqual(inputs[0]['key'], 'banner_json')

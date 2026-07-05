from unittest.mock import MagicMock, patch

from django.test import TestCase
from wagtail.models import Locale, Page

from core.models import ShopConfig
from shopify_content.models import ShopifyRootPage
from shopify_content.sync.import_parents import resource_type_for_root_slug
from shopify_content.sync.outbound import (
    _root_page_definition,
    ensure_root_page_definition,
    sync_shopify_root_page,
)
from metaobjects.shopify_metaobjects.metaobject import Metaobject


class RootPageDefinitionTests(TestCase):
    def test_definition_includes_core_fields(self):
        spec = _root_page_definition()
        field_keys = {field.key for field in spec.fields}
        self.assertEqual(spec.type, 'root_page')
        self.assertEqual(spec.display_name_field, 'title')
        self.assertEqual(
            field_keys,
            {'title', 'slug', 'resource_type', 'config', 'meta_title', 'meta_description'},
        )
        self.assertNotIn('onlineStore', spec.capabilities or {})

    def test_resource_type_mapping(self):
        self.assertEqual(resource_type_for_root_slug('glossary'), 'glossary')
        self.assertEqual(resource_type_for_root_slug('root'), 'products')
        self.assertEqual(resource_type_for_root_slug('unknown'), 'unknown')


class EnsureRootPageDefinitionTests(TestCase):
    def test_ensure_calls_client(self):
        client = MagicMock()
        client.ensure_definition.return_value = MagicMock(type='root_page', id='gid://def/1')
        result = ensure_root_page_definition(client)
        client.ensure_definition.assert_called_once()
        self.assertEqual(result.type, 'root_page')


class SyncShopifyRootPageTests(TestCase):
    def setUp(self):
        ShopConfig.objects.create(shop='test-shop.myshopify.com', access_token='tok')
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.parent = ShopifyRootPage(title='Site Root', slug='site-root', locale=locale)
        home.add_child(instance=self.parent)
        self.parent.save_revision().publish()

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_sync_includes_config_and_resource_type(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.sync.return_value = Metaobject(
            type='root_page',
            handle='glossary',
            id='gid://shopify/Metaobject/10',
        )
        mock_client_cls.return_value = mock_client

        export_config = {
            'glossary_index': {
                'enabled': True,
                'pages': {'en': 'gid://shopify/Page/1'},
            },
        }
        page = ShopifyRootPage(
            title='Glossary',
            slug='glossary',
            handle='glossary',
            export_config=export_config,
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()

        success, message = sync_shopify_root_page(page)

        self.assertTrue(success)
        self.assertIn('successfully', message)
        data = mock_client.sync.call_args.args[0]
        self.assertEqual(data['title'], 'Glossary')
        self.assertEqual(data['slug'], 'glossary')
        self.assertEqual(data['resource_type'], 'glossary')
        self.assertEqual(data['config'], export_config)
        self.assertEqual(data['meta_title'], 'Glossary')

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_sync_skipped_when_disabled(self, mock_client_cls):
        page = ShopifyRootPage(
            title='Glossary',
            slug='glossary',
            sync_enabled=False,
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()

        success, message = sync_shopify_root_page(page)

        self.assertFalse(success)
        self.assertIn('disabled', message)
        mock_client_cls.assert_not_called()

from unittest.mock import MagicMock, patch

from django.test import TestCase
from wagtail.models import Locale, Page

from core.models import ShopConfig
from shopify_content.models import GlossaryTermPage, ShopifyRootPage
from shopify_content.sync.outbound import _glossary_term_definition, sync_glossary_term_page
from metaobjects.shopify_metaobjects.metaobject import Metaobject


class GlossaryTermDefinitionTests(TestCase):
    def test_definition_includes_fields_and_renderable_keys(self):
        spec = _glossary_term_definition()
        field_keys = {field.key for field in spec.fields}
        self.assertEqual(spec.display_name_field, 'term')
        self.assertEqual(
            field_keys,
            {'term', 'definition', 'locale', 'related_links', 'external_links'},
        )

        renderable = spec.capabilities['renderable']['data']
        self.assertEqual(renderable['metaTitleKey'], 'term')
        self.assertEqual(renderable['metaDescriptionKey'], 'definition')

        online_store = spec.capabilities['onlineStore']['data']
        self.assertEqual(online_store['urlHandle'], 'glossary')

        payload = spec.to_shopify_input()
        renderable_data = payload['capabilities']['renderable']['data']
        self.assertEqual(renderable_data['metaTitleKey'], 'term')
        self.assertEqual(renderable_data['metaDescriptionKey'], 'definition')


class SyncGlossaryTermPageTests(TestCase):
    def setUp(self):
        ShopConfig.objects.create(shop='test-shop.myshopify.com', access_token='tok')
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.parent = ShopifyRootPage(title='Glossary', slug='glossary', locale=locale)
        home.add_child(instance=self.parent)
        self.parent.save_revision().publish()

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_sync_includes_core_fields(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.sync.return_value = Metaobject(
            type='glossary_term',
            handle='vibrator',
            id='gid://shopify/Metaobject/1',
        )
        mock_client_cls.return_value = mock_client

        page = GlossaryTermPage(
            title='Vibrator',
            term='Vibrator',
            definition='<p>A device that vibrates.</p>',
            locale_code='en',
            slug='vibrator',
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()

        success, message = sync_glossary_term_page(page)

        self.assertTrue(success)
        self.assertIn('successfully', message)
        mock_client.sync.assert_called_once()
        data = mock_client.sync.call_args.args[0]
        self.assertEqual(data['term'], 'Vibrator')
        self.assertEqual(data['locale'], 'en')
        self.assertEqual(data['definition'], '<p>A device that vibrates.</p>')

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_handle_defaults_to_slugified_term(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.sync.return_value = Metaobject(
            type='glossary_term',
            handle='satisfyer-pro-2',
            id='gid://shopify/Metaobject/2',
        )
        mock_client_cls.return_value = mock_client

        page = GlossaryTermPage(
            title='Satisfyer Pro 2',
            term='Satisfyer Pro 2',
            locale_code='en',
            slug='satisfyer-pro-2',
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()

        success, _ = sync_glossary_term_page(page)

        self.assertTrue(success)
        data = mock_client.sync.call_args.args[0]
        self.assertEqual(data['handle'], 'satisfyer-pro-2')

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_sync_includes_json_links_when_present(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.sync.return_value = Metaobject(
            type='glossary_term',
            handle='term-with-links',
            id='gid://shopify/Metaobject/3',
        )
        mock_client_cls.return_value = mock_client

        related_links = [{
            'type': 'product',
            'handle': 'satisfyer-pro-2',
            'label': 'Satisfyer Pro 2',
        }]
        external_links = [{
            'url': 'https://example.com/fda',
            'label': 'FDA Guidelines on Materials',
        }]
        page = GlossaryTermPage(
            title='Term With Links',
            term='Term With Links',
            locale_code='es',
            related_links=related_links,
            external_links=external_links,
            slug='term-with-links',
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()

        success, _ = sync_glossary_term_page(page)

        self.assertTrue(success)
        data = mock_client.sync.call_args.args[0]
        self.assertEqual(data['related_links'], related_links)
        self.assertEqual(data['external_links'], external_links)

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_sync_skips_empty_json_fields(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.sync.return_value = Metaobject(
            type='glossary_term',
            handle='plain-term',
            id='gid://shopify/Metaobject/4',
        )
        mock_client_cls.return_value = mock_client

        page = GlossaryTermPage(
            title='Plain Term',
            term='Plain Term',
            locale_code='fr',
            slug='plain-term',
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()

        success, _ = sync_glossary_term_page(page)

        self.assertTrue(success)
        data = mock_client.sync.call_args.args[0]
        self.assertNotIn('related_links', data)
        self.assertNotIn('external_links', data)

    def test_sync_aborts_without_term(self):
        page = GlossaryTermPage(
            title='Placeholder',
            term='Placeholder',
            slug='empty-term',
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()
        page.term = ''

        success, message = sync_glossary_term_page(page)

        self.assertFalse(success)
        self.assertIn('term is required', message)

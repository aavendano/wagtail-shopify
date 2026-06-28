from unittest.mock import MagicMock, patch

from django.test import TestCase
from wagtail.models import Locale, Page

from core.models import ShopConfig
from shopify_content.models import LocationPage, ShopifyRootPage
from shopify_content.sync.outbound import _location_page_definition, sync_location_page
from metaobjects.shopify_metaobjects.metaobject import Metaobject


class LocationPageDefinitionSeoTests(TestCase):
    def test_definition_includes_seo_fields_and_renderable_keys(self):
        spec = _location_page_definition()
        field_keys = {field.key for field in spec.fields}
        self.assertIn('meta_titulo', field_keys)
        self.assertIn('meta_descripcion', field_keys)
        self.assertIn('slug', field_keys)

        renderable = spec.capabilities['renderable']['data']
        self.assertEqual(renderable['metaTitleKey'], 'meta_titulo')
        self.assertEqual(renderable['metaDescriptionKey'], 'meta_descripcion')

        payload = spec.to_shopify_input()
        renderable_data = payload['capabilities']['renderable']['data']
        self.assertEqual(renderable_data['metaTitleKey'], 'meta_titulo')
        self.assertEqual(renderable_data['metaDescriptionKey'], 'meta_descripcion')


class SyncLocationPageSeoTests(TestCase):
    def setUp(self):
        ShopConfig.objects.create(shop='test-shop.myshopify.com', access_token='tok')
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.parent = ShopifyRootPage(title='Root', slug='root', locale=locale)
        home.add_child(instance=self.parent)
        self.parent.save_revision().publish()

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_sync_includes_seo_fields_in_metaobject_data(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.sync.return_value = Metaobject(
            type='local_page',
            handle='en-us-austin',
            id='gid://shopify/Metaobject/1',
        )
        mock_client_cls.return_value = mock_client

        page = LocationPage(
            title='Austin',
            titulo='Austin',
            city='Austin',
            state='Texas',
            slug='en-us-austin-texas',
            handle='en-us-austin-texas',
            locale=Locale.get_default(),
            seo_title='Austin SEO Title',
            search_description='Austin meta description',
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()

        success, message = sync_location_page(page)

        self.assertTrue(success)
        mock_client.sync.assert_called_once()
        data = mock_client.sync.call_args.kwargs['data']
        self.assertEqual(data['meta_titulo'], 'Austin SEO Title')
        self.assertEqual(data['meta_descripcion'], 'Austin meta description')
        self.assertEqual(data['handle'], 'en-us-austin-texas')
        self.assertEqual(data['slug'], 'en-us-austin-texas')
        self.assertIsNone(mock_client.sync.call_args.kwargs['existing_id'])

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_sync_updates_existing_metaobject_when_handle_changes(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.sync.return_value = Metaobject(
            type='local_page',
            handle='en-us-austin',
            id='gid://shopify/Metaobject/1',
        )
        mock_client_cls.return_value = mock_client

        page = LocationPage(
            title='Austin',
            titulo='Austin',
            city='Austin',
            slug='austin',
            handle='austin',
            shopify_id='gid://shopify/Metaobject/1',
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()

        success, _ = sync_location_page(page)

        self.assertTrue(success)
        kwargs = mock_client.sync.call_args.kwargs
        self.assertEqual(kwargs['existing_id'], 'gid://shopify/Metaobject/1')
        self.assertEqual(kwargs['data']['handle'], 'en-us-austin')

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_sync_resolves_legacy_handle_without_shopify_id(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.get_by_handle.return_value = Metaobject(
            type='local_page',
            handle='austin',
            id='gid://shopify/Metaobject/42',
        )
        mock_client.sync.return_value = Metaobject(
            type='local_page',
            handle='en-us-austin',
            id='gid://shopify/Metaobject/42',
        )
        mock_client_cls.return_value = mock_client

        page = LocationPage(
            title='Austin',
            titulo='Austin',
            city='Austin',
            slug='austin',
            handle='austin',
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()

        success, _ = sync_location_page(page)

        self.assertTrue(success)
        mock_client.get_by_handle.assert_called_once_with('local_page', 'austin')
        self.assertEqual(
            mock_client.sync.call_args.kwargs['existing_id'],
            'gid://shopify/Metaobject/42',
        )

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_sync_fails_without_city(self, mock_client_cls):
        page = LocationPage(
            title='Austin',
            titulo='Austin',
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()

        success, message = sync_location_page(page)

        self.assertFalse(success)
        self.assertIn('city and locale', message)
        mock_client_cls.return_value.sync.assert_not_called()

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_sync_falls_back_to_hero_fields_for_seo(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.sync.return_value = Metaobject(
            type='local_page',
            handle='en-us-denver',
            id='gid://shopify/Metaobject/2',
        )
        mock_client_cls.return_value = mock_client

        page = LocationPage(
            title='Denver',
            titulo='Denver',
            subtitulo='Colorado location',
            city='Denver',
            state='Colorado',
            slug='en-us-denver-colorado',
            handle='en-us-denver-colorado',
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()

        success, _ = sync_location_page(page)

        self.assertTrue(success)
        data = mock_client.sync.call_args.kwargs['data']
        self.assertEqual(data['meta_titulo'], 'Denver')
        self.assertEqual(data['meta_descripcion'], 'Colorado location')

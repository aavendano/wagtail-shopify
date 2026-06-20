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
            handle='austin',
            id='gid://shopify/Metaobject/1',
        )
        mock_client_cls.return_value = mock_client

        page = LocationPage(
            title='Austin',
            titulo='Austin',
            slug='austin',
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

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_sync_falls_back_to_hero_fields_for_seo(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.sync.return_value = Metaobject(
            type='local_page',
            handle='denver',
            id='gid://shopify/Metaobject/2',
        )
        mock_client_cls.return_value = mock_client

        page = LocationPage(
            title='Denver',
            titulo='Denver',
            subtitulo='Colorado location',
            slug='denver',
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()

        success, _ = sync_location_page(page)

        self.assertTrue(success)
        data = mock_client.sync.call_args.kwargs['data']
        self.assertEqual(data['meta_titulo'], 'Denver')
        self.assertEqual(data['meta_descripcion'], 'Colorado location')

from unittest.mock import MagicMock, patch

from django.test import TestCase
from wagtail.models import Locale, Page

from core.models import ShopConfig
from shopify_content.models import HomePage, ShopifyRootPage
from shopify_content.home_slug import home_page_handle
from shopify_content.sync.outbound import _home_page_definition, sync_home_page
from shopify_content.sync.publish_sync import is_syncable_page, queue_shopify_sync_on_publish
from metaobjects.shopify_metaobjects.metaobject import Metaobject


class HomePageDefinitionTests(TestCase):
    def test_definition_includes_hero_and_seo_fields(self):
        spec = _home_page_definition()
        field_keys = {field.key for field in spec.fields}
        self.assertIn('hero_heading', field_keys)
        self.assertIn('hero_eyebrow', field_keys)
        self.assertIn('sections_json', field_keys)
        self.assertIn('meta_titulo', field_keys)
        self.assertIn('meta_descripcion', field_keys)

        renderable = spec.capabilities['renderable']['data']
        self.assertEqual(renderable['metaTitleKey'], 'meta_titulo')
        self.assertEqual(renderable['metaDescriptionKey'], 'meta_descripcion')


class HomePageHandleTests(TestCase):
    def test_handle_from_wagtail_locale(self):
        page = HomePage(
            hero_heading='Shop Bold.',
            locale=Locale.objects.get_or_create(language_code='es-US')[0],
        )
        self.assertEqual(home_page_handle(page), 'home-es-us')


class SyncHomePageTests(TestCase):
    def setUp(self):
        ShopConfig.objects.create(shop='test-shop.myshopify.com', access_token='tok')
        locale = Locale.get_default()
        site_root = Page.get_first_root_node()
        if site_root is None:
            site_root = Page.add_root(instance=Page(title='Site Home', slug='site-home', locale=locale))

        self.parent = ShopifyRootPage.objects.filter(slug='cms-home').first()
        if self.parent is None:
            self.parent = ShopifyRootPage(title='CMS Home', slug='cms-home', locale=locale)
            site_root.add_child(instance=self.parent)
            self.parent.save_revision().publish()

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_sync_includes_hero_and_seo_fields(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.sync.return_value = Metaobject(
            type='home_page',
            handle='home-en-us',
            id='gid://shopify/Metaobject/99',
        )
        mock_client_cls.return_value = mock_client

        page = HomePage(
            title='Shop Bold.',
            hero_eyebrow='PlayLoveToys',
            hero_heading='Shop Bold.',
            hero_subheading='Curated products.',
            slug='home-en-us',
            handle='home-en-us',
            locale=Locale.get_default(),
            seo_title='Home SEO',
            search_description='Home meta description',
            sections_json={
                'version': 1,
                'sections': [
                    {
                        'type': 'trust_bar',
                        'id': 'trust-1',
                        'value': {
                            'items': [
                                {'icon': 'lock', 'title': 'Secure', 'description': 'Encrypted'},
                            ],
                        },
                    },
                ],
            },
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()

        success, message = sync_home_page(page)

        self.assertTrue(success)
        mock_client.sync.assert_called_once()
        data = mock_client.sync.call_args.args[0]
        self.assertEqual(data['hero_heading'], 'Shop Bold.')
        self.assertEqual(data['hero_eyebrow'], 'PlayLoveToys')
        self.assertEqual(data['hero_subheading'], 'Curated products.')
        self.assertEqual(data['sections_json']['version'], 1)
        self.assertEqual(data['meta_titulo'], 'Home SEO')
        self.assertEqual(data['meta_descripcion'], 'Home meta description')
        self.assertEqual(data['handle'], 'home-en-us')
        self.assertEqual(data['locale'], 'en-US')

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_sync_disabled_returns_false(self, mock_client_cls):
        page = HomePage(
            title='Shop Bold.',
            hero_heading='Shop Bold.',
            locale=Locale.get_default(),
            sync_enabled=False,
        )
        self.parent.add_child(instance=page)

        success, message = sync_home_page(page)

        self.assertFalse(success)
        mock_client_cls.return_value.sync.assert_not_called()


class HomePagePublishSyncTests(TestCase):
    def setUp(self):
        locale = Locale.get_default()
        site_root = Page.get_first_root_node()
        if site_root is None:
            site_root = Page.add_root(instance=Page(title='Site Home', slug='site-home', locale=locale))

        self.parent = ShopifyRootPage.objects.filter(slug='cms-home').first()
        if self.parent is None:
            self.parent = ShopifyRootPage(title='CMS Home', slug='cms-home', locale=locale)
            site_root.add_child(instance=self.parent)
            self.parent.save_revision().publish()

    def test_home_page_is_syncable(self):
        page = HomePage(
            title='Shop Bold.',
            hero_heading='Shop Bold.',
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        self.assertTrue(is_syncable_page(page))

    @patch('shopify_content.sync.publish_sync.enqueue_page_outbound_sync')
    def test_queue_sync_on_publish(self, mock_enqueue):
        page = HomePage(
            title='Shop Bold.',
            hero_heading='Shop Bold.',
            locale=Locale.get_default(),
            sync_enabled=True,
        )
        self.parent.add_child(instance=page)

        queue_shopify_sync_on_publish(page)

        mock_enqueue.assert_called_once()

    def test_sync_disabled_skips_enqueue(self):
        page = HomePage(
            title='Shop Bold.',
            hero_heading='Shop Bold.',
            locale=Locale.get_default(),
            sync_enabled=False,
        )
        self.parent.add_child(instance=page)

        result = queue_shopify_sync_on_publish(page)
        self.assertIsNone(result)

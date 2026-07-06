from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from django.test import TestCase, override_settings
from wagtail.models import Locale, Page

from core.models import ShopConfig
from metaobjects.shopify_metaobjects.metaobject import Metaobject
from shopify_content.locations.index import build_location_index_json
from shopify_content.models import LocationPage, ShopifyRootPage
from shopify_content.sync.location_index import (
    get_location_index_config,
    sync_location_index_pages,
)


class BuildLocationIndexJsonTests(TestCase):
    def setUp(self):
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.parent = ShopifyRootPage(title='Local US', slug='local-us', locale=locale)
        home.add_child(instance=self.parent)
        self.parent.save_revision().publish()

    def _add_location(self, *, titulo, city, state='', shopify_id='gid://shopify/Metaobject/1',
                      shopify_locale='', live=True):
        page = LocationPage(
            title=titulo,
            titulo=titulo,
            city=city,
            state=state,
            shopify_id=shopify_id,
            shopify_locale=shopify_locale,
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        if live:
            page.save_revision().publish()
        else:
            page.save_revision()
        return page

    def test_groups_by_state(self):
        fixed = datetime(2026, 7, 5, 12, 0, tzinfo=timezone.utc)
        self._add_location(titulo='LA Store', city='Los Angeles', state='California', shopify_id='gid://1')
        self._add_location(titulo='NYC Store', city='New York', state='New York', shopify_id='gid://2')
        self._add_location(titulo='No State', city='Austin', state='', shopify_id='gid://3')

        payload = build_location_index_json('en-US', generated_at=fixed)

        self.assertEqual(payload['version'], 1)
        self.assertEqual(payload['locale'], 'en-US')
        self.assertEqual(payload['count'], 3)
        keys = [section['key'] for section in payload['sections']]
        self.assertEqual(keys[-1], '#')
        self.assertEqual(payload['sections'][0]['items'][0]['path'], '/pages/location/en-us-los-angeles-california')

    def test_filters_by_shopify_locale_override(self):
        self._add_location(
            titulo='Montreal',
            city='Montreal',
            state='Quebec',
            shopify_id='gid://1',
            shopify_locale='en-CA',
        )
        self._add_location(
            titulo='NYC',
            city='New York',
            state='New York',
            shopify_id='gid://2',
        )

        en_ca = build_location_index_json('en-CA')
        en_us = build_location_index_json('en-US')

        self.assertEqual(en_ca['count'], 1)
        self.assertEqual(en_us['count'], 1)


class SyncLocationIndexPagesTests(TestCase):
    def setUp(self):
        ShopConfig.objects.create(shop='test-shop.myshopify.com', access_token='tok')
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        site_root = ShopifyRootPage(title='Site Root', slug='site-root', locale=locale)
        home.add_child(instance=site_root)
        site_root.save_revision().publish()

        self.location_root = ShopifyRootPage(
            title='Local US',
            slug='local-us',
            export_config={
                'location_index': {
                    'enabled': True,
                    'locales': ['en-US'],
                },
            },
            locale=locale,
        )
        site_root.add_child(instance=self.location_root)
        self.location_root.save_revision().publish()

        loc = LocationPage(
            title='LA',
            titulo='LA Store',
            city='Los Angeles',
            state='California',
            shopify_id='gid://shopify/Metaobject/20',
            locale=locale,
        )
        self.location_root.add_child(instance=loc)
        loc.save_revision().publish()

    def test_get_location_index_config_reads_export_config(self):
        config = get_location_index_config(self.location_root)
        self.assertTrue(config['enabled'])
        self.assertEqual(config['locales'], ['en-US'])

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_sync_upserts_metaobject_entry(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.sync.return_value = Metaobject(type='root_page', handle='locations-en-us', id='gid://1')
        mock_client_cls.return_value = mock_client

        stats = sync_location_index_pages()

        self.assertEqual(stats['pushed'], 1)
        mock_client.sync.assert_called_once()
        data = mock_client.sync.call_args.args[0]
        self.assertEqual(data['handle'], 'locations-en-us')
        self.assertEqual(data['locale'], 'en-US')
        self.assertEqual(data['index']['count'], 1)
        self.assertEqual(data['index_alternates']['alternates'][0]['handle'], 'locations-en-us')
        self.assertFalse(data['index_noindex'])


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class LocationIndexSignalTests(TestCase):
    def setUp(self):
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        site_root = ShopifyRootPage(title='Site Root', slug='site-root', locale=locale)
        home.add_child(instance=site_root)
        site_root.save_revision().publish()

        self.location_root = ShopifyRootPage(
            title='Local US',
            slug='local-us',
            export_config={
                'location_index': {
                    'enabled': True,
                    'locales': ['en-US'],
                },
            },
            locale=locale,
        )
        site_root.add_child(instance=self.location_root)
        self.location_root.save_revision().publish()

    @patch('shopify_content.sync.location_index.sync_location_index_pages')
    @patch('shopify_content.sync.outbound.sync_location_page')
    def test_location_publish_queues_index_sync_after_outbound(self, mock_loc_sync, mock_index_sync):
        from shopify_content.export_config.registry import queue_index_sync_for_content_page

        def _sync_and_set_gid(page):
            LocationPage.objects.filter(pk=page.pk).update(
                shopify_id='gid://shopify/Metaobject/1',
            )
            queue_index_sync_for_content_page(page)
            return True, 'ok'

        mock_loc_sync.side_effect = _sync_and_set_gid

        loc = LocationPage(
            title='Chicago',
            titulo='Chicago Store',
            city='Chicago',
            state='Illinois',
            locale=Locale.get_default(),
            sync_enabled=True,
        )
        self.location_root.add_child(instance=loc)

        with self.captureOnCommitCallbacks(execute=True):
            loc.save_revision().publish()

        mock_loc_sync.assert_called_once()
        mock_index_sync.assert_called_once_with(locale_codes=['en-US'], dry_run=False)

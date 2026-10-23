from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from django.test import TestCase, override_settings
from wagtail.models import Locale, Page

from shopify_config.models import ShopConfig
from metaobjects.shopify_metaobjects.metaobject import Metaobject
from shopify_content.locations.index import (
    build_location_index_json,
    build_location_index_listings,
)
from shopify_content.models import LocationPage, ShopifyRootPage
from shopify_content.sync.location_index import (
    get_location_index_config,
    sync_location_index_pages,
)


def _locale(code: str) -> Locale:
    locale, _ = Locale.objects.get_or_create(language_code=code)
    return locale


class BuildLocationIndexJsonTests(TestCase):
    def setUp(self):
        locale = _locale('en-US')
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
            locale=_locale('en-US'),
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

        listings = build_location_index_listings()
        en_ca = listings['locales']['en-CA']
        en_us = listings['locales']['en-US']

        self.assertEqual(en_ca['count'], 1)
        self.assertEqual(en_us['count'], 1)


class SyncLocationIndexPagesTests(TestCase):
    def setUp(self):
        ShopConfig.objects.create(shop='test-shop.myshopify.com', access_token='tok')
        locale = _locale('en-US')
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
        mock_client.sync.return_value = Metaobject(
            type='root_page', handle='locations-en-us', id='gid://1',
        )
        mock_client_cls.return_value = mock_client

        stats = sync_location_index_pages()

        self.assertEqual(stats['pushed'], 1)
        mock_client.sync.assert_called_once()
        data = mock_client.sync.call_args.args[0]
        self.assertEqual(data['handle'], 'locations-en-us')
        self.assertEqual(data['index']['count'], 1)


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class LocationIndexSignalTests(TestCase):
    def setUp(self):
        locale = _locale('en-US')
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
            locale=_locale('en-US'),
            sync_enabled=True,
        )
        self.location_root.add_child(instance=loc)

        with self.captureOnCommitCallbacks(execute=True):
            loc.save_revision().publish()

        mock_loc_sync.assert_called_once()
        mock_index_sync.assert_called_once_with(locale_codes=None, dry_run=False)


class RegionGroupedLocationIndexTests(TestCase):
    def setUp(self):
        locale = _locale('en-CA')
        _locale('en-US')
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.root = ShopifyRootPage(title='Local US', slug='local-us', locale=locale)
        home.add_child(instance=self.root)
        self.root.save_revision().publish()
        self.locale = locale

    def _region(self, title, code, country='Canada', handle=''):
        from shopify_content.models import RegionPage

        region = RegionPage(
            title=title, slug=f'en-ca-{title.lower().replace(" ", "-")}', country=country,
            region_code=code, handle=handle or title.lower().replace(' ', '-'), locale=self.locale,
        )
        self.root.add_child(instance=region)
        region.save_revision().publish()
        return region

    def _location(self, parent, city, **extra):
        extra.setdefault('shopify_id', f'gid://shopify/Metaobject/{city}')
        page = LocationPage(
            title=city, titulo=city, city=city, locale=self.locale, handle=city.lower(),
            keep_shopify_handle=True, **extra,
        )
        parent.add_child(instance=page)
        page.save_revision().publish()
        return page

    def test_sections_are_the_regions_with_a_region_summary(self):
        ontario = self._region('Ontario', 'ON')
        quebec = self._region('Quebec', 'QC')
        self._location(ontario, 'Toronto')
        self._location(ontario, 'Ajax')
        self._location(quebec, 'Montreal')

        payload = build_location_index_json('en-CA')

        self.assertEqual([s['key'] for s in payload['sections']], ['Ontario', 'Quebec'])
        ontario_section = payload['sections'][0]
        self.assertEqual([i['city'] for i in ontario_section['items']], ['Ajax', 'Toronto'])
        self.assertEqual(ontario_section['region'], {
            'handle': 'ontario', 'code': 'ON', 'country': 'Canada', 'path': '/pages/canada/ontario',
        })
        self.assertEqual(payload['count'], 3)

    def test_canadian_locations_link_to_the_canadian_pages(self):
        ontario = self._region('Ontario', 'ON')
        self._location(ontario, 'Ajax')
        item = build_location_index_json('en-CA')['sections'][0]['items'][0]
        self.assertEqual(item['path'], '/pages/canada-location/ajax')
        self.assertEqual(item['country'], 'Canada')

    def test_us_region_has_no_public_path_yet_and_us_locations_keep_their_path(self):
        texas = self._region('Texas', 'TX', country='United States')
        self._location(texas, 'Austin')
        section = build_location_index_json('en-CA')['sections'][0]
        self.assertIsNone(section['region']['path'])
        self.assertEqual(section['items'][0]['path'], '/pages/location/austin')

    def test_loose_location_falls_back_to_its_state_and_has_no_region(self):
        self._location(self.root, 'Austin', state='Texas')
        self._location(self.root, 'Nowhere')
        payload = build_location_index_json('en-CA')

        self.assertEqual([s['key'] for s in payload['sections']], ['Texas', '#'])
        self.assertNotIn('region', payload['sections'][0])

    def test_region_name_wins_over_the_state_text_and_merges_with_loose_pages(self):
        texas = self._region('Texas', 'TX', country='United States')
        austin = self._location(texas, 'Austin')
        # Moving a page or renaming its region does not re-run clean(), so state can go stale.
        LocationPage.objects.filter(pk=austin.pk).update(state='stale')
        self._location(self.root, 'Dallas', state='Texas')
        payload = build_location_index_json('en-CA')

        self.assertEqual([s['key'] for s in payload['sections']], ['Texas'])
        self.assertEqual([i['city'] for i in payload['sections'][0]['items']], ['Austin', 'Dallas'])

    def test_unpublished_region_leaves_its_locations_listed_without_a_region(self):
        ontario = self._region('Ontario', 'ON')
        self._location(ontario, 'Ajax', state='Ontario')
        ontario.unpublish()
        payload = build_location_index_json('en-CA')

        # unpublish() leaves the children live: they stay listed under their state text.
        self.assertEqual(payload['count'], 1)
        self.assertEqual([s['key'] for s in payload['sections']], ['Ontario'])
        self.assertNotIn('region', payload['sections'][0])

    def test_index_does_not_query_once_per_location(self):
        ontario = self._region('Ontario', 'ON')
        for city in ('Ajax', 'Barrie', 'Cobourg', 'Dundas', 'Elora', 'Fergus'):
            self._location(ontario, city)
        with self.assertNumQueries(3):
            build_location_index_json('en-CA')

    def test_region_publish_queues_a_rebuild_of_its_locale(self):
        from shopify_content.export_config.location import location_index_consumer

        with patch.object(location_index_consumer, 'queue_sync') as queue:
            ontario = self._region('Ontario', 'ON')
        queue.assert_called_with(locale_codes=['en-CA'])
        self.assertTrue(ontario.live)

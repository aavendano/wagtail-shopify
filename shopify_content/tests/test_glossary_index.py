from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from django.test import TestCase, override_settings
from wagtail.models import Locale, Page

from core.models import ShopConfig
from metaobjects.shopify_metaobjects.exceptions import UpsertError
from metaobjects.shopify_metaobjects.metaobject import Metaobject
from shopify_content.glossary.index import build_glossary_index_json
from shopify_content.models import GlossaryTermPage, ShopifyRootPage
from shopify_content.sync.glossary_index import (
    get_glossary_index_config,
    sync_glossary_index_pages,
)


class BuildGlossaryIndexJsonTests(TestCase):
    def setUp(self):
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.parent = ShopifyRootPage(title='Glossary', slug='glossary', locale=locale)
        home.add_child(instance=self.parent)
        self.parent.save_revision().publish()

    def _add_term(self, *, term, locale_code='en', shopify_id='gid://shopify/Metaobject/1',
                  handle='', slug='', live=True):
        page = GlossaryTermPage(
            title=term,
            term=term,
            locale_code=locale_code,
            shopify_id=shopify_id,
            handle=handle,
            slug=slug or term.lower().replace(' ', '-'),
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        if live:
            page.save_revision().publish()
        else:
            page.save_revision()
        return page

    def test_groups_terms_by_letter_digit_and_symbol(self):
        fixed = datetime(2026, 7, 5, 12, 0, tzinfo=timezone.utc)
        self._add_term(term='Alpha', shopify_id='gid://1')
        self._add_term(term='beta', shopify_id='gid://2')
        self._add_term(term='9 Lives', shopify_id='gid://3')
        self._add_term(term='#hashtag', shopify_id='gid://4', slug='hashtag')

        payload = build_glossary_index_json('en', generated_at=fixed)

        self.assertEqual(payload['version'], 1)
        self.assertEqual(payload['locale'], 'en')
        self.assertEqual(payload['generated_at'], fixed.isoformat())
        self.assertEqual(payload['count'], 4)
        keys = [section['key'] for section in payload['sections']]
        self.assertEqual(keys, ['A', 'B', '0-9', '#'])
        self.assertEqual(payload['sections'][0]['items'][0]['term'], 'Alpha')
        self.assertEqual(payload['sections'][0]['items'][0]['path'], '/pages/glossary/alpha')

    def test_excludes_unpublished_and_missing_shopify_id(self):
        self._add_term(term='Live Term', shopify_id='gid://1')
        draft = self._add_term(term='Draft Term', shopify_id='gid://2', live=False)
        draft.save_revision().publish()
        draft.unpublish()
        self._add_term(term='No Shopify', shopify_id='')

        payload = build_glossary_index_json('en')

        self.assertEqual(payload['count'], 1)
        self.assertEqual(payload['sections'][0]['items'][0]['term'], 'Live Term')

    def test_filters_by_locale_code(self):
        self._add_term(term='English', locale_code='en', shopify_id='gid://1')
        self._add_term(term='Español', locale_code='es', shopify_id='gid://2')

        en_payload = build_glossary_index_json('en')
        es_payload = build_glossary_index_json('es')

        self.assertEqual(en_payload['count'], 1)
        self.assertEqual(es_payload['count'], 1)
        self.assertEqual(en_payload['sections'][0]['items'][0]['term'], 'English')
        self.assertEqual(es_payload['sections'][0]['items'][0]['term'], 'Español')


class SyncGlossaryIndexPagesTests(TestCase):
    def setUp(self):
        ShopConfig.objects.create(shop='test-shop.myshopify.com', access_token='tok')
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        site_root = ShopifyRootPage(title='Site Root', slug='site-root', locale=locale)
        home.add_child(instance=site_root)
        site_root.save_revision().publish()

        self.glossary_root = ShopifyRootPage(
            title='Glossary',
            slug='glossary',
            export_config={
                'glossary_index': {
                    'enabled': True,
                    'locales': ['en', 'es'],
                },
            },
            locale=locale,
        )
        site_root.add_child(instance=self.glossary_root)
        self.glossary_root.save_revision().publish()

        term = GlossaryTermPage(
            title='Vibrator',
            term='Vibrator',
            locale_code='en',
            shopify_id='gid://shopify/Metaobject/10',
            slug='vibrator',
            locale=locale,
        )
        self.glossary_root.add_child(instance=term)
        term.save_revision().publish()

    def test_get_glossary_index_config_reads_export_config(self):
        config = get_glossary_index_config(self.glossary_root)
        self.assertTrue(config['enabled'])
        self.assertEqual(config['locales'], ['en', 'es'])

    def test_sync_disabled_when_not_configured(self):
        self.glossary_root.export_config = {}
        self.glossary_root.save()

        stats = sync_glossary_index_pages()

        self.assertFalse(stats['enabled'])
        self.assertEqual(stats['pushed'], 0)

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_sync_upserts_metaobject_entries_for_configured_locales(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.sync.return_value = Metaobject(type='root_page', handle='glossary-en', id='gid://1')
        mock_client_cls.return_value = mock_client

        stats = sync_glossary_index_pages()

        self.assertEqual(stats['pushed'], 2)
        self.assertEqual(mock_client.sync.call_count, 2)

        calls_by_locale = {
            call.args[0]['locale']: call.args[0]
            for call in mock_client.sync.call_args_list
        }
        en_data = calls_by_locale['en']
        self.assertEqual(en_data['handle'], 'glossary-en')
        self.assertEqual(en_data['index']['count'], 1)
        self.assertEqual(en_data['index_alternates']['version'], 1)
        self.assertEqual(
            {alt['handle'] for alt in en_data['index_alternates']['alternates']},
            {'glossary-en', 'glossary-es'},
        )
        self.assertFalse(en_data['index_noindex'])
        self.assertEqual(calls_by_locale['es']['handle'], 'glossary-es')

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_sync_marks_noindex_locales(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.sync.return_value = Metaobject(type='root_page', handle='glossary-en', id='gid://1')
        mock_client_cls.return_value = mock_client

        self.glossary_root.export_config['glossary_index']['noindex_locales'] = ['es']
        self.glossary_root.save()

        sync_glossary_index_pages()

        calls_by_locale = {
            call.args[0]['locale']: call.args[0]
            for call in mock_client.sync.call_args_list
        }
        self.assertFalse(calls_by_locale['en']['index_noindex'])
        self.assertTrue(calls_by_locale['es']['index_noindex'])

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_dry_run_skips_shopify_push(self, mock_client_cls):
        stats = sync_glossary_index_pages(dry_run=True)

        self.assertEqual(stats['pushed'], 2)
        mock_client_cls.assert_not_called()

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_sync_records_errors(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.sync.side_effect = UpsertError('boom')
        mock_client_cls.return_value = mock_client

        stats = sync_glossary_index_pages(locale_codes=['en'])

        self.assertEqual(stats['errors'], ['en'])
        mock_client.sync.assert_called_once()


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class GlossaryIndexSignalTests(TestCase):
    def setUp(self):
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        site_root = ShopifyRootPage(title='Site Root', slug='site-root', locale=locale)
        home.add_child(instance=site_root)
        site_root.save_revision().publish()

        self.glossary_root = ShopifyRootPage(
            title='Glossary',
            slug='glossary',
            export_config={
                'glossary_index': {
                    'enabled': True,
                    'locales': ['en'],
                },
            },
            locale=locale,
        )
        site_root.add_child(instance=self.glossary_root)
        self.glossary_root.save_revision().publish()

    @patch('shopify_content.sync.glossary_index.sync_glossary_index_pages')
    @patch('shopify_content.sync.outbound.sync_glossary_term_page')
    def test_term_publish_queues_index_sync_after_outbound(self, mock_term_sync, mock_index_sync):
        from shopify_content.export_config.registry import queue_index_sync_for_content_page

        def _sync_and_set_gid(page):
            GlossaryTermPage.objects.filter(pk=page.pk).update(
                shopify_id='gid://shopify/Metaobject/1',
            )
            queue_index_sync_for_content_page(page)
            return True, 'ok'

        mock_term_sync.side_effect = _sync_and_set_gid

        term = GlossaryTermPage(
            title='Term',
            term='Term',
            locale_code='en',
            slug='term',
            locale=Locale.get_default(),
            sync_enabled=True,
        )
        self.glossary_root.add_child(instance=term)

        with self.captureOnCommitCallbacks(execute=True):
            term.save_revision().publish()

        mock_term_sync.assert_called_once()
        mock_index_sync.assert_called_once_with(locale_codes=['en'], dry_run=False)

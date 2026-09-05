"""Tests for migrate_index_export_config management command."""

from django.core.management import call_command
from django.test import TestCase
from wagtail.models import Locale, Page

from core.models import ShopConfig
from shopify_content.models import ShopifyRootPage


class MigrateIndexExportConfigTests(TestCase):
    def setUp(self):
        ShopConfig.objects.create(shop='test-shop.myshopify.com', access_token='tok')
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))

        self.glossary_root = ShopifyRootPage(
            title='Glossary',
            slug='glossary',
            export_config={
                'glossary_index': {
                    'enabled': True,
                    'pages': {'en': 'gid://shopify/Page/legacy-en', 'es': 'gid://shopify/Page/legacy-es'},
                },
            },
            locale=locale,
        )
        home.add_child(instance=self.glossary_root)
        self.glossary_root.save_revision().publish()

    def test_apply_migrates_glossary_export_config(self):
        call_command('migrate_index_export_config', '--apply')

        self.glossary_root.refresh_from_db()
        section = self.glossary_root.export_config['glossary_index']
        self.assertEqual(section['locales'], ['en', 'es'])
        self.assertEqual(section['_legacy_pages']['en'], 'gid://shopify/Page/legacy-en')
        self.assertNotIn('pages', section)
        self.assertNotIn('page_gid', section)

    def test_apply_migrates_page_gid_to_locales(self):
        self.glossary_root.export_config = {
            'glossary_index': {
                'enabled': True,
                'page_gid': 'gid://shopify/Page/old',
            },
        }
        self.glossary_root.save(update_fields=['export_config'])

        call_command('migrate_index_export_config', '--apply')

        self.glossary_root.refresh_from_db()
        section = self.glossary_root.export_config['glossary_index']
        self.assertTrue(section['locales'])
        self.assertEqual(section['_legacy_page_gid'], 'gid://shopify/Page/old')
        self.assertNotIn('page_gid', section)

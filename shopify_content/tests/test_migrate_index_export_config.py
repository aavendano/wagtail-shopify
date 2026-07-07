"""Tests for migrate_index_export_config management command."""

from unittest.mock import patch

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
                    'pages': {'en': 'gid://shopify/Page/legacy-en'},
                },
            },
            locale=locale,
        )
        home.add_child(instance=self.glossary_root)
        self.glossary_root.save_revision().publish()

    @patch('shopify_content.management.commands.migrate_index_export_config.ensure_index_pages')
    def test_apply_migrates_glossary_export_config(self, mock_ensure):
        mock_ensure.return_value = {
            'glossary': {'id': 'gid://shopify/Page/new-glossary', 'created': False},
            'locations': {'id': 'gid://shopify/Page/new-locations', 'created': False},
        }

        call_command('migrate_index_export_config', '--apply')

        self.glossary_root.refresh_from_db()
        section = self.glossary_root.export_config['glossary_index']
        self.assertEqual(section['page_gid'], 'gid://shopify/Page/new-glossary')
        self.assertEqual(section['_legacy_pages']['en'], 'gid://shopify/Page/legacy-en')
        self.assertNotIn('pages', section)

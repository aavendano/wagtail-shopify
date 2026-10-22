"""Channel projection registry: schema type → Shopify type per reader."""

import ast
import inspect
from pathlib import Path

from django.test import SimpleTestCase

import shopify_content
import shopify_content.models as content_models
from shopify_content.projection import PROJECTIONS, projection
from shopify_content.sync import import_parents
from shopify_content.sync.outbound import (
    _glossary_term_definition,
    _home_page_definition,
    _location_page_definition,
    _root_page_definition,
)


class ChannelProjectionTests(SimpleTestCase):
    def test_registry_keys(self):
        self.assertEqual(
            set(PROJECTIONS),
            {
                'location',
                'region',
                'glossary_term',
                'index',
                'home',
                'product',
                'collection',
                'blog',
                'article',
                'page',
            },
        )

    def test_location_writes_local_page_and_hydrogen_reads_location_page(self):
        row = projection('location')
        self.assertEqual(row.wagtail_model, 'LocationPage')
        self.assertEqual(row.resource_class, 'metaobject')
        self.assertEqual(row.wagtail_type, 'local_page')
        self.assertEqual(row.liquid_type, 'local_page')
        self.assertEqual(row.hydrogen_type, 'location_page')
        self.assertTrue(row.wagtail_sync)

    def test_region_and_page_are_not_wagtail_synced(self):
        region = projection('region')
        page = projection('page')
        self.assertFalse(region.wagtail_sync)
        self.assertIsNone(region.wagtail_model)
        self.assertEqual(region.hydrogen_type, 'region')
        self.assertFalse(page.wagtail_sync)
        self.assertIsNone(page.wagtail_model)
        self.assertFalse(hasattr(content_models, 'RegionPage'))

        models_root = Path(content_models.__file__).resolve().parent
        for path in models_root.rglob('*.py'):
            self.assertNotIn(
                'class RegionPage',
                path.read_text(encoding='utf-8'),
                msg=str(path),
            )

    def test_index_root_page_has_no_hydrogen_reader(self):
        row = projection('index')
        self.assertEqual(row.wagtail_model, 'ShopifyRootPage')
        self.assertEqual(row.resource_class, 'metaobject')
        self.assertEqual(row.wagtail_type, 'root_page')
        self.assertEqual(row.liquid_type, 'root_page')
        self.assertIsNone(row.hydrogen_type)
        self.assertTrue(row.wagtail_sync)

    def test_article_is_native_not_metaobject(self):
        row = projection('article')
        self.assertEqual(row.wagtail_model, 'ArticlePage')
        self.assertEqual(row.resource_class, 'native')
        self.assertEqual(row.wagtail_type, 'Article')
        self.assertEqual(row.hydrogen_type, 'Article')
        self.assertEqual(row.liquid_type, 'Article')
        self.assertNotEqual(row.wagtail_type, 'article')
        self.assertTrue(row.wagtail_sync)

    def test_unknown_type_raises_key_error(self):
        with self.assertRaises(KeyError):
            projection('seo_collection')
        with self.assertRaises(KeyError):
            projection('not-a-document-type')

    def test_outbound_definition_types_match_registry(self):
        self.assertEqual(
            _location_page_definition().type,
            projection('location').wagtail_type,
        )
        self.assertEqual(
            _glossary_term_definition().type,
            projection('glossary_term').wagtail_type,
        )
        self.assertEqual(
            _root_page_definition().type,
            projection('index').wagtail_type,
        )
        self.assertEqual(
            _home_page_definition().type,
            projection('home').wagtail_type,
        )

    def test_default_site_lookup_has_no_channel_factory(self):
        source = inspect.getsource(import_parents._get_site_home_page)
        self.assertIn('Site.objects.get(is_default_site=True)', source)

        package = Path(shopify_content.__file__).resolve().parent
        creates = []
        factory_names = []
        for path in package.rglob('*.py'):
            if 'tests' in path.parts or 'migrations' in path.parts:
                continue
            text = path.read_text(encoding='utf-8')
            if 'Site.objects.create' in text or 'Site.objects.get_or_create' in text:
                creates.append(path.relative_to(package).as_posix())
            tree = ast.parse(text)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    name = node.name.lower()
                    if 'site' in name and 'channel' in name:
                        factory_names.append(
                            f'{path.relative_to(package).as_posix()}:{node.name}',
                        )
        self.assertEqual(creates, [])
        self.assertEqual(factory_names, [])

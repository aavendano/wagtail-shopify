"""Tests for HomePage sections_json reference resolution."""

from django.test import TestCase
from wagtail.models import Locale, Page

from shopify_content.home_references import build_home_sync_references
from shopify_content.models import CollectionPage, HomePage, ShopifyRootPage
from shopify_content.sync.outbound import _home_page_definition


class HomeReferencesTests(TestCase):
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

        self.collection = CollectionPage(
            title='Vibrators',
            slug='vibrators',
            handle='vibrators',
            shopify_id='gid://shopify/Collection/10',
            locale=locale,
        )
        self.parent.add_child(instance=self.collection)
        self.collection.save_revision().publish()

    def test_build_references_from_sections_json(self):
        sections_json = {
            'version': 1,
            'sections': [
                {
                    'type': 'featured_collections',
                    'id': 'feat-1',
                    'value': {
                        'title': 'Core',
                        'items': [{'page_id': self.collection.pk}],
                    },
                },
                {
                    'type': 'best_sellers',
                    'id': 'best-1',
                    'value': {
                        'title': 'Best',
                        'collection_page_id': self.collection.pk,
                    },
                },
            ],
        }
        refs = build_home_sync_references(sections_json)
        self.assertEqual(
            refs['featured_collections_refs'],
            ['gid://shopify/Collection/10'],
        )
        self.assertEqual(
            refs['best_sellers_collection_ref'],
            'gid://shopify/Collection/10',
        )
        self.assertTrue(refs['related_links'])


class HomePageDefinitionNativeFieldsTests(TestCase):
    def test_definition_includes_native_reference_fields(self):
        spec = _home_page_definition()
        field_keys = {field.key for field in spec.fields}
        self.assertIn('hero_eyebrow', field_keys)
        self.assertIn('featured_collections_refs', field_keys)
        self.assertIn('best_sellers_collection_ref', field_keys)
        self.assertIn('related_links', field_keys)

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

        self.collection_b = CollectionPage(
            title='Couples',
            slug='couples',
            handle='couples',
            shopify_id='gid://shopify/Collection/11',
            locale=locale,
        )
        self.parent.add_child(instance=self.collection_b)
        self.collection_b.save_revision().publish()

        self.collection_c = CollectionPage(
            title='Best Sex Toys',
            slug='best-sex-toys',
            handle='best-sex-toys',
            shopify_id='gid://shopify/Collection/12',
            locale=locale,
        )
        self.parent.add_child(instance=self.collection_c)
        self.collection_c.save_revision().publish()

        self.collection_d = CollectionPage(
            title='Lingerie',
            slug='sexy-lingerie',
            handle='sexy-lingerie',
            shopify_id='gid://shopify/Collection/13',
            locale=locale,
        )
        self.parent.add_child(instance=self.collection_d)
        self.collection_d.save_revision().publish()

        self.collection_e = CollectionPage(
            title='Male Wand',
            slug='male-wand',
            handle='male-wand',
            shopify_id='gid://shopify/Collection/20',
            locale=locale,
        )
        self.parent.add_child(instance=self.collection_e)
        self.collection_e.save_revision().publish()

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

    def test_promo_gateway_ref_order(self):
        """Ref order contract for promo-gateway-card Liquid cursor — see test name in snippet."""
        sections_json = {
            'version': 1,
            'sections': [
                {
                    'type': 'promo_gateway',
                    'id': 'promo-gateway',
                    'value': {
                        'cards': [
                            {
                                'title': 'Products card',
                                'media_source': 'collection_products',
                                'primary_collection_page_id': self.collection.pk,
                                'category_page_ids': [
                                    self.collection_b.pk,
                                    self.collection_c.pk,
                                    self.collection_d.pk,
                                ],
                            },
                            {
                                'title': 'List card',
                                'media_source': 'collection_list',
                                'category_page_ids': [
                                    self.collection_e.pk,
                                    self.collection.pk,
                                ],
                            },
                        ],
                    },
                },
            ],
        }
        refs = build_home_sync_references(sections_json)
        self.assertEqual(
            refs['promo_gateway_collection_refs'],
            [
                'gid://shopify/Collection/10',
                'gid://shopify/Collection/11',
                'gid://shopify/Collection/12',
                'gid://shopify/Collection/13',
                'gid://shopify/Collection/20',
                'gid://shopify/Collection/10',
            ],
        )


class HomePageDefinitionNativeFieldsTests(TestCase):
    def test_definition_includes_native_reference_fields(self):
        spec = _home_page_definition()
        field_keys = {field.key for field in spec.fields}
        self.assertIn('hero_eyebrow', field_keys)
        self.assertIn('featured_collections_refs', field_keys)
        self.assertIn('best_sellers_collection_ref', field_keys)
        self.assertIn('promo_gateway_collection_refs', field_keys)
        self.assertIn('related_links', field_keys)

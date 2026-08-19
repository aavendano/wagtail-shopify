"""Round-trip tests for HomePage sections_json ↔ StreamField."""

from django.core.exceptions import ValidationError
from django.test import TestCase
from wagtail.models import Locale, Page

from shopify_content.home_sections_normalization import (
    CANONICAL_SECTION_TYPES,
    normalize_sections_json,
)
from shopify_content.home_serialization import (
    sections_json_to_stream_data,
    streamfield_to_sections_json,
)
from shopify_content.models import CollectionPage, HomePage, ShopifyRootPage


class HomeSectionsRoundTripTests(TestCase):
    def setUp(self):
        self.locale = Locale.get_default()
        site_root = Page.get_first_root_node()
        if site_root is None:
            site_root = Page.add_root(
                instance=Page(title='Site Home', slug='site-home', locale=self.locale)
            )
        self.parent = ShopifyRootPage.objects.filter(slug='cms-home').first()
        if self.parent is None:
            self.parent = ShopifyRootPage(title='CMS Home', slug='cms-home', locale=self.locale)
            site_root.add_child(instance=self.parent)
            self.parent.save_revision().publish()

        self.collection = CollectionPage(
            title='Vibrators',
            slug='vibrators-rt',
            handle='vibrators-rt',
            shopify_id='gid://shopify/Collection/99',
            locale=self.locale,
        )
        self.parent.add_child(instance=self.collection)
        self.collection.save_revision().publish()

    def test_empty_round_trip_preserves_thirteen_types(self):
        original = normalize_sections_json({})
        stream_data = sections_json_to_stream_data(original)
        self.assertEqual(len(stream_data), 13)
        self.assertEqual(
            [block['type'] for block in stream_data],
            list(CANONICAL_SECTION_TYPES),
        )

        page = HomePage(
            title='Home RT',
            hero_heading='Home RT',
            locale=self.locale,
            body=stream_data,
        )
        self.parent.add_child(instance=page)
        page.refresh_from_db()

        round_tripped = streamfield_to_sections_json(page.body)
        self.assertEqual(round_tripped['version'], 1)
        self.assertEqual(
            [s['type'] for s in round_tripped['sections']],
            list(CANONICAL_SECTION_TYPES),
        )
        self.assertEqual(
            round_tripped['sections'][4]['id'],
            'editorial-intro',
        )

    def test_populated_round_trip_keeps_page_ids_and_copy(self):
        original = normalize_sections_json({
            'sections': [
                {
                    'type': 'editorial_intro',
                    'value': {
                        'heading': 'Welcome',
                        'body': '<p>Hello</p>',
                        'alignment': 'center',
                    },
                },
                {
                    'type': 'featured_collections',
                    'value': {
                        'title': 'Shop',
                        'items': [
                            {
                                'page_id': self.collection.pk,
                                'override_title': 'Vibrators',
                            },
                        ],
                    },
                },
                {
                    'type': 'best_sellers',
                    'value': {
                        'title': 'Best',
                        'collection_page_id': self.collection.pk,
                        'product_limit': 6,
                    },
                },
                {
                    'type': 'faq',
                    'value': {
                        'heading': 'FAQ',
                        'items': [
                            {'question': 'Q1', 'answer': '<p>A1</p>'},
                        ],
                    },
                },
            ],
        })
        stream_data = sections_json_to_stream_data(original)
        page = HomePage(
            title='Home Pop',
            hero_heading='Home Pop',
            locale=self.locale,
            body=stream_data,
        )
        self.parent.add_child(instance=page)
        page.refresh_from_db()

        result = streamfield_to_sections_json(page.body)
        by_type = {s['type']: s['value'] for s in result['sections']}
        self.assertEqual(by_type['editorial_intro']['heading'], 'Welcome')
        self.assertEqual(by_type['editorial_intro']['alignment'], 'center')
        self.assertEqual(by_type['featured_collections']['items'][0]['page_id'], self.collection.pk)
        self.assertEqual(by_type['featured_collections']['items'][0]['override_title'], 'Vibrators')
        self.assertEqual(by_type['best_sellers']['collection_page_id'], self.collection.pk)
        self.assertEqual(by_type['best_sellers']['product_limit'], 6)
        self.assertEqual(by_type['faq']['items'][0]['question'], 'Q1')

    def test_homepage_clean_serializes_body_to_sections_json(self):
        stream_data = sections_json_to_stream_data(normalize_sections_json({
            'sections': [{
                'type': 'editorial_intro',
                'value': {'heading': 'From body', 'body': '<p>x</p>'},
            }],
        }))
        page = HomePage(
            title='Home Clean',
            hero_heading='Home Clean',
            locale=self.locale,
            body=stream_data,
            sections_json={},
        )
        self.parent.add_child(instance=page)
        page.full_clean()
        by_type = {s['type']: s['value'] for s in page.sections_json['sections']}
        self.assertEqual(by_type['editorial_intro']['heading'], 'From body')
        self.assertEqual(len(page.sections_json['sections']), 13)

    def test_block_counts_reject_duplicate_faq(self):
        stream_data = sections_json_to_stream_data(normalize_sections_json({}))
        stream_data.append({
            'type': 'faq',
            'id': 'faq-extra',
            'value': {'heading': 'Extra', 'items': []},
        })
        page = HomePage(
            title='Home Dup',
            hero_heading='Home Dup',
            locale=self.locale,
            body=stream_data,
        )
        with self.assertRaises(ValidationError):
            page.full_clean()

    def test_clean_restores_full_envelope_from_partial_body(self):
        page = HomePage(
            title='Home Partial',
            hero_heading='Home Partial',
            locale=self.locale,
            body=[{
                'type': 'editorial_intro',
                'id': 'editorial-intro',
                'value': {'heading': 'Only intro', 'body': '<p>x</p>', 'alignment': 'left'},
            }],
            sections_json={},
        )
        self.parent.add_child(instance=page)
        page.full_clean()
        self.assertEqual(len(page.body), 13)
        self.assertEqual(
            [block.block_type for block in page.body],
            list(CANONICAL_SECTION_TYPES),
        )
        by_type = {s['type']: s['value'] for s in page.sections_json['sections']}
        self.assertEqual(by_type['editorial_intro']['heading'], 'Only intro')
        self.assertEqual(by_type['faq']['heading'], 'Frequently asked questions')

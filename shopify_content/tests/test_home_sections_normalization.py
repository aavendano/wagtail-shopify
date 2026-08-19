from django.test import TestCase

from shopify_content.home_sections_normalization import (
    CANONICAL_SECTION_TYPES,
    coerce_incoming_sections,
    normalize_sections_json,
)


class NormalizeSectionsJsonTests(TestCase):
    def test_empty_payload_fills_thirteen_canonical_types(self):
        payload = normalize_sections_json({})
        types = [section['type'] for section in payload['sections']]
        self.assertEqual(payload['version'], 1)
        self.assertEqual(tuple(types), CANONICAL_SECTION_TYPES)
        self.assertEqual(payload['sections'][4]['id'], 'editorial-intro')
        self.assertEqual(payload['sections'][4]['value']['alignment'], 'left')
        self.assertEqual(payload['sections'][-1]['value']['include_faq_schema'], True)

    def test_partial_overlay_merges_by_type_and_keeps_defaults(self):
        existing = normalize_sections_json({
            'sections': [{
                'type': 'faq',
                'id': 'faq',
                'value': {
                    'heading': 'FAQ',
                    'items': [{'question': 'Q1', 'answer': '<p>A1</p>'}],
                },
            }],
        })
        payload = normalize_sections_json(
            {'sections': [{
                'type': 'editorial_intro',
                'value': {'heading': 'Welcome', 'body': '<p>Hi</p>'},
            }]},
            existing=existing,
        )
        by_type = {section['type']: section['value'] for section in payload['sections']}
        self.assertEqual(by_type['editorial_intro']['heading'], 'Welcome')
        self.assertEqual(by_type['editorial_intro']['alignment'], 'left')
        self.assertEqual(by_type['faq']['heading'], 'FAQ')
        self.assertEqual(by_type['faq']['items'][0]['question'], 'Q1')
        self.assertEqual(len(payload['sections']), 13)

    def test_keyed_dict_is_coerced_to_sections_list(self):
        coerced = coerce_incoming_sections({
            'editorial_intro': {'heading': 'H', 'body': '<p>B</p>'},
            'best_sellers': {'title': 'Best', 'product_limit': 4},
        })
        types = [section['type'] for section in coerced['sections']]
        self.assertEqual(types, ['editorial_intro', 'best_sellers'])

        payload = normalize_sections_json(coerced)
        best = next(s for s in payload['sections'] if s['type'] == 'best_sellers')
        self.assertEqual(best['value']['product_limit'], 4)
        self.assertEqual(best['value']['background'], 'contrast')

    def test_drops_items_without_page_id_and_clamps_product_limit(self):
        payload = normalize_sections_json({
            'sections': [
                {
                    'type': 'featured_collections',
                    'value': {
                        'title': 'Shop',
                        'items': [
                            {'page_id': 12, 'override_title': 'Vibrators'},
                            {'override_title': 'Missing'},
                        ],
                    },
                },
                {
                    'type': 'best_sellers',
                    'value': {'product_limit': 99},
                },
            ],
        })
        by_type = {section['type']: section['value'] for section in payload['sections']}
        self.assertEqual(by_type['featured_collections']['items'], [
            {'page_id': 12, 'override_title': 'Vibrators'},
        ])
        self.assertEqual(by_type['best_sellers']['product_limit'], 12)

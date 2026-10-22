"""
The generalized definitions are checked against the definitions read from the live store
(2026-10-22, read-only queries): the plan must keep every live field and only add.
"""

from django.test import SimpleTestCase, override_settings

from metaobjects.shopify_metaobjects.definition import MetaobjectDefinitionSpec
from shopify_content.sync import unified_definitions as ud


def _live(type_, fields, capabilities, definition_id):
    """Build a live definition the way MetaobjectClient.get_definition returns it."""
    raw_fields = []
    for entry in fields:
        key, field_type, *rest = entry
        raw_fields.append({
            'key': key,
            'name': key,
            'type': {'name': field_type},
            'required': bool(rest and rest[0]),
            'validations': rest[1] if len(rest) > 1 else [],
        })
    return MetaobjectDefinitionSpec.from_dict({
        'id': definition_id, 'type': type_, 'name': type_,
        'fieldDefinitions': raw_fields, 'capabilities': capabilities,
    })


LIVE_FAQ = _live(
    'faq',
    [('question', 'single_line_text_field'), ('answer', 'rich_text_field')],
    {'publishable': {'enabled': True}, 'onlineStore': {'enabled': False}, 'renderable': {'enabled': False}},
    'gid://shopify/MetaobjectDefinition/FAQ',
)

LIVE_REGION = _live(
    'region',
    [
        ('province', 'single_line_text_field', True),
        ('province_code', 'single_line_text_field', True,
         [{'name': 'min', 'value': '2'}, {'name': 'max', 'value': '2'}]),
        ('country', 'single_line_text_field', False, [{'name': 'choices', 'value': '["Canada"]'}]),
        ('greeting', 'multi_line_text_field'),
        ('header1', 'single_line_text_field'),
        ('header2', 'single_line_text_field'),
        ('location_pages', 'list.metaobject_reference', False,
         [{'name': 'metaobject_definition_id', 'value': 'gid://shopify/MetaobjectDefinition/6170968139'}]),
        ('metatitulo', 'single_line_text_field', True),
        ('metadescription', 'multi_line_text_field', True),
    ],
    {
        'publishable': {'enabled': True},
        'onlineStore': {'enabled': True, 'data': {'urlHandle': 'canada'}},
        'renderable': {'enabled': True, 'data': {
            'metaTitleKey': 'metatitulo', 'metaDescriptionKey': 'metadescription'}},
    },
    'gid://shopify/MetaobjectDefinition/6200819787',
)

LIVE_LOCATION = _live(
    'location_page',
    [
        ('city', 'single_line_text_field'),
        ('province', 'single_line_text_field'),
        ('province_page', 'metaobject_reference', False,
         [{'name': 'metaobject_definition_id', 'value': 'gid://shopify/MetaobjectDefinition/6200819787'}]),
        ('country', 'single_line_text_field'),
        ('header1', 'single_line_text_field'),
        ('header2', 'single_line_text_field'),
        ('greeting', 'multi_line_text_field'),
        ('discreet_shipping', 'multi_line_text_field'),
        ('quality_focus', 'multi_line_text_field'),
        ('body_safe_materials', 'multi_line_text_field'),
        ('meta_description', 'multi_line_text_field'),
        ('meta_titulo', 'single_line_text_field'),
        ('seo_keyword', 'metaobject_reference', False,
         [{'name': 'metaobject_definition_id', 'value': 'gid://shopify/MetaobjectDefinition/9751298123'}]),
    ],
    {
        'publishable': {'enabled': True},
        'onlineStore': {'enabled': True, 'data': {'urlHandle': 'canada-location'}},
        'renderable': {'enabled': True, 'data': {
            'metaTitleKey': 'meta_titulo', 'metaDescriptionKey': 'meta_description'}},
    },
    'gid://shopify/MetaobjectDefinition/6170968139',
)


class FakeClient:
    """Stands in for MetaobjectClient. Records every write; reads come from `definitions`."""

    def __init__(self, definitions):
        self.definitions = dict(definitions)
        self.writes = []

    def get_definition(self, type_):
        return self.definitions.get(type_)

    def create_definition(self, spec):
        self.writes.append(('create', spec.type, [f.key for f in spec.fields]))
        created = MetaobjectDefinitionSpec.from_dict({
            'id': f'gid://shopify/MetaobjectDefinition/new-{spec.type}', 'type': spec.type,
            'fieldDefinitions': [f.to_shopify_input() for f in spec.fields],
        })
        self.definitions[spec.type] = created
        return created

    def update_definition(self, definition_id, *, fields=None, capabilities=None, field_validations=None):
        self.writes.append((
            'update', definition_id, [f.key for f in fields or []], capabilities, field_validations,
        ))
        return None


LIVE_STORE = {'faq': LIVE_FAQ, 'region': LIVE_REGION, 'location_page': LIVE_LOCATION}


def _specs():
    return {spec.type: spec for spec in ud.build_definitions()}


class SpecsKeepTheLiveFieldsTests(SimpleTestCase):
    def test_every_live_field_is_kept_with_the_same_type(self):
        specs = _specs()
        for live in (LIVE_FAQ, LIVE_REGION, LIVE_LOCATION):
            wanted = {f.key: f.type for f in specs[live.type].fields}
            for live_field in live.fields:
                self.assertEqual(
                    wanted.get(live_field.key), live_field.type,
                    f'{live.type}.{live_field.key} must keep its live type',
                )

    def test_live_capabilities_and_url_handles_are_unchanged(self):
        specs = _specs()
        self.assertEqual(specs['region'].capabilities['onlineStore']['data']['urlHandle'], 'canada')
        self.assertEqual(specs['location_page'].capabilities['onlineStore']['data']['urlHandle'], 'canada-location')

    @override_settings(REGION_PAGE_URL_HANDLE='regions', LOCATION_PAGE_URL_HANDLE='locations')
    def test_url_handles_are_explicit_settings_only(self):
        specs = _specs()
        self.assertEqual(specs['region'].capabilities['onlineStore']['data']['urlHandle'], 'regions')
        self.assertEqual(specs['location_page'].capabilities['onlineStore']['data']['urlHandle'], 'locations')

    def test_region_country_gains_the_united_states(self):
        country = next(f for f in _specs()['region'].fields if f.key == 'country')
        self.assertEqual(country.validations, [{'name': 'choices', 'value': ['Canada', 'United States']}])

    def test_location_page_carries_the_us_layout_under_clean_names(self):
        keys = {f.key for f in _specs()['location_page'].fields}
        self.assertTrue({
            'slug', 'locale', 'intro', 'section2_title', 'section2_content', 'section3_title',
            'brand_section_content', 'map_content', 'after_page_content', 'faqs',
        } <= keys)
        legacy_names = {'titulo', 'subtitulo', 'titulo_2', 'subtitulo_h2', 'content_2', 'state'}
        self.assertFalse(legacy_names & keys, 'legacy local_page names are not repeated')

    def test_faqs_are_references_to_faq_entries_not_json(self):
        for spec in ud.build_definitions():
            faqs = [f for f in spec.fields if f.key == 'faqs']
            for spec_field in faqs:
                self.assertEqual(spec_field.type, 'list.metaobject_reference', spec.type)
                self.assertEqual(spec_field.validations[0]['value'], '<definition:faq>')
        self.assertFalse(
            [f for spec in ud.build_definitions() for f in spec.fields if f.type == 'json'],
            'no JSON fields in the generalized definitions',
        )

    def test_content_links_replaces_the_loose_related_metafields(self):
        keys = {f.key for f in _specs()['content_links'].fields}
        self.assertEqual(keys, {
            'title', 'related_products', 'related_collections', 'related_articles',
            'related_glossary_terms', 'internal_links', 'faqs',
        })


class PlanTests(SimpleTestCase):
    def test_plan_only_adds_to_the_live_definitions(self):
        plans = {plan.type: plan for plan in ud.plan_definitions(FakeClient(LIVE_STORE))}

        self.assertEqual(plans['faq'].action, 'unchanged')

        self.assertEqual(plans['region'].action, 'update')
        self.assertEqual(sorted(plans['region'].missing_fields), ['faqs', 'locale'])
        self.assertEqual(list(plans['region'].changed_validations), ['country'])
        self.assertEqual(plans['region'].capability_changes, {})

        self.assertEqual(plans['location_page'].action, 'update')
        missing = set(plans['location_page'].missing_fields)
        self.assertIn('section2_title', missing)
        self.assertIn('faqs', missing)
        self.assertFalse(missing & {f.key for f in LIVE_LOCATION.fields}, 'existing fields are never re-added')
        self.assertEqual(plans['location_page'].changed_validations, {})

        self.assertEqual(plans['content_links'].action, 'create')

    def test_a_store_that_already_has_everything_is_unchanged(self):
        client = FakeClient(LIVE_STORE)
        specs = {spec.type: spec for spec in ud.build_definitions(lambda t: f'gid://x/{t}')}
        # Pretend the generalized definitions were already applied.
        for type_, spec in specs.items():
            client.definitions[type_] = MetaobjectDefinitionSpec.from_dict({
                'id': f'gid://x/{type_}', 'type': type_,
                'fieldDefinitions': [f.to_shopify_input() for f in spec.fields],
                'capabilities': spec.capabilities,
            })
        self.assertEqual({p.action for p in ud.plan_definitions(client)}, {'unchanged'})

    def test_planning_never_writes(self):
        client = FakeClient(LIVE_STORE)
        ud.plan_definitions(client)
        self.assertEqual(client.writes, [])


class ApplyGuardTests(SimpleTestCase):
    def test_apply_is_refused_by_default_and_writes_nothing(self):
        client = FakeClient(LIVE_STORE)
        with self.assertRaises(ud.SchemaChangesDisabled):
            ud.apply_definitions(client)
        self.assertEqual(client.writes, [])

    @override_settings(SHOPIFY_SCHEMA_CHANGES_ENABLED=True)
    def test_apply_extends_live_definitions_and_creates_the_missing_one(self):
        client = FakeClient(LIVE_STORE)
        applied = ud.apply_definitions(client)

        by_action = {}
        for write in client.writes:
            by_action.setdefault((write[0], write[1]), write)
        self.assertIn(('create', 'content_links'), by_action)

        region_update = next(w for w in client.writes if w[0] == 'update' and w[1] == LIVE_REGION.id)
        self.assertEqual(sorted(region_update[2]), ['faqs', 'locale'])
        self.assertEqual(list(region_update[4]), ['country'])
        self.assertTrue({p.type for p in applied} >= {'region', 'location_page', 'content_links'})

        self.assertFalse(
            [w for w in client.writes if w[0] == 'update' and w[1] == LIVE_FAQ.id],
            'the unchanged faq definition is not touched',
        )

    @override_settings(SHOPIFY_SCHEMA_CHANGES_ENABLED=True)
    def test_a_fresh_store_gets_references_on_the_second_pass(self):
        client = FakeClient({})
        ud.apply_definitions(client)

        creates = {w[1]: w[2] for w in client.writes if w[0] == 'create'}
        self.assertEqual(list(creates), ['faq', 'location_page', 'region', 'content_links'])
        # location_page is created before region exists, and region before location_page has
        # its pointer: the circular references arrive in the second pass.
        self.assertNotIn('province_page', creates['location_page'])
        added_later = [w for w in client.writes if w[0] == 'update']
        added_keys = {key for w in added_later for key in w[2]}
        self.assertIn('province_page', added_keys)

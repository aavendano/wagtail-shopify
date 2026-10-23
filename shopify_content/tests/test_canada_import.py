import json
from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.test import SimpleTestCase
from wagtail.models import Locale

from shopify_content.models import LocationPage, RegionPage
from shopify_content.sync import canada_inbound as ci

from .test_region_page import RegionPageTestCase

ONTARIO = 'gid://shopify/Metaobject/163059269707'
QUEBEC = 'gid://shopify/Metaobject/174101626955'
NOVA_SCOTIA = 'gid://shopify/Metaobject/163262890059'
AJAX = 'gid://shopify/Metaobject/162883567691'
MONTREAL = 'gid://shopify/Metaobject/174101364811'
HALIFAX = 'gid://shopify/Metaobject/163387179083'
LOOSE = 'gid://shopify/Metaobject/999'


def _node(gid, handle, type_, fields, status='ACTIVE', references=None):
    """A node shaped like the Admin API answer (read from the live store, 2026-10-23)."""
    references = references or {}
    return {
        'id': gid, 'handle': handle, 'type': type_,
        'capabilities': {'publishable': {'status': status}},
        'fields': [
            {'key': key, 'value': value, 'reference': references.get(key)}
            for key, value in fields.items()
        ],
    }


def region(gid, handle, name, code, country, location_gids, **extra):
    fields = {
        'province': name, 'province_code': code, 'country': country, 'header1': None, 'header2': None,
        'greeting': f'Ready to ignite passion, {name}?', 'metatitulo': f'Sex Toys {name}',
        'metadescription': f'Shop in {name}', 'location_pages': json.dumps(location_gids),
    }
    fields.update(extra)
    return _node(gid, handle, 'region', fields)


def location(gid, handle, city, province, **extra):
    status = extra.pop('status', 'ACTIVE')
    references = extra.pop('references', None)
    fields = {
        'city': city, 'province': province, 'province_page': None, 'country': 'Canada',
        'header1': f'Adult Toys & Sex Shop {city}', 'header2': 'Your Premier Online Sex Toy Shop',
        'greeting': 'Hello!\n\nPrivacy <b>matters</b>.\nPlain packaging.',
        'discreet_shipping': 'Plain, unmarked packaging.', 'quality_focus': 'Curated.',
        'body_safe_materials': 'Medical-grade silicone.', 'meta_description': f'Best {city} sex toys.',
        'meta_titulo': f'Adult Toys {city} | PlayLoveToys', 'seo_keyword': None,
    }
    fields.update(extra)
    return _node(gid, handle, 'location_page', fields, status=status, references=references)


REGIONS = [
    region(ONTARIO, 'ontario', 'Ontario', 'ON', 'Canada', [AJAX]),
    region(QUEBEC, 'quebec', 'Quebec', 'QC', 'Canada', [MONTREAL]),
    region(NOVA_SCOTIA, 'nova-scotia', 'Nova Scotia', 'NS', None, [HALIFAX]),
]
LOCATIONS = [
    location(AJAX, 'ajax', 'Ajax', 'Ontario'),
    location(MONTREAL, 'montreal', 'Montreal', 'Quebec'),
    location(HALIFAX, 'halifax', 'Halifax', 'Nova Scotia'),
]


class BuildPlanTests(SimpleTestCase):
    def test_parent_comes_from_the_region_list_not_from_the_location(self):
        # Ajax says it is in Quebec, but the Ontario region lists it: the region wins.
        wrong = location(AJAX, 'ajax', 'Ajax', 'Quebec')
        plan = ci.build_plan(REGIONS[:2], [wrong])
        self.assertEqual(plan.locations[0].region_gid, ONTARIO)

    def test_falls_back_to_province_page_then_province_name(self):
        by_page = location(LOOSE, 'a', 'A', 'Nowhere', province_page=QUEBEC)
        by_name = location(LOOSE + '1', 'b', 'B', 'ontario')
        plan = ci.build_plan(REGIONS, [by_page, by_name])
        self.assertEqual([l.region_gid for l in plan.locations], [QUEBEC, ONTARIO])
        self.assertEqual(plan.unparented, [])

    def test_unlisted_location_is_unparented_and_reported(self):
        plan = ci.build_plan(REGIONS, [location(LOOSE, 'orphan', 'Orphan', 'Atlantis')])
        self.assertEqual([l.handle for l in plan.unparented], ['orphan'])
        self.assertIn('orphan', plan.warnings[0])

    def test_inactive_and_nameless_entries_are_skipped(self):
        draft = location(LOOSE, 'draft', 'Draft', 'Ontario', status='DRAFT')
        nameless = location(LOOSE + '1', 'x', '', 'Ontario')
        plan = ci.build_plan(REGIONS, [draft, nameless])
        self.assertEqual((plan.locations, plan.skipped), ([], 2))

    def test_country_is_inferred_from_the_province_code_when_missing(self):
        plan = ci.build_plan(REGIONS, [])
        self.assertEqual({r.name: r.country for r in plan.regions}['Nova Scotia'], 'Canada')

    def test_two_regions_listing_one_location_keeps_the_first_and_warns(self):
        twice = [
            region(ONTARIO, 'ontario', 'Ontario', 'ON', 'Canada', [AJAX]),
            region(QUEBEC, 'quebec', 'Quebec', 'QC', 'Canada', [AJAX]),
        ]
        plan = ci.build_plan(twice, [LOCATIONS[0]])
        self.assertEqual(plan.locations[0].region_gid, ONTARIO)
        self.assertTrue(plan.warnings)

    def test_seo_keyword_is_read_from_the_referenced_entry(self):
        reference = {'id': 'gid://x', 'type': 'seo_keyword', 'handle': 'k',
                     'fields': [{'key': 'keyword', 'value': 'sex shop ajax'}]}
        node = location(AJAX, 'ajax', 'Ajax', 'Ontario', references={'seo_keyword': reference},
                        seo_keyword='gid://x')
        self.assertEqual(ci.parse_location(node).seo_keyword, 'sex shop ajax')

    def test_plain_text_becomes_escaped_paragraphs(self):
        html = ci.plain_text_to_html('One <b>two</b>\nthree\n\nFour')
        self.assertEqual(html, '<p>One &lt;b&gt;two&lt;/b&gt;<br>three</p>\n\n<p>Four</p>')
        self.assertEqual(ci.plain_text_to_html('  '), '')


class ImportCanadaTests(RegionPageTestCase):
    def setUp(self):
        super().setUp()
        self.ca = Locale.objects.get(language_code='en-CA')

    def _import(self, regions=None, locations=None, **kwargs):
        plan = ci.build_plan(regions if regions is not None else REGIONS,
                             locations if locations is not None else LOCATIONS)
        return ci.import_canada_locations(None, self.root, plan=plan, **kwargs)

    def test_regions_and_locations_are_created_with_the_region_as_parent(self):
        stats = self._import()
        self.assertEqual(stats['regions']['created'], 3)
        self.assertEqual(stats['locations']['created'], 3)

        ontario = RegionPage.objects.get(shopify_id=ONTARIO)
        self.assertEqual((ontario.title, ontario.region_code, ontario.country), ('Ontario', 'ON', 'Canada'))
        self.assertEqual((ontario.handle, ontario.slug, ontario.locale), ('ontario', 'en-ca-ontario', self.ca))
        self.assertEqual(ontario.search_description, 'Shop in Ontario')
        self.assertEqual([p.city for p in ontario.location_pages], ['Ajax'])

        ajax = LocationPage.objects.get(shopify_id=AJAX)
        self.assertEqual(ajax.get_parent().pk, ontario.pk)
        self.assertEqual((ajax.state, ajax.country, ajax.city), ('Ontario', 'Canada', 'Ajax'))
        self.assertEqual(ajax.titulo, 'Adult Toys & Sex Shop Ajax')
        self.assertEqual(ajax.discreet_shipping, 'Plain, unmarked packaging.')
        self.assertEqual(ajax.seo_title, 'Adult Toys Ajax | PlayLoveToys')
        self.assertEqual(ajax.search_description, 'Best Ajax sex toys.')
        self.assertIn('&lt;b&gt;matters&lt;/b&gt;', ajax.intro)

    def test_the_handle_the_store_uses_is_kept_even_after_an_editor_saves(self):
        self._import()
        ajax = LocationPage.objects.get(shopify_id=AJAX)
        self.assertEqual(ajax.handle, 'ajax')
        self.assertEqual(ajax.slug, 'en-ca-ajax-ontario', 'the Wagtail slug stays canonical')

        ajax.quality_focus = 'Edited by an editor.'
        ajax.full_clean()
        ajax.save()
        self.assertEqual(LocationPage.objects.get(pk=ajax.pk).handle, 'ajax')

    def test_imported_pages_are_never_synced_to_shopify(self):
        with mock.patch('shopify_content.sync.publish_sync.enqueue_page_outbound_sync') as enqueue:
            self._import()
        enqueue.assert_not_called()
        self.assertFalse(LocationPage.objects.filter(sync_enabled=True).exists())
        self.assertFalse(RegionPage.objects.filter(sync_enabled=True).exists())

    def test_existing_store_copy_is_not_rejected_by_the_editorial_check(self):
        text = location(AJAX, 'ajax', 'Ajax', 'Ontario', quality_focus='Stop by and see us')
        self._import(locations=[text])
        self.assertEqual(LocationPage.objects.get(shopify_id=AJAX).quality_focus, 'Stop by and see us')

    def test_rerun_updates_in_place_and_is_idempotent(self):
        self._import()
        changed = location(AJAX, 'ajax', 'Ajax', 'Ontario', header2='A new subtitle')
        stats = self._import(locations=[changed, LOCATIONS[1], LOCATIONS[2]])

        self.assertEqual(stats['locations'], {'created': 0, 'updated': 3, 'skipped': 0, 'errors': 0})
        self.assertEqual(LocationPage.objects.count(), 3)
        self.assertEqual(RegionPage.objects.count(), 3)
        self.assertEqual(LocationPage.objects.get(shopify_id=AJAX).subtitulo, 'A new subtitle')

    def test_new_only_leaves_existing_pages_alone(self):
        self._import()
        changed = location(AJAX, 'ajax', 'Ajax', 'Ontario', header2='A new subtitle')
        stats = self._import(locations=[changed], new_only=True)
        self.assertEqual(stats['locations']['skipped'], 1)
        self.assertNotEqual(LocationPage.objects.get(shopify_id=AJAX).subtitulo, 'A new subtitle')

    def test_a_loose_location_moves_under_its_region_when_the_region_lists_it(self):
        self._import(regions=[], locations=[LOCATIONS[0]])
        self.assertEqual(LocationPage.objects.get(shopify_id=AJAX).get_parent().pk, self.root.pk)

        self._import()
        ajax = LocationPage.objects.get(shopify_id=AJAX)
        self.assertEqual(ajax.get_parent().specific.shopify_id, ONTARIO)

    def test_unlisted_location_is_kept_loose_under_the_root(self):
        orphan = location(LOOSE, 'orphan', 'Orphan', 'Atlantis')
        stats = self._import(locations=[orphan])
        self.assertEqual(stats['unparented'], 1)
        self.assertEqual(LocationPage.objects.get(shopify_id=LOOSE).get_parent().pk, self.root.pk)

    def test_dry_run_writes_nothing(self):
        stats = self._import(dry_run=True)
        self.assertEqual((stats['regions']['created'], stats['locations']['created']), (3, 3))
        self.assertEqual((RegionPage.objects.count(), LocationPage.objects.count()), (0, 0))

    def test_missing_wagtail_locale_is_an_error_not_a_silent_fallback(self):
        with self.assertRaises(ValueError):
            self._import(locale_code='en-ZZ')

    def test_nothing_in_the_import_calls_shopify_for_writing(self):
        # Reads go through _paginate only; there is no mutation helper in the module.
        source = ci.__file__
        with open(source) as handle:
            code = handle.read()
        for word in ('mutation', 'execute_admin_graphql', 'MetaobjectClient', '.upsert('):
            self.assertNotIn(word, code.replace('Read-only', ''), word)


class CommandTests(RegionPageTestCase):
    def test_command_reads_through_fetch_plan_and_reports(self):
        plan = ci.build_plan(REGIONS, LOCATIONS)
        out = StringIO()
        with mock.patch('shopify_content.management.commands.import_canada_locations.fetch_plan', return_value=plan), \
                mock.patch('shopify_content.management.commands.import_canada_locations.resolve_shop_for_command_or_sole',
                           return_value='shop.example'), \
                mock.patch('shopify_content.management.commands.import_canada_locations.resolve_shopify_import_parent',
                           return_value=self.root):
            call_command('import_canada_locations', '--dry-run', stdout=out)
        text = out.getvalue()
        self.assertIn('Found 3 region(s) and 3 location(s)', text)
        self.assertIn('Dry run: nothing was written.', text)
        self.assertEqual(RegionPage.objects.count(), 0)

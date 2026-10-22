from io import StringIO

from django.core.management import call_command
from wagtail.models import Locale, Page

from shopify_content.models import LocationPage, RegionPage
from shopify_content.region_codes import region_code_for

from .test_region_page import RegionPageTestCase


class RegionCodeTests(RegionPageTestCase):
    def test_codes_for_provinces_and_states(self):
        self.assertEqual(region_code_for('Canada', 'Ontario'), 'ON')
        self.assertEqual(region_code_for('United States', 'Texas'), 'TX')
        self.assertEqual(region_code_for('United States', 'texas'), 'TX', 'case-insensitive')
        self.assertEqual(region_code_for('Canada', 'Atlantis'), '', 'unknown stays empty')


class OrganizeLocationRegionsTests(RegionPageTestCase):
    def _run(self, *args):
        out = StringIO()
        call_command('organize_location_regions', *args, stdout=out)
        return out.getvalue()

    def _loose(self, city, state, country='United States', locale=None):
        page = LocationPage(
            title=city, titulo=city, city=city, state=state, country=country,
            locale=locale or self.locale,
        )
        self.root.add_child(instance=page)
        page.save_revision().publish()
        return page

    def test_dry_run_writes_nothing(self):
        austin = self._loose('Austin', 'Texas')
        output = self._run()

        self.assertIn('Dry run', output)
        self.assertEqual(RegionPage.objects.count(), 0)
        self.assertEqual(LocationPage.objects.get(pk=austin.pk).get_parent().pk, self.root.pk)

    def test_apply_creates_regions_and_moves_locations(self):
        austin = self._loose('Austin', 'Texas')
        houston = self._loose('Houston', 'Texas')
        toronto = self._loose('Toronto', 'Ontario', country='Canada')
        self._run('--apply')

        texas = RegionPage.objects.get(slug='en-us-texas')
        self.assertEqual((texas.title, texas.country, texas.region_code), ('Texas', 'United States', 'TX'))
        self.assertTrue(texas.live)
        self.assertEqual(
            {LocationPage.objects.get(pk=p.pk).get_parent().pk for p in (austin, houston)},
            {texas.pk},
        )
        ontario = RegionPage.objects.get(slug='en-us-ontario')
        self.assertEqual((ontario.country, ontario.region_code), ('Canada', 'ON'))
        self.assertEqual(LocationPage.objects.get(pk=toronto.pk).get_parent().pk, ontario.pk)

    def test_apply_keeps_handles_and_does_not_touch_shopify_state(self):
        austin = self._loose('Austin', 'Texas')
        before = (austin.handle, austin.slug, austin.shopify_id)
        self._run('--apply')
        austin = LocationPage.objects.get(pk=austin.pk)
        self.assertEqual((austin.handle, austin.slug, austin.shopify_id), before)

    def test_apply_is_idempotent(self):
        self._loose('Austin', 'Texas')
        self._run('--apply')
        output = self._run('--apply')

        self.assertEqual(RegionPage.objects.count(), 1)
        self.assertIn('0 region(s) created', output)
        self.assertIn('0 location(s) moved', output)

    def test_new_loose_location_joins_the_existing_region(self):
        self._loose('Austin', 'Texas')
        self._run('--apply')
        dallas = self._loose('Dallas', 'Texas')
        self._run('--apply')

        texas = RegionPage.objects.get(slug='en-us-texas')
        self.assertEqual(RegionPage.objects.count(), 1)
        self.assertEqual(LocationPage.objects.get(pk=dallas.pk).get_parent().pk, texas.pk)

    def test_locations_without_a_state_are_skipped(self):
        orphan = self._loose('Nowhere', '')
        output = self._run('--apply')

        self.assertEqual(RegionPage.objects.count(), 0)
        self.assertEqual(LocationPage.objects.get(pk=orphan.pk).get_parent().pk, self.root.pk)
        self.assertIn('skipped', output)

    def test_each_locale_gets_its_own_region(self):
        spanish = Locale.objects.get(language_code='es-US')
        self._loose('Austin', 'Texas')
        self._loose('Austin', 'Texas', locale=spanish)
        self._run('--apply')

        self.assertEqual(
            sorted(RegionPage.objects.values_list('slug', flat=True)),
            ['en-us-texas', 'es-us-texas'],
        )
        self.assertEqual(
            {region.locale.language_code for region in RegionPage.objects.all()},
            {'en-US', 'es-US'},
        )

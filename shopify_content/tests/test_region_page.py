from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from wagtail.models import Locale, Page

from shopify_content.models import LocationPage, RegionPage, ShopifyRootPage


class RegionPageTestCase(TestCase):
    def setUp(self):
        for lang in ('en-US', 'es-US', 'en-CA', 'fr-CA'):
            Locale.objects.get_or_create(language_code=lang)
        self.locale = Locale.objects.get(language_code='en-US')
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=self.locale))
        self.root = ShopifyRootPage(title='Local', slug='local-us', locale=self.locale)
        home.add_child(instance=self.root)
        self.root.save_revision().publish()

    def _region(self, title='Texas', slug='texas', **extra):
        extra.setdefault('country', 'United States')
        extra.setdefault('region_code', 'TX')
        region = RegionPage(title=title, slug=slug, locale=self.locale, **extra)
        self.root.add_child(instance=region)
        region.save_revision().publish()
        return region

    def _location(self, parent, city, **extra):
        page = LocationPage(
            title=city, titulo=city, city=city, locale=self.locale,
            **extra,
        )
        parent.add_child(instance=page)
        page.save_revision().publish()
        return page


class RegionTreeRulesTests(RegionPageTestCase):
    def test_region_lives_under_a_root_and_holds_locations(self):
        self.assertEqual(RegionPage.parent_page_types, ['shopify_content.ShopifyRootPage'])
        self.assertEqual(RegionPage.subpage_types, ['shopify_content.LocationPage'])
        self.assertIn('shopify_content.RegionPage', ShopifyRootPage.subpage_types)
        self.assertIn('shopify_content.RegionPage', LocationPage.parent_page_types)

    def test_location_can_still_hang_off_a_root_during_the_transition(self):
        self.assertIn('shopify_content.ShopifyRootPage', LocationPage.parent_page_types)

    def test_region_cannot_be_created_under_a_plain_page(self):
        plain = Page.objects.first()
        self.assertFalse(RegionPage.can_create_at(plain))
        self.assertTrue(RegionPage.can_create_at(self.root))


class RegionPageTests(RegionPageTestCase):
    def test_handle_defaults_to_slug_and_sync_is_off(self):
        region = self._region()
        self.assertEqual(region.handle, 'texas')
        self.assertFalse(region.sync_enabled)

    def test_region_code_is_normalized_and_validated(self):
        region = self._region(region_code='tx')
        region.clean()
        self.assertEqual(region.region_code, 'TX')

        region.region_code = 'TEX'
        with self.assertRaises(ValidationError) as ctx:
            region.clean()
        self.assertIn('region_code', ctx.exception.message_dict)

    def test_location_pages_lists_live_children_by_city(self):
        region = self._region()
        self._location(region, 'Houston', state='Texas')
        self._location(region, 'Austin', state='Texas')
        draft = LocationPage(title='Dallas', titulo='Dallas', city='Dallas', locale=self.locale, live=False)
        region.add_child(instance=draft)

        self.assertEqual(
            [page.city for page in region.location_pages],
            ['Austin', 'Houston'],
            'live children only, ordered by city',
        )


class LocationRegionTests(RegionPageTestCase):
    def test_region_property_follows_the_parent(self):
        region = self._region()
        under_region = self._location(region, 'Austin')
        under_root = self._location(self.root, 'Orphan')

        self.assertEqual(under_region.region.pk, region.pk)
        self.assertIsNone(under_root.region)

    def test_clean_takes_state_and_country_from_the_region(self):
        region = self._region(title='Texas', country='United States')
        page = LocationPage(title='Austin', titulo='Austin', city='Austin', locale=self.locale,
                            state='wrong', country='Canada')
        region.add_child(instance=page)
        page.clean()

        self.assertEqual(page.state, 'Texas')
        self.assertEqual(page.country, 'United States')
        self.assertEqual(page.slug, 'en-us-austin-texas', 'handle scheme is unchanged')

    def test_clean_leaves_a_page_under_a_root_alone(self):
        page = LocationPage(title='Austin', titulo='Austin', city='Austin', locale=self.locale,
                            state='Texas', country='United States')
        self.root.add_child(instance=page)
        page.clean()
        self.assertEqual(page.state, 'Texas')
        self.assertEqual(page.country, 'United States')

    def test_canadian_service_messaging_fields_are_stored(self):
        region = self._region(title='Ontario', slug='ontario', country='Canada', region_code='ON')
        page = self._location(
            region, 'Ajax',
            discreet_shipping='Plain packaging.', quality_focus='Curated.',
            body_safe_materials='Medical-grade silicone.', seo_keyword='sex shop ajax',
        )
        page.refresh_from_db()
        self.assertEqual(page.discreet_shipping, 'Plain packaging.')
        self.assertEqual(page.seo_keyword, 'sex shop ajax')

    def test_forbidden_phrases_are_checked_in_the_new_text_fields(self):
        from shopify_content.content_templates.location_city_en_us import FORBIDDEN_PHRASES

        phrase = next(iter(FORBIDDEN_PHRASES))
        region = self._region()
        page = LocationPage(title='Austin', titulo='Austin', city='Austin', locale=self.locale,
                            quality_focus=f'Visit our {phrase} today')
        with self.assertRaises(ValidationError) as ctx:
            region.add_child(instance=page)
        self.assertIn(phrase, str(ctx.exception))


class RegionAdminAndPreviewTests(RegionPageTestCase):
    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_superuser('admin', 'a@example.com', 'pw-region-123')
        self.client.force_login(self.user)

    def test_admin_edit_screens_render_for_region_and_location(self):
        region = self._region()
        location = self._location(region, 'Austin', state='Texas')
        for page in (region, location):
            response = self.client.get(f'/admin/pages/{page.pk}/edit/')
            self.assertEqual(response.status_code, 200, page)

    def test_templates_render_with_region_links(self):
        region = self._region()
        location = self._location(region, 'Austin', state='Texas')
        region_response = self.client.get(f'/admin/pages/{region.pk}/view_draft/')
        location_response = self.client.get(f'/admin/pages/{location.pk}/view_draft/')
        self.assertEqual(region_response.status_code, 200)
        self.assertContains(region_response, 'Austin')
        self.assertEqual(location_response.status_code, 200)
        self.assertContains(location_response, 'Texas')

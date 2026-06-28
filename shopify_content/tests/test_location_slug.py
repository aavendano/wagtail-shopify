from django.test import TestCase
from wagtail.models import Locale, Page

from shopify_content.location_slug import location_page_slug
from shopify_content.models import LocationPage, ShopifyRootPage


class LocationPageSlugTests(TestCase):
    def setUp(self):
        for lang in ('en-US', 'es-US', 'en-CA', 'fr-CA'):
            Locale.objects.get_or_create(language_code=lang)
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.parent = ShopifyRootPage(title='Root', slug='root', locale=locale)
        home.add_child(instance=self.parent)
        self.parent.save_revision().publish()

    def _page(self, *, city, locale_code='en-US', shopify_locale='', state=''):
        locale = Locale.objects.get(language_code=locale_code)
        return LocationPage(
            title=city,
            titulo=city,
            city=city,
            state=state,
            shopify_locale=shopify_locale,
            locale=locale,
        )

    def test_en_ca_montreal(self):
        page = self._page(city='Montreal', locale_code='en-CA')
        self.assertEqual(location_page_slug(page), 'en-ca-montreal')

    def test_fr_ca_montreal(self):
        page = self._page(city='Montreal', locale_code='fr-CA')
        self.assertEqual(location_page_slug(page), 'fr-ca-montreal')

    def test_en_us_new_york(self):
        page = self._page(city='New York', locale_code='en-US')
        self.assertEqual(location_page_slug(page), 'en-us-new-york')

    def test_es_us_new_york(self):
        page = self._page(city='New York', locale_code='es-US')
        self.assertEqual(location_page_slug(page), 'es-us-new-york')

    def test_shopify_locale_override(self):
        page = self._page(city='Montreal', locale_code='en-US', shopify_locale='fr-CA')
        self.assertEqual(location_page_slug(page), 'fr-ca-montreal')

    def test_missing_city_returns_empty(self):
        page = self._page(city='', locale_code='en-US')
        self.assertEqual(location_page_slug(page), '')

    def test_clean_sets_slug_and_handle(self):
        page = self._page(city='Austin', state='Texas', locale_code='en-US')
        self.parent.add_child(instance=page)
        page.clean()
        self.assertEqual(page.slug, 'en-us-austin-texas')
        self.assertEqual(page.handle, 'en-us-austin-texas')

    def test_homonymous_cities_differ_by_state(self):
        glendale_az = self._page(city='Glendale', state='Arizona', locale_code='en-US')
        glendale_ca = self._page(city='Glendale', state='California', locale_code='en-US')
        self.assertEqual(location_page_slug(glendale_az), 'en-us-glendale-arizona')
        self.assertEqual(location_page_slug(glendale_ca), 'en-us-glendale-california')
        self.assertNotEqual(location_page_slug(glendale_az), location_page_slug(glendale_ca))

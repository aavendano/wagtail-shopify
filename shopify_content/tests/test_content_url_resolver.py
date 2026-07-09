from django.test import TestCase
from wagtail.models import Locale, Page

from shopify_content.content_url_index import rebuild_index_for_page
from shopify_content.content_url_resolver import normalize_url, resolve_url
from shopify_content.models import GlossaryTermPage, ShopifyRootPage


def _locale(code: str) -> Locale:
    locale, _ = Locale.objects.get_or_create(language_code=code)
    return locale


class NormalizeUrlTests(TestCase):
    def test_strips_domain_and_query(self):
        path, prefix = normalize_url(
            'https://playlovetoys.com/pages/glossary/alpha?utm=1',
            property_url='https://playlovetoys.com/',
        )
        self.assertEqual(path, '/pages/glossary/alpha')
        self.assertEqual(prefix, '')

    def test_detects_locale_prefix(self):
        path, prefix = normalize_url(
            'https://playlovetoys.com/es-us/pages/glossary/alpha',
        )
        self.assertEqual(path, '/pages/glossary/alpha')
        self.assertEqual(prefix, 'es-us')

    def test_strips_trailing_slash(self):
        path, prefix = normalize_url('/products/toy/')
        self.assertEqual(path, '/products/toy')
        self.assertEqual(prefix, '')


class ResolveUrlTests(TestCase):
    def setUp(self):
        locale = _locale('en-US')
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.parent = ShopifyRootPage(title='Glossary', slug='glossary', locale=locale)
        home.add_child(instance=self.parent)
        self.parent.save_revision().publish()

        self.term = GlossaryTermPage(
            title='Alpha',
            term='Alpha',
            slug='alpha',
            handle='alpha',
            locale_code='en',
            shopify_id='gid://shopify/Metaobject/1',
            locale=locale,
        )
        self.parent.add_child(instance=self.term)
        self.term.save_revision().publish()
        rebuild_index_for_page(self.term)

    def test_resolves_canonical_url(self):
        match = resolve_url('https://playlovetoys.com/pages/glossary/alpha')
        self.assertIsNotNone(match)
        self.assertEqual(match.wagtail_page_id, self.term.pk)
        self.assertEqual(match.content_type, 'glossary_term')
        self.assertEqual(match.match_quality, 'exact')

    def test_resolves_prefixed_url(self):
        match = resolve_url('https://playlovetoys.com/es-us/pages/glossary/alpha')
        self.assertIsNotNone(match)
        self.assertEqual(match.wagtail_page_id, self.term.pk)

    def test_returns_none_for_unmapped(self):
        self.assertIsNone(resolve_url('https://playlovetoys.com/cart'))

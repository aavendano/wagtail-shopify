from django.test import TestCase
from wagtail.models import Locale, Page

from shopify_content.content_url_index import rebuild_index_for_page
from shopify_content.models import GlossaryTermPage, ShopifyRootPage
from shopify_content.storefront_url_display import get_storefront_url_display


def _locale(code: str) -> Locale:
    locale, _ = Locale.objects.get_or_create(language_code=code)
    return locale


class StorefrontUrlDisplayTests(TestCase):
    def setUp(self):
        locale = _locale('en-US')
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.parent = ShopifyRootPage(title='Glossary', slug='glossary', locale=locale)
        home.add_child(instance=self.parent)
        self.parent.save_revision().publish()

    def test_computed_paths_when_not_indexed(self):
        page = GlossaryTermPage(
            title='Alpha',
            term='Alpha',
            slug='alpha',
            handle='alpha',
            locale_code='en',
            shopify_id='gid://shopify/Metaobject/1',
            locale=_locale('en-US'),
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()

        display = get_storefront_url_display(page)

        self.assertEqual(display['canonical_path'], '/pages/glossary/alpha')
        self.assertIn('/pages/glossary/alpha', display['paths'])
        self.assertFalse(display['indexed'])

    def test_indexed_paths_after_rebuild(self):
        page = GlossaryTermPage(
            title='Beta',
            term='Beta',
            slug='beta',
            handle='beta',
            locale_code='en',
            shopify_id='gid://shopify/Metaobject/2',
            locale=_locale('en-US'),
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()
        rebuild_index_for_page(page)

        display = get_storefront_url_display(page)

        self.assertTrue(display['indexed'])
        self.assertIn('/pages/glossary/beta', display['paths'])

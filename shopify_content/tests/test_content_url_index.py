from django.test import TestCase
from wagtail.models import Locale, Page

from shopify_content.content_url_index import (
    clear_index_for_page,
    rebuild_full_index,
    rebuild_index_for_page,
)
from shopify_content.models import ContentUrlIndex, GlossaryTermPage, ShopifyRootPage


def _locale(code: str) -> Locale:
    locale, _ = Locale.objects.get_or_create(language_code=code)
    return locale


class ContentUrlIndexTests(TestCase):
    def setUp(self):
        locale = _locale('en-US')
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.parent = ShopifyRootPage(title='Glossary', slug='glossary', locale=locale)
        home.add_child(instance=self.parent)
        self.parent.save_revision().publish()

    def _add_term(self, *, live=True, shopify_id='gid://shopify/Metaobject/1'):
        page = GlossaryTermPage(
            title='Alpha',
            term='Alpha',
            slug='alpha',
            handle='alpha',
            locale_code='en',
            shopify_id=shopify_id,
            locale=_locale('en-US'),
        )
        self.parent.add_child(instance=page)
        if live:
            page.save_revision().publish()
        else:
            page.save_revision()
        return page

    def test_rebuild_index_for_live_page_with_shopify_id(self):
        page = self._add_term()
        count = rebuild_index_for_page(page)
        self.assertGreaterEqual(count, 1)
        self.assertTrue(
            ContentUrlIndex.objects.filter(
                wagtail_page_id=page.pk,
                normalized_path='/pages/glossary/alpha',
            ).exists()
        )

    def test_skips_page_without_shopify_id(self):
        page = self._add_term(shopify_id='')
        count = rebuild_index_for_page(page)
        self.assertEqual(count, 0)
        self.assertEqual(ContentUrlIndex.objects.filter(wagtail_page_id=page.pk).count(), 0)

    def test_clear_index_for_page(self):
        page = self._add_term()
        rebuild_index_for_page(page)
        deleted = clear_index_for_page(page.pk)
        self.assertGreater(deleted, 0)
        self.assertEqual(ContentUrlIndex.objects.filter(wagtail_page_id=page.pk).count(), 0)

    def test_rebuild_full_index(self):
        self._add_term()
        stats = rebuild_full_index()
        self.assertGreater(stats['created'], 0)

    def test_publish_signal_updates_index(self):
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
        with self.captureOnCommitCallbacks(execute=True):
            page.save_revision().publish()

        self.assertTrue(
            ContentUrlIndex.objects.filter(
                wagtail_page_id=page.pk,
                normalized_path='/pages/glossary/beta',
            ).exists()
        )

    def test_unpublish_removes_index_rows(self):
        page = self._add_term()
        rebuild_index_for_page(page)
        page.unpublish()
        self.assertEqual(ContentUrlIndex.objects.filter(wagtail_page_id=page.pk).count(), 0)

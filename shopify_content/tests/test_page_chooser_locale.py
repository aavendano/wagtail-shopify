from django.db.models.query import QuerySet
from django.test import RequestFactory, TestCase
from django.urls import resolve
from wagtail.models import Locale, Page

from shopify_content.models.glossary import GlossaryTermPage
from shopify_content.page_chooser_locale import (
    _include_glossary_root_in_browse,
    install_page_chooser_browse_locale_fix,
    maybe_include_glossary_root_at_chooser_root,
)
from shopify_content.wagtail_hooks import filter_page_chooser_by_locale


class PageChooserLocaleFilterTests(TestCase):
    def test_filter_with_multi_page_type_and_locale_does_not_raise(self):
        request = RequestFactory().get(
            '/admin/choose-page/',
            {
                'homepage_locale': 'es-US',
                'page_type': (
                    'shopify_content.productpage,'
                    'shopify_content.collectionpage,'
                    'shopify_content.articlepage,'
                    'shopify_content.glossarytermpage,'
                    'shopify_content.blogpage'
                ),
            },
        )
        request.session = {}

        qs = filter_page_chooser_by_locale(Page.objects.all(), request)

        self.assertGreaterEqual(qs.count(), 0)

    def test_search_glossary_terms_does_not_break_autocomplete(self):
        request = RequestFactory().get(
            '/admin/choose-page/search/',
            {
                'homepage_locale': 'es-US',
                'page_type': 'shopify_content.glossarytermpage',
                'q': 'vibrador',
            },
        )
        request.session = {}
        request.resolver_match = resolve('/admin/choose-page/search/')

        pages = filter_page_chooser_by_locale(Page.objects.all(), request)
        pages = pages.exclude(depth=1).type(GlossaryTermPage).specific()
        try:
            results = pages.autocomplete('vibrador')
        except Exception as exc:
            self.fail(f'autocomplete raised: {exc}')
        self.assertGreaterEqual(results.count(), 0)

    def test_root_browse_includes_glossary_folder_for_non_en_home_locale(self):
        install_page_chooser_browse_locale_fix()

        glossary_root = Page.objects.filter(slug='glossary', locale__language_code='en-US').first()
        if glossary_root is None:
            self.skipTest('No en-US glossary root in database')

        es_locale = Locale.objects.get(language_code='es-US')
        request = RequestFactory().get(
            '/admin/choose-page/',
            {
                'homepage_locale': 'es-US',
                'locale': 'es-US',
                'page_type': 'shopify_content.glossarytermpage',
            },
        )
        request.session = {}
        request.resolver_match = resolve('/admin/choose-page/')

        maybe_include_glossary_root_at_chooser_root(request)
        self.assertTrue(_include_glossary_root_in_browse.get())

        root = Page.get_first_root_node()
        children = root.get_children().defer_streamfields().specific()
        children = filter_page_chooser_by_locale(children, request)
        filtered = children.filter(locale=es_locale)

        self.assertIn(glossary_root.pk, list(filtered.values_list('pk', flat=True)))

    def test_browse_inside_glossary_shows_editor_locale_terms(self):
        install_page_chooser_browse_locale_fix()

        glossary_root = Page.objects.filter(slug='glossary', locale__language_code='en-US').first()
        if glossary_root is None:
            self.skipTest('No en-US glossary root in database')

        es_locale = Locale.objects.get(language_code='es-US')
        params = {
            'homepage_locale': 'es-US',
            'page_type': 'shopify_content.glossarytermpage',
        }
        request = RequestFactory().get(f'/admin/choose-page/{glossary_root.pk}/', params)
        request.session = {}
        request.user = None
        request.resolver_match = resolve(f'/admin/choose-page/{glossary_root.pk}/')

        children = glossary_root.get_children().defer_streamfields().specific()
        children = filter_page_chooser_by_locale(children, request)
        filtered = children.filter(locale=es_locale)

        self.assertGreater(filtered.type(GlossaryTermPage).count(), 0)

    def test_browse_patch_installs_once(self):
        install_page_chooser_browse_locale_fix()
        from shopify_content import page_chooser_locale

        self.assertIsNotNone(page_chooser_locale._original_queryset_filter)
        self.assertIsNot(QuerySet.filter, page_chooser_locale._original_queryset_filter)

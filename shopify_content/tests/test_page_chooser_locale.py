from django.db.models.query import QuerySet
from django.test import RequestFactory, TestCase
from django.urls import resolve
from wagtail.models import Locale, Page

from shopify_content.models import CollectionPage, GlossaryTermPage, ShopifyRootPage
from shopify_content.page_chooser_locale import (
    _include_glossary_root_in_browse,
    install_page_chooser_browse_locale_fix,
    maybe_include_glossary_root_at_chooser_root,
)
from shopify_content.wagtail_hooks import filter_page_chooser_by_locale


class PageChooserLocaleFilterTests(TestCase):
    def setUp(self):
        self.locale_en = Locale.get_default()
        self.locale_es, _ = Locale.objects.get_or_create(language_code='es-US')

        site_root = Page.get_first_root_node()
        if site_root is None:
            site_root = Page.add_root(
                instance=Page(title='Site Home', slug='site-home', locale=self.locale_en)
            )
        self.site_root = site_root

        self.glossary_root = ShopifyRootPage.objects.filter(
            slug='glossary', locale=self.locale_en
        ).first()
        if self.glossary_root is None:
            self.glossary_root = ShopifyRootPage(
                title='Glossary',
                slug='glossary',
                locale=self.locale_en,
            )
            site_root.add_child(instance=self.glossary_root)
            self.glossary_root.save_revision().publish()

        self.term_en = GlossaryTermPage(
            title='Vibrator',
            slug='vibrator-chooser-en',
            handle='vibrator-chooser-en',
            term='Vibrator',
            locale_code='en',
            shopify_id='gid://shopify/Metaobject/chooser-en',
            locale=self.locale_en,
        )
        self.glossary_root.add_child(instance=self.term_en)
        self.term_en.save_revision().publish()

        self.term_es = GlossaryTermPage(
            title='Vibrador',
            slug='vibrador-chooser-es',
            handle='vibrador-chooser-es',
            term='Vibrador',
            locale_code='es',
            shopify_id='gid://shopify/Metaobject/chooser-es',
            locale=self.locale_es,
        )
        self.glossary_root.add_child(instance=self.term_es)
        self.term_es.save_revision().publish()

        cms_home = ShopifyRootPage.objects.filter(slug='cms-home').first()
        if cms_home is None:
            cms_home = ShopifyRootPage(
                title='CMS Home',
                slug='cms-home',
                locale=self.locale_en,
            )
            site_root.add_child(instance=cms_home)
            cms_home.save_revision().publish()

        self.collection = CollectionPage(
            title='Vibrators',
            slug='vibrators-chooser',
            handle='vibrators-chooser',
            shopify_id='gid://shopify/Collection/chooser-10',
            locale=self.locale_en,
        )
        cms_home.add_child(instance=self.collection)
        self.collection.save_revision().publish()

        install_page_chooser_browse_locale_fix()

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
        pks = set(qs.values_list('pk', flat=True))

        self.assertIn(self.term_es.pk, pks)
        self.assertNotIn(self.term_en.pk, pks)
        self.assertIn(self.collection.pk, pks)

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

    def test_es_us_home_root_browse_shows_glossary_folder(self):
        """HomePage es-US chooser root still lists the shared en-US glossary folder."""
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
        # Simulate Wagtail browse filtering children by the chooser UI locale (es-US).
        filtered = children.filter(locale=self.locale_es)

        self.assertIn(self.glossary_root.pk, list(filtered.values_list('pk', flat=True)))

    def test_es_us_home_browse_inside_glossary_shows_es_terms_only(self):
        """Inside glossary/, es-US HomePage edit sees es-US terms, not en-US."""
        params = {
            'homepage_locale': 'es-US',
            'page_type': 'shopify_content.glossarytermpage',
        }
        request = RequestFactory().get(f'/admin/choose-page/{self.glossary_root.pk}/', params)
        request.session = {}
        request.user = None
        request.resolver_match = resolve(f'/admin/choose-page/{self.glossary_root.pk}/')

        children = self.glossary_root.get_children().defer_streamfields().specific()
        children = filter_page_chooser_by_locale(children, request)
        pks = set(children.type(GlossaryTermPage).values_list('pk', flat=True))

        self.assertIn(self.term_es.pk, pks)
        self.assertNotIn(self.term_en.pk, pks)

    def test_collection_chooser_without_homepage_locale_is_unrestricted(self):
        """Other page-type choosers stay unrestricted when homepage_locale is absent."""
        request = RequestFactory().get(
            '/admin/choose-page/',
            {'page_type': 'shopify_content.collectionpage'},
        )
        request.session = {}

        before = list(Page.objects.type(CollectionPage).values_list('pk', flat=True))
        after = list(
            filter_page_chooser_by_locale(Page.objects.all(), request)
            .type(CollectionPage)
            .values_list('pk', flat=True)
        )

        self.assertEqual(sorted(before), sorted(after))
        self.assertIn(self.collection.pk, after)

    def test_collection_chooser_ignores_homepage_locale(self):
        """homepage_locale must not alter CollectionPage-only chooser querysets."""
        request = RequestFactory().get(
            '/admin/choose-page/',
            {
                'homepage_locale': 'es-US',
                'page_type': 'shopify_content.collectionpage',
            },
        )
        request.session = {}

        base_qs = Page.objects.all()
        filtered = filter_page_chooser_by_locale(base_qs, request)

        self.assertEqual(
            sorted(base_qs.values_list('pk', flat=True)),
            sorted(filtered.values_list('pk', flat=True)),
        )
        self.assertIn(self.collection.pk, filtered.values_list('pk', flat=True))

    def test_browse_patch_installs_once(self):
        from shopify_content import page_chooser_locale

        first = page_chooser_locale._original_queryset_filter
        install_page_chooser_browse_locale_fix()
        self.assertIs(page_chooser_locale._original_queryset_filter, first)
        self.assertIsNot(QuerySet.filter, page_chooser_locale._original_queryset_filter)

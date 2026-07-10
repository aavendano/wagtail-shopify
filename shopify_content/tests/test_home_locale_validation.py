"""Tests for HomePage sections_json locale validation."""

from django.core.exceptions import ValidationError
from django.test import TestCase
from wagtail.models import Locale, Page

from shopify_content.home_locale_validation import (
    collect_sections_page_ids,
    is_page_valid_for_home_locale,
    validate_sections_json_locale,
)
from shopify_content.models import (
    ArticlePage,
    BlogPage,
    CollectionPage,
    GlossaryTermPage,
    HomePage,
    ShopifyRootPage,
)


class HomeLocaleValidationTests(TestCase):
    def setUp(self):
        self.locale_en = Locale.get_default()
        self.locale_es, _ = Locale.objects.get_or_create(language_code='es-US')

        site_root = Page.get_first_root_node()
        if site_root is None:
            site_root = Page.add_root(
                instance=Page(title='Site Home', slug='site-home', locale=self.locale_en)
            )

        self.cms_home_root = ShopifyRootPage.objects.filter(slug='cms-home').first()
        if self.cms_home_root is None:
            self.cms_home_root = ShopifyRootPage(
                title='CMS Home',
                slug='cms-home',
                locale=self.locale_en,
            )
            site_root.add_child(instance=self.cms_home_root)
            self.cms_home_root.save_revision().publish()

        self.blog_root = ShopifyRootPage.objects.filter(slug='blogs').first()
        if self.blog_root is None:
            self.blog_root = ShopifyRootPage(title='Blogs', slug='blogs', locale=self.locale_en)
            site_root.add_child(instance=self.blog_root)
            self.blog_root.save_revision().publish()

        self.blog = BlogPage(
            title='Guides',
            slug='guides',
            handle='guides',
            locale=self.locale_en,
            sync_enabled=True,
        )
        self.blog_root.add_child(instance=self.blog)
        self.blog.save_revision().publish()

        self.article_en = ArticlePage(
            title='Guide EN',
            slug='guide-en',
            handle='guide-en',
            shopify_id='gid://shopify/Article/1',
            locale=self.locale_en,
        )
        self.blog.add_child(instance=self.article_en)
        self.article_en.save_revision().publish()

        self.article_es = ArticlePage(
            title='Guide ES',
            slug='guide-es',
            handle='guide-es',
            shopify_id='gid://shopify/Article/2',
            locale=self.locale_es,
        )
        self.blog.add_child(instance=self.article_es)
        self.article_es.save_revision().publish()

        glossary_root = ShopifyRootPage.objects.filter(slug='glossary').first()
        if glossary_root is None:
            glossary_root = ShopifyRootPage(
                title='Glossary',
                slug='glossary',
                locale=self.locale_en,
            )
            site_root.add_child(instance=glossary_root)
            glossary_root.save_revision().publish()

        self.term_en = GlossaryTermPage(
            title='Vibrator',
            slug='vibrator',
            handle='vibrator',
            term='Vibrator',
            locale_code='en',
            shopify_id='gid://shopify/Metaobject/1',
            locale=self.locale_en,
        )
        glossary_root.add_child(instance=self.term_en)
        self.term_en.save_revision().publish()

        self.term_es = GlossaryTermPage(
            title='Vibrador',
            slug='vibrador',
            handle='vibrador',
            term='Vibrador',
            locale_code='es',
            shopify_id='gid://shopify/Metaobject/2',
            locale=self.locale_es,
        )
        glossary_root.add_child(instance=self.term_es)
        self.term_es.save_revision().publish()

        self.collection = CollectionPage(
            title='Vibrators',
            slug='vibrators-col',
            handle='vibrators',
            shopify_id='gid://shopify/Collection/10',
            locale=self.locale_en,
        )
        self.cms_home_root.add_child(instance=self.collection)
        self.collection.save_revision().publish()

        self.home_en = HomePage(
            title='Home EN',
            slug='home-en-us',
            hero_heading='Home EN',
            locale=self.locale_en,
        )
        self.cms_home_root.add_child(instance=self.home_en)
        self.home_en.save_revision().publish()

    def test_collect_sections_page_ids_includes_promo_gateway(self):
        sections_json = {
            'version': 1,
            'sections': [
                {
                    'type': 'promo_gateway',
                    'id': 'promo',
                    'value': {
                        'cards': [
                            {
                                'primary_collection_page_id': self.collection.pk,
                                'category_page_ids': [self.collection.pk],
                            }
                        ]
                    },
                }
            ],
        }
        ids = collect_sections_page_ids(sections_json)
        self.assertIn(self.collection.pk, ids)

    def test_article_same_locale_is_valid(self):
        self.assertTrue(
            is_page_valid_for_home_locale(self.home_en, self.article_en)
        )

    def test_article_wrong_locale_is_invalid(self):
        self.assertFalse(
            is_page_valid_for_home_locale(self.home_en, self.article_es)
        )

    def test_glossary_matching_short_locale_is_valid(self):
        self.assertTrue(
            is_page_valid_for_home_locale(self.home_en, self.term_en)
        )

    def test_glossary_wrong_short_locale_is_invalid(self):
        self.assertFalse(
            is_page_valid_for_home_locale(self.home_en, self.term_es)
        )

    def test_collection_has_no_locale_restriction(self):
        self.assertTrue(
            is_page_valid_for_home_locale(self.home_en, self.collection)
        )

    def test_validate_sections_json_locale_rejects_wrong_article(self):
        self.home_en.sections_json = {
            'version': 1,
            'sections': [
                {
                    'type': 'educational_hub',
                    'id': 'edu',
                    'value': {
                        'title': 'Learn',
                        'links': [{'page_id': self.article_es.pk}],
                    },
                }
            ],
        }
        errors = validate_sections_json_locale(self.home_en)
        self.assertTrue(errors)

    def test_home_page_clean_rejects_wrong_article(self):
        self.home_en.sections_json = {
            'version': 1,
            'sections': [
                {
                    'type': 'educational_hub',
                    'id': 'edu',
                    'value': {
                        'title': 'Learn',
                        'links': [{'page_id': self.article_es.pk}],
                    },
                }
            ],
        }
        with self.assertRaises(ValidationError):
            self.home_en.full_clean()

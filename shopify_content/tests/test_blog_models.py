"""Tests for available_locales validation on blog models."""

from django.core.exceptions import ValidationError
from django.test import TestCase
from wagtail.models import Locale, Page

from shopify_content.available_locales import (
    normalize_available_locales,
    validate_available_locales,
)
from shopify_content.models import ArticlePage, BlogPage, ShopifyRootPage


class AvailableLocalesHelperTests(TestCase):
    def test_normalize_deduplicates_and_filters(self):
        result = normalize_available_locales(['en-US', 'es-US', 'en-US', 'invalid'])
        self.assertEqual(result, ['en-US', 'es-US'])

    def test_validate_requires_locale_when_sync_enabled(self):
        with self.assertRaises(ValidationError):
            validate_available_locales([], page_locale_code='en-US', sync_enabled=True)

    def test_validate_requires_page_locale_in_list(self):
        with self.assertRaises(ValidationError):
            validate_available_locales(
                ['es-US'],
                page_locale_code='en-US',
                sync_enabled=True,
            )


class BlogPageAvailableLocalesTests(TestCase):
    def setUp(self):
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.root = ShopifyRootPage(title='Blogs', slug='blogs', locale=locale)
        home.add_child(instance=self.root)
        self.root.save_revision().publish()

    def test_defaults_to_page_locale_on_save(self):
        blog = BlogPage(
            title='Cluster',
            slug='cluster',
            handle='cluster',
            locale=Locale.get_default(),
            sync_enabled=True,
        )
        self.root.add_child(instance=blog)
        blog.save_revision().publish()
        blog.refresh_from_db()
        self.assertEqual(blog.available_locales, ['en-US'])

    def test_clean_rejects_missing_page_locale(self):
        blog = BlogPage(
            title='Cluster',
            slug='cluster-2',
            handle='cluster-2',
            locale=Locale.get_default(),
            available_locales=['es-US'],
            sync_enabled=True,
        )
        with self.assertRaises(ValidationError):
            blog.full_clean()


class ArticlePageAvailableLocalesTests(TestCase):
    def setUp(self):
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.root = ShopifyRootPage(title='Blogs', slug='blogs', locale=locale)
        home.add_child(instance=self.root)
        self.root.save_revision().publish()
        self.blog = BlogPage(
            title='Cluster',
            slug='cluster',
            handle='cluster',
            locale=locale,
            available_locales=['en-US'],
        )
        self.root.add_child(instance=self.blog)
        self.blog.save_revision().publish()

    def test_defaults_to_page_locale_on_save(self):
        article = ArticlePage(
            title='Post',
            slug='post',
            handle='post',
            locale=Locale.get_default(),
            sync_enabled=True,
        )
        self.blog.add_child(instance=article)
        article.save_revision().publish()
        article.refresh_from_db()
        self.assertEqual(article.available_locales, ['en-US'])

"""Tests for export_config registry."""

from django.test import TestCase
from wagtail.models import Locale, Page

from shopify_content.export_config.blog import blog_listings_consumer
from shopify_content.export_config.glossary import glossary_listings_consumer
from shopify_content.export_config.location import location_listings_consumer
from shopify_content.export_config.registry import (
    get_consumer_for_slug,
    on_content_page_changed,
    registered_root_slugs,
)
from shopify_content.models import ArticlePage, BlogPage, ShopifyRootPage


class ExportConfigRegistryTests(TestCase):
    def test_registered_root_slugs(self):
        slugs = registered_root_slugs()
        self.assertIn('glossary', slugs)
        self.assertIn('local-us', slugs)
        self.assertIn('blogs', slugs)

    def test_get_consumer_for_slug(self):
        self.assertIs(get_consumer_for_slug('glossary'), glossary_listings_consumer)
        self.assertIs(get_consumer_for_slug('local-us'), location_listings_consumer)
        self.assertIs(get_consumer_for_slug('blogs'), blog_listings_consumer)
        self.assertIsNone(get_consumer_for_slug('unknown-root'))

    def test_on_content_page_changed_walks_up_to_blogs_root(self):
        from unittest.mock import patch

        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        root = ShopifyRootPage(title='Blogs', slug='blogs', locale=locale)
        home.add_child(instance=root)
        root.save_revision().publish()
        blog = BlogPage(title='Cluster', slug='cluster', handle='cluster', locale=locale)
        root.add_child(instance=blog)
        blog.save_revision().publish()
        article = ArticlePage(title='Post', slug='post', handle='post', locale=locale)
        blog.add_child(instance=article)
        article.save_revision().publish()

        with patch.object(blog_listings_consumer, 'queue_sync') as mock_queue:
            on_content_page_changed(article)
            mock_queue.assert_called_once()

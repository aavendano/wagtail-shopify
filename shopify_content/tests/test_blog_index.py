"""Tests for blog index listings builder and consumer."""

import json
from datetime import datetime, timezone
from unittest.mock import patch

from django.test import TestCase
from wagtail.models import Locale, Page

from core.models import ShopConfig
from shopify_content.blogs.index import article_path, build_blog_index_listings
from shopify_content.export_config.blog import blog_listings_consumer
from shopify_content.models import ArticlePage, BlogPage, ShopifyRootPage
from shopify_content.sync.blog_index import sync_blog_index_listings


class BuildBlogIndexListingsTests(TestCase):
    def setUp(self):
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.root = ShopifyRootPage(title='Blogs', slug='blogs', locale=locale)
        home.add_child(instance=self.root)
        self.root.save_revision().publish()

        self.blog = BlogPage(
            title='Sex Toys Artisans',
            slug='sex-toys-artisans',
            handle='sex-toys-artisans',
            locale=locale,
            available_locales=['en-US'],
        )
        self.root.add_child(instance=self.blog)
        self.blog.save_revision().publish()

    def _add_article(self, *, title, handle, shopify_id='gid://shopify/Article/1', live=True):
        article = ArticlePage(
            title=title,
            slug=handle,
            handle=handle,
            locale=Locale.get_default(),
            shopify_id=shopify_id,
            available_locales=['en-US'],
        )
        self.blog.add_child(instance=article)
        if live:
            article.save_revision().publish()
        else:
            article.save_revision()
        return article

    def test_article_path(self):
        self.assertEqual(
            article_path('cluster', 'my-post'),
            '/blogs/cluster/my-post',
        )

    def test_groups_articles_by_blog_cluster(self):
        fixed = datetime(2026, 7, 5, 12, 0, tzinfo=timezone.utc)
        self._add_article(title='Alpha Post', handle='alpha-post', shopify_id='gid://1')
        self._add_article(title='Beta Post', handle='beta-post', shopify_id='gid://2')

        payload = build_blog_index_listings(generated_at=fixed)

        self.assertEqual(payload['version'], 1)
        self.assertEqual(payload['generated_at'], fixed.isoformat())
        en_listing = payload['locales']['en-US']
        self.assertEqual(en_listing['count'], 2)
        self.assertEqual(len(en_listing['sections']), 1)
        section = en_listing['sections'][0]
        self.assertEqual(section['key'], 'sex-toys-artisans')
        paths = [item['path'] for item in section['items']]
        self.assertIn('/blogs/sex-toys-artisans/alpha-post', paths)
        self.assertIn('/blogs/sex-toys-artisans/beta-post', paths)

    def test_excludes_unpublished_and_missing_shopify_id(self):
        self._add_article(title='Live', handle='live', shopify_id='gid://1')
        draft = self._add_article(title='Draft', handle='draft', shopify_id='gid://2', live=False)
        draft.unpublish()
        self._add_article(title='No Shopify', handle='no-shopify', shopify_id='')

        payload = build_blog_index_listings()
        en_listing = payload['locales']['en-US']
        self.assertEqual(en_listing['count'], 1)
        self.assertEqual(en_listing['sections'][0]['items'][0]['title'], 'Live')


class BlogListingsConsumerTests(TestCase):
    def setUp(self):
        ShopConfig.objects.create(shop='test-shop.myshopify.com', access_token='tok')
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.root = ShopifyRootPage(
            title='Blogs',
            slug='blogs',
            locale=locale,
            export_config={
                'blog_index': {
                    'enabled': True,
                    'page_gid': 'gid://shopify/Page/999',
                },
            },
        )
        home.add_child(instance=self.root)
        self.root.save_revision().publish()

    def test_sync_dry_run(self):
        stats = sync_blog_index_listings(dry_run=True)
        self.assertTrue(stats['root_found'])
        self.assertTrue(stats['enabled'])
        self.assertEqual(stats['pushed'], 1)

    @patch('shopify_content.export_config.single_page._push_metafields', return_value=True)
    def test_sync_pushes_index_listings(self, mock_push):
        stats = blog_listings_consumer.sync()
        self.assertEqual(stats['pushed'], 1)
        mock_push.assert_called_once()
        metafields = mock_push.call_args[0][1]
        self.assertEqual(metafields[0]['key'], 'index_listings')
        payload = json.loads(metafields[0]['value'])
        self.assertIn('locales', payload)

    def test_locale_codes_for_article_page(self):
        blog = BlogPage(
            title='Cluster',
            slug='cluster',
            handle='cluster',
            locale=Locale.get_default(),
        )
        self.root.add_child(instance=blog)
        blog.save_revision().publish()
        article = ArticlePage(
            title='Post',
            slug='post',
            handle='post',
            locale=Locale.get_default(),
        )
        blog.add_child(instance=article)
        article.save_revision().publish()
        self.assertEqual(
            blog_listings_consumer.locale_codes_for_page(article),
            ['en-US'],
        )

"""Tests for blog/article outbound sync helpers."""

from unittest.mock import patch

from django.test import TestCase
from wagtail.models import Locale, Page

from core.models import ShopConfig
from shopify_content.models import ArticlePage, BlogPage, ShopifyRootPage
from shopify_content.sync.outbound import (
    _push_available_locales_metafield,
    sync_article_page,
    sync_blog_page,
)


class PushAvailableLocalesMetafieldTests(TestCase):
    def setUp(self):
        ShopConfig.objects.create(shop='test-shop.myshopify.com', access_token='tok')

    @patch('shopify_content.sync.outbound._push_metafields', return_value=True)
    def test_pushes_normalized_locales(self, mock_push):
        ok = _push_available_locales_metafield(
            'test-shop.myshopify.com',
            'gid://shopify/Article/1',
            ['en-US', 'es-US', 'en-US'],
        )
        self.assertTrue(ok)
        mock_push.assert_called_once()
        metafield = mock_push.call_args[0][1][0]
        self.assertEqual(metafield['key'], 'available_locales')
        self.assertEqual(metafield['type'], 'list.single_line_text_field')
        self.assertEqual(metafield['value'], '["en-US", "es-US"]')


class SyncBlogPageAvailableLocalesTests(TestCase):
    def setUp(self):
        ShopConfig.objects.create(shop='test-shop.myshopify.com', access_token='tok')
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        root = ShopifyRootPage(title='Blogs', slug='blogs', locale=locale)
        home.add_child(instance=root)
        root.save_revision().publish()
        self.blog = BlogPage(
            title='Cluster',
            slug='cluster',
            handle='cluster',
            shopify_id='gid://shopify/Blog/1',
            locale=locale,
            available_locales=['en-US', 'es-US'],
        )
        root.add_child(instance=self.blog)
        self.blog.save_revision().publish()

    @patch('shopify_content.sync.outbound._register_shopify_translations')
    @patch('shopify_content.sync.outbound._push_available_locales_metafield', return_value=True)
    @patch('shopify_content.sync.outbound._push_seo_metafields', return_value=True)
    @patch('shopify_content.sync.outbound._push_faq_metafield', return_value=True)
    @patch('shopify_content.sync.outbound._push_metafields', return_value=True)
    @patch('shopify_content.sync.outbound.execute_admin_graphql')
    def test_sync_blog_pushes_available_locales_and_registers_translations(
        self,
        mock_graphql,
        mock_push_metafields,
        mock_push_faq,
        mock_push_seo,
        mock_push_available,
        mock_register,
    ):
        mock_graphql.return_value.ok = True
        mock_graphql.return_value.data = {
            'blogUpdate': {'blog': {'id': 'gid://shopify/Blog/1'}, 'userErrors': []},
        }
        sync_blog_page(self.blog)
        mock_push_available.assert_called_once_with(
            'test-shop.myshopify.com',
            'gid://shopify/Blog/1',
            ['en-US', 'es-US'],
        )
        mock_register.assert_called_once()
        register_args = mock_register.call_args.args
        self.assertEqual(register_args[2], 'gid://shopify/Blog/1')
        translatable_fields = register_args[3]
        self.assertIn('title', translatable_fields)
        self.assertIn('metafields.custom.description', translatable_fields)
        self.assertIn('metafields.global.title_tag', translatable_fields)
        self.assertIn('metafields.global.description_tag', translatable_fields)


class SyncArticlePageAvailableLocalesTests(TestCase):
    def setUp(self):
        ShopConfig.objects.create(shop='test-shop.myshopify.com', access_token='tok')
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        root = ShopifyRootPage(title='Blogs', slug='blogs', locale=locale)
        home.add_child(instance=root)
        root.save_revision().publish()
        self.blog = BlogPage(
            title='Cluster',
            slug='cluster',
            handle='cluster',
            shopify_id='gid://shopify/Blog/1',
            locale=locale,
        )
        root.add_child(instance=self.blog)
        self.blog.save_revision().publish()
        self.article = ArticlePage(
            title='Post',
            slug='post',
            handle='post',
            shopify_id='gid://shopify/Article/1',
            locale=locale,
            available_locales=['en-US', 'fr-CA'],
        )
        self.blog.add_child(instance=self.article)
        self.article.save_revision().publish()

    @patch('shopify_content.sync.outbound._queue_index_sync_after_content_sync')
    @patch('shopify_content.sync.outbound._register_shopify_translations')
    @patch('shopify_content.sync.outbound._push_available_locales_metafield', return_value=True)
    @patch('shopify_content.sync.outbound._push_native_reference_metafields', return_value=True)
    @patch('shopify_content.sync.outbound._push_internal_links_metafield', return_value=True)
    @patch('shopify_content.sync.outbound._push_faq_metafield', return_value=True)
    @patch('shopify_content.sync.outbound._collect_inline_metafields', return_value=[])
    @patch('shopify_content.sync.outbound._collect_streamfield_metafields', return_value=[])
    @patch('shopify_content.sync.outbound._push_seo_metafields', return_value=True)
    @patch('shopify_content.sync.outbound._push_metafields', return_value=True)
    @patch('shopify_content.sync.outbound.execute_admin_graphql')
    def test_sync_article_pushes_available_locales_and_queues_index(
        self,
        mock_graphql,
        mock_push_metafields,
        mock_push_seo,
        mock_stream_mf,
        mock_inline_mf,
        mock_push_faq,
        mock_push_internal,
        mock_push_native,
        mock_push_available,
        mock_register,
        mock_queue_index,
    ):
        mock_graphql.return_value.ok = True
        mock_graphql.return_value.data = {
            'articleUpdate': {'article': {'id': 'gid://shopify/Article/1'}, 'userErrors': []},
        }
        sync_article_page(self.article)
        mock_push_available.assert_called_once_with(
            'test-shop.myshopify.com',
            'gid://shopify/Article/1',
            ['en-US', 'fr-CA'],
        )
        mock_queue_index.assert_called_once_with(self.article)

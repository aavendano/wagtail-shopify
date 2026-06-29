from unittest.mock import MagicMock, patch

from django.test import TestCase, override_settings
from wagtail.models import Locale, Page

from shopify_content.models import (
    CollectionPage,
    GlossaryTermPage,
    ProductPage,
    ShopifyRootPage,
)
from shopify_content.models.blog import ArticlePage, BlogPage
from shopify_content.semantic_links.serialization import (
    page_to_related_link,
    related_link_url,
    serialize_semantic_links,
)
from shopify_content.semantic_links.service import classify_and_cap, refresh_semantic_links
from shopify_content.tasks import sync_page_to_shopify_task
from shopify_content.models.sync_run import ShopifySyncRun


class PageToRelatedLinkTests(TestCase):
    def setUp(self):
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.root = ShopifyRootPage(title='Root', slug='root', locale=locale)
        home.add_child(instance=self.root)
        self.root.save_revision().publish()

        self.product = ProductPage(
            title='Test Product',
            slug='test-product',
            handle='test-product',
            locale=locale,
        )
        self.root.add_child(instance=self.product)
        self.product.save_revision().publish()

        self.collection = CollectionPage(
            title='Summer',
            slug='summer',
            handle='summer',
            locale=locale,
        )
        self.root.add_child(instance=self.collection)
        self.collection.save_revision().publish()

        self.blog = BlogPage(title='News', slug='news', handle='news', locale=locale)
        self.root.add_child(instance=self.blog)
        self.blog.save_revision().publish()

        self.article = ArticlePage(
            title='Article One',
            slug='article-one',
            handle='article-one',
            locale=locale,
        )
        self.blog.add_child(instance=self.article)
        self.article.save_revision().publish()

        glossary_root = ShopifyRootPage(title='Glossary', slug='glossary', locale=locale)
        self.root.add_child(instance=glossary_root)
        glossary_root.save_revision().publish()

        self.term = GlossaryTermPage(
            title='Vibrator',
            term='Vibrator',
            slug='vibrator',
            handle='vibrator',
            locale=locale,
        )
        glossary_root.add_child(instance=self.term)
        self.term.save_revision().publish()

    def test_product_link(self):
        link = page_to_related_link(self.product)
        self.assertEqual(link['type'], 'product')
        self.assertEqual(link['handle'], 'test-product')
        self.assertEqual(related_link_url(link), '/products/test-product')

    def test_collection_link(self):
        link = page_to_related_link(self.collection)
        self.assertEqual(link['type'], 'collection')
        self.assertEqual(link['handle'], 'summer')

    def test_article_link_includes_blog_handle(self):
        link = page_to_related_link(self.article)
        self.assertEqual(link['type'], 'article')
        self.assertEqual(link['blog_handle'], 'news')

    def test_glossary_link(self):
        link = page_to_related_link(self.term)
        self.assertEqual(link['type'], 'metaobject')
        self.assertEqual(link['url_handle'], 'glossary')


class RefreshSemanticLinksTests(TestCase):
    def setUp(self):
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.root = ShopifyRootPage(title='Root', slug='root', locale=locale)
        home.add_child(instance=self.root)
        self.root.save_revision().publish()

        self.source = ProductPage(
            title='Source Product',
            slug='source-product',
            handle='source-product',
            locale=locale,
        )
        self.root.add_child(instance=self.source)
        self.source.save_revision().publish()

        self.target = CollectionPage(
            title='Target Collection',
            slug='target-collection',
            handle='target-collection',
            locale=locale,
        )
        self.root.add_child(instance=self.target)
        self.target.save_revision().publish()

        self.source.semantic_links.create(
            related_page=self.target,
            is_auto=False,
            sort_order=0,
        )

    @override_settings(SEMANTIC_LINKS_ENABLED=True, SEMANTIC_LINKS_LIMIT_PER_TYPE=2)
    @patch('shopify_content.semantic_links.service.search_similar_pages')
    def test_refresh_preserves_manual_links(self, mock_search):
        blog_page = BlogPage(title='B', slug='b', handle='b', locale=self.source.locale)
        self.root.add_child(instance=blog_page)
        blog_page.save_revision().publish()
        article = ArticlePage(title='A', slug='a', handle='a', locale=self.source.locale)
        blog_page.add_child(instance=article)
        article.save_revision().publish()

        mock_search.return_value = [article]

        refresh_semantic_links(self.source)

        manual = self.source.semantic_links.filter(is_auto=False).count()
        auto = self.source.semantic_links.filter(is_auto=True).count()
        self.assertEqual(manual, 1)
        self.assertEqual(auto, 1)
        self.assertTrue(
            self.source.semantic_links.filter(related_page=self.target, is_auto=False).exists()
        )

    @override_settings(SEMANTIC_LINKS_ENABLED=True)
    @patch('shopify_content.semantic_links.service.search_similar_pages')
    def test_refresh_replaces_auto_only(self, mock_search):
        other = ProductPage(
            title='Other',
            slug='other',
            handle='other',
            locale=self.source.locale,
        )
        self.root.add_child(instance=other)
        other.save_revision().publish()

        self.source.semantic_links.create(
            related_page=other,
            is_auto=True,
            sort_order=1,
        )

        blog_page = BlogPage(title='B2', slug='b2', handle='b2', locale=self.source.locale)
        self.root.add_child(instance=blog_page)
        blog_page.save_revision().publish()
        article = ArticlePage(title='A2', slug='a2', handle='a2', locale=self.source.locale)
        blog_page.add_child(instance=article)
        article.save_revision().publish()

        mock_search.return_value = [article]

        refresh_semantic_links(self.source)

        self.assertFalse(self.source.semantic_links.filter(related_page=other, is_auto=True).exists())
        self.assertTrue(self.source.semantic_links.filter(related_page=article, is_auto=True).exists())


class ClassifyAndCapTests(TestCase):
    def test_respects_limit_per_type(self):
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        root = ShopifyRootPage(title='Root', slug='root2', locale=locale)
        home.add_child(instance=root)
        root.save_revision().publish()

        source = ProductPage(title='S', slug='s', handle='s', locale=locale)
        root.add_child(instance=source)
        source.save_revision().publish()

        pages = []
        for i in range(3):
            page = CollectionPage(title=f'C{i}', slug=f'c{i}', handle=f'c{i}', locale=locale)
            root.add_child(instance=page)
            page.save_revision().publish()
            pages.append(page)

        grouped = classify_and_cap(pages, source_page=source, limit_per_type=2)
        self.assertEqual(len(grouped['collection']), 2)


@override_settings(
    CELERY_TASK_ALWAYS_EAGER=True,
    SEMANTIC_LINKS_ENABLED=True,
    SEMANTIC_LINKS_AUTO_ON_PUBLISH=True,
    SEMANTIC_LINKS_INDEX_ON_PUBLISH=False,
)
class CelerySemanticLinksPipelineTests(TestCase):
    def setUp(self):
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.parent = ShopifyRootPage(title='Root', slug='root-celery', locale=locale)
        home.add_child(instance=self.parent)
        self.parent.save_revision().publish()

    @patch('shopify_content.sync.outbound.sync_product_page', return_value=True)
    @patch('shopify_content.semantic_links.service.refresh_semantic_links')
    def test_sync_task_refreshes_links_before_sync(self, mock_refresh, mock_sync):
        page = ProductPage(
            title='Test Product',
            slug='test-product-celery',
            shopify_id='gid://shopify/Product/1',
            locale=Locale.get_default(),
            sync_enabled=True,
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()

        sync_run = ShopifySyncRun.objects.create(
            kind=ShopifySyncRun.KIND_OUTBOUND,
            page=page,
        )
        sync_page_to_shopify_task(sync_run.pk, page.pk)

        mock_refresh.assert_called_once()
        mock_sync.assert_called_once()


class RevisionPersistenceTests(TestCase):
    @override_settings(SEMANTIC_LINKS_ENABLED=True, SEMANTIC_LINKS_LIMIT_PER_TYPE=2)
    @patch('shopify_content.semantic_links.service.search_similar_pages')
    def test_refresh_persists_links_for_stale_draft_revision(self, mock_search):
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        root = ShopifyRootPage(title='Root', slug='root-rev', locale=locale)
        home.add_child(instance=root)
        root.save_revision().publish()

        source = GlossaryTermPage(
            title='Orgasm',
            term='Orgasm',
            slug='orgasm',
            handle='orgasm',
            locale=locale,
        )
        root.add_child(instance=source)
        source.save_revision().publish()

        target = ProductPage(title='Toy', slug='toy', handle='toy', locale=locale)
        root.add_child(instance=target)
        target.save_revision().publish()

        # Simulate stale draft revision without semantic links.
        source.save_revision(log_action=False)

        mock_search.return_value = [target]
        refresh_semantic_links(source)

        page = Page.objects.get(pk=source.pk)
        editor_page = page.get_latest_revision_as_object()
        self.assertEqual(editor_page.semantic_links.count(), 1)


class SerializeSemanticLinksTests(TestCase):
    def test_serializes_fk_rows(self):
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        root = ShopifyRootPage(title='Root', slug='root-ser', locale=locale)
        home.add_child(instance=root)
        root.save_revision().publish()

        product = ProductPage(title='P', slug='p', handle='p', locale=locale)
        root.add_child(instance=product)
        product.save_revision().publish()

        collection = CollectionPage(title='C', slug='c', handle='c', locale=locale)
        root.add_child(instance=collection)
        collection.save_revision().publish()

        product.semantic_links.create(related_page=collection, is_auto=True, sort_order=0)

        links = serialize_semantic_links(product)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0]['type'], 'collection')

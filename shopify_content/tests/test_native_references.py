import json
from unittest.mock import patch

from django.test import TestCase, override_settings
from wagtail.models import Locale, Page

from core.models import ShopConfig
from shopify_content.models import (
    CollectionPage,
    GlossaryTermPage,
    ProductPage,
    ShopifyRootPage,
)
from shopify_content.models.blog import ArticlePage, BlogPage
from shopify_content.semantic_links.references import (
    format_list_reference_value,
    page_to_shopify_gid,
    relation_to_shopify_gids,
    resolve_metafield_reference_value,
    serialize_native_references,
)
from shopify_content.sync.outbound import (
    _collect_inline_metafields,
    _push_native_reference_metafields,
    sync_product_page,
)


class NativeReferenceResolutionTests(TestCase):
    def setUp(self):
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.root = ShopifyRootPage(title='Root', slug='root-native', locale=locale)
        home.add_child(instance=self.root)
        self.root.save_revision().publish()

        self.product = ProductPage(
            title='Source Product',
            slug='source-product',
            handle='source-product',
            shopify_id='gid://shopify/Product/1',
            locale=locale,
        )
        self.root.add_child(instance=self.product)
        self.product.save_revision().publish()

        self.target = ProductPage(
            title='Target Product',
            slug='target-product',
            handle='target-product',
            shopify_id='gid://shopify/Product/2',
            locale=locale,
        )
        self.root.add_child(instance=self.target)
        self.target.save_revision().publish()

        self.no_gid = ProductPage(
            title='No GID Product',
            slug='no-gid-product',
            handle='no-gid-product',
            locale=locale,
        )
        self.root.add_child(instance=self.no_gid)
        self.no_gid.save_revision().publish()

        self.blog = BlogPage(
            title='Native Blog',
            slug='native-blog',
            handle='native-blog',
            shopify_id='gid://shopify/Blog/1',
            locale=locale,
        )
        self.root.add_child(instance=self.blog)
        self.blog.save_revision().publish()

        self.article = ArticlePage(
            title='Native Article',
            slug='native-article',
            handle='native-article',
            shopify_id='gid://shopify/Article/10',
            locale=locale,
        )
        self.blog.add_child(instance=self.article)
        self.article.save_revision().publish()

    def test_page_to_shopify_gid_returns_gid(self):
        self.assertEqual(
            page_to_shopify_gid(self.product),
            'gid://shopify/Product/1',
        )

    def test_page_to_shopify_gid_returns_none_when_missing(self):
        self.assertIsNone(page_to_shopify_gid(self.no_gid))

    def test_relation_to_shopify_gids_resolves_targets(self):
        self.product.related_products.create(
            related_page=self.target,
            is_auto=False,
            sort_order=0,
        )
        gids = relation_to_shopify_gids(self.product, 'related_products')
        self.assertEqual(gids, ['gid://shopify/Product/2'])

    def test_relation_skips_targets_without_shopify_id(self):
        self.product.related_products.create(
            related_page=self.no_gid,
            is_auto=False,
            sort_order=0,
        )
        with self.assertLogs('shopify_content.semantic_links.references', level='WARNING'):
            gids = relation_to_shopify_gids(self.product, 'related_products')
        self.assertEqual(gids, [])

    def test_serialize_native_references_groups_by_relation(self):
        collection = CollectionPage(
            title='Summer',
            slug='summer',
            handle='summer',
            shopify_id='gid://shopify/Collection/10',
            locale=Locale.get_default(),
        )
        self.root.add_child(instance=collection)
        collection.save_revision().publish()

        self.product.related_collections.create(
            related_page=collection,
            is_auto=True,
            sort_order=0,
        )
        self.product.related_articles.create(
            related_page=self.article,
            is_auto=True,
            sort_order=1,
        )
        refs = serialize_native_references(self.product)
        self.assertEqual(
            refs,
            {
                'related_collections': ['gid://shopify/Collection/10'],
                'related_articles': ['gid://shopify/Article/10'],
            },
        )

    def test_format_list_reference_value_json_encodes_gids(self):
        gids = ['gid://shopify/Product/1', 'gid://shopify/Product/2']
        self.assertEqual(
            format_list_reference_value(gids),
            json.dumps(gids),
        )

    def test_resolve_metafield_reference_value_from_handle(self):
        resolved = resolve_metafield_reference_value(
            'product_reference',
            'target-product',
        )
        self.assertEqual(resolved, 'gid://shopify/Product/2')

    def test_resolve_list_reference_value_from_handles(self):
        self.product.related_products.create(
            related_page=self.target,
            is_auto=False,
            sort_order=0,
        )
        resolved = resolve_metafield_reference_value(
            'list.product_reference',
            '["target-product"]',
        )
        self.assertEqual(
            resolved,
            format_list_reference_value(['gid://shopify/Product/2']),
        )

    def test_resolve_article_reference_value_from_handle(self):
        resolved = resolve_metafield_reference_value(
            'list.article_reference',
            '["native-article"]',
        )
        self.assertEqual(
            resolved,
            format_list_reference_value(['gid://shopify/Article/10']),
        )


class PushNativeReferenceMetafieldsTests(TestCase):
    def setUp(self):
        ShopConfig.objects.create(shop='test-shop.myshopify.com', access_token='tok')
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.root = ShopifyRootPage(title='Root', slug='root-push', locale=locale)
        home.add_child(instance=self.root)
        self.root.save_revision().publish()

        self.product = ProductPage(
            title='Push Product',
            slug='push-product',
            handle='push-product',
            shopify_id='gid://shopify/Product/100',
            locale=locale,
            sync_enabled=True,
        )
        self.root.add_child(instance=self.product)
        self.product.save_revision().publish()

        self.target = ProductPage(
            title='Linked Product',
            slug='linked-product',
            handle='linked-product',
            shopify_id='gid://shopify/Product/200',
            locale=locale,
        )
        self.root.add_child(instance=self.target)
        self.target.save_revision().publish()

        self.product.related_products.create(
            related_page=self.target,
            is_auto=False,
            sort_order=0,
        )

        self.blog = BlogPage(
            title='Push Blog',
            slug='push-blog',
            handle='push-blog',
            shopify_id='gid://shopify/Blog/200',
            locale=locale,
        )
        self.root.add_child(instance=self.blog)
        self.blog.save_revision().publish()

        self.article = ArticlePage(
            title='Linked Article',
            slug='linked-article',
            handle='linked-article',
            shopify_id='gid://shopify/Article/300',
            locale=locale,
        )
        self.blog.add_child(instance=self.article)
        self.article.save_revision().publish()

        self.product.related_articles.create(
            related_page=self.article,
            is_auto=False,
            sort_order=1,
        )

    @override_settings(SEMANTIC_LINKS_NATIVE_REFS_ENABLED=True)
    @patch('shopify_content.sync.outbound._push_metafields', return_value=True)
    def test_push_native_reference_metafields_emits_reference_inputs(
        self, mock_push,
    ):
        ok = _push_native_reference_metafields(
            'test-shop.myshopify.com',
            'gid://shopify/Product/100',
            self.product,
        )
        self.assertTrue(ok)
        mock_push.assert_called_once()
        inputs = mock_push.call_args.args[1]
        by_key = {item['key']: item for item in inputs}
        self.assertEqual(set(by_key), {'related_products', 'related_articles'})
        self.assertEqual(by_key['related_products']['namespace'], 'custom')
        self.assertEqual(by_key['related_products']['type'], 'list.product_reference')
        self.assertEqual(
            json.loads(by_key['related_products']['value']),
            ['gid://shopify/Product/200'],
        )
        self.assertEqual(by_key['related_articles']['namespace'], 'custom')
        self.assertEqual(by_key['related_articles']['type'], 'list.article_reference')
        self.assertEqual(
            json.loads(by_key['related_articles']['value']),
            ['gid://shopify/Article/300'],
        )

    @override_settings(SEMANTIC_LINKS_NATIVE_REFS_ENABLED=False)
    @patch('shopify_content.sync.outbound._push_metafields')
    def test_push_skipped_when_disabled(self, mock_push):
        ok = _push_native_reference_metafields(
            'test-shop.myshopify.com',
            'gid://shopify/Product/100',
            self.product,
        )
        self.assertTrue(ok)
        mock_push.assert_not_called()

    @override_settings(SEMANTIC_LINKS_NATIVE_REFS_ENABLED=True)
    @patch('shopify_content.sync.outbound.execute_admin_graphql')
    @patch('shopify_content.sync.outbound._push_metafields', return_value=True)
    def test_sync_product_page_pushes_native_refs_after_internal_links(
        self, mock_push_metafields, mock_graphql,
    ):
        from shopify_requests.graphql_service import AdminGraphqlResult
        from types import SimpleNamespace

        mock_graphql.return_value = AdminGraphqlResult(
            ok=True,
            shop='test-shop.myshopify.com',
            data={'productUpdate': {'userErrors': []}},
            extensions=None,
            error_code=None,
            log_detail='ok',
            reauthorization_required=False,
            retryable=False,
            raw=SimpleNamespace(),
        )

        sync_product_page(self.product)

        native_calls = [
            call
            for call in mock_push_metafields.call_args_list
            if call.args[1]
            and any(item.get('type') == 'list.product_reference' for item in call.args[1])
        ]
        self.assertEqual(len(native_calls), 1)
        self.assertTrue(
            any(
                item.get('type') == 'list.article_reference'
                for item in native_calls[0].args[1]
            )
        )


class CollectInlineMetafieldsReferenceTests(TestCase):
    def setUp(self):
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.root = ShopifyRootPage(title='Root', slug='root-inline', locale=locale)
        home.add_child(instance=self.root)
        self.root.save_revision().publish()

        self.product = ProductPage(
            title='Inline Product',
            slug='inline-product',
            handle='inline-product',
            shopify_id='gid://shopify/Product/50',
            locale=locale,
        )
        self.root.add_child(instance=self.product)
        self.product.save_revision().publish()

        self.ref_product = ProductPage(
            title='Ref Product',
            slug='ref-product',
            handle='ref-product',
            shopify_id='gid://shopify/Product/51',
            locale=locale,
        )
        self.root.add_child(instance=self.ref_product)
        self.ref_product.save_revision().publish()

    def test_collect_inline_metafields_resolves_product_reference(self):
        self.product.metafields.create(
            namespace='custom',
            key='featured',
            type='product_reference',
            value='ref-product',
        )
        inputs = _collect_inline_metafields(self.product, 'gid://shopify/Product/50')
        self.assertEqual(inputs[0]['value'], 'gid://shopify/Product/51')

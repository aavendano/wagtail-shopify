from unittest.mock import patch

from django.test import TestCase
from wagtail.models import Locale, Page

from core.models import ShopConfig
from shopify_content.models import (
    ArticlePage,
    BlogPage,
    CollectionPage,
    ProductPage,
    ProductPageImage,
    ProductPageMetafield,
    ShopifyRootPage,
)
from shopify_content.sync.inbound import (
    import_blogs_and_articles,
    import_collections,
    import_products,
)
from shopify_content.sync.utils import absolute_shopify_media_url


def _make_product_node(gid, handle, title, images=None, metafields=None):
    if images is None:
        images = {'edges': []}
    return {
        'id': gid,
        'title': title,
        'handle': handle,
        'vendor': 'Acme',
        'productType': 'Shirt',
        'status': 'ACTIVE',
        'tags': [],
        'seo': {'title': '', 'description': ''},
        'descriptionHtml': '<p>Description</p>',
        'images': images,
        'metafields': metafields or {'edges': []},
    }


def _make_image_edges(count, url_prefix='https://cdn.shopify.com/img'):
    return {
        'edges': [
            {
                'node': {
                    'id': f'gid://shopify/MediaImage/{i}',
                    'url': f'{url_prefix}/{i}.jpg',
                    'altText': f'Alt {i}',
                }
            }
            for i in range(1, count + 1)
        ]
    }


class AbsoluteShopifyMediaUrlTests(TestCase):
    def test_empty_returns_empty(self):
        self.assertEqual(absolute_shopify_media_url(''), '')
        self.assertEqual(absolute_shopify_media_url('   '), '')

    def test_protocol_relative_normalized(self):
        url = '//cdn.shopify.com/s/files/1/1/photo.jpg'
        self.assertEqual(
            absolute_shopify_media_url(url),
            'https://cdn.shopify.com/s/files/1/1/photo.jpg',
        )

    def test_https_unchanged(self):
        url = 'https://cdn.shopify.com/photo.jpg'
        self.assertEqual(absolute_shopify_media_url(url), url)

    def test_relative_rejected(self):
        self.assertEqual(absolute_shopify_media_url('/relative/path.jpg'), '')


class ImportProductImagesTests(TestCase):
    def setUp(self):
        ShopConfig.objects.create(
            shop='test-shop.myshopify.com',
            access_token='tok',
        )
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.parent = ShopifyRootPage(title='Root', slug='root', locale=locale)
        home.add_child(instance=self.parent)
        self.parent.save_revision().publish()

    @patch('shopify_content.sync.inbound._paginate')
    def test_import_persists_max_ten_absolute_urls(self, mock_paginate):
        gid = 'gid://shopify/Product/100'
        mock_paginate.return_value = iter([
            _make_product_node(
                gid,
                'ten-images',
                'Ten Images',
                images=_make_image_edges(12),
            ),
        ])

        stats = import_products('test-shop.myshopify.com', self.parent)

        self.assertEqual(stats['created'], 1)
        page = ProductPage.objects.get(shopify_id=gid)
        images = list(page.shopify_images.order_by('sort_order'))
        self.assertEqual(len(images), 10)
        self.assertEqual(images[0].url, 'https://cdn.shopify.com/img/1.jpg')
        self.assertEqual(images[0].alt_text, 'Alt 1')
        self.assertEqual(images[0].shopify_id, 'gid://shopify/MediaImage/1')
        self.assertEqual(images[9].sort_order, 9)

    @patch('shopify_content.sync.inbound._paginate')
    def test_import_normalizes_protocol_relative_urls(self, mock_paginate):
        gid = 'gid://shopify/Product/101'
        mock_paginate.return_value = iter([
            _make_product_node(
                gid,
                'protocol-relative',
                'Protocol Relative',
                images={
                    'edges': [
                        {
                            'node': {
                                'id': 'gid://shopify/MediaImage/1',
                                'url': '//cdn.shopify.com/photo.jpg',
                                'altText': 'Photo',
                            }
                        }
                    ]
                },
            ),
        ])

        import_products('test-shop.myshopify.com', self.parent)

        page = ProductPage.objects.get(shopify_id=gid)
        self.assertEqual(
            page.shopify_images.get().url,
            'https://cdn.shopify.com/photo.jpg',
        )

    @patch('shopify_content.sync.inbound._paginate')
    def test_import_does_not_create_metafields(self, mock_paginate):
        gid = 'gid://shopify/Product/102'
        mock_paginate.return_value = iter([
            _make_product_node(
                gid,
                'with-metafields',
                'With Metafields',
                metafields={
                    'edges': [
                        {
                            'node': {
                                'namespace': 'custom',
                                'key': 'material',
                                'type': 'single_line_text_field',
                                'value': 'Cotton',
                            }
                        }
                    ]
                },
            ),
        ])

        import_products('test-shop.myshopify.com', self.parent)

        page = ProductPage.objects.get(shopify_id=gid)
        self.assertEqual(page.metafields.count(), 0)
        self.assertFalse(ProductPageMetafield.objects.filter(page=page).exists())

    @patch('shopify_content.sync.inbound._paginate')
    def test_new_only_skips_existing_images(self, mock_paginate):
        locale = Locale.get_default()
        gid = 'gid://shopify/Product/103'
        page = ProductPage(
            title='Existing',
            slug='existing',
            shopify_id=gid,
            locale=locale,
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()
        ProductPageImage.objects.create(
            page=page,
            shopify_id='gid://shopify/MediaImage/old',
            url='https://cdn.shopify.com/old.jpg',
            alt_text='Old',
            sort_order=0,
        )

        mock_paginate.return_value = iter([
            _make_product_node(
                gid,
                'existing',
                'Updated Title',
                images=_make_image_edges(2),
            ),
        ])

        stats = import_products(
            'test-shop.myshopify.com',
            self.parent,
            new_only=True,
        )

        self.assertEqual(stats['skipped'], 1)
        page.refresh_from_db()
        self.assertEqual(page.title, 'Existing')
        images = list(page.shopify_images.all())
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0].url, 'https://cdn.shopify.com/old.jpg')


class ImportCollectionImageTests(TestCase):
    def setUp(self):
        ShopConfig.objects.create(
            shop='test-shop.myshopify.com',
            access_token='tok',
        )
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.parent = ShopifyRootPage(title='Root', slug='root', locale=locale)
        home.add_child(instance=self.parent)
        self.parent.save_revision().publish()

    @patch('shopify_content.sync.inbound._paginate')
    def test_import_collection_saves_image_url(self, mock_paginate):
        gid = 'gid://shopify/Collection/1'
        mock_paginate.return_value = iter([
            {
                'id': gid,
                'title': 'Summer',
                'handle': 'summer',
                'sortOrder': 'MANUAL',
                'seo': {'title': '', 'description': ''},
                'descriptionHtml': '',
                'image': {
                    'id': 'gid://shopify/MediaImage/99',
                    'url': 'https://cdn.shopify.com/collection.jpg',
                    'altText': 'Summer collection',
                },
            },
        ])

        import_collections('test-shop.myshopify.com', self.parent)

        page = CollectionPage.objects.get(shopify_id=gid)
        self.assertEqual(page.image_url, 'https://cdn.shopify.com/collection.jpg')
        self.assertEqual(page.image_alt_text, 'Summer collection')
        self.assertEqual(page.shopify_image_id, 'gid://shopify/MediaImage/99')


class ImportArticleImageTests(TestCase):
    def setUp(self):
        ShopConfig.objects.create(
            shop='test-shop.myshopify.com',
            access_token='tok',
        )
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.parent = ShopifyRootPage(title='Root', slug='root', locale=locale)
        home.add_child(instance=self.parent)
        self.parent.save_revision().publish()
        self.blog = BlogPage(title='News', slug='news', locale=locale)
        self.parent.add_child(instance=self.blog)
        self.blog.save_revision().publish()

    @patch('shopify_content.sync.inbound._paginate')
    def test_import_article_saves_featured_image_url(self, mock_paginate):
        blog_gid = 'gid://shopify/Blog/1'
        art_gid = 'gid://shopify/Article/1'
        self.blog.shopify_id = blog_gid
        self.blog.save()

        def paginate_side_effect(shop, query, data_path, variables=None):
            if data_path == 'blogs':
                return iter([
                    {
                        'id': blog_gid,
                        'title': 'News',
                        'handle': 'news',
                        'commentPolicy': 'CLOSED',
                    },
                ])
            if data_path == 'blog.articles':
                return iter([
                    {
                        'id': art_gid,
                        'title': 'Hello',
                        'handle': 'hello',
                        'author': {'name': 'Author'},
                        'publishedAt': None,
                        'summary': '',
                        'tags': [],
                        'body': '<p>Body</p>',
                        'image': {
                            'id': 'gid://shopify/MediaImage/50',
                            'url': 'https://cdn.shopify.com/article.jpg',
                            'altText': 'Article hero',
                        },
                    },
                ])
            return iter([])

        mock_paginate.side_effect = paginate_side_effect

        import_blogs_and_articles('test-shop.myshopify.com', self.parent)

        page = ArticlePage.objects.get(shopify_id=art_gid)
        self.assertEqual(page.featured_image_url, 'https://cdn.shopify.com/article.jpg')
        self.assertEqual(page.featured_image_alt, 'Article hero')
        self.assertEqual(page.shopify_featured_image_id, 'gid://shopify/MediaImage/50')
        self.assertEqual(page.seo_title, '')
        self.assertEqual(page.search_description, '')

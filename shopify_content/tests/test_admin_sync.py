from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from wagtail.models import Locale, Page

from core.models import ShopConfig
from shopify_content.models import ProductPage, ShopifyRootPage
from shopify_content.sync.inbound import import_products
from shopify_content.sync.service import run_shopify_import


def _make_product_node(gid, handle, title):
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
        'metafields': {'edges': []},
    }


class ImportNewOnlyTests(TestCase):
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

        self.existing_gid = 'gid://shopify/Product/1'
        existing = ProductPage(
            title='Existing Product',
            slug='existing-product',
            shopify_id=self.existing_gid,
            locale=locale,
        )
        self.parent.add_child(instance=existing)
        existing.save_revision().publish()

    @patch('shopify_content.sync.inbound._paginate')
    def test_import_products_new_only_skips_existing_and_creates_new(self, mock_paginate):
        new_gid = 'gid://shopify/Product/2'
        mock_paginate.return_value = iter([
            _make_product_node(self.existing_gid, 'existing-product', 'Existing Product'),
            _make_product_node(new_gid, 'new-product', 'New Product'),
        ])

        stats = import_products(
            'test-shop.myshopify.com',
            self.parent,
            new_only=True,
        )

        self.assertEqual(stats['created'], 1)
        self.assertEqual(stats['updated'], 0)
        self.assertEqual(stats['skipped'], 1)
        self.assertEqual(stats['errors'], 0)
        self.assertTrue(ProductPage.objects.filter(shopify_id=new_gid).exists())
        self.assertEqual(ProductPage.objects.filter(shopify_id=self.existing_gid).count(), 1)

    @patch('shopify_content.sync.inbound._paginate')
    def test_import_products_full_sync_updates_existing(self, mock_paginate):
        mock_paginate.return_value = iter([
            _make_product_node(self.existing_gid, 'existing-product', 'Updated Title'),
        ])

        stats = import_products(
            'test-shop.myshopify.com',
            self.parent,
            new_only=False,
        )

        self.assertEqual(stats['created'], 0)
        self.assertEqual(stats['updated'], 1)
        self.assertEqual(stats['skipped'], 0)
        page = ProductPage.objects.get(shopify_id=self.existing_gid)
        self.assertEqual(page.title, 'Updated Title')


class RunShopifyImportTests(TestCase):
    @patch('shopify_content.sync.service._import_blogs')
    @patch('shopify_content.sync.service._import_collections')
    @patch('shopify_content.sync.service._import_products')
    @patch('shopify_content.sync.service._get_shop')
    def test_run_shopify_import_all_aggregates_stats(
        self,
        mock_get_shop,
        mock_import_products,
        mock_import_collections,
        mock_import_blogs,
    ):
        mock_get_shop.return_value = 'test-shop.myshopify.com'
        mock_import_products.return_value = {
            'created': 2, 'updated': 0, 'skipped': 1, 'errors': 0,
        }
        mock_import_collections.return_value = {
            'created': 1, 'updated': 0, 'skipped': 0, 'errors': 0,
        }
        mock_import_blogs.return_value = {
            'blogs': {'created': 1, 'updated': 0, 'skipped': 0, 'errors': 0},
            'articles': {'created': 3, 'updated': 0, 'skipped': 2, 'errors': 1},
        }

        result = run_shopify_import('all', new_only=True)

        self.assertEqual(result['resource'], 'all')
        self.assertEqual(result['stats']['created'], 7)
        self.assertEqual(result['stats']['skipped'], 3)
        self.assertEqual(result['stats']['errors'], 1)
        mock_import_products.assert_called_once_with('test-shop.myshopify.com', new_only=True)
        mock_import_collections.assert_called_once_with('test-shop.myshopify.com', new_only=True)
        mock_import_blogs.assert_called_once_with('test-shop.myshopify.com', new_only=True)


class ShopifySyncViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password',
        )
        self.client.login(username='admin', password='password')

    def test_get_requires_admin_login(self):
        self.client.logout()
        response = self.client.get(reverse('shopify_sync'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

    def test_get_renders_sync_page(self):
        ShopConfig.objects.create(
            shop='test-shop.myshopify.com',
            access_token='tok',
        )
        response = self.client.get(reverse('shopify_sync'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sincronizar desde Shopify')
        self.assertContains(response, 'test-shop.myshopify.com')
        self.assertContains(response, 'Importar productos nuevos')

    def test_get_shows_warning_when_shop_not_configured(self):
        response = self.client.get(reverse('shopify_sync'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No hay una tienda Shopify conectada')

    @patch('shopify_content.admin.sync_views.run_shopify_import')
    def test_post_triggers_new_only_import(self, mock_run_import):
        ShopConfig.objects.create(
            shop='test-shop.myshopify.com',
            access_token='tok',
        )
        mock_run_import.return_value = {
            'resource': 'products',
            'stats': {'created': 1, 'updated': 0, 'skipped': 0, 'errors': 0},
            'message': 'Productos — Creados: 1, Omitidos: 0, Errores: 0',
        }

        response = self.client.post(
            reverse('shopify_sync'),
            data={'resource': 'products'},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('shopify_sync'))
        mock_run_import.assert_called_once_with('products', new_only=True)

    def test_post_rejects_invalid_resource(self):
        ShopConfig.objects.create(
            shop='test-shop.myshopify.com',
            access_token='tok',
        )
        response = self.client.post(
            reverse('shopify_sync'),
            data={'resource': 'invalid'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('shopify_sync'))

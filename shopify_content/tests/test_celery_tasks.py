from unittest.mock import patch

from django.test import TestCase, override_settings
from wagtail.models import Locale, Page

from core.models import ShopConfig
from shopify_content.models import ProductPage, ShopifySyncRun
from shopify_content.models.root import ShopifyRootPage
from shopify_content.sync.task_dispatch import enqueue_shopify_import
from shopify_content.tasks import run_shopify_import_task, sync_page_to_shopify_task


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class CeleryImportTaskTests(TestCase):
    @patch('shopify_content.sync.inbound._paginate')
    def test_enqueue_shopify_import_completes_sync_run(self, mock_paginate):
        ShopConfig.objects.create(shop='test-shop.myshopify.com', access_token='tok')
        mock_paginate.return_value = iter([])

        sync_run = enqueue_shopify_import('products', new_only=True)
        sync_run.refresh_from_db()

        self.assertEqual(sync_run.status, ShopifySyncRun.STATUS_SUCCESS)
        self.assertIn('Productos', sync_run.message)

    @patch('shopify_content.sync.service.run_shopify_import')
    def test_run_shopify_import_task_marks_failed_on_error(self, mock_import):
        sync_run = ShopifySyncRun.objects.create(
            kind=ShopifySyncRun.KIND_INBOUND,
            resource='products',
            new_only=True,
        )
        mock_import.side_effect = RuntimeError('No ShopConfig')

        with self.assertRaises(RuntimeError):
            run_shopify_import_task(sync_run.pk, 'products', new_only=True)

        sync_run.refresh_from_db()
        self.assertEqual(sync_run.status, ShopifySyncRun.STATUS_FAILED)
        self.assertIn('No ShopConfig', sync_run.error_detail)


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class CeleryOutboundTaskTests(TestCase):
    def setUp(self):
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.parent = ShopifyRootPage(title='Root', slug='root', locale=locale)
        home.add_child(instance=self.parent)
        self.parent.save_revision().publish()

    @patch('shopify_content.sync.outbound.sync_product_page', return_value=True)
    def test_sync_page_to_shopify_task_success(self, mock_sync):
        page = ProductPage(
            title='Test Product',
            slug='test-product',
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

        sync_run.refresh_from_db()
        self.assertEqual(sync_run.status, ShopifySyncRun.STATUS_SUCCESS)
        mock_sync.assert_called_once()

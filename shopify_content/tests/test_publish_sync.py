from unittest.mock import patch

from django.db import transaction
from django.test import TestCase, TransactionTestCase, override_settings
from wagtail.models import Locale, Page

from shopify_content.models import LocationPage, ShopifyRootPage, ShopifySyncRun
from shopify_content.sync.publish_sync import queue_shopify_sync_on_publish
from shopify_content.sync.task_dispatch import enqueue_page_outbound_sync


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class PublishSyncSignalTests(TestCase):
    def setUp(self):
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.parent = ShopifyRootPage(title='Root', slug='root', locale=locale)
        home.add_child(instance=self.parent)
        self.parent.save_revision().publish()

    @patch('shopify_content.sync.outbound.sync_location_page', return_value=(True, 'ok'))
    def test_revision_publish_queues_outbound_sync(self, mock_sync):
        page = LocationPage(
            title='NYC',
            slug='nyc',
            titulo='NYC',
            locale=Locale.get_default(),
            sync_enabled=True,
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()

        sync_run = ShopifySyncRun.objects.filter(
            page=page,
            kind=ShopifySyncRun.KIND_OUTBOUND,
        ).first()
        self.assertIsNotNone(sync_run)
        self.assertEqual(sync_run.status, ShopifySyncRun.STATUS_SUCCESS)
        mock_sync.assert_called_once()

    @patch('shopify_content.sync.task_dispatch.enqueue_page_outbound_sync')
    def test_bulk_publish_path_calls_enqueue_via_page_published(self, mock_enqueue):
        sync_run = ShopifySyncRun.objects.create(
            kind=ShopifySyncRun.KIND_OUTBOUND,
            message='queued',
        )
        mock_enqueue.return_value = sync_run

        page = LocationPage(
            title='LA',
            slug='la',
            titulo='LA',
            locale=Locale.get_default(),
            sync_enabled=True,
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()

        mock_enqueue.assert_called_once()
        called_page = mock_enqueue.call_args[0][0]
        self.assertEqual(called_page.pk, page.pk)

    def test_sync_disabled_skips_enqueue(self):
        page = LocationPage(
            title='Miami',
            slug='miami',
            titulo='Miami',
            locale=Locale.get_default(),
            sync_enabled=False,
        )
        self.parent.add_child(instance=page)

        result = queue_shopify_sync_on_publish(page)
        self.assertIsNone(result)
        self.assertFalse(
            ShopifySyncRun.objects.filter(page=page).exists(),
        )


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class BulkPublishTransactionTests(TransactionTestCase):
    def setUp(self):
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.parent = ShopifyRootPage(title='Root', slug='root', locale=locale)
        home.add_child(instance=self.parent)
        self.parent.save_revision().publish()

    @patch('shopify_content.tasks.sync_page_to_shopify_task.delay')
    def test_enqueue_waits_until_bulk_transaction_commits(self, mock_delay):
        mock_delay.return_value = type('Result', (), {'id': 'task-id'})()

        pages = []
        for slug in ('city-a', 'city-b', 'city-c'):
            page = LocationPage(
                title=slug,
                slug=slug,
                titulo=slug,
                locale=Locale.get_default(),
                sync_enabled=True,
            )
            self.parent.add_child(instance=page)
            pages.append(page)

        with transaction.atomic():
            for page in pages:
                enqueue_page_outbound_sync(page)
            mock_delay.assert_not_called()

        self.assertEqual(mock_delay.call_count, len(pages))
        self.assertEqual(
            ShopifySyncRun.objects.filter(kind=ShopifySyncRun.KIND_OUTBOUND).count(),
            len(pages),
        )

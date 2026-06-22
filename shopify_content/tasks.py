"""
Celery tasks for Shopify ↔ Wagtail sync.
"""

import logging

from celery import shared_task
from wagtail.models import Page

from shopify_content.models.sync_run import ShopifySyncRun
from shopify_content.sync.service import run_shopify_import

logger = logging.getLogger(__name__)


def _get_sync_run(sync_run_id: int) -> ShopifySyncRun:
    return ShopifySyncRun.objects.get(pk=sync_run_id)


@shared_task(bind=True, name='shopify_content.tasks.run_shopify_import_task')
def run_shopify_import_task(self, sync_run_id: int, resource: str, new_only: bool = False):
    sync_run = _get_sync_run(sync_run_id)
    sync_run.mark_running()
    try:
        result = run_shopify_import(resource, new_only=new_only)
        sync_run.mark_success(message=result['message'], stats=result['stats'])
        return result
    except Exception as exc:
        logger.exception(
            'Shopify import task failed sync_run_id=%s resource=%s',
            sync_run_id,
            resource,
        )
        sync_run.mark_failed(error_detail=str(exc))
        raise


@shared_task(bind=True, name='shopify_content.tasks.sync_page_to_shopify_task')
def sync_page_to_shopify_task(self, sync_run_id: int, page_id: int):
    from shopify_content.models import (
        ProductPage,
        CollectionPage,
        BlogPage,
        ArticlePage,
        LocationPage,
        GlossaryTermPage,
    )
    from shopify_content.sync.outbound import (
        sync_product_page,
        sync_collection_page,
        sync_blog_page,
        sync_article_page,
        sync_location_page,
        sync_glossary_term_page,
    )

    sync_run = _get_sync_run(sync_run_id)
    sync_run.mark_running()

    page_sync_map = {
        ProductPage: sync_product_page,
        CollectionPage: sync_collection_page,
        BlogPage: sync_blog_page,
        ArticlePage: sync_article_page,
        LocationPage: sync_location_page,
        GlossaryTermPage: sync_glossary_term_page,
    }

    try:
        page = Page.objects.get(pk=page_id)
        specific = page.specific
        sync_fn = page_sync_map.get(type(specific))

        if sync_fn is None:
            sync_run.mark_failed(
                error_detail=f'Page type {type(specific).__name__} is not syncable.',
            )
            return {'success': False}

        if not getattr(specific, 'sync_enabled', True):
            sync_run.mark_success(message='Sync disabled for this page; skipped.')
            return {'success': False, 'skipped': True}

        raw = sync_fn(specific)
        if isinstance(raw, tuple):
            success, detail = raw
        else:
            success, detail = bool(raw), ""

        if success:
            sync_run.mark_success(
                message=detail or f'"{page.title}" synced to Shopify successfully.',
                stats={'success': True},
            )
        else:
            sync_run.mark_failed(
                message=f'"{page.title}" publish sync failed.',
                error_detail=detail or 'sync_*_page returned False; check server logs.',
            )
        return {'success': success, 'message': detail}
    except Page.DoesNotExist:
        sync_run.mark_failed(error_detail=f'Page id={page_id} not found.')
        raise
    except Exception as exc:
        logger.exception(
            'Outbound sync task failed sync_run_id=%s page_id=%s',
            sync_run_id,
            page_id,
        )
        sync_run.mark_failed(error_detail=str(exc))
        raise


@shared_task(name='shopify_content.tasks.scheduled_import_new_content')
def scheduled_import_new_content():
    """Periodic beat entrypoint: import all new Shopify content into Wagtail."""
    from shopify_content.sync.task_dispatch import enqueue_shopify_import

    enqueue_shopify_import('all', new_only=True)

"""
Wagtail hooks for shopify_content.

Outbound sync is queued via the page_published signal (all publish paths,
including bulk actions and API publish). These hooks only surface admin feedback.
"""

import logging

from django.urls import path, reverse
from wagtail import hooks
from wagtail.admin import messages as wagtail_messages
from wagtail.admin.menu import MenuItem

from .admin.sync_views import ShopifySyncView
from .models.sync_run import ShopifySyncRun
from .sync.publish_sync import is_syncable_page

logger = logging.getLogger(__name__)


@hooks.register('register_admin_urls')
def register_shopify_sync_urls():
    return [
        path('shopify-sync/', ShopifySyncView.as_view(), name='shopify_sync'),
    ]


@hooks.register('register_settings_menu_item')
def register_shopify_sync_menu_item():
    return MenuItem(
        'Shopify Sync',
        reverse('shopify_sync'),
        icon_name='download',
        order=100,
    )


def _latest_outbound_sync_run(page):
    return (
        page.shopify_sync_runs.filter(kind=ShopifySyncRun.KIND_OUTBOUND)
        .order_by('-created_at')
        .first()
    )


def _notify_sync_queued(request, page):
    sync_run = _latest_outbound_sync_run(page)
    if sync_run and sync_run.status in (
        ShopifySyncRun.STATUS_PENDING,
        ShopifySyncRun.STATUS_RUNNING,
        ShopifySyncRun.STATUS_SUCCESS,
    ):
        wagtail_messages.success(
            request,
            (
                f'"{page.title}" encolado para sincronizar con Shopify '
                f'(job id={sync_run.pk}).'
            ),
            extra_tags='shopify-sync',
        )
        return

    wagtail_messages.error(
        request,
        (
            f'No se pudo encolar la sincronización con Shopify para "{page.title}". '
            'La página se publicó localmente. Consulta los logs del servidor.'
        ),
        extra_tags='shopify-sync-error',
    )


@hooks.register('after_publish_page')
def notify_shopify_sync_on_publish(request, page):
    """Show admin feedback after single-page publish (sync queued via page_published)."""
    specific_page = page.specific
    if not is_syncable_page(page):
        return
    if not getattr(specific_page, 'sync_enabled', True):
        return

    _notify_sync_queued(request, page)


@hooks.register('after_bulk_action')
def notify_shopify_sync_after_bulk_publish(request, action_type, objects, action_class_instance):
    """Show admin feedback after bulk publish (sync queued via page_published per page)."""
    if action_type != 'publish':
        return

    queued = 0
    failed = 0
    for page in objects:
        if not is_syncable_page(page):
            continue
        if not getattr(page.specific, 'sync_enabled', True):
            continue

        sync_run = _latest_outbound_sync_run(page)
        if sync_run and sync_run.status in (
            ShopifySyncRun.STATUS_PENDING,
            ShopifySyncRun.STATUS_RUNNING,
            ShopifySyncRun.STATUS_SUCCESS,
        ):
            queued += 1
        else:
            failed += 1
            logger.error(
                'Bulk publish: Shopify sync not queued for page pk=%s title=%r',
                page.pk,
                page.title,
            )

    if queued:
        wagtail_messages.success(
            request,
            (
                f'{queued} página(s) encolada(s) para sincronizar con Shopify '
                'tras la publicación masiva.'
            ),
            extra_tags='shopify-sync',
        )
    if failed:
        wagtail_messages.error(
            request,
            (
                f'No se pudo encolar la sincronización con Shopify para {failed} '
                'página(s). Consulta los logs del servidor.'
            ),
            extra_tags='shopify-sync-error',
        )

"""
Wagtail hooks for shopify_content.

Registers an after_publish_page hook that queues published Shopify content
pages for outbound sync to Shopify Admin via Celery.
"""

import logging

from django.urls import path, reverse
from wagtail import hooks
from wagtail.admin import messages as wagtail_messages
from wagtail.admin.menu import MenuItem

from .admin.sync_views import ShopifySyncView

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


@hooks.register('after_publish_page')
def sync_to_shopify_on_publish(request, page):
    """
    After a shopify_content page is published in Wagtail admin,
    queue outbound sync to Shopify Admin.
    """
    from .models import ProductPage, CollectionPage, BlogPage, ArticlePage, LocationPage

    page_sync_types = (
        ProductPage,
        CollectionPage,
        BlogPage,
        ArticlePage,
        LocationPage,
    )

    specific_page = page.specific
    if not isinstance(specific_page, page_sync_types):
        return

    if not getattr(specific_page, 'sync_enabled', True):
        return

    try:
        sync_run = enqueue_page_outbound_sync(page)
        if sync_run is None:
            return
        wagtail_messages.success(
            request,
            (
                f'"{page.title}" encolado para sincronizar con Shopify '
                f'(job id={sync_run.pk}).'
            ),
            extra_tags='shopify-sync',
        )
    except Exception:
        logger.exception(
            'Unhandled error queueing after_publish_page Shopify sync for page pk=%s',
            page.pk,
        )
        wagtail_messages.error(
            request,
            (
                f'No se pudo encolar la sincronización con Shopify para "{page.title}". '
                'La página se publicó localmente. Consulta los logs del servidor.'
            ),
            extra_tags='shopify-sync-error',
        )

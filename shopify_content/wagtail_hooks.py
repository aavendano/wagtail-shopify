"""
Wagtail hooks for shopify_content.

Registers an after_publish_page hook that automatically syncs published
Shopify content pages to Shopify Admin via GraphQL.

Sync is synchronous and non-blocking: if it fails, the publish still succeeds
and the editor sees a warning message. For high-volume stores, replace the
direct call with a background task (Celery, Django-Q, etc.).
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
    push the changes to Shopify Admin.
    """
    # Lazy imports keep the Shopify SDK out of the startup path.
    from .models import ProductPage, CollectionPage, BlogPage, ArticlePage, LocationPage
    from .sync.outbound import (
        sync_product_page,
        sync_collection_page,
        sync_blog_page,
        sync_article_page,
        sync_location_page,
    )

    page_sync_map = {
        ProductPage: sync_product_page,
        CollectionPage: sync_collection_page,
        BlogPage: sync_blog_page,
        ArticlePage: sync_article_page,
        LocationPage: sync_location_page,
    }

    specific_page = page.specific
    sync_fn = page_sync_map.get(type(specific_page))

    if sync_fn is None:
        return  # Not a shopify_content page; nothing to do

    try:
        success = sync_fn(specific_page)
        if success:
            wagtail_messages.success(
                request,
                f'"{page.title}" synced to Shopify successfully.',
                extra_tags='shopify-sync',
            )
        else:
            wagtail_messages.warning(
                request,
                (
                    f'"{page.title}" was published but Shopify sync failed. '
                    'Check the server logs for details.'
                ),
                extra_tags='shopify-sync-error',
            )
    except Exception:
        logger.exception(
            'Unhandled error in after_publish_page Shopify sync for page pk=%s', page.pk
        )
        wagtail_messages.error(
            request,
            (
                f'Shopify sync raised an unexpected error for "{page.title}". '
                'The page was published locally. Check server logs.'
            ),
            extra_tags='shopify-sync-error',
        )

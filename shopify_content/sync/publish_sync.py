"""Queue outbound Shopify sync when syncable pages are published."""

import logging

from shopify_content.sync.task_dispatch import enqueue_page_outbound_sync

logger = logging.getLogger(__name__)


def get_syncable_page_types():
    from shopify_content.models import (
        ArticlePage,
        BlogPage,
        CollectionPage,
        GlossaryTermPage,
        LocationPage,
        ProductPage,
    )

    return (
        ProductPage,
        CollectionPage,
        BlogPage,
        ArticlePage,
        LocationPage,
        GlossaryTermPage,
    )


def is_syncable_page(page) -> bool:
    return isinstance(page.specific, get_syncable_page_types())


def queue_shopify_sync_on_publish(page):
    """
    Enqueue outbound sync if page type is supported and sync_enabled.

    Returns ShopifySyncRun or None. Logs errors without raising.
    """
    if not is_syncable_page(page):
        return None

    specific = page.specific
    if not getattr(specific, 'sync_enabled', True):
        return None

    try:
        return enqueue_page_outbound_sync(page)
    except Exception:
        logger.exception(
            'Failed to queue Shopify sync on publish for page pk=%s',
            page.pk,
        )
        return None

"""Pluggable export_config consumers for ShopifyRootPage → Shopify resources."""

from .registry import (
    get_consumer_for_root,
    get_consumer_for_slug,
    on_content_page_changed,
    queue_index_sync_for_content_page,
    registered_root_slugs,
)

__all__ = [
    'get_consumer_for_root',
    'get_consumer_for_slug',
    'on_content_page_changed',
    'queue_index_sync_for_content_page',
    'registered_root_slugs',
]

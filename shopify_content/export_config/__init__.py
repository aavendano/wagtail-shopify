"""Pluggable export_config consumers for ShopifyRootPage → Shopify resources."""

from .registry import (
    get_consumer_for_root,
    get_consumer_for_slug,
    on_content_page_changed,
    on_root_published,
    queue_index_sync,
    registered_root_slugs,
)

__all__ = [
    'get_consumer_for_root',
    'get_consumer_for_slug',
    'on_content_page_changed',
    'on_root_published',
    'queue_index_sync',
    'registered_root_slugs',
]

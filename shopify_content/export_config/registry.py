"""Registry of export_config consumers keyed by ShopifyRootPage slug."""

from __future__ import annotations

from typing import TYPE_CHECKING

from shopify_content.export_config.base import PageIndexConsumer
from shopify_content.export_config.glossary import glossary_index_consumer
from shopify_content.export_config.location import location_index_consumer

if TYPE_CHECKING:
    from shopify_content.models import ShopifyRootPage

_CONSUMERS_BY_SLUG: dict[str, PageIndexConsumer] = {
    glossary_index_consumer.root_slug: glossary_index_consumer,
    location_index_consumer.root_slug: location_index_consumer,
}


def registered_root_slugs() -> list[str]:
    return list(_CONSUMERS_BY_SLUG.keys())


def get_consumer_for_slug(slug: str) -> PageIndexConsumer | None:
    return _CONSUMERS_BY_SLUG.get(slug)


def get_consumer_for_root(root: ShopifyRootPage) -> PageIndexConsumer | None:
    return get_consumer_for_slug(root.slug)


def queue_index_sync(*, root_slug: str, locale_codes: list[str] | None = None) -> None:
    consumer = get_consumer_for_slug(root_slug)
    if consumer is not None:
        consumer.queue_sync(locale_codes=locale_codes)


def queue_index_sync_for_content_page(page) -> None:
    """Rebuild index locale(s) after a child page was synced to Shopify."""
    on_content_page_changed(page)


def on_root_published(root) -> None:
    specific = root.specific if hasattr(root, 'specific') else root
    consumer = get_consumer_for_slug(specific.slug)
    if consumer is not None:
        consumer.queue_sync()


def on_content_page_changed(page) -> None:
    """Rebuild index locale(s) when a child page affecting an index changes."""
    specific = page.specific if hasattr(page, 'specific') else page
    parent = specific.get_parent()
    if parent is None:
        return
    parent_specific = parent.specific
    consumer = get_consumer_for_slug(parent_specific.slug)
    if consumer is None:
        return
    locale_codes = consumer.locale_codes_for_page(specific)
    if locale_codes:
        consumer.queue_sync(locale_codes=locale_codes)

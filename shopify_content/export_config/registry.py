"""Registry of export_config consumers keyed by ShopifyRootPage slug."""

from __future__ import annotations

from typing import TYPE_CHECKING

from shopify_content.export_config.base import RootIndexConsumer
from shopify_content.export_config.blog import BlogListingsConsumer, blog_listings_consumer
from shopify_content.export_config.glossary import glossary_index_consumer
from shopify_content.export_config.location import location_index_consumer
from shopify_content.export_config.single_page import SinglePageListingsConsumer

if TYPE_CHECKING:
    from shopify_content.models import ShopifyRootPage

ExportConsumer = RootIndexConsumer | SinglePageListingsConsumer | BlogListingsConsumer

_CONSUMERS_BY_SLUG: dict[str, ExportConsumer] = {
    glossary_index_consumer.root_slug: glossary_index_consumer,
    location_index_consumer.root_slug: location_index_consumer,
    blog_listings_consumer.root_slug: blog_listings_consumer,
}


def registered_root_slugs() -> list[str]:
    return list(_CONSUMERS_BY_SLUG.keys())


def get_consumer_for_slug(slug: str) -> ExportConsumer | None:
    return _CONSUMERS_BY_SLUG.get(slug)


def get_consumer_for_root(root: ShopifyRootPage) -> ExportConsumer | None:
    return get_consumer_for_slug(root.slug)


def _find_shopify_root_ancestor(page):
    """Walk up the tree until a ShopifyRootPage ancestor is found."""
    from shopify_content.models import ShopifyRootPage

    ancestor = page.get_parent()
    while ancestor is not None:
        specific = ancestor.specific
        if isinstance(specific, ShopifyRootPage):
            return specific
        ancestor = ancestor.get_parent()
    return None


def queue_index_sync(*, root_slug: str, locale_codes: list[str] | None = None) -> None:
    consumer = get_consumer_for_slug(root_slug)
    if consumer is not None:
        consumer.queue_sync(locale_codes=locale_codes)


def queue_index_sync_for_content_page(page) -> None:
    """Rebuild index locale(s) after a child page was synced to Shopify."""
    on_content_page_changed(page)


def on_root_published(root) -> None:
    """
    Queue index rebuild for single-Page consumers (blog).

    Glossary/locations RootIndexConsumers sync via sync_shopify_root_page on the
    standard publish→sync path; do not double-queue them here.
    """
    specific = root.specific if hasattr(root, 'specific') else root
    consumer = get_consumer_for_slug(specific.slug)
    if consumer is None or isinstance(consumer, RootIndexConsumer):
        return
    consumer.queue_sync()


def on_content_page_changed(page) -> None:
    """Rebuild index when a child page affecting an index changes."""
    specific = page.specific if hasattr(page, 'specific') else page
    root = _find_shopify_root_ancestor(specific)
    if root is None:
        return
    consumer = get_consumer_for_slug(root.slug)
    if consumer is None:
        return
    locale_codes = consumer.locale_codes_for_page(specific)
    if locale_codes:
        consumer.queue_sync(locale_codes=locale_codes)

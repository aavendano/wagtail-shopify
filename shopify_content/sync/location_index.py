"""Push precomputed location index JSON to Shopify Pages via metafieldsSet."""

from __future__ import annotations

from shopify_content.export_config.location import (
    LOCATION_ROOT_SLUG,
    location_index_consumer,
)


def get_location_root_page():
    return location_index_consumer.get_root_page()


def get_location_index_config(root=None) -> dict | None:
    return location_index_consumer.get_config(root)


def sync_location_index_pages(
    *,
    locale_codes: list[str] | None = None,
    dry_run: bool = False,
) -> dict:
    return location_index_consumer.sync(dry_run=dry_run)


def queue_location_index_sync(*, locale_codes: list[str] | None = None) -> None:
    location_index_consumer.queue_sync(locale_codes=locale_codes)

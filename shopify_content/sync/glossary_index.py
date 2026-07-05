"""Push precomputed glossary index JSON to Shopify Pages via metafieldsSet."""

from __future__ import annotations

from shopify_content.export_config.glossary import (
    GLOSSARY_ROOT_SLUG,
    glossary_index_consumer,
)

METAFIELD_NAMESPACE = 'custom'
METAFIELD_LOCALE_KEY = 'glossary_locale'
METAFIELD_INDEX_KEY = 'glossary_index'


def get_glossary_root_page():
    return glossary_index_consumer.get_root_page()


def get_glossary_index_config(root=None) -> dict | None:
    return glossary_index_consumer.get_config(root)


def sync_glossary_index_pages(
    *,
    locale_codes: list[str] | None = None,
    dry_run: bool = False,
) -> dict:
    return glossary_index_consumer.sync(locale_codes=locale_codes, dry_run=dry_run)


def queue_glossary_index_sync(*, locale_codes: list[str] | None = None) -> None:
    glossary_index_consumer.queue_sync(locale_codes=locale_codes)

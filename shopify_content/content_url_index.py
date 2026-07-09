"""Rebuild and maintain the ContentUrlIndex materialized mapping."""

from __future__ import annotations

import logging

from django.db import transaction

from shopify_content.models.content_url_index import ContentUrlIndex
from shopify_content.storefront_urls import (
    page_index_metadata,
    path_variants_for_index,
    storefront_path_for_page,
)
from shopify_content.sync.publish_sync import get_syncable_page_types

logger = logging.getLogger(__name__)


def _page_locale_code(page) -> str:
    specific = page.specific
    if hasattr(specific, 'locale') and specific.locale_id:
        return specific.locale.language_code
    return ''


def _is_indexable(page) -> bool:
    """Only live pages with a non-empty shopify_id and a resolvable storefront path."""
    specific = page.specific
    if not page.live:
        return False
    if not getattr(specific, 'shopify_id', ''):
        return False
    return storefront_path_for_page(page) is not None


def _rows_for_page(page) -> list[ContentUrlIndex]:
    variants = path_variants_for_index(page)
    if not variants:
        return []

    content_type, handle, blog_handle = page_index_metadata(page)
    locale = _page_locale_code(page)

    return [
        ContentUrlIndex(
            normalized_path=variant.normalized_path,
            wagtail_page_id=page.pk,
            content_type=content_type,
            handle=handle,
            blog_handle=blog_handle,
            locale=locale,
            locale_prefix=variant.locale_prefix,
            is_canonical=variant.is_canonical,
        )
        for variant in variants
    ]


def clear_index_for_page(page_id: int) -> int:
    deleted, _ = ContentUrlIndex.objects.filter(wagtail_page_id=page_id).delete()
    return deleted


@transaction.atomic
def rebuild_index_for_page(page) -> int:
    """Replace index rows for a single page. Returns number of rows created."""
    page = page.specific if hasattr(page, 'specific') else page
    page_pk = page.pk
    clear_index_for_page(page_pk)

    if not _is_indexable(page):
        return 0

    rows = _rows_for_page(page)
    if rows:
        ContentUrlIndex.objects.bulk_create(rows)
    return len(rows)


@transaction.atomic
def rebuild_full_index() -> dict[str, int]:
    """Truncate and rebuild the full content URL index."""
    ContentUrlIndex.objects.all().delete()

    created = 0
    skipped = 0
    for model in get_syncable_page_types():
        for page in model.objects.live().select_related('locale'):
            if not _is_indexable(page):
                skipped += 1
                continue
            rows = _rows_for_page(page)
            if rows:
                ContentUrlIndex.objects.bulk_create(rows)
                created += len(rows)
            else:
                skipped += 1

    logger.info(
        'Content URL index rebuilt: %d rows, %d pages skipped',
        created,
        skipped,
    )
    return {'created': created, 'skipped': skipped}


def indexed_paths_for_page(page_id: int) -> list[str]:
    """Return indexed storefront paths for a page (for admin/API display)."""
    entries = ContentUrlIndex.objects.filter(wagtail_page_id=page_id).order_by(
        '-is_canonical', 'locale_prefix',
    )
    paths: list[str] = []
    for entry in entries:
        if entry.locale_prefix:
            paths.append(f'/{entry.locale_prefix}{entry.normalized_path}')
        else:
            paths.append(entry.normalized_path)
    return paths

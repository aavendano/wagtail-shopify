"""Git-authoritative adapter for LocationPage outbound publication.

Phase E externalizes the six single-value RichText sections on ``LocationPage``.
The legacy Shopify serializer still expects those values on the Wagtail instance,
so this adapter overlays the authoritative domain values in-memory for the
single duration of the outbound call and restores the DB-backed values
unconditionally afterwards.

This is deliberately NOT persistence: no model save, filesystem write, or Git
command happens here. The authoritative read is always ``page.editorial.<field>``.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from shopify_content.content_store.accessors import MIRRORED_FIELDS, is_git_authoritative

from .outbound import sync_location_page as _legacy_sync_location_page

_LOCATION_CONTENT_TYPE = 'shopify_content.locationpage'
LOCATION_EDITORIAL_FIELDS = tuple(
    field_key
    for content_type, field_key in sorted(MIRRORED_FIELDS)
    if content_type == _LOCATION_CONTENT_TYPE
)


@contextmanager
def _authoritative_location_overlay(page) -> Iterator[None]:
    """Temporarily expose Git-authoritative RichText through legacy attributes."""
    if not is_git_authoritative():
        yield
        return

    originals = {
        field_key: getattr(page, field_key)
        for field_key in LOCATION_EDITORIAL_FIELDS
    }
    try:
        # Resolve every value through the domain boundary. A missing file raises
        # ContentNotFound and aborts publication rather than silently using DB.
        for field_key in LOCATION_EDITORIAL_FIELDS:
            setattr(page, field_key, getattr(page.editorial, field_key))
        yield
    finally:
        # The adapter is read-only. Never leak the overlay back into Wagtail or
        # a later save/revision operation, even if Shopify sync raises.
        for field_key, value in originals.items():
            setattr(page, field_key, value)


def _validate_authoritative_location_content(page) -> tuple[bool, str]:
    """Preserve LocationPage editorial rules after authority moves out of DB.

    ``LocationPage.clean()`` historically validated the RichText columns. Once
    Git is authoritative those columns may be stale, so publication must apply
    the same forbidden-phrase rule to the overlaid authoritative values.
    """
    from shopify_content.content_templates.location_city_en_us import (
        find_forbidden_phrases,
    )

    parts = [
        str(getattr(page, field_key) or '')
        for field_key in LOCATION_EDITORIAL_FIELDS
    ]
    for faq in page.faqs.all():
        parts.append(faq.question)
        parts.append(faq.answer)

    forbidden = find_forbidden_phrases(' '.join(parts))
    if not forbidden:
        return True, ''
    return (
        False,
        'Sync aborted: authoritative Git content contains forbidden '
        'brick-and-mortar phrases: ' + ', '.join(forbidden),
    )


def sync_location_page(page):
    """Publish a LocationPage using Git-authoritative editorial RichText."""
    with _authoritative_location_overlay(page):
        valid, message = _validate_authoritative_location_content(page)
        if not valid:
            return False, message
        return _legacy_sync_location_page(page)


def install_location_editorial_sync() -> None:
    """Install the Phase E adapter at the existing outbound import surface.

    Keeping ``shopify_content.sync.outbound.sync_location_page`` stable avoids
    changing Celery/API/management callers while the legacy serializer is being
    decomposed. Installation is idempotent and happens from AppConfig.ready().
    """
    from . import outbound

    if outbound.sync_location_page is not sync_location_page:
        outbound.sync_location_page = sync_location_page

"""Shared helpers for multi-locale index_listings payloads."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timezone

INDEX_LISTINGS_VERSION = 1


def build_multi_locale_index(
    *,
    locale_codes: tuple[str, ...],
    build_locale_listing: Callable[[str], dict],
    generated_at: datetime | None = None,
) -> dict:
    """Build the common custom.index_listings envelope."""
    when = generated_at or datetime.now(timezone.utc)
    return {
        'version': INDEX_LISTINGS_VERSION,
        'generated_at': when.isoformat(),
        'locales': {
            locale_code: build_locale_listing(locale_code)
            for locale_code in locale_codes
        },
    }

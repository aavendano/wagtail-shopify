"""Validation helpers for blog/article available_locales fields."""

from __future__ import annotations

from django.core.exceptions import ValidationError

from config.settings import ALLOWED_LOCALE_CODES

ALLOWED_LOCALE_CODE_LIST: tuple[str, ...] = tuple(ALLOWED_LOCALE_CODES.keys())


def normalize_available_locales(locales) -> list[str]:
    """Return a deduplicated list of allowed Wagtail locale codes."""
    if not locales:
        return []
    normalized: list[str] = []
    for raw in locales:
        code = str(raw).strip()
        if not code or code not in ALLOWED_LOCALE_CODES:
            continue
        if code not in normalized:
            normalized.append(code)
    return normalized


def validate_available_locales(
    locales,
    *,
    page_locale_code: str | None,
    sync_enabled: bool,
) -> list[str]:
    """
    Validate and normalize available_locales for BlogPage / ArticlePage.

    When sync_enabled is true, at least one locale is required.
    The page's own locale must appear in the list when locales are set.
    """
    normalized = normalize_available_locales(locales)
    if sync_enabled and not normalized:
        raise ValidationError(
            'Select at least one available locale when Shopify sync is enabled.'
        )
    if page_locale_code and normalized and page_locale_code not in normalized:
        raise ValidationError(
            f"The page locale '{page_locale_code}' must be included in available locales."
        )
    return normalized


def default_available_locales_for_page(page) -> list[str]:
    """Default to the page's Wagtail locale when none are selected."""
    if getattr(page, 'locale_id', None):
        return [page.locale.language_code]
    return []

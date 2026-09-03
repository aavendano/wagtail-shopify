"""Centralized locale <-> content-path policy (Phase C).

The Git content topology uses lowercase, hyphenated locale roots
(``content/en-us/`` ...). This module is the ONE place that normalizes a
Wagtail locale code (e.g. ``en-US``) to its content-path segment (``en-us``).
Do not scatter this mapping elsewhere.
"""

from __future__ import annotations


class UnsupportedLocale(Exception):
    """Raised when a locale has no configured content-path mapping."""


# Wagtail locale code -> content-path segment. Mirrors the four supported
# storefront locales (see config.settings WAGTAIL_CONTENT_LANGUAGES).
_WAGTAIL_TO_CONTENT = {
    "en-US": "en-us",
    "en-CA": "en-ca",
    "fr-CA": "fr-ca",
    "es-US": "es-us",
}
_CONTENT_TO_WAGTAIL = {v: k for k, v in _WAGTAIL_TO_CONTENT.items()}


def supported_wagtail_locales() -> tuple[str, ...]:
    return tuple(_WAGTAIL_TO_CONTENT.keys())


def supported_content_locales() -> tuple[str, ...]:
    return tuple(_WAGTAIL_TO_CONTENT.values())


def to_content_locale(wagtail_code: str) -> str:
    """Map a Wagtail locale code to its content-path segment.

    Raises UnsupportedLocale for anything outside the configured set.
    """
    try:
        return _WAGTAIL_TO_CONTENT[wagtail_code]
    except KeyError as exc:
        raise UnsupportedLocale(
            f"No content-path mapping for locale {wagtail_code!r}; "
            f"supported: {sorted(_WAGTAIL_TO_CONTENT)}"
        ) from exc


def to_wagtail_locale(content_code: str) -> str:
    try:
        return _CONTENT_TO_WAGTAIL[content_code]
    except KeyError as exc:
        raise UnsupportedLocale(
            f"No Wagtail locale for content segment {content_code!r}"
        ) from exc

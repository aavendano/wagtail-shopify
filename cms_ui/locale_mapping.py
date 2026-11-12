"""Map Shopify Admin ``shopLocales`` codes to Wagtail ``ALLOWED_LOCALE_CODES``."""

from __future__ import annotations

from django.conf import settings

# Shopify often returns ISO 639-1 (`en`, `es`, `fr`) or regional tags (`en-CA`).
_SHOPIFY_TO_WAGTAIL: dict[str, str] = {
    "en": "en-US",
    "en-us": "en-US",
    "en_us": "en-US",
    "en-ca": "en-CA",
    "en_ca": "en-CA",
    "es": "es-US",
    "es-us": "es-US",
    "es_us": "es-US",
    "fr": "fr-CA",
    "fr-ca": "fr-CA",
    "fr_ca": "fr-CA",
}


def normalize_shopify_locale_tag(locale: str) -> str:
    return (locale or "").strip().replace("_", "-")


def shopify_locale_to_wagtail(locale: str) -> str | None:
    """Return a configured Wagtail UI locale or None if not supported."""
    if not locale:
        return None
    raw = normalize_shopify_locale_tag(locale)
    allowed = settings.ALLOWED_LOCALE_CODES
    if raw in allowed:
        return raw
    key = raw.lower()
    mapped = _SHOPIFY_TO_WAGTAIL.get(key)
    if mapped and mapped in allowed:
        return mapped
    return None


def wagtail_locale_label(code: str) -> str:
    return settings.ALLOWED_LOCALE_CODES.get(code, code)

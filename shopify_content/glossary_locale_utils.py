"""Map between Wagtail locale codes and glossary metaobject short locale codes."""

from __future__ import annotations

WAGTAIL_TO_GLOSSARY_LOCALE: dict[str, str] = {
    'en-US': 'en',
    'en-CA': 'en',
    'es-US': 'es',
    'fr-CA': 'fr',
}

GLOSSARY_TO_WAGTAIL_LOCALE: dict[str, str] = {
    'en': 'en-US',
    'es': 'es-US',
    'fr': 'fr-CA',
}


def glossary_locale_code_for_wagtail(wagtail_code: str) -> str:
    """Map a Wagtail locale code to the short code pushed to Shopify metaobjects."""
    return WAGTAIL_TO_GLOSSARY_LOCALE.get(wagtail_code, wagtail_code.split('-')[0])


def wagtail_locale_code_for_glossary(short_code: str) -> str:
    """Map a glossary short locale code to the canonical Wagtail locale code."""
    return GLOSSARY_TO_WAGTAIL_LOCALE.get(short_code, short_code)

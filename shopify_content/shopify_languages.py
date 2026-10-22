"""
Shopify languages and markets for Wagtail locales.

Shopify is the source of truth. The store has three languages (``en`` primary,
``es``, ``fr``) and two Markets: ``ca`` (playlovetoys.ca: en + fr) and ``usa``
(playlovetoys.com: en + es). The market is the domain, not part of the language,
so ``en-CA`` and ``en-US`` are both Shopify ``en``.

Wagtail keeps four market-language locales internally. At the Shopify boundary
only the language code is used.
"""

from __future__ import annotations

from .glossary_locale_utils import glossary_locale_code_for_wagtail

SHOPIFY_PRIMARY_LANGUAGE = 'en'
SHOPIFY_LANGUAGES = ('en', 'es', 'fr')

MARKET_BY_WAGTAIL_LOCALE: dict[str, str] = {
    'en-US': 'usa',
    'es-US': 'usa',
    'en-CA': 'ca',
    'fr-CA': 'ca',
}

COUNTRY_BY_MARKET: dict[str, str] = {
    'usa': 'United States',
    'ca': 'Canada',
}


def shopify_language(wagtail_code: str) -> str:
    """Shopify language code (``en``/``es``/``fr``) for a Wagtail locale code."""
    return glossary_locale_code_for_wagtail(wagtail_code)


def shopify_market(wagtail_code: str) -> str | None:
    """Shopify Market handle (``ca``/``usa``) for a Wagtail locale code."""
    return MARKET_BY_WAGTAIL_LOCALE.get(wagtail_code)


def shopify_country(wagtail_code: str) -> str | None:
    """Country name as Shopify spells it in region/location metaobjects."""
    market = shopify_market(wagtail_code)
    return COUNTRY_BY_MARKET.get(market) if market else None


def shopify_translation_language(wagtail_code: str) -> str | None:
    """
    Language to register through translationsRegister, or None.

    The primary language is the resource itself, not a translation. ``en-CA`` and
    ``en-US`` share the Shopify language ``en``, so ``en-CA`` is never a translation.
    """
    language = shopify_language(wagtail_code)
    if language == SHOPIFY_PRIMARY_LANGUAGE or language not in SHOPIFY_LANGUAGES:
        return None
    return language

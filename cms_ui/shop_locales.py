"""Fetch and cache Shopify store locales for the embedded CMS SPA."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from django.conf import settings
from django.utils import timezone

from core.shop_config_lookup import get_shop_config
from shopify_requests.graphql_service import execute_admin_graphql

from .locale_mapping import shopify_locale_to_wagtail, wagtail_locale_label

logger = logging.getLogger(__name__)

SHOP_LOCALES_QUERY = """
{
  shopLocales(published: true) {
    locale
    primary
    published
    name
  }
}
"""

CACHE_TTL = timedelta(minutes=15)


def fallback_spa_locales() -> dict[str, Any]:
    """Safe defaults when Shopify is unreachable or unconfigured."""
    primary = settings.LANGUAGE_CODE
    if primary not in settings.ALLOWED_LOCALE_CODES:
        primary = next(iter(settings.ALLOWED_LOCALE_CODES))
    languages = [
        {
            "code": code,
            "label": label,
            "primary": code == primary,
        }
        for code, label in settings.ALLOWED_LOCALE_CODES.items()
    ]
    return {
        "primaryLocale": primary,
        "availableLocales": languages,
        "source": "fallback",
    }


def _parse_shop_locales(data: dict | None) -> dict[str, Any]:
    rows = (data or {}).get("shopLocales") or []
    mapped: list[dict[str, Any]] = []
    primary_code: str | None = None

    for row in rows:
        if not row.get("published", True):
            continue
        wagtail_code = shopify_locale_to_wagtail(str(row.get("locale", "")))
        if not wagtail_code:
            continue
        is_primary = bool(row.get("primary"))
        entry = {
            "code": wagtail_code,
            "label": wagtail_locale_label(wagtail_code),
            "primary": is_primary,
            "shopifyLocale": row.get("locale"),
            "shopifyName": row.get("name"),
        }
        if not any(e["code"] == wagtail_code for e in mapped):
            mapped.append(entry)
        if is_primary:
            primary_code = wagtail_code

    if not mapped:
        return fallback_spa_locales()

    if primary_code is None:
        primary_code = mapped[0]["code"]
    for entry in mapped:
        entry["primary"] = entry["code"] == primary_code

    return {
        "primaryLocale": primary_code,
        "availableLocales": [
            {k: v for k, v in e.items() if k in ("code", "label", "primary")}
            for e in mapped
        ],
        "source": "shop",
    }


def _cache_fresh(config) -> bool:
    if not config or not config.spa_locales_fetched_at:
        return False
    return timezone.now() - config.spa_locales_fetched_at < CACHE_TTL


def _read_cache(config) -> dict[str, Any] | None:
    if not config or not config.cached_spa_locales:
        return None
    primary = config.cached_spa_primary_locale or settings.LANGUAGE_CODE
    return {
        "primaryLocale": primary,
        "availableLocales": config.cached_spa_locales,
        "source": "shop_cache",
    }


def _write_cache(config, payload: dict[str, Any]) -> None:
    if config is None:
        return
    config.cached_spa_locales = payload.get("availableLocales") or []
    config.cached_spa_primary_locale = payload.get("primaryLocale") or ""
    config.spa_locales_fetched_at = timezone.now()
    config.save(
        update_fields=[
            "cached_spa_locales",
            "cached_spa_primary_locale",
            "spa_locales_fetched_at",
        ]
    )


def fetch_shop_spa_locales(*, force_refresh: bool = False) -> dict[str, Any]:
    """
    Return ``primaryLocale``, ``availableLocales`` (SPA switcher), and ``source``.

    Uses ShopConfig cache with TTL; calls Admin GraphQL ``shopLocales`` on miss.
    """
    config = get_shop_config()
    if config and _cache_fresh(config) and not force_refresh:
        cached = _read_cache(config)
        if cached:
            return cached

    if not config or not config.access_token:
        return fallback_spa_locales()

    result = execute_admin_graphql(
        SHOP_LOCALES_QUERY,
        shop=config.shop,
    )
    if not result.ok or not result.data:
        logger.warning(
            "shopLocales fetch failed shop=%s code=%s detail=%s",
            config.shop,
            result.error_code,
            result.log_detail,
        )
        if config.cached_spa_locales:
            stale = _read_cache(config) or {}
            stale["source"] = "stale_cache"
            return stale
        return fallback_spa_locales()

    payload = _parse_shop_locales(result.data)
    _write_cache(config, payload)
    return payload


def codes_from_locale_payload(payload: dict[str, Any]) -> list[str]:
    return [row["code"] for row in payload.get("availableLocales") or []]

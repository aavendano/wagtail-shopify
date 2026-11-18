"""Resolve embedded CMS SPA UI language from store, session, and cookies."""

from __future__ import annotations

from django.conf import settings
from django.utils import translation

from .shop_locales import codes_from_locale_payload, fetch_shop_spa_locales

CMS_UI_LOCALE_COOKIE = "cms_ui_locale"
CMS_UI_LOCALE_STORAGE_KEY = "cms_ui_locale"


def resolve_spa_language(request) -> str:
    """
    Pick UI language: user cookie → Django language cookie → shop primary → fallback.
    """
    payload = fetch_shop_spa_locales()
    allowed = codes_from_locale_payload(payload)
    if not allowed:
        return settings.LANGUAGE_CODE

    preferred = request.COOKIES.get(CMS_UI_LOCALE_COOKIE)
    if preferred in allowed:
        return preferred

    primary = payload.get("primaryLocale")
    if primary in allowed:
        return primary

    django_cookie = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
    if django_cookie in allowed:
        return django_cookie

    django_lang = translation.get_language()
    if django_lang and django_lang in allowed:
        return django_lang

    return allowed[0]


def activate_request_language(request) -> str:
    """Activate Django translation for the SPA shell request."""
    code = resolve_spa_language(request)
    translation.activate(code)
    request.LANGUAGE_CODE = code
    return code

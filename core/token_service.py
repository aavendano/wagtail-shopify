from dataclasses import asdict, is_dataclass

from django.utils.dateparse import parse_datetime

from .models import ShopConfig
from .utils import _get_attr, get_shopify_app, log_shopify_result


TOKEN_ERROR_CODES = {"invalid_subject_token", "unauthorized", "invalid_client"}


def _to_dict(value):
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    if is_dataclass(value):
        return asdict(value)
    return {
        "access_mode": _get_attr(value, "access_mode"),
        "shop": _get_attr(value, "shop"),
        "token": _get_attr(value, "token"),
        "scope": _get_attr(value, "scope"),
        "expires": _get_attr(value, "expires"),
        "refresh_token": _get_attr(value, "refresh_token"),
        "refresh_token_expires": _get_attr(value, "refresh_token_expires"),
    }


def _parse_optional_datetime(value):
    if not value:
        return None
    if hasattr(value, "isoformat"):
        return value
    return parse_datetime(str(value))


def _clear_tokens(shop):
    ShopConfig.objects.filter(shop=shop).update(
        access_token=None,
        refresh_token=None,
        refresh_token_expires=None,
        expires=None,
        scope=None,
    )


def clear_shop_tokens(shop):
    _clear_tokens(shop)


def refresh_stored_token_if_possible(shopify_app, shop):
    record = ShopConfig.objects.filter(shop=shop).first()
    if not record:
        return None
    return _refresh_token_if_possible(shopify_app, record)


def persist_access_token(access_token, fallback_shop=None):
    payload = _to_dict(access_token)
    shop = payload.get("shop") or fallback_shop
    if not shop:
        return None

    is_online = payload.get("access_mode") == "online"
    defaults = {
        "is_online": is_online,
        "scope": payload.get("scope") or None,
        "expires": _parse_optional_datetime(payload.get("expires")),
        "access_token": payload.get("token") or None,
        "refresh_token": payload.get("refresh_token") or None,
        "refresh_token_expires": _parse_optional_datetime(
            payload.get("refresh_token_expires")
        ),
    }
    record, _ = ShopConfig.objects.update_or_create(shop=shop, defaults=defaults)
    return record


def _refresh_token_if_possible(shopify_app, record):
    if not record.refresh_token:
        return None

    access_mode = "online" if record.is_online else "offline"
    refresh_result = shopify_app.refresh_token_exchanged_access_token(
        {
            "shop": record.shop,
            "access_mode": access_mode,
            "token": record.access_token,
            "scope": record.scope,
            "expires": record.expires.isoformat().replace("+00:00", "Z")
            if record.expires
            else None,
            "refresh_token": record.refresh_token,
            "refresh_token_expires": record.refresh_token_expires.isoformat().replace(
                "+00:00", "Z"
            )
            if record.refresh_token_expires
            else None,
        }
    )
    log_shopify_result(refresh_result)
    if _get_attr(refresh_result, "ok", False):
        persist_access_token(_get_attr(refresh_result, "access_token"), fallback_shop=record.shop)
        return None

    if _get_attr(_get_attr(refresh_result, "log", {}), "code") in TOKEN_ERROR_CODES:
        _clear_tokens(record.shop)
    return refresh_result


def ensure_offline_token_lifecycle(verification_result, shopify_app=None):
    shop = _get_attr(verification_result, "shop")
    if not shop:
        return None

    shopify_app = shopify_app or get_shopify_app()
    token_record = ShopConfig.objects.filter(shop=shop).first()
    if token_record:
        refresh_result = _refresh_token_if_possible(shopify_app, token_record)
        if refresh_result is not None:
            return refresh_result
        if token_record.access_token:
            return None

    exchange_result = shopify_app.exchange_using_token_exchange(
        access_mode="offline",
        id_token=_get_attr(verification_result, "id_token"),
        invalid_token_response=_get_attr(verification_result, "new_id_token_response"),
    )
    log_shopify_result(exchange_result)
    if _get_attr(exchange_result, "ok", False):
        persist_access_token(
            _get_attr(exchange_result, "access_token"),
            fallback_shop=shop,
        )
        return None

    if _get_attr(_get_attr(exchange_result, "log", {}), "code") in TOKEN_ERROR_CODES:
        _clear_tokens(shop)
    return exchange_result

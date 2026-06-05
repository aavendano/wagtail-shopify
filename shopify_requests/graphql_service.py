from dataclasses import dataclass
from typing import Any, Optional

from django.conf import settings

from core.utils import _get_attr, get_shopify_app
from core.token_service import TOKEN_ERROR_CODES, clear_shop_tokens

from . import graphql_client
from .token_provider import resolve_access_token_for_admin


@dataclass
class AdminGraphqlResult:
    ok: bool
    shop: Optional[str]
    data: Optional[dict]
    extensions: Optional[dict]
    error_code: Optional[str]
    log_detail: str
    reauthorization_required: bool
    retryable: bool
    raw: Any


def _result_from_sdk(shop: str, sdk_result: Any) -> AdminGraphqlResult:
    ok = bool(_get_attr(sdk_result, "ok", False))
    log = _get_attr(sdk_result, "log", {}) or {}
    code = _get_attr(log, "code")
    detail = _get_attr(log, "detail", "") or ""
    data = _get_attr(sdk_result, "data")
    extensions = _get_attr(sdk_result, "extensions")
    reauth = (not ok) and (code in TOKEN_ERROR_CODES or code == "unauthorized")
    retryable = (not ok) and code == "throttled"
    return AdminGraphqlResult(
        ok=ok,
        shop=_get_attr(sdk_result, "shop", None) or shop,
        data=data if isinstance(data, dict) else None,
        extensions=extensions if isinstance(extensions, dict) else None,
        error_code=code,
        log_detail=str(detail),
        reauthorization_required=reauth and not ok,
        retryable=retryable and not ok,
        raw=sdk_result,
    )


def execute_admin_graphql(
    query,
    *,
    shop,
    api_version=None,
    variables=None,
    headers=None,
    max_retries=None,
    verification_result=None,
    invalid_token_response=None,
    shopify_app=None,
):
    """
    Load persisted offline access (with optional App Home verification context),
    then run Admin GraphQL. Maps SDK results to AdminGraphqlResult.
    """
    shopify_app = shopify_app or get_shopify_app()
    api_version = api_version or getattr(
        settings, "SHOPIFY_ADMIN_API_VERSION", "2025-04"
    )

    access_token, token_err = resolve_access_token_for_admin(
        shop, shopify_app=shopify_app, verification_result=verification_result
    )
    if token_err is not None:
        return _result_from_sdk(shop, token_err)

    if not access_token:
        return AdminGraphqlResult(
            ok=False,
            shop=shop,
            data=None,
            extensions=None,
            error_code="missing_access_token",
            log_detail="No persisted access token and no verification context to exchange.",
            reauthorization_required=True,
            retryable=False,
            raw=None,
        )

    raw = graphql_client.raw_admin_graphql(
        shopify_app,
        query,
        shop=shop,
        access_token=access_token,
        api_version=api_version,
        variables=variables,
        headers=headers,
        max_retries=max_retries,
        invalid_token_response=invalid_token_response,
    )
    out = _result_from_sdk(shop, raw)
    if not out.ok:
        err_code = out.error_code
        if err_code in TOKEN_ERROR_CODES or err_code == "unauthorized":
            clear_shop_tokens(shop)
    return out

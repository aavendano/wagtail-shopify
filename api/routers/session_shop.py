"""Session shop selector for CMS editors (deploy-per-shop tenancy)."""

from ninja import Router, Schema
from ninja.errors import HttpError

from api.auth import CmsEditorSessionAuth
from api.openapi_agent import agent_openapi_extra, capability_docstring
from shopify_config.membership import user_may_access_shop, user_shops
from shopify_config.tenancy import (
    SESSION_SHOP,
    ensure_session_shop,
    is_installed_shop,
    normalize_shop,
)

router = Router()


class SessionShopOut(Schema):
    shop: str
    shops: list[str]


class SessionShopSetIn(Schema):
    shop: str


class SessionShopSetOut(Schema):
    ok: bool
    shop: str


def _allowed_session_shops(request) -> list[str]:
    return [s for s in user_shops(request.user) if is_installed_shop(s)]


@router.get(
    "/",
    response=SessionShopOut,
    auth=CmsEditorSessionAuth(),
    operation_id="get_session_shop",
    summary="Get session shop and allowed shops",
    description=capability_docstring("get_session_shop"),
    openapi_extra=agent_openapi_extra("get_session_shop"),
)
def get_session_shop(request):
    # Soft membership path: list shops even before sole-shop seed completes.
    ensure_session_shop(request)
    shops = _allowed_session_shops(request)
    active = normalize_shop(request.session.get(SESSION_SHOP) or "")
    if active and active not in shops:
        active = ""
    if not active and len(shops) == 1:
        active = ensure_session_shop(request, shops[0])
    return SessionShopOut(shop=active or "", shops=shops)


@router.post(
    "/",
    response=SessionShopSetOut,
    auth=CmsEditorSessionAuth(),
    operation_id="set_session_shop",
    summary="Set session shop",
    description=capability_docstring("set_session_shop"),
    openapi_extra=agent_openapi_extra("set_session_shop"),
)
def set_session_shop_endpoint(request, payload: SessionShopSetIn):
    shop = normalize_shop(payload.shop)
    if not shop:
        raise HttpError(400, "shop is required")
    if not is_installed_shop(shop):
        raise HttpError(404, "shop is not installed")
    if not user_may_access_shop(request.user, shop):
        raise HttpError(403, "not allowed to select this shop")
    request.session[SESSION_SHOP] = shop
    return SessionShopSetOut(ok=True, shop=shop)

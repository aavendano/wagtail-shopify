from django.utils import timezone

from core.models import ShopConfig
from core.utils import get_shopify_app
from core.token_service import (
    ensure_offline_token_lifecycle,
    refresh_stored_token_if_possible,
)


def _record_needs_refresh(record):
    if not record or not record.refresh_token or not record.expires:
        return False
    return record.expires <= timezone.now()


def resolve_access_token_for_admin(shop, shopify_app=None, verification_result=None):
    """
    Return (access_token, None) on success, or (None, sdk_error_result) when token
    lifecycle fails, or (None, None) when there is no token and no exchange context.
    """
    shopify_app = shopify_app or get_shopify_app()
    record = ShopConfig.objects.filter(shop=shop).first()
    if record and record.access_token:
        if _record_needs_refresh(record):
            refresh_err = refresh_stored_token_if_possible(shopify_app, shop)
            if refresh_err is not None:
                return None, refresh_err
            record.refresh_from_db()
        if record.access_token:
            return record.access_token, None

    if verification_result is not None:
        lifecycle_err = ensure_offline_token_lifecycle(verification_result, shopify_app)
        if lifecycle_err is not None:
            return None, lifecycle_err
        record = ShopConfig.objects.filter(shop=shop).first()
        if record and record.access_token:
            return record.access_token, None

    return None, None

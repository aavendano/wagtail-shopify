from shopify_config.membership import delete_memberships_for_shop
from shopify_config.models import ShopConfig

from ..utils import shop_lookup_variants


def handle_app_uninstalled(shop: str, raw_body: bytes) -> None:
    del raw_body  # reserved for future idempotency / payload inspection
    if not shop:
        return
    delete_memberships_for_shop(shop)
    keys = shop_lookup_variants(shop)
    if keys:
        ShopConfig.objects.filter(shop__in=keys).delete()

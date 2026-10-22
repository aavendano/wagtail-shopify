from webhooks.utils import shop_lookup_variants


def get_shop_config(shop=None):
    """
    Resolve ShopConfig for a store.

    When *shop* is given, match both short subdomain and *.myshopify.com forms.
    Prefer a row that already has an access_token when multiple rows exist.

    When *shop* is omitted, resolve via :func:`resolve_sole_installed_shop`
    (exactly one installed ShopConfig). Returns None if zero or multiple shops.
    """
    from shopify_config.models import ShopConfig
    from shopify_config.tenancy import ShopUnresolvedError, resolve_sole_installed_shop

    if not shop:
        try:
            shop = resolve_sole_installed_shop()
        except ShopUnresolvedError:
            return None

    configs = []
    seen_ids = set()
    for variant in shop_lookup_variants(shop):
        for config in ShopConfig.objects.filter(shop=variant):
            if config.pk not in seen_ids:
                seen_ids.add(config.pk)
                configs.append(config)
    if not configs:
        return None
    for config in configs:
        if config.access_token:
            return config
    return configs[0]


def shop_has_access_token(shop=None) -> bool:
    config = get_shop_config(shop)
    return bool(config and config.access_token)

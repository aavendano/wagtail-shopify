from webhooks.utils import shop_lookup_variants


def get_shop_config(shop=None):
    """
    Resolve ShopConfig for a store.

    When *shop* is given, match both short subdomain and *.myshopify.com forms.
    Prefer a row that already has an access_token when multiple rows exist.
    """
    from .models import ShopConfig

    if shop:
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

    return (
        ShopConfig.objects.exclude(access_token__isnull=True)
        .exclude(access_token="")
        .order_by("-id")
        .first()
        or ShopConfig.objects.first()
    )


def shop_has_access_token(shop=None) -> bool:
    config = get_shop_config(shop)
    return bool(config and config.access_token)

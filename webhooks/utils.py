def shop_for_sdk_api(shop_domain_or_identifier: str) -> str:
    """
    Normalize a shop identifier for ShopifyApp HTTP calls.

    The SDK appends ``.myshopify.com`` internally; pass the short subdomain only
    (e.g. ``demo``), not ``demo.myshopify.com``.
    """
    s = (shop_domain_or_identifier or "").strip().lower()
    s = s.replace("https://", "").replace("http://", "").split("/")[0]
    if s.endswith(".myshopify.com"):
        return s[: -len(".myshopify.com")]
    return s


def shop_lookup_variants(shop_domain_or_identifier: str) -> list[str]:
    """
    Return possible values of ShopConfig.shop for the same store (short subdomain
    vs full *.myshopify.com), for filters and deletes after webhooks.
    """
    s = (shop_domain_or_identifier or "").strip().lower()
    if not s:
        return []
    s = s.replace("https://", "").replace("http://", "").split("/")[0]
    if s.endswith(".myshopify.com"):
        short = s[: -len(".myshopify.com")]
        return list({short, s})
    return list({s, f"{s}.myshopify.com"})

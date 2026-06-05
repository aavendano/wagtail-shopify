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

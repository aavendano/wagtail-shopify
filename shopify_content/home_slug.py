def home_page_handle(page) -> str:
    """
    Build canonical home metaobject handle: home-<locale>.

    Examples: home-en-us, home-es-us, home-en-ca, home-fr-ca.
    Locale source: shopify_locale override, else Wagtail page locale.
    """
    locale_code = (page.shopify_locale or page.locale.language_code or '').strip()
    locale_part = locale_code.lower().replace('_', '-')
    if not locale_part:
        return ''
    return f'home-{locale_part}'

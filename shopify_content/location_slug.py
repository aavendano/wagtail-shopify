from django.utils.text import slugify


def location_page_slug(page) -> str:
    """
    Build canonical location slug/handle: <locale>-<city>[-<state>].

    State is appended when set so homonymous US cities (e.g. Glendale AZ vs CA)
    do not collide under the same Wagtail parent.

    Examples: en-ca-montreal, en-us-glendale-arizona, en-us-columbus-georgia.
    Locale source: shopify_locale override, else Wagtail page locale.
    """
    locale_code = (page.shopify_locale or page.locale.language_code or '').strip()
    locale_part = locale_code.lower().replace('_', '-')
    city_part = slugify(page.city or '')
    state_part = slugify(page.state or '')
    if not locale_part or not city_part:
        return ''
    if state_part:
        return f'{locale_part}-{city_part}-{state_part}'
    return f'{locale_part}-{city_part}'

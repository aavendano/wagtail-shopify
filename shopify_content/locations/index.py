"""Build precomputed location index JSON for Shopify Page metafields."""

from __future__ import annotations

from datetime import datetime, timezone

from shopify_content.available_locales import ALLOWED_LOCALE_CODE_LIST
from shopify_content.index_builders import build_multi_locale_index
from shopify_content.location_slug import location_page_slug
from shopify_content.models import LocationPage, ShopifyRootPage

LOCATION_INDEX_VERSION = 1
LOCATION_ROOT_SLUG = 'local-us'
UNKNOWN_STATE_KEY = '#'


def location_page_path(handle: str) -> str:
    return f'/pages/location/{handle}'


def _location_locale_code(page: LocationPage) -> str:
    if page.shopify_locale:
        return page.shopify_locale
    return page.locale.language_code


def _state_key(page: LocationPage) -> str:
    state = (page.state or '').strip()
    return state if state else UNKNOWN_STATE_KEY


def _build_location_locale_listing(locale_code: str) -> dict:
    root = (
        ShopifyRootPage.objects.live()
        .filter(slug=LOCATION_ROOT_SLUG)
        .first()
    )
    if root is None:
        return {'count': 0, 'sections': []}

    pages = (
        LocationPage.objects.live()
        .descendant_of(root)
        .select_related('locale')
        .exclude(shopify_id='')
        .order_by('state', 'city', 'titulo')
    )

    buckets: dict[str, list[dict]] = {}
    for page in pages:
        if _location_locale_code(page) != locale_code:
            continue
        handle = (page.handle or location_page_slug(page) or page.slug or '').strip()
        if not handle:
            continue
        titulo = (page.titulo or page.title or '').strip()
        if not titulo:
            continue
        key = _state_key(page)
        buckets.setdefault(key, []).append({
            'titulo': titulo,
            'handle': handle,
            'path': location_page_path(handle),
            'city': (page.city or '').strip(),
            'state': (page.state or '').strip(),
        })

    section_keys = sorted(
        (key for key in buckets if key != UNKNOWN_STATE_KEY),
        key=str.casefold,
    )
    if UNKNOWN_STATE_KEY in buckets:
        section_keys.append(UNKNOWN_STATE_KEY)

    sections = []
    for key in section_keys:
        items = buckets.get(key)
        if items:
            sections.append({'key': key, 'items': items})

    count = sum(len(section['items']) for section in sections)
    return {'count': count, 'sections': sections}


def build_location_index_listings(*, generated_at: datetime | None = None) -> dict:
    """Build multi-locale location index payload for custom.index_listings."""
    return build_multi_locale_index(
        locale_codes=ALLOWED_LOCALE_CODE_LIST,
        build_locale_listing=_build_location_locale_listing,
        generated_at=generated_at,
    )


def build_location_index_json(locale_code: str, *, generated_at: datetime | None = None) -> dict:
    """
    Build grouped location index payload for one Wagtail locale code.

    Deprecated: prefer build_location_index_listings() for the single-page architecture.
    """
    when = generated_at or datetime.now(timezone.utc)
    listing = _build_location_locale_listing(locale_code)
    return {
        'version': LOCATION_INDEX_VERSION,
        'locale': locale_code,
        'generated_at': when.isoformat(),
        'count': listing['count'],
        'sections': listing['sections'],
    }

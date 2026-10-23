"""Build precomputed location index JSON for Shopify Page metafields.

Sections are the regions (province or state) the locations sit under; a location still hanging
off the root falls back to its ``state`` text, and one with neither goes to the ``#`` section.
Sections that come from a RegionPage also carry a ``region`` summary. Everything added since
version 1 is additive, so the version stays 1.
"""

from __future__ import annotations

from datetime import datetime, timezone

from wagtail.models import Page

from shopify_content.available_locales import ALLOWED_LOCALE_CODE_LIST
from shopify_content.index_builders import build_multi_locale_index
from shopify_content.location_slug import location_page_slug
from shopify_content.models import LocationPage, RegionPage, ShopifyRootPage
from shopify_content.storefront_urls import location_page_path, region_page_path

LOCATION_INDEX_VERSION = 1
LOCATION_ROOT_SLUG = 'local-us'
UNKNOWN_STATE_KEY = '#'


def _location_locale_code(page: LocationPage) -> str:
    if page.shopify_locale:
        return page.shopify_locale
    return page.locale.language_code


def _section_key(page: LocationPage, region: RegionPage | None) -> str:
    """The region name when the page sits under a region, else its state/province text."""
    if region is not None:
        return region.title.strip() or UNKNOWN_STATE_KEY
    state = (page.state or '').strip()
    return state if state else UNKNOWN_STATE_KEY


def _region_summary(region: RegionPage) -> dict:
    handle = (region.handle or region.slug or '').strip()
    return {
        'handle': handle,
        'code': region.region_code,
        'country': region.country,
        'path': region_page_path(handle, region.country),
    }


def _build_location_locale_listing(locale_code: str) -> dict:
    root = (
        ShopifyRootPage.objects.live()
        .filter(slug=LOCATION_ROOT_SLUG)
        .first()
    )
    if root is None:
        return {'count': 0, 'sections': []}

    # A page's parent path is its own path minus the last step: no query per page.
    regions_by_path = {
        region.path: region
        for region in RegionPage.objects.live().descendant_of(root)
    }

    pages = (
        LocationPage.objects.live()
        .descendant_of(root)
        .select_related('locale')
        .exclude(shopify_id='')
        .order_by('state', 'city', 'titulo')
    )

    buckets: dict[str, list[dict]] = {}
    section_regions: dict[str, RegionPage] = {}
    for page in pages:
        if _location_locale_code(page) != locale_code:
            continue
        handle = (page.handle or location_page_slug(page) or page.slug or '').strip()
        if not handle:
            continue
        titulo = (page.titulo or page.title or '').strip()
        if not titulo:
            continue
        region = regions_by_path.get(page.path[:-Page.steplen])
        key = _section_key(page, region)
        if region is not None:
            section_regions.setdefault(key, region)
        buckets.setdefault(key, []).append({
            'titulo': titulo,
            'handle': handle,
            'path': location_page_path(handle, page.country),
            'city': (page.city or '').strip(),
            'state': (page.state or '').strip(),
            'country': (page.country or '').strip(),
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
        if not items:
            continue
        # A section can merge pages whose state text differs, so order it here, not in the query.
        items.sort(key=lambda item: (item['city'].casefold(), item['titulo'].casefold()))
        section = {'key': key, 'items': items}
        if key in section_regions:
            section['region'] = _region_summary(section_regions[key])
        sections.append(section)

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
    """Build grouped location index payload for one Wagtail locale code."""
    when = generated_at or datetime.now(timezone.utc)
    listing = _build_location_locale_listing(locale_code)
    return {
        'version': LOCATION_INDEX_VERSION,
        'locale': locale_code,
        'generated_at': when.isoformat(),
        'count': listing['count'],
        'sections': listing['sections'],
    }

"""Build precomputed location index JSON for Shopify Page metafields."""

from __future__ import annotations

from datetime import datetime, timezone

from shopify_content.location_slug import location_page_slug
from shopify_content.models.location_page import LocationPage

LOCATION_INDEX_VERSION = 1
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


def build_location_index_json(locale_code: str, *, generated_at: datetime | None = None) -> dict:
    """
    Build grouped location index payload for a Wagtail/Shopify locale code.

    Only includes live locations with a non-empty shopify_id.
    Groups by state (or #), cities sorted alphabetically within each state.
    """
    when = generated_at or datetime.now(timezone.utc)
    pages = (
        LocationPage.objects.live()
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
            'label': titulo,
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
    return {
        'version': LOCATION_INDEX_VERSION,
        'locale': locale_code,
        'generated_at': when.isoformat(),
        'count': count,
        'sections': sections,
    }

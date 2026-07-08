"""Build precomputed glossary index JSON for Shopify Page metafields."""

from __future__ import annotations

from datetime import datetime, timezone

from django.utils.text import slugify

from shopify_content.available_locales import ALLOWED_LOCALE_CODE_LIST
from shopify_content.index_builders import build_multi_locale_index
from shopify_content.models import GlossaryTermPage, ShopifyRootPage

GLOSSARY_INDEX_VERSION = 1
GLOSSARY_ROOT_SLUG = 'glossary'
SECTION_ORDER = tuple(chr(code) for code in range(ord('A'), ord('Z') + 1)) + ('0-9', '#')


def glossary_term_path(handle: str) -> str:
    return f'/pages/glossary/{handle}'


def _section_key(term: str) -> str:
    stripped = (term or '').strip()
    if not stripped:
        return '#'
    first = stripped[0]
    if first.isalpha():
        return first.upper()
    if first.isdigit():
        return '0-9'
    return '#'


def _term_handle(page: GlossaryTermPage) -> str:
    return (page.handle or page.slug or slugify(page.term or '')).strip()


def _glossary_index_item(page: GlossaryTermPage, term: str, handle: str) -> dict:
    item = {
        'term': term,
        'handle': handle,
        'path': glossary_term_path(handle),
    }
    image_url = (getattr(page, 'image_url', '') or '').strip()
    if image_url:
        item['image_url'] = image_url
    image_alt = (getattr(page, 'image_alt_text', '') or '').strip()
    if image_alt:
        item['image_alt'] = image_alt
    return item


def _build_glossary_locale_listing(locale_code: str) -> dict:
    root = (
        ShopifyRootPage.objects.live()
        .filter(slug=GLOSSARY_ROOT_SLUG)
        .first()
    )
    if root is None:
        return {'count': 0, 'sections': []}

    pages = (
        GlossaryTermPage.objects.live()
        .descendant_of(root)
        .filter(locale__language_code=locale_code)
        .exclude(shopify_id='')
        .select_related('locale')
        .order_by('term')
    )

    buckets: dict[str, list[dict]] = {}
    for page in pages:
        term = (page.term or '').strip()
        if not term:
            continue
        handle = _term_handle(page)
        if not handle:
            continue
        key = _section_key(term)
        buckets.setdefault(key, []).append(_glossary_index_item(page, term, handle))

    sections = []
    for key in SECTION_ORDER:
        items = buckets.get(key)
        if items:
            sections.append({'key': key, 'items': items})

    count = sum(len(section['items']) for section in sections)
    return {'count': count, 'sections': sections}


def build_glossary_index_listings(*, generated_at: datetime | None = None) -> dict:
    """Build multi-locale glossary index payload for custom.index_listings."""
    return build_multi_locale_index(
        locale_codes=ALLOWED_LOCALE_CODE_LIST,
        build_locale_listing=_build_glossary_locale_listing,
        generated_at=generated_at,
    )


def build_glossary_index_json(locale_code: str, *, generated_at: datetime | None = None) -> dict:
    """
    Build grouped glossary index payload for one Wagtail locale code.

    Deprecated: prefer build_glossary_index_listings() for the single-page architecture.
    """
    when = generated_at or datetime.now(timezone.utc)
    listing = _build_glossary_locale_listing(locale_code)
    return {
        'version': GLOSSARY_INDEX_VERSION,
        'locale': locale_code,
        'generated_at': when.isoformat(),
        'count': listing['count'],
        'sections': listing['sections'],
    }

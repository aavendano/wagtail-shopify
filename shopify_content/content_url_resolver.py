"""Resolve GSC / storefront URLs to Wagtail content pages."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse

from shopify_content.models.content_url_index import ContentUrlIndex
from shopify_content.storefront_urls import KNOWN_LOCALE_PREFIXES


@dataclass(frozen=True)
class ContentUrlMatch:
    wagtail_page_id: int
    content_type: str
    title: str
    normalized_path: str
    locale_prefix: str | None
    match_quality: str  # exact | unmapped


def normalize_url(raw_url: str, *, property_url: str = '') -> tuple[str, str]:
    """
    Normalize a GSC or storefront URL to (normalized_path, locale_prefix).

    Strips domain, query string, fragment, and trailing slash. Detects Shopify
    Markets locale prefixes (/es-us/, /en-ca/, etc.).
    """
    url = (raw_url or '').strip()
    if not url:
        return '', ''

    if '://' in url or url.startswith('//'):
        parsed = urlparse(url if '://' in url else f'https:{url}')
        path = parsed.path or ''
    else:
        path = url.split('?', 1)[0].split('#', 1)[0]

    path = path.rstrip('/').lower() or '/'

    prop = (property_url or '').strip().rstrip('/').lower()
    if prop and path.startswith(prop):
        path = path[len(prop):] or '/'

    locale_prefix = ''
    for prefix in KNOWN_LOCALE_PREFIXES:
        prefix_with_slashes = f'/{prefix}'
        if path.startswith(f'{prefix_with_slashes}/'):
            locale_prefix = prefix
            path = path[len(prefix_with_slashes):]
            if not path.startswith('/'):
                path = f'/{path}' if path else '/'
            break
        if path == prefix_with_slashes:
            locale_prefix = prefix
            path = '/'
            break

    if not path.startswith('/'):
        path = f'/{path}'

    return path, locale_prefix


def resolve_url(raw_url: str, *, property_url: str = '') -> ContentUrlMatch | None:
    """
    Look up a storefront URL in ContentUrlIndex.

    Returns None when no indexed page matches (unmapped URL).
    """
    normalized_path, locale_prefix = normalize_url(raw_url, property_url=property_url)
    if not normalized_path or normalized_path == '/':
        return None

    entry = (
        ContentUrlIndex.objects.filter(
            normalized_path=normalized_path,
            locale_prefix=locale_prefix,
        )
        .select_related('wagtail_page')
        .first()
    )
    if entry is None and locale_prefix:
        entry = (
            ContentUrlIndex.objects.filter(
                normalized_path=normalized_path,
                locale_prefix='',
            )
            .select_related('wagtail_page')
            .first()
        )

    if entry is None:
        return None

    page = entry.wagtail_page.specific
    title = getattr(page, 'term', '') or page.title or ''

    return ContentUrlMatch(
        wagtail_page_id=entry.wagtail_page_id,
        content_type=entry.content_type,
        title=title,
        normalized_path=entry.normalized_path,
        locale_prefix=entry.locale_prefix or None,
        match_quality='exact',
    )

"""Serialize Wagtail pages to Shopify RelatedLinkSchema dicts."""

from typing import Any

from wagtail.models import Page

from shopify_content.models.blog import ArticlePage, BlogPage
from shopify_content.models.collection import CollectionPage
from shopify_content.models.glossary import GlossaryTermPage
from shopify_content.models.product import ProductPage

GLOSSARY_METAOBJECT_URL_HANDLE = 'glossary'

LINKABLE_PAGE_TYPES = (
    ProductPage,
    CollectionPage,
    ArticlePage,
    GlossaryTermPage,
)


def page_to_related_link(page: Page) -> dict[str, Any] | None:
    """Map a Wagtail page to a RelatedLinkSchema-compatible dict."""
    specific = page.specific

    if isinstance(specific, ProductPage):
        handle = specific.handle or specific.slug
        if not handle:
            return None
        return {
            'type': 'product',
            'handle': handle,
            'label': specific.title,
        }

    if isinstance(specific, CollectionPage):
        handle = specific.handle or specific.slug
        if not handle:
            return None
        return {
            'type': 'collection',
            'handle': handle,
            'label': specific.title,
        }

    if isinstance(specific, ArticlePage):
        handle = specific.handle or specific.slug
        if not handle:
            return None
        try:
            parent = specific.get_parent().specific
        except Exception:
            return None
        if not isinstance(parent, BlogPage) or not parent.handle:
            return None
        return {
            'type': 'article',
            'handle': handle,
            'label': specific.title,
            'blog_handle': parent.handle,
        }

    if isinstance(specific, GlossaryTermPage):
        handle = specific.handle or specific.slug
        if not handle:
            return None
        return {
            'type': 'metaobject',
            'handle': handle,
            'label': specific.term or specific.title,
            'url_handle': GLOSSARY_METAOBJECT_URL_HANDLE,
        }

    return None


def related_link_url(link: dict[str, Any]) -> str:
    """Build a storefront-relative URL from a serialized link."""
    link_type = link.get('type')
    handle = link.get('handle', '')
    if link_type == 'product':
        return f'/products/{handle}'
    if link_type == 'collection':
        return f'/collections/{handle}'
    if link_type == 'article':
        blog_handle = link.get('blog_handle', '')
        return f'/blogs/{blog_handle}/{handle}'
    if link_type == 'metaobject':
        url_handle = link.get('url_handle', GLOSSARY_METAOBJECT_URL_HANDLE)
        return f'/pages/{url_handle}/{handle}'
    if link_type == 'blog':
        return f'/blogs/{handle}'
    return f'/{handle}'


def serialize_semantic_links(source_page) -> list[dict[str, Any]]:
    """Read semantic_links FK rows and serialize to RelatedLinkSchema dicts."""
    if not hasattr(source_page, 'semantic_links'):
        return []

    links = []
    seen_handles: set[tuple[str, str, str | None]] = set()

    for row in source_page.semantic_links.select_related('related_page').order_by('sort_order'):
        related = row.related_page
        if related is None:
            continue
        try:
            related = related.specific
        except Exception:
            continue

        link = page_to_related_link(related)
        if link is None:
            continue

        dedupe_key = (
            link['type'],
            link['handle'],
            link.get('blog_handle') or link.get('url_handle'),
        )
        if dedupe_key in seen_handles:
            continue
        seen_handles.add(dedupe_key)
        links.append(link)

    return links


def serialize_semantic_links_with_urls(source_page) -> list[dict[str, Any]]:
    """Serialize links and attach storefront URL + Wagtail full URL when available."""
    result = []
    for link in serialize_semantic_links(source_page):
        enriched = dict(link)
        enriched['url'] = related_link_url(link)
        result.append(enriched)
    return result

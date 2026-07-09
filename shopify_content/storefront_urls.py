"""Canonical Shopify storefront path helpers for Wagtail content pages."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from django.utils.text import slugify
from wagtail.models import Page

GLOSSARY_METAOBJECT_URL_HANDLE = 'glossary'
LOCATION_METAOBJECT_URL_HANDLE = 'location'

# Shopify Markets locale path prefixes (aligned with bigquery_gsc scoring).
KNOWN_LOCALE_PREFIXES: tuple[str, ...] = (
    'es-us',
    'en-us',
    'fr',
    'en-ca',
    'fr-ca',
)

LOCALE_CODE_TO_PREFIX: dict[str, str] = {
    'en-US': 'en-us',
    'es-US': 'es-us',
    'en-CA': 'en-ca',
    'fr-CA': 'fr-ca',
}

ROOT_SLUG_TO_INDEX_PATH: dict[str, str] = {
    'glossary': '/pages/glossary',
    'local-us': '/pages/locations',
    'blogs': '/pages/blogs',
}


def product_path(handle: str) -> str:
    return f'/products/{handle}'


def collection_path(handle: str) -> str:
    return f'/collections/{handle}'


def blog_path(handle: str) -> str:
    return f'/blogs/{handle}'


def article_path(blog_handle: str, article_handle: str) -> str:
    return f'/blogs/{blog_handle}/{article_handle}'


def glossary_term_path(handle: str) -> str:
    return f'/pages/{GLOSSARY_METAOBJECT_URL_HANDLE}/{handle}'


def location_page_path(handle: str) -> str:
    return f'/pages/{LOCATION_METAOBJECT_URL_HANDLE}/{handle}'


def home_page_path(handle: str) -> str:
    return f'/pages/{handle}'


def metaobject_page_path(url_handle: str, handle: str) -> str:
    return f'/pages/{url_handle}/{handle}'


def root_index_path(slug: str) -> str | None:
    return ROOT_SLUG_TO_INDEX_PATH.get(slug)


def related_link_path(link: dict[str, Any]) -> str:
    """Build a storefront-relative URL from a serialized related link dict."""
    link_type = link.get('type')
    handle = link.get('handle', '')
    if link_type == 'product':
        return product_path(handle)
    if link_type == 'collection':
        return collection_path(handle)
    if link_type == 'article':
        return article_path(link.get('blog_handle', ''), handle)
    if link_type == 'metaobject':
        url_handle = link.get('url_handle', GLOSSARY_METAOBJECT_URL_HANDLE)
        return metaobject_page_path(url_handle, handle)
    if link_type == 'blog':
        return blog_path(handle)
    return f'/{handle}'


def _page_handle(page) -> str:
    return (getattr(page, 'handle', '') or page.slug or '').strip()


def page_content_type_key(page) -> str | None:
    """Return a stable content type key for ContentUrlIndex rows."""
    from shopify_content.models.blog import ArticlePage, BlogPage
    from shopify_content.models.collection import CollectionPage
    from shopify_content.models.glossary import GlossaryTermPage
    from shopify_content.models.home_page import HomePage
    from shopify_content.models.location_page import LocationPage
    from shopify_content.models.product import ProductPage
    from shopify_content.models.root import ShopifyRootPage

    specific = page.specific if isinstance(page, Page) else page

    if isinstance(specific, ProductPage):
        return 'product'
    if isinstance(specific, CollectionPage):
        return 'collection'
    if isinstance(specific, BlogPage):
        return 'blog'
    if isinstance(specific, ArticlePage):
        return 'article'
    if isinstance(specific, GlossaryTermPage):
        return 'glossary_term'
    if isinstance(specific, LocationPage):
        return 'location'
    if isinstance(specific, HomePage):
        return 'home'
    if isinstance(specific, ShopifyRootPage):
        if specific.slug in ROOT_SLUG_TO_INDEX_PATH:
            return 'index'
        return 'root'
    return None


def _article_blog_handle(page) -> str:
    from shopify_content.models.blog import ArticlePage, BlogPage

    if not isinstance(page, ArticlePage):
        return ''
    parent = page.get_parent()
    if parent is None:
        return ''
    blog = parent.specific
    if not isinstance(blog, BlogPage):
        return ''
    return (blog.handle or blog.slug or '').strip()


def _location_handle(page) -> str:
    from shopify_content.location_slug import location_page_slug

    return (page.handle or location_page_slug(page) or page.slug or '').strip()


def _home_handle(page) -> str:
    from shopify_content.home_slug import home_page_handle

    return (page.handle or home_page_handle(page) or page.slug or '').strip()


def storefront_path_for_page(page) -> str | None:
    """Return the canonical storefront-relative path for a Wagtail page."""
    from shopify_content.models.blog import ArticlePage, BlogPage
    from shopify_content.models.collection import CollectionPage
    from shopify_content.models.glossary import GlossaryTermPage
    from shopify_content.models.home_page import HomePage
    from shopify_content.models.location_page import LocationPage
    from shopify_content.models.product import ProductPage
    from shopify_content.models.root import ShopifyRootPage

    specific = page.specific if isinstance(page, Page) else page

    if isinstance(specific, ProductPage):
        handle = _page_handle(specific)
        return product_path(handle) if handle else None

    if isinstance(specific, CollectionPage):
        handle = _page_handle(specific)
        return collection_path(handle) if handle else None

    if isinstance(specific, BlogPage):
        handle = _page_handle(specific)
        return blog_path(handle) if handle else None

    if isinstance(specific, ArticlePage):
        article_handle = _page_handle(specific)
        blog_handle = _article_blog_handle(specific)
        if article_handle and blog_handle:
            return article_path(blog_handle, article_handle)
        return None

    if isinstance(specific, GlossaryTermPage):
        handle = _page_handle(specific) or slugify(specific.term or '')
        return glossary_term_path(handle) if handle else None

    if isinstance(specific, LocationPage):
        handle = _location_handle(specific)
        return location_page_path(handle) if handle else None

    if isinstance(specific, HomePage):
        handle = _home_handle(specific)
        return home_page_path(handle) if handle else None

    if isinstance(specific, ShopifyRootPage):
        return root_index_path(specific.slug)

    return None


def locale_prefix_for_page(page) -> str:
    """Return the Markets URL prefix for the page locale, or empty string."""
    specific = page.specific if isinstance(page, Page) else page
    locale_code = ''
    if hasattr(specific, 'locale') and specific.locale_id:
        locale_code = specific.locale.language_code
    return LOCALE_CODE_TO_PREFIX.get(locale_code, '')


def page_index_metadata(page) -> tuple[str, str, str]:
    """
    Return (content_type, handle, blog_handle) for ContentUrlIndex rows.
    blog_handle is empty except for articles.
    """
    specific = page.specific if isinstance(page, Page) else page
    content_type = page_content_type_key(specific) or ''
    handle = _page_handle(specific)
    blog_handle = ''

    from shopify_content.models.blog import ArticlePage
    from shopify_content.models.glossary import GlossaryTermPage
    from shopify_content.models.home_page import HomePage
    from shopify_content.models.location_page import LocationPage
    from shopify_content.models.root import ShopifyRootPage

    if isinstance(specific, ArticlePage):
        blog_handle = _article_blog_handle(specific)
    elif isinstance(specific, GlossaryTermPage):
        handle = handle or slugify(specific.term or '')
    elif isinstance(specific, LocationPage):
        handle = _location_handle(specific)
    elif isinstance(specific, HomePage):
        handle = _home_handle(specific)
    elif isinstance(specific, ShopifyRootPage):
        handle = specific.slug

    return content_type, handle, blog_handle


@dataclass(frozen=True)
class PathVariant:
    normalized_path: str
    locale_prefix: str
    is_canonical: bool


def path_variants_for_index(page) -> list[PathVariant]:
    """
    Return normalized path variants for ContentUrlIndex (canonical + locale prefix).
    """
    canonical = storefront_path_for_page(page)
    if not canonical:
        return []

    canonical = canonical.rstrip('/').lower() or canonical
    variants = [PathVariant(normalized_path=canonical, locale_prefix='', is_canonical=True)]

    prefix = locale_prefix_for_page(page)
    if prefix:
        variants.append(
            PathVariant(normalized_path=canonical, locale_prefix=prefix, is_canonical=False)
        )

    return variants


def all_paths_for_page(page) -> list[str]:
    """Return full relative storefront paths (canonical + locale-prefixed)."""
    variants = path_variants_for_index(page)
    paths: list[str] = []
    for variant in variants:
        if variant.locale_prefix:
            paths.append(f'/{variant.locale_prefix}{variant.normalized_path}')
        else:
            paths.append(variant.normalized_path)
    return paths

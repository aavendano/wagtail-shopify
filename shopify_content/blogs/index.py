"""Build precomputed blog index listings JSON for Shopify Page metafields."""

from __future__ import annotations

from datetime import datetime, timezone

from shopify_content.available_locales import ALLOWED_LOCALE_CODE_LIST
from shopify_content.models import ArticlePage, BlogPage, ShopifyRootPage

BLOG_INDEX_LISTINGS_VERSION = 1
BLOGS_ROOT_SLUG = 'blogs'


def article_path(blog_handle: str, article_handle: str) -> str:
    return f'/blogs/{blog_handle}/{article_handle}'


def _article_handle(page: ArticlePage) -> str:
    return (page.handle or page.slug or '').strip()


def _blog_handle(page: ArticlePage) -> str:
    parent = page.get_parent()
    if parent is None:
        return ''
    blog = parent.specific
    if not isinstance(blog, BlogPage):
        return ''
    return (blog.handle or blog.slug or '').strip()


def _build_locale_listing(locale_code: str) -> dict:
    root = (
        ShopifyRootPage.objects.live()
        .filter(slug=BLOGS_ROOT_SLUG)
        .first()
    )
    if root is None:
        return {'count': 0, 'sections': []}

    articles = (
        ArticlePage.objects.live()
        .descendant_of(root)
        .filter(locale__language_code=locale_code)
        .exclude(shopify_id='')
        .select_related('locale')
        .order_by('-published_at', 'title')
    )

    buckets: dict[str, dict] = {}
    for article in articles:
        blog_handle = _blog_handle(article)
        article_handle = _article_handle(article)
        if not blog_handle or not article_handle:
            continue

        parent = article.get_parent().specific
        label = parent.title if isinstance(parent, BlogPage) else blog_handle

        bucket = buckets.setdefault(
            blog_handle,
            {'key': blog_handle, 'label': label, 'items': []},
        )
        published_at = article.published_at
        bucket['items'].append({
            'title': article.title,
            'handle': article_handle,
            'blog_handle': blog_handle,
            'path': article_path(blog_handle, article_handle),
            'published_at': published_at.isoformat() if published_at else None,
        })

    sections = sorted(buckets.values(), key=lambda section: section['label'].lower())
    count = sum(len(section['items']) for section in sections)
    return {'count': count, 'sections': sections}


def build_blog_index_listings(*, generated_at: datetime | None = None) -> dict:
    """
    Build multi-locale blog index payload for custom.index_listings.

    Only includes live ArticlePage rows with a non-empty shopify_id under root blogs.
    """
    when = generated_at or datetime.now(timezone.utc)
    locales_payload = {
        locale_code: _build_locale_listing(locale_code)
        for locale_code in ALLOWED_LOCALE_CODE_LIST
    }
    return {
        'version': BLOG_INDEX_LISTINGS_VERSION,
        'generated_at': when.isoformat(),
        'locales': locales_payload,
    }

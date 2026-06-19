"""
Inbound sync: fetch Shopify content and create/update Wagtail pages.

Called from management commands (no HTTP request context).
Token resolution relies on ShopConfig having a valid offline access_token.

Import strategy:
  - Existing pages (matched by shopify_id) are updated in place.
  - New pages are created as children of the specified parent page.
  - On import, body HTML is stored as a single HtmlBlock. Editors can later
    break it into structured blocks.
  - Metafields are not imported on pull (manual/API/outbound only).
  - Images are stored as absolute URLs in the local DB (no wagtailimages download).
"""

import logging
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from wagtail.models import Page, Locale

from shopify_requests.graphql_service import execute_admin_graphql
from .queries import (
    LIST_PRODUCTS,
    LIST_COLLECTIONS,
    LIST_BLOGS,
    LIST_ARTICLES_FOR_BLOG,
)
from ..models import (
    ProductPage, ProductPageImage,
    CollectionPage,
    BlogPage,
    ArticlePage,
)
from .import_parents import ensure_child_of_import_parent
from .utils import absolute_shopify_media_url, MAX_PRODUCT_IMAGES

logger = logging.getLogger(__name__)

PAGE_SIZE = 100


def _get_shop():
    from core.models import ShopConfig
    config = ShopConfig.objects.first()
    if not config:
        raise RuntimeError('No ShopConfig found. Install the app on Shopify first.')
    return config.shop


def _paginate(shop, query, data_path, variables=None):
    """
    Generator yielding node dicts from a cursor-paginated Shopify query.
    data_path: dot-separated keys to drill into result.data, e.g. 'blog.articles'.
    """
    cursor = None
    while True:
        vars_ = {'first': PAGE_SIZE, 'after': cursor, **(variables or {})}
        result = execute_admin_graphql(query, shop=shop, variables=vars_)
        if not result.ok or not result.data:
            logger.error(
                'Paginated query failed shop=%s path=%s error=%s',
                shop, data_path, result.error_code,
            )
            break

        data = result.data
        for key in data_path.split('.'):
            data = (data or {}).get(key, {})

        edges = (data or {}).get('edges', [])
        page_info = (data or {}).get('pageInfo', {})

        for edge in edges:
            yield edge.get('node', {})

        if not page_info.get('hasNextPage'):
            break
        cursor = page_info.get('endCursor')


def _empty_import_stats():
    return {'created': 0, 'updated': 0, 'skipped': 0, 'errors': 0}


def _get_or_create_page(model_class, shopify_id, shop):
    """
    Look up an existing page by shopify_id, or return a new unsaved instance.
    Returns (page_instance, is_new_bool).
    """
    locale = Locale.get_default()
    existing = (
        model_class.objects
        .filter(shopify_id=shopify_id, locale=locale)
        .first()
    )
    if existing:
        return existing, False
    new_page = model_class(locale=locale)
    new_page.shopify_id = shopify_id
    return new_page, True


def _sync_product_images(page, node):
    """Replace product image URLs from Shopify (max MAX_PRODUCT_IMAGES)."""
    edges = (node.get('images') or {}).get('edges', [])[:MAX_PRODUCT_IMAGES]
    page.shopify_images.all().delete()
    for sort_order, edge in enumerate(edges):
        img = edge.get('node') or {}
        url = absolute_shopify_media_url(img.get('url') or '')
        if not url:
            continue
        ProductPageImage.objects.create(
            page=page,
            shopify_id=img.get('id') or '',
            url=url,
            alt_text=img.get('altText') or '',
            sort_order=sort_order,
        )


def _set_collection_image(page, node):
    """Set collection featured image URL fields from Shopify."""
    image = node.get('image') or {}
    url = absolute_shopify_media_url(image.get('url') or '')
    page.image_url = url
    page.image_alt_text = image.get('altText') or ''
    page.shopify_image_id = image.get('id') or ''


def _set_article_featured_image_url(page, node):
    """Set article featured image URL fields from Shopify."""
    image = node.get('image') or {}
    url = absolute_shopify_media_url(image.get('url') or '')
    page.featured_image_url = url
    page.featured_image_alt = image.get('altText') or ''
    page.shopify_featured_image_id = image.get('id') or ''


# ---------------------------------------------------------------------------
# Public import functions — called from management commands
# ---------------------------------------------------------------------------

def import_products(shop, parent_page, new_only=False):
    """
    Fetch all Shopify Products and create/update ProductPage instances
    as children of parent_page.

    When new_only is True, existing pages (matched by shopify_id) are skipped.
    """
    stats = _empty_import_stats()

    for node in _paginate(shop, LIST_PRODUCTS, 'products'):
        try:
            gid = node['id']
            page, is_new = _get_or_create_page(ProductPage, gid, shop)

            if not is_new and new_only:
                stats['skipped'] += 1
                continue

            page.title = node.get('title', '')
            page.slug = node.get('handle', gid.rsplit('/', 1)[-1])
            page.handle = node.get('handle', '')
            page.vendor = node.get('vendor', '')
            page.product_type = node.get('productType', '')
            page.status = node.get('status', 'ACTIVE')

            seo = node.get('seo') or {}
            page.seo_title = seo.get('title') or ''
            page.search_description = seo.get('description') or ''

            desc_html = node.get('descriptionHtml') or ''
            if desc_html:
                page.body = [{'type': 'html', 'value': desc_html}]

            tags = node.get('tags') or []

            if is_new:
                parent_page.add_child(instance=page)
            else:
                page.save_revision().publish()

            if tags:
                page.tags.set(tags)

            _sync_product_images(page, node)

            type(page).objects.filter(pk=page.pk).update(last_synced_at=timezone.now())
            stats['created' if is_new else 'updated'] += 1

        except Exception as exc:
            logger.exception('Error importing product gid=%s: %s', node.get('id'), exc)
            stats['errors'] += 1

    return stats


def import_collections(shop, parent_page, new_only=False):
    """
    Fetch all Shopify Collections and create/update CollectionPage instances.

    When new_only is True, existing pages (matched by shopify_id) are skipped.
    """
    stats = _empty_import_stats()

    for node in _paginate(shop, LIST_COLLECTIONS, 'collections'):
        try:
            gid = node['id']
            page, is_new = _get_or_create_page(CollectionPage, gid, shop)

            if not is_new and new_only:
                stats['skipped'] += 1
                continue

            page.title = node.get('title', '')
            page.slug = node.get('handle', gid.rsplit('/', 1)[-1])
            page.handle = node.get('handle', '')
            page.sort_order = node.get('sortOrder', 'MANUAL')

            seo = node.get('seo') or {}
            page.seo_title = seo.get('title') or ''
            page.search_description = seo.get('description') or ''

            desc_html = node.get('descriptionHtml') or ''
            if desc_html:
                page.description = [{'type': 'html', 'value': desc_html}]

            _set_collection_image(page, node)

            if is_new:
                parent_page.add_child(instance=page)
            else:
                ensure_child_of_import_parent(page, parent_page)
                page.save_revision().publish()

            type(page).objects.filter(pk=page.pk).update(last_synced_at=timezone.now())
            stats['created' if is_new else 'updated'] += 1

        except Exception as exc:
            logger.exception('Error importing collection gid=%s: %s', node.get('id'), exc)
            stats['errors'] += 1

    return stats


def import_blogs_and_articles(shop, parent_page, new_only=False):
    """
    Fetch all Shopify Blogs and their Articles.
    Blogs become BlogPage instances; articles become ArticlePage children.
    Run this before import_products/import_collections if you want
    a clean page tree.

    When new_only is True, existing blogs and articles are not updated;
    new articles under existing blogs are still imported.
    """
    blog_stats = _empty_import_stats()
    article_stats = _empty_import_stats()

    for blog_node in _paginate(shop, LIST_BLOGS, 'blogs'):
        try:
            gid = blog_node['id']
            blog_page, is_new = _get_or_create_page(BlogPage, gid, shop)

            if is_new:
                blog_page.title = blog_node.get('title', '')
                blog_page.slug = blog_node.get('handle', gid.rsplit('/', 1)[-1])
                blog_page.handle = blog_node.get('handle', '')
                blog_page.comment_policy = blog_node.get('commentPolicy', 'CLOSED')
                parent_page.add_child(instance=blog_page)
                type(blog_page).objects.filter(pk=blog_page.pk).update(last_synced_at=timezone.now())
                blog_stats['created'] += 1
            elif new_only:
                blog_stats['skipped'] += 1
            else:
                blog_page.title = blog_node.get('title', '')
                blog_page.slug = blog_node.get('handle', gid.rsplit('/', 1)[-1])
                blog_page.handle = blog_node.get('handle', '')
                blog_page.comment_policy = blog_node.get('commentPolicy', 'CLOSED')
                ensure_child_of_import_parent(blog_page, parent_page)
                blog_page.save_revision().publish()
                type(blog_page).objects.filter(pk=blog_page.pk).update(last_synced_at=timezone.now())
                blog_stats['updated'] += 1

            # Import articles for this blog
            for art_node in _paginate(
                shop,
                LIST_ARTICLES_FOR_BLOG,
                'blog.articles',
                variables={'blogId': gid},
            ):
                try:
                    art_gid = art_node['id']
                    art_page, art_is_new = _get_or_create_page(ArticlePage, art_gid, shop)

                    if not art_is_new and new_only:
                        article_stats['skipped'] += 1
                        continue

                    art_page.title = art_node.get('title', '')
                    art_page.slug = art_node.get('handle', art_gid.rsplit('/', 1)[-1])
                    art_page.handle = art_node.get('handle', '')
                    art_page.author = (art_node.get('author') or {}).get('name', '')

                    published_str = art_node.get('publishedAt')
                    art_page.published_at = parse_datetime(published_str) if published_str else None

                    art_page.summary = art_node.get('summary') or ''
                    tags = art_node.get('tags') or []

                    body_html = art_node.get('body') or ''
                    if body_html:
                        art_page.body = [{'type': 'html', 'value': body_html}]

                    _set_article_featured_image_url(art_page, art_node)

                    if art_is_new:
                        blog_page.add_child(instance=art_page)
                    else:
                        ensure_child_of_import_parent(art_page, blog_page)
                        art_page.save_revision().publish()

                    if tags:
                        art_page.tags.set(tags)

                    type(art_page).objects.filter(pk=art_page.pk).update(last_synced_at=timezone.now())
                    article_stats['created' if art_is_new else 'updated'] += 1

                except Exception as exc:
                    logger.exception('Error importing article gid=%s: %s', art_node.get('id'), exc)
                    article_stats['errors'] += 1

        except Exception as exc:
            logger.exception('Error importing blog gid=%s: %s', blog_node.get('id'), exc)
            blog_stats['errors'] += 1

    return {'blogs': blog_stats, 'articles': article_stats}

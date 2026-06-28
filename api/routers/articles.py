import json
from typing import List, Optional

from ninja import Router
from django.utils.text import slugify
from django.shortcuts import get_object_or_404

from shopify_content.models import BlogPage, ArticlePage
from shopify_content.models.blog import ArticlePageMetafield
from shopify_content.sync.outbound import sync_article_page
from ..sync import execute_pull
from ..schemas.article import ArticleIn, ArticlePatch, ArticleOut
from ..schemas.common import SyncResultSchema, ImportResultSchema, ErrorSchema
from ..openapi_agent import agent_openapi_extra, capability_docstring
from ..locale_utils import (
    resolve_locale,
    apply_translation_link,
    inherit_shopify_id_from_source,
    filter_queryset_by_locale,
)

router = Router()


@router.get(
    '/',
    response=List[ArticleOut],
    summary="List Articles",
    operation_id="list_articles",
    description=capability_docstring("list_articles"),
    openapi_extra=agent_openapi_extra("list_articles"),
)
def list_articles(
    request,
    live_only: bool = False,
    locale: Optional[str] = None,
    blog_id: Optional[int] = None,
    limit: int = 50,
    offset: int = 0,
    # Enhanced filters
    live: Optional[bool] = None,
    updated_after: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    ordering: Optional[str] = None,
):
    """Discover articles; filter by blog_id, tag, locale, live, updated_after, or search."""
    from django.db.models import Q
    from django.utils.dateparse import parse_datetime

    qs = (
        ArticlePage.objects
        .select_related('locale', 'featured_image')
        .prefetch_related('metafields', 'tagged_items__tag')
    )
    # Legacy param: live_only
    if live_only:
        qs = qs.live()
    # New param: live (overrides live_only if explicitly set)
    if live is not None:
        qs = qs.live() if live else qs.filter(live=False)
    qs = filter_queryset_by_locale(qs, locale)
    if blog_id:
        qs = qs.child_of(BlogPage.objects.filter(pk=blog_id).first() or BlogPage())
    if updated_after:
        dt = parse_datetime(updated_after)
        if dt:
            qs = qs.filter(last_published_at__gt=dt)
    if tag:
        qs = qs.filter(tagged_items__tag__name=tag)
    if search:
        qs = qs.filter(title__icontains=search)
    if ordering:
        valid = {'title', '-title', 'last_published_at', '-last_published_at',
                 'first_published_at', '-first_published_at'}
        if ordering in valid:
            qs = qs.order_by(ordering)
    return list(qs[offset:offset + limit])


@router.post(
    '/',
    response={201: ArticleOut, 400: ErrorSchema},
    summary="Create Article",
    operation_id="create_article",
    description=capability_docstring("create_article"),
    openapi_extra=agent_openapi_extra("create_article"),
)
def create_article(request, data: ArticleIn):
    """Create article under parent BlogPage."""
    blog_page = get_object_or_404(BlogPage, pk=data.blog_id)

    slug = slugify(data.handle or data.title)

    page = ArticlePage(
        title=data.title,
        slug=slug,
        locale=resolve_locale(data.locale),
        shopify_id=data.shopify_id or '',
        handle=data.handle or slug,
        author=data.author or '',
        published_at=data.published_at,
        summary=data.summary or '',
        sync_enabled=data.sync_enabled if data.sync_enabled is not None else True,
        seo_title=data.seo_title or '',
        search_description=data.search_description or '',
    )

    if data.featured_image_id:
        page.featured_image_id = data.featured_image_id

    if data.body:
        page.body = json.dumps(data.body)

    source = apply_translation_link(page, data.translation_of, ArticlePage)
    inherit_shopify_id_from_source(page, source)

    blog_page.add_child(instance=page)

    if data.tags:
        page.tags.set(data.tags)

    if data.metafields:
        for mf in data.metafields:
            ArticlePageMetafield.objects.create(
                page=page,
                namespace=mf.namespace,
                key=mf.key,
                type=mf.type,
                value=mf.value,
            )

    page.refresh_from_db()
    return 201, page


@router.post(
    '/pull',
    response={200: ImportResultSchema, 400: ErrorSchema},
    summary="Pull Articles from Shopify (sync)",
    operation_id="pull_articles_sync",
    description=capability_docstring("pull_articles_sync"),
    openapi_extra=agent_openapi_extra("pull_articles_sync"),
)
def pull_articles(request):
    """Alias for blogs pull — imports blogs and articles together."""
    return execute_pull('blogs')


@router.get(
    '/{page_id}',
    response={200: ArticleOut, 404: ErrorSchema},
    summary="Get Article",
    operation_id="get_article",
    description=capability_docstring("get_article"),
    openapi_extra=agent_openapi_extra("get_article"),
)
def get_article(request, page_id: int):
    """Get single article by Wagtail page ID."""
    try:
        page = (
            ArticlePage.objects
            .select_related('locale', 'featured_image')
            .prefetch_related('metafields', 'tagged_items__tag')
            .get(pk=page_id)
        )
        return page
    except ArticlePage.DoesNotExist:
        return 404, {"detail": f"Article page {page_id} not found."}


@router.patch(
    '/{page_id}',
    response={200: ArticleOut, 404: ErrorSchema, 400: ErrorSchema},
    summary="Update Article",
    operation_id="update_article",
    description=capability_docstring("update_article"),
    openapi_extra=agent_openapi_extra("update_article"),
)
def update_article(request, page_id: int, data: ArticlePatch):
    """Partially update article; publish=true syncs when enabled."""
    try:
        page = (
            ArticlePage.objects
            .select_related('locale', 'featured_image')
            .prefetch_related('metafields', 'tagged_items__tag')
            .get(pk=page_id)
        )
    except ArticlePage.DoesNotExist:
        return 404, {"detail": f"Article page {page_id} not found."}

    if data.title is not None:
        page.title = data.title
    if data.shopify_id is not None:
        page.shopify_id = data.shopify_id
    if data.handle is not None:
        page.handle = data.handle
        page.slug = slugify(data.handle)
    if data.author is not None:
        page.author = data.author
    if data.published_at is not None:
        page.published_at = data.published_at
    if data.summary is not None:
        page.summary = data.summary
    if data.featured_image_id is not None:
        page.featured_image_id = data.featured_image_id
    if data.sync_enabled is not None:
        page.sync_enabled = data.sync_enabled
    if data.seo_title is not None:
        page.seo_title = data.seo_title
    if data.search_description is not None:
        page.search_description = data.search_description
    if data.locale is not None:
        page.locale = resolve_locale(data.locale)
    if data.translation_of is not None:
        source = apply_translation_link(page, data.translation_of, ArticlePage)
        inherit_shopify_id_from_source(page, source)
    if data.body is not None:
        page.body = json.dumps(data.body)

    if data.tags is not None:
        page.tags.set(data.tags)

    if data.metafields is not None:
        page.metafields.all().delete()
        for mf in data.metafields:
            ArticlePageMetafield.objects.create(
                page=page,
                namespace=mf.namespace,
                key=mf.key,
                type=mf.type,
                value=mf.value,
            )

    if data.publish:
        revision = page.save_revision()
        revision.publish()
    else:
        page.save()

    page.refresh_from_db()
    return page


@router.delete(
    '/{page_id}',
    response={204: None, 404: ErrorSchema},
    summary="Delete Article",
    operation_id="delete_article",
    description=capability_docstring("delete_article"),
    openapi_extra=agent_openapi_extra("delete_article"),
)
def delete_article(request, page_id: int):
    """Delete Wagtail article page only."""
    try:
        page = ArticlePage.objects.get(pk=page_id)
        page.delete()
        return 204, None
    except ArticlePage.DoesNotExist:
        return 404, {"detail": f"Article page {page_id} not found."}


@router.post(
    '/{page_id}/push',
    response={200: SyncResultSchema, 404: ErrorSchema, 400: ErrorSchema},
    summary="Push Article to Shopify",
    operation_id="push_article",
    description=capability_docstring("push_article"),
    openapi_extra=agent_openapi_extra("push_article"),
)
def push_article(request, page_id: int):
    """Push article to Shopify; parent blog must have shopify_id."""
    try:
        page = ArticlePage.objects.get(pk=page_id)
    except ArticlePage.DoesNotExist:
        return 404, {"detail": f"Article page {page_id} not found."}

    try:
        success = sync_article_page(page)
        page.refresh_from_db()
        return {
            "success": success,
            "message": (
                "Article synced to Shopify successfully."
                if success
                else "Sync failed. Ensure the parent BlogPage has a shopify_id. Check server logs for details."
            ),
            "shopify_id": page.shopify_id or None,
        }
    except Exception as e:
        return 400, {"detail": f"Sync error: {str(e)}"}

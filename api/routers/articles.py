import json
from typing import List, Optional

from ninja import Router
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from ninja.errors import HttpError

from shopify_content.models import BlogPage, ArticlePage
from shopify_content.models.blog import ArticlePageMetafield
from shopify_content.sync.outbound import sync_article_page
from shopify_content.sync.task_dispatch import enqueue_shopify_import, sync_run_to_task_response

from ..schemas.article import ArticleIn, ArticlePatch, ArticleOut
from ..schemas.common import SyncResultSchema, ImportResultSchema, ImportTaskSchema, ErrorSchema
from ..locale_utils import (
    resolve_locale,
    apply_translation_link,
    inherit_shopify_id_from_source,
    filter_queryset_by_locale,
)

router = Router()


@router.get('/', response=List[ArticleOut], summary="List Articles")
def list_articles(
    request,
    live_only: bool = False,
    locale: Optional[str] = None,
    blog_id: Optional[int] = None,
    limit: int = 50,
    offset: int = 0,
):
    """
    Retrieve a paginated list of Article pages from Wagtail.

    Use this to discover all articles across all blogs, or filter by blog_id to list
    articles for a specific blog. Each article is nested under a parent BlogPage.

    Filter by blog_id (Wagtail page ID of the parent BlogPage) to get articles for a specific blog.
    Filter by locale (e.g. 'en-US', 'es-US', 'fr-CA') to get locale-specific versions.
    Set live_only=true to exclude unpublished drafts.

    Pagination: use limit (default 50) and offset to page through results.
    Returns an empty list if no articles match the filters.
    """
    qs = (
        ArticlePage.objects
        .select_related('locale', 'featured_image')
        .prefetch_related('metafields', 'tagged_items__tag')
    )
    if live_only:
        qs = qs.live()
    qs = filter_queryset_by_locale(qs, locale)
    if blog_id:
        qs = qs.child_of(BlogPage.objects.filter(pk=blog_id).first() or BlogPage())
    return list(qs[offset:offset + limit])


@router.post('/', response={201: ArticleOut, 400: ErrorSchema}, summary="Create Article")
def create_article(request, data: ArticleIn):
    """
    Create a new Article page in Wagtail as a child of the specified BlogPage.

    This creates the Wagtail CMS entry only — it does NOT create an article in Shopify.
    The article will be created in Shopify when POST /articles/{id}/push is called,
    provided the parent BlogPage has a shopify_id.

    Required: blog_id — Wagtail page ID of the parent BlogPage.
    Use GET /blogs/ to find available blogs and their IDs.

    Typical agent workflow:
    1. Ensure the parent BlogPage exists and has a shopify_id (push it first if needed).
    2. POST /articles/ with the content and blog_id.
    3. PATCH /articles/{id} with publish=true to publish and sync to Shopify.

    The page is saved as a draft (unpublished). Call PATCH with publish=true to publish and sync.

    Returns HTTP 400 if the blog_id does not correspond to a BlogPage.
    """
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


@router.post('/pull', response={202: ImportTaskSchema, 400: ErrorSchema}, summary="Pull Articles from Shopify")
def pull_articles(request):
    """
    Import all blogs and articles from the connected Shopify store into Wagtail.

    Articles are nested inside blogs in Shopify, so this endpoint imports both blogs
    and their articles in one operation. BlogPage instances are created under ShopifyRootPage,
    and ArticlePage instances are created as children of their respective BlogPage.

    This is equivalent to POST /blogs/pull — both trigger the same blog+article import.
    Use this endpoint when you specifically want to refresh article content.

    Existing pages are matched by shopify_id and updated in place.
    New blogs/articles are created as draft pages.

    Prerequisites:
    - A ShopConfig with a valid Shopify offline access token must exist.
    - The ShopifyRootPage for blogs (slug=blogs) is created automatically if missing.

    Returns 202 with sync_run_id and celery_task_id for async import tracking.
    """
    try:
        sync_run = enqueue_shopify_import('blogs', new_only=False)
        return 202, sync_run_to_task_response(sync_run)
    except RuntimeError as e:
        raise HttpError(400, str(e))


@router.get('/{page_id}', response={200: ArticleOut, 404: ErrorSchema}, summary="Get Article")
def get_article(request, page_id: int):
    """
    Retrieve a single Article page by its Wagtail page ID.

    Returns full article data including body blocks, metafields, tags, author, published_at,
    sync state, locale, blog_id (parent blog page ID), and blog_title.
    Use the 'shopify_id' field to correlate with the corresponding Shopify Article.
    The 'last_synced_at' timestamp shows when the article was last pushed to Shopify.

    The page_id is the Wagtail integer page ID returned by GET /articles/ or POST /articles/.
    """
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


@router.patch('/{page_id}', response={200: ArticleOut, 404: ErrorSchema, 400: ErrorSchema}, summary="Update Article")
def update_article(request, page_id: int, data: ArticlePatch):
    """
    Partially update an Article page. Only fields included in the request body are changed.

    Set publish=true to publish the page immediately. If sync_enabled=true on the page,
    publishing will automatically trigger an outbound sync to Shopify via the publish hook.

    If the article has no shopify_id, publishing with sync_enabled=true will CREATE the article
    in Shopify (articleCreate mutation), provided the parent BlogPage has a shopify_id.
    The returned Shopify GID is saved to the page automatically.

    To update content without syncing to Shopify, set sync_enabled=false before patching,
    or leave publish=false (default) to save as a draft only.

    To replace all tags, pass the full desired tags list. To clear tags, pass an empty list [].
    To replace all metafields, pass the full desired metafields list. To clear, pass [].
    Omit any field from the request body to leave it unchanged.
    """
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


@router.delete('/{page_id}', response={204: None, 404: ErrorSchema}, summary="Delete Article")
def delete_article(request, page_id: int):
    """
    Delete an Article page from Wagtail. This does NOT delete the article in Shopify.

    Use this to remove a Wagtail page that should no longer be managed here.
    The Shopify article remains untouched. This action is irreversible.
    """
    try:
        page = ArticlePage.objects.get(pk=page_id)
        page.delete()
        return 204, None
    except ArticlePage.DoesNotExist:
        return 404, {"detail": f"Article page {page_id} not found."}


@router.post('/{page_id}/push', response={200: SyncResultSchema, 404: ErrorSchema, 400: ErrorSchema}, summary="Push Article to Shopify")
def push_article(request, page_id: int):
    """
    Push an Article page's content from Wagtail to Shopify Admin API.

    Triggers an explicit outbound sync regardless of the page's publish state.
    Pushes: title, body (HTML), summary, author, tags, published_at, isPublished,
    SEO as metafields (global.title_tag, global.description_tag), and all inline metafields.

    If the article has no shopify_id, this will CREATE a new article in Shopify (articleCreate)
    using the parent BlogPage's shopify_id as the target blog. The returned Shopify GID
    is saved to the page automatically. Re-fetch the page after creation to see the populated shopify_id.

    Requirements:
    - The parent BlogPage must have a shopify_id set. Push the blog first if needed.
    - A ShopConfig with a valid Shopify access token must exist.

    Returns success=false if Shopify returns errors or the parent blog is not synced.
    Check the 'message' field for details on failures.
    """
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

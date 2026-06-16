from typing import List, Optional

from ninja import Router
from django.utils.text import slugify
from ninja.errors import HttpError

from shopify_content.models import BlogPage
from shopify_content.sync.outbound import sync_blog_page
from shopify_content.sync.service import run_shopify_import_for_api
from shopify_content.sync.import_parents import resolve_shopify_import_parent

from ..schemas.blog import BlogIn, BlogPatch, BlogOut
from ..schemas.common import SyncResultSchema, ImportResultSchema, ErrorSchema
from ..locale_utils import (
    resolve_locale,
    apply_translation_link,
    inherit_shopify_id_from_source,
    filter_queryset_by_locale,
)

router = Router()


@router.get('/', response=List[BlogOut], summary="List Blogs")
def list_blogs(
    request,
    live_only: bool = False,
    locale: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
):
    """
    Retrieve a paginated list of Blog pages from Wagtail.

    Blogs are containers for articles. Each blog corresponds to a Shopify Blog object.
    Use this to discover all blogs and their article counts.
    Filter by locale (e.g. 'en-US', 'es-US', 'fr-CA') to get locale-specific versions.
    Set live_only=true to exclude unpublished drafts.

    Pagination: use limit (default 50) and offset to page through results.
    Returns an empty list if no blogs match the filters.
    """
    qs = BlogPage.objects.select_related('locale')
    if live_only:
        qs = qs.live()
    qs = filter_queryset_by_locale(qs, locale)
    return list(qs[offset:offset + limit])


@router.post('/', response={201: BlogOut, 400: ErrorSchema}, summary="Create Blog")
def create_blog(request, data: BlogIn):
    """
    Create a new Blog page in Wagtail under the ShopifyRootPage.

    This creates the Wagtail CMS entry only. The blog will be created in Shopify when
    POST /blogs/{id}/push is called (Shopify Blog creation happens on first push).
    The blog's shopify_id is populated automatically after the first successful push.

    The page is saved as a draft (unpublished). Call PATCH with publish=true to publish.
    After publishing with sync_enabled=true, the blog is created/updated in Shopify.

    Returns HTTP 400 if the Wagtail site is not configured.
    """
    try:
        parent = resolve_shopify_import_parent('blogs')
    except RuntimeError as e:
        return 400, {"detail": str(e)}

    slug = slugify(data.handle or data.title)

    page = BlogPage(
        title=data.title,
        slug=slug,
        locale=resolve_locale(data.locale),
        shopify_id=data.shopify_id or '',
        handle=data.handle or slug,
        comment_policy=data.comment_policy or 'CLOSED',
        sync_enabled=data.sync_enabled if data.sync_enabled is not None else True,
    )

    source = apply_translation_link(page, data.translation_of, BlogPage)
    inherit_shopify_id_from_source(page, source)

    parent.add_child(instance=page)
    page.refresh_from_db()
    return 201, page


@router.post('/pull', response=ImportResultSchema, summary="Pull Blogs (and Articles) from Shopify")
def pull_blogs(request):
    """
    Import all blogs and their articles from the connected Shopify store into Wagtail.

    Fetches all Shopify Blogs and their nested Articles, creating or updating:
    - BlogPage instances under ShopifyRootPage
    - ArticlePage instances as children of their respective BlogPage

    Existing pages are matched by shopify_id and updated in place.
    New blogs/articles are created as draft pages.

    This is the recommended starting point for agents managing blog content:
    call this once to populate Wagtail with all Shopify blog content, then use
    PATCH and /push to make content changes to individual blogs or articles.

    Note: This endpoint also imports all articles. You do not need to call
    POST /articles/pull separately.

    Prerequisites:
    - A ShopConfig with a valid Shopify offline access token must exist.
    - The ShopifyRootPage for blogs (slug=blogs) is created automatically if missing.

    Returns blog import counts (articles are imported as a side effect).
    """
    try:
        return run_shopify_import_for_api('blogs', new_only=False)
    except RuntimeError as e:
        raise HttpError(400, str(e))


@router.get('/{page_id}', response={200: BlogOut, 404: ErrorSchema}, summary="Get Blog")
def get_blog(request, page_id: int):
    """
    Retrieve a single Blog page by its Wagtail page ID.

    Returns full blog data including comment_policy, sync state, locale, and article_count.
    Use the 'shopify_id' field to correlate with the corresponding Shopify Blog.
    The 'last_synced_at' timestamp shows when the blog was last pushed to Shopify.
    The 'article_count' field shows how many published articles are nested under this blog.

    The page_id is the Wagtail integer page ID returned by GET /blogs/ or POST /blogs/.
    """
    try:
        page = BlogPage.objects.select_related('locale').get(pk=page_id)
        return page
    except BlogPage.DoesNotExist:
        return 404, {"detail": f"Blog page {page_id} not found."}


@router.patch('/{page_id}', response={200: BlogOut, 404: ErrorSchema, 400: ErrorSchema}, summary="Update Blog")
def update_blog(request, page_id: int, data: BlogPatch):
    """
    Partially update a Blog page. Only fields included in the request body are changed.

    Set publish=true to publish the page immediately. If sync_enabled=true on the page,
    publishing will automatically trigger an outbound sync to Shopify via the publish hook.

    If the blog has no shopify_id and sync_enabled=true, publishing will CREATE the blog
    in Shopify (blogCreate mutation) and save the returned shopify_id automatically.

    To update content without syncing to Shopify, set sync_enabled=false before patching,
    or leave publish=false (default) to save as a draft only.

    Omit any field from the request body to leave it unchanged.
    """
    try:
        page = BlogPage.objects.select_related('locale').get(pk=page_id)
    except BlogPage.DoesNotExist:
        return 404, {"detail": f"Blog page {page_id} not found."}

    if data.title is not None:
        page.title = data.title
    if data.shopify_id is not None:
        page.shopify_id = data.shopify_id
    if data.handle is not None:
        page.handle = data.handle
        page.slug = slugify(data.handle)
    if data.comment_policy is not None:
        page.comment_policy = data.comment_policy
    if data.sync_enabled is not None:
        page.sync_enabled = data.sync_enabled
    if data.locale is not None:
        page.locale = resolve_locale(data.locale)
    if data.translation_of is not None:
        source = apply_translation_link(page, data.translation_of, BlogPage)
        inherit_shopify_id_from_source(page, source)

    if data.publish:
        revision = page.save_revision()
        revision.publish()
    else:
        page.save()

    page.refresh_from_db()
    return page


@router.delete('/{page_id}', response={204: None, 404: ErrorSchema}, summary="Delete Blog")
def delete_blog(request, page_id: int):
    """
    Delete a Blog page and all its child Article pages from Wagtail.
    This does NOT delete the blog or articles in Shopify.

    Warning: This is a cascading delete — all ArticlePage children of this blog
    will also be removed from Wagtail. The Shopify blog and articles remain untouched.
    This action is irreversible.
    """
    try:
        page = BlogPage.objects.get(pk=page_id)
        page.delete()
        return 204, None
    except BlogPage.DoesNotExist:
        return 404, {"detail": f"Blog page {page_id} not found."}


@router.post('/{page_id}/push', response={200: SyncResultSchema, 404: ErrorSchema, 400: ErrorSchema}, summary="Push Blog to Shopify")
def push_blog(request, page_id: int):
    """
    Push a Blog page's content from Wagtail to Shopify Admin API.

    Triggers an explicit outbound sync regardless of the page's publish state.
    Pushes: title, handle, comment_policy.

    If the blog has no shopify_id, this will CREATE a new blog in Shopify (blogCreate)
    and save the returned Shopify GID to the page automatically.
    If shopify_id is already set, this performs a blogUpdate.

    Requirements:
    - A ShopConfig with a valid Shopify access token must exist.

    Returns success=false if Shopify returns errors or the token is invalid.
    After a successful push of a new blog, re-fetch the page to see the populated shopify_id.
    """
    try:
        page = BlogPage.objects.get(pk=page_id)
    except BlogPage.DoesNotExist:
        return 404, {"detail": f"Blog page {page_id} not found."}

    try:
        success = sync_blog_page(page)
        page.refresh_from_db()
        return {
            "success": success,
            "message": (
                "Blog synced to Shopify successfully."
                if success
                else "Sync failed. Check server logs for GraphQL errors."
            ),
            "shopify_id": page.shopify_id or None,
        }
    except Exception as e:
        return 400, {"detail": f"Sync error: {str(e)}"}

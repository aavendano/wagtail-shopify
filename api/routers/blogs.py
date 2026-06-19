from typing import List, Optional

from ninja import Router
from django.utils.text import slugify

from shopify_content.models import BlogPage
from shopify_content.sync.outbound import sync_blog_page
from shopify_content.sync.import_parents import resolve_shopify_import_parent

from ..sync import execute_pull
from ..schemas.blog import BlogIn, BlogPatch, BlogOut
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
    response=List[BlogOut],
    summary="List Blogs",
    operation_id="list_blogs",
    description=capability_docstring("list_blogs"),
    openapi_extra=agent_openapi_extra("list_blogs"),
)
def list_blogs(
    request,
    live_only: bool = False,
    locale: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
):
    """Discover blogs before managing articles."""
    qs = BlogPage.objects.select_related('locale')
    if live_only:
        qs = qs.live()
    qs = filter_queryset_by_locale(qs, locale)
    return list(qs[offset:offset + limit])


@router.post(
    '/',
    response={201: BlogOut, 400: ErrorSchema},
    summary="Create Blog",
    operation_id="create_blog",
    description=capability_docstring("create_blog"),
    openapi_extra=agent_openapi_extra("create_blog"),
)
def create_blog(request, data: BlogIn):
    """Create Wagtail blog page."""
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


@router.post(
    '/pull',
    response={200: ImportResultSchema, 400: ErrorSchema},
    summary="Pull Blogs and Articles from Shopify (sync)",
    operation_id="pull_blogs_sync",
    description=capability_docstring("pull_blogs_sync"),
    openapi_extra=agent_openapi_extra("pull_blogs_sync"),
)
def pull_blogs(request):
    """Import blogs and nested articles from Shopify synchronously."""
    return execute_pull('blogs')


@router.get(
    '/{page_id}',
    response={200: BlogOut, 404: ErrorSchema},
    summary="Get Blog",
    operation_id="get_blog",
    description=capability_docstring("get_blog"),
    openapi_extra=agent_openapi_extra("get_blog"),
)
def get_blog(request, page_id: int):
    """Get single blog by Wagtail page ID."""
    try:
        page = BlogPage.objects.select_related('locale').get(pk=page_id)
        return page
    except BlogPage.DoesNotExist:
        return 404, {"detail": f"Blog page {page_id} not found."}


@router.patch(
    '/{page_id}',
    response={200: BlogOut, 404: ErrorSchema, 400: ErrorSchema},
    summary="Update Blog",
    operation_id="update_blog",
    description=capability_docstring("update_blog"),
    openapi_extra=agent_openapi_extra("update_blog"),
)
def update_blog(request, page_id: int, data: BlogPatch):
    """Partially update blog; publish=true may create blog in Shopify."""
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


@router.delete(
    '/{page_id}',
    response={204: None, 404: ErrorSchema},
    summary="Delete Blog",
    operation_id="delete_blog",
    description=capability_docstring("delete_blog"),
    openapi_extra=agent_openapi_extra("delete_blog"),
)
def delete_blog(request, page_id: int):
    """Delete blog and child articles from Wagtail only."""
    try:
        page = BlogPage.objects.get(pk=page_id)
        page.delete()
        return 204, None
    except BlogPage.DoesNotExist:
        return 404, {"detail": f"Blog page {page_id} not found."}


@router.post(
    '/{page_id}/push',
    response={200: SyncResultSchema, 404: ErrorSchema, 400: ErrorSchema},
    summary="Push Blog to Shopify",
    operation_id="push_blog",
    description=capability_docstring("push_blog"),
    openapi_extra=agent_openapi_extra("push_blog"),
)
def push_blog(request, page_id: int):
    """Push blog to Shopify; creates blog if shopify_id is missing."""
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

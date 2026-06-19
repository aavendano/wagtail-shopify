import json
from typing import List, Optional

from ninja import Router
from django.utils.text import slugify

from shopify_content.models import CollectionPage
from shopify_content.models.collection import CollectionPageMetafield
from shopify_content.sync.outbound import sync_collection_page
from shopify_content.sync.import_parents import resolve_shopify_import_parent

from ..sync import execute_pull
from ..schemas.collection import CollectionIn, CollectionPatch, CollectionOut
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
    response=List[CollectionOut],
    summary="List Collections",
    operation_id="list_collections",
    description=capability_docstring("list_collections"),
    openapi_extra=agent_openapi_extra("list_collections"),
)
def list_collections(
    request,
    live_only: bool = False,
    locale: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
):
    """Discover collections before read/update."""
    qs = CollectionPage.objects.select_related('locale').prefetch_related('metafields')
    if live_only:
        qs = qs.live()
    qs = filter_queryset_by_locale(qs, locale)
    return list(qs[offset:offset + limit])


@router.post(
    '/',
    response={201: CollectionOut, 400: ErrorSchema},
    summary="Create Collection",
    operation_id="create_collection",
    description=capability_docstring("create_collection"),
    openapi_extra=agent_openapi_extra("create_collection"),
)
def create_collection(request, data: CollectionIn):
    """Create Wagtail collection page."""
    try:
        parent = resolve_shopify_import_parent('collections')
    except RuntimeError as e:
        return 400, {"detail": str(e)}

    slug = slugify(data.handle or data.title)

    page = CollectionPage(
        title=data.title,
        slug=slug,
        locale=resolve_locale(data.locale),
        shopify_id=data.shopify_id or '',
        handle=data.handle or slug,
        sort_order=data.sort_order or 'MANUAL',
        sync_enabled=data.sync_enabled if data.sync_enabled is not None else True,
        seo_title=data.seo_title or '',
        search_description=data.search_description or '',
    )

    if data.description:
        page.description = json.dumps(data.description)

    source = apply_translation_link(page, data.translation_of, CollectionPage)
    inherit_shopify_id_from_source(page, source)

    parent.add_child(instance=page)

    if data.metafields:
        for mf in data.metafields:
            CollectionPageMetafield.objects.create(
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
    summary="Pull Collections from Shopify (sync)",
    operation_id="pull_collections_sync",
    description=capability_docstring("pull_collections_sync"),
    openapi_extra=agent_openapi_extra("pull_collections_sync"),
)
def pull_collections(request):
    """Import all collections from Shopify synchronously."""
    return execute_pull('collections')


@router.get(
    '/{page_id}',
    response={200: CollectionOut, 404: ErrorSchema},
    summary="Get Collection",
    operation_id="get_collection",
    description=capability_docstring("get_collection"),
    openapi_extra=agent_openapi_extra("get_collection"),
)
def get_collection(request, page_id: int):
    """Get single collection by Wagtail page ID."""
    try:
        page = (
            CollectionPage.objects
            .select_related('locale')
            .prefetch_related('metafields')
            .get(pk=page_id)
        )
        return page
    except CollectionPage.DoesNotExist:
        return 404, {"detail": f"Collection page {page_id} not found."}


@router.patch(
    '/{page_id}',
    response={200: CollectionOut, 404: ErrorSchema, 400: ErrorSchema},
    summary="Update Collection",
    operation_id="update_collection",
    description=capability_docstring("update_collection"),
    openapi_extra=agent_openapi_extra("update_collection"),
)
def update_collection(request, page_id: int, data: CollectionPatch):
    """Partially update collection; publish=true triggers sync when enabled."""
    try:
        page = (
            CollectionPage.objects
            .select_related('locale')
            .prefetch_related('metafields')
            .get(pk=page_id)
        )
    except CollectionPage.DoesNotExist:
        return 404, {"detail": f"Collection page {page_id} not found."}

    if data.title is not None:
        page.title = data.title
    if data.shopify_id is not None:
        page.shopify_id = data.shopify_id
    if data.handle is not None:
        page.handle = data.handle
        page.slug = slugify(data.handle)
    if data.sort_order is not None:
        page.sort_order = data.sort_order
    if data.sync_enabled is not None:
        page.sync_enabled = data.sync_enabled
    if data.seo_title is not None:
        page.seo_title = data.seo_title
    if data.search_description is not None:
        page.search_description = data.search_description
    if data.locale is not None:
        page.locale = resolve_locale(data.locale)
    if data.translation_of is not None:
        source = apply_translation_link(page, data.translation_of, CollectionPage)
        inherit_shopify_id_from_source(page, source)
    if data.description is not None:
        page.description = json.dumps(data.description)

    if data.metafields is not None:
        page.metafields.all().delete()
        for mf in data.metafields:
            CollectionPageMetafield.objects.create(
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
    summary="Delete Collection",
    operation_id="delete_collection",
    description=capability_docstring("delete_collection"),
    openapi_extra=agent_openapi_extra("delete_collection"),
)
def delete_collection(request, page_id: int):
    """Delete Wagtail collection page only."""
    try:
        page = CollectionPage.objects.get(pk=page_id)
        page.delete()
        return 204, None
    except CollectionPage.DoesNotExist:
        return 404, {"detail": f"Collection page {page_id} not found."}


@router.post(
    '/{page_id}/push',
    response={200: SyncResultSchema, 404: ErrorSchema, 400: ErrorSchema},
    summary="Push Collection to Shopify",
    operation_id="push_collection",
    description=capability_docstring("push_collection"),
    openapi_extra=agent_openapi_extra("push_collection"),
)
def push_collection(request, page_id: int):
    """Push collection content to Shopify Admin API."""
    try:
        page = CollectionPage.objects.get(pk=page_id)
    except CollectionPage.DoesNotExist:
        return 404, {"detail": f"Collection page {page_id} not found."}

    if not page.shopify_id:
        return 400, {
            "detail": (
                "This collection has no shopify_id. Set shopify_id before pushing, "
                "or use POST /collections/pull/ to import from Shopify."
            )
        }

    try:
        success = sync_collection_page(page)
        page.refresh_from_db()
        return {
            "success": success,
            "message": (
                "Collection synced to Shopify successfully."
                if success
                else "Sync failed. Check server logs for GraphQL errors."
            ),
            "shopify_id": page.shopify_id,
        }
    except Exception as e:
        return 400, {"detail": f"Sync error: {str(e)}"}

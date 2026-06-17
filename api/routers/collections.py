import json
from typing import List, Optional

from ninja import Router
from django.utils.text import slugify
from ninja.errors import HttpError

from shopify_content.models import CollectionPage
from shopify_content.models.collection import CollectionPageMetafield
from shopify_content.sync.outbound import sync_collection_page
from shopify_content.sync.task_dispatch import enqueue_shopify_import, sync_run_to_task_response
from shopify_content.sync.import_parents import resolve_shopify_import_parent

from ..schemas.collection import CollectionIn, CollectionPatch, CollectionOut
from ..schemas.common import SyncResultSchema, ImportResultSchema, ImportTaskSchema, ErrorSchema
from ..locale_utils import (
    resolve_locale,
    apply_translation_link,
    inherit_shopify_id_from_source,
    filter_queryset_by_locale,
)

router = Router()


@router.get('/', response=List[CollectionOut], summary="List Collections")
def list_collections(
    request,
    live_only: bool = False,
    locale: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
):
    """
    Retrieve a paginated list of Collection pages from Wagtail.

    Use this to discover all collections, check sync status, or find collections by locale.
    Filter by locale (e.g. 'en-US', 'es-US', 'fr-CA') to get locale-specific versions.
    Set live_only=true to exclude unpublished drafts.

    Pagination: use limit (default 50) and offset to page through results.
    Returns an empty list if no collections match the filters.
    """
    qs = CollectionPage.objects.select_related('locale').prefetch_related('metafields')
    if live_only:
        qs = qs.live()
    qs = filter_queryset_by_locale(qs, locale)
    return list(qs[offset:offset + limit])


@router.post('/', response={201: CollectionOut, 400: ErrorSchema}, summary="Create Collection")
def create_collection(request, data: CollectionIn):
    """
    Create a new Collection page in Wagtail under the ShopifyRootPage.

    This creates the Wagtail CMS entry only — it does NOT create a collection in Shopify.
    Typical agent workflow:
    1. Create collection in Shopify first (via Shopify API or admin).
    2. Set shopify_id to link this page to the Shopify collection.
    3. Call POST /collections/{id}/push/ to push content to Shopify.

    Alternatively, use POST /collections/pull/ to import all collections from Shopify automatically.
    The page is saved as a draft (unpublished). Call PATCH with publish=true to publish and sync.

    Returns HTTP 400 if the Wagtail site is not configured.
    """
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


@router.post('/pull', response={202: ImportTaskSchema, 400: ErrorSchema}, summary="Pull Collections from Shopify")
def pull_collections(request):
    """
    Import all collections from the connected Shopify store into Wagtail as CollectionPage instances.

    Fetches all collections from Shopify Admin API and creates or updates matching Wagtail pages
    under the ShopifyRootPage. Existing pages are matched by shopify_id and updated in place.
    New collections are created as draft pages.

    This is the recommended starting point for agents working with an existing Shopify store:
    call this once to populate Wagtail with all Shopify collections, then use PATCH and /push
    to make content changes.

    Prerequisites:
    - A ShopConfig with a valid Shopify offline access token must exist.
    - The ShopifyRootPage for collections (slug=collections) is created automatically if missing.

    Returns 202 with sync_run_id and celery_task_id for async import tracking.
    """
    try:
        sync_run = enqueue_shopify_import('collections', new_only=False)
        return 202, sync_run_to_task_response(sync_run)
    except RuntimeError as e:
        raise HttpError(400, str(e))


@router.get('/{page_id}', response={200: CollectionOut, 404: ErrorSchema}, summary="Get Collection")
def get_collection(request, page_id: int):
    """
    Retrieve a single Collection page by its Wagtail page ID.

    Returns full collection data including description blocks, metafields, sync state, and locale.
    Use the 'shopify_id' field to correlate with the corresponding Shopify collection.
    The 'last_synced_at' timestamp shows when content was last pushed to Shopify.
    A null 'last_synced_at' means the collection has never been synced to Shopify.

    The page_id is the Wagtail integer page ID returned by GET /collections/ or POST /collections/.
    """
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


@router.patch('/{page_id}', response={200: CollectionOut, 404: ErrorSchema, 400: ErrorSchema}, summary="Update Collection")
def update_collection(request, page_id: int, data: CollectionPatch):
    """
    Partially update a Collection page. Only fields included in the request body are changed.

    Set publish=true to publish the page immediately. If sync_enabled=true on the page,
    publishing will automatically trigger an outbound sync to Shopify via the publish hook.

    To update content without syncing to Shopify, set sync_enabled=false before patching,
    or leave publish=false (default) to save as a draft only.

    To replace all metafields, pass the full desired metafields list. To clear, pass [].
    Omit any field from the request body to leave it unchanged.
    """
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


@router.delete('/{page_id}', response={204: None, 404: ErrorSchema}, summary="Delete Collection")
def delete_collection(request, page_id: int):
    """
    Delete a Collection page from Wagtail. This does NOT delete the collection in Shopify.

    Use this to remove a Wagtail page that should no longer be managed here.
    The Shopify collection remains untouched. This action is irreversible.
    """
    try:
        page = CollectionPage.objects.get(pk=page_id)
        page.delete()
        return 204, None
    except CollectionPage.DoesNotExist:
        return 404, {"detail": f"Collection page {page_id} not found."}


@router.post('/{page_id}/push', response={200: SyncResultSchema, 404: ErrorSchema, 400: ErrorSchema}, summary="Push Collection to Shopify")
def push_collection(request, page_id: int):
    """
    Push a Collection page's content from Wagtail to Shopify Admin API.

    Triggers an explicit outbound sync regardless of the page's publish state.
    Pushes: title, descriptionHtml (rendered StreamField description), SEO fields, and all metafields.

    Requirements:
    - The page must have a shopify_id set (format: 'gid://shopify/Collection/{id}').
    - A ShopConfig with a valid Shopify access token must exist.

    Returns success=false if Shopify returns errors or the token is invalid.
    Check the 'message' field for details on failures.
    Use POST /collections/pull first if collections have not yet been imported from Shopify.
    """
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

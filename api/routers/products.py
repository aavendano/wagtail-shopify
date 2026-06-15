import json
from typing import List, Optional

from ninja import Router
from django.utils.text import slugify
from ninja.errors import HttpError

from shopify_content.models import ProductPage, ShopifyRootPage
from shopify_content.models.product import ProductPageMetafield
from shopify_content.sync.outbound import sync_product_page
from shopify_content.sync.inbound import import_products, _get_shop

from ..schemas.product import ProductIn, ProductPatch, ProductOut
from ..schemas.common import SyncResultSchema, ImportResultSchema, ErrorSchema
from ..locale_utils import (
    resolve_locale,
    apply_translation_link,
    inherit_shopify_id_from_source,
    filter_queryset_by_locale,
)

router = Router()


@router.get('/', response=List[ProductOut], summary="List Products")
def list_products(
    request,
    live_only: bool = False,
    locale: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
):
    """
    Retrieve a paginated list of Product pages from Wagtail.

    Use this to discover all products, check sync status, or find products by locale/status.
    Filter by locale (e.g. 'en-US', 'es-US', 'fr-CA') to get locale-specific versions.
    Filter by status='ACTIVE' to only see published Shopify products.
    Set live_only=true to exclude unpublished drafts.

    Pagination: use limit (default 50, max recommended 200) and offset to page through results.
    Returns an empty list if no products match the filters.
    """
    qs = ProductPage.objects.select_related('locale').prefetch_related(
        'metafields', 'tagged_items__tag'
    )
    if live_only:
        qs = qs.live()
    qs = filter_queryset_by_locale(qs, locale)
    if status:
        qs = qs.filter(status=status)
    return list(qs[offset:offset + limit])


@router.post('/', response={201: ProductOut, 400: ErrorSchema}, summary="Create Product")
def create_product(request, data: ProductIn):
    """
    Create a new Product page in Wagtail under the ShopifyRootPage.

    This creates the Wagtail CMS entry only — it does NOT create a product in Shopify.
    Typical agent workflow:
    1. Create product in Shopify first (via Shopify API or admin).
    2. Set shopify_id to link this page to the Shopify product.
    3. Call POST /products/{id}/push/ to push content to Shopify.

    Alternatively, use POST /products/pull/ to import all products from Shopify automatically.
    The page is saved as a draft (unpublished). Call PATCH with publish=true to publish and sync.

    Returns HTTP 400 if no ShopifyRootPage exists in the Wagtail page tree (create one in Wagtail admin first).
    """
    parent = ShopifyRootPage.objects.first()
    if not parent:
        return 400, {"detail": "No ShopifyRootPage found. Create one in Wagtail admin first."}

    slug = slugify(data.handle or data.title)

    page = ProductPage(
        title=data.title,
        slug=slug,
        locale=resolve_locale(data.locale),
        shopify_id=data.shopify_id or '',
        handle=data.handle or slug,
        status=data.status or 'ACTIVE',
        vendor=data.vendor or '',
        product_type=data.product_type or '',
        sync_enabled=data.sync_enabled if data.sync_enabled is not None else True,
        seo_title=data.seo_title or '',
        search_description=data.search_description or '',
    )

    if data.body:
        page.body = json.dumps(data.body)

    source = apply_translation_link(page, data.translation_of, ProductPage)
    inherit_shopify_id_from_source(page, source)

    parent.add_child(instance=page)

    if data.tags:
        page.tags.set(*data.tags)

    if data.metafields:
        for mf in data.metafields:
            ProductPageMetafield.objects.create(
                page=page,
                namespace=mf.namespace,
                key=mf.key,
                type=mf.type,
                value=mf.value,
            )

    page.refresh_from_db()
    return 201, page


@router.get('/pull', response=ImportResultSchema, summary="Pull Products from Shopify")
def pull_products_get(request):
    """
    Alias for POST /products/pull — provided for agent discoverability.
    Use POST /products/pull for the actual import operation.
    """
    return _do_pull_products()


@router.post('/pull', response=ImportResultSchema, summary="Pull Products from Shopify")
def pull_products(request):
    """
    Import all products from the connected Shopify store into Wagtail as ProductPage instances.

    Fetches all products from Shopify Admin API and creates or updates matching Wagtail pages
    under the ShopifyRootPage. Existing pages are matched by shopify_id and updated in place.
    New products are created as draft pages.

    This is the recommended starting point for agents working with an existing Shopify store:
    call this once to populate Wagtail with all Shopify products, then use PATCH and /push
    to make content changes.

    Prerequisites:
    - A ShopifyRootPage must exist in the Wagtail page tree.
    - A ShopConfig with a valid Shopify offline access token must exist.

    Returns counts of created, updated, and failed imports.
    Failures are logged server-side; the operation continues despite individual errors.
    """
    return _do_pull_products()


def _do_pull_products():
    try:
        shop = _get_shop()
    except RuntimeError as e:
        raise HttpError(400, str(e))

    parent = ShopifyRootPage.objects.first()
    if not parent:
        raise HttpError(400, "No ShopifyRootPage found. Create one in Wagtail admin first.")

    stats = import_products(shop, parent)
    return {
        **stats,
        "message": f"Import complete. Created: {stats['created']}, Updated: {stats['updated']}, Errors: {stats['errors']}",
    }


@router.get('/{page_id}', response={200: ProductOut, 404: ErrorSchema}, summary="Get Product")
def get_product(request, page_id: int):
    """
    Retrieve a single Product page by its Wagtail page ID.

    Returns full product data including body blocks, metafields, tags, sync state, and locale.
    Use the 'shopify_id' field to correlate with the corresponding Shopify product.
    The 'last_synced_at' timestamp shows when content was last pushed to Shopify.
    A null 'last_synced_at' means the product has never been synced to Shopify.

    The page_id is the Wagtail integer page ID returned by GET /products/ or POST /products/.
    """
    try:
        page = (
            ProductPage.objects
            .select_related('locale')
            .prefetch_related('metafields', 'tagged_items__tag')
            .get(pk=page_id)
        )
        return page
    except ProductPage.DoesNotExist:
        return 404, {"detail": f"Product page {page_id} not found."}


@router.patch('/{page_id}', response={200: ProductOut, 404: ErrorSchema, 400: ErrorSchema}, summary="Update Product")
def update_product(request, page_id: int, data: ProductPatch):
    """
    Partially update a Product page. Only fields included in the request body are changed.

    Set publish=true to publish the page immediately. If sync_enabled=true on the page,
    publishing will automatically trigger an outbound sync to Shopify via the publish hook.

    To update content without syncing to Shopify, set sync_enabled=false before patching,
    or leave publish=false (default) to save as a draft only.

    To replace all tags, pass the full desired tags list. To clear tags, pass an empty list [].
    To replace all metafields, pass the full desired metafields list. To clear, pass [].

    Omit any field from the request body to leave it unchanged.
    """
    try:
        page = (
            ProductPage.objects
            .select_related('locale')
            .prefetch_related('metafields', 'tagged_items__tag')
            .get(pk=page_id)
        )
    except ProductPage.DoesNotExist:
        return 404, {"detail": f"Product page {page_id} not found."}

    if data.title is not None:
        page.title = data.title
    if data.shopify_id is not None:
        page.shopify_id = data.shopify_id
    if data.handle is not None:
        page.handle = data.handle
        page.slug = slugify(data.handle)
    if data.status is not None:
        page.status = data.status
    if data.vendor is not None:
        page.vendor = data.vendor
    if data.product_type is not None:
        page.product_type = data.product_type
    if data.sync_enabled is not None:
        page.sync_enabled = data.sync_enabled
    if data.seo_title is not None:
        page.seo_title = data.seo_title
    if data.search_description is not None:
        page.search_description = data.search_description
    if data.locale is not None:
        page.locale = resolve_locale(data.locale)
    if data.translation_of is not None:
        source = apply_translation_link(page, data.translation_of, ProductPage)
        inherit_shopify_id_from_source(page, source)
    if data.body is not None:
        page.body = json.dumps(data.body)

    if data.tags is not None:
        page.tags.set(*data.tags)

    if data.metafields is not None:
        page.metafields.all().delete()
        for mf in data.metafields:
            ProductPageMetafield.objects.create(
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


@router.delete('/{page_id}', response={204: None, 404: ErrorSchema}, summary="Delete Product")
def delete_product(request, page_id: int):
    """
    Delete a Product page from Wagtail. This does NOT delete the product in Shopify.

    Use this to remove a Wagtail page that should no longer be managed here.
    To archive a product in Shopify instead, use PATCH with status='ARCHIVED' and publish=true.

    This action is irreversible. The Shopify product remains untouched.
    """
    try:
        page = ProductPage.objects.get(pk=page_id)
        page.delete()
        return 204, None
    except ProductPage.DoesNotExist:
        return 404, {"detail": f"Product page {page_id} not found."}


@router.post('/{page_id}/push', response={200: SyncResultSchema, 404: ErrorSchema, 400: ErrorSchema}, summary="Push Product to Shopify")
def push_product(request, page_id: int):
    """
    Push a Product page's content from Wagtail to Shopify Admin API.

    Triggers an explicit outbound sync regardless of the page's publish state.
    Pushes: title, descriptionHtml (rendered StreamField body), vendor, product_type,
    tags, status, SEO fields, and all metafields.

    Requirements:
    - The page must have a shopify_id set (format: 'gid://shopify/Product/{id}').
    - A ShopConfig with a valid Shopify access token must exist.

    Returns success=false if Shopify returns errors or the token is invalid.
    Check the 'message' field for details on failures.
    Use POST /products/pull first if products have not yet been imported from Shopify.
    """
    try:
        page = ProductPage.objects.get(pk=page_id)
    except ProductPage.DoesNotExist:
        return 404, {"detail": f"Product page {page_id} not found."}

    if not page.shopify_id:
        return 400, {
            "detail": (
                "This product has no shopify_id. Set shopify_id before pushing, "
                "or use POST /products/pull/ to import from Shopify."
            )
        }

    try:
        success = sync_product_page(page)
        page.refresh_from_db()
        return {
            "success": success,
            "message": (
                "Product synced to Shopify successfully."
                if success
                else "Sync failed. Check server logs for GraphQL errors."
            ),
            "shopify_id": page.shopify_id,
        }
    except Exception as e:
        return 400, {"detail": f"Sync error: {str(e)}"}

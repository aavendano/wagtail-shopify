import json
from typing import List, Optional

from ninja import Router
from django.utils.text import slugify

from shopify_content.models import ProductPage
from shopify_content.models.product import ProductPageMetafield
from shopify_content.sync.outbound import sync_product_page
from shopify_content.sync.import_parents import resolve_shopify_import_parent

from ..sync import execute_pull
from ..schemas.product import ProductIn, ProductPatch, ProductOut
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
    response=List[ProductOut],
    summary="List Products",
    operation_id="list_products",
    description=capability_docstring("list_products"),
    openapi_extra=agent_openapi_extra("list_products"),
)
def list_products(
    request,
    live_only: bool = False,
    locale: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    # Enhanced filters
    live: Optional[bool] = None,
    updated_after: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    ordering: Optional[str] = None,
    collection_id: Optional[int] = None,
):
    """Discover products before read/update."""
    from django.db.models import Q
    from django.utils.dateparse import parse_datetime

    qs = ProductPage.objects.select_related('locale').prefetch_related(
        'metafields', 'tagged_items__tag', 'shopify_images'
    )
    if live_only:
        qs = qs.live()
    # New param: live (overrides live_only if explicitly set)
    if live is not None:
        qs = qs.live() if live else qs.filter(live=False)
    qs = filter_queryset_by_locale(qs, locale)
    if status:
        qs = qs.filter(status=status)
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
    if collection_id:
        # Filter products whose shopify_handle matches any handle stored in the collection.
        # Practical approach: filter by handle using CollectionPage's handle field.
        from shopify_content.models import CollectionPage
        try:
            collection = CollectionPage.objects.get(pk=collection_id)
            qs = qs.filter(handle=collection.handle)
        except CollectionPage.DoesNotExist:
            qs = qs.none()

    pages = list(qs[offset:offset + limit])
    return pages


@router.post(
    '/',
    response={201: ProductOut, 400: ErrorSchema},
    summary="Create Product",
    operation_id="create_product",
    description=capability_docstring("create_product"),
    openapi_extra=agent_openapi_extra("create_product"),
)
def create_product(request, data: ProductIn):
    """Create Wagtail product page."""
    try:
        parent = resolve_shopify_import_parent('products')
    except RuntimeError as e:
        return 400, {"detail": str(e)}

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
        page.tags.set(data.tags)

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


@router.get(
    '/pull',
    response={200: ImportResultSchema, 400: ErrorSchema},
    summary="Pull Products from Shopify (sync)",
    operation_id="pull_products_sync",
    description=capability_docstring("pull_products_sync"),
    openapi_extra=agent_openapi_extra("pull_products_sync"),
)
def pull_products_get(request):
    """GET alias for POST /products/pull."""
    return execute_pull('products')


@router.post(
    '/pull',
    response={200: ImportResultSchema, 400: ErrorSchema},
    summary="Pull Products from Shopify (sync)",
    operation_id="pull_products_sync_post",
    description=capability_docstring("pull_products_sync_post"),
    openapi_extra=agent_openapi_extra("pull_products_sync_post"),
)
def pull_products(request):
    """Import all products from Shopify synchronously."""
    return execute_pull('products')


@router.get(
    '/{page_id}',
    response={200: ProductOut, 404: ErrorSchema},
    summary="Get Product",
    operation_id="get_product",
    description=capability_docstring("get_product"),
    openapi_extra=agent_openapi_extra("get_product"),
)
def get_product(request, page_id: int):
    """Get single product by Wagtail page ID."""
    try:
        page = (
            ProductPage.objects
            .select_related('locale')
            .prefetch_related('metafields', 'tagged_items__tag', 'shopify_images')
            .get(pk=page_id)
        )
        return page
    except ProductPage.DoesNotExist:
        return 404, {"detail": f"Product page {page_id} not found."}


@router.patch(
    '/{page_id}',
    response={200: ProductOut, 404: ErrorSchema, 400: ErrorSchema},
    summary="Update Product",
    operation_id="update_product",
    description=capability_docstring("update_product"),
    openapi_extra=agent_openapi_extra("update_product"),
)
def update_product(request, page_id: int, data: ProductPatch):
    """Partially update product; publish=true triggers sync when enabled."""
    try:
        page = (
            ProductPage.objects
            .select_related('locale')
            .prefetch_related('metafields', 'tagged_items__tag', 'shopify_images')
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
        page.tags.set(data.tags)

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


@router.delete(
    '/{page_id}',
    response={204: None, 404: ErrorSchema},
    summary="Delete Product",
    operation_id="delete_product",
    description=capability_docstring("delete_product"),
    openapi_extra=agent_openapi_extra("delete_product"),
)
def delete_product(request, page_id: int):
    """Delete Wagtail product page only."""
    try:
        page = ProductPage.objects.get(pk=page_id)
        page.delete()
        return 204, None
    except ProductPage.DoesNotExist:
        return 404, {"detail": f"Product page {page_id} not found."}


@router.post(
    '/{page_id}/push',
    response={200: SyncResultSchema, 404: ErrorSchema, 400: ErrorSchema},
    summary="Push Product to Shopify",
    operation_id="push_product",
    description=capability_docstring("push_product"),
    openapi_extra=agent_openapi_extra("push_product"),
)
def push_product(request, page_id: int):
    """Push product content to Shopify Admin API."""
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

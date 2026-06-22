from typing import List, Optional

from django.core.exceptions import ValidationError
from django.utils.text import slugify
from ninja import Router

from shopify_content.models import ShopifyRootPage

from shopify_content.models import LocationPage
from shopify_content.models.location_page import LocationPageFAQ
from shopify_content.sync.outbound import sync_location_page
from shopify_content.sync.import_parents import resolve_shopify_import_parent

from ..schemas.location import LocationIn, LocationPatch, LocationOut
from ..schemas.common import SyncResultSchema, ErrorSchema
from ..openapi_agent import agent_openapi_extra, capability_docstring
from ..locale_utils import (
    resolve_locale,
    apply_translation_link,
    inherit_shopify_id_from_source,
    filter_queryset_by_locale,
)

router = Router()

_RICH_TEXT_FIELDS = (
    'intro',
    'content_2',
    'content_3',
    'brand_section_content',
    'map_content',
    'after_page_content',
)


def _apply_location_fields(page: LocationPage, data, *, is_create: bool = False):
    if is_create:
        page.titulo = data.titulo
        page.title = data.titulo
        page.shopify_id = data.shopify_id or ''
        slug = slugify(data.handle or data.titulo)
        page.handle = data.handle or slug
        page.slug = slug
        page.sync_enabled = data.sync_enabled if data.sync_enabled is not None else True
        page.seo_title = data.seo_title or ''
        page.search_description = data.search_description or ''
    elif data.titulo is not None:
        page.titulo = data.titulo
        page.title = data.titulo

    scalar_fields = [
        'subtitulo', 'country', 'state', 'city',
        'titulo_2', 'subtitulo_h2', 'titulo_3', 'subtitulo_3',
        'brand_section_title', 'brand_section_subtitle', 'map_title', 'shopify_locale',
    ]
    for field in scalar_fields:
        value = getattr(data, field, None)
        if is_create:
            setattr(page, field, value or '')
        elif value is not None:
            setattr(page, field, value)

    if not is_create:
        if data.shopify_id is not None:
            page.shopify_id = data.shopify_id
        if data.handle is not None:
            page.handle = data.handle
            page.slug = slugify(data.handle)
        if data.sync_enabled is not None:
            page.sync_enabled = data.sync_enabled
        if data.seo_title is not None:
            page.seo_title = data.seo_title
        if data.search_description is not None:
            page.search_description = data.search_description

    for field in _RICH_TEXT_FIELDS:
        value = getattr(data, field, None)
        if is_create:
            if value:
                setattr(page, field, value)
        elif value is not None:
            setattr(page, field, value)


def _replace_faqs(page: LocationPage, faqs):
    page.faqs.all().delete()
    for sort_order, faq in enumerate(faqs):
        LocationPageFAQ.objects.create(
            page=page,
            question=faq.question,
            answer=faq.answer,
            sort_order=sort_order,
        )


@router.get(
    '/',
    response=List[LocationOut],
    summary="List Location Pages",
    operation_id="list_locations",
    description=capability_docstring("list_locations"),
    openapi_extra=agent_openapi_extra("list_locations"),
)
def list_locations(
    request,
    live_only: bool = False,
    locale: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
):
    """Discover Wagtail location pages before push."""
    qs = LocationPage.objects.select_related('locale').prefetch_related('faqs')
    if live_only:
        qs = qs.live()
    qs = filter_queryset_by_locale(qs, locale)
    return list(qs[offset:offset + limit])


@router.post(
    '/',
    response={201: LocationOut, 400: ErrorSchema},
    summary="Create Location Page",
    operation_id="create_location",
    description=capability_docstring("create_location"),
    openapi_extra=agent_openapi_extra("create_location"),
)
def create_location(request, data: LocationIn):
    """Create Wagtail location page for metaobject push."""
    # #region agent log
    from shopify_content.publish_debug import debug_log

    debug_log(
        "F",
        "locations.py:create_location",
        "create_location requested",
        {
            "titulo": data.titulo[:80],
            "parent_page_id": data.parent_page_id,
            "city": data.city or "",
        },
    )
    # #endregion
    try:
        parent = resolve_shopify_import_parent(
            'locations',
            explicit_parent_id=data.parent_page_id,
        )
    except RuntimeError as e:
        # #region agent log
        debug_log(
            "F",
            "locations.py:create_location",
            "parent resolution failed",
            {"detail": str(e), "parent_page_id": data.parent_page_id},
        )
        # #endregion
        return 400, {"detail": str(e)}

    if not isinstance(parent, ShopifyRootPage):
        detail = (
            f'Parent page id={parent.pk} is a {type(parent).__name__}, '
            'not a ShopifyRootPage. Use the Local US root (slug=local-us) or pass parent_page_id.'
        )
        # #region agent log
        debug_log(
            "F",
            "locations.py:create_location",
            "invalid parent page type",
            {"parent_id": parent.pk, "parent_type": type(parent).__name__},
        )
        # #endregion
        return 400, {"detail": detail}

    # #region agent log
    debug_log(
        "F",
        "locations.py:create_location",
        "parent resolved",
        {"parent_id": parent.pk, "parent_slug": parent.slug, "parent_title": parent.title},
    )
    # #endregion

    try:
        page = LocationPage(locale=resolve_locale(data.locale))
        _apply_location_fields(page, data, is_create=True)

        source = apply_translation_link(page, data.translation_of, LocationPage)
        inherit_shopify_id_from_source(page, source)

        parent.add_child(instance=page)

        if data.faqs:
            _replace_faqs(page, data.faqs)

        page.refresh_from_db()
    except ValidationError as exc:
        # #region agent log
        debug_log(
            "F",
            "locations.py:create_location",
            "validation failed during create",
            {"detail": str(exc)},
        )
        # #endregion
        return 400, {"detail": str(exc)}
    except Exception as exc:
        # #region agent log
        import traceback

        debug_log(
            "F",
            "locations.py:create_location",
            "unexpected create failure",
            {
                "exc_type": type(exc).__name__,
                "exc": str(exc),
                "traceback": traceback.format_exc(),
            },
        )
        # #endregion
        raise

    # #region agent log
    debug_log(
        "F",
        "locations.py:create_location",
        "create succeeded",
        {"page_id": page.pk, "parent_id": parent.pk, "slug": page.slug},
    )
    # #endregion
    return 201, page


@router.get(
    '/{page_id}',
    response={200: LocationOut, 404: ErrorSchema},
    summary="Get Location Page",
    operation_id="get_location",
    description=capability_docstring("get_location"),
    openapi_extra=agent_openapi_extra("get_location"),
)
def get_location(request, page_id: int):
    """Get single location by Wagtail page ID."""
    try:
        page = (
            LocationPage.objects
            .select_related('locale')
            .prefetch_related('faqs')
            .get(pk=page_id)
        )
        return page
    except LocationPage.DoesNotExist:
        return 404, {"detail": f"Location page {page_id} not found."}


@router.patch(
    '/{page_id}',
    response={200: LocationOut, 404: ErrorSchema, 400: ErrorSchema},
    summary="Update Location Page",
    operation_id="update_location",
    description=capability_docstring("update_location"),
    openapi_extra=agent_openapi_extra("update_location"),
)
def update_location(request, page_id: int, data: LocationPatch):
    """Partially update location; publish=true optional before push."""
    try:
        page = (
            LocationPage.objects
            .select_related('locale')
            .prefetch_related('faqs')
            .get(pk=page_id)
        )
    except LocationPage.DoesNotExist:
        return 404, {"detail": f"Location page {page_id} not found."}

    if data.locale is not None:
        page.locale = resolve_locale(data.locale)
    if data.translation_of is not None:
        source = apply_translation_link(page, data.translation_of, LocationPage)
        inherit_shopify_id_from_source(page, source)

    _apply_location_fields(page, data, is_create=False)

    if data.faqs is not None:
        _replace_faqs(page, data.faqs)

    if data.publish:
        # #region agent log
        from shopify_content.publish_debug import debug_log

        debug_log(
            "A",
            "locations.py:update_location",
            "API publish requested",
            {"page_id": page_id, "slug": page.slug, "titulo": page.titulo[:80]},
        )
        # #endregion
        try:
            revision = page.save_revision()
            revision.publish()
        except Exception as exc:
            # #region agent log
            import traceback

            debug_log(
                "A",
                "locations.py:update_location",
                "revision.publish failed",
                {
                    "page_id": page_id,
                    "exc_type": type(exc).__name__,
                    "exc": str(exc),
                    "traceback": traceback.format_exc(),
                },
            )
            # #endregion
            raise
    else:
        page.save()

    page.refresh_from_db()
    # #region agent log
    if data.publish:
        from shopify_content.publish_debug import debug_log

        debug_log(
            "D",
            "locations.py:update_location",
            "publish succeeded, returning LocationOut",
            {"page_id": page_id, "live": page.live},
        )
    # #endregion
    return page


@router.delete(
    '/{page_id}',
    response={204: None, 404: ErrorSchema},
    summary="Delete Location Page",
    operation_id="delete_location",
    description=capability_docstring("delete_location"),
    openapi_extra=agent_openapi_extra("delete_location"),
)
def delete_location(request, page_id: int):
    """Delete Wagtail location page only."""
    try:
        page = LocationPage.objects.get(pk=page_id)
        page.delete()
        return 204, None
    except LocationPage.DoesNotExist:
        return 404, {"detail": f"Location page {page_id} not found."}


@router.post(
    '/{page_id}/push',
    response={200: SyncResultSchema, 404: ErrorSchema, 400: ErrorSchema},
    summary="Push Location Page to Shopify",
    operation_id="push_location",
    description=capability_docstring("push_location"),
    openapi_extra=agent_openapi_extra("push_location"),
)
def push_location(request, page_id: int):
    """Push location to Shopify metaobject local_page."""
    try:
        page = LocationPage.objects.get(pk=page_id)
    except LocationPage.DoesNotExist:
        return 404, {"detail": f"Location page {page_id} not found."}

    try:
        success, message = sync_location_page(page)
        page.refresh_from_db()
        return {
            "success": success,
            "message": message,
            "shopify_id": page.shopify_id or None,
        }
    except Exception as e:
        return 400, {"detail": f"Sync error: {str(e)}"}

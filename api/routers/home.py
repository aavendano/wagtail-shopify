from typing import List, Optional

from django.core.exceptions import ValidationError
from ninja import Router

from shopify_content.models import HomePage, ShopifyRootPage
from shopify_content.home_sections_normalization import incoming_sections_from_api
from shopify_content.home_serialization import sections_json_to_stream_data
from shopify_content.home_slug import home_page_handle
from shopify_content.richtext_sanitize import sanitize_richtext_html
from shopify_content.sync.import_parents import resolve_shopify_import_parent
from shopify_content.sync.outbound import sync_home_page

from ..schemas.home import HomeIn, HomePatch, HomeOut
from ..schemas.common import SyncResultSchema, ErrorSchema
from ..openapi_agent import agent_openapi_extra, capability_docstring
from ..locale_utils import (
    resolve_locale,
    apply_translation_link,
    filter_queryset_by_locale,
)

router = Router()

_RICH_TEXT_FIELDS = ('hero_body',)


def _apply_home_slug(page: HomePage) -> None:
    canonical = home_page_handle(page)
    if canonical:
        page.slug = canonical
        page.handle = canonical


def _apply_home_fields(page: HomePage, data, *, is_create: bool = False):
    if is_create:
        page.hero_heading = data.hero_heading
        page.title = data.hero_heading
        page.shopify_id = data.shopify_id or ''
        page.sync_enabled = data.sync_enabled if data.sync_enabled is not None else True
        page.seo_title = data.seo_title or ''
        page.search_description = data.search_description or ''
        page.sections_json = incoming_sections_from_api(data, is_create=True)
        page.body = sections_json_to_stream_data(page.sections_json)
    elif data.hero_heading is not None:
        page.hero_heading = data.hero_heading
        page.title = data.hero_heading

    scalar_fields = [
        'hero_eyebrow',
        'hero_subheading',
        'hero_primary_cta_label',
        'hero_primary_cta_url',
        'hero_secondary_cta_label',
        'hero_secondary_cta_url',
        'hero_image_url',
        'shopify_locale',
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
        if data.sync_enabled is not None:
            page.sync_enabled = data.sync_enabled
        if data.seo_title is not None:
            page.seo_title = data.seo_title
        if data.search_description is not None:
            page.search_description = data.search_description
        sections_payload = incoming_sections_from_api(
            data,
            existing=page.sections_json,
            is_create=False,
        )
        if sections_payload is not None:
            page.sections_json = sections_payload
            page.body = sections_json_to_stream_data(sections_payload)

    for field in _RICH_TEXT_FIELDS:
        value = getattr(data, field, None)
        if is_create:
            if value:
                setattr(page, field, sanitize_richtext_html(value))
        elif value is not None:
            setattr(page, field, sanitize_richtext_html(value))

    _apply_home_slug(page)


@router.get(
    '/',
    response=List[HomeOut],
    summary="List Home Pages",
    operation_id="list_home_pages",
    description=capability_docstring("list_home_pages"),
    openapi_extra=agent_openapi_extra("list_home_pages"),
)
def list_home_pages(
    request,
    live_only: bool = False,
    locale: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
):
    """Discover Wagtail home pages before push."""
    qs = HomePage.objects.select_related('locale')
    if live_only:
        qs = qs.live()
    qs = filter_queryset_by_locale(qs, locale)
    return list(qs[offset:offset + limit])


@router.post(
    '/',
    response={201: HomeOut, 400: ErrorSchema},
    summary="Create Home Page",
    operation_id="create_home_page",
    description=capability_docstring("create_home_page"),
    openapi_extra=agent_openapi_extra("create_home_page"),
)
def create_home_page(request, data: HomeIn):
    """Create Wagtail home page for metaobject push."""
    try:
        parent = resolve_shopify_import_parent(
            'home',
            explicit_parent_id=data.parent_page_id,
        )
    except RuntimeError as e:
        return 400, {"detail": str(e)}

    if not isinstance(parent, ShopifyRootPage):
        detail = (
            f'Parent page id={parent.pk} is a {type(parent).__name__}, '
            'not a ShopifyRootPage. Use the CMS Home root (slug=cms-home) or pass parent_page_id.'
        )
        return 400, {"detail": detail}

    try:
        page = HomePage(locale=resolve_locale(data.locale))
        _apply_home_fields(page, data, is_create=True)

        if data.translation_of is not None:
            apply_translation_link(page, data.translation_of, HomePage)

        parent.add_child(instance=page)
        page.refresh_from_db()
    except ValidationError as exc:
        return 400, {"detail": str(exc)}

    return 201, page


@router.get(
    '/{page_id}',
    response={200: HomeOut, 404: ErrorSchema},
    summary="Get Home Page",
    operation_id="get_home_page",
    description=capability_docstring("get_home_page"),
    openapi_extra=agent_openapi_extra("get_home_page"),
)
def get_home_page(request, page_id: int):
    """Get single home page by Wagtail page ID."""
    try:
        page = HomePage.objects.select_related('locale').get(pk=page_id)
        return page
    except HomePage.DoesNotExist:
        return 404, {"detail": f"Home page {page_id} not found."}


@router.patch(
    '/{page_id}',
    response={200: HomeOut, 404: ErrorSchema, 400: ErrorSchema},
    summary="Update Home Page",
    operation_id="update_home_page",
    description=capability_docstring("update_home_page"),
    openapi_extra=agent_openapi_extra("update_home_page"),
)
def update_home_page(request, page_id: int, data: HomePatch):
    """Partially update home page; publish=true optional before push."""
    try:
        page = HomePage.objects.select_related('locale').get(pk=page_id)
    except HomePage.DoesNotExist:
        return 404, {"detail": f"Home page {page_id} not found."}

    if data.locale is not None:
        page.locale = resolve_locale(data.locale)
    if data.translation_of is not None:
        apply_translation_link(page, data.translation_of, HomePage)

    _apply_home_fields(page, data, is_create=False)

    try:
        page.full_clean()
    except ValidationError as exc:
        return 400, {"detail": str(exc)}

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
    summary="Delete Home Page",
    operation_id="delete_home_page",
    description=capability_docstring("delete_home_page"),
    openapi_extra=agent_openapi_extra("delete_home_page"),
)
def delete_home_page(request, page_id: int):
    """Delete Wagtail home page only."""
    try:
        page = HomePage.objects.get(pk=page_id)
        page.delete()
        return 204, None
    except HomePage.DoesNotExist:
        return 404, {"detail": f"Home page {page_id} not found."}


@router.post(
    '/{page_id}/push',
    response={200: SyncResultSchema, 404: ErrorSchema, 400: ErrorSchema},
    summary="Push Home Page to Shopify",
    operation_id="push_home_page",
    description=capability_docstring("push_home_page"),
    openapi_extra=agent_openapi_extra("push_home_page"),
)
def push_home_page(request, page_id: int):
    """Push home page to Shopify metaobject home_page."""
    try:
        page = HomePage.objects.get(pk=page_id)
    except HomePage.DoesNotExist:
        return 404, {"detail": f"Home page {page_id} not found."}

    try:
        success, message = sync_home_page(page)
        page.refresh_from_db()
        return {
            "success": success,
            "message": message,
            "shopify_id": page.shopify_id or None,
        }
    except Exception as e:
        return 400, {"detail": f"Sync error: {str(e)}"}

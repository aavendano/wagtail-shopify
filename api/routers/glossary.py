from typing import List, Optional, Union

from django.core.exceptions import ValidationError
from django.utils.text import slugify
from ninja import Query, Router
from ninja.responses import Response

from shopify_content.models import GlossaryTermPage, ShopifyRootPage
from shopify_content.sync.outbound import sync_glossary_term_page
from shopify_content.sync.import_parents import resolve_shopify_import_parent
from shopify_content.glossary_locale_utils import wagtail_locale_code_for_glossary

from ..sync import execute_pull
from ..schemas.glossary import (
    GlossaryTermIn,
    GlossaryTermListOut,
    GlossaryTermOut,
    GlossaryTermPatch,
)
from ..schemas.common import SyncResultSchema, ImportResultSchema, ErrorSchema
from ..openapi_agent import agent_openapi_extra, capability_docstring
from ..locale_utils import (
    resolve_locale,
    apply_translation_link,
    inherit_shopify_id_from_source,
    filter_queryset_by_locale,
)

router = Router()


def _serialize_links(links):
    if not links:
        return []
    result = []
    for link in links:
        if hasattr(link, 'model_dump'):
            result.append(link.model_dump(exclude_none=True))
        elif hasattr(link, 'dict'):
            result.append(link.dict(exclude_none=True))
        else:
            result.append(link)
    return result


def _validation_detail(exc: ValidationError) -> str:
    if hasattr(exc, 'messages'):
        return '; '.join(str(message) for message in exc.messages)
    return str(exc)


def _apply_related_links(page: GlossaryTermPage, data, *, persist_revision: bool):
    """Persist related_links as typed manual FKs once the page has a primary key."""
    if data.related_links is None:
        return
    from shopify_content.semantic_links.manual_links import apply_manual_related_links

    apply_manual_related_links(
        page,
        _serialize_links(data.related_links),
        persist_revision=persist_revision,
    )


def _apply_glossary_fields(page: GlossaryTermPage, data, *, is_create: bool = False):
    if is_create:
        page.term = data.term
        page.title = data.term
        page.shopify_id = data.shopify_id or ''
        slug = slugify(data.handle or data.term)
        page.handle = data.handle or slug
        page.slug = slug
        page.sync_enabled = data.sync_enabled if data.sync_enabled is not None else True
        page.locale_code = data.locale_code or 'en'
        page.seo_title = data.seo_title or ''
        page.search_description = data.search_description or ''
        if data.image_id:
            page.image_id = data.image_id
        page.image_alt_text = data.image_alt_text or ''
        page.shopify_image_id = data.shopify_image_id or ''
        page.external_links = _serialize_links(data.external_links)
        page.synonyms = data.synonyms or []
        page.same_as = data.same_as or []
        if data.definition:
            page.definition = data.definition
    elif data.term is not None:
        page.term = data.term
        page.title = data.term

    if not is_create:
        if data.shopify_id is not None:
            page.shopify_id = data.shopify_id
        if data.handle is not None:
            page.handle = data.handle
            page.slug = slugify(data.handle)
        if data.sync_enabled is not None:
            page.sync_enabled = data.sync_enabled
        if data.locale_code is not None:
            page.locale_code = data.locale_code
        if data.external_links is not None:
            page.external_links = _serialize_links(data.external_links)
        if data.synonyms is not None:
            page.synonyms = data.synonyms
        if data.same_as is not None:
            page.same_as = data.same_as
        if data.definition is not None:
            page.definition = data.definition
        if data.image_id is not None:
            page.image_id = data.image_id
        if data.image_alt_text is not None:
            page.image_alt_text = data.image_alt_text
        if data.shopify_image_id is not None:
            page.shopify_image_id = data.shopify_image_id
        if data.seo_title is not None:
            page.seo_title = data.seo_title
        if data.search_description is not None:
            page.search_description = data.search_description


FULL_LIST_QUERY_DESCRIPTION = (
    "When false (default), return a compact list of terms "
    "(id, term, handle, slug, shopify_id, locale_code, live, last_synced_at). "
    "When true, return full GlossaryTermOut including definition HTML, links, and SEO. "
    "Prefer false; use get_glossary_term for a single full record."
)


@router.get(
    '/',
    response=Union[List[GlossaryTermListOut], List[GlossaryTermOut]],
    summary="List Glossary Terms",
    operation_id="list_glossary_terms",
    description=capability_docstring("list_glossary_terms"),
    openapi_extra=agent_openapi_extra("list_glossary_terms"),
)
def list_glossary_terms(
    request,
    live_only: bool = False,
    locale: Optional[str] = None,
    locale_code: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    full: bool = Query(False, description=FULL_LIST_QUERY_DESCRIPTION),
):
    """Discover Wagtail glossary terms before push."""
    qs = GlossaryTermPage.objects.select_related('locale', 'image')
    if live_only:
        qs = qs.live()
    qs = filter_queryset_by_locale(qs, locale)
    if locale_code:
        qs = qs.filter(locale_code=locale_code)
    pages = list(qs[offset:offset + limit])
    schema_cls = GlossaryTermOut if full else GlossaryTermListOut
    # Return JsonResponse so Ninja does not coerce the Union to the first schema.
    return Response([schema_cls.from_orm(page) for page in pages])


@router.post(
    '/pull',
    response={200: ImportResultSchema, 400: ErrorSchema},
    summary="Pull Glossary Terms from Shopify (sync)",
    operation_id="pull_glossary_sync",
    description=capability_docstring("pull_glossary_sync"),
    openapi_extra=agent_openapi_extra("pull_glossary_sync"),
)
def pull_glossary(request):
    """Import glossary_term metaobjects from Shopify synchronously."""
    return execute_pull('glossary')


@router.post(
    '/',
    response={201: GlossaryTermOut, 400: ErrorSchema},
    summary="Create Glossary Term",
    operation_id="create_glossary_term",
    description=capability_docstring("create_glossary_term"),
    openapi_extra=agent_openapi_extra("create_glossary_term"),
)
def create_glossary_term(request, data: GlossaryTermIn):
    """Create Wagtail glossary term page for metaobject push."""
    try:
        parent = resolve_shopify_import_parent(
            'glossary',
            explicit_parent_id=data.parent_page_id,
        )
    except RuntimeError as e:
        return 400, {"detail": str(e)}

    if not isinstance(parent, ShopifyRootPage):
        detail = (
            f'Parent page id={parent.pk} is a {type(parent).__name__}, '
            'not a ShopifyRootPage. Use the Glossary root (slug=glossary) or pass parent_page_id.'
        )
        return 400, {"detail": detail}

    try:
        wagtail_locale = data.locale
        if not wagtail_locale and data.locale_code:
            wagtail_locale = wagtail_locale_code_for_glossary(data.locale_code)
        page = GlossaryTermPage(locale=resolve_locale(wagtail_locale))
        _apply_glossary_fields(page, data, is_create=True)

        source = apply_translation_link(page, data.translation_of, GlossaryTermPage)
        inherit_shopify_id_from_source(page, source)

        parent.add_child(instance=page)
        page.refresh_from_db()
        _apply_related_links(page, data, persist_revision=True)
        page.refresh_from_db()
    except ValidationError as exc:
        return 400, {"detail": _validation_detail(exc)}

    return 201, page


@router.get(
    '/{page_id}',
    response={200: GlossaryTermOut, 404: ErrorSchema},
    summary="Get Glossary Term",
    operation_id="get_glossary_term",
    description=capability_docstring("get_glossary_term"),
    openapi_extra=agent_openapi_extra("get_glossary_term"),
)
def get_glossary_term(request, page_id: int):
    """Get single glossary term by Wagtail page ID."""
    try:
        page = GlossaryTermPage.objects.select_related('locale', 'image').get(pk=page_id)
        return page
    except GlossaryTermPage.DoesNotExist:
        return 404, {"detail": f"Glossary term page {page_id} not found."}


@router.patch(
    '/{page_id}',
    response={200: GlossaryTermOut, 404: ErrorSchema, 400: ErrorSchema},
    summary="Update Glossary Term",
    operation_id="update_glossary_term",
    description=capability_docstring("update_glossary_term"),
    openapi_extra=agent_openapi_extra("update_glossary_term"),
)
def update_glossary_term(request, page_id: int, data: GlossaryTermPatch):
    """Partially update glossary term; publish=true optional before push."""
    try:
        page = GlossaryTermPage.objects.select_related('locale', 'image').get(pk=page_id)
    except GlossaryTermPage.DoesNotExist:
        return 404, {"detail": f"Glossary term page {page_id} not found."}

    if data.locale is not None:
        page.locale = resolve_locale(data.locale)
    elif data.locale_code is not None:
        page.locale = resolve_locale(wagtail_locale_code_for_glossary(data.locale_code))
    if data.translation_of is not None:
        source = apply_translation_link(page, data.translation_of, GlossaryTermPage)
        inherit_shopify_id_from_source(page, source)

    _apply_glossary_fields(page, data, is_create=False)

    # Persist scalar fields first, then manual FKs, then publish so enrich keeps manuals.
    try:
        if data.publish:
            page.save()
            _apply_related_links(page, data, persist_revision=False)
            revision = page.save_revision()
            revision.publish()
        else:
            page.save()
            _apply_related_links(
                page,
                data,
                persist_revision=bool(page.live),
            )
    except ValidationError as exc:
        return 400, {"detail": _validation_detail(exc)}

    page.refresh_from_db()
    return page


@router.delete(
    '/{page_id}',
    response={204: None, 404: ErrorSchema},
    summary="Delete Glossary Term",
    operation_id="delete_glossary_term",
    description=capability_docstring("delete_glossary_term"),
    openapi_extra=agent_openapi_extra("delete_glossary_term"),
)
def delete_glossary_term(request, page_id: int):
    """Delete Wagtail glossary term page only."""
    try:
        page = GlossaryTermPage.objects.get(pk=page_id)
        page.delete()
        return 204, None
    except GlossaryTermPage.DoesNotExist:
        return 404, {"detail": f"Glossary term page {page_id} not found."}


@router.post(
    '/{page_id}/push',
    response={200: SyncResultSchema, 404: ErrorSchema, 400: ErrorSchema},
    summary="Push Glossary Term to Shopify",
    operation_id="push_glossary_term",
    description=capability_docstring("push_glossary_term"),
    openapi_extra=agent_openapi_extra("push_glossary_term"),
)
def push_glossary_term(request, page_id: int):
    """Push glossary term to Shopify metaobject glossary_term."""
    try:
        page = GlossaryTermPage.objects.get(pk=page_id)
    except GlossaryTermPage.DoesNotExist:
        return 404, {"detail": f"Glossary term page {page_id} not found."}

    try:
        success, message = sync_glossary_term_page(page)
        page.refresh_from_db()
        return {
            "success": success,
            "message": message,
            "shopify_id": page.shopify_id or None,
        }
    except Exception as e:
        return 400, {"detail": f"Sync error: {str(e)}"}

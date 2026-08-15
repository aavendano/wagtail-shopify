from ninja import Router

from shopify_content.semantic_links.service import (
    PAGE_TYPE_KEYS,
    PAGE_TYPE_QUERY_FIELDS,
    assemble_preview_query_text,
    extract_page_content,
    page_type_key_for,
    suggest_related_with_scores,
    SemanticSuggestUnavailable,
)

from ..locale_utils import resolve_locale
from ..openapi_agent import agent_openapi_extra, capability_docstring
from ..schemas.common import ErrorSchema
from ..schemas.semantic_links import SuggestRelatedIn, SuggestRelatedOut

router = Router()

_CONTENT_FIELD_NAMES = (
    'title',
    'seo_title',
    'search_description',
    'definition',
    'summary',
    'body',
    'description',
    'synonyms',
    'vendor',
    'product_type',
    'author',
)


def _content_fields(data: SuggestRelatedIn) -> dict:
    fields = {}
    for name in _CONTENT_FIELD_NAMES:
        value = getattr(data, name, None)
        if value is not None:
            fields[name] = value
    return fields


def _has_text_origin(data: SuggestRelatedIn) -> bool:
    if data.text and str(data.text).strip():
        return True
    return bool(_content_fields(data))


@router.post(
    '/suggest',
    response={200: SuggestRelatedOut, 400: ErrorSchema, 404: ErrorSchema, 503: ErrorSchema},
    summary="Suggest related pages (preview)",
    operation_id="suggest_related_pages",
    description=capability_docstring("suggest_related_pages"),
    openapi_extra=agent_openapi_extra("suggest_related_pages"),
)
def suggest_related_pages(request, data: SuggestRelatedIn):
    """Preview semantically related pages; does not persist links."""
    text_origin = _has_text_origin(data)
    if data.page_id is not None and text_origin:
        return 400, {
            'detail': 'Provide page_id or text/fields, not both.',
        }
    if data.page_id is None and not text_origin:
        return 400, {
            'detail': 'Provide page_id or text/fields as the query origin.',
        }

    from wagtail.models import Page

    locale = resolve_locale(data.locale)
    exclude_pks = []
    page_type = data.page_type

    if data.page_id is not None:
        try:
            page = Page.objects.get(pk=data.page_id)
        except Page.DoesNotExist:
            return 404, {'detail': f'page_id {data.page_id} not found.'}
        inferred = page_type_key_for(page)
        if inferred is None:
            return 400, {
                'detail': (
                    f'page_id {data.page_id} is not a product, collection, '
                    'article, or glossary term.'
                ),
            }
        if page_type and page_type != inferred:
            return 400, {
                'detail': (
                    f'page_type {page_type!r} does not match page_id type {inferred!r}.'
                ),
            }
        page_type = inferred
        content = extract_page_content(page)
        exclude_pks.append(data.page_id)
    else:
        if not page_type:
            return 400, {
                'detail': 'page_type is required when suggesting from text or fields.',
            }
        if page_type not in PAGE_TYPE_QUERY_FIELDS:
            return 400, {'detail': f'Invalid page_type {page_type!r}.'}
        content = assemble_preview_query_text(
            page_type,
            text=data.text,
            fields=_content_fields(data),
        )
        if not content.strip():
            return 400, {'detail': 'Query text is empty after assembling fields.'}

    if data.exclude_page_id is not None:
        exclude_pks.append(data.exclude_page_id)

    allowed_types = list(data.types) if data.types else list(PAGE_TYPE_KEYS)
    invalid = [item for item in allowed_types if item not in PAGE_TYPE_KEYS]
    if invalid:
        return 400, {'detail': f'Invalid types: {invalid!r}.'}

    try:
        grouped = suggest_related_with_scores(
            content=content,
            locale_id=locale.pk,
            allowed_types=allowed_types,
            exclude_pks=exclude_pks,
            limit_per_type=data.limit_per_type,
        )
    except SemanticSuggestUnavailable as exc:
        return 503, {'detail': str(exc)}

    return {
        'locale': data.locale,
        'page_type': page_type,
        'limit_per_type': data.limit_per_type,
        'candidates': grouped,
    }

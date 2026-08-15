"""Semantic internal link generation and persistence."""

import logging
from contextlib import contextmanager, nullcontext

from django.conf import settings
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.signals import page_published

from shopify_content.models.blog import ArticlePage
from shopify_content.models.collection import CollectionPage
from shopify_content.models.glossary import GlossaryTermPage
from shopify_content.models.product import ProductPage
from shopify_content.models.semantic_links import (
    count_auto_semantic_links,
    delete_auto_semantic_links,
    get_typed_link_model,
    inbound_related_product_sources,
    manual_related_page_pks,
    relation_for_page_type,
)
from shopify_content.semantic_links.constants import (
    SEMANTIC_LINK_RELATION_NAMES,
)
from shopify_content.semantic_links.serialization import (
    LINKABLE_PAGE_TYPES,
    serialize_semantic_links,
)

from shopify_content.indexing import (
    ARTICLE_INDEX_FIELDS,
    COLLECTION_INDEX_FIELDS,
    GLOSSARY_INDEX_FIELDS,
    PRODUCT_INDEX_FIELDS,
)

logger = logging.getLogger(__name__)

SEMANTIC_LINK_PAGE_TYPES = LINKABLE_PAGE_TYPES
PAGE_TYPE_KEYS = ('product', 'collection', 'article', 'glossary')
PAGE_TYPE_QUERY_FIELDS = {
    'product': PRODUCT_INDEX_FIELDS,
    'collection': COLLECTION_INDEX_FIELDS,
    'article': ARTICLE_INDEX_FIELDS,
    'glossary': GLOSSARY_INDEX_FIELDS,
}
SUGGEST_FETCH_CAP = 200
SUGGEST_LIMIT_PER_TYPE_DEFAULT = 20
SUGGEST_LIMIT_PER_TYPE_MAX = 100


class SemanticSuggestUnavailable(Exception):
    """Raised when PageIndex / pgvector cannot serve a preview search."""


def is_semantic_linkable_page(page) -> bool:
    return isinstance(page.specific, SEMANTIC_LINK_PAGE_TYPES)


def page_type_key_for(page) -> str | None:
    specific = page.specific if isinstance(page, Page) else page
    if isinstance(specific, ProductPage):
        return 'product'
    if isinstance(specific, CollectionPage):
        return 'collection'
    if isinstance(specific, ArticlePage):
        return 'article'
    if isinstance(specific, GlossaryTermPage):
        return 'glossary'
    return None


def extract_page_content(page) -> str:
    """Build searchable text from a page (mirrors index fields + StreamFields)."""
    specific = page.specific
    parts: list[str] = []

    def add(value):
        text = str(value or '').strip()
        if text:
            parts.append(text)

    add(getattr(specific, 'title', None))
    add(getattr(specific, 'seo_title', None))
    add(getattr(specific, 'search_description', None))
    add(getattr(specific, 'summary', None))
    add(getattr(specific, 'author', None))
    add(getattr(specific, 'term', None))
    add(getattr(specific, 'definition', None))
    add(getattr(specific, 'vendor', None))
    add(getattr(specific, 'product_type', None))

    synonyms = getattr(specific, 'synonyms', None)
    if synonyms:
        if isinstance(synonyms, list):
            add(', '.join(str(s) for s in synonyms if s))
        else:
            add(synonyms)

    for field in specific._meta.fields:
        if isinstance(field, StreamField):
            value = getattr(specific, field.name, None)
            if value:
                add(str(value))

    return '\n\n'.join(parts)


def assemble_preview_query_text(
    page_type: str,
    *,
    text: str | None = None,
    fields: dict | None = None,
) -> str:
    """Build query text from free text and/or index fields for a page type."""
    parts: list[str] = []
    if text and str(text).strip():
        parts.append(str(text).strip())
    field_names = PAGE_TYPE_QUERY_FIELDS.get(page_type) or ()
    values = fields or {}
    for name in field_names:
        value = values.get(name)
        if value is None:
            continue
        if isinstance(value, list):
            joined = ', '.join(str(item) for item in value if item)
            if joined:
                parts.append(joined)
            continue
        rendered = str(value).strip()
        if rendered:
            parts.append(rendered)
    return '\n\n'.join(parts)


def is_eligible_semantic_candidate(
    page,
    *,
    locale_id: int,
    exclude_pks: set[int] | None = None,
    allowed_types: set[str] | None = None,
) -> str | None:
    """Return page type key if the page passes locale/live/ACTIVE filters."""
    if exclude_pks and page.pk in exclude_pks:
        return None
    if not page.live:
        return None
    if page.locale_id != locale_id:
        return None
    key = page_type_key_for(page)
    if key is None:
        return None
    if allowed_types is not None and key not in allowed_types:
        return None
    specific = page.specific
    if isinstance(specific, ProductPage) and specific.status != 'ACTIVE':
        return None
    return key


def classify_and_cap(pages, *, source_page, limit_per_type: int) -> dict[str, list[Page]]:
    """Group candidate pages by type and apply per-type caps with locale filtering."""
    grouped: dict[str, list[Page]] = {key: [] for key in PAGE_TYPE_KEYS}
    exclude = {source_page.pk}

    for page in pages:
        key = is_eligible_semantic_candidate(
            page,
            locale_id=source_page.locale_id,
            exclude_pks=exclude,
        )
        if key is None:
            continue
        if len(grouped[key]) >= limit_per_type:
            continue
        grouped[key].append(page)

    return grouped


def _page_pk_from_document(document) -> int | None:
    metadata = getattr(document, 'metadata', None) or {}
    pk = metadata.get('pk')
    if pk is not None:
        try:
            return int(pk)
        except (TypeError, ValueError):
            return None
    key = str(getattr(document, 'document_key', '') or '')
    parts = key.split(':')
    if len(parts) >= 2:
        try:
            return int(parts[1])
        except ValueError:
            return None
    return None


def _candidate_payload(page, type_key: str, score: float) -> dict:
    specific = page.specific
    handle = getattr(specific, 'handle', None) or getattr(specific, 'slug', '') or ''
    title = getattr(specific, 'term', None) or specific.title
    return {
        'id': specific.pk,
        'type': type_key,
        'title': title,
        'handle': handle,
        'score': score,
    }


def suggest_related_with_scores(
    *,
    content: str,
    locale_id: int,
    allowed_types: list[str] | None,
    exclude_pks: list[int],
    limit_per_type: int,
) -> dict[str, list[dict]]:
    """
    Preview-only nearest neighbors with similarity scores.

    Does not persist FKs. Cap is the request ``limit_per_type``, not
    SEMANTIC_LINKS_LIMIT_PER_TYPE.
    """
    grouped: dict[str, list[dict]] = {key: [] for key in PAGE_TYPE_KEYS}
    if not (content or '').strip():
        return grouped
    if limit_per_type <= 0:
        return grouped
    if not getattr(settings, 'WAGTAIL_AI_PGVECTOR', False):
        raise SemanticSuggestUnavailable(
            'Vector index is disabled (WAGTAIL_AI_PGVECTOR).'
        )

    from django_ai_core.contrib.index.base import registry

    if 'PageIndex' not in registry.list():
        raise SemanticSuggestUnavailable(
            'PageIndex is not registered. Set GEMINI_API_KEY and WAGTAIL_AI_PGVECTOR.'
        )

    allowed = set(allowed_types or PAGE_TYPE_KEYS)
    exclude = set(exclude_pks)
    overfetch = max(1, int(getattr(settings, 'SEMANTIC_LINKS_TYPE_OVERFETCH', 10)))
    fetch = min(
        SUGGEST_FETCH_CAP,
        max(limit_per_type, limit_per_type * max(len(allowed), 1) * overfetch),
    )

    index = registry.get('PageIndex')()
    documents = list(index.search_documents(content)[:fetch])
    seen_pks: set[int] = set()

    for document in documents:
        pk = _page_pk_from_document(document)
        if pk is None or pk in seen_pks:
            continue
        seen_pks.add(pk)
        try:
            page = Page.objects.get(pk=pk)
        except Page.DoesNotExist:
            continue
        key = is_eligible_semantic_candidate(
            page,
            locale_id=locale_id,
            exclude_pks=exclude,
            allowed_types=allowed,
        )
        if key is None:
            continue
        bucket = grouped[key]
        if len(bucket) >= limit_per_type:
            if all(len(grouped[type_key]) >= limit_per_type for type_key in allowed):
                break
            continue
        score = float(getattr(document, 'score', 0) or 0)
        bucket.append(_candidate_payload(page, key, score))

    return grouped


def search_similar_pages(
    content: str,
    *,
    exclude_pks: list[int],
    limit: int,
    allowed_types: list[str] | None = None,
) -> list[Page]:
    """
    Vector search against PageIndex.

    Pass ``allowed_types`` so the SuggestedContentAgent wrapper can overfetch
    and filter by page type before returning.
    """
    if not content.strip():
        return []
    if not getattr(settings, 'WAGTAIL_AI_PGVECTOR', False):
        return []
    if limit <= 0:
        return []

    from wagtail_ai.agents.suggested_content import SuggestedContentAgent

    agent = SuggestedContentAgent()
    results = agent.execute(
        vector_index='PageIndex',
        content=content,
        exclude_pks=[str(pk) for pk in exclude_pks],
        limit=limit,
        allowed_types=allowed_types,
    )

    pages: list[Page] = []
    for item in results or []:
        if isinstance(item, Page):
            page = item
        else:
            pk = getattr(item, 'pk', None)
            if pk is None and isinstance(item, dict):
                pk = item.get('pk') or item.get('id')
            if pk is None:
                continue
            try:
                page = Page.objects.get(pk=int(pk))
            except (Page.DoesNotExist, TypeError, ValueError):
                continue

        type_key = page_type_key_for(page)
        if allowed_types and type_key not in allowed_types:
            continue
        pages.append(page)
        if len(pages) >= limit:
            break
    return pages


def _existing_manual_related_pks(page) -> set[int]:
    return manual_related_page_pks(page)


def _suggest_links_by_type(
    content: str,
    *,
    source_page,
    exclude_pks: list[int],
    limit_per_type: int,
) -> dict[str, list[Page]]:
    """
    Fill up to ``limit_per_type`` suggestions per linkable type via separate searches.

    Only ``exclude_pks`` (self + manuals) are withheld; prior auto links may be
    re-selected so regeneration is not starved by the previous top-K.
    """
    grouped: dict[str, list[Page]] = {
        'product': [],
        'collection': [],
        'article': [],
        'glossary': [],
    }
    chosen: set[int] = set(exclude_pks)

    for type_key in ('product', 'collection', 'article', 'glossary'):
        candidates = search_similar_pages(
            content,
            exclude_pks=list(chosen),
            limit=limit_per_type,
            allowed_types=[type_key],
        )
        typed = classify_and_cap(
            candidates,
            source_page=source_page,
            limit_per_type=limit_per_type,
        )
        for page in typed[type_key]:
            if page.pk in chosen:
                continue
            grouped[type_key].append(page)
            chosen.add(page.pk)
            if len(grouped[type_key]) >= limit_per_type:
                break

    return grouped


def _suggest_product_links_hybrid(
    content: str,
    *,
    source_page: ProductPage,
    exclude_pks: list[int],
    limit_per_type: int,
) -> dict[str, list[Page]]:
    """
    ProductPage hybrid suggestions:

    - articles / collections / glossary from reverse ORM (who links to this product)
    - related_products from a single vector search
    """
    reverse = inbound_related_product_sources(
        source_page,
        limit_per_type=limit_per_type,
        exclude_pks=set(exclude_pks),
    )
    grouped: dict[str, list[Page]] = {
        'product': [],
        'collection': list(reverse.get('collection', [])),
        'article': list(reverse.get('article', [])),
        'glossary': list(reverse.get('glossary', [])),
    }
    chosen: set[int] = set(exclude_pks)
    for pages in (grouped['collection'], grouped['article'], grouped['glossary']):
        chosen.update(page.pk for page in pages)

    candidates = search_similar_pages(
        content,
        exclude_pks=list(chosen),
        limit=limit_per_type,
        allowed_types=['product'],
    )
    typed = classify_and_cap(
        candidates,
        source_page=source_page,
        limit_per_type=limit_per_type,
    )
    for page in typed['product']:
        if page.pk in chosen:
            continue
        grouped['product'].append(page)
        chosen.add(page.pk)
        if len(grouped['product']) >= limit_per_type:
            break

    return grouped


def _sync_glossary_related_links_cache(page: GlossaryTermPage):
    page.related_links = serialize_semantic_links(page)


def _semantic_link_prefetch_names() -> list[str]:
    return [f'{name}__related_page' for name in SEMANTIC_LINK_RELATION_NAMES]


@contextmanager
def suppress_page_published_signals():
    """Avoid Shopify sync / recursive semantic refresh when publishing from batch jobs."""
    from shopify_content.signals import _on_page_published
    from shopify_content.sync.publish_sync import get_syncable_page_types

    connected = []
    for model in get_syncable_page_types():
        dispatch_uid = f'shopify_content_sync_on_publish_{model._meta.label_lower}'
        page_published.disconnect(
            receiver=_on_page_published,
            sender=model,
            dispatch_uid=dispatch_uid,
        )
        connected.append((model, dispatch_uid))
    try:
        yield
    finally:
        for model, dispatch_uid in connected:
            page_published.connect(
                _on_page_published,
                sender=model,
                dispatch_uid=dispatch_uid,
            )


def persist_semantic_links_revision(specific, *, skip_publish_signals: bool = True):
    """
    Write typed semantic link cluster children into the Wagtail revision graph.
    """
    model_class = type(specific)
    specific = model_class.objects.prefetch_related(
        *_semantic_link_prefetch_names(),
    ).get(pk=specific.pk)

    signal_guard = suppress_page_published_signals() if skip_publish_signals else nullcontext()
    with signal_guard:
        revision = specific.save_revision(log_action=False, changed=True)
        if specific.live:
            revision.publish(log_action=False, skip_permission_checks=True)

    return revision


def refresh_semantic_links(
    page,
    *,
    dry_run: bool = False,
    update_revision: bool = True,
    skip_publish_signals: bool = True,
) -> dict[str, int]:
    """
    Replace is_auto semantic links with fresh suggestions per typed relation.

    ProductPage uses hybrid reverse ORM (non-product buckets) + one vector
    search for related_products. Other linkable types use per-type vector search.

    Returns counts: {'created': N, 'removed': N, 'manual_kept': N}
    """
    if not getattr(settings, 'SEMANTIC_LINKS_ENABLED', False):
        return {'created': 0, 'removed': 0, 'manual_kept': 0}

    specific = page.specific
    if not is_semantic_linkable_page(specific):
        return {'created': 0, 'removed': 0, 'manual_kept': 0}

    limit_per_type = getattr(settings, 'SEMANTIC_LINKS_LIMIT_PER_TYPE', 5)
    content = extract_page_content(specific)
    manual_pks = _existing_manual_related_pks(specific)
    # Exclude only self + manual links. Prior auto links must remain searchable
    # so regeneration can refill each type up to the limit.
    exclude_pks = [specific.pk, *manual_pks]

    if isinstance(specific, ProductPage):
        grouped = _suggest_product_links_hybrid(
            content,
            source_page=specific,
            exclude_pks=exclude_pks,
            limit_per_type=limit_per_type,
        )
    else:
        grouped = _suggest_links_by_type(
            content,
            source_page=specific,
            exclude_pks=exclude_pks,
            limit_per_type=limit_per_type,
        )

    created_count = sum(len(grouped[key]) for key in grouped)
    removed_count = count_auto_semantic_links(specific)

    if dry_run:
        return {
            'created': created_count,
            'removed': removed_count,
            'manual_kept': len(manual_pks),
        }

    removed_count = delete_auto_semantic_links(specific)
    specific = type(specific).objects.get(pk=specific.pk)

    for type_key in ('product', 'collection', 'article', 'glossary'):
        relation_name = relation_for_page_type(type_key)
        model_cls = get_typed_link_model(specific, relation_name)
        max_sort = (
            model_cls.objects.filter(page_id=specific.pk)
            .order_by('-sort_order')
            .values_list('sort_order', flat=True)
            .first()
        )
        next_sort = (max_sort + 1) if max_sort is not None else 0

        for related in grouped[type_key]:
            if related.pk in manual_pks:
                continue
            model_cls.objects.create(
                page_id=specific.pk,
                related_page=related,
                is_auto=True,
                sort_order=next_sort,
            )
            next_sort += 1

    if isinstance(specific, GlossaryTermPage):
        _sync_glossary_related_links_cache(specific)
        type(specific).objects.filter(pk=specific.pk).update(related_links=specific.related_links)

    links_changed = removed_count > 0 or created_count > 0
    if update_revision and links_changed:
        try:
            persist_semantic_links_revision(
                type(specific).objects.get(pk=specific.pk),
                skip_publish_signals=skip_publish_signals,
            )
        except Exception:
            logger.exception(
                'Failed to persist semantic links revision for page pk=%s',
                specific.pk,
            )

    return {
        'created': created_count,
        'removed': removed_count,
        'manual_kept': len(manual_pks),
    }

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
from shopify_content.semantic_links.serialization import (
    LINKABLE_PAGE_TYPES,
    serialize_semantic_links,
)

logger = logging.getLogger(__name__)

SEMANTIC_LINK_PAGE_TYPES = LINKABLE_PAGE_TYPES


def is_semantic_linkable_page(page) -> bool:
    return isinstance(page.specific, SEMANTIC_LINK_PAGE_TYPES)


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


def _page_type_key(page) -> str | None:
    specific = page.specific
    if isinstance(specific, ProductPage):
        return 'product'
    if isinstance(specific, CollectionPage):
        return 'collection'
    if isinstance(specific, ArticlePage):
        return 'article'
    if isinstance(specific, GlossaryTermPage):
        return 'glossary'
    return None


def classify_and_cap(pages, *, source_page, limit_per_type: int) -> dict[str, list[Page]]:
    """Group candidate pages by type and apply per-type caps with locale filtering."""
    source_locale_id = source_page.locale_id
    grouped: dict[str, list[Page]] = {
        'product': [],
        'collection': [],
        'article': [],
        'glossary': [],
    }

    for page in pages:
        if page.pk == source_page.pk:
            continue
        if not page.live:
            continue
        if page.locale_id != source_locale_id:
            continue

        specific = page.specific
        if isinstance(specific, ProductPage):
            if specific.status != 'ACTIVE':
                continue
            key = 'product'
        elif isinstance(specific, CollectionPage):
            key = 'collection'
        elif isinstance(specific, ArticlePage):
            key = 'article'
        elif isinstance(specific, GlossaryTermPage):
            key = 'glossary'
        else:
            continue

        if len(grouped[key]) >= limit_per_type:
            continue
        grouped[key].append(page)

    return grouped


def search_similar_pages(content: str, *, exclude_pks: list[int], limit: int) -> list[Page]:
    if not content.strip():
        return []
    if not getattr(settings, 'WAGTAIL_AI_PGVECTOR', False):
        return []

    from wagtail_ai.agents.suggested_content import SuggestedContentAgent

    agent = SuggestedContentAgent()
    results = agent.execute(
        vector_index='PageIndex',
        content=content,
        exclude_pks=[str(pk) for pk in exclude_pks],
        limit=limit,
    )

    pages: list[Page] = []
    for item in results or []:
        if isinstance(item, Page):
            pages.append(item)
            continue
        pk = getattr(item, 'pk', None)
        if pk is None and isinstance(item, dict):
            pk = item.get('pk') or item.get('id')
        if pk is None:
            continue
        try:
            pages.append(Page.objects.get(pk=int(pk)))
        except (Page.DoesNotExist, TypeError, ValueError):
            continue
    return pages


def _existing_manual_related_pks(page) -> set[int]:
    return set(
        page.semantic_links.filter(is_auto=False).values_list('related_page_id', flat=True)
    )


def _sync_glossary_related_links_cache(page: GlossaryTermPage):
    page.related_links = serialize_semantic_links(page)


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
    Write semantic_links cluster children into the Wagtail revision graph.

    Without this step, links created via ORM are in the DB but the admin editor
    may still show an older revision snapshot (when has_unpublished_changes=True).
    """
    model_class = type(specific)
    specific = model_class.objects.prefetch_related(
        'semantic_links__related_page',
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
    Replace is_auto semantic links with fresh vector suggestions.

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
    exclude_pks = [specific.pk, *manual_pks, *specific.semantic_links.values_list('related_page_id', flat=True)]

    candidates = search_similar_pages(
        content,
        exclude_pks=list(exclude_pks),
        limit=limit_per_type * len(SEMANTIC_LINK_PAGE_TYPES),
    )
    grouped = classify_and_cap(candidates, source_page=specific, limit_per_type=limit_per_type)

    new_pages: list[Page] = []
    for key in ('product', 'collection', 'article', 'glossary'):
        new_pages.extend(grouped[key])

    if dry_run:
        return {
            'created': len(new_pages),
            'removed': specific.semantic_links.filter(is_auto=True).count(),
            'manual_kept': len(manual_pks),
        }

    removed = specific.semantic_links.filter(is_auto=True).delete()[0]

    max_sort = (
        specific.semantic_links.order_by('-sort_order').values_list('sort_order', flat=True).first()
    )
    next_sort = (max_sort + 1) if max_sort is not None else 0

    for related in new_pages:
        if related.pk in manual_pks:
            continue
        specific.semantic_links.create(
            related_page=related,
            is_auto=True,
            sort_order=next_sort,
        )
        next_sort += 1

    if isinstance(specific, GlossaryTermPage):
        _sync_glossary_related_links_cache(specific)
        type(specific).objects.filter(pk=specific.pk).update(related_links=specific.related_links)

    links_changed = removed > 0 or bool(new_pages)
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
        'created': len(new_pages),
        'removed': removed,
        'manual_kept': len(manual_pks),
    }

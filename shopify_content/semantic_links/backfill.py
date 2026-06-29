"""Batch backfill helpers for semantic internal links."""

from django.conf import settings

from shopify_content.indexing import INDEX_MODELS, live_queryset_for
from shopify_content.models.semantic_links import page_has_auto_semantic_links
from shopify_content.semantic_links.service import refresh_semantic_links


def run_semantic_links_backfill(
    *,
    model: str = 'all',
    only_missing: bool = True,
    dry_run: bool = False,
    update_revision: bool = True,
    skip_publish_signals: bool = True,
) -> dict[str, int]:
    if not getattr(settings, 'SEMANTIC_LINKS_ENABLED', False):
        return {
            'pages_processed': 0,
            'pages_skipped': 0,
            'created': 0,
            'removed': 0,
            'manual_kept': 0,
        }

    targets = (
        ['article', 'product', 'collection', 'glossary']
        if model == 'all'
        else [model]
    )

    totals = {
        'pages_processed': 0,
        'pages_skipped': 0,
        'created': 0,
        'removed': 0,
        'manual_kept': 0,
    }

    for key in targets:
        page_model, _fields = INDEX_MODELS[key]
        for page in live_queryset_for(page_model).iterator():
            if only_missing and page_has_auto_semantic_links(page):
                totals['pages_skipped'] += 1
                continue

            stats = refresh_semantic_links(
                page,
                dry_run=dry_run,
                update_revision=update_revision,
                skip_publish_signals=skip_publish_signals,
            )
            totals['pages_processed'] += 1
            totals['created'] += stats['created']
            totals['removed'] += stats['removed']
            totals['manual_kept'] += stats['manual_kept']

    return totals

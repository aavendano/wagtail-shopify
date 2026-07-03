"""Backfill native Shopify reference metafields from typed semantic link FK rows."""

from django.core.management.base import BaseCommand

from shopify_content.models import CollectionPage, GlossaryTermPage, ProductPage
from shopify_content.models.blog import ArticlePage
from shopify_content.models.semantic_links import page_has_semantic_links
from shopify_content.semantic_links.constants import NATIVE_REFERENCE_RELATION_NAMES
from shopify_content.semantic_links.references import serialize_native_references
from shopify_content.sync.task_dispatch import enqueue_page_outbound_sync


MODEL_MAP = {
    'product': ProductPage,
    'collection': CollectionPage,
    'article': ArticlePage,
    'glossary': GlossaryTermPage,
}


class Command(BaseCommand):
    help = (
        'Enqueue outbound sync for pages with semantic link FK rows so native '
        'list.*_reference metafields are pushed to Shopify.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--model',
            choices=['product', 'collection', 'article', 'glossary', 'all'],
            default='all',
            help='Which page type to backfill (default: all).',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Report coverage without enqueueing sync tasks.',
        )

    def handle(self, *args, **options):
        model_key = options['model']
        dry_run = options['dry_run']

        models = (
            list(MODEL_MAP.values())
            if model_key == 'all'
            else [MODEL_MAP[model_key]]
        )

        pages_with_links = 0
        pages_with_gids = 0
        pages_without_gids = 0
        omitted_targets = 0
        enqueued = 0

        for model in models:
            for page in model.objects.live().iterator():
                if not page_has_semantic_links(page):
                    continue
                pages_with_links += 1

                refs = serialize_native_references(page)
                if refs:
                    pages_with_gids += 1
                else:
                    pages_without_gids += 1

                for relation_name in NATIVE_REFERENCE_RELATION_NAMES:
                    manager = getattr(page, relation_name, None)
                    if manager is None:
                        continue
                    row_count = manager.count()
                    resolved = len(refs.get(relation_name, []))
                    omitted_targets += max(row_count - resolved, 0)

                if dry_run:
                    continue

                if not getattr(page, 'sync_enabled', True):
                    continue
                if model is not GlossaryTermPage and not page.shopify_id:
                    continue

                sync_run = enqueue_page_outbound_sync(page)
                if sync_run is not None:
                    enqueued += 1

        self.stdout.write(
            self.style.SUCCESS(
                'Done. '
                f'pages_with_links={pages_with_links}, '
                f'pages_with_resolved_gids={pages_with_gids}, '
                f'pages_without_resolved_gids={pages_without_gids}, '
                f'omitted_targets={omitted_targets}, '
                f'enqueued={enqueued}, '
                f'dry_run={dry_run}.'
            )
        )

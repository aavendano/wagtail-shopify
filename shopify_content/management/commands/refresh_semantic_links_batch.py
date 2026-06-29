"""Backfill semantic internal links for live pages."""

from django.core.management.base import BaseCommand

from shopify_content.indexing import INDEX_MODELS, live_queryset_for
from shopify_content.semantic_links.service import refresh_semantic_links


class Command(BaseCommand):
    help = 'Generate auto semantic internal links for all live linkable pages.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--model',
            choices=['article', 'product', 'collection', 'glossary', 'all'],
            default='all',
            help='Which page type to refresh (default: all).',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Report counts without writing links.',
        )
        parser.add_argument(
            '--skip-revision-sync',
            action='store_true',
            help='Do not save/publish Wagtail revisions after updating links.',
        )

    def handle(self, *args, **options):
        model_choice = options['model']
        dry_run = options['dry_run']
        targets = (
            ['article', 'product', 'collection', 'glossary']
            if model_choice == 'all'
            else [model_choice]
        )

        total_created = 0
        total_removed = 0
        pages_processed = 0

        for key in targets:
            model, _fields = INDEX_MODELS[key]
            qs = live_queryset_for(model)
            self.stdout.write(f'Processing {model._meta.label} ({qs.count()} live pages)...')

            for page in qs.iterator():
                stats = refresh_semantic_links(
                    page,
                    dry_run=dry_run,
                    update_revision=not options['skip_revision_sync'],
                )
                total_created += stats['created']
                total_removed += stats['removed']
                pages_processed += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Done. Processed {pages_processed} pages '
                f'(created={total_created}, removed={total_removed}, dry_run={dry_run}).'
            )
        )

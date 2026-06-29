"""Backfill semantic internal links for live pages."""

from django.core.management.base import BaseCommand

from shopify_content.semantic_links.backfill import run_semantic_links_backfill


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
            '--only-missing',
            action='store_true',
            help='Skip pages that already have at least one auto link.',
        )
        parser.add_argument(
            '--skip-revision-sync',
            action='store_true',
            help='Do not save/publish Wagtail revisions after updating links.',
        )

    def handle(self, *args, **options):
        totals = run_semantic_links_backfill(
            model=options['model'],
            only_missing=options['only_missing'],
            dry_run=options['dry_run'],
            update_revision=not options['skip_revision_sync'],
        )

        self.stdout.write(
            self.style.SUCCESS(
                'Done. '
                f"processed={totals['pages_processed']}, "
                f"skipped={totals['pages_skipped']}, "
                f"created={totals['created']}, "
                f"removed={totals['removed']}, "
                f"dry_run={options['dry_run']}."
            )
        )

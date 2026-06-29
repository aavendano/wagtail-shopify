"""Sync existing semantic_links FK rows into Wagtail revisions (admin visibility fix)."""

from django.core.management.base import BaseCommand
from django.db.models import Count

from shopify_content.indexing import INDEX_MODELS, live_queryset_for
from shopify_content.semantic_links.service import persist_semantic_links_revision


class Command(BaseCommand):
    help = (
        'Save/publish Wagtail revisions for pages that already have semantic_links rows. '
        'Use after refresh_semantic_links_batch if links exist in DB but not in admin UI.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--model',
            choices=['article', 'product', 'collection', 'glossary', 'all'],
            default='all',
            help='Which page type to sync (default: all).',
        )

    def handle(self, *args, **options):
        model_choice = options['model']
        targets = (
            ['article', 'product', 'collection', 'glossary']
            if model_choice == 'all'
            else [model_choice]
        )

        synced = 0

        for key in targets:
            model, _fields = INDEX_MODELS[key]
            qs = (
                live_queryset_for(model)
                .annotate(_link_count=Count('semantic_links'))
                .filter(_link_count__gt=0)
            )
            total = qs.count()
            self.stdout.write(
                f'Syncing revisions for {model._meta.label} ({total} pages with links)...'
            )

            for page in qs.iterator(chunk_size=100):
                persist_semantic_links_revision(page)
                synced += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Done. Synced revisions for {synced} pages.'
            )
        )

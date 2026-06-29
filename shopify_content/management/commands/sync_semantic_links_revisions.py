"""Sync existing typed semantic link FK rows into Wagtail revisions (admin visibility fix)."""

from django.core.management.base import BaseCommand

from shopify_content.indexing import INDEX_MODELS, live_queryset_for
from shopify_content.models.semantic_links import page_has_semantic_links
from shopify_content.semantic_links.service import persist_semantic_links_revision


class Command(BaseCommand):
    help = (
        'Save/publish Wagtail revisions for pages that already have typed internal link rows. '
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
            qs = live_queryset_for(model)
            self.stdout.write(
                f'Scanning {model._meta.label} ({qs.count()} live pages)...'
            )

            for page in qs.iterator(chunk_size=100):
                if not page_has_semantic_links(page):
                    continue
                persist_semantic_links_revision(page)
                synced += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Done. Synced revisions for {synced} pages.'
            )
        )

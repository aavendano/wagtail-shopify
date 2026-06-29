"""Index Wagtail pages into PageIndex in small batches to avoid memory spikes."""
import gc
import time

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django_ai_core.contrib.index.base import registry

from shopify_content.indexing import INDEX_MODELS, model_source_for


class Command(BaseCommand):
    help = (
        'Update PageIndex in batches (memory-safe alternative to rebuild_indexes). '
        'Resume with --start-pk after interruption.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--model',
            choices=['article', 'product', 'collection', 'glossary', 'all'],
            default='all',
            help='Which page type to index (default: all).',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=25,
            help='Number of pages per batch (default: 25).',
        )
        parser.add_argument(
            '--pause',
            type=float,
            default=3.0,
            help='Seconds to sleep between batches (default: 3).',
        )
        parser.add_argument(
            '--start-pk',
            type=int,
            default=0,
            help='Resume indexing pages with pk greater than this value.',
        )
        parser.add_argument(
            '--skip-semantic-backfill',
            action='store_true',
            help='Do not enqueue semantic links backfill when indexing completes.',
        )

    def handle(self, *args, **options):
        if 'PageIndex' not in registry.list():
            raise CommandError(
                'PageIndex is not registered. Enable WAGTAIL_AI_PGVECTOR and GEMINI_API_KEY.'
            )

        model_choice = options['model']
        batch_size = options['batch_size']
        pause_seconds = options['pause']
        start_pk = options['start_pk']

        if batch_size < 1:
            raise CommandError('--batch-size must be at least 1')

        targets = (
            ['article', 'product', 'collection', 'glossary']
            if model_choice == 'all'
            else [model_choice]
        )

        index = registry.get('PageIndex')()

        total_pages = 0
        total_docs = 0
        last_pk = start_pk

        for key in targets:
            model, fields = INDEX_MODELS[key]
            source = model_source_for(model, fields, start_pk=start_pk)
            pending = []
            last_pk = start_pk
            model_pages = 0
            model_docs = 0

            self.stdout.write(
                f'Indexing {model._meta.label} (batch_size={batch_size}, start_pk>{start_pk})...'
            )

            for obj in source.queryset.iterator(chunk_size=batch_size):
                pending.append(obj)
                last_pk = obj.pk
                if len(pending) < batch_size:
                    continue

                docs = list(source.objects_to_documents(pending))
                if docs:
                    index.update(docs)
                    model_docs += len(docs)
                model_pages += len(pending)
                pending.clear()
                gc.collect()

                self.stdout.write(
                    f'  {model._meta.label}: {model_pages} pages, '
                    f'{model_docs} chunks (last pk={last_pk})'
                )
                self.stdout.flush()

                if pause_seconds > 0:
                    time.sleep(pause_seconds)

            if pending:
                docs = list(source.objects_to_documents(pending))
                if docs:
                    index.update(docs)
                    model_docs += len(docs)
                model_pages += len(pending)
                self.stdout.write(
                    f'  {model._meta.label}: {model_pages} pages, '
                    f'{model_docs} chunks (last pk={last_pk})'
                )
                self.stdout.flush()

            total_pages += model_pages
            total_docs += model_docs
            self.stdout.write(
                self.style.SUCCESS(
                    f'Finished {model._meta.label}: {model_pages} pages, {model_docs} chunks.'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'Done. Indexed {total_pages} pages ({total_docs} chunks). '
                f'Last pk processed: {last_pk}.'
            )
        )

        if (
            getattr(settings, 'SEMANTIC_LINKS_ENABLED', False)
            and not options['skip_semantic_backfill']
        ):
            from shopify_content.tasks import backfill_semantic_links_task

            result = backfill_semantic_links_task.delay(
                model=model_choice,
                only_missing=True,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Semantic links backfill enqueued (task id={result.id}).'
                )
            )


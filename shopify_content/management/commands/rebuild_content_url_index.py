from django.core.management.base import BaseCommand

from shopify_content.content_url_index import rebuild_full_index, rebuild_index_for_page
from wagtail.models import Page


class Command(BaseCommand):
    help = 'Rebuild the ContentUrlIndex mapping from live Wagtail pages with shopify_id.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--page-id',
            type=int,
            default=None,
            help='Rebuild index rows for a single Wagtail page ID only.',
        )

    def handle(self, *args, **options):
        page_id = options.get('page_id')
        if page_id is not None:
            try:
                page = Page.objects.get(pk=page_id)
            except Page.DoesNotExist:
                self.stderr.write(self.style.ERROR(f'Page {page_id} not found.'))
                return
            count = rebuild_index_for_page(page)
            self.stdout.write(
                self.style.SUCCESS(f'Indexed {count} URL variant(s) for page {page_id}.')
            )
            return

        stats = rebuild_full_index()
        self.stdout.write(
            self.style.SUCCESS(
                f'Content URL index rebuilt: {stats["created"]} rows, '
                f'{stats["skipped"]} pages skipped.'
            )
        )

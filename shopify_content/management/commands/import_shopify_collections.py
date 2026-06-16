"""Import all Shopify Collections into Wagtail as CollectionPage instances."""
from django.core.management.base import BaseCommand, CommandError
from wagtail.models import Page

from shopify_content.sync.inbound import import_collections, _get_shop
from shopify_content.sync.import_parents import resolve_shopify_import_parent
from shopify_content.models import ShopifyRootPage


class Command(BaseCommand):
    help = 'Import all Shopify Collections into Wagtail CollectionPage instances.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--parent-page-id',
            type=int,
            help='Wagtail Page ID to use as parent. Defaults to ShopifyRootPage slug "collections" (auto-created if missing).',
        )

    def handle(self, *args, **options):
        shop = _get_shop()
        parent_id = options.get('parent_page_id')

        if parent_id:
            try:
                parent = Page.objects.get(pk=parent_id).specific
            except Page.DoesNotExist:
                raise CommandError(f'Page id={parent_id} does not exist.')
        else:
            parent = resolve_shopify_import_parent('collections')
            if not isinstance(parent, ShopifyRootPage):
                raise CommandError(
                    f'Page id={parent.pk} is not a ShopifyRootPage.'
                )

        self.stdout.write(f'Importing collections for shop={shop}...')
        stats = import_collections(shop, parent)
        self.stdout.write(self.style.SUCCESS(
            f'Done. Created: {stats["created"]}, '
            f'Updated: {stats["updated"]}, '
            f'Errors: {stats["errors"]}'
        ))

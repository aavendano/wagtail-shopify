"""Import all Shopify Products into Wagtail as ProductPage instances."""
from django.core.management.base import BaseCommand, CommandError
from wagtail.models import Page

from shopify_content.sync.inbound import import_products, _get_shop
from shopify_content.sync.import_parents import resolve_shopify_import_parent
from shopify_content.models import ShopifyRootPage


class Command(BaseCommand):
    help = 'Import all Shopify Products into Wagtail ProductPage instances.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--parent-page-id',
            type=int,
            help='Wagtail Page ID to use as parent. Defaults to ShopifyRootPage slug "root" (auto-created if missing).',
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
            parent = resolve_shopify_import_parent('products')
            if not isinstance(parent, ShopifyRootPage):
                raise CommandError(
                    f'Page id={parent.pk} is not a ShopifyRootPage.'
                )

        self.stdout.write(f'Importing products for shop={shop}...')
        stats = import_products(shop, parent)
        self.stdout.write(self.style.SUCCESS(
            f'Done. Created: {stats["created"]}, '
            f'Updated: {stats["updated"]}, '
            f'Errors: {stats["errors"]}'
        ))

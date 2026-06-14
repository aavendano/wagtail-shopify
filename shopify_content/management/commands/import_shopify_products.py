"""Import all Shopify Products into Wagtail as ProductPage instances."""
from django.core.management.base import BaseCommand, CommandError
from wagtail.models import Page

from shopify_content.sync.inbound import import_products, _get_shop
from shopify_content.models import ShopifyRootPage


class Command(BaseCommand):
    help = 'Import all Shopify Products into Wagtail ProductPage instances.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--parent-page-id',
            type=int,
            help='Wagtail Page ID to use as parent. Defaults to the first ShopifyRootPage.',
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
            parent = ShopifyRootPage.objects.first()
            if not parent:
                raise CommandError(
                    'No ShopifyRootPage found. Create one in Wagtail admin first, '
                    'or pass --parent-page-id.'
                )

        self.stdout.write(f'Importing products for shop={shop}...')
        stats = import_products(shop, parent)
        self.stdout.write(self.style.SUCCESS(
            f'Done. Created: {stats["created"]}, '
            f'Updated: {stats["updated"]}, '
            f'Errors: {stats["errors"]}'
        ))

"""Import all Shopify Blogs and Articles into Wagtail."""
from django.core.management.base import BaseCommand, CommandError
from wagtail.models import Page

from shopify_config.tenancy import ShopUnresolvedError, add_shop_argument, resolve_shop_for_command_or_sole
from shopify_content.sync.inbound import import_blogs_and_articles
from shopify_content.sync.import_parents import resolve_shopify_import_parent
from shopify_content.models import ShopifyRootPage


class Command(BaseCommand):
    help = 'Import all Shopify Blogs and their Articles into Wagtail.'

    def add_arguments(self, parser):
        add_shop_argument(parser)
        parser.add_argument(
            '--parent-page-id',
            type=int,
            help='Wagtail Page ID to use as parent. Defaults to ShopifyRootPage slug "blogs" (auto-created if missing).',
        )

    def handle(self, *args, **options):
        try:
            shop = resolve_shop_for_command_or_sole(shop=options.get('shop') or None)
        except ShopUnresolvedError as exc:
            raise CommandError(str(exc)) from exc
        parent_id = options.get('parent_page_id')

        if parent_id:
            try:
                parent = Page.objects.get(pk=parent_id).specific
            except Page.DoesNotExist:
                raise CommandError(f'Page id={parent_id} does not exist.')
        else:
            parent = resolve_shopify_import_parent('blogs')
            if not isinstance(parent, ShopifyRootPage):
                raise CommandError(
                    f'Page id={parent.pk} is not a ShopifyRootPage.'
                )

        self.stdout.write(f'Importing blogs and articles for shop={shop}...')
        stats = import_blogs_and_articles(shop, parent)
        self.stdout.write(self.style.SUCCESS(
            f'Blogs — Created: {stats["blogs"]["created"]}, '
            f'Updated: {stats["blogs"]["updated"]}, '
            f'Errors: {stats["blogs"]["errors"]}\n'
            f'Articles — Created: {stats["articles"]["created"]}, '
            f'Updated: {stats["articles"]["updated"]}, '
            f'Errors: {stats["articles"]["errors"]}'
        ))

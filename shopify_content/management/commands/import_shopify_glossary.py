"""Import all Shopify glossary_term metaobjects into Wagtail GlossaryTermPage instances."""
from django.core.management.base import BaseCommand, CommandError
from wagtail.models import Page

from shopify_config.tenancy import ShopUnresolvedError, add_shop_argument, resolve_shop_for_command_or_sole
from shopify_content.sync.inbound import import_glossary_terms
from shopify_content.sync.import_parents import resolve_shopify_import_parent
from shopify_content.models import ShopifyRootPage


class Command(BaseCommand):
    help = 'Import glossary_term metaobjects from Shopify into Wagtail GlossaryTermPage instances.'

    def add_arguments(self, parser):
        add_shop_argument(parser)
        parser.add_argument(
            '--parent-page-id',
            type=int,
            help='Wagtail Page ID to use as parent. Defaults to ShopifyRootPage slug "glossary".',
        )
        parser.add_argument(
            '--new-only',
            action='store_true',
            help='Only create terms that do not exist in Wagtail; skip updates.',
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
            parent = resolve_shopify_import_parent('glossary')
            if not isinstance(parent, ShopifyRootPage):
                raise CommandError(
                    f'Page id={parent.pk} is not a ShopifyRootPage.'
                )

        self.stdout.write(f'Importing glossary terms for shop={shop}...')
        stats = import_glossary_terms(
            shop,
            parent,
            new_only=options['new_only'],
        )
        self.stdout.write(self.style.SUCCESS(
            f'Done. Created: {stats["created"]}, '
            f'Updated: {stats["updated"]}, '
            f'Skipped: {stats["skipped"]}, '
            f'Errors: {stats["errors"]}'
        ))

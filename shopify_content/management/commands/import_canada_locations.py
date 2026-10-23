"""
Import the Canadian ``region`` and ``location_page`` metaobjects into RegionPage / LocationPage.

Read-only against Shopify: only the Wagtail database changes. Each location goes under the
region that lists it in ``location_pages``. Imported pages keep their Shopify handle and have
``sync_enabled`` off.

Usage:
    python manage.py import_canada_locations --dry-run
    python manage.py import_canada_locations
    python manage.py import_canada_locations --new-only
"""

from django.core.management.base import BaseCommand, CommandError
from wagtail.models import Page

from shopify_config.tenancy import ShopUnresolvedError, add_shop_argument, resolve_shop_for_command_or_sole
from shopify_content.models import ShopifyRootPage
from shopify_content.sync.canada_inbound import DEFAULT_LOCALE_CODE, fetch_plan, import_canada_locations
from shopify_content.sync.import_parents import resolve_shopify_import_parent


class Command(BaseCommand):
    help = 'Import Canadian region and location_page metaobjects from Shopify (read-only on Shopify).'

    def add_arguments(self, parser):
        add_shop_argument(parser)
        parser.add_argument(
            '--parent-page-id', type=int,
            help='Wagtail ShopifyRootPage that will hold the regions. Defaults to the locations root.',
        )
        parser.add_argument(
            '--locale', default=DEFAULT_LOCALE_CODE,
            help=f'Wagtail locale for the imported pages (default {DEFAULT_LOCALE_CODE}).',
        )
        parser.add_argument('--new-only', action='store_true', help='Create missing pages; do not update existing ones.')
        parser.add_argument('--dry-run', action='store_true', help='Fetch and report; write nothing.')

    def handle(self, *args, **options):
        try:
            shop = resolve_shop_for_command_or_sole(shop=options.get('shop') or None)
        except ShopUnresolvedError as exc:
            raise CommandError(str(exc)) from exc

        parent_id = options.get('parent_page_id')
        if parent_id:
            try:
                root = Page.objects.get(pk=parent_id).specific
            except Page.DoesNotExist:
                raise CommandError(f'Page id={parent_id} does not exist.')
        else:
            try:
                root = resolve_shopify_import_parent('locations')
            except RuntimeError as exc:
                raise CommandError(str(exc)) from exc
        if not isinstance(root, ShopifyRootPage):
            raise CommandError(f'Page id={root.pk} is not a ShopifyRootPage.')

        self.stdout.write(f'Reading Canadian regions and locations for shop={shop} (read-only)...')
        plan = fetch_plan(shop)
        self.stdout.write(
            f'Found {len(plan.regions)} region(s) and {len(plan.locations)} location(s); '
            f'{len(plan.unparented)} without a region, {plan.skipped} inactive/invalid skipped.'
        )
        for warning in plan.warnings:
            self.stdout.write(self.style.WARNING(f'  {warning}'))

        try:
            stats = import_canada_locations(
                shop, root, locale_code=options['locale'], new_only=options['new_only'],
                dry_run=options['dry_run'], plan=plan,
            )
        except ValueError as exc:
            raise CommandError(str(exc)) from exc

        verb = 'Would create' if stats['dry_run'] else 'Done'
        for kind in ('regions', 'locations'):
            s = stats[kind]
            self.stdout.write(self.style.SUCCESS(
                f'{verb} {kind}: created {s["created"]}, updated {s["updated"]}, '
                f'skipped {s["skipped"]}, errors {s["errors"]}'
            ))
        if stats['dry_run']:
            self.stdout.write('Dry run: nothing was written.')

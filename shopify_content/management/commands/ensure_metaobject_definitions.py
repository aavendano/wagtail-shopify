"""
Bootstrap merchant-owned Shopify metaobject definitions.

Run this once after installing the app on a new store, or after a definition
is accidentally deleted from Shopify Admin. Safe to re-run — uses
ensure_definition() which is a no-op if the type already exists.

Usage:
    python manage.py ensure_metaobject_definitions
"""

from django.core.management.base import BaseCommand, CommandError

from core.models import ShopConfig
from metaobjects.shopify_metaobjects.client import MetaobjectClient
from metaobjects.shopify_metaobjects.exceptions import DefinitionError
from shopify_content.sync.outbound import _location_page_definition


class Command(BaseCommand):
    help = 'Create or verify merchant-owned Shopify metaobject definitions'

    def handle(self, *args, **options):
        config = ShopConfig.objects.first()
        if not config:
            raise CommandError('No ShopConfig found. Install the app on a Shopify store first.')

        shop = config.shop
        client = MetaobjectClient(shop=shop)

        definitions = [
            ('location_page', _location_page_definition),
        ]

        for type_name, spec_fn in definitions:
            self.stdout.write(f'Ensuring definition: {type_name} ... ', ending='')
            try:
                result = client.ensure_definition(spec_fn())
                self.stdout.write(self.style.SUCCESS(f'OK ({result.type})'))
            except DefinitionError as exc:
                self.stdout.write(self.style.ERROR(f'FAILED: {exc}'))
                raise CommandError(f'Failed to ensure definition for {type_name}: {exc}') from exc

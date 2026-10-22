"""
Bootstrap merchant-owned Shopify metaobject definitions.

Run this once after installing the app on a new store, or after a definition
is accidentally deleted from Shopify Admin. Safe to re-run — creates missing
definitions and adds any fieldDefinitions that are missing from existing types
via metaobjectDefinitionUpdate.

Usage:
    python manage.py ensure_metaobject_definitions
"""

from django.core.management.base import BaseCommand, CommandError

from metaobjects.shopify_metaobjects.client import MetaobjectClient
from metaobjects.shopify_metaobjects.exceptions import DefinitionError
from shopify_config.tenancy import (
    ShopUnresolvedError,
    add_shop_argument,
    resolve_shop_for_command_or_sole,
)
from shopify_content.sync.outbound import (
    _location_page_definition,
    _root_page_definition,
    _home_page_definition,
    ensure_glossary_term_definition,
)


class Command(BaseCommand):
    help = 'Create or verify merchant-owned Shopify metaobject definitions'

    def add_arguments(self, parser):
        add_shop_argument(parser)

    def handle(self, *args, **options):
        try:
            shop = resolve_shop_for_command_or_sole(shop=options.get('shop') or None)
        except ShopUnresolvedError as exc:
            raise CommandError(str(exc)) from exc
        client = MetaobjectClient(shop=shop)

        definitions = [
            ('local_page', _location_page_definition),
            ('root_page', _root_page_definition),
            ('home_page', _home_page_definition),
        ]

        for type_name, spec_fn in definitions:
            self.stdout.write(f'Ensuring definition: {type_name} ... ', ending='')
            try:
                result = client.ensure_definition(spec_fn())
                self.stdout.write(self.style.SUCCESS(f'OK ({result.type})'))
            except DefinitionError as exc:
                self.stdout.write(self.style.ERROR(f'FAILED: {exc}'))
                raise CommandError(f'Failed to ensure definition for {type_name}: {exc}') from exc

        self.stdout.write('Ensuring definition: glossary_term ... ', ending='')
        try:
            result = ensure_glossary_term_definition(client)
            self.stdout.write(self.style.SUCCESS(f'OK ({result.type})'))
        except DefinitionError as exc:
            self.stdout.write(self.style.ERROR(f'FAILED: {exc}'))
            raise CommandError(f'Failed to ensure definition for glossary_term: {exc}') from exc

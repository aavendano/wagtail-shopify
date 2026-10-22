"""
Plan or apply the generalized Shopify definitions: region, location_page, faq, content_links.

Default is an offline dry run that prints the definitions as code. ``--live`` compares them
with the store using read queries only. ``--apply`` writes, and is refused unless
SHOPIFY_SCHEMA_CHANGES_ENABLED is on: Shopify definitions and data do not change until the
project is operational.

Usage:
    python manage.py unified_location_definitions               # offline, nothing contacted
    python manage.py unified_location_definitions --live        # read-only diff vs the store
    python manage.py unified_location_definitions --apply       # guarded write
"""

import json

from django.core.management.base import BaseCommand, CommandError

from metaobjects.shopify_metaobjects.client import MetaobjectClient
from metaobjects.shopify_metaobjects.exceptions import DefinitionError
from shopify_config.tenancy import (
    ShopUnresolvedError,
    add_shop_argument,
    resolve_shop_for_command_or_sole,
)
from shopify_content.sync import unified_definitions as definitions


class Command(BaseCommand):
    help = 'Plan or apply the generalized region / location_page / faq / content_links definitions'

    def add_arguments(self, parser):
        add_shop_argument(parser)
        parser.add_argument('--live', action='store_true',
                            help='Compare with the store (read queries only).')
        parser.add_argument('--apply', action='store_true',
                            help='Write to the store. Refused unless SHOPIFY_SCHEMA_CHANGES_ENABLED is on.')
        parser.add_argument('--json', action='store_true', help='Machine-readable output.')

    def handle(self, *args, **options):
        if options['apply'] and not definitions.schema_changes_enabled():
            raise CommandError(
                'Refused: SHOPIFY_SCHEMA_CHANGES_ENABLED is off. Shopify definitions and data '
                'do not change until the project is operational.'
            )
        if not (options['live'] or options['apply']):
            self._offline(options)
            return

        try:
            shop = resolve_shop_for_command_or_sole(shop=options.get('shop') or None)
        except ShopUnresolvedError as exc:
            raise CommandError(str(exc)) from exc
        client = MetaobjectClient(shop=shop)
        try:
            if options['apply']:
                plans = definitions.apply_definitions(client)
                heading = 'Applied'
            else:
                plans = definitions.plan_definitions(client)
                heading = 'Plan (read only)'
        except DefinitionError as exc:
            raise CommandError(str(exc)) from exc

        if options['json']:
            self.stdout.write(json.dumps([plan.to_dict() for plan in plans], indent=2))
            return
        self.stdout.write(f'{heading} for {shop}:')
        for plan in plans:
            self.stdout.write(f'  {plan.type}: {plan.action}')
            if plan.missing_fields:
                self.stdout.write(f'    new fields: {", ".join(plan.missing_fields)}')
            for key in plan.changed_validations:
                self.stdout.write(f'    changed validations: {key}')
            if plan.capability_changes:
                self.stdout.write(f'    capabilities: {json.dumps(plan.capability_changes)}')

    def _offline(self, options):
        specs = definitions.build_definitions()
        if options['json']:
            self.stdout.write(json.dumps([spec.to_shopify_input() for spec in specs], indent=2))
            return
        self.stdout.write('Generalized definitions (offline; nothing was sent to Shopify):')
        for spec in specs:
            self.stdout.write(f'  {spec.type}: {len(spec.fields)} fields')
        self.stdout.write(
            'Pointer metafield for content_links: '
            f'{definitions.CONTENT_LINKS_POINTER_METAFIELD["namespace"]}.'
            f'{definitions.CONTENT_LINKS_POINTER_METAFIELD["key"]} '
            f'on {", ".join(definitions.CONTENT_LINKS_POINTER_OWNERS)} (not part of this command).'
        )
        self.stdout.write('Use --live for a read-only comparison with the store.')

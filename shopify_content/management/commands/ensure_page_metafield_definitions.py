"""
Create Shopify Page metafield definition for custom.index_listings.

Run once per store (safe to re-run):

    python manage.py ensure_page_metafield_definitions
    python manage.py ensure_index_metafield_definitions   # preferred (includes blog/article)

For legacy per-locale index metafields, use ensure_index_metafield_definitions --legacy.
"""

from django.core.management.base import BaseCommand, CommandError

from core.models import ShopConfig
from shopify_content.sync.page_metafield_definitions import (
    PAGE_INDEX_METAFIELD_DEFINITIONS,
    ensure_page_metafield_definitions,
)


class Command(BaseCommand):
    help = 'Create or verify Page metafield definitions for index sync'

    def add_arguments(self, parser):
        parser.add_argument(
            '--list-only',
            action='store_true',
            help='Only list existing PAGE metafield definitions; do not create.',
        )

    def handle(self, *args, **options):
        config = ShopConfig.objects.first()
        if not config:
            raise CommandError('No ShopConfig found. Install the app on a Shopify store first.')

        shop = config.shop
        self.stdout.write(f'Shop: {shop}')

        if options['list_only']:
            from shopify_content.sync.page_metafield_definitions import _existing_page_definitions

            existing = _existing_page_definitions(shop)
            if not existing:
                self.stdout.write(self.style.WARNING('No PAGE metafield definitions found.'))
                return
            for (namespace, key), node in sorted(existing.items()):
                type_name = (node.get('type') or {}).get('name', '?')
                self.stdout.write(f'  {namespace}.{key} ({type_name}) — {node.get("name")}')
            return

        for spec in PAGE_INDEX_METAFIELD_DEFINITIONS:
            self.stdout.write(
                f'  {spec.namespace}.{spec.key} ({spec.type})',
            )

        stats = ensure_page_metafield_definitions(shop)

        for key in stats['skipped']:
            self.stdout.write(self.style.SUCCESS(f'{key}: already exists'))
        for item in stats['created']:
            self.stdout.write(self.style.SUCCESS(
                f'{item["key"]}: created ({item.get("id") or "ok"})'
            ))
        for err in stats['errors']:
            self.stdout.write(self.style.ERROR(f'{err["key"]}: {err}'))

        if stats['errors']:
            raise CommandError(
                f'Failed to ensure {len(stats["errors"])} definition(s). '
                'Check scopes (write_metaobject_definitions or write_metafields) and retry.'
            )

        self.stdout.write(self.style.SUCCESS(
            f'Done. created={len(stats["created"])}, skipped={len(stats["skipped"])}.'
        ))

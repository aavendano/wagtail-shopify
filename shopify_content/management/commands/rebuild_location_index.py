"""Rebuild location index metafields on the canonical Shopify Page (handle locations)."""

import json

from django.core.management.base import BaseCommand

from shopify_content.locations.index import build_location_index_listings
from shopify_content.sync.location_index import sync_location_index_pages


class Command(BaseCommand):
    help = 'Rebuild custom.index_listings on the Shopify locations index page.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Build JSON and report stats without pushing to Shopify.',
        )

    def handle(self, *args, **options):
        stats = sync_location_index_pages(dry_run=options['dry_run'])

        if not stats['root_found']:
            self.stdout.write(self.style.WARNING('No live ShopifyRootPage with slug=local-us found.'))
            return

        if not stats['enabled']:
            reason = stats.get('failure_reason', 'unknown')
            messages = {
                'section_missing': (
                    'export_config no tiene la clave "location_index". '
                    'Ejecuta bootstrap_index_pages --apply-export-config o migrate_index_export_config.'
                ),
                'disabled': (
                    'export_config.location_index.enabled es false. '
                    'Actívalo en el root Wagtail "Local US" (slug=local-us).'
                ),
                'page_gid_missing': (
                    'export_config.location_index.page_gid falta. '
                    'Ejecuta migrate_index_export_config --apply o bootstrap_index_pages --apply-export-config.'
                ),
            }
            self.stdout.write(self.style.WARNING(messages.get(reason, (
                'Location index sync is disabled or page_gid is missing.'
            ))))
            return

        if options['dry_run']:
            payload = build_location_index_listings()
            self.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2))

        style = self.style.SUCCESS if not stats['errors'] else self.style.WARNING
        self.stdout.write(style(
            'Done. '
            f"pushed={stats['pushed']}, "
            f"errors={stats['errors']}, "
            f"dry_run={stats['dry_run']}."
        ))

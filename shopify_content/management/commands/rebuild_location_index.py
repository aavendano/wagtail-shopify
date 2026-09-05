"""Rebuild location index on root_page metaobject entries (one per locale)."""

import json

from django.core.management.base import BaseCommand

from shopify_content.locations.index import build_location_index_json
from shopify_content.sync.location_index import sync_location_index_pages


class Command(BaseCommand):
    help = 'Rebuild location index root_page metaobject entries (one per configured locale).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Build JSON and report stats without pushing to Shopify.',
        )
        parser.add_argument(
            '--locale',
            action='append',
            dest='locales',
            help='Limit rebuild to one or more locales (repeatable).',
        )

    def handle(self, *args, **options):
        locale_codes = options.get('locales') or None
        stats = sync_location_index_pages(locale_codes=locale_codes, dry_run=options['dry_run'])

        if not stats['root_found']:
            self.stdout.write(self.style.WARNING('No live ShopifyRootPage with slug=local-us found.'))
            return

        if not stats['enabled']:
            reason = stats.get('failure_reason', 'unknown')
            messages = {
                'section_missing': (
                    'export_config no tiene la clave "location_index". '
                    'Edita el root Wagtail "Local US" (slug=local-us) y pega el JSON de setup '
                    '(ver docs/shopify_content.md), p. ej. '
                    '{"location_index": {"enabled": true, "locales": ["en-US", "es-US"]}}.'
                ),
                'disabled': (
                    'export_config.location_index.enabled es false. '
                    'Actívalo en el root Wagtail "Local US" (slug=local-us).'
                ),
                'locales_empty': (
                    'export_config.location_index.locales está vacío. '
                    'Añade los códigos de locale a publicar '
                    'en el root Wagtail "Local US".'
                ),
                'consumer_not_registered': (
                    'No hay un RootIndexConsumer registrado para slug=local-us '
                    '(ver shopify_content/export_config/registry.py).'
                ),
                'title_required': 'El root Wagtail "Local US" necesita un título antes de sincronizar.',
            }
            self.stdout.write(self.style.WARNING(messages.get(reason, (
                f'Location index sync is disabled or misconfigured ({reason}).'
            ))))
            return

        if options['dry_run']:
            for locale_code in stats.get('locales') or []:
                payload = build_location_index_json(locale_code)
                self.stdout.write(f'--- locale={locale_code} ---')
                self.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2))

        style = self.style.SUCCESS if not stats['errors'] else self.style.WARNING
        self.stdout.write(style(
            'Done. '
            f"locales={stats.get('locales')}, "
            f"pushed={stats['pushed']}, "
            f"errors={stats['errors']}, "
            f"dry_run={stats['dry_run']}."
        ))

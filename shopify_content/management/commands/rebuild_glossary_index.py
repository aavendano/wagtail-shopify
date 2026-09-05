"""Rebuild glossary index on root_page metaobject entries (one per locale)."""

import json

from django.core.management.base import BaseCommand

from shopify_content.glossary.index import build_glossary_index_json
from shopify_content.sync.glossary_index import sync_glossary_index_pages


class Command(BaseCommand):
    help = 'Rebuild glossary index root_page metaobject entries (one per configured locale).'

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
        stats = sync_glossary_index_pages(locale_codes=locale_codes, dry_run=options['dry_run'])

        if not stats['root_found']:
            self.stdout.write(self.style.WARNING('No live ShopifyRootPage with slug=glossary found.'))
            return

        if not stats['enabled']:
            reason = stats.get('failure_reason', 'unknown')
            messages = {
                'section_missing': (
                    'export_config no tiene la clave "glossary_index". '
                    'Edita el root Wagtail "Glossary" (slug=glossary) y pega el JSON de setup '
                    '(ver docs/shopify_content.md), p. ej. '
                    '{"glossary_index": {"enabled": true, "locales": ["en", "es-US"]}}.'
                ),
                'disabled': (
                    'export_config.glossary_index.enabled es false. '
                    'Actívalo en el root Wagtail "Glossary" (slug=glossary).'
                ),
                'locales_empty': (
                    'export_config.glossary_index.locales está vacío. '
                    'Añade los códigos de locale a publicar '
                    'en el root Wagtail "Glossary".'
                ),
                'consumer_not_registered': (
                    'No hay un RootIndexConsumer registrado para slug=glossary '
                    '(ver shopify_content/export_config/registry.py).'
                ),
                'title_required': 'El root Wagtail "Glossary" necesita un título antes de sincronizar.',
            }
            self.stdout.write(self.style.WARNING(messages.get(reason, (
                f'Glossary index sync is disabled or misconfigured ({reason}).'
            ))))
            return

        if options['dry_run']:
            for locale_code in stats.get('locales') or []:
                payload = build_glossary_index_json(locale_code)
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

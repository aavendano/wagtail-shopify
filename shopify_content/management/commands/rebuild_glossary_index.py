"""Rebuild glossary index metafields on configured Shopify Pages."""

from django.core.management.base import BaseCommand

from shopify_content.sync.glossary_index import sync_glossary_index_pages


class Command(BaseCommand):
    help = 'Rebuild custom.glossary_index metafields on Shopify glossary index pages.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--locale',
            action='append',
            dest='locales',
            help='Locale code to rebuild (en/es/fr). Repeatable. Default: all configured.',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Build JSON and report stats without pushing to Shopify.',
        )

    def handle(self, *args, **options):
        stats = sync_glossary_index_pages(
            locale_codes=options['locales'],
            dry_run=options['dry_run'],
        )

        if not stats['root_found']:
            self.stdout.write(self.style.WARNING('No live ShopifyRootPage with slug=glossary found.'))
            return

        if not stats['enabled']:
            reason = stats.get('failure_reason', 'unknown')
            messages = {
                'section_missing': (
                    'export_config no tiene la clave "glossary_index". '
                    'Edita el root Wagtail "Glossary" (slug=glossary) y pega el JSON de setup '
                    '(ver docs/shopify_content.md o .cursor/plans/glossary-index-sync.plan.md).'
                ),
                'disabled': (
                    'export_config.glossary_index.enabled es false. '
                    'Actívalo en el root Wagtail "Glossary" (slug=glossary).'
                ),
                'pages_empty': (
                    'export_config.glossary_index.pages está vacío. '
                    'Añade los GIDs de las 3 Shopify Pages (en/es/fr) en el root Wagtail "Glossary".'
                ),
            }
            self.stdout.write(self.style.WARNING(messages.get(reason, (
                'Glossary index sync is disabled or export_config.glossary_index.pages is empty.'
            ))))
            return

        if options['dry_run']:
            from shopify_content.glossary.index import build_glossary_index_json
            import json

            for locale_code in stats['locales']:
                payload = build_glossary_index_json(locale_code)
                self.stdout.write(f'--- {locale_code} (count={payload["count"]}) ---')
                self.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2))

        style = self.style.SUCCESS if not stats['errors'] else self.style.WARNING
        self.stdout.write(style(
            'Done. '
            f"locales={stats['locales']}, "
            f"pushed={stats['pushed']}, "
            f"skipped={stats['skipped']}, "
            f"errors={stats['errors']}, "
            f"dry_run={stats['dry_run']}."
        ))

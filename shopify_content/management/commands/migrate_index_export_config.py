"""Migrate glossary/location export_config to RootIndexConsumer locales shape."""

import json

from django.core.management.base import BaseCommand, CommandError

from core.models import ShopConfig
from shopify_content.available_locales import ALLOWED_LOCALE_CODE_LIST
from shopify_content.models import ShopifyRootPage
from shopify_content.sync.index_pages_bootstrap import (
    build_glossary_export_config,
    build_location_export_config,
)


def _locales_from_legacy_section(section: dict) -> list[str]:
    """Derive locales from pages{}, page_gid-era configs, or existing locales."""
    if isinstance(section.get('locales'), list) and section['locales']:
        return list(section['locales'])
    pages = section.get('pages') or section.get('_legacy_pages') or {}
    if isinstance(pages, dict) and pages:
        return list(pages.keys())
    return list(ALLOWED_LOCALE_CODE_LIST)


class Command(BaseCommand):
    help = (
        'Migrate glossary/location export_config from pages{}/page_gid to '
        'locales[] (root_page metaobject architecture).'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--apply',
            action='store_true',
            help='Write updated export_config to Wagtail roots.',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Print planned changes without writing.',
        )

    def handle(self, *args, **options):
        config = ShopConfig.objects.first()
        if not config:
            raise CommandError('No ShopConfig found.')

        for root_slug, config_key, builder in (
            ('glossary', 'glossary_index', build_glossary_export_config),
            ('local-us', 'location_index', build_location_export_config),
        ):
            root = ShopifyRootPage.objects.filter(slug=root_slug).first()
            if root is None:
                self.stdout.write(self.style.WARNING(f'Root {root_slug} not found; skipped.'))
                continue

            export_config = dict(root.export_config or {})
            section = dict(export_config.get(config_key) or {})

            has_pages = bool(section.get('pages'))
            has_page_gid = bool(section.get('page_gid'))
            has_locales = isinstance(section.get('locales'), list) and bool(section.get('locales'))

            if has_locales and not has_pages and not has_page_gid:
                self.stdout.write(f'{root_slug}: already migrated (locales set).')
                continue

            locales = _locales_from_legacy_section(section)
            new_section = builder(locales=locales)[config_key]

            legacy_pages = section.pop('pages', None)
            legacy_page_gid = section.pop('page_gid', None)
            if legacy_pages:
                section['_legacy_pages'] = legacy_pages
            if legacy_page_gid:
                section['_legacy_page_gid'] = legacy_page_gid

            section['enabled'] = new_section.get('enabled', section.get('enabled', True))
            section['locales'] = new_section['locales']
            section.setdefault('noindex_locales', new_section.get('noindex_locales', []))
            if new_section.get('x_default_locale') and not section.get('x_default_locale'):
                section['x_default_locale'] = new_section['x_default_locale']

            export_config[config_key] = section

            self.stdout.write(f'\n--- {root_slug} export_config[{config_key}] ---')
            self.stdout.write(json.dumps({config_key: section}, indent=2))
            self.stdout.write(
                'Glossary/locations now sync via root_page metaobject entries '
                f'({config_key} locales → handles like glossary-en-us).'
            )

            if options['apply'] and not options['dry_run']:
                root.export_config = export_config
                root.save(update_fields=['export_config'])
                self.stdout.write(self.style.SUCCESS(f'Updated root {root_slug}.'))

        if options['dry_run']:
            self.stdout.write(self.style.WARNING('Dry run: no Wagtail changes written.'))

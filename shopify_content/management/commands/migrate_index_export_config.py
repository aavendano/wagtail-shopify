"""Migrate export_config from multi-page pages map to single page_gid."""

import json

from django.core.management.base import BaseCommand, CommandError

from core.models import ShopConfig
from shopify_content.models import ShopifyRootPage
from shopify_content.sync.index_pages_bootstrap import (
    GLOSSARY_INDEX_PAGE,
    LOCATION_INDEX_PAGE,
    build_glossary_export_config,
    build_location_export_config,
    ensure_index_pages,
)


class Command(BaseCommand):
    help = 'Migrate glossary/location export_config from pages{} to page_gid (single-page architecture).'

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

        shop = config.shop
        pages_by_handle = ensure_index_pages(
            shop,
            (GLOSSARY_INDEX_PAGE, LOCATION_INDEX_PAGE),
        )

        for root_slug, config_key, builder, page_spec in (
            ('glossary', 'glossary_index', build_glossary_export_config, GLOSSARY_INDEX_PAGE),
            ('local-us', 'location_index', build_location_export_config, LOCATION_INDEX_PAGE),
        ):
            root = ShopifyRootPage.objects.filter(slug=root_slug).first()
            if root is None:
                self.stdout.write(self.style.WARNING(f'Root {root_slug} not found; skipped.'))
                continue

            export_config = dict(root.export_config or {})
            section = dict(export_config.get(config_key) or {})
            new_section = builder(pages_by_handle)[config_key]

            if section.get('page_gid') == new_section.get('page_gid'):
                self.stdout.write(f'{root_slug}: already migrated (page_gid set).')
                continue

            legacy_pages = section.pop('pages', None)
            if legacy_pages:
                section['_legacy_pages'] = legacy_pages
            section['enabled'] = new_section.get('enabled', True)
            section['page_gid'] = new_section['page_gid']
            export_config[config_key] = section

            self.stdout.write(f'\n--- {root_slug} export_config[{config_key}] ---')
            self.stdout.write(json.dumps({config_key: section}, indent=2))
            self.stdout.write(
                f'Assign template page.{page_spec.template_suffix} to handle '
                f'{page_spec.handle} in Theme Editor.'
            )
            self.stdout.write(
                'Optional: add Shopify URL redirects from legacy index handles to '
                f'/pages/{page_spec.handle}.'
            )

            if options['apply'] and not options['dry_run']:
                root.export_config = export_config
                root.save(update_fields=['export_config'])
                self.stdout.write(self.style.SUCCESS(f'Updated root {root_slug}.'))

        if options['dry_run']:
            self.stdout.write(self.style.WARNING('Dry run: no Wagtail changes written.'))

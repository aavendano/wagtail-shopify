"""
Create Shopify Pages for glossary/location/blog index sync and print export_config GIDs.

Usage:
    python manage.py bootstrap_index_pages
    python manage.py bootstrap_index_pages --apply-export-config
    python manage.py bootstrap_index_pages --legacy-pages
"""

import json

from django.core.management.base import BaseCommand, CommandError

from core.models import ShopConfig
from shopify_content.models import ShopifyRootPage
from shopify_content.sync.index_pages_bootstrap import (
    BLOG_INDEX_PAGE,
    GLOSSARY_INDEX_PAGE,
    LEGACY_GLOSSARY_INDEX_PAGES,
    LEGACY_LOCATION_INDEX_PAGES,
    LOCATION_INDEX_PAGE,
    LOCATION_LEGACY_ALIAS_PAGES,
    build_blog_export_config,
    build_glossary_export_config,
    build_location_export_config,
    ensure_index_pages,
)
from shopify_content.sync.resource_metafield_definitions import ensure_index_metafield_definitions


class Command(BaseCommand):
    help = 'Create glossary/location/blog index Shopify Pages and show export_config JSON'

    def add_arguments(self, parser):
        parser.add_argument(
            '--apply-export-config',
            action='store_true',
            help='Merge generated GIDs into ShopifyRootPage.export_config in Wagtail DB.',
        )
        parser.add_argument(
            '--skip-metafield-definitions',
            action='store_true',
            help='Do not run metafield definition ensure commands first.',
        )
        parser.add_argument(
            '--legacy-pages',
            action='store_true',
            help='Also create deprecated per-locale index Pages (glossary-en, locations-en-us, etc.).',
        )

    def handle(self, *args, **options):
        config = ShopConfig.objects.first()
        if not config:
            raise CommandError('No ShopConfig found.')

        shop = config.shop
        self.stdout.write(f'Shop: {shop}')

        if not options['skip_metafield_definitions']:
            self.stdout.write('Ensuring index metafield definitions...')
            def_stats = ensure_index_metafield_definitions(shop)
            if def_stats['page']['errors']:
                raise CommandError(f'Page metafield definition errors: {def_stats["page"]["errors"]}')
            for scope in ('blog', 'article'):
                if def_stats[scope]['errors']:
                    raise CommandError(
                        f'Resource metafield definition errors ({scope}): {def_stats[scope]["errors"]}'
                    )

        canonical_specs = (GLOSSARY_INDEX_PAGE, LOCATION_INDEX_PAGE, BLOG_INDEX_PAGE)
        pages_by_handle = ensure_index_pages(shop, canonical_specs)

        if options['legacy_pages']:
            legacy_pages = ensure_index_pages(
                shop,
                LEGACY_GLOSSARY_INDEX_PAGES + LEGACY_LOCATION_INDEX_PAGES + LOCATION_LEGACY_ALIAS_PAGES,
            )
            pages_by_handle.update(legacy_pages)

        for handle, node in pages_by_handle.items():
            flag = 'created' if node.get('created') else 'exists'
            self.stdout.write(f'  [{flag}] {handle} → {node["id"]}')

        glossary_config = build_glossary_export_config(pages_by_handle)
        location_config = build_location_export_config(pages_by_handle)
        blog_config = build_blog_export_config(pages_by_handle)

        self.stdout.write('\n--- Pegar en ShopifyRootPage slug=glossary (export_config) ---')
        self.stdout.write(json.dumps(glossary_config, indent=2))

        self.stdout.write('\n--- Pegar en ShopifyRootPage slug=local-us (export_config) ---')
        self.stdout.write(json.dumps(location_config, indent=2))

        self.stdout.write('\n--- Pegar en ShopifyRootPage slug=blogs (export_config) ---')
        self.stdout.write(json.dumps(blog_config, indent=2))

        if options['apply_export_config']:
            self._apply_config('glossary', 'glossary_index', glossary_config['glossary_index'])
            self._apply_config('local-us', 'location_index', location_config['location_index'])
            self._apply_config('blogs', 'blog_index', blog_config['blog_index'])
            self.stdout.write(self.style.SUCCESS('\nexport_config actualizado en Wagtail.'))

    def _apply_config(self, root_slug: str, config_key: str, section: dict) -> None:
        root = ShopifyRootPage.objects.filter(slug=root_slug).first()
        if root is None:
            self.stdout.write(self.style.WARNING(f'Root slug={root_slug} not found; skipped.'))
            return
        export_config = dict(root.export_config or {})
        export_config[config_key] = section
        root.export_config = export_config
        root.save(update_fields=['export_config'])
        self.stdout.write(self.style.SUCCESS(
            f'Updated export_config[{config_key}] on root {root_slug} (id={root.pk}).'
        ))

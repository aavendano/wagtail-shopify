"""
Bootstrap Shopify index targets.

Blog still uses a native Shopify Page + custom.index_listings (page_gid).
Glossary/locations use root_page metaobject entries (locales in export_config);
this command only prints/applies their locales config — no Page bootstrap.

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
    help = (
        'Create blog index Shopify Page + print/apply export_config for '
        'glossary/locations (locales) and blog (page_gid).'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--apply-export-config',
            action='store_true',
            help='Merge generated config into ShopifyRootPage.export_config in Wagtail DB.',
        )
        parser.add_argument(
            '--skip-metafield-definitions',
            action='store_true',
            help='Do not run metafield definition ensure commands first.',
        )
        parser.add_argument(
            '--legacy-pages',
            action='store_true',
            help=(
                'Also create deprecated glossary/locations Shopify Pages '
                '(not used by the root_page metaobject sync path).'
            ),
        )

    def handle(self, *args, **options):
        config = ShopConfig.objects.first()
        if not config:
            raise CommandError('No ShopConfig found.')

        shop = config.shop
        self.stdout.write(f'Shop: {shop}')

        if not options['skip_metafield_definitions']:
            self.stdout.write('Ensuring index metafield definitions (blog Page path)...')
            def_stats = ensure_index_metafield_definitions(shop)
            if def_stats['page']['errors']:
                raise CommandError(f'Page metafield definition errors: {def_stats["page"]["errors"]}')
            for scope in ('blog', 'article'):
                if def_stats[scope]['errors']:
                    raise CommandError(
                        f'Resource metafield definition errors ({scope}): {def_stats[scope]["errors"]}'
                    )

        pages_by_handle = ensure_index_pages(shop, (BLOG_INDEX_PAGE,))

        if options['legacy_pages']:
            legacy_pages = ensure_index_pages(
                shop,
                (GLOSSARY_INDEX_PAGE, LOCATION_INDEX_PAGE)
                + LEGACY_GLOSSARY_INDEX_PAGES
                + LEGACY_LOCATION_INDEX_PAGES
                + LOCATION_LEGACY_ALIAS_PAGES,
            )
            pages_by_handle.update(legacy_pages)

        for handle, node in pages_by_handle.items():
            flag = 'created' if node.get('created') else 'exists'
            self.stdout.write(f'  [{flag}] {handle} → {node["id"]}')

        glossary_config = build_glossary_export_config()
        location_config = build_location_export_config()
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

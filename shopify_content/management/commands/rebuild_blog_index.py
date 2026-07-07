"""Rebuild blog index listings metafield on the Shopify Page handle blogs."""

from django.core.management.base import BaseCommand

from shopify_content.sync.blog_index import sync_blog_index_listings


class Command(BaseCommand):
    help = 'Rebuild custom.index_listings on the Shopify Page handle blogs.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Build JSON and report stats without pushing to Shopify.',
        )

    def handle(self, *args, **options):
        stats = sync_blog_index_listings(dry_run=options['dry_run'])

        if not stats['root_found']:
            self.stdout.write(self.style.WARNING('No live ShopifyRootPage with slug=blogs found.'))
            return

        if not stats['enabled']:
            reason = stats.get('failure_reason', 'unknown')
            messages = {
                'section_missing': (
                    'export_config no tiene la clave "blog_index". '
                    'Edita el root Wagtail "Blogs" (slug=blogs) o ejecuta bootstrap_index_pages.'
                ),
                'disabled': (
                    'export_config.blog_index.enabled es false. '
                    'Actívalo en el root Wagtail "Blogs" (slug=blogs).'
                ),
                'page_gid_missing': (
                    'export_config.blog_index.page_gid está vacío. '
                    'Ejecuta bootstrap_index_pages --apply-export-config.'
                ),
            }
            self.stdout.write(self.style.WARNING(messages.get(reason, (
                'Blog index sync is disabled or export_config.blog_index.page_gid is missing.'
            ))))
            return

        if options['dry_run']:
            from shopify_content.blogs.index import build_blog_index_listings
            import json

            payload = build_blog_index_listings()
            for locale_code, listing in payload['locales'].items():
                self.stdout.write(f'--- {locale_code} (count={listing["count"]}) ---')
                self.stdout.write(json.dumps(listing, ensure_ascii=False, indent=2))

        style = self.style.SUCCESS if not stats['errors'] else self.style.WARNING
        self.stdout.write(style(
            'Done. '
            f"pushed={stats['pushed']}, "
            f"skipped={stats['skipped']}, "
            f"errors={stats['errors']}, "
            f"dry_run={stats['dry_run']}."
        ))

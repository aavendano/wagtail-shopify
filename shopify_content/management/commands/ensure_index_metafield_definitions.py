"""Ensure Shopify metafield definitions for CMS index pages and blog resources."""

from django.core.management.base import BaseCommand, CommandError

from shopify_config.tenancy import (
    ShopUnresolvedError,
    add_shop_argument,
    resolve_shop_for_command_or_sole,
)
from shopify_content.sync.page_metafield_definitions import (
    LEGACY_PAGE_INDEX_METAFIELD_DEFINITIONS,
    ensure_page_metafield_definitions,
)
from shopify_content.sync.resource_metafield_definitions import ensure_index_metafield_definitions


class Command(BaseCommand):
    help = 'Ensure custom.index_listings (PAGE) and blog/article available_locales definitions.'

    def add_arguments(self, parser):
        add_shop_argument(parser)
        parser.add_argument(
            '--legacy',
            action='store_true',
            help='Also ensure deprecated per-locale index metafield definitions.',
        )

    def handle(self, *args, **options):
        try:
            shop = resolve_shop_for_command_or_sole(shop=options.get('shop') or None)
        except ShopUnresolvedError as exc:
            raise CommandError(str(exc)) from exc

        stats = ensure_index_metafield_definitions(shop)
        self._report('page', stats['page'])
        self._report('blog', stats['blog'])
        self._report('article', stats['article'])

        if options['legacy']:
            legacy_stats = ensure_page_metafield_definitions(
                shop,
                specs=LEGACY_PAGE_INDEX_METAFIELD_DEFINITIONS,
            )
            self._report('legacy PAGE', legacy_stats)

    def _report(self, label: str, stats: dict) -> None:
        if stats['errors']:
            raise CommandError(f'{label} metafield definition errors: {stats["errors"]}')
        self.stdout.write(
            f'{label}: created={stats["created"]}, skipped={stats["skipped"]}'
        )

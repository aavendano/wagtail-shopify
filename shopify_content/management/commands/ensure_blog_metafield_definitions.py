"""Ensure Shopify metafield definitions for blog index and blog/article locales."""

from django.core.management.base import BaseCommand, CommandError

from shopify_config.tenancy import (
    ShopUnresolvedError,
    add_shop_argument,
    resolve_shop_for_command_or_sole,
)
from shopify_content.sync.resource_metafield_definitions import ensure_blog_metafield_definitions


class Command(BaseCommand):
    help = (
        'Create Shopify metafield definitions for blog index listings (PAGE), '
        'and available_locales on BLOG and ARTICLE resources.'
    )

    def add_arguments(self, parser):
        add_shop_argument(parser)

    def handle(self, *args, **options):
        try:
            shop = resolve_shop_for_command_or_sole(shop=options.get('shop') or None)
        except ShopUnresolvedError as exc:
            raise CommandError(str(exc)) from exc
        self.stdout.write(f'Shop: {shop}')

        stats = ensure_blog_metafield_definitions(shop)
        for scope, scope_stats in stats.items():
            self.stdout.write(
                f'  [{scope}] created={scope_stats["created"]} '
                f'skipped={scope_stats["skipped"]} errors={scope_stats["errors"]}'
            )
            if scope_stats['errors']:
                raise CommandError(f'Metafield definition errors ({scope}): {scope_stats["errors"]}')

        self.stdout.write(self.style.SUCCESS('Blog metafield definitions ensured.'))

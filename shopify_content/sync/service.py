"""
Orchestration layer for Shopify → Wagtail inbound imports.

Used by the REST API, Wagtail admin sync UI, and management commands.
"""

from typing import Literal, TypedDict

from .inbound import (
    _get_shop,
    import_products,
    import_collections,
    import_blogs_and_articles,
)
from .import_parents import resolve_shopify_import_parent

ImportResource = Literal['products', 'collections', 'blogs', 'all']

VALID_IMPORT_RESOURCES = frozenset({'products', 'collections', 'blogs', 'all'})


class ImportStats(TypedDict):
    created: int
    updated: int
    skipped: int
    errors: int


def _format_stats_message(label: str, stats: ImportStats, *, new_only: bool) -> str:
    parts = [
        f'{label} — Creados: {stats["created"]}',
        f'Omitidos: {stats["skipped"]}' if new_only else f'Actualizados: {stats["updated"]}',
        f'Errores: {stats["errors"]}',
    ]
    return ', '.join(parts)


def _merge_stats(target: ImportStats, source: ImportStats) -> None:
    for key in ('created', 'updated', 'skipped', 'errors'):
        target[key] += source[key]


def _empty_stats() -> ImportStats:
    return {'created': 0, 'updated': 0, 'skipped': 0, 'errors': 0}


def _import_products(shop, *, new_only: bool) -> ImportStats:
    parent = resolve_shopify_import_parent('products')
    return import_products(shop, parent, new_only=new_only)


def _import_collections(shop, *, new_only: bool) -> ImportStats:
    parent = resolve_shopify_import_parent('collections')
    return import_collections(shop, parent, new_only=new_only)


def _import_blogs(shop, *, new_only: bool) -> dict:
    parent = resolve_shopify_import_parent('blogs')
    return import_blogs_and_articles(shop, parent, new_only=new_only)


def import_error_count(stats: dict, resource: ImportResource) -> int:
    if resource == 'blogs':
        return stats['blogs']['errors'] + stats['articles']['errors']
    return stats['errors']


def run_shopify_import(resource: ImportResource, *, new_only: bool = False) -> dict:
    """
    Run inbound import for one or all Shopify resource types.

    Returns a dict with keys:
      - resource: requested resource type
      - stats: per-resource stats (flat for products/collections; nested for blogs)
      - message: human-readable summary
    """
    shop = _get_shop()

    if resource == 'products':
        stats = _import_products(shop, new_only=new_only)
        return {
            'resource': resource,
            'stats': stats,
            'message': _format_stats_message('Productos', stats, new_only=new_only),
        }

    if resource == 'collections':
        stats = _import_collections(shop, new_only=new_only)
        return {
            'resource': resource,
            'stats': stats,
            'message': _format_stats_message('Colecciones', stats, new_only=new_only),
        }

    if resource == 'blogs':
        result = _import_blogs(shop, new_only=new_only)
        blog_stats = result['blogs']
        article_stats = result['articles']
        return {
            'resource': resource,
            'stats': result,
            'message': (
                f'{_format_stats_message("Blogs", blog_stats, new_only=new_only)}. '
                f'{_format_stats_message("Artículos", article_stats, new_only=new_only)}.'
            ),
        }

    if resource == 'all':
        products_stats = _import_products(shop, new_only=new_only)
        collections_stats = _import_collections(shop, new_only=new_only)
        blogs_result = _import_blogs(shop, new_only=new_only)
        combined = _empty_stats()
        _merge_stats(combined, products_stats)
        _merge_stats(combined, collections_stats)
        _merge_stats(combined, blogs_result['blogs'])
        _merge_stats(combined, blogs_result['articles'])
        message = ' | '.join([
            _format_stats_message('Productos', products_stats, new_only=new_only),
            _format_stats_message('Colecciones', collections_stats, new_only=new_only),
            _format_stats_message('Blogs', blogs_result['blogs'], new_only=new_only),
            _format_stats_message('Artículos', blogs_result['articles'], new_only=new_only),
        ])
        return {
            'resource': resource,
            'stats': combined,
            'details': {
                'products': products_stats,
                'collections': collections_stats,
                'blogs': blogs_result,
            },
            'message': message,
        }

    raise ValueError(f'Unknown resource: {resource}')


def run_shopify_import_for_api(resource: ImportResource, *, new_only: bool = False) -> dict:
    """
    API-friendly wrapper returning flat created/updated/skipped/errors/message fields.
    """
    result = run_shopify_import(resource, new_only=new_only)
    stats = result['stats']

    if resource == 'blogs':
        blog_stats = stats['blogs']
        article_stats = stats['articles']
        return {
            'created': blog_stats['created'],
            'updated': blog_stats['updated'],
            'skipped': blog_stats['skipped'],
            'errors': blog_stats['errors'] + article_stats['errors'],
            'message': result['message'],
        }

    return {**stats, 'message': result['message']}

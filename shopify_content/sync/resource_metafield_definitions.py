"""Ensure Shopify metafield definitions for blog/article resources and blog index Page."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from shopify_requests.graphql_service import execute_admin_graphql

from shopify_content.sync.page_metafield_definitions import (
    PAGE_INDEX_LISTINGS_DEFINITION,
    ensure_page_metafield_definitions,
)

logger = logging.getLogger(__name__)

METAFIELD_DEFINITIONS_QUERY = """
query ResourceMetafieldDefinitions($ownerType: MetafieldOwnerType!) {
  metafieldDefinitions(first: 50, ownerType: $ownerType) {
    edges {
      node {
        id
        name
        namespace
        key
        type {
          name
        }
      }
    }
  }
}
"""

METAFIELD_DEFINITION_CREATE = """
mutation MetafieldDefinitionCreate($definition: MetafieldDefinitionInput!) {
  metafieldDefinitionCreate(definition: $definition) {
    createdDefinition {
      id
      name
      namespace
      key
      type {
        name
      }
    }
    userErrors {
      field
      message
      code
    }
  }
}
"""


@dataclass(frozen=True)
class ResourceMetafieldDefinitionSpec:
    name: str
    namespace: str
    key: str
    type: str
    description: str
    owner_type: str



BLOG_INDEX_PAGE_METAFIELD_DEFINITION = PAGE_INDEX_LISTINGS_DEFINITION

BLOG_RESOURCE_METAFIELD_DEFINITIONS: tuple[ResourceMetafieldDefinitionSpec, ...] = (
    ResourceMetafieldDefinitionSpec(
        name='Available locales',
        namespace='custom',
        key='available_locales',
        type='list.single_line_text_field',
        description='Wagtail locale codes where this blog is available (en-US, es-US, etc.).',
        owner_type='BLOG',
    ),
)

ARTICLE_RESOURCE_METAFIELD_DEFINITIONS: tuple[ResourceMetafieldDefinitionSpec, ...] = (
    ResourceMetafieldDefinitionSpec(
        name='Available locales',
        namespace='custom',
        key='available_locales',
        type='list.single_line_text_field',
        description='Wagtail locale codes where this article is available (en-US, es-US, etc.).',
        owner_type='ARTICLE',
    ),
)


def _existing_definitions(shop: str, owner_type: str) -> dict[tuple[str, str], dict]:
    result = execute_admin_graphql(
        METAFIELD_DEFINITIONS_QUERY,
        shop=shop,
        variables={'ownerType': owner_type},
    )
    if not result.ok:
        raise RuntimeError(
            f'metafieldDefinitions query failed owner={owner_type}: '
            f'{result.error_code} {result.log_detail}'
        )
    edges = (result.data or {}).get('metafieldDefinitions', {}).get('edges', [])
    return {
        (node['namespace'], node['key']): node
        for edge in edges
        for node in [edge.get('node') or {}]
        if node.get('namespace') and node.get('key')
    }


def _ensure_resource_definitions(
    shop: str,
    specs: tuple[ResourceMetafieldDefinitionSpec, ...],
) -> dict:
    stats = {'created': [], 'skipped': [], 'errors': []}
    if not specs:
        return stats

    owner_type = specs[0].owner_type
    existing = _existing_definitions(shop, owner_type)

    for spec in specs:
        lookup = (spec.namespace, spec.key)
        if lookup in existing:
            stats['skipped'].append(spec.key)
            continue

        result = execute_admin_graphql(
            METAFIELD_DEFINITION_CREATE,
            shop=shop,
            variables={
                'definition': {
                    'name': spec.name,
                    'namespace': spec.namespace,
                    'key': spec.key,
                    'description': spec.description,
                    'type': spec.type,
                    'ownerType': spec.owner_type,
                },
            },
        )
        if not result.ok:
            stats['errors'].append({
                'key': spec.key,
                'owner': spec.owner_type,
                'error': result.error_code,
                'detail': result.log_detail,
            })
            continue

        payload = (result.data or {}).get('metafieldDefinitionCreate', {})
        user_errors = payload.get('userErrors') or []
        if user_errors:
            stats['errors'].append({
                'key': spec.key,
                'owner': spec.owner_type,
                'userErrors': user_errors,
            })
            continue

        created = payload.get('createdDefinition') or {}
        stats['created'].append({
            'key': spec.key,
            'owner': spec.owner_type,
            'id': created.get('id'),
        })

    return stats


def ensure_index_metafield_definitions(shop: str) -> dict:
    """
    Ensure Page index_listings plus Blog/Article metafield definitions.

    Safe to re-run (idempotent).
    """
    page_stats = ensure_page_metafield_definitions(
        shop,
        specs=(PAGE_INDEX_LISTINGS_DEFINITION,),
    )
    blog_stats = _ensure_resource_definitions(shop, BLOG_RESOURCE_METAFIELD_DEFINITIONS)
    article_stats = _ensure_resource_definitions(shop, ARTICLE_RESOURCE_METAFIELD_DEFINITIONS)

    return {
        'page': page_stats,
        'blog': blog_stats,
        'article': article_stats,
    }


def ensure_blog_metafield_definitions(shop: str) -> dict:
    """Backward-compatible alias for ensure_index_metafield_definitions."""
    return ensure_index_metafield_definitions(shop)

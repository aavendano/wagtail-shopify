"""Ensure Shopify Page metafield definitions for index sync consumers."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from shopify_requests.graphql_service import execute_admin_graphql

logger = logging.getLogger(__name__)

METAFIELD_DEFINITIONS_QUERY = """
query PageMetafieldDefinitions($ownerType: MetafieldOwnerType!) {
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
class PageMetafieldDefinitionSpec:
    name: str
    namespace: str
    key: str
    type: str
    description: str


PAGE_INDEX_LISTINGS_DEFINITION = PageMetafieldDefinitionSpec(
    name='Index listings',
    namespace='custom',
    key='index_listings',
    type='json',
    description=(
        'Precomputed multi-locale index listings JSON from Wagtail '
        '(blog, glossary, locations).'
    ),
)

# Deprecated: multi-page index architecture. Not created by default.
LEGACY_PAGE_INDEX_METAFIELD_DEFINITIONS: tuple[PageMetafieldDefinitionSpec, ...] = (
    PageMetafieldDefinitionSpec(
        name='Glossary locale',
        namespace='custom',
        key='glossary_locale',
        type='single_line_text_field',
        description='Locale code for the glossary index page (en, es, fr).',
    ),
    PageMetafieldDefinitionSpec(
        name='Glossary index',
        namespace='custom',
        key='glossary_index',
        type='json',
        description='Precomputed A–Z glossary index JSON from Wagtail.',
    ),
    PageMetafieldDefinitionSpec(
        name='Location locale',
        namespace='custom',
        key='location_locale',
        type='single_line_text_field',
        description='Locale code for the location index page (e.g. en-US).',
    ),
    PageMetafieldDefinitionSpec(
        name='Location index',
        namespace='custom',
        key='location_index',
        type='json',
        description='Precomputed location index JSON grouped by state from Wagtail.',
    ),
    PageMetafieldDefinitionSpec(
        name='Index alternates',
        namespace='custom',
        key='index_alternates',
        type='json',
        description=(
            'Reciprocal hreflang/locale-switcher contract for a CMS index Page '
            '(shared by any PageIndexConsumer: glossary, location, or future types).'
        ),
    ),
    PageMetafieldDefinitionSpec(
        name='Index noindex',
        namespace='custom',
        key='index_noindex',
        type='boolean',
        description='Whether this CMS index Page should be marked noindex in robots meta.',
    ),
)


PAGE_INDEX_METAFIELD_DEFINITIONS: tuple[PageMetafieldDefinitionSpec, ...] = (
    PAGE_INDEX_LISTINGS_DEFINITION,
)


def _existing_page_definitions(shop: str) -> dict[tuple[str, str], dict]:
    result = execute_admin_graphql(
        METAFIELD_DEFINITIONS_QUERY,
        shop=shop,
        variables={'ownerType': 'PAGE'},
    )
    if not result.ok:
        raise RuntimeError(
            f'metafieldDefinitions query failed: {result.error_code} {result.log_detail}'
        )
    edges = (result.data or {}).get('metafieldDefinitions', {}).get('edges', [])
    return {
        (node['namespace'], node['key']): node
        for edge in edges
        for node in [edge.get('node') or {}]
        if node.get('namespace') and node.get('key')
    }


def ensure_page_metafield_definitions(
    shop: str,
    *,
    specs: tuple[PageMetafieldDefinitionSpec, ...] | None = None,
) -> dict:
    """
    Create missing Page metafield definitions. Safe to re-run.

    Returns stats: created, skipped, errors.
    """
    specs = specs or PAGE_INDEX_METAFIELD_DEFINITIONS
    existing = _existing_page_definitions(shop)
    stats = {'created': [], 'skipped': [], 'errors': []}

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
                    'ownerType': 'PAGE',
                },
            },
        )
        if not result.ok:
            stats['errors'].append({
                'key': spec.key,
                'error': result.error_code,
                'detail': result.log_detail,
            })
            continue

        payload = (result.data or {}).get('metafieldDefinitionCreate', {})
        user_errors = payload.get('userErrors') or []
        if user_errors:
            stats['errors'].append({'key': spec.key, 'userErrors': user_errors})
            continue

        created = payload.get('createdDefinition') or {}
        stats['created'].append({
            'key': spec.key,
            'id': created.get('id'),
        })

    return stats

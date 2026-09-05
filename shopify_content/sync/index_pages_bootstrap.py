"""Bootstrap Shopify Pages used as glossary/location/blog index targets."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from shopify_requests.graphql_service import execute_admin_graphql

logger = logging.getLogger(__name__)

PAGES_QUERY = """
query ListPages($query: String) {
  pages(first: 5, query: $query) {
    edges {
      node {
        id
        title
        handle
      }
    }
  }
}
"""

PAGE_CREATE = """
mutation PageCreate($page: PageCreateInput!) {
  pageCreate(page: $page) {
    page {
      id
      title
      handle
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
class IndexPageSpec:
    handle: str
    title: str
    body: str
    template_suffix: str | None = None


GLOSSARY_INDEX_PAGE = IndexPageSpec(
    handle='glossary',
    title='Glossary',
    body='<p>A–Z glossary index. Content is rendered from Wagtail via metafields.</p>',
    template_suffix='glossary',
)

LOCATION_INDEX_PAGE = IndexPageSpec(
    handle='locations',
    title='Locations',
    body='<p>Location index by state. Content is rendered from Wagtail via metafields.</p>',
    template_suffix='locations',
)

BLOG_INDEX_PAGE = IndexPageSpec(
    handle='blogs',
    title='Blog',
    body='<p>Editorial blog index. Listings are rendered from Wagtail via metafields.</p>',
    template_suffix='blogs',
)

# Legacy multi-page specs (deprecated; use --legacy-pages to recreate).
LEGACY_GLOSSARY_INDEX_PAGES: tuple[IndexPageSpec, ...] = (
    IndexPageSpec(
        handle='glossary-en',
        title='Glossary (English)',
        body='<p>A–Z glossary index. Content is rendered from Wagtail via metafields.</p>',
    ),
    IndexPageSpec(
        handle='glossary-es',
        title='Glosario (Español)',
        body='<p>Índice A–Z del glosario. El contenido se renderiza desde Wagtail vía metafields.</p>',
    ),
    IndexPageSpec(
        handle='glossary-fr',
        title='Glossaire (Français)',
        body='<p>Index A–Z du glossaire. Le contenu est rendu depuis Wagtail via metafields.</p>',
    ),
)

LEGACY_LOCATION_INDEX_PAGES: tuple[IndexPageSpec, ...] = (
    IndexPageSpec(
        handle='locations-en-us',
        title='Locations (English)',
        body='<p>Location index by state. Content is rendered from Wagtail via metafields.</p>',
        template_suffix='locations',
    ),
    IndexPageSpec(
        handle='locations-es-us',
        title='Ubicaciones (Español)',
        body='<p>Índice de ubicaciones por estado. El contenido se renderiza desde Wagtail vía metafields.</p>',
        template_suffix='locations',
    ),
)

LOCATION_LEGACY_ALIAS_PAGES: tuple[IndexPageSpec, ...] = (
    IndexPageSpec(
        handle='locations-en',
        title='Locations (English)',
        body='<p>Redirecting to the locations index…</p>',
        template_suffix='locations-redirect',
    ),
    IndexPageSpec(
        handle='locations-es',
        title='Ubicaciones (Español)',
        body='<p>Redirigiendo al índice de ubicaciones…</p>',
        template_suffix='locations-redirect',
    ),
)


def build_single_page_export_config(
    pages_by_handle: dict[str, dict],
    *,
    handle: str,
    config_key: str,
) -> dict:
    node = pages_by_handle.get(handle)
    if not node:
        return {config_key: {'enabled': False, 'page_gid': None}}
    return {
        config_key: {
            'enabled': True,
            'page_gid': node['id'],
        },
    }


def build_blog_export_config(pages_by_handle: dict[str, dict]) -> dict:
    return build_single_page_export_config(
        pages_by_handle,
        handle='blogs',
        config_key='blog_index',
    )


def build_root_index_export_config(
    *,
    config_key: str,
    locales: list[str],
    x_default_locale: str | None = None,
) -> dict:
    """export_config shape for RootIndexConsumer families (glossary/locations)."""
    section: dict = {
        'enabled': True,
        'locales': list(locales),
        'noindex_locales': [],
    }
    if x_default_locale:
        section['x_default_locale'] = x_default_locale
    return {config_key: section}


def build_glossary_export_config(
    pages_by_handle: dict[str, dict] | None = None,
    *,
    locales: list[str] | None = None,
) -> dict:
    """Glossary uses root_page metaobject entries; pages_by_handle is ignored."""
    from shopify_content.available_locales import ALLOWED_LOCALE_CODE_LIST

    locale_list = list(locales or ALLOWED_LOCALE_CODE_LIST)
    return build_root_index_export_config(
        config_key='glossary_index',
        locales=locale_list,
        x_default_locale=locale_list[0] if locale_list else None,
    )


def build_location_export_config(
    pages_by_handle: dict[str, dict] | None = None,
    *,
    locales: list[str] | None = None,
) -> dict:
    """Locations use root_page metaobject entries; pages_by_handle is ignored."""
    from shopify_content.available_locales import ALLOWED_LOCALE_CODE_LIST

    locale_list = list(locales or ALLOWED_LOCALE_CODE_LIST)
    return build_root_index_export_config(
        config_key='location_index',
        locales=locale_list,
        x_default_locale=locale_list[0] if locale_list else None,
    )


def _find_page_by_handle(shop: str, handle: str) -> dict | None:
    result = execute_admin_graphql(
        PAGES_QUERY,
        shop=shop,
        variables={'query': f'handle:{handle}'},
    )
    if not result.ok:
        raise RuntimeError(
            f'pages query failed for handle={handle}: {result.error_code} {result.log_detail}'
        )
    edges = (result.data or {}).get('pages', {}).get('edges', [])
    return edges[0]['node'] if edges else None


def _create_page(shop: str, spec: IndexPageSpec) -> dict:
    page_input: dict = {
        'title': spec.title,
        'handle': spec.handle,
        'body': spec.body,
        'isPublished': True,
    }
    if spec.template_suffix:
        page_input['templateSuffix'] = spec.template_suffix
    result = execute_admin_graphql(
        PAGE_CREATE,
        shop=shop,
        variables={'page': page_input},
    )
    if not result.ok:
        raise RuntimeError(
            f'pageCreate failed handle={spec.handle}: {result.error_code} {result.log_detail}'
        )
    payload = (result.data or {}).get('pageCreate', {})
    user_errors = payload.get('userErrors') or []
    if user_errors:
        raise RuntimeError(f'pageCreate userErrors handle={spec.handle}: {user_errors}')
    page = payload.get('page')
    if not page:
        raise RuntimeError(f'pageCreate returned no page for handle={spec.handle}')
    return page


def ensure_index_pages(
    shop: str,
    specs: tuple[IndexPageSpec, ...],
) -> dict[str, dict]:
    """Return handle -> {id, title, handle, created} for each spec."""
    results: dict[str, dict] = {}
    for spec in specs:
        existing = _find_page_by_handle(shop, spec.handle)
        if existing:
            results[spec.handle] = {**existing, 'created': False}
            continue
        page = _create_page(shop, spec)
        results[spec.handle] = {**page, 'created': True}
    return results

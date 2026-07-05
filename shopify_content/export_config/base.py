"""Base types for export_config index consumers."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

from shopify_content.sync.outbound import _get_shop, _push_metafields
from shopify_requests.graphql_service import execute_admin_graphql

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

METAFIELD_NAMESPACE = 'custom'
ALTERNATES_KEY = 'index_alternates'
NOINDEX_KEY = 'index_noindex'

NODE_HANDLES_QUERY = """
query IndexPageHandles($ids: [ID!]!) {
  nodes(ids: $ids) {
    id
    ... on Page {
      handle
    }
  }
}
"""


def _resolve_page_handles(shop: str, gids: list[str]) -> dict[str, str]:
    """Return {gid: handle} for the given Shopify Page GIDs."""
    if not gids:
        return {}
    result = execute_admin_graphql(NODE_HANDLES_QUERY, shop=shop, variables={'ids': gids})
    if not result.ok:
        logger.error(
            'nodes query for index page handles failed shop=%s error=%s detail=%s',
            shop, result.error_code, result.log_detail,
        )
        return {}
    nodes = (result.data or {}).get('nodes') or []
    return {
        node['id']: node['handle']
        for node in nodes
        if node and node.get('handle')
    }


@dataclass(frozen=True)
class IndexMetafieldSpec:
    locale_key: str
    index_key: str


class PageIndexConsumer:
    """
    Sync precomputed JSON index payloads to Shopify Pages via metafieldsSet.

    Subclasses set root_slug, config_key, and index_metafields.
    """

    root_slug: str
    config_key: str
    index_metafields: IndexMetafieldSpec

    def get_root_page(self):
        from shopify_content.models import ShopifyRootPage

        return (
            ShopifyRootPage.objects.live()
            .filter(slug=self.root_slug)
            .first()
        )

    def get_config(self, root=None) -> dict | None:
        root = root or self.get_root_page()
        if root is None:
            return None
        export_config = root.export_config or {}
        section = export_config.get(self.config_key) or {}
        if not section.get('enabled'):
            return None
        pages = section.get('pages') or {}
        if not isinstance(pages, dict) or not pages:
            return None
        return section

    def configured_locales(self, config: dict, locale_codes: list[str] | None) -> list[str]:
        pages = config.get('pages') or {}
        available = [code for code, gid in pages.items() if gid]
        if locale_codes:
            return [code for code in locale_codes if code in available]
        return available

    def build_payload(self, locale_code: str) -> dict:
        raise NotImplementedError

    def locale_codes_for_page(self, page) -> list[str] | None:
        """Return locale keys to rebuild when a child page changes; None to skip."""
        return None

    def hreflang_for_locale(self, locale_code: str) -> str:
        """Map an internal locale code (e.g. 'en-US') to an hreflang value."""
        return locale_code.replace('_', '-')

    def is_noindex(self, config: dict, locale_code: str) -> bool:
        """Whether the index Page for this locale should get a noindex robots meta."""
        if config.get('noindex') is True:
            return True
        noindex_locales = config.get('noindex_locales') or []
        return any(str(entry).lower() == locale_code.lower() for entry in noindex_locales)

    def build_alternates_payload(
        self,
        config: dict,
        all_locales: list[str],
        handles_by_gid: dict[str, str],
    ) -> dict:
        """
        Build the custom.index_alternates JSON shared by every sibling index Page:
        the reciprocal hreflang/link-to-self-locales contract described in
        wagtail-root-index-section.plan.md, generic across any PageIndexConsumer.
        """
        pages = config.get('pages') or {}
        x_default_locale = config.get('x_default_locale') or (all_locales[0] if all_locales else None)

        alternates = []
        for locale_code in all_locales:
            handle = handles_by_gid.get(pages.get(locale_code))
            if not handle:
                continue
            alternates.append({
                'hreflang': self.hreflang_for_locale(locale_code),
                'label': locale_code,
                'handle': handle,
            })

        x_default_handle = handles_by_gid.get(pages.get(x_default_locale)) if x_default_locale else None

        return {
            'version': 1,
            'include_self': True,
            'x_default_handle': x_default_handle,
            'alternates': alternates,
        }

    def sync(self, *, locale_codes: list[str] | None = None, dry_run: bool = False) -> dict:
        root = self.get_root_page()
        config = self.get_config(root)
        stats = {
            'consumer': self.config_key,
            'root_found': root is not None,
            'enabled': config is not None,
            'locales': [],
            'pushed': 0,
            'skipped': 0,
            'errors': [],
            'dry_run': dry_run,
        }
        if config is None:
            stats['failure_reason'] = (
                'root_not_found' if root is None else (
                    'section_missing' if not (root.export_config or {}).get(self.config_key)
                    else 'disabled' if not ((root.export_config or {}).get(self.config_key) or {}).get('enabled')
                    else 'pages_empty'
                )
            )
            return stats

        locales = self.configured_locales(config, locale_codes)
        stats['locales'] = locales
        if not locales:
            return stats

        shop = None if dry_run else _get_shop()
        pages = config.get('pages') or {}
        spec = self.index_metafields

        # Alternates must reflect every configured sibling locale, not just the
        # (possibly partial) subset being rebuilt in this call.
        all_locales = self.configured_locales(config, None)
        handles_by_gid = {} if dry_run else _resolve_page_handles(shop, list(pages.values()))

        for locale_code in locales:
            page_gid = pages.get(locale_code)
            if not page_gid:
                stats['skipped'] += 1
                continue

            payload = self.build_payload(locale_code)
            if dry_run:
                stats['pushed'] += 1
                continue

            alternates_payload = self.build_alternates_payload(config, all_locales, handles_by_gid)
            noindex = self.is_noindex(config, locale_code)

            metafields = [
                {
                    'ownerId': page_gid,
                    'namespace': METAFIELD_NAMESPACE,
                    'key': spec.locale_key,
                    'type': 'single_line_text_field',
                    'value': locale_code,
                },
                {
                    'ownerId': page_gid,
                    'namespace': METAFIELD_NAMESPACE,
                    'key': spec.index_key,
                    'type': 'json',
                    'value': json.dumps(payload, ensure_ascii=False),
                },
                {
                    'ownerId': page_gid,
                    'namespace': METAFIELD_NAMESPACE,
                    'key': ALTERNATES_KEY,
                    'type': 'json',
                    'value': json.dumps(alternates_payload, ensure_ascii=False),
                },
                {
                    'ownerId': page_gid,
                    'namespace': METAFIELD_NAMESPACE,
                    'key': NOINDEX_KEY,
                    'type': 'boolean',
                    'value': 'true' if noindex else 'false',
                },
            ]
            ok = _push_metafields(shop, metafields)
            if ok:
                stats['pushed'] += 1
            else:
                stats['errors'].append(locale_code)

        return stats

    def queue_sync(self, *, locale_codes: list[str] | None = None) -> None:
        raise NotImplementedError(f'queue_sync not implemented for {self.config_key}')

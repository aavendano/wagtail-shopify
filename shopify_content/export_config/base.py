"""Base types for export_config index consumers."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

from shopify_content.sync.outbound import _get_shop, _push_metafields

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

METAFIELD_NAMESPACE = 'custom'


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

        for locale_code in locales:
            page_gid = pages.get(locale_code)
            if not page_gid:
                stats['skipped'] += 1
                continue

            payload = self.build_payload(locale_code)
            if dry_run:
                stats['pushed'] += 1
                continue

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
            ]
            ok = _push_metafields(shop, metafields)
            if ok:
                stats['pushed'] += 1
            else:
                stats['errors'].append(locale_code)

        return stats

    def queue_sync(self, *, locale_codes: list[str] | None = None) -> None:
        raise NotImplementedError(f'queue_sync not implemented for {self.config_key}')

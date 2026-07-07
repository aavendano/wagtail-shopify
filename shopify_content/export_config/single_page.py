"""Base consumer for single Shopify Page index listings (custom.index_listings)."""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING

from shopify_content.sync.outbound import _get_shop, _push_metafields

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

METAFIELD_NAMESPACE = 'custom'
LISTINGS_KEY = 'index_listings'


class SinglePageListingsConsumer:
    """Push custom.index_listings to one Shopify Page via export_config.page_gid."""

    root_slug: str
    config_key: str

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
        section = (root.export_config or {}).get(self.config_key) or {}
        if not section.get('enabled'):
            return None
        page_gid = section.get('page_gid')
        if not page_gid:
            return None
        return section

    def build_payload(self) -> dict:
        raise NotImplementedError

    def locale_codes_for_page(self, page) -> list[str] | None:
        return None

    def sync(self, *, dry_run: bool = False) -> dict:
        root = self.get_root_page()
        config = self.get_config(root)
        stats = {
            'consumer': self.config_key,
            'root_found': root is not None,
            'enabled': config is not None,
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
                    else 'page_gid_missing'
                )
            )
            return stats

        page_gid = config['page_gid']
        payload = self.build_payload()

        if dry_run:
            stats['pushed'] = 1
            return stats

        shop = _get_shop()
        ok = _push_metafields(shop, [{
            'ownerId': page_gid,
            'namespace': METAFIELD_NAMESPACE,
            'key': LISTINGS_KEY,
            'type': 'json',
            'value': json.dumps(payload, ensure_ascii=False),
        }])
        if ok:
            stats['pushed'] = 1
        else:
            stats['errors'].append('push_failed')

        return stats

    def queue_sync(self, *, locale_codes: list[str] | None = None) -> None:
        raise NotImplementedError(f'queue_sync not implemented for {self.config_key}')

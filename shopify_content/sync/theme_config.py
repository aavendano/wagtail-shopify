"""Push theme_config metafields from Wagtail pages to Shopify resources."""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def collect_theme_config_metafield_inputs(page, owner_gid: str) -> list[dict]:
    """
    Build metafieldsSet inputs from page.theme_config.metafields.

    Each entry: namespace, key, type, value (all required except namespace defaults to custom).
    """
    theme_config = getattr(page, 'theme_config', None) or {}
    if not isinstance(theme_config, dict):
        return []

    metafields = theme_config.get('metafields') or []
    if not isinstance(metafields, list):
        return []

    inputs = []
    for item in metafields:
        if not isinstance(item, dict):
            continue
        key = item.get('key')
        value = item.get('value')
        if not key or value is None:
            continue
        inputs.append({
            'ownerId': owner_gid,
            'namespace': item.get('namespace') or 'custom',
            'key': str(key),
            'type': item.get('type') or 'single_line_text_field',
            'value': str(value),
        })
    return inputs


def push_theme_config_metafields(shop, page, owner_gid: str) -> bool:
    """Push theme_config metafields to a Shopify resource owner GID."""
    from shopify_content.sync.outbound import _push_metafields

    inputs = collect_theme_config_metafield_inputs(page, owner_gid)
    if not inputs:
        return True
    return _push_metafields(shop, inputs)

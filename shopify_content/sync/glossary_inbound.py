"""Parse Shopify glossary_term metaobject nodes from Admin GraphQL."""

from __future__ import annotations

import json
from typing import Any

from shopify_content.glossary_locale_utils import wagtail_locale_code_for_glossary
from shopify_content.sync.utils import absolute_shopify_media_url


def metaobject_field_map(node: dict[str, Any]) -> dict[str, Any]:
    """Build key → raw value map from metaobject fields array."""
    result: dict[str, Any] = {}
    for field in node.get('fields') or []:
        if not isinstance(field, dict):
            continue
        key = field.get('key')
        if key:
            result[key] = field.get('value')
    return result


def metaobject_image_from_fields(node: dict[str, Any]) -> tuple[str, str, str]:
    """
    Extract (shopify_image_id, image_url, alt_text) from metaobject fields.

    Returns empty strings when no image reference is present.
    """
    for field in node.get('fields') or []:
        if not isinstance(field, dict) or field.get('key') != 'image':
            continue
        reference = field.get('reference') or {}
        if not isinstance(reference, dict):
            continue
        shopify_image_id = reference.get('id') or field.get('value') or ''
        image_payload = reference.get('image') or {}
        url = absolute_shopify_media_url(image_payload.get('url') or '')
        alt_text = (image_payload.get('altText') or '').strip()
        return str(shopify_image_id), url, alt_text
    return '', '', ''


def metaobject_publishable_status(node: dict[str, Any]) -> str:
    capabilities = node.get('capabilities') or {}
    publishable = capabilities.get('publishable') or {}
    return (publishable.get('status') or '').upper()


def glossary_locale_wagtail_code(node: dict[str, Any]) -> str:
    fields = metaobject_field_map(node)
    short_locale = (fields.get('locale') or 'en').strip() or 'en'
    return wagtail_locale_code_for_glossary(short_locale)


def glossary_definition_html(node: dict[str, Any]) -> str:
    """Best-effort conversion of Shopify rich_text_field JSON to HTML for Wagtail."""
    fields = metaobject_field_map(node)
    raw = fields.get('definition')
    if not raw:
        return ''
    if isinstance(raw, str):
        stripped = raw.strip()
        if not stripped:
            return ''
        if stripped.startswith('{'):
            try:
                payload = json.loads(stripped)
            except json.JSONDecodeError:
                return stripped
        else:
            return stripped
    elif isinstance(raw, dict):
        payload = raw
    else:
        return ''

    parts: list[str] = []
    for child in payload.get('children') or []:
        if not isinstance(child, dict):
            continue
        if child.get('type') != 'paragraph':
            continue
        text_bits: list[str] = []
        for text_node in child.get('children') or []:
            if isinstance(text_node, dict) and text_node.get('type') == 'text':
                text_bits.append(text_node.get('value') or '')
        paragraph = ''.join(text_bits).strip()
        if paragraph:
            parts.append(f'<p>{paragraph}</p>')
    return ''.join(parts)

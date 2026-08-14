"""Normalize HomePage sections_json to the canonical 13-section envelope.

AI agents and PATCH payloads may send a partial sections list (or a dict keyed
by section type). This module fills version, order, stable ids, and required
value keys so all four locales share the same structure.
"""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

CANONICAL_SECTION_TYPES: tuple[str, ...] = (
    'promo_gateway',
    'nav_collection_pills',
    'trust_bar',
    'featured_collections',
    'editorial_intro',
    'best_sellers',
    'shop_by_need',
    'educational_hub',
    'brand_values',
    'market_block',
    'faq',
    'internal_links',
    'seo_schema',
)

SECTION_DEFAULTS: dict[str, dict[str, Any]] = {
    'promo_gateway': {'cards': []},
    'nav_collection_pills': {'items': []},
    'trust_bar': {'items': []},
    'featured_collections': {'badge': '', 'title': '', 'intro': '', 'items': []},
    'editorial_intro': {'heading': '', 'body': '', 'alignment': 'left'},
    'best_sellers': {
        'title': '',
        'product_limit': 8,
        'badge': '',
        'background': 'contrast',
    },
    'shop_by_need': {'title': '', 'cards': []},
    'educational_hub': {'title': '', 'intro': '', 'links': []},
    'brand_values': {
        'eyebrow': '',
        'heading': '',
        'body': '',
        'image_url': '',
        'media_position': 'left',
        'values': [],
        'cta_label': '',
        'cta_url': '',
    },
    'market_block': {
        'heading': '',
        'body': '',
        'highlights': [],
        'cta_label': '',
        'cta_url': '',
        'market_code': '',
    },
    'faq': {'heading': 'Frequently asked questions', 'items': []},
    'internal_links': {'heading': '', 'groups': []},
    'seo_schema': {'include_faq_schema': True, 'include_organization': True},
}

_ID_RE = re.compile(r'^[a-z0-9-]+$')

_TRUST_ITEM_DEFAULTS = {'icon': '', 'title': '', 'description': ''}
_BRAND_VALUE_DEFAULTS = {'icon': '', 'title': '', 'description': ''}
_FAQ_ITEM_DEFAULTS = {'question': '', 'answer': ''}
_SHOP_CARD_DEFAULTS = {
    'title': '',
    'description': '',
    'cta_label': 'Shop',
    'intent_tag': '',
}
_PROMO_CARD_DEFAULTS = {
    'title': '',
    'badge': '',
    'media_source': 'collection_products',
    'cta_label': 'Shop trending',
    'cta_url': '',
    'column_span': '1',
}


def default_section_id(section_type: str) -> str:
    return section_type.replace('_', '-')


def normalize_sections_json(
    incoming: dict | None,
    *,
    existing: dict | None = None,
) -> dict[str, Any]:
    """Return `{version: 1, sections: [...]}` with all canonical types present.

    `incoming` overlays `existing`. Missing types are filled from
    `SECTION_DEFAULTS`. Unknown types are dropped.
    """
    incoming_by_type = _index_sections(coerce_incoming_sections(incoming))
    existing_by_type = _index_sections(existing or {})

    sections: list[dict[str, Any]] = []
    for section_type in CANONICAL_SECTION_TYPES:
        value = deepcopy(SECTION_DEFAULTS[section_type])
        existing_section = existing_by_type.get(section_type) or {}
        incoming_section = incoming_by_type.get(section_type) or {}
        if existing_section.get('value'):
            value = _deep_merge(value, existing_section['value'])
        if incoming_section.get('value'):
            value = _deep_merge(value, incoming_section['value'])
        value = _normalize_section_value(section_type, value)
        section_id = _resolve_section_id(
            section_type,
            incoming_section.get('id'),
            existing_section.get('id'),
        )
        sections.append({
            'type': section_type,
            'id': section_id,
            'value': value,
        })
    return {'version': 1, 'sections': sections}


def coerce_incoming_sections(incoming: dict | None) -> dict[str, Any]:
    """Accept either `{sections: [...]}` or a dict keyed by section type."""
    if not incoming:
        return {}
    if isinstance(incoming.get('sections'), list):
        return incoming

    sections = []
    for section_type in CANONICAL_SECTION_TYPES:
        raw = incoming.get(section_type)
        if raw is None:
            continue
        if isinstance(raw, dict) and raw.get('type') == section_type and 'value' in raw:
            sections.append(raw)
        elif isinstance(raw, dict):
            sections.append({'type': section_type, 'value': raw})
    if not sections:
        return incoming if isinstance(incoming, dict) else {}
    return {'version': 1, 'sections': sections}


def dump_section_payload(value: Any) -> dict[str, Any] | None:
    """Convert a Ninja/Pydantic schema (or dict) to a plain dict of set fields."""
    if value is None:
        return None
    if isinstance(value, dict):
        return value
    if hasattr(value, 'model_dump'):
        return value.model_dump(exclude_unset=True)
    if hasattr(value, 'dict'):
        return value.dict(exclude_unset=True)
    return None


def incoming_sections_from_api(
    data,
    *,
    existing: dict | None = None,
    is_create: bool = False,
) -> dict[str, Any] | None:
    """Build a normalized envelope from HomeIn/HomePatch fields.

    Returns None on PATCH when the caller omitted both `sections_json` and
    every typed section field (leave stored JSON unchanged until model.clean).
    """
    envelope = dump_section_payload(getattr(data, 'sections_json', None))
    keyed_sections: list[dict[str, Any]] = []
    for section_type in CANONICAL_SECTION_TYPES:
        payload = dump_section_payload(getattr(data, section_type, None))
        if payload is None:
            continue
        keyed_sections.append({'type': section_type, 'value': payload})

    if envelope is None and not keyed_sections:
        if is_create:
            return normalize_sections_json({}, existing=None)
        return None

    merged = dict(envelope or {})
    if keyed_sections:
        by_type = _index_sections(merged)
        for section in keyed_sections:
            by_type[section['type']] = section
        merged['sections'] = [
            by_type[section_type]
            for section_type in CANONICAL_SECTION_TYPES
            if section_type in by_type
        ] + [
            section
            for section_type, section in by_type.items()
            if section_type not in CANONICAL_SECTION_TYPES
        ]
    return normalize_sections_json(merged, existing=existing)


def _index_sections(payload: dict | None) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for section in (payload or {}).get('sections') or []:
        if not isinstance(section, dict):
            continue
        section_type = section.get('type')
        if not section_type:
            continue
        indexed[section_type] = section
    return indexed


def _deep_merge(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    result = dict(base)
    for key, value in overlay.items():
        if value is None:
            continue
        current = result.get(key)
        if isinstance(value, dict) and isinstance(current, dict):
            result[key] = _deep_merge(current, value)
        else:
            result[key] = value
    return result


def _resolve_section_id(section_type: str, *candidates: Any) -> str:
    for candidate in candidates:
        if isinstance(candidate, str) and _ID_RE.match(candidate):
            return candidate
    return default_section_id(section_type)


def _merge_item(defaults: dict[str, Any], item: Any) -> dict[str, Any]:
    if not isinstance(item, dict):
        return deepcopy(defaults)
    return _deep_merge(deepcopy(defaults), item)


def _page_id(item: dict[str, Any], *keys: str) -> int | None:
    for key in keys:
        raw = item.get(key)
        if raw is None or raw == '':
            continue
        try:
            page_id = int(raw)
        except (TypeError, ValueError):
            continue
        if page_id > 0:
            return page_id
    return None


def _normalize_page_ref(item: dict[str, Any], *, required: bool = True) -> dict[str, Any] | None:
    page_id = _page_id(item, 'page_id')
    if page_id is None:
        return None if required else item
    normalized = dict(item)
    normalized['page_id'] = page_id
    return normalized


def _normalize_section_value(section_type: str, value: dict[str, Any]) -> dict[str, Any]:
    if section_type == 'trust_bar':
        value['items'] = [
            _merge_item(_TRUST_ITEM_DEFAULTS, item)
            for item in value.get('items') or []
            if isinstance(item, dict)
        ]
        return value

    if section_type == 'featured_collections':
        items = []
        for item in value.get('items') or []:
            if not isinstance(item, dict):
                continue
            ref = _normalize_page_ref(item)
            if ref:
                items.append(ref)
        value['items'] = items
        return value

    if section_type == 'nav_collection_pills':
        items = []
        for item in value.get('items') or []:
            if not isinstance(item, dict):
                continue
            ref = _normalize_page_ref(item)
            if ref:
                items.append(ref)
        value['items'] = items
        source_id = _page_id(value, 'source_collection_page_id')
        if source_id:
            value['source_collection_page_id'] = source_id
        elif 'source_collection_page_id' in value:
            value.pop('source_collection_page_id', None)
        return value

    if section_type == 'best_sellers':
        collection_id = _page_id(value, 'collection_page_id')
        if collection_id:
            value['collection_page_id'] = collection_id
        elif 'collection_page_id' in value:
            value.pop('collection_page_id', None)
        try:
            limit = int(value.get('product_limit') or 8)
        except (TypeError, ValueError):
            limit = 8
        value['product_limit'] = min(12, max(4, limit))
        background = value.get('background') or 'contrast'
        value['background'] = background if background in ('default', 'contrast') else 'contrast'
        return value

    if section_type == 'shop_by_need':
        cards = []
        for card in value.get('cards') or []:
            if not isinstance(card, dict):
                continue
            normalized = _merge_item(_SHOP_CARD_DEFAULTS, card)
            target_id = _page_id(normalized, 'target_page_id')
            if target_id:
                normalized['target_page_id'] = target_id
            else:
                normalized.pop('target_page_id', None)
            cards.append(normalized)
        value['cards'] = cards
        return value

    if section_type == 'educational_hub':
        links = []
        for link in value.get('links') or []:
            if not isinstance(link, dict):
                continue
            ref = _normalize_page_ref(link)
            if ref:
                links.append(ref)
        value['links'] = links
        return value

    if section_type == 'brand_values':
        value['values'] = [
            _merge_item(_BRAND_VALUE_DEFAULTS, item)
            for item in value.get('values') or []
            if isinstance(item, dict)
        ]
        position = value.get('media_position') or 'left'
        value['media_position'] = position if position in ('left', 'right') else 'left'
        return value

    if section_type == 'market_block':
        highlights = []
        for item in value.get('highlights') or []:
            if isinstance(item, str) and item.strip():
                highlights.append(item)
        value['highlights'] = highlights
        market_code = value.get('market_code') or ''
        value['market_code'] = market_code if market_code in ('US', 'CA', '') else ''
        return value

    if section_type == 'faq':
        value['items'] = [
            _merge_item(_FAQ_ITEM_DEFAULTS, item)
            for item in value.get('items') or []
            if isinstance(item, dict)
        ]
        if not value.get('heading'):
            value['heading'] = SECTION_DEFAULTS['faq']['heading']
        return value

    if section_type == 'internal_links':
        groups = []
        for group in value.get('groups') or []:
            if not isinstance(group, dict):
                continue
            links = []
            for link in group.get('links') or []:
                if not isinstance(link, dict):
                    continue
                ref = _normalize_page_ref(link)
                if ref:
                    links.append(ref)
            groups.append({
                'title': group.get('title') or '',
                'links': links,
            })
        value['groups'] = groups
        return value

    if section_type == 'promo_gateway':
        cards = []
        for card in value.get('cards') or []:
            if not isinstance(card, dict):
                continue
            normalized = _merge_item(_PROMO_CARD_DEFAULTS, card)
            media_source = normalized.get('media_source') or 'collection_products'
            if media_source not in ('collection_products', 'collection_list'):
                media_source = 'collection_products'
            normalized['media_source'] = media_source
            column_span = str(normalized.get('column_span') or '1')
            normalized['column_span'] = column_span if column_span in ('1', '2') else '1'
            primary_id = _page_id(normalized, 'primary_collection_page_id')
            if primary_id:
                normalized['primary_collection_page_id'] = primary_id
            else:
                normalized.pop('primary_collection_page_id', None)
            category_ids = []
            for raw in normalized.get('category_page_ids') or []:
                try:
                    category_id = int(raw)
                except (TypeError, ValueError):
                    continue
                if category_id > 0:
                    category_ids.append(category_id)
            if category_ids:
                normalized['category_page_ids'] = category_ids[:4]
            else:
                normalized.pop('category_page_ids', None)
            cards.append(normalized)
        value['cards'] = cards
        return value

    if section_type == 'seo_schema':
        value['include_faq_schema'] = bool(value.get('include_faq_schema', True))
        value['include_organization'] = bool(value.get('include_organization', True))
        return value

    alignment = value.get('alignment') or 'left'
    if section_type == 'editorial_intro':
        value['alignment'] = alignment if alignment in ('left', 'center') else 'left'
    return value

"""Serialize HomePage StreamField blocks to sections_json."""

from __future__ import annotations

import uuid
from typing import Any

from wagtail.blocks import StructValue


def _page_id_from_chooser(value) -> int | None:
    if value is None:
        return None
    if hasattr(value, 'pk'):
        return value.pk
    return None


def _block_id(prefix: str) -> str:
    return f'{prefix}-{uuid.uuid4().hex[:8]}'


def _serialize_trust_bar(block: StructValue) -> dict[str, Any]:
    items = []
    for item in block.get('items') or []:
        items.append({
            'icon': item.get('icon') or '',
            'title': item.get('title') or '',
            'description': item.get('description') or '',
        })
    return {'items': items}


def _serialize_featured_collections(block: StructValue) -> dict[str, Any]:
    items = []
    for item in block.get('items') or []:
        page_id = _page_id_from_chooser(item.get('collection'))
        if not page_id:
            continue
        entry: dict[str, Any] = {'page_id': page_id}
        if item.get('override_title'):
            entry['override_title'] = item['override_title']
        if item.get('override_label'):
            entry['override_label'] = item['override_label']
        items.append(entry)
    return {
        'badge': block.get('badge') or '',
        'title': block.get('title') or '',
        'intro': block.get('intro') or '',
        'items': items,
    }


def _serialize_editorial_intro(block: StructValue) -> dict[str, Any]:
    return {
        'heading': block.get('heading') or '',
        'body': str(block.get('body') or ''),
        'alignment': block.get('alignment') or 'left',
    }


def _serialize_best_sellers(block: StructValue) -> dict[str, Any]:
    page_id = _page_id_from_chooser(block.get('collection'))
    value: dict[str, Any] = {
        'title': block.get('title') or '',
        'product_limit': block.get('product_limit') or 8,
        'badge': block.get('badge') or '',
        'background': block.get('background') or 'contrast',
    }
    if page_id:
        value['collection_page_id'] = page_id
    return value


def _serialize_shop_by_need(block: StructValue) -> dict[str, Any]:
    cards = []
    for card in block.get('cards') or []:
        entry: dict[str, Any] = {
            'title': card.get('title') or '',
            'description': card.get('description') or '',
            'cta_label': card.get('cta_label') or 'Shop',
            'intent_tag': card.get('intent_tag') or '',
        }
        target_id = _page_id_from_chooser(card.get('target_page'))
        if target_id:
            entry['target_page_id'] = target_id
        elif card.get('cta_url'):
            entry['cta_url'] = card['cta_url']
        if card.get('image_url'):
            entry['image_url'] = card['image_url']
        cards.append(entry)
    return {'title': block.get('title') or '', 'cards': cards}


def _serialize_educational_hub(block: StructValue) -> dict[str, Any]:
    links = []
    for link in block.get('links') or []:
        page_id = _page_id_from_chooser(link.get('page'))
        if not page_id:
            continue
        entry: dict[str, Any] = {'page_id': page_id}
        if link.get('label'):
            entry['label'] = link['label']
        if link.get('description'):
            entry['description'] = link['description']
        links.append(entry)
    return {
        'title': block.get('title') or '',
        'intro': block.get('intro') or '',
        'links': links,
    }


def _serialize_brand_values(block: StructValue) -> dict[str, Any]:
    values = []
    for item in block.get('values') or []:
        values.append({
            'icon': item.get('icon') or '',
            'title': item.get('title') or '',
            'description': item.get('description') or '',
        })
    return {
        'eyebrow': block.get('eyebrow') or '',
        'heading': block.get('heading') or '',
        'body': str(block.get('body') or ''),
        'image_url': block.get('image_url') or '',
        'media_position': block.get('media_position') or 'left',
        'values': values,
        'cta_label': block.get('cta_label') or '',
        'cta_url': block.get('cta_url') or '',
    }


def _serialize_market_block(block: StructValue) -> dict[str, Any]:
    return {
        'heading': block.get('heading') or '',
        'body': str(block.get('body') or ''),
        'highlights': list(block.get('highlights') or []),
        'cta_label': block.get('cta_label') or '',
        'cta_url': block.get('cta_url') or '',
        'market_code': block.get('market_code') or '',
    }


def _serialize_faq(block: StructValue) -> dict[str, Any]:
    items = []
    for item in block.get('items') or []:
        items.append({
            'question': item.get('question') or '',
            'answer': str(item.get('answer') or ''),
        })
    return {'heading': block.get('heading') or '', 'items': items}


def _serialize_internal_links(block: StructValue) -> dict[str, Any]:
    groups = []
    for group in block.get('groups') or []:
        links = []
        for link in group.get('links') or []:
            page_id = _page_id_from_chooser(link.get('page'))
            if not page_id:
                continue
            entry: dict[str, Any] = {'page_id': page_id}
            if link.get('label'):
                entry['label'] = link['label']
            links.append(entry)
        groups.append({
            'title': group.get('title') or '',
            'links': links,
        })
    return {'heading': block.get('heading') or '', 'groups': groups}


def _serialize_promo_gateway(block: StructValue) -> dict[str, Any]:
    cards = []
    for card in block.get('cards') or []:
        entry: dict[str, Any] = {
            'title': card.get('title') or '',
            'badge': card.get('badge') or '',
            'media_source': card.get('media_source') or 'collection_products',
            'cta_label': card.get('cta_label') or 'Shop trending',
            'cta_url': card.get('cta_url') or '',
            'column_span': card.get('column_span') or '1',
        }
        primary_id = _page_id_from_chooser(card.get('primary_collection'))
        if primary_id:
            entry['primary_collection_page_id'] = primary_id
        category_ids = []
        for category in card.get('category_collections') or []:
            category_id = _page_id_from_chooser(category)
            if category_id:
                category_ids.append(category_id)
        if category_ids:
            entry['category_page_ids'] = category_ids
        cards.append(entry)
    return {'cards': cards}


def _serialize_seo_schema(block: StructValue) -> dict[str, Any]:
    return {
        'include_faq_schema': bool(block.get('include_faq_schema', True)),
        'include_organization': bool(block.get('include_organization', True)),
    }


_SERIALIZERS = {
    'trust_bar': _serialize_trust_bar,
    'featured_collections': _serialize_featured_collections,
    'editorial_intro': _serialize_editorial_intro,
    'best_sellers': _serialize_best_sellers,
    'shop_by_need': _serialize_shop_by_need,
    'educational_hub': _serialize_educational_hub,
    'brand_values': _serialize_brand_values,
    'market_block': _serialize_market_block,
    'faq': _serialize_faq,
    'internal_links': _serialize_internal_links,
    'promo_gateway': _serialize_promo_gateway,
    'seo_schema': _serialize_seo_schema,
}


def streamfield_to_sections_json(stream_value) -> dict[str, Any]:
    """Convert HomePage body StreamField to canonical sections_json."""
    sections = []
    for child in stream_value or []:
        block_type = child.block_type
        serializer = _SERIALIZERS.get(block_type)
        if serializer is None:
            continue
        sections.append({
            'type': block_type,
            'id': _block_id(block_type),
            'value': serializer(child.value),
        })
    return {'version': 1, 'sections': sections}

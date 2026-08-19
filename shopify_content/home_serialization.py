"""Serialize HomePage StreamField blocks to sections_json and hydrate the reverse."""

from __future__ import annotations

from typing import Any

from wagtail.blocks import StructValue
from wagtail.models import Page

from .home_sections_normalization import (
    CANONICAL_SECTION_TYPES,
    default_section_id,
    normalize_sections_json,
)


def _page_id_from_chooser(value) -> int | None:
    if value is None:
        return None
    if hasattr(value, 'pk'):
        return value.pk
    return None


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


def _serialize_nav_collection_pills(block: StructValue) -> dict[str, Any]:
    items = []
    for item in block.get('items') or []:
        page_id = _page_id_from_chooser(item.get('collection'))
        if not page_id:
            continue
        entry: dict[str, Any] = {'page_id': page_id}
        if item.get('override_label'):
            entry['override_label'] = item['override_label']
        items.append(entry)
    value: dict[str, Any] = {'items': items}
    source_id = _page_id_from_chooser(block.get('source_collection'))
    if source_id:
        value['source_collection_page_id'] = source_id
    return value


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
    'nav_collection_pills': _serialize_nav_collection_pills,
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
        section_id = getattr(child, 'id', None) or default_section_id(block_type)
        sections.append({
            'type': block_type,
            'id': section_id,
            'value': serializer(child.value),
        })
    return normalize_sections_json({'version': 1, 'sections': sections})


def _existing_page_id(page_id: Any) -> int | None:
    if page_id is None or page_id == '':
        return None
    try:
        pk = int(page_id)
    except (TypeError, ValueError):
        return None
    if pk <= 0:
        return None
    if not Page.objects.filter(pk=pk).exists():
        return None
    return pk


def _hydrate_trust_bar(value: dict[str, Any]) -> dict[str, Any]:
    return {
        'items': [
            {
                'icon': item.get('icon') or '',
                'title': item.get('title') or '',
                'description': item.get('description') or '',
            }
            for item in value.get('items') or []
            if isinstance(item, dict)
        ],
    }


def _hydrate_featured_collections(value: dict[str, Any]) -> dict[str, Any]:
    items = []
    for item in value.get('items') or []:
        if not isinstance(item, dict):
            continue
        page_id = _existing_page_id(item.get('page_id'))
        if not page_id:
            continue
        entry: dict[str, Any] = {'collection': page_id}
        if item.get('override_title'):
            entry['override_title'] = item['override_title']
        if item.get('override_label'):
            entry['override_label'] = item['override_label']
        items.append(entry)
    return {
        'badge': value.get('badge') or '',
        'title': value.get('title') or '',
        'intro': value.get('intro') or '',
        'items': items,
    }


def _hydrate_nav_collection_pills(value: dict[str, Any]) -> dict[str, Any]:
    items = []
    for item in value.get('items') or []:
        if not isinstance(item, dict):
            continue
        page_id = _existing_page_id(item.get('page_id'))
        if not page_id:
            continue
        entry: dict[str, Any] = {'collection': page_id}
        if item.get('override_label'):
            entry['override_label'] = item['override_label']
        items.append(entry)
    result: dict[str, Any] = {'items': items}
    source_id = _existing_page_id(value.get('source_collection_page_id'))
    if source_id:
        result['source_collection'] = source_id
    return result


def _hydrate_editorial_intro(value: dict[str, Any]) -> dict[str, Any]:
    return {
        'heading': value.get('heading') or '',
        'body': value.get('body') or '',
        'alignment': value.get('alignment') or 'left',
    }


def _hydrate_best_sellers(value: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        'title': value.get('title') or '',
        'product_limit': value.get('product_limit') or 8,
        'badge': value.get('badge') or '',
        'background': value.get('background') or 'contrast',
    }
    collection_id = _existing_page_id(value.get('collection_page_id'))
    if collection_id:
        result['collection'] = collection_id
    return result


def _hydrate_shop_by_need(value: dict[str, Any]) -> dict[str, Any]:
    cards = []
    for card in value.get('cards') or []:
        if not isinstance(card, dict):
            continue
        entry: dict[str, Any] = {
            'title': card.get('title') or '',
            'description': card.get('description') or '',
            'cta_label': card.get('cta_label') or 'Shop',
            'intent_tag': card.get('intent_tag') or '',
        }
        target_id = _existing_page_id(card.get('target_page_id'))
        if target_id:
            entry['target_page'] = target_id
        if card.get('cta_url'):
            entry['cta_url'] = card['cta_url']
        if card.get('image_url'):
            entry['image_url'] = card['image_url']
        cards.append(entry)
    return {'title': value.get('title') or '', 'cards': cards}


def _hydrate_educational_hub(value: dict[str, Any]) -> dict[str, Any]:
    links = []
    for link in value.get('links') or []:
        if not isinstance(link, dict):
            continue
        page_id = _existing_page_id(link.get('page_id'))
        if not page_id:
            continue
        entry: dict[str, Any] = {'page': page_id}
        if link.get('label'):
            entry['label'] = link['label']
        if link.get('description'):
            entry['description'] = link['description']
        links.append(entry)
    return {
        'title': value.get('title') or '',
        'intro': value.get('intro') or '',
        'links': links,
    }


def _hydrate_brand_values(value: dict[str, Any]) -> dict[str, Any]:
    return {
        'eyebrow': value.get('eyebrow') or '',
        'heading': value.get('heading') or '',
        'body': value.get('body') or '',
        'image_url': value.get('image_url') or '',
        'media_position': value.get('media_position') or 'left',
        'values': [
            {
                'icon': item.get('icon') or '',
                'title': item.get('title') or '',
                'description': item.get('description') or '',
            }
            for item in value.get('values') or []
            if isinstance(item, dict)
        ],
        'cta_label': value.get('cta_label') or '',
        'cta_url': value.get('cta_url') or '',
    }


def _hydrate_market_block(value: dict[str, Any]) -> dict[str, Any]:
    return {
        'heading': value.get('heading') or '',
        'body': value.get('body') or '',
        'highlights': [
            item for item in (value.get('highlights') or [])
            if isinstance(item, str) and item.strip()
        ],
        'cta_label': value.get('cta_label') or '',
        'cta_url': value.get('cta_url') or '',
        'market_code': value.get('market_code') or '',
    }


def _hydrate_faq(value: dict[str, Any]) -> dict[str, Any]:
    return {
        'heading': value.get('heading') or 'Frequently asked questions',
        'items': [
            {
                'question': item.get('question') or '',
                'answer': item.get('answer') or '',
            }
            for item in value.get('items') or []
            if isinstance(item, dict)
        ],
    }


def _hydrate_internal_links(value: dict[str, Any]) -> dict[str, Any]:
    groups = []
    for group in value.get('groups') or []:
        if not isinstance(group, dict):
            continue
        links = []
        for link in group.get('links') or []:
            if not isinstance(link, dict):
                continue
            page_id = _existing_page_id(link.get('page_id'))
            if not page_id:
                continue
            entry: dict[str, Any] = {'page': page_id}
            if link.get('label'):
                entry['label'] = link['label']
            links.append(entry)
        groups.append({
            'title': group.get('title') or '',
            'links': links,
        })
    return {'heading': value.get('heading') or '', 'groups': groups}


def _hydrate_promo_gateway(value: dict[str, Any]) -> dict[str, Any]:
    cards = []
    for card in value.get('cards') or []:
        if not isinstance(card, dict):
            continue
        entry: dict[str, Any] = {
            'title': card.get('title') or '',
            'badge': card.get('badge') or '',
            'media_source': card.get('media_source') or 'collection_products',
            'cta_label': card.get('cta_label') or 'Shop trending',
            'cta_url': card.get('cta_url') or '',
            'column_span': str(card.get('column_span') or '1'),
        }
        primary_id = _existing_page_id(card.get('primary_collection_page_id'))
        if primary_id:
            entry['primary_collection'] = primary_id
        category_ids = []
        for raw in card.get('category_page_ids') or []:
            category_id = _existing_page_id(raw)
            if category_id:
                category_ids.append(category_id)
        if category_ids:
            entry['category_collections'] = category_ids[:4]
        cards.append(entry)
    return {'cards': cards}


def _hydrate_seo_schema(value: dict[str, Any]) -> dict[str, Any]:
    return {
        'include_faq_schema': bool(value.get('include_faq_schema', True)),
        'include_organization': bool(value.get('include_organization', True)),
    }


_HYDRATORS = {
    'trust_bar': _hydrate_trust_bar,
    'featured_collections': _hydrate_featured_collections,
    'nav_collection_pills': _hydrate_nav_collection_pills,
    'editorial_intro': _hydrate_editorial_intro,
    'best_sellers': _hydrate_best_sellers,
    'shop_by_need': _hydrate_shop_by_need,
    'educational_hub': _hydrate_educational_hub,
    'brand_values': _hydrate_brand_values,
    'market_block': _hydrate_market_block,
    'faq': _hydrate_faq,
    'internal_links': _hydrate_internal_links,
    'promo_gateway': _hydrate_promo_gateway,
    'seo_schema': _hydrate_seo_schema,
}


def sections_json_to_stream_data(payload: dict | None) -> list[dict[str, Any]]:
    """Convert normalized sections_json into StreamField raw_data list."""
    normalized = normalize_sections_json(payload)
    by_type = {
        section['type']: section
        for section in normalized.get('sections') or []
        if isinstance(section, dict) and section.get('type')
    }
    stream_data: list[dict[str, Any]] = []
    for section_type in CANONICAL_SECTION_TYPES:
        section = by_type.get(section_type) or {
            'type': section_type,
            'id': default_section_id(section_type),
            'value': {},
        }
        hydrator = _HYDRATORS[section_type]
        stream_data.append({
            'type': section_type,
            'id': section.get('id') or default_section_id(section_type),
            'value': hydrator(section.get('value') or {}),
        })
    return stream_data

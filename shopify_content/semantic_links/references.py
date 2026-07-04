"""Resolve Wagtail semantic link FK rows to Shopify GIDs for native reference metafields."""

import json
import logging
from typing import Any

from wagtail.models import Page

from shopify_content.semantic_links.constants import (
    NATIVE_REFERENCE_CONFIG,
    NATIVE_REFERENCE_RELATION_NAMES,
)

logger = logging.getLogger(__name__)


REFERENCE_TYPE_TO_MODEL = {
    'product_reference': 'shopify_content.ProductPage',
    'collection_reference': 'shopify_content.CollectionPage',
    'article_reference': 'shopify_content.ArticlePage',
    'metaobject_reference': 'shopify_content.GlossaryTermPage',
}


def page_to_shopify_gid(page: Page) -> str | None:
    """Read specific.shopify_id; return None when empty."""
    try:
        specific = page.specific
    except Exception:
        specific = page
    shopify_id = getattr(specific, 'shopify_id', None)
    if not shopify_id or not str(shopify_id).strip():
        return None
    return str(shopify_id).strip()


def relation_to_shopify_gids(source_page, relation_name: str) -> list[str]:
    """Iterate FK rows for a relation and return valid Shopify GIDs."""
    manager = getattr(source_page, relation_name, None)
    if manager is None:
        return []

    gids: list[str] = []
    for row in manager.select_related('related_page').order_by('sort_order'):
        related = row.related_page
        if related is None:
            continue
        try:
            related = related.specific
        except Exception:
            pass
        gid = page_to_shopify_gid(related)
        if gid:
            gids.append(gid)
            continue
        logger.warning(
            'Skipping native reference: target page pk=%s has no shopify_id '
            '(source pk=%s, relation=%s)',
            getattr(related, 'pk', None),
            getattr(source_page, 'pk', None),
            relation_name,
        )
    return gids


def serialize_native_references(source_page) -> dict[str, list[str]]:
    """Return {relation_name: [gid, ...]} for relations with at least one resolved GID."""
    result: dict[str, list[str]] = {}
    for relation_name in NATIVE_REFERENCE_RELATION_NAMES:
        gids = relation_to_shopify_gids(source_page, relation_name)
        if gids:
            result[relation_name] = gids
    return result


def format_list_reference_value(gids: list[str]) -> str:
    """JSON-encode GID list for Shopify list.*_reference metafield types."""
    return json.dumps(gids, ensure_ascii=False)


def is_reference_metafield_type(mf_type: str) -> bool:
    return mf_type.endswith('_reference')


def lookup_gid_by_handle(handle: str, reference_type: str) -> str | None:
    """Resolve a Wagtail page handle/slug to a Shopify GID for inline metafields."""
    from django.apps import apps

    model_label = REFERENCE_TYPE_TO_MODEL.get(reference_type)
    if not model_label:
        return None
    model = apps.get_model(model_label)
    page = (
        model.objects.filter(handle=handle).first()
        or model.objects.filter(slug=handle).first()
    )
    if page is None:
        return None
    return page_to_shopify_gid(page)


def resolve_metafield_reference_value(mf_type: str, value: Any) -> str:
    """
    Resolve handle/slug values to GIDs for *_reference and list.*_reference metafields.
    Values that are already GIDs are passed through unchanged.
    """
    value_str = str(value).strip()
    if not is_reference_metafield_type(mf_type):
        return value_str

    if mf_type.startswith('list.'):
        base_type = mf_type[len('list.'):]
        try:
            items = json.loads(value_str)
        except json.JSONDecodeError:
            items = [part.strip() for part in value_str.split(',') if part.strip()]
        if not isinstance(items, list):
            items = [items]
        resolved: list[str] = []
        for item in items:
            item_str = str(item).strip()
            if item_str.startswith('gid://'):
                resolved.append(item_str)
                continue
            gid = lookup_gid_by_handle(item_str, base_type)
            if gid:
                resolved.append(gid)
            else:
                logger.warning(
                    'Could not resolve %s reference handle=%r; skipping item',
                    mf_type,
                    item_str,
                )
        return format_list_reference_value(resolved)

    if value_str.startswith('gid://'):
        return value_str
    gid = lookup_gid_by_handle(value_str, mf_type)
    return gid if gid else value_str


def native_metaobject_field_values(source_page) -> dict[str, list[str]]:
    """Map native reference relations to metaobject field keys for glossary sync."""
    refs = serialize_native_references(source_page)
    values: dict[str, list[str]] = {}
    for relation_name, gids in refs.items():
        config = NATIVE_REFERENCE_CONFIG[relation_name]
        values[config['metaobject_field_key']] = gids
    return values

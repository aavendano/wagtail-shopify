"""Resolve HomePage sections_json references to Shopify GIDs and related_links."""

from __future__ import annotations

import logging
from typing import Any

from wagtail.models import Page

from shopify_content.models.blog import ArticlePage, BlogPage
from shopify_content.models.collection import CollectionPage
from shopify_content.models.glossary import GlossaryTermPage
from shopify_content.models.product import ProductPage
from shopify_content.semantic_links.references import page_to_shopify_gid
from shopify_content.semantic_links.serialization import page_to_related_link

logger = logging.getLogger(__name__)


def _append_unique_link(links: list[dict[str, Any]], seen: set, link: dict[str, Any] | None) -> None:
    if not link:
        return
    dedupe_key = (
        link.get('type'),
        link.get('handle'),
        link.get('blog_handle') or link.get('url_handle'),
    )
    if dedupe_key in seen:
        return
    seen.add(dedupe_key)
    links.append(link)


def _page_id_to_gid(page_id: Any) -> str | None:
    if not page_id:
        return None
    try:
        page = Page.objects.filter(pk=int(page_id)).first()
    except (TypeError, ValueError):
        return None
    if page is None:
        logger.warning('Home sync: page_id=%s not found', page_id)
        return None
    try:
        specific = page.specific
    except Exception:
        specific = page
    return page_to_shopify_gid(specific)


def _page_id_to_link(page_id: Any, *, label: str | None = None) -> dict[str, Any] | None:
    if not page_id:
        return None
    try:
        page = Page.objects.filter(pk=int(page_id)).first()
    except (TypeError, ValueError):
        return None
    if page is None:
        return None
    try:
        specific = page.specific
    except Exception:
        specific = page
    link = page_to_related_link(specific)
    if link:
        link = dict(link)
        if label:
            link['label'] = label
        if page_id:
            link['wagtail_page_id'] = int(page_id)
    return link


def _is_collection_page(page_id: Any) -> bool:
    try:
        page = Page.objects.filter(pk=int(page_id)).first()
        return isinstance(page.specific if page else None, CollectionPage)
    except (TypeError, ValueError):
        return False


def build_home_sync_references(sections_json: dict | None) -> dict[str, Any]:
    """
    Extract native reference GID lists and related_links from sections_json.

    Returns dict with keys matching home_page metaobject native fields.
    """
    sections = (sections_json or {}).get('sections') or []
    featured_collections_refs: list[str] = []
    shop_by_need_collection_refs: list[str] = []
    education_hub_article_refs: list[str] = []
    education_hub_glossary_refs: list[str] = []
    related_links: list[dict[str, Any]] = []
    seen_links: set[tuple] = set()
    best_sellers_collection_ref: str | None = None

    for section in sections:
        if not isinstance(section, dict):
            continue
        block_type = section.get('type')
        value = section.get('value') or {}
        if not isinstance(value, dict):
            continue

        if block_type == 'featured_collections':
            for item in value.get('items') or []:
                if not isinstance(item, dict):
                    continue
                gid = _page_id_to_gid(item.get('page_id'))
                if gid and _is_collection_page(item.get('page_id')):
                    featured_collections_refs.append(gid)
                label = item.get('override_label') or item.get('label')
                _append_unique_link(
                    related_links,
                    seen_links,
                    _page_id_to_link(item.get('page_id'), label=label),
                )

        elif block_type == 'best_sellers':
            gid = _page_id_to_gid(value.get('collection_page_id'))
            if gid:
                best_sellers_collection_ref = gid
            _append_unique_link(
                related_links,
                seen_links,
                _page_id_to_link(value.get('collection_page_id')),
            )

        elif block_type == 'shop_by_need':
            for card in value.get('cards') or []:
                if not isinstance(card, dict):
                    continue
                target_id = card.get('target_page_id')
                gid = _page_id_to_gid(target_id)
                if gid and _is_collection_page(target_id):
                    shop_by_need_collection_refs.append(gid)
                _append_unique_link(
                    related_links,
                    seen_links,
                    _page_id_to_link(target_id, label=card.get('cta_label')),
                )

        elif block_type == 'educational_hub':
            for link_item in value.get('links') or []:
                if not isinstance(link_item, dict):
                    continue
                page_id = link_item.get('page_id')
                gid = _page_id_to_gid(page_id)
                page = Page.objects.filter(pk=page_id).first() if page_id else None
                specific = page.specific if page else None
                if gid and isinstance(specific, ArticlePage):
                    education_hub_article_refs.append(gid)
                elif gid and isinstance(specific, GlossaryTermPage):
                    education_hub_glossary_refs.append(gid)
                _append_unique_link(
                    related_links,
                    seen_links,
                    _page_id_to_link(page_id, label=link_item.get('label')),
                )

        elif block_type == 'internal_links':
            for group in value.get('groups') or []:
                if not isinstance(group, dict):
                    continue
                for link_item in group.get('links') or []:
                    if not isinstance(link_item, dict):
                        continue
                    _append_unique_link(
                        related_links,
                        seen_links,
                        _page_id_to_link(link_item.get('page_id'), label=link_item.get('label')),
                    )

    result: dict[str, Any] = {}
    if featured_collections_refs:
        result['featured_collections_refs'] = featured_collections_refs
    if best_sellers_collection_ref:
        result['best_sellers_collection_ref'] = best_sellers_collection_ref
    if shop_by_need_collection_refs:
        result['shop_by_need_collection_refs'] = shop_by_need_collection_refs
    if education_hub_article_refs:
        result['education_hub_article_refs'] = education_hub_article_refs
    if education_hub_glossary_refs:
        result['education_hub_glossary_refs'] = education_hub_glossary_refs
    if related_links:
        result['related_links'] = related_links
    return result

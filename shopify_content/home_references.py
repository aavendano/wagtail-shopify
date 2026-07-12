"""Resolve HomePage sections_json references to Shopify GIDs and related_links."""

from __future__ import annotations

import logging
from typing import Any

from wagtail.models import Page

from shopify_content.home_locale_validation import is_page_valid_for_home_locale
from shopify_content.models.blog import ArticlePage
from shopify_content.models.collection import CollectionPage
from shopify_content.models.glossary import GlossaryTermPage
from shopify_content.models.home_page import HomePage
from shopify_content.semantic_links.references import page_to_shopify_gid
from shopify_content.semantic_links.serialization import page_to_related_link

logger = logging.getLogger(__name__)

NAV_COLLECTION_PILLS_MAX = 8

# (shopify handle, default label) — omitted when CollectionPage missing for locale.
DEFAULT_NAV_COLLECTION_PILLS: tuple[tuple[str, str], ...] = (
    ('vibrators', 'Vibrators'),
    ('lubricants', 'Lubricants'),
    ('anal-stimulation', 'Anal Stimulation'),
    ('penis-ring-cock-ring-sex-toys-for-men', 'For Men'),
)


def _page_is_allowed(home_page: HomePage | None, page: Page | None) -> bool:
    if page is None:
        return False
    if home_page is None:
        return True
    return is_page_valid_for_home_locale(home_page, page)


def _get_page(page_id: Any, *, home_page: HomePage | None = None) -> Page | None:
    if not page_id:
        return None
    try:
        page = Page.objects.filter(pk=int(page_id)).select_related('locale').first()
    except (TypeError, ValueError):
        return None
    if page is None:
        logger.warning('Home sync: page_id=%s not found', page_id)
        return None
    if not _page_is_allowed(home_page, page):
        logger.warning(
            'Home sync: omitting page_id=%s (locale mismatch for HomePage pk=%s)',
            page_id,
            getattr(home_page, 'pk', None),
        )
        return None
    return page


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


def _page_id_to_gid(page_id: Any, *, home_page: HomePage | None = None) -> str | None:
    page = _get_page(page_id, home_page=home_page)
    if page is None:
        return None
    try:
        specific = page.specific
    except Exception:
        specific = page
    return page_to_shopify_gid(specific)


def _page_id_to_link(
    page_id: Any,
    *,
    label: str | None = None,
    home_page: HomePage | None = None,
) -> dict[str, Any] | None:
    page = _get_page(page_id, home_page=home_page)
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


def _is_collection_page(page_id: Any, *, home_page: HomePage | None = None) -> bool:
    page = _get_page(page_id, home_page=home_page)
    if page is None:
        return False
    try:
        return isinstance(page.specific, CollectionPage)
    except Exception:
        return False


def _collection_page_by_handle(
    handle: str,
    *,
    home_page: HomePage | None = None,
) -> CollectionPage | None:
    if not handle:
        return None
    page = CollectionPage.objects.filter(handle=handle).first()
    if page is None:
        return None
    if not _page_is_allowed(home_page, page):
        return None
    return page


def resolve_nav_collection_pill_entries(
    value: dict[str, Any] | None,
    *,
    home_page: HomePage | None = None,
) -> list[dict[str, Any]]:
    """
    Resolve nav pills: manual items → source related_collections → default handles.

    Each entry: {'page_id': int, 'override_label': str | None}
    """
    value = value or {}
    entries: list[dict[str, Any]] = []

    for item in value.get('items') or []:
        if not isinstance(item, dict):
            continue
        page_id = item.get('page_id')
        if not page_id or not _is_collection_page(page_id, home_page=home_page):
            continue
        entry: dict[str, Any] = {'page_id': int(page_id)}
        label = item.get('override_label') or item.get('label')
        if label:
            entry['override_label'] = label
        entries.append(entry)
        if len(entries) >= NAV_COLLECTION_PILLS_MAX:
            return entries

    if entries:
        return entries

    source_id = value.get('source_collection_page_id')
    source_page = _get_page(source_id, home_page=home_page)
    if source_page is not None:
        try:
            specific = source_page.specific
        except Exception:
            specific = source_page
        if isinstance(specific, CollectionPage):
            from shopify_content.models.semantic_links import get_typed_link_model

            link_model = get_typed_link_model(specific, 'related_collections')
            if link_model is not None:
                rows = (
                    link_model.objects.filter(page_id=specific.pk)
                    .select_related('related_page')
                    .order_by('sort_order')
                )
                for row in rows:
                    related = row.related_page
                    if related is None:
                        continue
                    try:
                        related_specific = related.specific
                    except Exception:
                        related_specific = related
                    if not isinstance(related_specific, CollectionPage):
                        continue
                    if not _page_is_allowed(home_page, related):
                        continue
                    entries.append({'page_id': related.pk})
                    if len(entries) >= NAV_COLLECTION_PILLS_MAX:
                        return entries

    if entries:
        return entries

    for handle, label in DEFAULT_NAV_COLLECTION_PILLS:
        collection = _collection_page_by_handle(handle, home_page=home_page)
        if collection is None:
            continue
        entries.append({'page_id': collection.pk, 'override_label': label})
        if len(entries) >= NAV_COLLECTION_PILLS_MAX:
            break

    return entries


def build_home_sync_references(
    sections_json: dict | None,
    *,
    home_page: HomePage | None = None,
) -> dict[str, Any]:
    """
    Extract native reference GID lists and related_links from sections_json.

    Returns dict with keys matching home_page metaobject native fields.
    """
    sections = (sections_json or {}).get('sections') or []
    featured_collections_refs: list[str] = []
    nav_collection_pills_refs: list[str] = []
    shop_by_need_collection_refs: list[str] = []
    education_hub_article_refs: list[str] = []
    education_hub_glossary_refs: list[str] = []
    promo_gateway_collection_refs: list[str] = []
    related_links: list[dict[str, Any]] = []
    seen_links: set[tuple] = set()
    best_sellers_collection_ref: str | None = None
    nav_pills_value: dict[str, Any] | None = None

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
                page_id = item.get('page_id')
                gid = _page_id_to_gid(page_id, home_page=home_page)
                if gid and _is_collection_page(page_id, home_page=home_page):
                    featured_collections_refs.append(gid)
                label = item.get('override_label') or item.get('label')
                _append_unique_link(
                    related_links,
                    seen_links,
                    _page_id_to_link(page_id, label=label, home_page=home_page),
                )

        elif block_type == 'nav_collection_pills':
            nav_pills_value = value

        elif block_type == 'best_sellers':
            page_id = value.get('collection_page_id')
            gid = _page_id_to_gid(page_id, home_page=home_page)
            if gid:
                best_sellers_collection_ref = gid
            _append_unique_link(
                related_links,
                seen_links,
                _page_id_to_link(page_id, home_page=home_page),
            )

        elif block_type == 'shop_by_need':
            for card in value.get('cards') or []:
                if not isinstance(card, dict):
                    continue
                target_id = card.get('target_page_id')
                gid = _page_id_to_gid(target_id, home_page=home_page)
                if gid and _is_collection_page(target_id, home_page=home_page):
                    shop_by_need_collection_refs.append(gid)
                _append_unique_link(
                    related_links,
                    seen_links,
                    _page_id_to_link(target_id, label=card.get('cta_label'), home_page=home_page),
                )

        elif block_type == 'educational_hub':
            for link_item in value.get('links') or []:
                if not isinstance(link_item, dict):
                    continue
                page_id = link_item.get('page_id')
                gid = _page_id_to_gid(page_id, home_page=home_page)
                page = _get_page(page_id, home_page=home_page)
                specific = page.specific if page else None
                if gid and isinstance(specific, ArticlePage):
                    education_hub_article_refs.append(gid)
                elif gid and isinstance(specific, GlossaryTermPage):
                    education_hub_glossary_refs.append(gid)
                _append_unique_link(
                    related_links,
                    seen_links,
                    _page_id_to_link(page_id, label=link_item.get('label'), home_page=home_page),
                )

        elif block_type == 'internal_links':
            for group in value.get('groups') or []:
                if not isinstance(group, dict):
                    continue
                for link_item in group.get('links') or []:
                    if not isinstance(link_item, dict):
                        continue
                    page_id = link_item.get('page_id')
                    _append_unique_link(
                        related_links,
                        seen_links,
                        _page_id_to_link(page_id, label=link_item.get('label'), home_page=home_page),
                    )

        elif block_type == 'promo_gateway':
            for card in value.get('cards') or []:
                if not isinstance(card, dict):
                    continue
                media_source = card.get('media_source') or 'collection_products'
                if media_source == 'collection_products':
                    primary_id = card.get('primary_collection_page_id')
                    gid = _page_id_to_gid(primary_id, home_page=home_page)
                    if gid and _is_collection_page(primary_id, home_page=home_page):
                        promo_gateway_collection_refs.append(gid)
                    _append_unique_link(
                        related_links,
                        seen_links,
                        _page_id_to_link(primary_id, label=card.get('cta_label'), home_page=home_page),
                    )
                for category_id in card.get('category_page_ids') or []:
                    gid = _page_id_to_gid(category_id, home_page=home_page)
                    if gid and _is_collection_page(category_id, home_page=home_page):
                        promo_gateway_collection_refs.append(gid)
                    _append_unique_link(
                        related_links,
                        seen_links,
                        _page_id_to_link(category_id, home_page=home_page),
                    )

    # Always resolve pills (defaults when block absent or empty).
    for pill in resolve_nav_collection_pill_entries(nav_pills_value, home_page=home_page):
        page_id = pill.get('page_id')
        gid = _page_id_to_gid(page_id, home_page=home_page)
        if gid and _is_collection_page(page_id, home_page=home_page):
            nav_collection_pills_refs.append(gid)
        _append_unique_link(
            related_links,
            seen_links,
            _page_id_to_link(
                page_id,
                label=pill.get('override_label'),
                home_page=home_page,
            ),
        )

    result: dict[str, Any] = {}
    if featured_collections_refs:
        result['featured_collections_refs'] = featured_collections_refs
    if nav_collection_pills_refs:
        result['nav_collection_pills_refs'] = nav_collection_pills_refs
    if best_sellers_collection_ref:
        result['best_sellers_collection_ref'] = best_sellers_collection_ref
    if shop_by_need_collection_refs:
        result['shop_by_need_collection_refs'] = shop_by_need_collection_refs
    if education_hub_article_refs:
        result['education_hub_article_refs'] = education_hub_article_refs
    if education_hub_glossary_refs:
        result['education_hub_glossary_refs'] = education_hub_glossary_refs
    if promo_gateway_collection_refs:
        result['promo_gateway_collection_refs'] = promo_gateway_collection_refs
    if related_links:
        result['related_links'] = related_links
    return result

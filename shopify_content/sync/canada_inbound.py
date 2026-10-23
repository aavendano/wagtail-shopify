"""
Read-only import of the Canadian ``region`` and ``location_page`` metaobjects into Wagtail.

Nothing is written to Shopify. Each region becomes a ``RegionPage`` and each location a
``LocationPage`` under it. The parent link is derived from ``region.location_pages``: in the
live store ``location_page.province_page`` is empty, so the region is the only side that knows
its children. When a region does not list a location, ``province_page`` and then the
``province`` name are tried; what is left is imported loose under the root and reported.

Imported pages keep the handle the store already uses (``keep_shopify_handle``) and have
``sync_enabled`` off: pushing Canadian locations is not wired yet, and a publish must not send
them to the ``local_page`` metaobject.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Any

from django.utils.text import slugify
from wagtail.models import Locale

from shopify_content.models import LocationPage, RegionPage
from shopify_content.region_codes import CANADA_REGION_CODES
from shopify_content.shopify_languages import shopify_country

from .glossary_inbound import metaobject_field_map, metaobject_publishable_status
from .import_parents import ensure_child_of_import_parent
from .inbound import _empty_import_stats, _paginate
from .queries import LIST_CA_LOCATION_PAGES, LIST_REGIONS

logger = logging.getLogger(__name__)

DEFAULT_LOCALE_CODE = 'en-CA'
_CANADA = 'Canada'
_CODE_TO_PROVINCE = {code: name for name, code in CANADA_REGION_CODES.items()}


def plain_text_to_html(text: str | None) -> str:
    """Multi-line plain text as escaped paragraphs; single line breaks become <br>."""
    from django.template.defaultfilters import linebreaks_filter

    return str(linebreaks_filter((text or '').strip(), autoescape=True)) if (text or '').strip() else ''


def _clean(value: Any) -> str:
    return (value or '').strip() if isinstance(value, str) else ''


@dataclass
class RegionData:
    gid: str
    handle: str
    name: str
    code: str
    country: str
    header1: str
    header2: str
    greeting: str
    seo_title: str
    seo_description: str
    location_gids: list[str]


@dataclass
class LocationData:
    gid: str
    handle: str
    city: str
    province: str
    country: str
    header1: str
    header2: str
    greeting: str
    discreet_shipping: str
    quality_focus: str
    body_safe_materials: str
    seo_title: str
    seo_description: str
    seo_keyword: str
    province_page_gid: str
    region_gid: str | None = None


@dataclass
class CanadaPlan:
    regions: list[RegionData] = field(default_factory=list)
    locations: list[LocationData] = field(default_factory=list)
    unparented: list[LocationData] = field(default_factory=list)
    skipped: int = 0
    warnings: list[str] = field(default_factory=list)


def _json_list(raw: Any) -> list[str]:
    import json

    if isinstance(raw, list):
        return [str(item) for item in raw]
    if not isinstance(raw, str) or not raw.strip():
        return []
    try:
        value = json.loads(raw)
    except ValueError:
        return []
    return [str(item) for item in value] if isinstance(value, list) else []


def _reference_keyword(node: dict[str, Any]) -> str:
    """The ``keyword`` of the referenced ``seo_keyword`` entry, or ''."""
    for entry in node.get('fields') or []:
        if entry.get('key') != 'seo_keyword':
            continue
        reference = entry.get('reference') or {}
        for inner in reference.get('fields') or []:
            if inner.get('key') == 'keyword':
                return _clean(inner.get('value'))
    return ''


def parse_region(node: dict[str, Any]) -> RegionData | None:
    fields = metaobject_field_map(node)
    name = _clean(fields.get('province'))
    if not node.get('id') or not name:
        return None
    code = _clean(fields.get('province_code')).upper() or CANADA_REGION_CODES.get(name, '')
    # Several live regions have no country; their province code says which one it is.
    country = _clean(fields.get('country')) or (_CANADA if code in _CODE_TO_PROVINCE else '')
    return RegionData(
        gid=node['id'], handle=_clean(node.get('handle')), name=name, code=code, country=country,
        header1=_clean(fields.get('header1')), header2=_clean(fields.get('header2')),
        greeting=_clean(fields.get('greeting')),
        seo_title=_clean(fields.get('metatitulo')), seo_description=_clean(fields.get('metadescription')),
        location_gids=_json_list(fields.get('location_pages')),
    )


def parse_location(node: dict[str, Any]) -> LocationData | None:
    fields = metaobject_field_map(node)
    city = _clean(fields.get('city'))
    if not node.get('id') or not city:
        return None
    return LocationData(
        gid=node['id'], handle=_clean(node.get('handle')), city=city,
        province=_clean(fields.get('province')), country=_clean(fields.get('country')),
        header1=_clean(fields.get('header1')), header2=_clean(fields.get('header2')),
        greeting=_clean(fields.get('greeting')),
        discreet_shipping=_clean(fields.get('discreet_shipping')),
        quality_focus=_clean(fields.get('quality_focus')),
        body_safe_materials=_clean(fields.get('body_safe_materials')),
        seo_title=_clean(fields.get('meta_titulo')), seo_description=_clean(fields.get('meta_description')),
        seo_keyword=_reference_keyword(node),
        province_page_gid=_clean(fields.get('province_page')),
    )


def build_plan(region_nodes: list[dict[str, Any]], location_nodes: list[dict[str, Any]]) -> CanadaPlan:
    """Pure: parse the nodes (active ones only) and decide each location's region."""
    plan = CanadaPlan()
    for node in region_nodes:
        if metaobject_publishable_status(node) != 'ACTIVE':
            plan.skipped += 1
            continue
        region = parse_region(node)
        if region is None:
            plan.skipped += 1
            continue
        plan.regions.append(region)

    regions_by_gid = {region.gid: region for region in plan.regions}
    region_of: dict[str, str] = {}
    for region in plan.regions:
        for gid in region.location_gids:
            if gid in region_of and region_of[gid] != region.gid:
                plan.warnings.append(
                    f'{gid} is listed by {regions_by_gid[region_of[gid]].handle} and {region.handle}; '
                    f'keeping {regions_by_gid[region_of[gid]].handle}.'
                )
                continue
            region_of[gid] = region.gid
    regions_by_name = {region.name.lower(): region.gid for region in plan.regions}

    for node in location_nodes:
        if metaobject_publishable_status(node) != 'ACTIVE':
            plan.skipped += 1
            continue
        location = parse_location(node)
        if location is None:
            plan.skipped += 1
            continue
        location.region_gid = (
            region_of.get(location.gid)
            or (location.province_page_gid if location.province_page_gid in regions_by_gid else None)
            or regions_by_name.get(location.province.lower())
        )
        if location.region_gid is None:
            plan.unparented.append(location)
            plan.warnings.append(
                f'{location.handle}: no region lists it and province "{location.province}" matches none.'
            )
        plan.locations.append(location)
    return plan


def fetch_plan(shop) -> CanadaPlan:
    region_nodes = list(_paginate(shop, LIST_REGIONS, 'metaobjects'))
    location_nodes = list(_paginate(shop, LIST_CA_LOCATION_PAGES, 'metaobjects'))
    return build_plan(region_nodes, location_nodes)


def _wagtail_locale(locale_code: str) -> Locale:
    locale = Locale.objects.filter(language_code=locale_code).first()
    if locale is None:
        raise ValueError(f'Wagtail locale "{locale_code}" does not exist; run setup_locales first.')
    return locale


def _moved_under(page, parent):
    """Move the page under parent if needed, then reload it: a move leaves treebeard's path stale."""
    if ensure_child_of_import_parent(page, parent):
        return type(page).objects.get(pk=page.pk)
    return page


def _upsert_region(root, locale, data: RegionData, *, new_only: bool):
    page = RegionPage.objects.filter(shopify_id=data.gid, locale=locale).first()
    slug = f'{slugify(locale.language_code)}-{slugify(data.name)}'
    if page is None:
        page = RegionPage.objects.child_of(root).filter(slug=slug, locale=locale).first()
    is_new = page is None
    if not is_new and new_only:
        return page, 'skipped'
    if is_new:
        page = RegionPage(slug=slug, locale=locale)
    else:
        page = _moved_under(page, root)
    page.title = data.name
    page.shopify_id = data.gid
    page.handle = data.handle or slug
    page.country = data.country
    page.region_code = data.code
    page.header1, page.header2, page.greeting = data.header1, data.header2, data.greeting
    page.seo_title, page.search_description = data.seo_title, data.seo_description
    page.sync_enabled = False
    if is_new:
        root.add_child(instance=page)
    page.save_revision().publish()
    return page, 'created' if is_new else 'updated'


def _upsert_location(parent, locale, data: LocationData, *, region_country: str, new_only: bool):
    page = LocationPage.objects.filter(shopify_id=data.gid, locale=locale).first()
    is_new = page is None
    if not is_new and new_only:
        return page, 'skipped'
    if is_new:
        page = LocationPage(locale=locale)
    else:
        page = _moved_under(page, parent)
    page.shopify_id = data.gid
    page.handle = data.handle
    page.keep_shopify_handle = True
    page.sync_enabled = False
    page.city = data.city
    page.state = data.province
    page.country = region_country or data.country
    page.title = data.header1 or data.city
    page.titulo = data.header1 or data.city
    page.subtitulo = data.header2
    page.intro = plain_text_to_html(data.greeting)
    page.discreet_shipping = data.discreet_shipping
    page.quality_focus = data.quality_focus
    page.body_safe_materials = data.body_safe_materials
    page.seo_keyword = data.seo_keyword
    page.seo_title, page.search_description = data.seo_title, data.seo_description
    page._skip_editorial_checks = True
    if is_new:
        parent.add_child(instance=page)
    page.save_revision().publish()
    return page, 'created' if is_new else 'updated'


def import_canada_locations(
    shop,
    root_page,
    *,
    locale_code: str = DEFAULT_LOCALE_CODE,
    new_only: bool = False,
    dry_run: bool = False,
    plan: CanadaPlan | None = None,
) -> dict[str, Any]:
    """Import regions and locations; returns counts per kind plus the plan's warnings."""
    plan = plan or fetch_plan(shop)
    stats = {
        'regions': _empty_import_stats(),
        'locations': _empty_import_stats(),
        'unparented': len(plan.unparented),
        'skipped_inactive': plan.skipped,
        'warnings': list(plan.warnings),
        'dry_run': dry_run,
    }
    if dry_run:
        for kind, model, items in (
            ('regions', RegionPage, plan.regions), ('locations', LocationPage, plan.locations),
        ):
            existing = set(model.objects.filter(shopify_id__in=[i.gid for i in items]).values_list('shopify_id', flat=True))
            stats[kind]['updated' if not new_only else 'skipped'] = len(existing)
            stats[kind]['created'] = len(items) - len(existing)
        return stats

    locale = _wagtail_locale(locale_code)
    region_pages: dict[str, RegionPage] = {}
    for region in plan.regions:
        try:
            page, outcome = _upsert_region(root_page, locale, region, new_only=new_only)
        except Exception:
            logger.exception('Region import failed handle=%s', region.handle)
            stats['regions']['errors'] += 1
            continue
        stats['regions'][outcome] += 1
        region_pages[region.gid] = page

    default_country = shopify_country(locale_code) or _CANADA
    for location in plan.locations:
        parent = region_pages.get(location.region_gid) if location.region_gid else None
        if parent is None:
            # Unlisted, or its region failed: keep the content, loose under the root.
            parent = root_page
        try:
            _, outcome = _upsert_location(
                parent, locale, location,
                region_country=(parent.country if isinstance(parent, RegionPage) else default_country),
                new_only=new_only,
            )
        except Exception:
            logger.exception('Location import failed handle=%s', location.handle)
            stats['locations']['errors'] += 1
            continue
        stats['locations'][outcome] += 1
    return stats

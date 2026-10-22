"""
Generalized Shopify metaobject definitions for regions, locations, FAQs and content links.

Code only. Nothing here runs against the store on its own: the Shopify definitions and
data stay as they are until the project is operational. ``plan_definitions`` computes the
difference against the live store with read queries; ``apply_definitions`` writes and is
refused unless ``settings.SHOPIFY_SCHEMA_CHANGES_ENABLED`` is on.

What is generalized
-------------------
- ``region``: one page per province or state, publishable as a web page, linking to its
  locations through ``location_pages``. Adds the United States to ``country``, a ``locale``
  and ``faqs``.
- ``location_page``: one location type for Canada and the United States. Keeps every live
  field and adds the US layout (intro, sections 2 and 3, brand, map, closing content), a
  ``slug``, a ``locale`` and ``faqs``. It makes the US-only ``local_page`` retirable.
- ``faq``: one question and answer per entry (rich text answer, translatable). FAQs are
  entries of this type referenced from other metaobjects, not JSON in metafields.
- ``content_links``: the definitions that were missing (related products, collections,
  articles, glossary terms, internal links, FAQs) as one metaobject instead of loose
  metafields.

Language codes follow Shopify (``en``/``es``/``fr``): see ``shopify_content/shopify_languages.py``.
Existing field keys and types are kept exactly as in the live store; new fields are additive.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from django.conf import settings

from metaobjects.shopify_metaobjects.definition import (
    MetaobjectDefinitionSpec,
    MetaobjectFieldSpec,
)
from metaobjects.shopify_metaobjects.exceptions import DefinitionError

FAQ_TYPE = 'faq'
REGION_TYPE = 'region'
LOCATION_TYPE = 'location_page'
CONTENT_LINKS_TYPE = 'content_links'
SEO_KEYWORD_TYPE = 'seo_keyword'
GLOSSARY_TYPE = 'glossary_term'
LEGACY_US_LOCATION_TYPE = 'local_page'

COUNTRIES = ['Canada', 'United States']

# Order matters: a definition can only reference one that already exists.
DEFINITION_ORDER = (FAQ_TYPE, LOCATION_TYPE, REGION_TYPE, CONTENT_LINKS_TYPE)

SINGLE = 'single_line_text_field'
MULTI = 'multi_line_text_field'
RICH = 'rich_text_field'
JSON = 'json'

# One pointer metafield per resource attaches a content_links entry. Shopify requires a
# reference to connect a metaobject to a product, collection, article, blog or page.
CONTENT_LINKS_POINTER_OWNERS = ('PRODUCT', 'COLLECTION', 'ARTICLE', 'BLOG', 'PAGE')
CONTENT_LINKS_POINTER_METAFIELD = {'namespace': 'custom', 'key': 'content_links'}


def _url_handle(setting_name: str, default: str) -> str:
    return getattr(settings, setting_name, '') or default


def _ref(definition_type: str, gid_for: Callable[[str], str]) -> list[dict[str, Any]]:
    return [{'name': 'metaobject_definition_id', 'value': gid_for(definition_type)}]


def placeholder_gid(definition_type: str) -> str:
    """Stand-in used when rendering a spec without a store (dry run)."""
    return f'<definition:{definition_type}>'


def faq_definition(gid_for: Callable[[str], str] = placeholder_gid) -> MetaobjectDefinitionSpec:
    """One question and answer per entry. Mirrors the live ``faq`` definition."""
    return MetaobjectDefinitionSpec(
        type=FAQ_TYPE,
        name='FAQ set',
        description='One question and its answer. Referenced from content_links, region and location_page.',
        display_name_field='question',
        capabilities={'publishable': {'enabled': True}},
        access={'admin': 'PUBLIC_READ_WRITE', 'storefront': 'PUBLIC_READ'},
        fields=[
            MetaobjectFieldSpec(key='question', name='Question', type=SINGLE),
            MetaobjectFieldSpec(key='answer', name='Answer', type=RICH),
        ],
    )


def region_definition(gid_for: Callable[[str], str] = placeholder_gid) -> MetaobjectDefinitionSpec:
    """
    A province or state published as a web page that links to its locations.

    Live fields are unchanged; ``country`` also accepts the United States and ``locale``
    and ``faqs`` are new.
    """
    return MetaobjectDefinitionSpec(
        type=REGION_TYPE,
        name='Region Pages',
        description='Region Page',
        display_name_field='province',
        capabilities={
            'publishable': {'enabled': True},
            'onlineStore': {'enabled': True, 'data': {
                'urlHandle': _url_handle('REGION_PAGE_URL_HANDLE', 'canada'),
            }},
            'renderable': {'enabled': True, 'data': {
                'metaTitleKey': 'metatitulo',
                'metaDescriptionKey': 'metadescription',
            }},
        },
        access={'admin': 'PUBLIC_READ_WRITE', 'storefront': 'PUBLIC_READ'},
        fields=[
            MetaobjectFieldSpec(key='province', name='province', type=SINGLE, required=True),
            MetaobjectFieldSpec(
                key='province_code', name='Province Code', type=SINGLE, required=True,
                validations=[{'name': 'min', 'value': '2'}, {'name': 'max', 'value': '2'}],
            ),
            MetaobjectFieldSpec(
                key='country', name='country', type=SINGLE,
                validations=[{'name': 'choices', 'value': COUNTRIES}],
            ),
            MetaobjectFieldSpec(key='greeting', name='Greeting', type=MULTI),
            MetaobjectFieldSpec(key='header1', name='Header1', type=SINGLE),
            MetaobjectFieldSpec(key='header2', name='Header2', type=SINGLE),
            MetaobjectFieldSpec(
                key='location_pages', name='Location_Pages', type='list.metaobject_reference',
                validations=_ref(LOCATION_TYPE, gid_for),
            ),
            MetaobjectFieldSpec(key='metatitulo', name='metatitulo', type=SINGLE, required=True),
            MetaobjectFieldSpec(key='metadescription', name='metadescription', type=MULTI, required=True),
            MetaobjectFieldSpec(key='locale', name='Locale', type=SINGLE,
                                description='Shopify language code: en, es or fr.'),
            MetaobjectFieldSpec(
                key='faqs', name='FAQs', type='list.metaobject_reference',
                validations=_ref(FAQ_TYPE, gid_for),
            ),
        ],
    )


def location_page_definition(gid_for: Callable[[str], str] = placeholder_gid) -> MetaobjectDefinitionSpec:
    """
    One location type for Canada and the United States.

    Live fields are unchanged. The US layout of ``local_page`` is added under clean names
    (``section2_title`` instead of ``titulo_2``); ``header1``, ``header2``, ``greeting`` and
    ``province`` already cover ``titulo``, ``subtitulo``, ``intro`` and ``state``.
    """
    return MetaobjectDefinitionSpec(
        type=LOCATION_TYPE,
        name='Location Page',
        description='Information about service areas (cities)',
        display_name_field='city',
        capabilities={
            'publishable': {'enabled': True},
            'onlineStore': {'enabled': True, 'data': {
                'urlHandle': _url_handle('LOCATION_PAGE_URL_HANDLE', 'canada-location'),
            }},
            'renderable': {'enabled': True, 'data': {
                'metaTitleKey': 'meta_titulo',
                'metaDescriptionKey': 'meta_description',
            }},
        },
        access={'storefront': 'PUBLIC_READ'},
        fields=[
            # Live fields, unchanged.
            MetaobjectFieldSpec(key='city', name='City', type=SINGLE),
            MetaobjectFieldSpec(key='province', name='Province', type=SINGLE),
            MetaobjectFieldSpec(
                key='province_page', name='province_page', type='metaobject_reference',
                validations=_ref(REGION_TYPE, gid_for),
            ),
            MetaobjectFieldSpec(key='country', name='Country', type=SINGLE),
            MetaobjectFieldSpec(key='header1', name='Header1', type=SINGLE),
            MetaobjectFieldSpec(key='header2', name='Header2', type=SINGLE),
            MetaobjectFieldSpec(key='greeting', name='Greeting', type=MULTI),
            MetaobjectFieldSpec(key='discreet_shipping', name='discreet_shipping', type=MULTI),
            MetaobjectFieldSpec(key='quality_focus', name='quality_focus', type=MULTI),
            MetaobjectFieldSpec(key='body_safe_materials', name='body_safe_materials', type=MULTI),
            MetaobjectFieldSpec(key='meta_description', name='meta_description', type=MULTI),
            MetaobjectFieldSpec(key='meta_titulo', name='meta_titulo', type=SINGLE),
            MetaobjectFieldSpec(
                key='seo_keyword', name='seo_keyword', type='metaobject_reference',
                validations=_ref(SEO_KEYWORD_TYPE, gid_for),
            ),
            # Added by the generalization.
            MetaobjectFieldSpec(key='slug', name='Slug', type=SINGLE),
            MetaobjectFieldSpec(key='locale', name='Locale', type=SINGLE,
                                description='Shopify language code: en, es or fr.'),
            MetaobjectFieldSpec(key='intro', name='Intro', type=RICH),
            MetaobjectFieldSpec(key='section2_title', name='Section 2 title', type=SINGLE),
            MetaobjectFieldSpec(key='section2_subtitle', name='Section 2 subtitle', type=SINGLE),
            MetaobjectFieldSpec(key='section2_content', name='Section 2 content', type=RICH),
            MetaobjectFieldSpec(key='section3_title', name='Section 3 title', type=SINGLE),
            MetaobjectFieldSpec(key='section3_subtitle', name='Section 3 subtitle', type=SINGLE),
            MetaobjectFieldSpec(key='section3_content', name='Section 3 content', type=RICH),
            MetaobjectFieldSpec(key='brand_section_title', name='Brand section title', type=SINGLE),
            MetaobjectFieldSpec(key='brand_section_subtitle', name='Brand section subtitle', type=SINGLE),
            MetaobjectFieldSpec(key='brand_section_content', name='Brand section content', type=RICH),
            MetaobjectFieldSpec(key='map_title', name='Map title', type=SINGLE),
            MetaobjectFieldSpec(key='map_content', name='Map content', type=RICH),
            MetaobjectFieldSpec(key='after_page_content', name='After page content', type=RICH),
            MetaobjectFieldSpec(
                key='faqs', name='FAQs', type='list.metaobject_reference',
                validations=_ref(FAQ_TYPE, gid_for),
            ),
        ],
    )


def content_links_definition(gid_for: Callable[[str], str] = placeholder_gid) -> MetaobjectDefinitionSpec:
    """The links and FAQs that used to be loose ``custom.related_*`` / FAQ metafields."""
    return MetaobjectDefinitionSpec(
        type=CONTENT_LINKS_TYPE,
        name='Content links',
        description='Related content and FAQs for a product, collection, article, blog or page.',
        display_name_field='title',
        capabilities={'publishable': {'enabled': True}},
        access={'admin': 'PUBLIC_READ_WRITE', 'storefront': 'PUBLIC_READ'},
        fields=[
            MetaobjectFieldSpec(key='title', name='Title', type=SINGLE, required=True),
            MetaobjectFieldSpec(key='related_products', name='Related products', type='list.product_reference'),
            MetaobjectFieldSpec(key='related_collections', name='Related collections',
                                type='list.collection_reference'),
            MetaobjectFieldSpec(key='related_articles', name='Related articles', type='list.article_reference'),
            MetaobjectFieldSpec(
                key='related_glossary_terms', name='Related glossary terms', type='list.metaobject_reference',
                validations=_ref(GLOSSARY_TYPE, gid_for),
            ),
            MetaobjectFieldSpec(key='internal_links', name='Internal links', type='list.link'),
            MetaobjectFieldSpec(
                key='faqs', name='FAQs', type='list.metaobject_reference',
                validations=_ref(FAQ_TYPE, gid_for),
            ),
        ],
    )


DEFINITION_BUILDERS: dict[str, Callable[..., MetaobjectDefinitionSpec]] = {
    FAQ_TYPE: faq_definition,
    LOCATION_TYPE: location_page_definition,
    REGION_TYPE: region_definition,
    CONTENT_LINKS_TYPE: content_links_definition,
}


def _build(definition_type: str, gid_for: Callable[[str], str | None]) -> MetaobjectDefinitionSpec:
    """
    Build one definition. A reference whose target does not exist yet (``gid_for`` returns
    None) is left out, to be added on the second pass: region and location_page reference
    each other, so neither can carry its reference when it is created first.
    """
    spec = DEFINITION_BUILDERS[definition_type](gid_for)
    spec.fields = [
        spec_field for spec_field in spec.fields
        if not any(validation.get('value') is None for validation in spec_field.validations)
    ]
    return spec


def build_definitions(gid_for: Callable[[str], str | None] = placeholder_gid) -> list[MetaobjectDefinitionSpec]:
    """The generalized definitions, in the order they must exist."""
    return [_build(definition_type, gid_for) for definition_type in DEFINITION_ORDER]


# ---------------------------------------------------------------------------
# Plan against the live store (read only)
# ---------------------------------------------------------------------------

@dataclass
class DefinitionPlan:
    type: str
    action: str  # 'create' | 'update' | 'unchanged'
    missing_fields: list[str] = field(default_factory=list)
    changed_validations: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    capability_changes: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            'type': self.type,
            'action': self.action,
            'missing_fields': self.missing_fields,
            'changed_validations': self.changed_validations,
            'capability_changes': self.capability_changes,
        }


def _normalized_validations(validations: list[dict[str, Any]] | None) -> dict[str, Any]:
    """Validations as {name: value}, comparing JSON values by content, not by spelling."""
    import json

    result: dict[str, Any] = {}
    for validation in validations or []:
        value = validation.get('value')
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except ValueError:
                pass
        result[validation['name']] = value
    return result


def _diff_definition(
    existing: MetaobjectDefinitionSpec | None, desired: MetaobjectDefinitionSpec,
) -> DefinitionPlan:
    from metaobjects.shopify_metaobjects.client import _capabilities_diff

    if existing is None:
        return DefinitionPlan(
            type=desired.type, action='create',
            missing_fields=[spec_field.key for spec_field in desired.fields],
        )
    existing_fields = {spec_field.key: spec_field for spec_field in existing.fields}
    missing = [spec_field.key for spec_field in desired.fields if spec_field.key not in existing_fields]

    changed: dict[str, list[dict[str, Any]]] = {}
    for spec_field in desired.fields:
        live = existing_fields.get(spec_field.key)
        if live is None or live.type != spec_field.type:
            continue
        # Reference validations point at definition ids, which differ per store: compare
        # only the validations that carry a literal (choices, min, max).
        wanted = {
            name: value for name, value in _normalized_validations(spec_field.validations).items()
            if name != 'metaobject_definition_id'
        }
        current = {
            name: value for name, value in _normalized_validations(live.validations).items()
            if name != 'metaobject_definition_id'
        }
        if wanted and wanted != current:
            changed[spec_field.key] = spec_field.validations

    capability_changes = _capabilities_diff(existing.capabilities, desired.capabilities) or {}
    action = 'update' if (missing or changed or capability_changes) else 'unchanged'
    return DefinitionPlan(
        type=desired.type, action=action, missing_fields=missing,
        changed_validations=changed, capability_changes=capability_changes,
    )


def plan_definitions(client) -> list[DefinitionPlan]:
    """Compare the generalized definitions with the live store. Read queries only."""
    plans: list[DefinitionPlan] = []
    for definition_type in DEFINITION_ORDER:
        desired = _build(definition_type, placeholder_gid)
        plans.append(_diff_definition(client.get_definition(definition_type), desired))
    return plans


# ---------------------------------------------------------------------------
# Apply (guarded)
# ---------------------------------------------------------------------------

class SchemaChangesDisabled(DefinitionError):
    """Raised when something tries to write definitions while the freeze is on."""


def schema_changes_enabled() -> bool:
    return bool(getattr(settings, 'SHOPIFY_SCHEMA_CHANGES_ENABLED', False))


def apply_definitions(client) -> list[DefinitionPlan]:
    """
    Create or extend the generalized definitions in the store.

    Refused unless ``SHOPIFY_SCHEMA_CHANGES_ENABLED`` is on: Shopify definitions and data
    do not change until the project is operational. Additive for new fields; also updates
    the validations of existing fields (``region.country`` gains the United States).
    """
    if not schema_changes_enabled():
        raise SchemaChangesDisabled(
            'Shopify schema changes are disabled (SHOPIFY_SCHEMA_CHANGES_ENABLED is off). '
            'Definitions stay as they are until the project is operational.'
        )

    gids: dict[str, str] = {}

    def gid_for(definition_type: str) -> str | None:
        if definition_type not in gids:
            existing = client.get_definition(definition_type)
            if existing is None or not existing.id:
                return None
            gids[definition_type] = existing.id
        return gids[definition_type]

    applied: list[DefinitionPlan] = []
    # Two passes: references between definitions that did not exist yet are added in the second.
    for _ in range(2):
        for definition_type in DEFINITION_ORDER:
            desired = _build(definition_type, gid_for)
            existing = client.get_definition(definition_type)
            plan = _diff_definition(existing, desired)
            if plan.action == 'create':
                created = client.create_definition(desired)
                if created.id:
                    gids[definition_type] = created.id
            elif plan.action == 'update':
                missing = [spec_field for spec_field in desired.fields if spec_field.key in plan.missing_fields]
                client.update_definition(
                    existing.id,
                    fields=missing or None,
                    capabilities=plan.capability_changes or None,
                    field_validations=plan.changed_validations or None,
                )
                gids.setdefault(definition_type, existing.id)
            if plan.action != 'unchanged':
                applied.append(plan)
    return applied

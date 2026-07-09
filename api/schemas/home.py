from typing import Any, Dict, Optional
from datetime import datetime
from ninja import Schema
from pydantic import Field

from wagtail.rich_text import expand_db_html

from .common import LocaleCreateFields, LocalePatchFields, LocaleOutFields, StorefrontUrlOutFields

RICH_TEXT_DESCRIPTION = (
    "Rich text content as HTML string. On read, internal Wagtail references are expanded to URLs. "
    "On write, pass HTML directly. Empty string clears the field."
)

SHOPIFY_LOCALE_DESCRIPTION = (
    "Shopify metaobject locale field pushed on sync (e.g. 'en-US', 'es-US'). "
    "Distinct from Wagtail page locale. Blank uses Wagtail locale on sync."
)


class HomeIn(LocaleCreateFields):
    hero_heading: str = Field(
        ...,
        description="Primary hero headline. Also used as Wagtail Page.title when creating.",
        max_length=255,
    )
    shopify_id: Optional[str] = Field(
        None,
        description=(
            "Shopify metaobject GID after first push. "
            "Leave null for new pages — populated after POST /home/{id}/push."
        ),
    )
    handle: Optional[str] = Field(
        None,
        description="Ignored. Handle is auto-derived as home-<locale>. Set locale instead.",
    )
    hero_eyebrow: Optional[str] = Field(None, description="Hero eyebrow text above H1.", max_length=60)
    hero_subheading: Optional[str] = Field(None, description="Hero subheading.", max_length=500)
    hero_body: Optional[str] = Field(None, description=RICH_TEXT_DESCRIPTION)
    hero_primary_cta_label: Optional[str] = Field(None, max_length=255)
    hero_primary_cta_url: Optional[str] = Field(None, max_length=500)
    hero_secondary_cta_label: Optional[str] = Field(None, max_length=255)
    hero_secondary_cta_url: Optional[str] = Field(None, max_length=500)
    hero_image_url: Optional[str] = Field(
        None,
        description="Optional absolute hero image URL pushed to Shopify.",
        max_length=500,
    )
    sections_json: Optional[Dict[str, Any]] = Field(
        None,
        description=(
            "Home sections JSON (version 1). References use page_id (Wagtail FK). "
            "Synced to Shopify metaobject sections_json + native reference fields."
        ),
    )
    shopify_locale: Optional[str] = Field(None, description=SHOPIFY_LOCALE_DESCRIPTION, max_length=20)
    seo_title: Optional[str] = Field(None, max_length=255)
    search_description: Optional[str] = Field(None)
    sync_enabled: Optional[bool] = Field(
        True,
        description="When true, publishing triggers outbound sync to Shopify metaobject.",
    )
    parent_page_id: Optional[int] = Field(
        None,
        description=(
            "Wagtail page ID of the ShopifyRootPage parent (expected slug=cms-home). "
            "Omit to use slug-based resolution."
        ),
    )


class HomePatch(LocalePatchFields):
    hero_heading: Optional[str] = Field(None, max_length=255)
    shopify_id: Optional[str] = Field(None)
    handle: Optional[str] = Field(
        None,
        description="Ignored. Handle is read-only and derived from locale.",
    )
    hero_eyebrow: Optional[str] = Field(None, max_length=60)
    hero_subheading: Optional[str] = Field(None)
    hero_body: Optional[str] = Field(None, description=RICH_TEXT_DESCRIPTION)
    hero_primary_cta_label: Optional[str] = Field(None)
    hero_primary_cta_url: Optional[str] = Field(None)
    hero_secondary_cta_label: Optional[str] = Field(None)
    hero_secondary_cta_url: Optional[str] = Field(None)
    hero_image_url: Optional[str] = Field(None)
    sections_json: Optional[Dict[str, Any]] = Field(None)
    shopify_locale: Optional[str] = Field(None, description=SHOPIFY_LOCALE_DESCRIPTION)
    seo_title: Optional[str] = Field(None, max_length=255)
    search_description: Optional[str] = Field(None)
    sync_enabled: Optional[bool] = Field(None)
    publish: bool = Field(
        False,
        description="When true, publishes after saving. sync_enabled=true triggers outbound sync on publish.",
    )


class HomeOut(StorefrontUrlOutFields, LocaleOutFields):
    id: int = Field(..., description="Wagtail page ID for /home/{page_id}/ endpoints.")
    shopify_id: str = Field(..., description="Shopify metaobject GID. Empty if never pushed.")
    hero_heading: str = Field(..., description="Hero headline.")
    title: str = Field(..., description="Wagtail Page.title (mirrors hero_heading).")
    handle: str = Field(..., description="Shopify metaobject handle (home-<locale>).")
    slug: str = Field(..., description="Wagtail page slug; matches handle.")
    hero_eyebrow: str = Field(..., description="Hero eyebrow.")
    hero_subheading: str = Field(..., description="Hero subheading.")
    hero_body: str = Field(..., description="Hero body HTML.")
    hero_primary_cta_label: str = Field(..., description="Primary CTA label.")
    hero_primary_cta_url: str = Field(..., description="Primary CTA URL.")
    hero_secondary_cta_label: str = Field(..., description="Secondary CTA label.")
    hero_secondary_cta_url: str = Field(..., description="Secondary CTA URL.")
    hero_image_url: str = Field(..., description="Hero image URL pushed to Shopify.")
    sections_json: Dict[str, Any] = Field(default_factory=dict, description="Extensible sections JSON.")
    shopify_locale: str = Field(..., description="Shopify locale pushed on sync.")
    seo_title: str = Field(..., description="SEO meta title.")
    search_description: str = Field(..., description="SEO meta description.")
    sync_enabled: bool = Field(..., description="Outbound sync enabled on publish.")
    last_synced_at: Optional[datetime] = Field(None, description="Last successful push timestamp.")
    live: bool = Field(..., description="True if published in Wagtail.")
    locale: str = Field(..., description="Wagtail locale code.")
    url: Optional[str] = Field(None, description="Public page URL if site configured.")
    first_published_at: Optional[datetime] = Field(None)
    last_published_at: Optional[datetime] = Field(None)

    @staticmethod
    def resolve_translation_page_ids(obj):
        from ..locale_utils import resolve_translation_page_ids
        return resolve_translation_page_ids(obj)

    @staticmethod
    def _expand_richtext(value):
        if not value:
            return ''
        return expand_db_html(str(value))

    @staticmethod
    def resolve_hero_body(obj):
        return HomeOut._expand_richtext(obj.hero_body)

    @staticmethod
    def resolve_locale(obj):
        return str(obj.locale)

    @staticmethod
    def resolve_url(obj):
        try:
            return obj.get_full_url()
        except Exception:
            return None

    @staticmethod
    def resolve_title(obj):
        return obj.title

    @staticmethod
    def resolve_sections_json(obj):
        return obj.sections_json or {}

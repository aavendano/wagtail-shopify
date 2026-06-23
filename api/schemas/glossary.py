from typing import List, Literal, Optional
from datetime import datetime
from ninja import Schema
from pydantic import Field

from wagtail.rich_text import expand_db_html

from .common import LocaleCreateFields, LocalePatchFields, LocaleOutFields

RICH_TEXT_DESCRIPTION = (
    "Rich text content as HTML string. On read, internal Wagtail references are expanded to URLs. "
    "On write, pass HTML directly. Empty string clears the field."
)

LOCALE_CODE_DESCRIPTION = (
    "Shopify metaobject locale field pushed on sync. Values: 'en', 'es', 'fr'. "
    "Distinct from Wagtail page locale used for translation linking."
)


class RelatedLinkSchema(Schema):
    type: Literal['product', 'collection', 'blog', 'article', 'page', 'metaobject'] = Field(
        ...,
        description="Target resource type in Shopify.",
    )
    handle: str = Field(..., description="Resource handle in Shopify.")
    label: str = Field(..., description="Display label for the link.")
    blog_handle: Optional[str] = Field(
        None,
        description="Required when type is 'article'. Parent blog handle.",
    )
    url_handle: Optional[str] = Field(
        None,
        description="Required when type is 'metaobject'. Metaobject definition URL handle.",
    )


class ExternalLinkSchema(Schema):
    url: str = Field(..., description="Absolute external URL.")
    label: str = Field(..., description="Display label for the external link.")


class GlossaryTermIn(LocaleCreateFields):
    term: str = Field(
        ...,
        description="Glossary term text. Also used as Wagtail Page.title. Required.",
        max_length=255,
    )
    shopify_id: Optional[str] = Field(
        None,
        description=(
            "Shopify metaobject GID after first push. Format: 'gid://shopify/Metaobject/12345678'. "
            "Leave null for new pages — populated automatically after POST /glossary/{id}/push."
        ),
    )
    handle: Optional[str] = Field(
        None,
        description=(
            "Shopify metaobject handle (URL slug). Defaults to slugified term. "
            "Used in storefront metaobject URLs."
        ),
    )
    definition: Optional[str] = Field(None, description=RICH_TEXT_DESCRIPTION)
    locale_code: Optional[Literal['en', 'es', 'fr']] = Field(
        'en',
        description=LOCALE_CODE_DESCRIPTION,
    )
    related_links: Optional[List[RelatedLinkSchema]] = Field(
        None,
        description="Internal Shopify/Wagtail links synced as JSON on push.",
    )
    external_links: Optional[List[ExternalLinkSchema]] = Field(
        None,
        description="External reference links synced as JSON on push.",
    )
    sync_enabled: Optional[bool] = Field(
        True,
        description="When true, publishing triggers outbound sync to Shopify metaobject.",
    )
    parent_page_id: Optional[int] = Field(
        None,
        description=(
            "Wagtail page ID of the ShopifyRootPage parent (expected slug=glossary). "
            "Omit to use slug-based resolution."
        ),
    )


class GlossaryTermPatch(LocalePatchFields):
    term: Optional[str] = Field(None, description="Update term and Page.title.", max_length=255)
    shopify_id: Optional[str] = Field(None, description="Set or update Shopify metaobject GID.")
    handle: Optional[str] = Field(None, description="Update metaobject handle; slug updated to match.")
    definition: Optional[str] = Field(None, description=RICH_TEXT_DESCRIPTION)
    locale_code: Optional[Literal['en', 'es', 'fr']] = Field(
        None,
        description=LOCALE_CODE_DESCRIPTION,
    )
    related_links: Optional[List[RelatedLinkSchema]] = Field(
        None,
        description="Replace related links. Pass [] to clear. Omit to leave unchanged.",
    )
    external_links: Optional[List[ExternalLinkSchema]] = Field(
        None,
        description="Replace external links. Pass [] to clear. Omit to leave unchanged.",
    )
    sync_enabled: Optional[bool] = Field(None, description="Enable or disable Shopify sync on publish.")
    publish: bool = Field(
        False,
        description="When true, publishes after saving. sync_enabled=true triggers outbound sync on publish.",
    )


class GlossaryTermOut(LocaleOutFields):
    id: int = Field(..., description="Wagtail page ID for /glossary/{page_id}/ endpoints.")
    shopify_id: str = Field(
        ...,
        description="Shopify metaobject GID. Empty if never pushed.",
    )
    term: str = Field(..., description="Glossary term text.")
    title: str = Field(..., description="Wagtail Page.title (mirrors term).")
    handle: str = Field(..., description="Shopify metaobject handle.")
    slug: str = Field(..., description="Wagtail page slug.")
    definition: str = Field(..., description="Definition HTML.")
    locale_code: str = Field(..., description="Shopify locale pushed on sync (en/es/fr).")
    related_links: List[RelatedLinkSchema] = Field(
        default_factory=list,
        description="Internal links synced to Shopify.",
    )
    external_links: List[ExternalLinkSchema] = Field(
        default_factory=list,
        description="External links synced to Shopify.",
    )
    sync_enabled: bool = Field(..., description="Outbound sync enabled on publish.")
    last_synced_at: Optional[datetime] = Field(
        None,
        description="UTC timestamp of last successful push to Shopify metaobject.",
    )
    live: bool = Field(..., description="True if published in Wagtail.")
    locale: str = Field(
        ...,
        description="Shopify metaobject locale pushed on sync (en/es/fr). Mirrors locale_code.",
    )
    url: Optional[str] = Field(None, description="Public page URL if site configured.")
    first_published_at: Optional[datetime] = Field(None, description="First publish timestamp.")
    last_published_at: Optional[datetime] = Field(None, description="Most recent publish timestamp.")

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
    def resolve_definition(obj):
        return GlossaryTermOut._expand_richtext(obj.definition)

    @staticmethod
    def resolve_related_links(obj):
        return obj.related_links or []

    @staticmethod
    def resolve_external_links(obj):
        return obj.external_links or []

    @staticmethod
    def resolve_locale(obj):
        return obj.locale_code

    @staticmethod
    def resolve_last_synced_at(obj):
        return obj.last_synced_at

    @staticmethod
    def resolve_first_published_at(obj):
        return obj.first_published_at

    @staticmethod
    def resolve_last_published_at(obj):
        return obj.last_published_at

    @staticmethod
    def resolve_url(obj):
        try:
            return obj.get_full_url()
        except Exception:
            return None

    @staticmethod
    def resolve_title(obj):
        return obj.title

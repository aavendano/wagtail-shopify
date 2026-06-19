from typing import List, Optional
from datetime import datetime
from ninja import Schema
from pydantic import Field

from wagtail.rich_text import expand_db_html

from .common import FAQSchema, LocaleCreateFields, LocalePatchFields, LocaleOutFields

RICH_TEXT_DESCRIPTION = (
    "Rich text content as HTML string. On read, internal Wagtail references are expanded to URLs. "
    "On write, pass HTML directly. Empty string clears the field."
)

SHOPIFY_LOCALE_DESCRIPTION = (
    "Shopify metaobject locale field pushed on sync (e.g. 'en-US', 'es-US'). "
    "Distinct from Wagtail page locale. Blank uses Wagtail locale mapping on sync."
)


class LocationIn(LocaleCreateFields):
    titulo: str = Field(
        ...,
        description=(
            "Primary location page title (hero). Also used as Wagtail Page.title. Required."
        ),
        max_length=255,
    )
    shopify_id: Optional[str] = Field(
        None,
        description=(
            "Shopify metaobject GID after first push. Format: 'gid://shopify/Metaobject/12345678'. "
            "Leave null for new pages — populated automatically after POST /locations/{id}/push."
        ),
    )
    handle: Optional[str] = Field(
        None,
        description=(
            "Shopify metaobject handle (URL slug). Defaults to slugified titulo. "
            "Used in storefront metaobject URLs."
        ),
    )
    subtitulo: Optional[str] = Field(None, description="Hero subtitle.", max_length=255)
    intro: Optional[str] = Field(None, description=RICH_TEXT_DESCRIPTION)
    country: Optional[str] = Field(None, description="Country name.", max_length=100)
    state: Optional[str] = Field(None, description="State or province.", max_length=100)
    city: Optional[str] = Field(None, description="City name.", max_length=100)
    titulo_2: Optional[str] = Field(None, description="Section 2 title.", max_length=255)
    subtitulo_h2: Optional[str] = Field(None, description="Section 2 subtitle.", max_length=255)
    content_2: Optional[str] = Field(None, description=RICH_TEXT_DESCRIPTION)
    titulo_3: Optional[str] = Field(None, description="Section 3 title.", max_length=255)
    subtitulo_3: Optional[str] = Field(None, description="Section 3 subtitle.", max_length=255)
    content_3: Optional[str] = Field(None, description=RICH_TEXT_DESCRIPTION)
    brand_section_title: Optional[str] = Field(None, description="Brand section title.", max_length=255)
    brand_section_subtitle: Optional[str] = Field(None, description="Brand section subtitle.", max_length=255)
    brand_section_content: Optional[str] = Field(None, description=RICH_TEXT_DESCRIPTION)
    map_title: Optional[str] = Field(None, description="Map section title.", max_length=255)
    map_content: Optional[str] = Field(None, description=RICH_TEXT_DESCRIPTION)
    after_page_content: Optional[str] = Field(None, description=RICH_TEXT_DESCRIPTION)
    shopify_locale: Optional[str] = Field(None, description=SHOPIFY_LOCALE_DESCRIPTION, max_length=20)
    faqs: Optional[List[FAQSchema]] = Field(
        None,
        description="FAQ items synced to Shopify metaobject faqs JSON field. Pass [] to clear.",
    )
    sync_enabled: Optional[bool] = Field(
        True,
        description="When true, publishing triggers outbound sync to Shopify metaobject.",
    )


class LocationPatch(LocalePatchFields):
    titulo: Optional[str] = Field(None, description="Update hero title and Page.title.", max_length=255)
    shopify_id: Optional[str] = Field(None, description="Set or update Shopify metaobject GID.")
    handle: Optional[str] = Field(None, description="Update metaobject handle; slug updated to match.")
    subtitulo: Optional[str] = Field(None, description="Update hero subtitle.")
    intro: Optional[str] = Field(None, description=RICH_TEXT_DESCRIPTION)
    country: Optional[str] = Field(None, description="Update country.")
    state: Optional[str] = Field(None, description="Update state/province.")
    city: Optional[str] = Field(None, description="Update city.")
    titulo_2: Optional[str] = Field(None, description="Update section 2 title.")
    subtitulo_h2: Optional[str] = Field(None, description="Update section 2 subtitle.")
    content_2: Optional[str] = Field(None, description=RICH_TEXT_DESCRIPTION)
    titulo_3: Optional[str] = Field(None, description="Update section 3 title.")
    subtitulo_3: Optional[str] = Field(None, description="Update section 3 subtitle.")
    content_3: Optional[str] = Field(None, description=RICH_TEXT_DESCRIPTION)
    brand_section_title: Optional[str] = Field(None, description="Update brand section title.")
    brand_section_subtitle: Optional[str] = Field(None, description="Update brand section subtitle.")
    brand_section_content: Optional[str] = Field(None, description=RICH_TEXT_DESCRIPTION)
    map_title: Optional[str] = Field(None, description="Update map section title.")
    map_content: Optional[str] = Field(None, description=RICH_TEXT_DESCRIPTION)
    after_page_content: Optional[str] = Field(None, description=RICH_TEXT_DESCRIPTION)
    shopify_locale: Optional[str] = Field(None, description=SHOPIFY_LOCALE_DESCRIPTION)
    faqs: Optional[List[FAQSchema]] = Field(
        None,
        description="Replace all FAQs. Pass [] to clear. Omit to leave unchanged.",
    )
    sync_enabled: Optional[bool] = Field(None, description="Enable or disable Shopify sync on publish.")
    publish: bool = Field(
        False,
        description="When true, publishes after saving. sync_enabled=true triggers outbound sync on publish.",
    )


class LocationOut(LocaleOutFields):
    id: int = Field(..., description="Wagtail page ID for /locations/{page_id}/ endpoints.")
    shopify_id: str = Field(
        ...,
        description="Shopify metaobject GID. Empty if never pushed.",
    )
    titulo: str = Field(..., description="Hero title.")
    title: str = Field(..., description="Wagtail Page.title (mirrors titulo).")
    handle: str = Field(..., description="Shopify metaobject handle.")
    slug: str = Field(..., description="Wagtail page slug.")
    subtitulo: str = Field(..., description="Hero subtitle.")
    intro: str = Field(..., description="Hero intro HTML.")
    country: str = Field(..., description="Country.")
    state: str = Field(..., description="State or province.")
    city: str = Field(..., description="City.")
    titulo_2: str = Field(..., description="Section 2 title.")
    subtitulo_h2: str = Field(..., description="Section 2 subtitle.")
    content_2: str = Field(..., description="Section 2 HTML content.")
    titulo_3: str = Field(..., description="Section 3 title.")
    subtitulo_3: str = Field(..., description="Section 3 subtitle.")
    content_3: str = Field(..., description="Section 3 HTML content.")
    brand_section_title: str = Field(..., description="Brand section title.")
    brand_section_subtitle: str = Field(..., description="Brand section subtitle.")
    brand_section_content: str = Field(..., description="Brand section HTML content.")
    map_title: str = Field(..., description="Map section title.")
    map_content: str = Field(..., description="Map section HTML content.")
    after_page_content: str = Field(..., description="Closing content HTML.")
    shopify_locale: str = Field(..., description="Shopify locale pushed on sync.")
    faqs: List[FAQSchema] = Field(default_factory=list, description="FAQ items.")
    sync_enabled: bool = Field(..., description="Outbound sync enabled on publish.")
    last_synced_at: Optional[datetime] = Field(
        None,
        description="UTC timestamp of last successful push to Shopify metaobject.",
    )
    live: bool = Field(..., description="True if published in Wagtail.")
    locale: str = Field(..., description="Wagtail locale code.")
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
    def resolve_intro(obj):
        return LocationOut._expand_richtext(obj.intro)

    @staticmethod
    def resolve_content_2(obj):
        return LocationOut._expand_richtext(obj.content_2)

    @staticmethod
    def resolve_content_3(obj):
        return LocationOut._expand_richtext(obj.content_3)

    @staticmethod
    def resolve_brand_section_content(obj):
        return LocationOut._expand_richtext(obj.brand_section_content)

    @staticmethod
    def resolve_map_content(obj):
        return LocationOut._expand_richtext(obj.map_content)

    @staticmethod
    def resolve_after_page_content(obj):
        return LocationOut._expand_richtext(obj.after_page_content)

    @staticmethod
    def resolve_faqs(obj):
        return [
            {'question': faq.question, 'answer': faq.answer}
            for faq in obj.faqs.all()
        ]

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

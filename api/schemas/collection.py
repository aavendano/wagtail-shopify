from typing import Any, Dict, List, Optional
from datetime import datetime
from ninja import Schema
from pydantic import Field

from .common import MetafieldSchema, LocaleCreateFields, LocalePatchFields, LocaleOutFields, RelatedLinkSchema


SORT_ORDER_DESCRIPTION = (
    "Shopify collection sort order controlling default product display sequence. "
    "'ALPHA_ASC' — alphabetical A–Z; "
    "'ALPHA_DESC' — alphabetical Z–A; "
    "'BEST_SELLING' — by sales volume descending; "
    "'CREATED' — oldest products first; "
    "'CREATED_DESC' — newest products first (default for new collections); "
    "'MANUAL' — drag-and-drop ordering in Shopify admin (default); "
    "'PRICE_ASC' — lowest price first; "
    "'PRICE_DESC' — highest price first."
)


class CollectionIn(LocaleCreateFields):
    title: str = Field(
        ...,
        description=(
            "Collection title as it appears in Shopify storefront and admin. "
            "E.g. 'Summer Sale', 'New Arrivals'. Required."
        ),
        max_length=255,
    )
    shopify_id: Optional[str] = Field(
        None,
        description=(
            "Shopify GID linking this Wagtail page to a Shopify collection. "
            "Format: 'gid://shopify/Collection/12345678'. "
            "Leave null when creating a Wagtail-only draft. Must be set before calling /push."
        ),
    )
    handle: Optional[str] = Field(
        None,
        description=(
            "Shopify URL handle (slug) for this collection. "
            "E.g. 'summer-sale'. Used in storefront URLs: /collections/{handle}. "
            "Auto-derived from title if omitted."
        ),
    )
    sort_order: Optional[str] = Field(
        'MANUAL',
        description=SORT_ORDER_DESCRIPTION,
    )
    description: Optional[List[Dict[str, Any]]] = Field(
        None,
        description=(
            "Collection description as Wagtail StreamField block list. "
            "Each item is a dict with 'type' and 'value' keys. "
            "Rendered to HTML and pushed to Shopify as descriptionHtml. "
            "Pass [] to clear the description. Omit to leave unchanged."
        ),
    )
    seo_title: Optional[str] = Field(
        None,
        description=(
            "SEO page title override. Maps to Shopify seo.title. "
            "Appears in browser tabs and search engine results. "
            "Recommended length: 50–60 characters. Falls back to collection title if blank."
        ),
        max_length=255,
    )
    search_description: Optional[str] = Field(
        None,
        description=(
            "SEO meta description. Maps to Shopify seo.description. "
            "Appears in search engine result snippets. "
            "Recommended length: 120–160 characters."
        ),
    )
    metafields: Optional[List[MetafieldSchema]] = Field(
        None,
        description=(
            "List of Shopify metafields to attach to this collection. "
            "Replaces all existing metafields when provided. "
            "Pass [] to clear all metafields. Omit to leave unchanged."
        ),
    )
    sync_enabled: Optional[bool] = Field(
        True,
        description=(
            "When true, publishing this page triggers an outbound sync to Shopify. "
            "Set to false to make Wagtail-only edits without pushing to Shopify."
        ),
    )


class CollectionPatch(LocalePatchFields):
    title: Optional[str] = Field(
        None,
        description="Update the collection title. Omit to leave unchanged.",
        max_length=255,
    )
    shopify_id: Optional[str] = Field(
        None,
        description=(
            "Set or update the Shopify GID. Format: 'gid://shopify/Collection/12345678'. "
            "Required before using /push if not already set."
        ),
    )
    handle: Optional[str] = Field(
        None,
        description="Update the Shopify URL handle. Slug will be updated to match. Omit to leave unchanged.",
    )
    sort_order: Optional[str] = Field(
        None,
        description=SORT_ORDER_DESCRIPTION + " Omit to leave unchanged.",
    )
    description: Optional[List[Dict[str, Any]]] = Field(
        None,
        description=(
            "Replace the StreamField description blocks. Pass [] to clear. Omit to leave unchanged. "
            "Format: list of {'type': str, 'value': any} dicts."
        ),
    )
    seo_title: Optional[str] = Field(
        None,
        description="Update SEO title. Omit to leave unchanged.",
        max_length=255,
    )
    search_description: Optional[str] = Field(
        None,
        description="Update SEO meta description. Omit to leave unchanged.",
    )
    metafields: Optional[List[MetafieldSchema]] = Field(
        None,
        description=(
            "Replace all metafields. Pass [] to clear. Omit to leave unchanged. "
            "This is a full replacement, not a merge."
        ),
    )
    sync_enabled: Optional[bool] = Field(
        None,
        description="Enable or disable Shopify sync on publish. Omit to leave unchanged.",
    )
    publish: bool = Field(
        False,
        description=(
            "When true, publishes the page after saving changes. "
            "If sync_enabled=true on the page, publishing triggers an outbound sync to Shopify. "
            "When false (default), changes are saved as a draft only."
        ),
    )


class CollectionOut(LocaleOutFields):
    id: int = Field(
        ...,
        description="Wagtail page ID. Use this as page_id in all /collections/{page_id}/ endpoints.",
    )
    shopify_id: str = Field(
        ...,
        description=(
            "Shopify GID for this collection. "
            "Format: 'gid://shopify/Collection/12345678'. "
            "Empty string if not yet linked to Shopify."
        ),
    )
    title: str = Field(..., description="Collection title.")
    handle: str = Field(..., description="Shopify URL handle. Used in storefront URLs: /collections/{handle}.")
    slug: str = Field(..., description="Wagtail page slug (mirrors handle).")
    sort_order: str = Field(
        ...,
        description="Current collection sort order. One of: ALPHA_ASC, ALPHA_DESC, BEST_SELLING, CREATED, CREATED_DESC, MANUAL, PRICE_ASC, PRICE_DESC.",
    )
    description: List[Dict[str, Any]] = Field(
        ...,
        description=(
            "StreamField description blocks. Each item has 'type' and 'value' keys. "
            "Rendered to HTML and pushed to Shopify as descriptionHtml on sync."
        ),
    )
    seo_title: str = Field(..., description="SEO title. Maps to Shopify seo.title.")
    search_description: str = Field(..., description="SEO meta description. Maps to Shopify seo.description.")
    image_url: str = Field('', description="Absolute Shopify collection image URL from pull.")
    image_alt_text: str = Field('', description="Alt text for the collection image URL.")
    metafields: List[Dict[str, Any]] = Field(
        ...,
        description="Attached Shopify metafields with namespace, key, type, and value.",
    )
    related_links: List[RelatedLinkSchema] = Field(
        default_factory=list,
        description="Semantic internal links from Wagtail FK relations (auto + manual).",
    )
    sync_enabled: bool = Field(..., description="When true, publishing triggers an outbound sync to Shopify.")
    last_synced_at: Optional[datetime] = Field(
        None,
        description="UTC timestamp of the last successful outbound sync to Shopify. Null if never synced.",
    )
    live: bool = Field(..., description="True if the page is published (live) in Wagtail.")
    locale: str = Field(..., description="Wagtail locale code, e.g. 'en-US', 'es-US', 'en-CA', 'fr-CA'.")
    url: Optional[str] = Field(None, description="Full public URL of this page. Null if the site is not configured.")
    first_published_at: Optional[datetime] = Field(None, description="UTC timestamp when this page was first published.")
    last_published_at: Optional[datetime] = Field(None, description="UTC timestamp of the most recent publish.")

    @staticmethod
    def resolve_translation_page_ids(obj):
        from ..locale_utils import resolve_translation_page_ids
        return resolve_translation_page_ids(obj)

    @staticmethod
    def resolve_description(obj):
        # #region agent log
        import json, time
        try:
            description = list(obj.description.raw_data) if obj.description else []
            with open('/home/alejandro/apps/wagtail-shopify/.cursor/debug-fdc58d.log', 'a', encoding='utf-8') as _f:
                _f.write(json.dumps({'sessionId':'fdc58d','hypothesisId':'B','location':'collection.py:resolve_description','message':'description resolved','data':{'page_id':getattr(obj,'pk',None),'block_count':len(description)},'timestamp':int(time.time()*1000),'runId':'post-fix'})+'\n')
            return description
        except Exception as exc:
            with open('/home/alejandro/apps/wagtail-shopify/.cursor/debug-fdc58d.log', 'a', encoding='utf-8') as _f:
                _f.write(json.dumps({'sessionId':'fdc58d','hypothesisId':'B','location':'collection.py:resolve_description','message':'description resolve failed','data':{'page_id':getattr(obj,'pk',None),'error':type(exc).__name__,'detail':str(exc)},'timestamp':int(time.time()*1000),'runId':'post-fix'})+'\n')
            raise
        # #endregion

    @staticmethod
    def resolve_metafields(obj):
        return [
            {"namespace": m.namespace, "key": m.key, "type": m.type, "value": m.value}
            for m in obj.metafields.all()
        ]

    @staticmethod
    def resolve_related_links(obj):
        from shopify_content.semantic_links.serialization import serialize_semantic_links
        return serialize_semantic_links(obj)

    @staticmethod
    def resolve_locale(obj):
        return str(obj.locale)

    @staticmethod
    def resolve_url(obj):
        try:
            return obj.get_full_url()
        except Exception:
            return None

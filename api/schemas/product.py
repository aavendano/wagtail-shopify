from typing import Any, Dict, List, Optional
from datetime import datetime
from ninja import Schema
from pydantic import Field

from .common import MetafieldSchema, LocaleCreateFields, LocalePatchFields, LocaleOutFields


class ProductIn(LocaleCreateFields):
    title: str = Field(
        ...,
        description=(
            "Product title as it appears in Shopify storefront and admin. "
            "E.g. 'Organic Cotton T-Shirt'. Required."
        ),
        max_length=255,
    )
    shopify_id: Optional[str] = Field(
        None,
        description=(
            "Shopify GID linking this Wagtail page to a Shopify product. "
            "Format: 'gid://shopify/Product/12345678'. "
            "Leave null when creating a Wagtail-only draft before it exists in Shopify. "
            "Must be set before calling /push."
        ),
    )
    handle: Optional[str] = Field(
        None,
        description=(
            "Shopify URL handle (slug) for this product. "
            "E.g. 'organic-cotton-t-shirt'. Used in storefront URLs: /products/{handle}. "
            "Auto-derived from title if omitted."
        ),
    )
    status: Optional[str] = Field(
        'ACTIVE',
        description=(
            "Shopify product status controlling storefront visibility. "
            "'ACTIVE' — live and purchasable (default); "
            "'DRAFT' — hidden from storefront, visible in admin; "
            "'ARCHIVED' — removed from storefront and collections."
        ),
    )
    vendor: Optional[str] = Field(
        None,
        description=(
            "Product vendor or brand name. Maps to Shopify product.vendor. "
            "E.g. 'Acme Co', 'Nike'. Appears on storefront product pages."
        ),
    )
    product_type: Optional[str] = Field(
        None,
        description=(
            "Shopify product type for filtering and organization. "
            "E.g. 'T-Shirts', 'Accessories', 'Footwear'. "
            "Maps to Shopify product.productType."
        ),
    )
    tags: Optional[List[str]] = Field(
        None,
        description=(
            "List of string tags for the product. Maps to Shopify product.tags. "
            "E.g. ['sale', 'new-arrival', 'cotton']. "
            "Used for filtering, automated collections, and storefront search."
        ),
    )
    body: Optional[List[Dict[str, Any]]] = Field(
        None,
        description=(
            "Product description as Wagtail StreamField block list. "
            "Each item is a dict with 'type' and 'value' keys. "
            "Common block types: 'html' (value: HTML string), 'paragraph' (value: rich text). "
            "Rendered to HTML and pushed to Shopify as descriptionHtml. "
            "Pass [] to clear the description. Omit to leave unchanged."
        ),
    )
    seo_title: Optional[str] = Field(
        None,
        description=(
            "SEO page title override. Maps to Shopify seo.title. "
            "Appears in browser tabs and search engine results. "
            "Recommended length: 50–60 characters. Falls back to product title if blank."
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
            "List of Shopify metafields to attach to this product. "
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


class ProductPatch(LocalePatchFields):
    title: Optional[str] = Field(
        None,
        description="Update the product title. Omit to leave unchanged.",
        max_length=255,
    )
    shopify_id: Optional[str] = Field(
        None,
        description=(
            "Set or update the Shopify GID. Format: 'gid://shopify/Product/12345678'. "
            "Required before using /push if not already set."
        ),
    )
    handle: Optional[str] = Field(
        None,
        description="Update the Shopify URL handle. Slug will be updated to match. Omit to leave unchanged.",
    )
    status: Optional[str] = Field(
        None,
        description=(
            "Update Shopify product status. "
            "'ACTIVE' — live; 'DRAFT' — hidden; 'ARCHIVED' — removed. "
            "Omit to leave unchanged."
        ),
    )
    vendor: Optional[str] = Field(None, description="Update the vendor/brand name. Omit to leave unchanged.")
    product_type: Optional[str] = Field(None, description="Update the product type. Omit to leave unchanged.")
    tags: Optional[List[str]] = Field(
        None,
        description=(
            "Replace the full tag list. Pass [] to clear all tags. Omit to leave unchanged. "
            "This is a full replacement, not an append."
        ),
    )
    body: Optional[List[Dict[str, Any]]] = Field(
        None,
        description=(
            "Replace the StreamField body blocks. Pass [] to clear. Omit to leave unchanged. "
            "Format: list of {'type': str, 'value': any} dicts."
        ),
    )
    seo_title: Optional[str] = Field(None, description="Update SEO title. Omit to leave unchanged.", max_length=255)
    search_description: Optional[str] = Field(
        None, description="Update SEO meta description. Omit to leave unchanged."
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


class ProductOut(LocaleOutFields):
    id: int = Field(..., description="Wagtail page ID. Use this as the page_id in all /products/{page_id}/ endpoints.")
    shopify_id: str = Field(
        ...,
        description="Shopify GID for this product. Format: 'gid://shopify/Product/12345678'. Empty string if not yet linked to Shopify.",
    )
    title: str = Field(..., description="Product title.")
    handle: str = Field(..., description="Shopify URL handle. Used in storefront URLs: /products/{handle}.")
    slug: str = Field(..., description="Wagtail page slug (mirrors handle).")
    status: str = Field(..., description="Shopify product status: ACTIVE, DRAFT, or ARCHIVED.")
    vendor: str = Field(..., description="Product vendor or brand name.")
    product_type: str = Field(..., description="Shopify product type.")
    tags: List[str] = Field(..., description="List of tag strings attached to this product.")
    body: List[Dict[str, Any]] = Field(
        ...,
        description=(
            "StreamField body blocks. Each item has 'type' and 'value' keys. "
            "Rendered to HTML and pushed to Shopify as descriptionHtml on sync."
        ),
    )
    seo_title: str = Field(..., description="SEO title. Maps to Shopify seo.title. Falls back to product title.")
    search_description: str = Field(..., description="SEO meta description. Maps to Shopify seo.description.")
    metafields: List[Dict[str, Any]] = Field(..., description="Attached Shopify metafields with namespace, key, type, and value.")
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
    def resolve_tags(obj):
        return list(obj.tags.values_list('name', flat=True))

    @staticmethod
    def resolve_body(obj):
        return list(obj.body.stream_data) if obj.body else []

    @staticmethod
    def resolve_metafields(obj):
        return [
            {"namespace": m.namespace, "key": m.key, "type": m.type, "value": m.value}
            for m in obj.metafields.all()
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

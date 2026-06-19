from typing import Any, Dict, List, Optional
from datetime import datetime
from ninja import Schema
from pydantic import Field

from .common import MetafieldSchema, LocaleCreateFields, LocalePatchFields, LocaleOutFields


class ArticleIn(LocaleCreateFields):
    title: str = Field(
        ...,
        description=(
            "Article title as it appears in Shopify storefront and admin. "
            "E.g. 'Top 10 Summer Trends'. Required."
        ),
        max_length=255,
    )
    blog_id: int = Field(
        ...,
        description=(
            "Wagtail page ID of the parent BlogPage. The article will be created as a child "
            "of this blog. Use GET /blogs/ to find available blogs and their IDs. "
            "The parent BlogPage must exist before creating articles under it. "
            "Required."
        ),
    )
    shopify_id: Optional[str] = Field(
        None,
        description=(
            "Shopify GID linking this Wagtail page to a Shopify Article. "
            "Format: 'gid://shopify/Article/12345678'. "
            "Leave null when creating a new article — Shopify will create it on first /push "
            "and the ID will be saved automatically. "
            "The parent BlogPage must have a shopify_id set before articles can be pushed."
        ),
    )
    handle: Optional[str] = Field(
        None,
        description=(
            "Shopify URL handle for this article. "
            "E.g. 'top-10-summer-trends'. "
            "Used in storefront URLs: /blogs/{blog_handle}/{handle}. "
            "Auto-derived from title if omitted."
        ),
    )
    author: Optional[str] = Field(
        None,
        description=(
            "Article author full name. Maps to Shopify AuthorInput.name. "
            "E.g. 'Jane Smith'. Displayed on the storefront article page."
        ),
        max_length=255,
    )
    published_at: Optional[datetime] = Field(
        None,
        description=(
            "ISO 8601 datetime when the article was or should be published. "
            "Maps to Shopify publishedAt. "
            "Auto-set to the current time on first publish if omitted."
        ),
    )
    summary: Optional[str] = Field(
        None,
        description=(
            "Short article summary (HTML allowed). Maps to Shopify article.summary. "
            "Typically shown in blog listing pages and cards."
        ),
    )
    tags: Optional[List[str]] = Field(
        None,
        description=(
            "List of string tags for the article. Maps to Shopify article.tags. "
            "E.g. ['fashion', 'summer', 'trends']. "
            "Used for filtering and cross-linking related articles."
        ),
    )
    featured_image_id: Optional[int] = Field(
        None,
        description=(
            "Wagtail Image ID for the article's featured image. "
            "Maps to Shopify Article image. "
            "Use the Wagtail Images API to upload an image and get its ID."
        ),
    )
    body: Optional[List[Dict[str, Any]]] = Field(
        None,
        description=(
            "Article body as Wagtail StreamField block list. "
            "Each item is a dict with 'type' and 'value' keys. "
            "Rendered to HTML and pushed to Shopify as the article body. "
            "Pass [] to clear the body. Omit to leave unchanged."
        ),
    )
    seo_title: Optional[str] = Field(
        None,
        description=(
            "SEO page title override. For articles, pushed as Shopify metafield global.title_tag "
            "(Shopify Articles have no native SEO field in Admin GraphQL API). "
            "Recommended length: 50–60 characters."
        ),
        max_length=255,
    )
    search_description: Optional[str] = Field(
        None,
        description=(
            "SEO meta description. For articles, pushed as Shopify metafield global.description_tag. "
            "Recommended length: 120–160 characters."
        ),
    )
    metafields: Optional[List[MetafieldSchema]] = Field(
        None,
        description=(
            "List of Shopify metafields to attach to this article. "
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


class ArticlePatch(LocalePatchFields):
    title: Optional[str] = Field(
        None,
        description="Update the article title. Omit to leave unchanged.",
        max_length=255,
    )
    shopify_id: Optional[str] = Field(
        None,
        description=(
            "Set or update the Shopify GID. Format: 'gid://shopify/Article/12345678'. "
            "Normally populated automatically after first push."
        ),
    )
    handle: Optional[str] = Field(
        None,
        description="Update the Shopify URL handle. Slug will be updated to match. Omit to leave unchanged.",
    )
    author: Optional[str] = Field(
        None,
        description="Update the author full name. Omit to leave unchanged.",
        max_length=255,
    )
    published_at: Optional[datetime] = Field(
        None,
        description="Update the published_at datetime (ISO 8601). Omit to leave unchanged.",
    )
    summary: Optional[str] = Field(
        None,
        description="Update the article summary. Omit to leave unchanged.",
    )
    tags: Optional[List[str]] = Field(
        None,
        description=(
            "Replace the full tag list. Pass [] to clear all tags. Omit to leave unchanged. "
            "This is a full replacement, not an append."
        ),
    )
    featured_image_id: Optional[int] = Field(
        None,
        description="Update the featured image by Wagtail Image ID. Omit to leave unchanged.",
    )
    body: Optional[List[Dict[str, Any]]] = Field(
        None,
        description=(
            "Replace the StreamField body blocks. Pass [] to clear. Omit to leave unchanged. "
            "Format: list of {'type': str, 'value': any} dicts."
        ),
    )
    seo_title: Optional[str] = Field(
        None,
        description="Update SEO title (pushed as metafield global.title_tag). Omit to leave unchanged.",
        max_length=255,
    )
    search_description: Optional[str] = Field(
        None,
        description="Update SEO meta description (pushed as metafield global.description_tag). Omit to leave unchanged.",
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
            "If sync_enabled=true, publishing triggers an outbound sync to Shopify. "
            "An article without a shopify_id will be created in Shopify on first publish "
            "(requires parent BlogPage to have a shopify_id). "
            "When false (default), changes are saved as a draft only."
        ),
    )


class ArticleOut(LocaleOutFields):
    id: int = Field(
        ...,
        description="Wagtail page ID. Use this as page_id in all /articles/{page_id}/ endpoints.",
    )
    shopify_id: str = Field(
        ...,
        description=(
            "Shopify GID for this article. "
            "Format: 'gid://shopify/Article/12345678'. "
            "Empty string if not yet pushed to Shopify."
        ),
    )
    title: str = Field(..., description="Article title.")
    handle: str = Field(..., description="Shopify URL handle. Used in storefront URLs: /blogs/{blog_handle}/{handle}.")
    slug: str = Field(..., description="Wagtail page slug (mirrors handle).")
    author: str = Field(..., description="Article author full name.")
    published_at: Optional[datetime] = Field(
        None,
        description="UTC datetime when the article was published. Null if not yet published.",
    )
    summary: str = Field(..., description="Short article summary (HTML allowed).")
    tags: List[str] = Field(..., description="List of tag strings attached to this article.")
    featured_image_id: Optional[int] = Field(
        None,
        description="Wagtail Image ID of the featured image. Null if no image is set.",
    )
    featured_image_url: str = Field(
        '',
        description="Absolute Shopify article image URL from pull.",
    )
    featured_image_alt: str = Field('', description="Alt text for the Shopify featured image URL.")
    body: List[Dict[str, Any]] = Field(
        ...,
        description=(
            "StreamField body blocks. Each item has 'type' and 'value' keys. "
            "Rendered to HTML and pushed to Shopify as the article body on sync."
        ),
    )
    seo_title: str = Field(
        ...,
        description="SEO title. Pushed as Shopify metafield global.title_tag on sync.",
    )
    search_description: str = Field(
        ...,
        description="SEO meta description. Pushed as Shopify metafield global.description_tag on sync.",
    )
    metafields: List[Dict[str, Any]] = Field(
        ...,
        description="Attached Shopify metafields with namespace, key, type, and value.",
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
    blog_id: Optional[int] = Field(
        None,
        description="Wagtail page ID of the parent BlogPage. Use GET /blogs/{blog_id} to retrieve blog details.",
    )
    blog_title: Optional[str] = Field(
        None,
        description="Title of the parent BlogPage.",
    )

    @staticmethod
    def resolve_translation_page_ids(obj):
        from ..locale_utils import resolve_translation_page_ids
        return resolve_translation_page_ids(obj)

    @staticmethod
    def resolve_tags(obj):
        return list(obj.tags.values_list('name', flat=True))

    @staticmethod
    def resolve_body(obj):
        return list(obj.body.raw_data) if obj.body else []

    @staticmethod
    def resolve_metafields(obj):
        return [
            {"namespace": m.namespace, "key": m.key, "type": m.type, "value": m.value}
            for m in obj.metafields.all()
        ]

    @staticmethod
    def resolve_featured_image_id(obj):
        return obj.featured_image_id

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
    def resolve_blog_id(obj):
        try:
            parent = obj.get_parent()
            return parent.pk if parent else None
        except Exception:
            return None

    @staticmethod
    def resolve_blog_title(obj):
        try:
            parent = obj.get_parent()
            return parent.title if parent else None
        except Exception:
            return None

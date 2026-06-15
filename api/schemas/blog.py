from typing import Optional
from datetime import datetime
from ninja import Schema
from pydantic import Field


COMMENT_POLICY_DESCRIPTION = (
    "Shopify Blog comment policy controlling visitor comment permissions. "
    "'AUTO_PUBLISHED' — comments appear immediately without moderation; "
    "'CLOSED' — comments disabled entirely (default); "
    "'MODERATED' — comments require staff approval before appearing."
)


class BlogIn(Schema):
    title: str = Field(
        ...,
        description=(
            "Blog title as it appears in Shopify admin and storefront. "
            "E.g. 'News & Updates', 'Style Guide'. Required."
        ),
        max_length=255,
    )
    shopify_id: Optional[str] = Field(
        None,
        description=(
            "Shopify GID linking this Wagtail page to a Shopify Blog. "
            "Format: 'gid://shopify/Blog/12345678'. "
            "Leave null when creating a new blog — Shopify will create it on first /push "
            "and the ID will be saved automatically."
        ),
    )
    handle: Optional[str] = Field(
        None,
        description=(
            "Shopify URL handle for this blog. "
            "E.g. 'news'. Used in storefront URLs: /blogs/{handle}. "
            "Auto-derived from title if omitted."
        ),
    )
    comment_policy: Optional[str] = Field(
        'CLOSED',
        description=COMMENT_POLICY_DESCRIPTION,
    )
    sync_enabled: Optional[bool] = Field(
        True,
        description=(
            "When true, publishing this page triggers an outbound sync to Shopify. "
            "Set to false to make Wagtail-only edits without pushing to Shopify."
        ),
    )


class BlogPatch(Schema):
    title: Optional[str] = Field(
        None,
        description="Update the blog title. Omit to leave unchanged.",
        max_length=255,
    )
    shopify_id: Optional[str] = Field(
        None,
        description=(
            "Set or update the Shopify GID. Format: 'gid://shopify/Blog/12345678'. "
            "Normally populated automatically after first push."
        ),
    )
    handle: Optional[str] = Field(
        None,
        description="Update the Shopify URL handle. Slug will be updated to match. Omit to leave unchanged.",
    )
    comment_policy: Optional[str] = Field(
        None,
        description=COMMENT_POLICY_DESCRIPTION + " Omit to leave unchanged.",
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
            "A Blog without a shopify_id will be created in Shopify on first publish. "
            "When false (default), changes are saved as a draft only."
        ),
    )


class BlogOut(Schema):
    id: int = Field(
        ...,
        description="Wagtail page ID. Use this as page_id in all /blogs/{page_id}/ endpoints.",
    )
    shopify_id: str = Field(
        ...,
        description=(
            "Shopify GID for this blog. "
            "Format: 'gid://shopify/Blog/12345678'. "
            "Empty string if not yet pushed to Shopify."
        ),
    )
    title: str = Field(..., description="Blog title.")
    handle: str = Field(..., description="Shopify URL handle. Used in storefront URLs: /blogs/{handle}.")
    slug: str = Field(..., description="Wagtail page slug (mirrors handle).")
    comment_policy: str = Field(
        ...,
        description="Comment policy: AUTO_PUBLISHED, CLOSED, or MODERATED.",
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
    article_count: int = Field(
        ...,
        description="Number of published ArticlePage children nested under this blog.",
    )

    @staticmethod
    def resolve_article_count(obj):
        return obj.get_children().live().count()

    @staticmethod
    def resolve_locale(obj):
        return str(obj.locale)

    @staticmethod
    def resolve_url(obj):
        try:
            return obj.get_full_url()
        except Exception:
            return None

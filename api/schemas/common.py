from typing import List, Optional
from ninja import Schema
from pydantic import Field

from ..locale_utils import LOCALE_FIELD_DESCRIPTION, TRANSLATION_OF_FIELD_DESCRIPTION


class LocaleCreateFields(Schema):
    locale: Optional[str] = Field(
        None,
        description=LOCALE_FIELD_DESCRIPTION,
    )
    translation_of: Optional[int] = Field(
        None,
        description=TRANSLATION_OF_FIELD_DESCRIPTION,
    )


class LocalePatchFields(Schema):
    locale: Optional[str] = Field(
        None,
        description=LOCALE_FIELD_DESCRIPTION + " Omit to leave unchanged.",
    )
    translation_of: Optional[int] = Field(
        None,
        description=TRANSLATION_OF_FIELD_DESCRIPTION + " Omit to leave unchanged.",
    )


class LocaleOutFields(Schema):
    translation_page_ids: List[int] = Field(
        ...,
        description=(
            "Wagtail page IDs of all locale variants in this translation group, "
            "including this page. Used to correlate market-specific variants."
        ),
    )


class MetafieldSchema(Schema):
    namespace: str = Field(
        default='custom',
        description=(
            "Shopify metafield namespace grouping. Standard namespaces: "
            "'custom' — store-specific data (default); "
            "'global' — SEO overrides (keys: title_tag, description_tag); "
            "'seo' — hreflang alternate locale URLs. "
            "Use your own prefix for app-owned data."
        ),
        max_length=255,
    )
    key: str = Field(
        ...,
        description="Metafield key within the namespace. E.g. 'ingredients', 'material', 'title_tag'.",
        max_length=64,
    )
    type: str = Field(
        default='single_line_text_field',
        description=(
            "Shopify metafield type controlling validation and display. "
            "'single_line_text_field' — plain text ≤255 chars; "
            "'multi_line_text_field' — long text; "
            "'json' — structured JSON (pass a JSON string as value); "
            "'url' — fully-qualified URL; "
            "'number_integer' — whole number as string; "
            "'number_decimal' — decimal as string; "
            "'boolean' — 'true' or 'false' as string; "
            "'date' — ISO 8601 date string; "
            "'date_time' — ISO 8601 datetime string."
        ),
    )
    value: str = Field(
        ...,
        description=(
            "Metafield value as a string. For 'json' type provide a valid JSON string. "
            "For 'boolean' use 'true' or 'false'. For numeric types use the string form of the number."
        ),
    )


class SyncResultSchema(Schema):
    success: bool = Field(..., description="True if the Shopify sync completed without errors.")
    message: str = Field(..., description="Outcome description. Contains error details when success=false.")
    shopify_id: Optional[str] = Field(
        None,
        description=(
            "Shopify GID of the synced resource, e.g. 'gid://shopify/Product/12345678'. "
            "Null if the resource was never linked to Shopify."
        ),
    )


class ImportResultSchema(Schema):
    created: int = Field(..., description="New Wagtail pages created from Shopify data.")
    updated: int = Field(..., description="Existing Wagtail pages updated from Shopify data.")
    skipped: int = Field(0, description="Existing pages skipped when new_only import is used.")
    errors: int = Field(..., description="Resources that failed to import. Check server logs for details.")
    message: str = Field(..., description="Summary of the import operation.")


class ErrorSchema(Schema):
    detail: str = Field(..., description="Human-readable error message describing what went wrong.")

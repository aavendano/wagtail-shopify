from typing import List, Literal, Optional

from ninja import Schema
from pydantic import Field

from shopify_content.semantic_links.service import (
    SUGGEST_LIMIT_PER_TYPE_DEFAULT,
    SUGGEST_LIMIT_PER_TYPE_MAX,
)

from ..locale_utils import LOCALE_FIELD_DESCRIPTION

PageType = Literal['product', 'collection', 'article', 'glossary']


class SuggestRelatedIn(Schema):
    locale: str = Field(..., description=LOCALE_FIELD_DESCRIPTION)
    page_id: Optional[int] = Field(
        None,
        description=(
            "Existing Wagtail page ID. Query text is extracted like refresh_semantic_links. "
            "Do not combine with text or structured fields."
        ),
    )
    page_type: Optional[PageType] = Field(
        None,
        description=(
            "Origin page type. Required when using text/fields (chooses which fields "
            "are concatenated). Inferred from page_id when omitted."
        ),
    )
    text: Optional[str] = Field(
        None,
        description="Free-text query for a page that does not exist yet.",
    )
    title: Optional[str] = Field(None, description="Title / heading used in the query text.")
    seo_title: Optional[str] = Field(None, description="SEO title used in the query text.")
    search_description: Optional[str] = Field(
        None,
        description="SEO meta description used in the query text.",
    )
    definition: Optional[str] = Field(None, description="Glossary definition HTML/text.")
    summary: Optional[str] = Field(None, description="Article summary used in the query text.")
    body: Optional[str] = Field(None, description="Product/article body used in the query text.")
    description: Optional[str] = Field(
        None,
        description="Collection description used in the query text.",
    )
    synonyms: Optional[List[str]] = Field(
        None,
        description="Glossary synonyms used in the query text.",
    )
    vendor: Optional[str] = Field(None, description="Product vendor used in the query text.")
    product_type: Optional[str] = Field(
        None,
        description="Shopify product type used in the query text.",
    )
    author: Optional[str] = Field(None, description="Article author used in the query text.")
    types: Optional[List[PageType]] = Field(
        None,
        description="Candidate types to search. Defaults to all four linkable types.",
    )
    exclude_page_id: Optional[int] = Field(
        None,
        description="Extra page ID to exclude (page_id is always excluded when set).",
    )
    limit_per_type: int = Field(
        SUGGEST_LIMIT_PER_TYPE_DEFAULT,
        ge=1,
        le=SUGGEST_LIMIT_PER_TYPE_MAX,
        description=(
            "Max candidates per type for this preview (default 20, max 100). "
            "Independent of SEMANTIC_LINKS_LIMIT_PER_TYPE used on publish."
        ),
    )


class SuggestRelatedCandidateOut(Schema):
    id: int = Field(..., description="Wagtail page ID of the candidate.")
    type: PageType = Field(..., description="Linkable page type of the candidate.")
    title: str = Field(..., description="Display title (glossary term when applicable).")
    handle: str = Field(..., description="Shopify/Wagtail handle or slug.")
    score: float = Field(
        ...,
        description="Cosine similarity (1 - distance) from pgvector; higher is closer.",
    )


class SuggestRelatedCandidatesOut(Schema):
    product: List[SuggestRelatedCandidateOut] = Field(default_factory=list)
    collection: List[SuggestRelatedCandidateOut] = Field(default_factory=list)
    article: List[SuggestRelatedCandidateOut] = Field(default_factory=list)
    glossary: List[SuggestRelatedCandidateOut] = Field(default_factory=list)


class SuggestRelatedOut(Schema):
    locale: str = Field(..., description="Wagtail locale used to filter candidates.")
    page_type: PageType = Field(..., description="Origin page type used to assemble query text.")
    limit_per_type: int = Field(..., description="Per-type cap applied to this preview.")
    candidates: SuggestRelatedCandidatesOut = Field(
        ...,
        description="Neighbors grouped by type, each ordered by score descending.",
    )

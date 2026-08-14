"""Typed HomePage section payloads for the agent-facing OpenAPI schema.

All write fields are optional so PATCH can send one section. The API normalizer
fills required keys, stable ids, and the canonical 13-section envelope.
"""

from typing import List, Literal, Optional

from ninja import Schema
from pydantic import Field

from .common import ContentReferenceSchema

RENDER_REQUIRED = 'Required for this section to render; omitted keys keep the stored value or the API default.'

Alignment = Literal['left', 'center']
MediaPosition = Literal['left', 'right']
Background = Literal['default', 'contrast']
MediaSource = Literal['collection_products', 'collection_list']
ColumnSpan = Literal['1', '2']
MarketCode = Literal['US', 'CA']
TrustIcon = Literal[
    'local_shipping',
    'verified',
    'lock',
    'favorite',
    'shield',
    'support_agent',
]


class TrustBarItemSchema(Schema):
    icon: Optional[TrustIcon] = Field(None, description='Material icon key.')
    title: Optional[str] = Field(None, max_length=80, description=RENDER_REQUIRED)
    description: Optional[str] = Field(None, max_length=200)


class TrustBarValueSchema(Schema):
    items: Optional[List[TrustBarItemSchema]] = Field(
        None,
        description='Trust chips. Schema min 2 / max 6 when the section is populated.',
    )


class FeaturedCollectionsValueSchema(Schema):
    badge: Optional[str] = Field(None, max_length=40)
    title: Optional[str] = Field(None, max_length=120, description=RENDER_REQUIRED)
    intro: Optional[str] = Field(None, max_length=300)
    items: Optional[List[ContentReferenceSchema]] = Field(
        None,
        description='CollectionPage references (page_id required per item). Max 6.',
    )


class NavCollectionPillItemSchema(Schema):
    page_id: int = Field(..., description='CollectionPage Wagtail ID.')
    override_label: Optional[str] = Field(None, max_length=80)


class NavCollectionPillsValueSchema(Schema):
    source_collection_page_id: Optional[int] = Field(
        None,
        description='Optional CollectionPage used to seed pills when items is empty.',
    )
    items: Optional[List[NavCollectionPillItemSchema]] = Field(None, description='Max 8 pills.')


class EditorialIntroValueSchema(Schema):
    heading: Optional[str] = Field(None, max_length=120, description=RENDER_REQUIRED)
    body: Optional[str] = Field(None, description=f'HTML rich text. {RENDER_REQUIRED}')
    alignment: Optional[Alignment] = Field(None, description='Default: left.')


class BestSellersValueSchema(Schema):
    title: Optional[str] = Field(None, max_length=120, description=RENDER_REQUIRED)
    collection_page_id: Optional[int] = Field(
        None,
        description='CollectionPage Wagtail ID. Required for the carousel to render products.',
    )
    product_limit: Optional[int] = Field(None, description='Default 8. Clamped to 4–12.')
    badge: Optional[str] = Field(None, max_length=20)
    background: Optional[Background] = Field(None, description='Default: contrast.')


class ShopByNeedCardSchema(Schema):
    title: Optional[str] = Field(None, max_length=80, description=RENDER_REQUIRED)
    description: Optional[str] = Field(None, max_length=160)
    target_page_id: Optional[int] = Field(None, description='CollectionPage or ProductPage ID.')
    cta_label: Optional[str] = Field(None, max_length=40, description="Default: 'Shop'.")
    cta_url: Optional[str] = Field(None, description='Used when target_page_id is omitted.')
    image_url: Optional[str] = None
    intent_tag: Optional[str] = Field(None, max_length=40)


class ShopByNeedValueSchema(Schema):
    title: Optional[str] = Field(None, max_length=120)
    cards: Optional[List[ShopByNeedCardSchema]] = Field(
        None,
        description='Intent cards. Schema min 4 / max 8 when populated.',
    )


class EducationalHubValueSchema(Schema):
    title: Optional[str] = Field(None, max_length=120, description=RENDER_REQUIRED)
    intro: Optional[str] = Field(None, max_length=300)
    links: Optional[List[ContentReferenceSchema]] = Field(
        None,
        description='page_id required per link. Min 3 / max 6 when populated.',
    )


class BrandValueItemSchema(Schema):
    icon: Optional[str] = Field(None, max_length=40)
    title: Optional[str] = Field(None, max_length=80, description=RENDER_REQUIRED)
    description: Optional[str] = Field(None, max_length=200)


class BrandValuesValueSchema(Schema):
    eyebrow: Optional[str] = Field(None, max_length=60)
    heading: Optional[str] = Field(None, max_length=120, description=RENDER_REQUIRED)
    body: Optional[str] = Field(None, description='HTML rich text.')
    image_url: Optional[str] = None
    media_position: Optional[MediaPosition] = Field(None, description='Default: left.')
    values: Optional[List[BrandValueItemSchema]] = Field(None, description='Max 4 value chips.')
    cta_label: Optional[str] = Field(None, max_length=80)
    cta_url: Optional[str] = None


class MarketBlockValueSchema(Schema):
    heading: Optional[str] = Field(None, max_length=120, description=RENDER_REQUIRED)
    body: Optional[str] = Field(None, description=f'HTML rich text. {RENDER_REQUIRED}')
    highlights: Optional[List[str]] = Field(None, description='Max 4 short strings.')
    cta_label: Optional[str] = Field(None, max_length=80)
    cta_url: Optional[str] = None
    market_code: Optional[MarketCode] = Field(None, description='US or CA.')


class HomeFaqItemSchema(Schema):
    question: Optional[str] = Field(None, max_length=500, description=RENDER_REQUIRED)
    answer: Optional[str] = Field(None, description=f'HTML rich text. {RENDER_REQUIRED}')


class FaqValueSchema(Schema):
    heading: Optional[str] = Field(
        None,
        max_length=120,
        description="Default: 'Frequently asked questions'.",
    )
    items: Optional[List[HomeFaqItemSchema]] = Field(
        None,
        description='Q&A pairs. Schema min 4 / max 6 when populated.',
    )


class InternalLinkItemSchema(Schema):
    page_id: int = Field(..., description='Wagtail page ID.')
    label: Optional[str] = Field(None, max_length=80)


class InternalLinkGroupSchema(Schema):
    title: Optional[str] = Field(None, max_length=80, description=RENDER_REQUIRED)
    links: Optional[List[InternalLinkItemSchema]] = Field(
        None,
        description='page_id required per link. Min 3 / max 12 when populated.',
    )


class InternalLinksValueSchema(Schema):
    heading: Optional[str] = Field(None, max_length=120)
    groups: Optional[List[InternalLinkGroupSchema]] = Field(
        None,
        description='Min 2 / max 6 groups when populated.',
    )


class PromoGatewayCardSchema(Schema):
    title: Optional[str] = Field(None, max_length=120, description=RENDER_REQUIRED)
    badge: Optional[str] = Field(None, max_length=80)
    media_source: Optional[MediaSource] = Field(
        None,
        description='Default: collection_products.',
    )
    primary_collection_page_id: Optional[int] = None
    category_page_ids: Optional[List[int]] = Field(None, description='Max 4 CollectionPage IDs.')
    cta_label: Optional[str] = Field(None, max_length=80, description="Default: 'Shop trending'.")
    cta_url: Optional[str] = None
    column_span: Optional[ColumnSpan] = Field(None, description="Default: '1'.")


class PromoGatewayValueSchema(Schema):
    cards: Optional[List[PromoGatewayCardSchema]] = Field(
        None,
        description='Exactly 4 cards when the section is populated.',
    )


class SeoSchemaValueSchema(Schema):
    include_faq_schema: Optional[bool] = Field(None, description='Default: true.')
    include_organization: Optional[bool] = Field(None, description='Default: true.')


class HomeSectionFields(Schema):
    """First-class section fields for agent PATCH/POST. Omitted keys are left unchanged."""

    promo_gateway: Optional[PromoGatewayValueSchema] = Field(
        None,
        description='Promo mosaic (4 cards). Merged by type into sections_json.',
    )
    nav_collection_pills: Optional[NavCollectionPillsValueSchema] = Field(
        None,
        description='Header collection pills. Merged by type into sections_json.',
    )
    trust_bar: Optional[TrustBarValueSchema] = None
    featured_collections: Optional[FeaturedCollectionsValueSchema] = None
    editorial_intro: Optional[EditorialIntroValueSchema] = None
    best_sellers: Optional[BestSellersValueSchema] = None
    shop_by_need: Optional[ShopByNeedValueSchema] = None
    educational_hub: Optional[EducationalHubValueSchema] = None
    brand_values: Optional[BrandValuesValueSchema] = None
    market_block: Optional[MarketBlockValueSchema] = None
    faq: Optional[FaqValueSchema] = None
    internal_links: Optional[InternalLinksValueSchema] = None
    seo_schema: Optional[SeoSchemaValueSchema] = None

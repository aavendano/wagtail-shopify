from wagtail.blocks import (
    StructBlock, CharBlock, TextBlock, ChoiceBlock, RichTextBlock,
    ListBlock, URLBlock, IntegerBlock, PageChooserBlock, BooleanBlock,
)
from wagtail.images.blocks import ImageChooserBlock


LINKABLE_PAGE_TYPES = [
    'shopify_content.ProductPage',
    'shopify_content.CollectionPage',
    'shopify_content.ArticlePage',
    'shopify_content.GlossaryTermPage',
    'shopify_content.BlogPage',
]

# URLBlock rejects storefront-relative paths like /collections/all.
STOREFRONT_CTA_URL_HELP = (
    'Storefront path (e.g. /collections/all) or absolute https URL.'
)


def _storefront_cta_url_block(**kwargs):
    return CharBlock(
        required=False,
        max_length=500,
        help_text=STOREFRONT_CTA_URL_HELP,
        **kwargs,
    )


class TrustBarItemBlock(StructBlock):
    icon = ChoiceBlock(
        choices=[
            ('local_shipping', 'Shipping'),
            ('verified', 'Verified'),
            ('lock', 'Secure'),
            ('favorite', 'Inclusive'),
            ('shield', 'Shield'),
            ('support_agent', 'Support'),
        ],
        required=False,
    )
    title = CharBlock(max_length=80, required=True)
    description = CharBlock(max_length=200, required=False)

    class Meta:
        icon = 'tick'
        label = 'Trust item'


class TrustBarBlock(StructBlock):
    items = ListBlock(TrustBarItemBlock(), min_num=0, max_num=6)

    class Meta:
        icon = 'list-ul'
        label = 'Trust bar'


class FeaturedCollectionItemBlock(StructBlock):
    collection = PageChooserBlock(
        required=True,
        page_type=['shopify_content.CollectionPage'],
    )
    override_title = CharBlock(max_length=120, required=False)
    override_label = CharBlock(max_length=80, required=False)

    class Meta:
        icon = 'folder'
        label = 'Collection'


class FeaturedCollectionsBlock(StructBlock):
    badge = CharBlock(max_length=40, required=False)
    title = CharBlock(max_length=120, required=False)
    intro = CharBlock(max_length=300, required=False)
    items = ListBlock(FeaturedCollectionItemBlock(), min_num=0, max_num=6)

    class Meta:
        icon = 'folder-open-1'
        label = 'Featured collections'


class NavCollectionPillItemBlock(StructBlock):
    collection = PageChooserBlock(
        required=True,
        page_type=['shopify_content.CollectionPage'],
    )
    override_label = CharBlock(max_length=80, required=False)

    class Meta:
        icon = 'tag'
        label = 'Nav pill'


class NavCollectionPillsBlock(StructBlock):
    """Header quick-link pills; not rendered as a home section."""

    source_collection = PageChooserBlock(
        required=False,
        page_type=['shopify_content.CollectionPage'],
        help_text='If items are empty, seed pills from this collection’s related_collections.',
    )
    items = ListBlock(NavCollectionPillItemBlock(), required=False, max_num=8)

    class Meta:
        icon = 'list-ul'
        label = 'Nav collection pills'


class EditorialIntroBlock(StructBlock):
    heading = CharBlock(max_length=120, required=False)
    body = RichTextBlock(
        features=['bold', 'italic', 'link', 'ol', 'ul'],
        required=False,
    )
    alignment = ChoiceBlock(
        choices=[('left', 'Left'), ('center', 'Center')],
        default='left',
        required=False,
    )

    class Meta:
        icon = 'pilcrow'
        label = 'Editorial intro'


class BestSellersBlock(StructBlock):
    title = CharBlock(max_length=120, required=False)
    collection = PageChooserBlock(
        required=False,
        page_type=['shopify_content.CollectionPage'],
    )
    product_limit = IntegerBlock(default=8, min_value=4, max_value=12, required=False)
    badge = CharBlock(max_length=20, required=False)
    background = ChoiceBlock(
        choices=[('default', 'Default'), ('contrast', 'Contrast')],
        default='contrast',
        required=False,
    )

    class Meta:
        icon = 'snippet'
        label = 'Best sellers'


class ShopByNeedCardBlock(StructBlock):
    title = CharBlock(max_length=80, required=True)
    description = CharBlock(max_length=160, required=False)
    target_page = PageChooserBlock(
        required=False,
        page_type=['shopify_content.CollectionPage', 'shopify_content.ProductPage'],
    )
    cta_label = CharBlock(max_length=40, required=False, default='Shop')
    cta_url = _storefront_cta_url_block()
    image_url = URLBlock(required=False)
    intent_tag = CharBlock(max_length=40, required=False)

    class Meta:
        icon = 'pick'
        label = 'Intent card'


class ShopByNeedBlock(StructBlock):
    title = CharBlock(max_length=120, required=False)
    cards = ListBlock(ShopByNeedCardBlock(), min_num=0, max_num=8)

    class Meta:
        icon = 'grip'
        label = 'Shop by need'


class EducationalHubLinkBlock(StructBlock):
    page = PageChooserBlock(required=True, page_type=LINKABLE_PAGE_TYPES)
    label = CharBlock(max_length=100, required=False)
    description = CharBlock(max_length=160, required=False)

    class Meta:
        icon = 'link'
        label = 'Link'


class EducationalHubBlock(StructBlock):
    title = CharBlock(max_length=120, required=False)
    intro = CharBlock(max_length=300, required=False)
    links = ListBlock(EducationalHubLinkBlock(), min_num=0, max_num=6)

    class Meta:
        icon = 'book'
        label = 'Educational hub'


class BrandValueItemBlock(StructBlock):
    icon = CharBlock(max_length=40, required=False)
    title = CharBlock(max_length=80, required=True)
    description = CharBlock(max_length=200, required=False)

    class Meta:
        icon = 'tick'
        label = 'Value'


class BrandValuesBlock(StructBlock):
    eyebrow = CharBlock(max_length=60, required=False)
    heading = CharBlock(max_length=120, required=False)
    body = RichTextBlock(features=['bold', 'italic', 'link'], required=False)
    image = ImageChooserBlock(required=False)
    image_url = URLBlock(required=False)
    media_position = ChoiceBlock(
        choices=[('left', 'Left'), ('right', 'Right')],
        default='left',
        required=False,
    )
    values = ListBlock(BrandValueItemBlock(), max_num=4, required=False)
    cta_label = CharBlock(max_length=80, required=False)
    cta_url = _storefront_cta_url_block()

    class Meta:
        icon = 'group'
        label = 'Brand values'


class MarketBlock(StructBlock):
    heading = CharBlock(max_length=120, required=False)
    body = RichTextBlock(features=['bold', 'italic', 'link'], required=False)
    highlights = ListBlock(CharBlock(max_length=120), max_num=4, required=False)
    cta_label = CharBlock(max_length=80, required=False)
    cta_url = _storefront_cta_url_block()
    market_code = ChoiceBlock(
        choices=[('US', 'United States'), ('CA', 'Canada')],
        required=False,
    )

    class Meta:
        icon = 'site'
        label = 'Market block'


class FAQItemBlock(StructBlock):
    question = CharBlock(max_length=500, required=True)
    answer = RichTextBlock(features=['bold', 'italic', 'link'], required=True)

    class Meta:
        icon = 'help'
        label = 'FAQ'


class FAQBlock(StructBlock):
    heading = CharBlock(
        max_length=120,
        required=False,
        default='Frequently asked questions',
    )
    items = ListBlock(FAQItemBlock(), min_num=0, max_num=6)

    class Meta:
        icon = 'help'
        label = 'FAQ'


class InternalLinkItemBlock(StructBlock):
    page = PageChooserBlock(required=True, page_type=LINKABLE_PAGE_TYPES)
    label = CharBlock(max_length=80, required=False)

    class Meta:
        icon = 'link'
        label = 'Link'


class InternalLinkGroupBlock(StructBlock):
    title = CharBlock(max_length=80, required=False)
    links = ListBlock(InternalLinkItemBlock(), min_num=0, max_num=12)

    class Meta:
        icon = 'list-ul'
        label = 'Link group'


class InternalLinksBlock(StructBlock):
    heading = CharBlock(max_length=120, required=False)
    groups = ListBlock(InternalLinkGroupBlock(), min_num=0, max_num=6)

    class Meta:
        icon = 'link-external'
        label = 'Internal links'


class PromoGatewayCardBlock(StructBlock):
    title = CharBlock(max_length=120, required=True)
    badge = CharBlock(max_length=80, required=False)
    media_source = ChoiceBlock(
        choices=[
            ('collection_products', 'Collection products'),
            ('collection_list', 'Collection list'),
        ],
        default='collection_products',
        required=False,
    )
    primary_collection = PageChooserBlock(
        required=False,
        page_type=['shopify_content.CollectionPage'],
    )
    # required=False: cards with media_source=collection_products omit
    # categories; Wagtail also POSTs empty chooser slots that must not fail.
    category_collections = ListBlock(
        PageChooserBlock(
            required=False,
            page_type=['shopify_content.CollectionPage'],
        ),
        min_num=0,
        max_num=4,
        required=False,
    )
    cta_label = CharBlock(max_length=80, required=False, default='Shop trending')
    cta_url = _storefront_cta_url_block()
    column_span = ChoiceBlock(
        choices=[('1', '1 column'), ('2', '2 columns')],
        default='1',
        required=False,
    )

    class Meta:
        icon = 'pick'
        label = 'Promo card'


class PromoGatewayBlock(StructBlock):
    cards = ListBlock(PromoGatewayCardBlock(), min_num=0, max_num=4)

    class Meta:
        icon = 'grip'
        label = 'Promo gateway'


class SEOSchemaBlock(StructBlock):
    include_faq_schema = BooleanBlock(default=True, required=False)
    include_organization = BooleanBlock(default=True, required=False)

    class Meta:
        icon = 'code'
        label = 'SEO schema flags'

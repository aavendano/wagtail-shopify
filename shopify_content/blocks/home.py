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
    items = ListBlock(TrustBarItemBlock(), min_num=2, max_num=6)

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
    title = CharBlock(max_length=120, required=True)
    intro = CharBlock(max_length=300, required=False)
    items = ListBlock(FeaturedCollectionItemBlock(), min_num=1, max_num=6)

    class Meta:
        icon = 'folder-open-1'
        label = 'Featured collections'


class EditorialIntroBlock(StructBlock):
    heading = CharBlock(max_length=120, required=True)
    body = RichTextBlock(
        features=['bold', 'italic', 'link', 'ol', 'ul'],
        required=True,
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
    title = CharBlock(max_length=120, required=True)
    collection = PageChooserBlock(
        required=True,
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
    cta_url = URLBlock(required=False)
    image_url = URLBlock(required=False)
    intent_tag = CharBlock(max_length=40, required=False)

    class Meta:
        icon = 'pick'
        label = 'Intent card'


class ShopByNeedBlock(StructBlock):
    title = CharBlock(max_length=120, required=False)
    cards = ListBlock(ShopByNeedCardBlock(), min_num=4, max_num=8)

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
    title = CharBlock(max_length=120, required=True)
    intro = CharBlock(max_length=300, required=False)
    links = ListBlock(EducationalHubLinkBlock(), min_num=3, max_num=6)

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
    heading = CharBlock(max_length=120, required=True)
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
    cta_url = URLBlock(required=False)

    class Meta:
        icon = 'group'
        label = 'Brand values'


class MarketBlock(StructBlock):
    heading = CharBlock(max_length=120, required=True)
    body = RichTextBlock(features=['bold', 'italic', 'link'], required=True)
    highlights = ListBlock(CharBlock(max_length=120), max_num=4, required=False)
    cta_label = CharBlock(max_length=80, required=False)
    cta_url = URLBlock(required=False)
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
    items = ListBlock(FAQItemBlock(), min_num=4, max_num=6)

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
    title = CharBlock(max_length=80, required=True)
    links = ListBlock(InternalLinkItemBlock(), min_num=3, max_num=12)

    class Meta:
        icon = 'list-ul'
        label = 'Link group'


class InternalLinksBlock(StructBlock):
    heading = CharBlock(max_length=120, required=False)
    groups = ListBlock(InternalLinkGroupBlock(), min_num=2, max_num=6)

    class Meta:
        icon = 'link-external'
        label = 'Internal links'


class SEOSchemaBlock(StructBlock):
    include_faq_schema = BooleanBlock(default=True, required=False)
    include_organization = BooleanBlock(default=True, required=False)

    class Meta:
        icon = 'code'
        label = 'SEO schema flags'

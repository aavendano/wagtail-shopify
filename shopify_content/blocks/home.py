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


class LocaleAwarePageChooserBlock(PageChooserBlock):
    """
    PageChooserBlock that filters GlossaryTermPage by the current page's locale.
    Used for GlossaryTermPage to ensure locale consistency in HomePage sections.
    """

    def get_queryset(self, request, model_admin, **kwargs):
        qs = super().get_queryset(request, model_admin, **kwargs)

        page_locale = getattr(request, 'homepage_locale', None)

        if not page_locale and hasattr(request, 'session'):
            page_locale = request.session.get('homepage_locale')

        if not page_locale:
            if hasattr(self, 'bound_field') and hasattr(self.bound_field, 'form'):
                form = self.bound_field.form
                if hasattr(form, 'instance') and form.instance and hasattr(form.instance, 'locale'):
                    page_locale = form.instance.locale.language_code

        if not page_locale:
            page = kwargs.get('page')
            if not page and hasattr(self, 'page'):
                page = self.page
            if page and hasattr(page, 'locale') and page.locale:
                page_locale = page.locale.language_code

        if page_locale:
            from django.contrib.contenttypes.models import ContentType
            from wagtail.models import Locale

            from shopify_content.models.glossary import GlossaryTermPage
            from shopify_content.page_chooser_locale import glossary_term_page_filter_q

            target_models = self.page_type or []
            if 'shopify_content.GlossaryTermPage' in target_models:
                try:
                    editor_locale = Locale.objects.get(language_code=page_locale)
                except Locale.DoesNotExist:
                    return qs

                glossary_ct = ContentType.objects.get_for_model(GlossaryTermPage)
                qs = qs.filter(glossary_term_page_filter_q(editor_locale, glossary_ct))

        return qs


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
    page = LocaleAwarePageChooserBlock(required=True, page_type=LINKABLE_PAGE_TYPES)
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
    page = LocaleAwarePageChooserBlock(required=True, page_type=LINKABLE_PAGE_TYPES)
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

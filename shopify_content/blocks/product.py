from wagtail.blocks import StructBlock, CharBlock, TextBlock
from wagtail.images.blocks import ImageChooserBlock


class ProductFeatureBlock(StructBlock):
    """
    Product feature item (icon + title + description).
    Used in product body to showcase key selling points.
    Renders as a definition-list or flex row in Shopify HTML.
    """
    icon = ImageChooserBlock(
        required=False,
        help_text='Optional SVG or PNG icon for this feature.',
    )
    title = CharBlock(max_length=100, required=True)
    description = TextBlock(required=True)

    class Meta:
        icon = 'list-ul'
        label = 'Product Feature'
        template = 'shopify_content/blocks/product_feature_block.html'

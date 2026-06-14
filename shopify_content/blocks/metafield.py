from wagtail.blocks import StructBlock, CharBlock, TextBlock, ChoiceBlock


SHOPIFY_METAFIELD_TYPES = [
    ('single_line_text_field', 'Single Line Text'),
    ('multi_line_text_field', 'Multi Line Text'),
    ('json', 'JSON'),
    ('number_integer', 'Integer'),
    ('number_decimal', 'Decimal'),
    ('boolean', 'Boolean'),
    ('color', 'Color'),
    ('date', 'Date'),
    ('date_time', 'Date & Time'),
    ('url', 'URL'),
    ('rich_text_field', 'Rich Text (HTML)'),
    ('file_reference', 'File Reference'),
    ('page_reference', 'Page Reference'),
    ('product_reference', 'Product Reference'),
    ('collection_reference', 'Collection Reference'),
    ('variant_reference', 'Variant Reference'),
    ('metaobject_reference', 'Metaobject Reference'),
]


class MetafieldBlock(StructBlock):
    """
    Inline metafield block for one-off metafields within a StreamField body.
    For structured metafield management, prefer the InlinePanel on each page
    (ProductPageMetafield, ArticlePageMetafield, etc.) which provides a
    cleaner editing UX and reliable ordering.
    """
    namespace = CharBlock(default='custom', required=True, max_length=255)
    key = CharBlock(required=True, max_length=64)
    type = ChoiceBlock(
        choices=SHOPIFY_METAFIELD_TYPES,
        default='single_line_text_field',
    )
    value = TextBlock(required=True)

    class Meta:
        icon = 'tag'
        label = 'Metafield'
        help_text = 'Prefer the Metafields panel below the editor for bulk metafield management.'

from wagtail.blocks import (
    StructBlock, CharBlock, ChoiceBlock, RichTextBlock, RawHTMLBlock,
)


class HeadingBlock(StructBlock):
    """Section heading. Renders as <h2>/<h3>/<h4> in Shopify HTML output."""
    text = CharBlock(required=True, max_length=255)
    level = ChoiceBlock(
        choices=[('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4')],
        default='h2',
    )

    class Meta:
        icon = 'title'
        label = 'Heading'
        template = 'shopify_content/blocks/heading_block.html'


class ParagraphBlock(StructBlock):
    """Rich-text paragraph. Features limited to HTML compatible with Shopify."""
    text = RichTextBlock(
        features=['bold', 'italic', 'link', 'ol', 'ul', 'hr'],
        required=True,
    )

    class Meta:
        icon = 'pilcrow'
        label = 'Paragraph'
        template = 'shopify_content/blocks/paragraph_block.html'


class HtmlBlock(RawHTMLBlock):
    """
    Raw HTML passthrough. Used for:
    - Inbound import: stores Shopify's existing HTML verbatim
    - Outbound sync: value sent to Shopify as-is
    """
    class Meta:
        icon = 'code'
        label = 'Raw HTML'
        help_text = 'Raw HTML sent to Shopify verbatim. Use for complex layouts.'


class CalloutBlock(StructBlock):
    """Highlighted callout box. Renders as a styled <div> in Shopify HTML."""
    callout_type = ChoiceBlock(
        choices=[
            ('info', 'Info'),
            ('warning', 'Warning'),
            ('tip', 'Tip'),
            ('note', 'Note'),
        ],
        default='info',
    )
    text = RichTextBlock(
        features=['bold', 'italic', 'link'],
        required=True,
    )

    class Meta:
        icon = 'warning'
        label = 'Callout'
        template = 'shopify_content/blocks/callout_block.html'

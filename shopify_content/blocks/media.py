from wagtail.blocks import StructBlock, CharBlock, URLBlock
from wagtail.images.blocks import ImageChooserBlock


class ImageBlock(StructBlock):
    """
    Embedded image block. On outbound sync, the Wagtail image URL is
    passed to Shopify as a media reference or embedded in HTML.
    """
    image = ImageChooserBlock(required=True)
    alt_text = CharBlock(
        max_length=255,
        required=False,
        help_text='Alt text overrides the image title for accessibility.',
    )
    caption = CharBlock(max_length=255, required=False)

    class Meta:
        icon = 'image'
        label = 'Image'
        template = 'shopify_content/blocks/image_block.html'


class VideoEmbedBlock(StructBlock):
    """YouTube or Vimeo embed. Rendered as an <iframe> in Shopify HTML."""
    url = URLBlock(
        required=True,
        help_text='YouTube or Vimeo video URL.',
    )
    caption = CharBlock(max_length=255, required=False)

    class Meta:
        icon = 'media'
        label = 'Video Embed'
        template = 'shopify_content/blocks/video_embed_block.html'

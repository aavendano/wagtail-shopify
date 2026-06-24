from wagtail.blocks import StreamBlock

from .content import HeadingBlock, ParagraphBlock, HtmlBlock, CalloutBlock, ProductBannerBlock
from .media import ImageBlock, VideoEmbedBlock
from .product import ProductFeatureBlock
from .metafield import MetafieldBlock


class ProductBodyStreamBlock(StreamBlock):
    heading = HeadingBlock()
    paragraph = ParagraphBlock()
    image = ImageBlock()
    video = VideoEmbedBlock()
    feature = ProductFeatureBlock()
    callout = CalloutBlock()
    html = HtmlBlock()
    metafield = MetafieldBlock()

    class Meta:
        label = 'Product Body'


class CollectionBodyStreamBlock(StreamBlock):
    heading = HeadingBlock()
    paragraph = ParagraphBlock()
    image = ImageBlock()
    callout = CalloutBlock()
    html = HtmlBlock()

    class Meta:
        label = 'Collection Description'


class ArticleBodyStreamBlock(StreamBlock):
    heading = HeadingBlock()
    paragraph = ParagraphBlock()
    image = ImageBlock()
    video = VideoEmbedBlock()
    callout = CalloutBlock()
    html = HtmlBlock()
    product_banner = ProductBannerBlock()

    class Meta:
        label = 'Article Body'


PRODUCT_BODY_BLOCKS = ProductBodyStreamBlock()
COLLECTION_BODY_BLOCKS = CollectionBodyStreamBlock()
ARTICLE_BODY_BLOCKS = ArticleBodyStreamBlock()

__all__ = [
    'HeadingBlock',
    'ParagraphBlock',
    'HtmlBlock',
    'CalloutBlock',
    'ImageBlock',
    'VideoEmbedBlock',
    'ProductFeatureBlock',
    'MetafieldBlock',
    'ProductBodyStreamBlock',
    'CollectionBodyStreamBlock',
    'ArticleBodyStreamBlock',
    'ProductBannerBlock',
    'PRODUCT_BODY_BLOCKS',
    'COLLECTION_BODY_BLOCKS',
    'ARTICLE_BODY_BLOCKS',
]

from wagtail.blocks import StreamBlock

from .content import HeadingBlock, ParagraphBlock, HtmlBlock, CalloutBlock, ProductBannerBlock
from .home import (
    TrustBarBlock,
    FeaturedCollectionsBlock,
    NavCollectionPillsBlock,
    EditorialIntroBlock,
    BestSellersBlock,
    ShopByNeedBlock,
    EducationalHubBlock,
    BrandValuesBlock,
    MarketBlock,
    FAQBlock,
    InternalLinksBlock,
    PromoGatewayBlock,
    SEOSchemaBlock,
)
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


class HomeBodyStreamBlock(StreamBlock):
    promo_gateway = PromoGatewayBlock()
    nav_collection_pills = NavCollectionPillsBlock()
    trust_bar = TrustBarBlock()
    featured_collections = FeaturedCollectionsBlock()
    editorial_intro = EditorialIntroBlock()
    best_sellers = BestSellersBlock()
    shop_by_need = ShopByNeedBlock()
    educational_hub = EducationalHubBlock()
    brand_values = BrandValuesBlock()
    market_block = MarketBlock()
    faq = FAQBlock()
    internal_links = InternalLinksBlock()
    seo_schema = SEOSchemaBlock()

    class Meta:
        label = 'Home Sections'
        # max_num only: min_num breaks admin save when the StreamField POST is
        # incomplete (preview/middleware). HomePage.clean() always restores the
        # canonical 13-block envelope.
        block_counts = {
            'promo_gateway': {'max_num': 1},
            'nav_collection_pills': {'max_num': 1},
            'trust_bar': {'max_num': 1},
            'featured_collections': {'max_num': 1},
            'editorial_intro': {'max_num': 1},
            'best_sellers': {'max_num': 1},
            'shop_by_need': {'max_num': 1},
            'educational_hub': {'max_num': 1},
            'brand_values': {'max_num': 1},
            'market_block': {'max_num': 1},
            'faq': {'max_num': 1},
            'internal_links': {'max_num': 1},
            'seo_schema': {'max_num': 1},
        }


HOME_BODY_BLOCKS = HomeBodyStreamBlock()

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
    'HomeBodyStreamBlock',
    'HOME_BODY_BLOCKS',
    'TrustBarBlock',
    'FeaturedCollectionsBlock',
    'NavCollectionPillsBlock',
    'EditorialIntroBlock',
    'BestSellersBlock',
    'ShopByNeedBlock',
    'EducationalHubBlock',
    'BrandValuesBlock',
    'MarketBlock',
    'FAQBlock',
    'InternalLinksBlock',
    'PromoGatewayBlock',
    'SEOSchemaBlock',
]

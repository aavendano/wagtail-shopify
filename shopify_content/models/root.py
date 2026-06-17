from wagtail.models import Page
from wagtail.admin.panels import FieldPanel


class ShopifyRootPage(Page):
    """
    Root/index page under which all Shopify content pages live.
    Create one instance in Wagtail admin as the parent for Products,
    Collections, and Blogs for this store.
    """
    parent_page_types = ['wagtailcore.Page']
    subpage_types = [
        'shopify_content.ProductPage',
        'shopify_content.CollectionPage',
        'shopify_content.BlogPage',
        'shopify_content.LocationPage',
    ]

    template = 'shopify_content/root_page.html'

    class Meta:
        verbose_name = 'Shopify Root'
        verbose_name_plural = 'Shopify Roots'

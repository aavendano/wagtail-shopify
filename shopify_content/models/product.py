from django.db import models
from django.utils.translation import gettext_lazy as _

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import (
    FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, TabbedInterface,
)
from wagtail.search import index

from .mixins import ShopifyMetafield, SHOPIFY_SYNC_PANELS
from ..blocks import PRODUCT_BODY_BLOCKS


class ProductPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'shopify_content.ProductPage',
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )


class ProductPageMetafield(ShopifyMetafield):
    page = ParentalKey(
        'shopify_content.ProductPage',
        on_delete=models.CASCADE,
        related_name='metafields',
    )


class ProductPage(Page):
    """
    Mirrors a Shopify Product.

    Shopify field → Wagtail field:
      title           → Page.title
      handle          → handle
      descriptionHtml → body (StreamField, rendered to HTML on outbound)
      vendor          → vendor
      productType     → product_type
      tags            → tags (ClusterTaggableManager)
      status          → status
      seo.title       → seo_title
      seo.description → seo_description
      metafields      → metafields InlinePanel (ProductPageMetafield)
    """

    # Shopify sync fields
    shopify_id = models.CharField(
        max_length=255, blank=True, db_index=True,
        help_text='Shopify GID, e.g. gid://shopify/Product/12345678',
    )
    handle = models.SlugField(
        max_length=255, blank=True,
        help_text='Shopify URL handle. Populated automatically on inbound import.',
    )
    sync_enabled = models.BooleanField(
        default=True,
        help_text='When unchecked, publishing will NOT sync to Shopify.',
    )
    last_synced_at = models.DateTimeField(null=True, blank=True)

    # Product-specific fields
    vendor = models.CharField(max_length=255, blank=True)
    product_type = models.CharField(max_length=255, blank=True)
    tags = ClusterTaggableManager(through=ProductPageTag, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('ACTIVE', 'Active'),
            ('ARCHIVED', 'Archived'),
            ('DRAFT', 'Draft'),
        ],
        default='ACTIVE',
    )

    body = StreamField(
        PRODUCT_BODY_BLOCKS,
        blank=True,
        use_json_field=True,
        help_text='Product description. Rendered to HTML for Shopify descriptionHtml.',
    )

    # seo_title and search_description are inherited from Page.
    # seo_title → Shopify seo.title
    # search_description → Shopify seo.description

    template = 'shopify_content/product_page.html'
    parent_page_types = ['wagtailcore.Page', 'shopify_content.ShopifyRootPage']
    subpage_types = []

    search_fields = Page.search_fields + [
        index.SearchField('vendor'),
        index.SearchField('product_type'),
        index.FilterField('status'),
        index.FilterField('shopify_id'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('vendor'),
            FieldPanel('product_type'),
            FieldPanel('tags'),
            FieldPanel('status'),
        ], heading='Shopify Product Details'),
        FieldPanel('body'),
        InlinePanel('metafields', label='Metafields'),
    ]

    promote_panels = [
        MultiFieldPanel([
            FieldPanel('seo_title'),
            FieldPanel('search_description'),
        ], heading='SEO'),
        MultiFieldPanel([
            FieldPanel('slug'),
        ], heading='Wagtail Internal'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(promote_panels, heading='SEO / Promote'),
        ObjectList(SHOPIFY_SYNC_PANELS, heading='Shopify'),
        ObjectList(Page.settings_panels, heading='Settings'),
    ])

    class Meta:
        verbose_name = 'Product Page'
        verbose_name_plural = 'Product Pages'

    def get_seo_title(self):
        return self.seo_title or self.title

    def get_seo_description(self):
        return self.search_description or ''

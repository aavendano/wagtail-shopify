from django.db import models
from django.utils.translation import gettext_lazy as _

from modelcluster.fields import ParentalKey

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import (
    FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, TabbedInterface,
)
from wagtail.search import index

from .mixins import ShopifyMetafield, SHOPIFY_SYNC_PANELS
from ..blocks import COLLECTION_BODY_BLOCKS


class CollectionPageMetafield(ShopifyMetafield):
    page = ParentalKey(
        'shopify_content.CollectionPage',
        on_delete=models.CASCADE,
        related_name='metafields',
    )


class CollectionPage(Page):
    """
    Mirrors a Shopify Collection.

    Shopify field → Wagtail field:
      title           → Page.title
      handle          → handle
      descriptionHtml → description (StreamField)
      sortOrder       → sort_order
      seo.title       → seo_title
      seo.description → seo_description
      metafields      → metafields InlinePanel
    """

    # Shopify sync fields
    shopify_id = models.CharField(
        max_length=255, blank=True, db_index=True,
        help_text='Shopify GID, e.g. gid://shopify/Collection/12345678',
    )
    handle = models.SlugField(max_length=255, blank=True)
    sync_enabled = models.BooleanField(default=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)

    sort_order = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('ALPHA_ASC', 'Alphabetically A–Z'),
            ('ALPHA_DESC', 'Alphabetically Z–A'),
            ('BEST_SELLING', 'Best Selling'),
            ('CREATED', 'Date Created (Oldest First)'),
            ('CREATED_DESC', 'Date Created (Newest First)'),
            ('MANUAL', 'Manually'),
            ('PRICE_ASC', 'Price Ascending'),
            ('PRICE_DESC', 'Price Descending'),
        ],
        default='MANUAL',
    )

    description = StreamField(
        COLLECTION_BODY_BLOCKS,
        blank=True,
        use_json_field=True,
        help_text='Collection description. Rendered to HTML for Shopify descriptionHtml.',
    )


    template = 'shopify_content/collection_page.html'
    parent_page_types = ['wagtailcore.Page', 'shopify_content.ShopifyRootPage']
    subpage_types = []

    search_fields = Page.search_fields + [
        index.FilterField('sort_order'),
        index.FilterField('shopify_id'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('sort_order'),
        FieldPanel('description'),
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
        verbose_name = 'Collection Page'
        verbose_name_plural = 'Collection Pages'

    def get_seo_title(self):
        return self.seo_title or self.title

    def get_seo_description(self):
        return self.search_description or ''

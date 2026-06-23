from django.db import models
from wagtail.models import Orderable
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

from wagtail_ai.panels import AIDescriptionFieldPanel


# Reusable panel list for the Shopify sync tab — imported by each page model.
# These panel names must match the fields defined in each page model class.
SHOPIFY_SYNC_PANELS = [
    MultiFieldPanel([
        FieldPanel('shopify_id'),
        FieldPanel('handle'),
        FieldPanel('sync_enabled'),
        FieldPanel('last_synced_at', read_only=True),
    ], heading='Shopify Sync'),
]

SHOPIFY_SEO_PANELS = [
    MultiFieldPanel([
        FieldPanel('seo_title'),
        AIDescriptionFieldPanel('search_description'),
    ], heading='SEO'),
]


class FAQItem(Orderable):
    """
    Abstract FAQ entry (question + answer) for any page type.
    Each concrete subclass adds a ParentalKey to its parent page.
    Synced to Shopify as metafield custom.faqs (JSON array).
    """
    question = models.CharField(max_length=500, verbose_name='Question')
    answer = models.TextField(verbose_name='Answer')

    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]

    class Meta(Orderable.Meta):
        abstract = True

    def __str__(self):
        return self.question[:80]


class ShopifyMetafield(models.Model):
    """
    Abstract base for inline metafield rows attached to a specific page type.
    Each concrete subclass defines a ParentalKey to its parent page.
    Maps 1:1 to Shopify's MetafieldsSetInput.
    """
    namespace = models.CharField(max_length=255, default='custom')
    key = models.CharField(max_length=64)
    type = models.CharField(
        max_length=100,
        default='single_line_text_field',
        help_text='Shopify metafield type, e.g. single_line_text_field, json, url',
    )
    value = models.TextField()

    panels = [
        FieldPanel('namespace'),
        FieldPanel('key'),
        FieldPanel('type'),
        FieldPanel('value'),
    ]

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.namespace}.{self.key}'

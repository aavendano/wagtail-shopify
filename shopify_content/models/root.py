from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import (
    FieldPanel, ObjectList, TabbedInterface,
)

from .mixins import SHOPIFY_SYNC_PANELS, SHOPIFY_SEO_PANELS


class ShopifyRootPage(Page):
    """
    Root/index page under which Shopify content pages live.

    Each instance syncs to a Shopify merchant-owned metaobject (type: root_page).
    Use export_config for type-specific theme/storefront configuration (JSON).
    """

    shopify_id = models.CharField(
        max_length=255, blank=True, db_index=True,
        help_text='Shopify metaobject GID (populated after first upsert)',
    )
    handle = models.SlugField(
        max_length=255, blank=True,
        help_text='Shopify metaobject handle (defaults to Wagtail slug)',
    )
    sync_enabled = models.BooleanField(default=True, db_default=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)
    export_config = models.JSONField(
        default=dict,
        blank=True,
        db_default={},
        help_text=(
            'Type-specific export payload pushed to Shopify metaobject field config. '
            'Example for slug=glossary: glossary_index.pages with Shopify Page GIDs.'
        ),
    )

    parent_page_types = ['wagtailcore.Page']
    subpage_types = [
        'shopify_content.ProductPage',
        'shopify_content.CollectionPage',
        'shopify_content.BlogPage',
        'shopify_content.LocationPage',
        'shopify_content.GlossaryTermPage',
    ]

    template = 'shopify_content/root_page.html'

    content_panels = Page.content_panels + [
        FieldPanel('export_config'),
    ]

    promote_panels = SHOPIFY_SEO_PANELS + [
        FieldPanel('slug'),
    ]

    settings_panels = SHOPIFY_SYNC_PANELS

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(promote_panels, heading='Promote'),
        ObjectList(settings_panels, heading='Shopify Sync'),
    ])

    class Meta:
        verbose_name = 'Shopify Root'
        verbose_name_plural = 'Shopify Roots'

    def save(self, **kwargs):
        if self.export_config is None:
            self.export_config = {}
        if not self.handle and self.slug:
            self.handle = self.slug
        super().save(**kwargs)

    def get_resource_type(self) -> str:
        from shopify_content.sync.import_parents import resource_type_for_root_slug
        return resource_type_for_root_slug(self.slug)

    def get_seo_title(self):
        return self.seo_title or self.title

    def get_seo_description(self):
        return self.search_description or ''

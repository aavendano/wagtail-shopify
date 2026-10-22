from django.core.exceptions import ValidationError
from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel, ObjectList, TabbedInterface
from wagtail.models import Page
from wagtail.search import index

from .mixins import SHOPIFY_SEO_PANELS

from ..admin_panels import StorefrontUrlsPanel

COUNTRY_CANADA = 'Canada'
COUNTRY_UNITED_STATES = 'United States'
COUNTRY_CHOICES = [
    (COUNTRY_CANADA, 'Canada'),
    (COUNTRY_UNITED_STATES, 'United States'),
]


class RegionPage(Page):
    """
    A province or state: a page of its own that links to the location pages inside it.

    Locations are its children in the Wagtail tree, so the link list is derived, not
    typed in. It maps to the Shopify ``region`` metaobject, which is published as a web
    page and holds ``location_pages``. The Wagtail ``title`` is the region name
    (Shopify ``province``).

    Syncing regions to Shopify is not wired yet: the Shopify definitions are generalized
    in code (``shopify_content/sync/unified_definitions.py``) and nothing changes in the
    store until the project is operational.
    """

    shopify_id = models.CharField(
        max_length=255, blank=True, db_index=True,
        help_text='Shopify metaobject GID (populated after first upsert)',
    )
    handle = models.SlugField(
        max_length=255, blank=True,
        help_text='Shopify metaobject handle (defaults to the Wagtail slug)',
    )
    sync_enabled = models.BooleanField(default=False, db_default=False)
    last_synced_at = models.DateTimeField(null=True, blank=True)

    country = models.CharField(
        max_length=100, choices=COUNTRY_CHOICES, verbose_name='Country',
        help_text='Spelled as Shopify spells it.',
    )
    region_code = models.CharField(
        max_length=2, blank=True, verbose_name='Province / state code',
        help_text='Two-letter code, e.g. ON or TX (Shopify province_code).',
    )
    header1 = models.CharField(max_length=255, blank=True, verbose_name='Header 1')
    header2 = models.CharField(max_length=255, blank=True, verbose_name='Header 2')
    greeting = models.TextField(blank=True, verbose_name='Greeting')

    template = 'shopify_content/region_page.html'
    parent_page_types = ['shopify_content.ShopifyRootPage']
    subpage_types = ['shopify_content.LocationPage']

    search_fields = Page.search_fields + [
        index.FilterField('shopify_id'),
        index.SearchField('greeting'),
        index.FilterField('country'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('country'),
            FieldPanel('region_code'),
        ], heading='Region'),
        MultiFieldPanel([
            FieldPanel('header1'),
            FieldPanel('header2'),
            FieldPanel('greeting'),
        ], heading='Hero'),
    ]

    promote_panels = SHOPIFY_SEO_PANELS + [
        FieldPanel('slug'),
    ]

    settings_panels = [
        MultiFieldPanel([
            FieldPanel('shopify_id'),
            FieldPanel('handle', read_only=True),
            FieldPanel('sync_enabled'),
            FieldPanel('last_synced_at', read_only=True),
        ], heading='Shopify Sync'),
        StorefrontUrlsPanel(),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(promote_panels, heading='SEO / Promote'),
        ObjectList(settings_panels, heading='Shopify Sync'),
    ])

    class Meta:
        verbose_name = 'Region Page'
        verbose_name_plural = 'Region Pages'

    def clean(self):
        super().clean()
        if self.region_code:
            self.region_code = self.region_code.strip().upper()
            if len(self.region_code) != 2 or not self.region_code.isalpha():
                raise ValidationError({'region_code': 'Use the two-letter code, e.g. ON or TX.'})

    def save(self, *args, **kwargs):
        if not self.handle:
            self.handle = self.slug
        super().save(*args, **kwargs)

    @property
    def location_pages(self):
        """Live location pages in this region, in city order (the region's link list)."""
        from .location_page import LocationPage

        return LocationPage.objects.child_of(self).live().order_by('city', 'title')

    def get_seo_title(self):
        return self.seo_title or self.title

    def get_seo_description(self):
        return self.search_description or self.header2 or ''

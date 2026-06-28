from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import (
    FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, TabbedInterface,
)
from wagtail.search import index

from .mixins import FAQItem, SHOPIFY_SEO_PANELS

from config.settings import ALLOWED_LOCALE_CODES
from ..location_slug import location_page_slug


class LocationPage(Page):
    """
    Wagtail page that syncs to a Shopify merchant-owned metaobject (type: local_page).

    The definition is created/verified at runtime via MetaobjectClient.ensure_definition().
    On publish, synced via MetaobjectClient.sync() with ensure_definition=True.
    Bootstrap the definition with: python manage.py ensure_metaobject_definitions
    """

    # Shopify sync fields
    shopify_id = models.CharField(
        max_length=255, blank=True, db_index=True,
        help_text='Shopify metaobject GID (populated after first upsert)',
    )
    handle = models.SlugField(
        max_length=255, blank=True,
        help_text='Shopify metaobject handle (auto-derived as <locale>-<city>[-<state>])',
    )
    sync_enabled = models.BooleanField(default=True, db_default=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)

    # Hero section
    titulo = models.CharField(max_length=255, verbose_name='Título')
    subtitulo = models.CharField(max_length=255, blank=True, verbose_name='Subtítulo')
    intro = RichTextField(
        blank=True, verbose_name='Intro',
        features=['bold', 'italic', 'link', 'ol', 'ul', 'h2', 'h3'],
    )

    # Location fields
    country = models.CharField(max_length=100, blank=True, verbose_name='Country')
    state = models.CharField(max_length=100, blank=True, verbose_name='State / Province')
    city = models.CharField(max_length=100, blank=True, verbose_name='City')

    # Section 2
    titulo_2 = models.CharField(max_length=255, blank=True, verbose_name='Título 2')
    subtitulo_h2 = models.CharField(max_length=255, blank=True, verbose_name='Subtítulo H2')
    content_2 = RichTextField(
        blank=True, verbose_name='Content 2',
        features=['bold', 'italic', 'link', 'ol', 'ul', 'h2', 'h3'],
    )

    # Section 3
    titulo_3 = models.CharField(max_length=255, blank=True, verbose_name='Título 3')
    subtitulo_3 = models.CharField(max_length=255, blank=True, verbose_name='Subtítulo 3')
    content_3 = RichTextField(
        blank=True, verbose_name='Content 3',
        features=['bold', 'italic', 'link', 'ol', 'ul', 'h2', 'h3'],
    )

    # Brand section
    brand_section_title = models.CharField(
        max_length=255, blank=True, verbose_name='Brand Section Title',
    )
    brand_section_subtitle = models.CharField(
        max_length=255, blank=True, verbose_name='Brand Section Subtitle',
    )
    brand_section_content = RichTextField(
        blank=True, verbose_name='Brand Section Content',
        features=['bold', 'italic', 'link', 'ol', 'ul', 'h2', 'h3'],
    )

    # Map section
    map_title = models.CharField(max_length=255, blank=True, verbose_name='Map Title')
    map_content = RichTextField(
        blank=True, verbose_name='Map Content',
        features=['bold', 'italic', 'link', 'ol', 'ul'],
    )

    # Closing content
    after_page_content = RichTextField(
        blank=True, verbose_name='After Page Content',
        features=['bold', 'italic', 'link', 'ol', 'ul', 'h2', 'h3'],
    )

    # Shopify locale override (e.g. "es", "en-CA"); blank = use page's locale
    shopify_locale = models.CharField(
        max_length=20, blank=True, verbose_name='Shopify Locale',
        help_text='Shopify locale code pushed to the locale field (e.g. "es", "en-CA").',
        choices=ALLOWED_LOCALE_CODES,
    )

    template = 'shopify_content/location_page.html'
    parent_page_types = ['wagtailcore.Page', 'shopify_content.ShopifyRootPage']
    subpage_types = []

    search_fields = Page.search_fields + [
        index.FilterField('shopify_id'),
        index.SearchField('titulo'),
        index.SearchField('city'),
        index.SearchField('country'),
        index.SearchField('intro'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('titulo'),
            FieldPanel('subtitulo'),
            FieldPanel('intro'),
        ], heading='Hero Section'),
        MultiFieldPanel([
            FieldPanel('country'),
            FieldPanel('state'),
            FieldPanel('city'),
        ], heading='Location'),
        MultiFieldPanel([
            FieldPanel('titulo_2'),
            FieldPanel('subtitulo_h2'),
            FieldPanel('content_2'),
        ], heading='Section 2'),
        MultiFieldPanel([
            FieldPanel('titulo_3'),
            FieldPanel('subtitulo_3'),
            FieldPanel('content_3'),
        ], heading='Section 3'),
        MultiFieldPanel([
            FieldPanel('brand_section_title'),
            FieldPanel('brand_section_subtitle'),
            FieldPanel('brand_section_content'),
        ], heading='Brand Section'),
        MultiFieldPanel([
            FieldPanel('map_title'),
            FieldPanel('map_content'),
        ], heading='Map Section'),
        FieldPanel('after_page_content'),
        InlinePanel('faqs', label='FAQs'),
    ]

    promote_panels = SHOPIFY_SEO_PANELS + [
        FieldPanel('shopify_locale'),
        FieldPanel('slug'),
    ]

    settings_panels = [
        MultiFieldPanel([
            FieldPanel('shopify_id'),
            FieldPanel('handle', read_only=True),
            FieldPanel('sync_enabled'),
            FieldPanel('last_synced_at', read_only=True),
        ], heading='Shopify Sync'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(promote_panels, heading='SEO / Promote'),
        ObjectList(settings_panels, heading='Shopify Sync'),
    ])

    class Meta:
        verbose_name = 'Location Page'
        verbose_name_plural = 'Location Pages'

    def clean(self):
        super().clean()
        canonical = location_page_slug(self)
        if canonical:
            self.slug = canonical
            self.handle = canonical

    def get_seo_title(self):
        return self.seo_title or self.titulo

    def get_seo_description(self):
        return self.search_description or self.subtitulo or ''


class LocationPageFAQ(FAQItem):
    page = ParentalKey(LocationPage, on_delete=models.CASCADE, related_name='faqs')

    class Meta(FAQItem.Meta):
        pass

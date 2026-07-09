from django.core.exceptions import ValidationError
from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import (
    FieldPanel, MultiFieldPanel, ObjectList, TabbedInterface,
)
from wagtail.search import index

from config.settings import ALLOWED_LOCALE_CODES
from .mixins import SHOPIFY_SEO_PANELS
from ..admin_panels import StorefrontUrlsPanel
from ..home_slug import home_page_handle


class HomePage(Page):
    """
    Wagtail page that syncs storefront home content to a Shopify merchant-owned
    metaobject (type: home_page), one instance per locale.

    Bootstrap the definition with: python manage.py ensure_metaobject_definitions
    """

    shopify_id = models.CharField(
        max_length=255, blank=True, db_index=True,
        help_text='Shopify metaobject GID (populated after first upsert)',
    )
    handle = models.SlugField(
        max_length=255, blank=True,
        help_text='Shopify metaobject handle (auto-derived as home-<locale>)',
    )
    sync_enabled = models.BooleanField(default=True, db_default=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)

    shopify_locale = models.CharField(
        max_length=20, blank=True, verbose_name='Shopify Locale',
        help_text='Locale code pushed to Shopify (e.g. en-US). Blank uses Wagtail locale.',
        choices=ALLOWED_LOCALE_CODES,
    )

    hero_eyebrow = models.CharField(
        max_length=60, blank=True, verbose_name='Hero eyebrow',
    )
    hero_heading = models.CharField(max_length=255, verbose_name='Hero heading')
    hero_subheading = models.CharField(max_length=500, blank=True, verbose_name='Hero subheading')
    hero_body = RichTextField(
        blank=True, verbose_name='Hero body',
        features=['bold', 'italic', 'link', 'ol', 'ul'],
    )
    hero_primary_cta_label = models.CharField(
        max_length=255, blank=True, verbose_name='Primary CTA label',
    )
    hero_primary_cta_url = models.URLField(max_length=500, blank=True, verbose_name='Primary CTA URL')
    hero_secondary_cta_label = models.CharField(
        max_length=255, blank=True, verbose_name='Secondary CTA label',
    )
    hero_secondary_cta_url = models.URLField(max_length=500, blank=True, verbose_name='Secondary CTA URL')
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Optional hero image; URL is pushed to Shopify on sync.',
    )
    hero_image_url = models.URLField(
        max_length=500,
        blank=True,
        help_text='Absolute hero image URL pushed to Shopify. Auto-filled from hero_image on sync.',
    )

    sections_json = models.JSONField(
        default=dict,
        blank=True,
        db_default={},
        help_text='Home sections JSON (version 1). See docs/home-page-content-schema.json.',
    )

    template = 'shopify_content/home_page.html'
    parent_page_types = ['shopify_content.ShopifyRootPage']
    subpage_types = []

    search_fields = Page.search_fields + [
        index.FilterField('shopify_id'),
        index.SearchField('hero_heading'),
        index.SearchField('hero_subheading'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_eyebrow'),
            FieldPanel('hero_heading'),
            FieldPanel('hero_subheading'),
            FieldPanel('hero_body'),
            FieldPanel('hero_image'),
            FieldPanel('hero_primary_cta_label'),
            FieldPanel('hero_primary_cta_url'),
            FieldPanel('hero_secondary_cta_label'),
            FieldPanel('hero_secondary_cta_url'),
        ], heading='Hero'),
        FieldPanel('sections_json'),
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
            FieldPanel('hero_image_url', read_only=True),
        ], heading='Shopify Sync'),
        StorefrontUrlsPanel(),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(promote_panels, heading='SEO / Promote'),
        ObjectList(settings_panels, heading='Shopify Sync'),
    ])

    class Meta:
        verbose_name = 'Home Page'
        verbose_name_plural = 'Home Pages'

    def clean(self):
        super().clean()
        canonical = home_page_handle(self)
        if canonical:
            self.slug = canonical
            self.handle = canonical

        if self.sections_json is None:
            self.sections_json = {}

        parent = self.get_parent()
        if parent is not None and parent.specific_class.__name__ == 'ShopifyRootPage':
            if parent.slug != 'cms-home':
                return
            siblings = HomePage.objects.child_of(parent).filter(locale=self.locale)
            if self.pk:
                siblings = siblings.exclude(pk=self.pk)
            if siblings.exists():
                raise ValidationError(
                    {'locale': 'Only one HomePage is allowed per locale under the home root.'}
                )

    def get_seo_title(self):
        return self.seo_title or self.hero_heading

    def get_seo_description(self):
        return self.search_description or self.hero_subheading or ''

from django.core.exceptions import ValidationError
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
from ..admin_panels import StorefrontUrlsPanel
from ..content_store.domain import EditorialMixin
from ..content_templates.location_city_en_us import find_forbidden_phrases
from ..forms import LocationPageForm
from ..location_slug import location_page_slug


class LocationPage(EditorialMixin, Page):
    """
    One location model for Canada and the United States.

    Today it syncs to the Shopify merchant-owned metaobject ``local_page`` (the US layout).
    The Canadian ``location_page`` fields (``discreet_shipping``, ``quality_focus``,
    ``body_safe_materials``, ``seo_keyword``) are stored here too; the generalized Shopify
    definitions are code-only for now (``shopify_content/sync/unified_definitions.py``).

    The parent is the ``RegionPage`` of its province or state (the region links back to its
    locations). A page placed directly under a root keeps working during the transition; run
    ``manage.py organize_location_regions`` to move such pages under their region.
    Field equivalences with the contract: titulo=header1, subtitulo=header2, intro=greeting,
    state=province.

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
    keep_shopify_handle = models.BooleanField(
        default=False, db_default=False,
        help_text=(
            'Keep the handle the store already uses instead of deriving it from locale, '
            'city and state. Set on pages imported from the Canadian location_page entries.'
        ),
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

    # Service messaging (Canadian layout; plain text, as in the Shopify location_page)
    discreet_shipping = models.TextField(blank=True, verbose_name='Discreet shipping')
    quality_focus = models.TextField(blank=True, verbose_name='Quality focus')
    body_safe_materials = models.TextField(blank=True, verbose_name='Body-safe materials')
    seo_keyword = models.CharField(max_length=255, blank=True, verbose_name='SEO keyword')

    # Shopify locale override (e.g. "es", "en-CA"); blank = use page's locale
    shopify_locale = models.CharField(
        max_length=20, blank=True, verbose_name='Shopify Locale',
        help_text='Shopify locale code pushed to the locale field (e.g. "es", "en-CA").',
        choices=ALLOWED_LOCALE_CODES,
    )

    template = 'shopify_content/location_page.html'
    base_form_class = LocationPageForm
    parent_page_types = [
        'shopify_content.RegionPage',
        'wagtailcore.Page',
        'shopify_content.ShopifyRootPage',
    ]
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
        MultiFieldPanel([
            FieldPanel('discreet_shipping'),
            FieldPanel('quality_focus'),
            FieldPanel('body_safe_materials'),
            FieldPanel('seo_keyword'),
        ], heading='Service messaging'),
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
            FieldPanel('keep_shopify_handle'),
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
        verbose_name = 'Location Page'
        verbose_name_plural = 'Location Pages'

    @property
    def region(self):
        """The RegionPage this location sits under, or None while it hangs off a root."""
        from .region_page import RegionPage

        parent = self.get_parent()
        if parent is None:
            return None
        specific = parent.specific
        return specific if isinstance(specific, RegionPage) else None

    # Set by importers (never persisted) so existing store content is not rejected.
    _skip_editorial_checks = False

    def clean(self):
        super().clean()
        self._apply_region_data()
        canonical = location_page_slug(self)
        if canonical:
            self.slug = canonical
            if not (self.keep_shopify_handle and self.handle):
                self.handle = canonical

        rich_parts = [
            str(self.intro or ''),
            str(self.content_2 or ''),
            str(self.content_3 or ''),
            str(self.brand_section_content or ''),
            str(self.map_content or ''),
            str(self.after_page_content or ''),
            str(self.discreet_shipping or ''),
            str(self.quality_focus or ''),
            str(self.body_safe_materials or ''),
        ]
        for faq in self.faqs.all():
            rich_parts.append(faq.question)
            rich_parts.append(faq.answer)

        # Content imported from Shopify is stored as the store has it; editors hit this check
        # on their next save.
        forbidden = [] if self._skip_editorial_checks else find_forbidden_phrases(' '.join(rich_parts))
        if forbidden:
            raise ValidationError(
                {
                    'intro': (
                        'Content contains forbidden brick-and-mortar phrases: '
                        + ', '.join(forbidden)
                    )
                }
            )

    def _apply_region_data(self):
        """Province/state and country follow the parent region page."""
        region = self.region
        if region is None:
            return
        self.state = region.title
        if region.country:
            self.country = region.country

    def get_seo_title(self):
        return self.seo_title or self.titulo

    def get_seo_description(self):
        return self.search_description or self.subtitulo or ''


class LocationPageFAQ(FAQItem):
    page = ParentalKey(LocationPage, on_delete=models.CASCADE, related_name='faqs')

    class Meta(FAQItem.Meta):
        pass

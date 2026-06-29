from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import (
    FieldPanel, ObjectList, TabbedInterface,
)
from wagtail.search import index

from shopify_content.admin_panels import semantic_links_panel
from .mixins import SHOPIFY_SYNC_PANELS

LOCALE_CODE_CHOICES = [
    ('en', 'English'),
    ('es', 'Spanish'),
    ('fr', 'French'),
]


class GlossaryTermPage(Page):
    """
    Wagtail page that syncs to a Shopify merchant-owned metaobject (type: glossary_term).

    Terms live under a ShopifyRootPage with slug=glossary (organizational only).
    The /pages/glossary list page is managed by the Shopify theme via Liquid.

    Bootstrap the definition with: python manage.py ensure_metaobject_definitions
    """

    # Shopify sync fields
    shopify_id = models.CharField(
        max_length=255, blank=True, db_index=True,
        help_text='Shopify metaobject GID (populated after first upsert)',
    )
    handle = models.SlugField(
        max_length=255, blank=True,
        help_text='Shopify metaobject handle (defaults to slugified term)',
    )
    sync_enabled = models.BooleanField(default=True, db_default=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)

    term = models.CharField(max_length=255, verbose_name='Term')
    definition = RichTextField(
        blank=True,
        features=['bold', 'italic', 'link', 'ol', 'ul', 'h2', 'h3'],
    )
    locale_code = models.CharField(
        max_length=10,
        choices=LOCALE_CODE_CHOICES,
        default='en',
        help_text='Locale pushed to the Shopify locale field.',
    )
    related_links = models.JSONField(default=list, blank=True, db_default=[])
    external_links = models.JSONField(default=list, blank=True, db_default=[])
    synonyms = models.JSONField(
        default=list,
        blank=True,
        db_default=[],
        help_text=(
            'Sinónimos / siglas / variantes. Lista de strings → '
            'Shopify list.single_line_text_field'
        ),
    )
    same_as = models.JSONField(
        default=list,
        blank=True,
        db_default=[],
        help_text=(
            'URLs de entidad canónica externa (Wikipedia/Wikidata). '
            'Lista de URLs → Shopify list.url'
        ),
    )

    template = 'shopify_content/glossary_term_page.html'
    parent_page_types = ['shopify_content.ShopifyRootPage']
    subpage_types = []

    search_fields = Page.search_fields + [
        index.FilterField('shopify_id'),
        index.SearchField('term'),
        index.SearchField('definition'),
        index.SearchField('synonyms'),
    ]

    content_panels = [
        FieldPanel('term'),
        FieldPanel('definition'),
        FieldPanel('locale_code'),
        semantic_links_panel(),
        FieldPanel('external_links'),
        FieldPanel('synonyms'),
        FieldPanel('same_as'),
    ]

    promote_panels = [
        FieldPanel('slug'),
    ]

    settings_panels = SHOPIFY_SYNC_PANELS

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(promote_panels, heading='Promote'),
        ObjectList(settings_panels, heading='Shopify Sync'),
    ])

    class Meta:
        verbose_name = 'Glossary Term'
        verbose_name_plural = 'Glossary Terms'

    def save(self, **kwargs):
        if self.term:
            self.title = self.term
        for field_name in ('related_links', 'external_links', 'synonyms', 'same_as'):
            if getattr(self, field_name) is None:
                setattr(self, field_name, [])
        super().save(**kwargs)

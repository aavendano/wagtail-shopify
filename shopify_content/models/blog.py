from django.db import models

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
from ..blocks import ARTICLE_BODY_BLOCKS


# ---------------------------------------------------------------------------
# Blog (index / container page)
# ---------------------------------------------------------------------------

class BlogPage(Page):
    """
    Mirrors a Shopify Blog (the container object).

    Shopify field → Wagtail field:
      id            → shopify_id
      handle        → handle
      title         → Page.title
      commentPolicy → comment_policy

    No native description or seo fields in Shopify Blog API.
    Synced as metafields:
      description        → descriptors.description
      seo_title          → global.title_tag
      search_description → global.description_tag
    """

    # Shopify sync fields
    shopify_id = models.CharField(
        max_length=255, blank=True, db_index=True,
        help_text='Shopify GID, e.g. gid://shopify/Blog/12345678',
    )
    handle = models.SlugField(max_length=255, blank=True)
    sync_enabled = models.BooleanField(default=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)

    comment_policy = models.CharField(
        max_length=20,
        choices=[
            ('AUTO_PUBLISHED', 'Auto Published (visible immediately)'),
            ('CLOSED', 'Closed (no comments)'),
            ('MODERATED', 'Moderated (staff approval required)'),
        ],
        default='CLOSED',
        help_text='Maps to Shopify Blog commentPolicy.',
    )

    description = models.TextField(
        blank=True,
        help_text='Blog description (HTML allowed). Synced as metafield descriptors.description.',
    )

    # seo_title and search_description inherited from Page.
    # Synced as metafields global.title_tag / global.description_tag
    # (Blog has no native seo field in Shopify Admin GraphQL API.)

    template = 'shopify_content/blog_page.html'
    parent_page_types = ['wagtailcore.Page', 'shopify_content.ShopifyRootPage']
    subpage_types = ['shopify_content.ArticlePage']

    search_fields = Page.search_fields + [
        index.FilterField('shopify_id'),
        index.SearchField('description'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('comment_policy'),
        FieldPanel('description'),
    ]

    promote_panels = [
        MultiFieldPanel([
            FieldPanel('seo_title'),
            FieldPanel('search_description'),
        ], heading='SEO (synced as Shopify metafields global.title_tag / description_tag)'),
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
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    def get_seo_title(self):
        return self.seo_title or self.title

    def get_seo_description(self):
        return self.search_description or self.description or ''


# ---------------------------------------------------------------------------
# Article
# ---------------------------------------------------------------------------

class ArticlePageTag(TaggedItemBase):
    content_object = ParentalKey(
        'shopify_content.ArticlePage',
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )


class ArticlePageMetafield(ShopifyMetafield):
    page = ParentalKey(
        'shopify_content.ArticlePage',
        on_delete=models.CASCADE,
        related_name='metafields',
    )


class ArticlePage(Page):
    """
    Mirrors a Shopify Article inside a Blog.

    Shopify field → Wagtail field:
      id          → shopify_id
      handle      → handle
      title       → Page.title
      author.name → author (CharField — full name string)
      body        → body (StreamField, rendered to HTML on outbound)
      publishedAt → published_at
      summary     → summary (HTML text)
      tags        → tags (ClusterTaggableManager)
      image       → featured_image (Wagtail Image FK)

    SEO: Article has no native seo field in Shopify Admin GraphQL API.
    Synced as metafields: namespace=global, key=title_tag / description_tag.
    """

    # Shopify sync fields
    shopify_id = models.CharField(
        max_length=255, blank=True, db_index=True,
        help_text='Shopify GID, e.g. gid://shopify/Article/12345678',
    )
    handle = models.SlugField(max_length=255, blank=True)
    sync_enabled = models.BooleanField(default=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)

    author = models.CharField(
        max_length=255, blank=True,
        help_text='Author full name. Maps to Shopify AuthorInput.name.',
    )
    published_at = models.DateTimeField(
        null=True, blank=True,
        help_text='Maps to Shopify publishedAt. Auto-set on first publish if blank.',
    )
    summary = models.TextField(
        blank=True,
        help_text='Short summary (HTML allowed). Maps to Shopify article summary field.',
    )
    tags = ClusterTaggableManager(through=ArticlePageTag, blank=True)
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Maps to Shopify Article image.',
    )

    body = StreamField(
        ARTICLE_BODY_BLOCKS,
        blank=True,
        use_json_field=True,
        help_text='Article body content. Rendered to HTML for Shopify body field.',
    )

    # seo_title and search_description are inherited from Page.
    # For Article: seo_title → metafield global.title_tag
    #              search_description → metafield global.description_tag
    # (Article has no native seo field in the Shopify Admin GraphQL API.)

    template = 'shopify_content/article_page.html'
    parent_page_types = ['shopify_content.BlogPage']
    subpage_types = []

    search_fields = Page.search_fields + [
        index.SearchField('author'),
        index.SearchField('summary'),
        index.FilterField('published_at'),
        index.FilterField('shopify_id'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('author'),
            FieldPanel('published_at'),
            FieldPanel('tags'),
        ], heading='Article Details'),
        FieldPanel('featured_image'),
        FieldPanel('summary'),
        FieldPanel('body'),
        InlinePanel('metafields', label='Metafields'),
    ]

    promote_panels = [
        MultiFieldPanel([
            FieldPanel('seo_title'),
            FieldPanel('search_description'),
        ], heading='SEO (synced as Shopify metafields global.title_tag / description_tag)'),
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
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def get_seo_title(self):
        return self.seo_title or self.title

    def get_seo_description(self):
        return self.search_description or self.summary or ''

    def save(self, **kwargs):
        from django.utils import timezone
        if self.live and not self.published_at:
            self.published_at = timezone.now()
        super().save(**kwargs)

from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.models import Orderable
from wagtail.admin.panels import FieldPanel


class SemanticPageLink(Orderable):
    """
    Abstract internal link from a content page to any Wagtail Page.

    is_auto=True rows are replaced on semantic refresh; is_auto=False are editor-curated.
    """

    related_page = models.ForeignKey(
        'wagtailcore.Page',
        related_name='+',
        on_delete=models.CASCADE,
    )
    is_auto = models.BooleanField(
        default=False,
        db_default=False,
        help_text='True when created by semantic auto-generation on publish.',
    )

    panels = [
        FieldPanel('related_page'),
    ]

    class Meta(Orderable.Meta):
        abstract = True


class ArticleSemanticLink(SemanticPageLink):
    page = ParentalKey(
        'shopify_content.ArticlePage',
        related_name='semantic_links',
        on_delete=models.CASCADE,
    )

    class Meta(Orderable.Meta):
        verbose_name = 'Internal link'
        verbose_name_plural = 'Internal links'


class ProductSemanticLink(SemanticPageLink):
    page = ParentalKey(
        'shopify_content.ProductPage',
        related_name='semantic_links',
        on_delete=models.CASCADE,
    )

    class Meta(Orderable.Meta):
        verbose_name = 'Internal link'
        verbose_name_plural = 'Internal links'


class CollectionSemanticLink(SemanticPageLink):
    page = ParentalKey(
        'shopify_content.CollectionPage',
        related_name='semantic_links',
        on_delete=models.CASCADE,
    )

    class Meta(Orderable.Meta):
        verbose_name = 'Internal link'
        verbose_name_plural = 'Internal links'


class GlossarySemanticLink(SemanticPageLink):
    page = ParentalKey(
        'shopify_content.GlossaryTermPage',
        related_name='semantic_links',
        on_delete=models.CASCADE,
    )

    class Meta(Orderable.Meta):
        verbose_name = 'Internal link'
        verbose_name_plural = 'Internal links'

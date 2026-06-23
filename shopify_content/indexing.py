"""Shared helpers for batched vector index updates."""

from django_ai_core.contrib.index.source import ModelSource

from shopify_content.models.blog import ArticlePage
from shopify_content.models.product import ProductPage

ARTICLE_INDEX_FIELDS = [
    'title',
    'seo_title',
    'search_description',
    'summary',
    'author',
    'body',
]

PRODUCT_INDEX_FIELDS = [
    'title',
    'seo_title',
    'search_description',
    'body',
    'vendor',
    'product_type',
]

INDEX_MODELS = {
    'article': (ArticlePage, ARTICLE_INDEX_FIELDS),
    'product': (ProductPage, PRODUCT_INDEX_FIELDS),
}


def model_source_for(model, content_fields, *, start_pk=0):
    return ModelSource(
        model=model,
        content_fields=content_fields,
        queryset=model.objects.live().filter(pk__gt=start_pk).order_by('pk'),
    )

"""Shared helpers for batched vector index updates."""

from django.conf import settings

from django_ai_core.contrib.index.base import registry
from django_ai_core.contrib.index.source import ModelSource

from shopify_content.models.blog import ArticlePage
from shopify_content.models.collection import CollectionPage
from shopify_content.models.glossary import GlossaryTermPage
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

COLLECTION_INDEX_FIELDS = [
    'title',
    'seo_title',
    'search_description',
    'description',
]

GLOSSARY_INDEX_FIELDS = [
    'term',
    'definition',
    'title',
    'search_description',
    'synonyms',
]

INDEX_MODELS = {
    'article': (ArticlePage, ARTICLE_INDEX_FIELDS),
    'product': (ProductPage, PRODUCT_INDEX_FIELDS),
    'collection': (CollectionPage, COLLECTION_INDEX_FIELDS),
    'glossary': (GlossaryTermPage, GLOSSARY_INDEX_FIELDS),
}

INDEX_CONTENT_FIELDS_BY_MODEL = {
    ArticlePage: ARTICLE_INDEX_FIELDS,
    ProductPage: PRODUCT_INDEX_FIELDS,
    CollectionPage: COLLECTION_INDEX_FIELDS,
    GlossaryTermPage: GLOSSARY_INDEX_FIELDS,
}


def live_queryset_for(model):
    qs = model.objects.live()
    if model is ProductPage:
        qs = qs.filter(status='ACTIVE')
    return qs


def model_source_for(model, content_fields, *, start_pk=0):
    return ModelSource(
        model=model,
        content_fields=content_fields,
        queryset=live_queryset_for(model).filter(pk__gt=start_pk).order_by('pk'),
    )


def index_single_page(page):
    """Update PageIndex for one published page (no-op when pgvector disabled)."""
    if not getattr(settings, 'WAGTAIL_AI_PGVECTOR', False):
        return False
    if 'PageIndex' not in registry.list():
        return False

    specific = page.specific
    content_fields = INDEX_CONTENT_FIELDS_BY_MODEL.get(type(specific))
    if content_fields is None:
        return False

    source = ModelSource(
        model=type(specific),
        content_fields=content_fields,
        queryset=live_queryset_for(type(specific)).filter(pk=specific.pk),
    )
    docs = list(source.objects_to_documents([specific]))
    if not docs:
        return False

    index = registry.get('PageIndex')()
    index.update(docs)
    return True

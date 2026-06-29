from django.conf import settings
from django_ai_core.contrib.index import (
    CachedEmbeddingTransformer,
    CoreEmbeddingTransformer,
    VectorIndex,
    registry,
)
from django_ai_core.contrib.index.source import ModelSource
from django_ai_core.contrib.index.storage.pgvector import PgVectorProvider
from django_ai_core.llm import LLMService

from shopify_content.indexing import (
    ARTICLE_INDEX_FIELDS,
    COLLECTION_INDEX_FIELDS,
    GLOSSARY_INDEX_FIELDS,
    PRODUCT_INDEX_FIELDS,
    live_queryset_for,
)
from shopify_content.models.blog import ArticlePage
from shopify_content.models.collection import CollectionPage
from shopify_content.models.glossary import GlossaryTermPage
from shopify_content.models.product import ProductPage


def _gemini_api_key():
    wagtail_ai = getattr(settings, 'WAGTAIL_AI', {})
    default_provider = wagtail_ai.get('PROVIDERS', {}).get('default', {})
    return default_provider.get('api_key', '')


def register_page_index():
    if not getattr(settings, 'WAGTAIL_AI_PGVECTOR', False):
        return
    if not _gemini_api_key():
        return

    llm_embedding_service = LLMService.create(
        provider='gemini',
        model='gemini-embedding-001',
        api_key=_gemini_api_key(),
    )

    @registry.register()
    class PageIndex(VectorIndex):
        sources = [
            ModelSource(
                model=ArticlePage,
                content_fields=ARTICLE_INDEX_FIELDS,
                queryset=live_queryset_for(ArticlePage),
            ),
            ModelSource(
                model=ProductPage,
                content_fields=PRODUCT_INDEX_FIELDS,
                queryset=live_queryset_for(ProductPage),
            ),
            ModelSource(
                model=CollectionPage,
                content_fields=COLLECTION_INDEX_FIELDS,
                queryset=live_queryset_for(CollectionPage),
            ),
            ModelSource(
                model=GlossaryTermPage,
                content_fields=GLOSSARY_INDEX_FIELDS,
                queryset=live_queryset_for(GlossaryTermPage),
            ),
        ]
        storage_provider = PgVectorProvider()
        embedding_transformer = CachedEmbeddingTransformer(
            base_transformer=CoreEmbeddingTransformer(llm_service=llm_embedding_service),
        )

    return PageIndex


register_page_index()

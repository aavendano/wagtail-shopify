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


def _debug_log_index(message, data=None):
    # #region agent log
    import json
    import time
    try:
        payload = {
            'sessionId': '0938b0',
            'runId': 'pre-fix',
            'hypothesisId': 'C',
            'location': 'shopify_content/indexes.py',
            'message': message,
            'data': data or {},
            'timestamp': int(time.time() * 1000),
        }
        with open('/home/alejandro/apps/wagtail-shopify/.cursor/debug-0938b0.log', 'a', encoding='utf-8') as log_file:
            log_file.write(json.dumps(payload) + '\n')
    except OSError:
        pass
    # #endregion


def _gemini_api_key():
    wagtail_ai = getattr(settings, 'WAGTAIL_AI', {})
    default_provider = wagtail_ai.get('PROVIDERS', {}).get('default', {})
    return default_provider.get('api_key', '')


def register_page_index():
    if not getattr(settings, 'WAGTAIL_AI_PGVECTOR', False):
        _debug_log_index('PageIndex skipped: WAGTAIL_AI_PGVECTOR disabled')
        return
    if not _gemini_api_key():
        _debug_log_index('PageIndex skipped: missing Gemini API key')
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


result = register_page_index()
_debug_log_index(
    'PageIndex registration complete',
    {'registered': result is not None, 'registry_keys': list(registry.list().keys())},
)

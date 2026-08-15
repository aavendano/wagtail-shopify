from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from django.test import TestCase, override_settings
from wagtail.models import Locale, Page

from shopify_content.models import (
    CollectionPage,
    GlossaryTermPage,
    ProductPage,
    ShopifyRootPage,
)
from shopify_content.semantic_links.service import (
    PAGE_TYPE_KEYS,
    SemanticSuggestUnavailable,
    assemble_preview_query_text,
    suggest_related_with_scores,
)


def _fake_doc(pk, score, model_label='shopify_content.CollectionPage'):
    return SimpleNamespace(
        metadata={'pk': pk},
        document_key=f'{model_label}:{pk}:0',
        score=score,
    )


class AssemblePreviewQueryTextTests(TestCase):
    def test_glossary_fields_and_free_text(self):
        text = assemble_preview_query_text(
            'glossary',
            text='Chastity Belt',
            fields={'definition': '<p>A locking device.</p>', 'synonyms': ['belt', 'cage']},
        )
        self.assertIn('Chastity Belt', text)
        self.assertIn('A locking device.', text)
        self.assertIn('belt, cage', text)


class SuggestRelatedWithScoresTests(TestCase):
    def setUp(self):
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.root = ShopifyRootPage(title='Root', slug='root', locale=locale)
        home.add_child(instance=self.root)
        self.root.save_revision().publish()

        self.collections = []
        for slug in [f'col-{i}' for i in range(6)]:
            page = CollectionPage(
                title=slug,
                slug=slug,
                handle=slug,
                locale=locale,
            )
            self.root.add_child(instance=page)
            page.save_revision().publish()
            self.collections.append(page)

        self.product = ProductPage(
            title='Active Product',
            slug='active-product',
            handle='active-product',
            locale=locale,
            status='ACTIVE',
        )
        self.root.add_child(instance=self.product)
        self.product.save_revision().publish()

        self.draft = ProductPage(
            title='Draft Product',
            slug='draft-product',
            handle='draft-product',
            locale=locale,
            status='DRAFT',
        )
        self.root.add_child(instance=self.draft)
        self.draft.save_revision().publish()

        Locale.objects.get_or_create(language_code='es-US')
        es = Locale.objects.get(language_code='es-US')
        self.es_collection = CollectionPage(
            title='es-col',
            slug='es-col',
            handle='es-col',
            locale=es,
        )
        self.root.add_child(instance=self.es_collection)
        self.es_collection.save_revision().publish()

        glossary_root = ShopifyRootPage(title='Glossary', slug='glossary', locale=locale)
        self.root.add_child(instance=glossary_root)
        glossary_root.save_revision().publish()
        self.source = GlossaryTermPage(
            title='Chastity Belt',
            term='Chastity Belt',
            slug='chastity-belt',
            handle='chastity-belt',
            locale=locale,
        )
        glossary_root.add_child(instance=self.source)
        self.source.save_revision().publish()

        self.locale_id = locale.pk

    def _patch_index(self, documents):
        index = MagicMock()
        index.search_documents.return_value = documents
        registry = MagicMock()
        registry.list.return_value = ['PageIndex']
        registry.get.return_value = lambda: index
        return patch(
            'django_ai_core.contrib.index.base.registry',
            registry,
        ), index

    @override_settings(WAGTAIL_AI_PGVECTOR=True, SEMANTIC_LINKS_TYPE_OVERFETCH=1)
    def test_limit_per_type_is_not_production_cap(self):
        docs = [
            _fake_doc(page.pk, 0.9 - i * 0.01)
            for i, page in enumerate(self.collections)
        ]
        ctx, index = self._patch_index(docs)
        with ctx:
            grouped = suggest_related_with_scores(
                content='bdsm gear',
                locale_id=self.locale_id,
                allowed_types=['collection'],
                exclude_pks=[],
                limit_per_type=20,
            )
        index.search_documents.assert_called_once()
        self.assertEqual(len(grouped['collection']), 6)
        self.assertTrue(all('score' in item for item in grouped['collection']))
        self.assertGreater(grouped['collection'][0]['score'], grouped['collection'][-1]['score'])

    @override_settings(WAGTAIL_AI_PGVECTOR=True, SEMANTIC_LINKS_TYPE_OVERFETCH=1)
    def test_types_filter_and_excludes_self(self):
        docs = [
            _fake_doc(self.product.pk, 0.99, 'shopify_content.ProductPage'),
            _fake_doc(self.collections[0].pk, 0.88),
            _fake_doc(self.source.pk, 0.95, 'shopify_content.GlossaryTermPage'),
        ]
        ctx, _index = self._patch_index(docs)
        with ctx:
            grouped = suggest_related_with_scores(
                content='Chastity Belt',
                locale_id=self.locale_id,
                allowed_types=['collection'],
                exclude_pks=[self.source.pk],
                limit_per_type=20,
            )
        self.assertEqual([item['id'] for item in grouped['collection']], [self.collections[0].pk])
        self.assertEqual(grouped['product'], [])
        self.assertEqual(grouped['glossary'], [])

    @override_settings(WAGTAIL_AI_PGVECTOR=True, SEMANTIC_LINKS_TYPE_OVERFETCH=1)
    def test_filters_locale_and_inactive_products(self):
        docs = [
            _fake_doc(self.es_collection.pk, 0.9),
            _fake_doc(self.draft.pk, 0.95, 'shopify_content.ProductPage'),
            _fake_doc(self.product.pk, 0.8, 'shopify_content.ProductPage'),
        ]
        ctx, _index = self._patch_index(docs)
        with ctx:
            grouped = suggest_related_with_scores(
                content='toy',
                locale_id=self.locale_id,
                allowed_types=list(PAGE_TYPE_KEYS),
                exclude_pks=[],
                limit_per_type=20,
            )
        self.assertEqual(grouped['collection'], [])
        self.assertEqual([item['id'] for item in grouped['product']], [self.product.pk])

    @override_settings(WAGTAIL_AI_PGVECTOR=True)
    @patch('shopify_content.semantic_links.service.delete_auto_semantic_links')
    def test_does_not_persist_links(self, mock_delete):
        docs = [_fake_doc(self.collections[0].pk, 0.7)]
        ctx, _index = self._patch_index(docs)
        with ctx:
            suggest_related_with_scores(
                content='bdsm',
                locale_id=self.locale_id,
                allowed_types=['collection'],
                exclude_pks=[],
                limit_per_type=20,
            )
        mock_delete.assert_not_called()

    @override_settings(WAGTAIL_AI_PGVECTOR=False)
    def test_unavailable_without_pgvector(self):
        with self.assertRaises(SemanticSuggestUnavailable):
            suggest_related_with_scores(
                content='bdsm',
                locale_id=self.locale_id,
                allowed_types=['collection'],
                exclude_pks=[],
                limit_per_type=20,
            )

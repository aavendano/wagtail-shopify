"""Regression tests for django-ai-core stable index_name tracking fix."""

from __future__ import annotations

from types import SimpleNamespace
from unittest import skipUnless

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from wagtail.models import Locale, Page

from shopify_content.models import ProductPage, ShopifyRootPage
from shopify_content.vector_index_tracking_fix import (
    install_stable_index_name_fix,
    patched_post_index_update,
    stable_index_name,
)

try:
    from django_ai_core.contrib.index.models import ModelSourceIndex
    from django_ai_core.contrib.index.source import ModelSource

    HAS_DJANGO_AI_CORE = True
except ImportError:  # pragma: no cover
    HAS_DJANGO_AI_CORE = False
    ModelSourceIndex = None  # type: ignore[misc, assignment]
    ModelSource = None  # type: ignore[misc, assignment]


class FakePageIndex:
    """Stand-in whose __str__ mimics the buggy upstream representation."""

    def __str__(self):
        return f'<{self.__class__.__module__}.{self.__class__.__qualname__} object at {hex(id(self))}>'


class StableIndexNameTests(TestCase):
    def test_class_name_is_stable_across_instances(self):
        a = FakePageIndex()
        b = FakePageIndex()
        self.assertEqual(stable_index_name(a), 'FakePageIndex')
        self.assertEqual(stable_index_name(b), 'FakePageIndex')
        self.assertNotEqual(str(a), str(b))

    def test_string_passthrough(self):
        self.assertEqual(stable_index_name('PageIndex'), 'PageIndex')


@skipUnless(HAS_DJANGO_AI_CORE, 'django-ai-core is not installed')
class ModelSourceIndexTrackingFixTests(TestCase):
    SOURCE_ID = 'shopify_content.ProductPage'

    def setUp(self):
        install_stable_index_name_fix()

        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.root = ShopifyRootPage(title='Root', slug='root-vix', locale=locale)
        home.add_child(instance=self.root)
        self.root.save_revision().publish()

        self.product_a = ProductPage(
            title='Product A',
            slug='product-a-vix',
            handle='product-a-vix',
            locale=locale,
            status='ACTIVE',
        )
        self.root.add_child(instance=self.product_a)
        self.product_a.save_revision().publish()

        self.product_b = ProductPage(
            title='Product B',
            slug='product-b-vix',
            handle='product-b-vix',
            locale=locale,
            status='ACTIVE',
        )
        self.root.add_child(instance=self.product_b)
        self.product_b.save_revision().publish()

        self.content_type = ContentType.objects.get_for_model(ProductPage)
        self.broken_name = (
            '<shopify_content.indexes.register_page_index.<locals>.PageIndex '
            'object at 0xdeadbeef>'
        )
        ModelSourceIndex.objects.create(
            content_type=self.content_type,
            object_id=self.product_a.pk,
            index_name=self.broken_name,
            source_id=self.SOURCE_ID,
        )

    def _source(self, queryset):
        return SimpleNamespace(
            model=ProductPage,
            queryset=queryset,
            source_id=self.SOURCE_ID,
        )

    def _stable_rows(self):
        return ModelSourceIndex.objects.filter(
            index_name='FakePageIndex',
            source_id=self.SOURCE_ID,
        )

    def _broken_rows(self):
        return ModelSourceIndex.objects.filter(index_name=self.broken_name)

    def test_two_syncs_are_idempotent(self):
        source = self._source(
            ProductPage.objects.filter(pk__in=[self.product_a.pk, self.product_b.pk])
        )
        index = FakePageIndex()

        patched_post_index_update(source, index)
        first_count = self._stable_rows().count()
        first_ids = set(self._stable_rows().values_list('id', flat=True))
        self.assertEqual(first_count, 2)

        patched_post_index_update(source, FakePageIndex())
        second_count = self._stable_rows().count()
        second_ids = set(self._stable_rows().values_list('id', flat=True))

        self.assertEqual(second_count, first_count)
        self.assertEqual(second_ids, first_ids)

    def test_adds_new_and_removes_obsolete_stable_rows(self):
        source = self._source(ProductPage.objects.filter(pk=self.product_a.pk))
        patched_post_index_update(source, FakePageIndex())
        self.assertEqual(
            set(self._stable_rows().values_list('object_id', flat=True)),
            {self.product_a.pk},
        )

        source = self._source(
            ProductPage.objects.filter(pk__in=[self.product_a.pk, self.product_b.pk])
        )
        patched_post_index_update(source, FakePageIndex())
        self.assertEqual(
            set(self._stable_rows().values_list('object_id', flat=True)),
            {self.product_a.pk, self.product_b.pk},
        )

        source = self._source(ProductPage.objects.filter(pk=self.product_b.pk))
        patched_post_index_update(source, FakePageIndex())
        self.assertEqual(
            set(self._stable_rows().values_list('object_id', flat=True)),
            {self.product_b.pk},
        )

    def test_source_id_isolation(self):
        other_source_id = 'shopify_content.ArticlePage'
        ModelSourceIndex.objects.create(
            content_type=self.content_type,
            object_id=self.product_a.pk,
            index_name='FakePageIndex',
            source_id=other_source_id,
        )
        source = self._source(ProductPage.objects.filter(pk=self.product_b.pk))
        patched_post_index_update(source, FakePageIndex())

        self.assertTrue(
            ModelSourceIndex.objects.filter(
                index_name='FakePageIndex',
                source_id=other_source_id,
                object_id=self.product_a.pk,
            ).exists()
        )
        self.assertEqual(
            set(
                ModelSourceIndex.objects.filter(
                    index_name='FakePageIndex',
                    source_id=self.SOURCE_ID,
                ).values_list('object_id', flat=True)
            ),
            {self.product_b.pk},
        )

    def test_historical_broken_names_are_left_alone(self):
        before = self._broken_rows().count()
        self.assertEqual(before, 1)

        source = self._source(
            ProductPage.objects.filter(pk__in=[self.product_a.pk, self.product_b.pk])
        )
        patched_post_index_update(source, FakePageIndex())

        self.assertEqual(self._broken_rows().count(), before)
        self.assertTrue(
            ModelSourceIndex.objects.filter(
                index_name=self.broken_name,
                object_id=self.product_a.pk,
            ).exists()
        )

    def test_model_source_method_is_patched(self):
        self.assertTrue(
            getattr(ModelSource.post_index_update, '_shopify_stable_index_name_patched', False)
        )

"""ContentIndex rebuild (CS4)."""

import tempfile

from django.test import TestCase, override_settings

from shopify_content.content_store.backends import FilesystemContentRepository
from shopify_content.content_store.contracts import ContentRef
from shopify_content.content_store.content_index_service import rebuild_content_index
from shopify_content.models.content_index import ContentIndex, ContentReferenceIndex


class ContentIndexRebuildTests(TestCase):
    def test_rebuild_indexes_article_references(self):
        root = tempfile.mkdtemp()
        ref = ContentRef("shopify_content.articlepage", "9", "body", "en-US")
        body = '{% product handle="sku-1" %}\n'
        FilesystemContentRepository(root).write(ref, body)

        with override_settings(CONTENT_STORE_ROOT=root):
            stats = rebuild_content_index(root)
        self.assertEqual(stats["files"], 1)
        self.assertEqual(stats["references"], 1)
        row = ContentIndex.objects.get(object_id="9", field_key="body")
        self.assertEqual(row.reference_count, 1)
        self.assertEqual(ContentReferenceIndex.objects.filter(content_index=row).count(), 1)

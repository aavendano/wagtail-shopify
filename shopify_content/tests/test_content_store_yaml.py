"""PyYAML frontmatter serializer (Agent 2 / CS1)."""

from django.test import SimpleTestCase

from shopify_content.content_store.contracts import ContentRef, InvalidEditorialFrontmatter
from shopify_content.content_store.serializers import (
    FrontmatterVerbatimSerializer,
    split_frontmatter,
    checksum,
)


class YamlFrontmatterTests(SimpleTestCase):
    def setUp(self):
        self.ref = ContentRef("shopify_content.blogpage", "1", "description", "en-US")
        self.ser = FrontmatterVerbatimSerializer()

    def test_roundtrip_unicode_and_multiline(self):
        value = "line1\nline2\nunicode: café — 日本語"
        doc = self.ser.loads(self.ref, self.ser.dumps(self.ref, value, meta={}))
        self.assertEqual(doc.body, value)

    def test_roundtrip_body_with_colons(self):
        value = "key: value stays in body\nnot yaml: true"
        raw = self.ser.dumps(self.ref, value, meta={})
        doc = self.ser.loads(self.ref, raw)
        self.assertEqual(doc.body, value)

    def test_meta_list_and_mapping_via_extra_meta(self):
        raw = self.ser.dumps(
            self.ref,
            "body",
            meta={"tags": "a, b", "note": "x"},
        )
        doc = self.ser.loads(self.ref, raw)
        self.assertEqual(doc.body, "body")
        self.assertIn("tags", doc.meta)

    def test_absent_frontmatter(self):
        meta, body, had = split_frontmatter("no frontmatter\n")
        self.assertFalse(had)
        self.assertEqual(body, "no frontmatter\n")

    def test_empty_frontmatter(self):
        raw = "---\n---\nonly body"
        meta, body, had = split_frontmatter(raw)
        self.assertTrue(had)
        self.assertEqual(body, "only body")

    def test_invalid_yaml_raises(self):
        raw = "---\n: broken yaml: [\n---\nbody"
        with self.assertRaises(InvalidEditorialFrontmatter):
            split_frontmatter(raw)

    def test_checksum_from_body_only(self):
        value = "checksum target"
        doc = self.ser.loads(self.ref, self.ser.dumps(self.ref, value, meta={}))
        self.assertEqual(doc.checksum, checksum(value))

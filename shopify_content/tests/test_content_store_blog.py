"""Tests for the editorial content store vertical slice (BlogPage.description).

Covers HG-001 conditions:
  C-001 deterministic ref keyed by pk (no persisted storage key)
  C-002 checksum is integrity metadata, DB authoritative
  C-003 lossless round-trip, no HTML->Markdown transformation
  C-004 content-write workflow decoupled from Shopify publish
and INV-PERSIST-001/002/003.
"""

import tempfile
from unittest.mock import patch

from django.test import TestCase, override_settings
from wagtail.models import Locale, Page

from shopify_content.content_store.accessors import (
    mirror_editorial_content,
    read_editorial_value,
)
from shopify_content.content_store.backends import FilesystemContentRepository
from shopify_content.content_store.contracts import ContentConflict, ContentNotFound
from shopify_content.content_store.refs import ref_for, relative_path
from shopify_content.content_store.serializers import (
    FrontmatterVerbatimSerializer,
    checksum,
)
from shopify_content.models import BlogPage, ShopifyRootPage


ROUND_TRIP_SAMPLES = [
    "",
    "Plain text.",
    "<p>HTML <strong>allowed</strong> &amp; kept verbatim.</p>",
    "Multi\nline\nbody\n",
    "no trailing newline",
    "trailing newlines\n\n\n",
    "body with a --- delimiter\n---\nstill body",
    "unicode: café — 日本語 — 🎉",
    "leading\n---\n",
]


class SerializerRoundTripTests(TestCase):
    def setUp(self):
        self.ser = FrontmatterVerbatimSerializer()

    def _ref(self):
        from shopify_content.content_store.contracts import ContentRef

        return ContentRef("shopify_content.blogpage", "7", "description", "en-US")

    def test_lossless_round_trip_all_samples(self):
        ref = self._ref()
        for value in ROUND_TRIP_SAMPLES:
            raw = self.ser.dumps(ref, value, meta={})
            doc = self.ser.loads(ref, raw)
            self.assertEqual(doc.body, value, f"round-trip changed value: {value!r}")

    def test_no_markdown_transformation(self):
        ref = self._ref()
        html = "<p>Bold <b>x</b> &amp; <em>y</em></p>"
        doc = self.ser.loads(ref, self.ser.dumps(ref, html, meta={}))
        self.assertEqual(doc.body, html)  # HTML preserved, not converted

    def test_checksum_is_of_body(self):
        ref = self._ref()
        value = "integrity check"
        doc = self.ser.loads(ref, self.ser.dumps(ref, value, meta={}))
        self.assertEqual(doc.checksum, checksum(value))


class FilesystemRepositoryTests(TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.repo = FilesystemContentRepository(self.tmp)
        from shopify_content.content_store.contracts import ContentRef

        self.ref = ContentRef("shopify_content.blogpage", "42", "description", "en-US")

    def test_write_read_round_trip(self):
        value = "<p>Store me</p>\nverbatim"
        self.repo.write(self.ref, value)
        self.assertTrue(self.repo.exists(self.ref))
        self.assertEqual(self.repo.read(self.ref).body, value)

    def test_missing_raises_not_found(self):
        with self.assertRaises(ContentNotFound):
            self.repo.read(self.ref)

    def test_delete_is_idempotent(self):
        self.repo.delete(self.ref)  # no error when absent
        self.repo.write(self.ref, "x")
        self.repo.delete(self.ref)
        self.assertFalse(self.repo.exists(self.ref))

    def test_path_is_keyed_by_pk_not_slug(self):
        # Phase C topology: locale segment normalized to content form (en-us).
        rel = relative_path(self.ref).as_posix()
        self.assertEqual(rel, "en-us/shopify_content/blogpage/42/description.md")

    def test_optimistic_concurrency_conflict(self):
        self.repo.write(self.ref, "v1")
        good = checksum("v1")
        with self.assertRaises(ContentConflict):
            self.repo.write(self.ref, "v2", expected_version="stale")
        # correct expected_version succeeds
        self.repo.write(self.ref, "v2", expected_version=good)
        self.assertEqual(self.repo.read(self.ref).body, "v2")


class _BlogSliceBase:
    def _make_blog(self, description="<p>desc</p>", slug="my-blog", sync_enabled=False):
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title="Home", slug="home", locale=locale))
        root = ShopifyRootPage(title="Root", slug="root", locale=locale, sync_enabled=False)
        home.add_child(instance=root)
        blog = BlogPage(
            title="Blog",
            slug=slug,
            locale=locale,
            description=description,
            sync_enabled=sync_enabled,
        )
        root.add_child(instance=blog)
        return blog


@override_settings(CONTENT_STORE_ENABLED=True)
class MirrorContentWriteTests(_BlogSliceBase, TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.override = override_settings(CONTENT_STORE_ROOT=self.tmp)
        self.override.enable()

    def tearDown(self):
        self.override.disable()

    def test_save_mirrors_description_on_commit(self):
        with self.captureOnCommitCallbacks(execute=True):
            blog = self._make_blog(description="<p>mirror me</p>")
        repo = FilesystemContentRepository(self.tmp)
        ref = ref_for(blog, "description")
        self.assertTrue(repo.exists(ref))
        self.assertEqual(repo.read(ref).body, "<p>mirror me</p>")

    def test_mirror_write_does_not_require_publish(self):
        # No page_published / Shopify sync involved; mirroring is a content-write.
        with patch("shopify_content.sync.publish_sync.enqueue_page_outbound_sync") as mock_pub:
            with self.captureOnCommitCallbacks(execute=True):
                blog = self._make_blog(description="<p>no publish</p>")
        mock_pub.assert_not_called()
        repo = FilesystemContentRepository(self.tmp)
        self.assertEqual(repo.read(ref_for(blog, "description")).body, "<p>no publish</p>")

    def test_rename_slug_keeps_same_file_path(self):
        with self.captureOnCommitCallbacks(execute=True):
            blog = self._make_blog(slug="original")
        ref_before = relative_path(ref_for(blog, "description")).as_posix()
        blog.slug = "renamed-slug"
        with self.captureOnCommitCallbacks(execute=True):
            blog.save()
        ref_after = relative_path(ref_for(blog, "description")).as_posix()
        self.assertEqual(ref_before, ref_after)  # path keyed by pk, INV-PERSIST-001


@override_settings(CONTENT_STORE_ENABLED=True)
class ReadAccessorTests(_BlogSliceBase, TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.override = override_settings(CONTENT_STORE_ROOT=self.tmp)
        self.override.enable()

    def tearDown(self):
        self.override.disable()

    def test_read_returns_db_value_authoritative(self):
        with self.captureOnCommitCallbacks(execute=True):
            blog = self._make_blog(description="<p>db value</p>")
        self.assertEqual(read_editorial_value(blog, "description"), "<p>db value</p>")

    def test_read_returns_db_value_even_on_mirror_drift(self):
        with self.captureOnCommitCallbacks(execute=True):
            blog = self._make_blog(description="<p>db value</p>")
        # Corrupt the mirror; DB stays authoritative (C-002).
        repo = FilesystemContentRepository(self.tmp)
        repo.write(ref_for(blog, "description"), "<p>TAMPERED</p>")
        self.assertEqual(read_editorial_value(blog, "description"), "<p>db value</p>")


class DisabledFlagTests(_BlogSliceBase, TestCase):
    def test_no_mirror_when_disabled(self):
        tmp = tempfile.mkdtemp()
        with override_settings(CONTENT_STORE_ENABLED=False, CONTENT_STORE_ROOT=tmp):
            with self.captureOnCommitCallbacks(execute=True):
                blog = self._make_blog(description="<p>x</p>")
            repo = FilesystemContentRepository(tmp)
            self.assertFalse(repo.exists(ref_for(blog, "description")))
            # Read still returns DB value.
            self.assertEqual(read_editorial_value(blog, "description"), "<p>x</p>")


@override_settings(CONTENT_STORE_ENABLED=True, CELERY_TASK_ALWAYS_EAGER=True)
class PublicationUsesAccessorTests(_BlogSliceBase, TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.override = override_settings(CONTENT_STORE_ROOT=self.tmp)
        self.override.enable()

    def tearDown(self):
        self.override.disable()

    @patch("shopify_content.sync.outbound._get_shop", return_value="test.myshopify.com")
    @patch("shopify_content.sync.outbound.execute_admin_graphql")
    def test_sync_blog_pushes_identical_description_metafield(self, mock_gql, _shop):
        # blogUpdate ok, then metafieldsSet ok
        class _R:
            ok = True
            data = {"blogUpdate": {"userErrors": []}}
            error_code = None
            log_detail = ""

        mock_gql.return_value = _R()

        with self.captureOnCommitCallbacks(execute=True):
            blog = self._make_blog(description="<p>publish body</p>", sync_enabled=True)
        BlogPage.objects.filter(pk=blog.pk).update(shopify_id="gid://shopify/Blog/1")
        blog.refresh_from_db()

        from shopify_content.sync.outbound import sync_blog_page

        sync_blog_page(blog)

        # Find the metafieldsSet call carrying custom.description
        pushed = None
        for call in mock_gql.call_args_list:
            variables = call.kwargs.get("variables", {})
            for mf in variables.get("metafields", []) or []:
                if mf.get("namespace") == "custom" and mf.get("key") == "description":
                    pushed = mf["value"]
        self.assertEqual(pushed, "<p>publish body</p>")

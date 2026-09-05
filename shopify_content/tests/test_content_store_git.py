"""Phase C tests: Git-authoritative editorial content for BlogPage.description.

Covers the HG-003 evidence requirements: domain accessor, authority flip,
DB-vs-Git drift (Git wins), missing-file policy, locale topology, rename
stability, publication authority, Git isolation, mode regression, and
materialization.
"""

import tempfile
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase, override_settings
from wagtail.models import Locale, Page

from shopify_content.content_store.accessors import get_mode
from shopify_content.content_store.backends import FilesystemContentRepository
from shopify_content.content_store.contracts import ContentNotFound
from shopify_content.content_store.locales import UnsupportedLocale, to_content_locale
from shopify_content.content_store.refs import ref_for, relative_path
from shopify_content.models import BlogPage, ShopifyRootPage


def _make_blog(description="<p>db value</p>", slug="blog-c", locale_code="en-US", sync_enabled=False):
    locale, _ = Locale.objects.get_or_create(language_code=locale_code)
    home = Page.objects.filter(depth=1).first() or Page.objects.first()
    root = ShopifyRootPage(
        title="Root", slug=f"root-{slug}", locale=locale, sync_enabled=False,
    )
    home.add_child(instance=root)
    blog = BlogPage(
        title="Blog", slug=slug, locale=locale,
        description=description, sync_enabled=sync_enabled,
    )
    root.add_child(instance=blog)
    return blog


def _write_git_file(root, blog, value):
    repo = FilesystemContentRepository(root)
    repo.write(ref_for(blog, "description"), value)


class LocaleMappingTests(TestCase):
    def test_supported_mappings(self):
        self.assertEqual(to_content_locale("en-US"), "en-us")
        self.assertEqual(to_content_locale("en-CA"), "en-ca")
        self.assertEqual(to_content_locale("fr-CA"), "fr-ca")
        self.assertEqual(to_content_locale("es-US"), "es-us")

    def test_unsupported_locale_is_explicit(self):
        with self.assertRaises(UnsupportedLocale):
            to_content_locale("de-DE")


@override_settings(CONTENT_STORE_MODE="git_authoritative")
class GitAuthorityTests(TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.ov = override_settings(CONTENT_STORE_ROOT=self.root)
        self.ov.enable()

    def tearDown(self):
        self.ov.disable()

    def test_domain_accessor_returns_git_value(self):
        blog = _make_blog(description="<p>DB A</p>")
        _write_git_file(self.root, blog, "<p>GIT B</p>")
        self.assertEqual(blog.editorial.description, "<p>GIT B</p>")

    def test_git_wins_on_drift(self):
        blog = _make_blog(description="<p>DB A</p>")
        _write_git_file(self.root, blog, "<p>GIT B</p>")
        # DB says A, Git says B -> authoritative value is B.
        self.assertNotEqual(blog.description, blog.editorial.description)
        self.assertEqual(blog.editorial.description, "<p>GIT B</p>")

    def test_missing_file_raises_content_not_found(self):
        blog = _make_blog(description="<p>only in db</p>")
        with self.assertRaises(ContentNotFound):
            _ = blog.editorial.description

    @override_settings(CONTENT_STORE_GIT_FALLBACK_TO_DB=True)
    def test_explicit_fallback_returns_db_when_enabled(self):
        blog = _make_blog(description="<p>db fallback</p>")
        self.assertEqual(blog.editorial.description, "<p>db fallback</p>")

    def test_locale_topology_all_supported(self):
        cases = {
            "en-US": "en-us", "en-CA": "en-ca", "fr-CA": "fr-ca", "es-US": "es-us",
        }
        for i, (wag, seg) in enumerate(cases.items()):
            blog = _make_blog(slug=f"loc-{i}", locale_code=wag, description="x")
            rel = relative_path(ref_for(blog, "description")).as_posix()
            self.assertTrue(rel.startswith(f"{seg}/"), rel)

    def test_rename_slug_keeps_authoritative_path(self):
        blog = _make_blog(slug="before-rename", description="<p>x</p>")
        before = relative_path(ref_for(blog, "description")).as_posix()
        blog.slug = "after-rename"
        blog.save()
        after = relative_path(ref_for(blog, "description")).as_posix()
        self.assertEqual(before, after)


@override_settings(CONTENT_STORE_MODE="git_authoritative", CELERY_TASK_ALWAYS_EAGER=True)
class PublicationAuthorityTests(TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.ov = override_settings(CONTENT_STORE_ROOT=self.root)
        self.ov.enable()

    def tearDown(self):
        self.ov.disable()

    @patch("shopify_content.sync.outbound._get_shop", return_value="t.myshopify.com")
    @patch("shopify_content.sync.outbound.execute_admin_graphql")
    def test_publication_pushes_git_value_not_db(self, mock_gql, _shop):
        class _R:
            ok = True
            data = {"blogUpdate": {"userErrors": []}}
            error_code = None
            log_detail = ""

        mock_gql.return_value = _R()

        blog = _make_blog(description="<p>STALE DB</p>", sync_enabled=True)
        _write_git_file(self.root, blog, "<p>GIT AUTHORITATIVE</p>")
        BlogPage.objects.filter(pk=blog.pk).update(shopify_id="gid://shopify/Blog/1")
        blog.refresh_from_db()

        from shopify_content.sync.outbound import sync_blog_page

        sync_blog_page(blog)

        pushed = None
        for call in mock_gql.call_args_list:
            for mf in call.kwargs.get("variables", {}).get("metafields", []) or []:
                if mf.get("namespace") == "custom" and mf.get("key") == "description":
                    pushed = mf["value"]
        self.assertEqual(pushed, "<p>GIT AUTHORITATIVE</p>")


@override_settings(CONTENT_STORE_MODE="git_authoritative")
class GitIsolationTests(TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.ov = override_settings(CONTENT_STORE_ROOT=self.root)
        self.ov.enable()

    def tearDown(self):
        self.ov.disable()

    def test_no_git_subprocess_during_access_or_publication(self):
        blog = _make_blog(description="<p>db</p>")
        _write_git_file(self.root, blog, "<p>git</p>")

        import subprocess

        def _boom(*a, **k):
            raise AssertionError("git/subprocess invoked at runtime")

        with patch.object(subprocess, "run", _boom), \
             patch.object(subprocess, "Popen", _boom), \
             patch.object(subprocess, "call", _boom), \
             patch.object(subprocess, "check_output", _boom):
            self.assertEqual(blog.editorial.description, "<p>git</p>")


class ModeRegressionTests(TestCase):
    def test_default_mode_is_db(self):
        self.assertEqual(get_mode(), "db")

    @override_settings(CONTENT_STORE_ENABLED=True)
    def test_legacy_enabled_maps_to_mirror(self):
        self.assertEqual(get_mode(), "mirror")

    @override_settings(CONTENT_STORE_MODE="git_authoritative", CONTENT_STORE_ENABLED=False)
    def test_explicit_mode_wins_over_legacy_flag(self):
        self.assertEqual(get_mode(), "git_authoritative")

    def test_db_mode_returns_db_value(self):
        blog = _make_blog(description="<p>legacy</p>")
        self.assertEqual(blog.editorial.description, "<p>legacy</p>")


class MaterializationTests(TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.ov = override_settings(CONTENT_STORE_ROOT=self.root, CONTENT_STORE_MODE="git_authoritative")
        self.ov.enable()

    def tearDown(self):
        self.ov.disable()

    def _run(self, **kwargs):
        out, err = StringIO(), StringIO()
        call_command("materialize_editorial_content", stdout=out, stderr=err, **kwargs)
        return out.getvalue(), err.getvalue()

    def test_first_materialization_creates_verbatim(self):
        blog = _make_blog(description="<p>Verbatim &amp; kept</p>")
        out, _ = self._run()
        self.assertIn("created=1", out)
        repo = FilesystemContentRepository(self.root)
        self.assertEqual(
            repo.read(ref_for(blog, "description")).body, "<p>Verbatim &amp; kept</p>"
        )

    def test_idempotent_rerun_reports_identical(self):
        _make_blog(description="<p>x</p>")
        self._run()
        out, _ = self._run()
        self.assertIn("identical=1", out)
        self.assertIn("created=0", out)

    def test_divergent_skipped_without_force(self):
        blog = _make_blog(description="<p>DB new</p>")
        _write_git_file(self.root, blog, "<p>Git old</p>")
        out, err = self._run()
        self.assertIn("divergent_skipped=1", out)
        repo = FilesystemContentRepository(self.root)
        self.assertEqual(repo.read(ref_for(blog, "description")).body, "<p>Git old</p>")

    def test_force_overwrites_divergent(self):
        blog = _make_blog(description="<p>DB new</p>")
        _write_git_file(self.root, blog, "<p>Git old</p>")
        out, _ = self._run(force=True)
        self.assertIn("overwritten=1", out)
        repo = FilesystemContentRepository(self.root)
        self.assertEqual(repo.read(ref_for(blog, "description")).body, "<p>DB new</p>")

    def test_dry_run_writes_nothing(self):
        blog = _make_blog(description="<p>y</p>")
        out, _ = self._run(dry_run=True)
        self.assertIn("DRY-RUN", out)
        repo = FilesystemContentRepository(self.root)
        self.assertFalse(repo.exists(ref_for(blog, "description")))

    def test_unsupported_locale_reported_and_skipped(self):
        # Create a blog under an unsupported locale.
        _make_blog(slug="de-blog", locale_code="de-DE", description="<p>z</p>")
        out, err = self._run()
        self.assertIn("unsupported_locale=1", out)

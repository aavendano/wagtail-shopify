"""Phase D tests: Git-authoritative editorial content for GlossaryTermPage.definition.

Proves reuse of the Phase C domain/content-store architecture for a RichText
field, plus canonical Markdown (.md) persistence with verbatim (lossless)
preservation of the existing HTML source.
"""

import tempfile
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase, override_settings
from wagtail.models import Locale, Page

from shopify_content.content_store.accessors import db_text
from shopify_content.content_store.backends import FilesystemContentRepository
from shopify_content.content_store.contracts import ContentNotFound
from shopify_content.content_store.refs import ref_for, relative_path
from shopify_content.models import GlossaryTermPage, ShopifyRootPage

DEFINITION_HTML = '<p>A <b>lubricant</b> reduces friction.</p>'


def _make_term(definition=DEFINITION_HTML, term="Lubricant", slug="lubricant",
               locale_code="en-US", sync_enabled=False):
    locale, _ = Locale.objects.get_or_create(language_code=locale_code)
    home = Page.objects.filter(depth=1).first() or Page.objects.first()
    root = ShopifyRootPage(title="Glossary", slug=f"glossary-{slug}", locale=locale, sync_enabled=False)
    home.add_child(instance=root)
    term_page = GlossaryTermPage(
        title=term, term=term, slug=slug, locale=locale,
        definition=definition, sync_enabled=sync_enabled,
    )
    root.add_child(instance=term_page)
    return term_page


def _write_git(root, page, value):
    FilesystemContentRepository(root).write(ref_for(page, "definition"), value)


@override_settings(CONTENT_STORE_MODE="git_authoritative")
class GlossaryGitAuthorityTests(TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.ov = override_settings(CONTENT_STORE_ROOT=self.root)
        self.ov.enable()

    def tearDown(self):
        self.ov.disable()

    def test_domain_api_definition_returns_git_value(self):
        term = _make_term(definition="<p>DB A</p>")
        _write_git(self.root, term, "<p>GIT B</p>")
        self.assertEqual(term.editorial.definition, "<p>GIT B</p>")

    def test_git_wins_over_db(self):
        term = _make_term(definition="<p>DB A</p>")
        _write_git(self.root, term, "<p>GIT B</p>")
        self.assertEqual(db_text(term, "definition"), "<p>DB A</p>")
        self.assertNotEqual(db_text(term, "definition"), term.editorial.definition)
        self.assertEqual(term.editorial.definition, "<p>GIT B</p>")

    def test_missing_file_raises(self):
        term = _make_term()
        with self.assertRaises(ContentNotFound):
            _ = term.editorial.definition

    @override_settings(CONTENT_STORE_GIT_FALLBACK_TO_DB=True)
    def test_explicit_fallback_opt_in(self):
        term = _make_term(definition="<p>db fallback</p>")
        self.assertEqual(term.editorial.definition, "<p>db fallback</p>")

    def test_db_column_not_authoritative_but_intact(self):
        term = _make_term(definition="<p>legacy db</p>")
        _write_git(self.root, term, "<p>git wins</p>")
        # DB column still holds its value (rollback/compat) ...
        self.assertEqual(db_text(term, "definition"), "<p>legacy db</p>")
        # ... but is not authoritative.
        self.assertEqual(term.editorial.definition, "<p>git wins</p>")

    def test_locale_topology(self):
        cases = {"en-US": "en-us", "en-CA": "en-ca", "fr-CA": "fr-ca", "es-US": "es-us"}
        for i, (wag, seg) in enumerate(cases.items()):
            term = _make_term(slug=f"loc-{i}", locale_code=wag, definition="x")
            rel = relative_path(ref_for(term, "definition")).as_posix()
            self.assertEqual(rel, f"{seg}/shopify_content/glossarytermpage/{term.pk}/definition.md")

    def test_rename_slug_keeps_path(self):
        term = _make_term(slug="before")
        before = relative_path(ref_for(term, "definition")).as_posix()
        term.slug = "after"
        term.save()
        after = relative_path(ref_for(term, "definition")).as_posix()
        self.assertEqual(before, after)

    def test_generated_md_is_verbatim_and_frontmatter(self):
        term = _make_term(definition=DEFINITION_HTML)
        _write_git(self.root, term, DEFINITION_HTML)
        path = FilesystemContentRepository(self.root)._abs(ref_for(term, "definition"))
        raw = path.read_text(encoding="utf-8")
        self.assertTrue(raw.startswith("---\n"))
        self.assertIn("content_type: shopify_content.glossarytermpage", raw)
        self.assertIn("field_key: definition", raw)
        self.assertIn("locale: en-us", raw)  # content-locale form
        self.assertIn("format: markdown", raw)
        self.assertNotIn("checksum:", raw)  # no stale integrity metadata in canonical file
        # Body preserved verbatim (HTML kept losslessly).
        self.assertTrue(raw.endswith(DEFINITION_HTML))


@override_settings(CONTENT_STORE_MODE="git_authoritative", CELERY_TASK_ALWAYS_EAGER=True)
class GlossaryPublicationTests(TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.ov = override_settings(CONTENT_STORE_ROOT=self.root)
        self.ov.enable()

    def tearDown(self):
        self.ov.disable()

    def test_publication_uses_git_definition(self):
        term = _make_term(definition="<p>STALE DB</p>", sync_enabled=True)
        _write_git(self.root, term, "<p>GIT AUTHORITATIVE</p>")
        GlossaryTermPage.objects.filter(pk=term.pk).update(shopify_id="gid://shopify/Metaobject/1")
        term.refresh_from_db()

        captured = {}

        def _fake_sync(data, **kwargs):
            captured.update(data)

            class _Res:
                id = "gid://shopify/Metaobject/1"
            return _Res()

        with patch("shopify_content.sync.outbound._get_shop", return_value="t.myshopify.com"), \
             patch("shopify_content.sync.outbound.ensure_glossary_term_definition"), \
             patch("shopify_content.sync.outbound._refresh_glossary_image_mirror"), \
             patch("metaobjects.shopify_metaobjects.client.MetaobjectClient") as MockClient:
            MockClient.return_value.sync.side_effect = _fake_sync
            from shopify_content.sync.outbound import sync_glossary_term_page
            ok, msg = sync_glossary_term_page(term)

        self.assertTrue(ok, msg)
        self.assertEqual(captured.get("definition"), "<p>GIT AUTHORITATIVE</p>")


@override_settings(CONTENT_STORE_MODE="git_authoritative")
class GlossaryGitIsolationTests(TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.ov = override_settings(CONTENT_STORE_ROOT=self.root)
        self.ov.enable()

    def tearDown(self):
        self.ov.disable()

    def test_no_subprocess_during_domain_read(self):
        term = _make_term(definition="<p>db</p>")
        _write_git(self.root, term, "<p>git</p>")
        import subprocess

        def _boom(*a, **k):
            raise AssertionError("git/subprocess invoked at runtime")

        with patch.object(subprocess, "run", _boom), \
             patch.object(subprocess, "Popen", _boom), \
             patch.object(subprocess, "call", _boom), \
             patch.object(subprocess, "check_output", _boom):
            self.assertEqual(term.editorial.definition, "<p>git</p>")


class GlossaryMaterializationTests(TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.ov = override_settings(CONTENT_STORE_ROOT=self.root, CONTENT_STORE_MODE="git_authoritative")
        self.ov.enable()

    def tearDown(self):
        self.ov.disable()

    def _run(self, **kwargs):
        out, err = StringIO(), StringIO()
        call_command("materialize_editorial_content", field="definition", stdout=out, stderr=err, **kwargs)
        return out.getvalue(), err.getvalue()

    def test_create_verbatim_richtext_source(self):
        term = _make_term(definition=DEFINITION_HTML)
        out, _ = self._run()
        self.assertIn("created=1", out)
        repo = FilesystemContentRepository(self.root)
        # RichText .source preserved verbatim (HTML), no conversion.
        self.assertEqual(repo.read(ref_for(term, "definition")).body, DEFINITION_HTML)

    def test_idempotent_rerun(self):
        _make_term(definition="<p>x</p>")
        self._run()
        out, _ = self._run()
        self.assertIn("identical=1", out)
        self.assertIn("created=0", out)

    def test_divergent_without_force(self):
        term = _make_term(definition="<p>DB new</p>")
        _write_git(self.root, term, "<p>Git old</p>")
        out, _ = self._run()
        self.assertIn("divergent_skipped=1", out)
        self.assertEqual(
            FilesystemContentRepository(self.root).read(ref_for(term, "definition")).body,
            "<p>Git old</p>",
        )

    def test_force_overwrites(self):
        term = _make_term(definition="<p>DB new</p>")
        _write_git(self.root, term, "<p>Git old</p>")
        out, _ = self._run(force=True)
        self.assertIn("overwritten=1", out)
        self.assertEqual(
            FilesystemContentRepository(self.root).read(ref_for(term, "definition")).body,
            "<p>DB new</p>",
        )

    def test_dry_run(self):
        term = _make_term(definition="<p>y</p>")
        out, _ = self._run(dry_run=True)
        self.assertIn("DRY-RUN", out)
        self.assertFalse(FilesystemContentRepository(self.root).exists(ref_for(term, "definition")))

    def test_unsupported_locale(self):
        # es-ES is a valid glossary locale (locale_code -> 'es') but is NOT in
        # the content-path mapping, so materialization must skip it explicitly.
        _make_term(slug="es-es", locale_code="es-ES", definition="<p>z</p>")
        out, _ = self._run()
        self.assertIn("unsupported_locale=1", out)

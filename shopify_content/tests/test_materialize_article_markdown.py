"""Controlled StreamField -> Git body.md seeding for Phase F."""

import tempfile
from io import StringIO

from django.core.management import call_command
from django.test import TestCase, override_settings
from wagtail.models import Locale, Page

from shopify_content.content_store.backends import FilesystemContentRepository
from shopify_content.content_store.refs import ref_for
from shopify_content.models import ArticlePage, BlogPage, ShopifyRootPage


LEGACY_HTML = '<section class="legacy"><p>Existing Shopify body</p></section>'


def _make_article(*, slug="legacy", body=None):
    locale, _ = Locale.objects.get_or_create(language_code="en-US")
    home = Page.objects.filter(depth=1).first() or Page.objects.first()
    root = ShopifyRootPage(
        title=f"Root {slug}", slug=f"root-{slug}", locale=locale, sync_enabled=False
    )
    home.add_child(instance=root)
    blog = BlogPage(
        title=f"Blog {slug}",
        slug=f"blog-{slug}",
        handle=f"blog-{slug}",
        locale=locale,
        sync_enabled=False,
    )
    root.add_child(instance=blog)
    article = ArticlePage(
        title=f"Article {slug}",
        slug=slug,
        handle=slug,
        locale=locale,
        sync_enabled=False,
        body=body or [],
    )
    blog.add_child(instance=article)
    return article


class ArticleMarkdownMaterializationTests(TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.ov = override_settings(CONTENT_STORE_ROOT=self.root)
        self.ov.enable()

    def tearDown(self):
        self.ov.disable()

    def _run(self, **kwargs):
        out, err = StringIO(), StringIO()
        call_command(
            "materialize_article_markdown",
            stdout=out,
            stderr=err,
            **kwargs,
        )
        return out.getvalue(), err.getvalue()

    def test_materializes_current_rendered_html_verbatim(self):
        article = _make_article(
            slug="create",
            body=[{'type': 'html', 'value': LEGACY_HTML}],
        )
        out, _ = self._run()
        self.assertIn("created=1", out)
        value = FilesystemContentRepository(self.root).read(ref_for(article, "body")).body
        self.assertEqual(value, LEGACY_HTML)

    def test_rerun_is_idempotent(self):
        _make_article(
            slug="idem",
            body=[{'type': 'html', 'value': LEGACY_HTML}],
        )
        self._run()
        out, _ = self._run()
        self.assertIn("identical=1", out)
        self.assertIn("created=0", out)

    def test_existing_git_edit_is_not_overwritten_without_force(self):
        article = _make_article(
            slug="divergent",
            body=[{'type': 'html', 'value': LEGACY_HTML}],
        )
        repo = FilesystemContentRepository(self.root)
        repo.write(ref_for(article, "body"), "## Human Git edit")
        out, err = self._run()
        self.assertIn("divergent_skipped=1", out)
        self.assertIn("[divergent]", err)
        self.assertEqual(repo.read(ref_for(article, "body")).body, "## Human Git edit")

    def test_force_can_replace_divergent_file_during_controlled_migration(self):
        article = _make_article(
            slug="force",
            body=[{'type': 'html', 'value': LEGACY_HTML}],
        )
        repo = FilesystemContentRepository(self.root)
        repo.write(ref_for(article, "body"), "old")
        out, _ = self._run(force=True)
        self.assertIn("overwritten=1", out)
        self.assertEqual(repo.read(ref_for(article, "body")).body, LEGACY_HTML)

    def test_empty_article_still_gets_authoritative_file(self):
        article = _make_article(slug="empty", body=[])
        self._run()
        repo = FilesystemContentRepository(self.root)
        self.assertTrue(repo.exists(ref_for(article, "body")))
        self.assertEqual(repo.read(ref_for(article, "body")).body, "")

    def test_dry_run_does_not_create_file(self):
        article = _make_article(
            slug="dry",
            body=[{'type': 'html', 'value': LEGACY_HTML}],
        )
        out, _ = self._run(dry_run=True)
        self.assertIn("DRY-RUN", out)
        self.assertFalse(FilesystemContentRepository(self.root).exists(ref_for(article, "body")))

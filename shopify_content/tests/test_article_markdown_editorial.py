"""Phase F: Git-native Markdown authority for ArticlePage.body."""

import tempfile
from types import SimpleNamespace
from unittest.mock import patch

from django.test import SimpleTestCase, TestCase, override_settings
from wagtail.models import Locale, Page

from shopify_content.content_store.backends import FilesystemContentRepository
from shopify_content.content_store.contracts import ContentNotFound
from shopify_content.content_store.markdown_renderer import (
    MarkdownRenderError,
    render_editorial_markdown,
)
from shopify_content.content_store.refs import ref_for, relative_path
from shopify_content.models import ArticlePage, BlogPage, ShopifyRootPage
from shopify_content.sync.article_markdown import article_body_html, sync_article_page


ARTICLE_MD = """## Choosing a vibrator

Start with **comfort** and adjust gradually.

{% product handle="satisfyer-pro-2" label="Satisfyer Pro 2" %}

{% callout type="tip" title="Tip" %}
Use plenty of water-based lubricant.
{% /callout %}
"""


def _make_article(*, slug="guide", locale_code="en-US", shopify_id="gid://shopify/Article/1"):
    locale, _ = Locale.objects.get_or_create(language_code=locale_code)
    home = Page.objects.filter(depth=1).first() or Page.objects.first()
    root = ShopifyRootPage(
        title=f"Blogs root {slug}",
        slug=f"blogs-{slug}",
        locale=locale,
        sync_enabled=False,
    )
    home.add_child(instance=root)
    blog = BlogPage(
        title=f"Blog {slug}",
        slug=f"blog-{slug}",
        handle=f"blog-{slug}",
        locale=locale,
        shopify_id="gid://shopify/Blog/1",
        sync_enabled=False,
    )
    root.add_child(instance=blog)
    article = ArticlePage(
        title="Guide",
        slug=slug,
        handle=slug,
        locale=locale,
        shopify_id=shopify_id,
        sync_enabled=True,
        author="Editorial",
        summary="Summary",
    )
    blog.add_child(instance=article)
    return article


def _write_git(root, page, source=ARTICLE_MD):
    FilesystemContentRepository(root).write(ref_for(page, "body"), source)


class EditorialMarkdownRendererTests(SimpleTestCase):
    def test_standard_markdown_and_product_component(self):
        html = render_editorial_markdown(ARTICLE_MD)
        self.assertIn("<h2>Choosing a vibrator</h2>", html)
        self.assertIn("<strong>comfort</strong>", html)
        self.assertIn('data-component="product"', html)
        self.assertIn('/products/satisfyer-pro-2', html)
        self.assertIn('class="plt-callout plt-callout--tip"', html)
        self.assertIn("water-based lubricant", html)

    def test_collection_and_internal_page_components(self):
        source = """{% collection handle="vibrators" label="Shop Vibrators" %}

{% page path="/pages/glossary/lubricant" label="Lubricant" %}
"""
        html = render_editorial_markdown(source)
        self.assertIn('/collections/vibrators', html)
        self.assertIn('/pages/glossary/lubricant', html)
        self.assertIn('data-component="collection"', html)
        self.assertIn('data-component="page"', html)

    def test_component_labels_are_html_escaped(self):
        html = render_editorial_markdown(
            '{% product handle="safe-handle" label="<script>alert(1)</script>" %}'
        )
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)

    def test_invalid_or_unknown_directive_fails_explicitly(self):
        with self.assertRaises(MarkdownRenderError):
            render_editorial_markdown('{% product handle="../bad" %}')
        with self.assertRaises(MarkdownRenderError):
            render_editorial_markdown('{% carousel id="x" %}')

    def test_unclosed_callout_fails(self):
        with self.assertRaises(MarkdownRenderError):
            render_editorial_markdown('{% callout type="tip" %}\nMissing end')


@override_settings(CONTENT_STORE_MODE="git_authoritative")
class ArticleGitAuthorityTests(TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.ov = override_settings(CONTENT_STORE_ROOT=self.root)
        self.ov.enable()

    def tearDown(self):
        self.ov.disable()

    def test_domain_api_returns_markdown_source(self):
        article = _make_article(slug="domain")
        _write_git(self.root, article)
        self.assertEqual(article.editorial.body, ARTICLE_MD)

    def test_body_path_is_locale_and_pk_stable(self):
        article = _make_article(slug="before")
        before = relative_path(ref_for(article, "body")).as_posix()
        self.assertEqual(
            before,
            f"en-us/shopify_content/articlepage/{article.pk}/body.md",
        )
        article.slug = "after"
        article.save()
        after = relative_path(ref_for(article, "body")).as_posix()
        self.assertEqual(before, after)

    def test_missing_file_has_no_streamfield_fallback(self):
        article = _make_article(slug="missing")
        with self.assertRaises(ContentNotFound):
            _ = article.editorial.body

    @override_settings(CONTENT_STORE_GIT_FALLBACK_TO_DB=True)
    def test_global_db_fallback_does_not_apply_to_git_native_body(self):
        article = _make_article(slug="no-fallback")
        with self.assertRaises(ContentNotFound):
            _ = article.editorial.body

    def test_article_body_html_renders_authoritative_markdown(self):
        article = _make_article(slug="render")
        _write_git(self.root, article)
        rendered = article_body_html(article)
        self.assertIn("<h2>Choosing a vibrator</h2>", rendered)
        self.assertIn('/products/satisfyer-pro-2', rendered)

    def test_shopify_mutation_receives_rendered_git_body(self):
        article = _make_article(slug="publish")
        _write_git(self.root, article)

        result = SimpleNamespace(
            ok=True,
            data={"articleUpdate": {"userErrors": [], "article": {}}},
            error_code=None,
            log_detail="",
            raw=None,
        )

        with patch(
            "shopify_content.sync.article_markdown.outbound._get_shop",
            return_value="example.myshopify.com",
        ), patch(
            "shopify_content.sync.article_markdown.outbound.execute_admin_graphql",
            return_value=result,
        ) as graphql, patch(
            "shopify_content.sync.article_markdown.outbound._push_seo_metafields"
        ), patch(
            "shopify_content.sync.article_markdown.outbound._push_metafields"
        ), patch(
            "shopify_content.sync.article_markdown.outbound._push_faq_metafield"
        ), patch(
            "shopify_content.sync.article_markdown.outbound._push_internal_links_metafield"
        ), patch(
            "shopify_content.sync.article_markdown.outbound._push_native_reference_metafields"
        ), patch(
            "shopify_content.sync.article_markdown.outbound._push_available_locales_metafield"
        ), patch(
            "shopify_content.sync.article_markdown.outbound._register_shopify_translations"
        ), patch(
            "shopify_content.sync.article_markdown.outbound._mark_synced"
        ), patch(
            "shopify_content.sync.article_markdown.outbound._queue_index_sync_after_content_sync"
        ):
            ok = sync_article_page(article)

        self.assertTrue(ok)
        variables = graphql.call_args.kwargs["variables"]
        body = variables["article"]["body"]
        self.assertIn("<h2>Choosing a vibrator</h2>", body)
        self.assertIn('data-component="product"', body)

    def test_missing_git_body_aborts_before_shopify_request(self):
        article = _make_article(slug="abort")
        with patch(
            "shopify_content.sync.article_markdown.outbound._get_shop",
            return_value="example.myshopify.com",
        ), patch(
            "shopify_content.sync.article_markdown.outbound.execute_admin_graphql"
        ) as graphql:
            with self.assertRaises(ContentNotFound):
                sync_article_page(article)
        graphql.assert_not_called()

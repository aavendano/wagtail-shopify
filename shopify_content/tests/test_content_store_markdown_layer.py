"""Markdown package: parser, references, assets, security (CS2–CS3)."""

from django.test import SimpleTestCase

from shopify_content.content_store.markdown.assets import AssetRef, PassthroughAssetResolver
from shopify_content.content_store.markdown.errors import MarkdownRenderError
from shopify_content.content_store.markdown.references import (
    ContentReference,
    DefaultReferenceResolver,
    extract_references,
)
from shopify_content.content_store.markdown.renderer import render_editorial_markdown
from shopify_content.content_store.markdown.security import RenderProfile, sanitize_html_for_profile


class MarkdownParserTests(SimpleTestCase):
    def test_tokenize_returns_tokens(self):
        from shopify_content.content_store.markdown.parser import tokenize

        tokens = tokenize("## Title\n\nParagraph.")
        self.assertGreater(len(tokens), 0)


class ReferenceTests(SimpleTestCase):
    def test_product_handle_directive(self):
        refs = extract_references('{% product handle="foo-bar" label="Foo" %}')
        self.assertEqual(refs[0], ContentReference("product", "foo-bar", "Foo"))

    def test_ref_attribute_future_form(self):
        refs = extract_references('{% product ref="product:my-handle" label="X" %}')
        self.assertEqual(refs[0].identifier, "my-handle")

    def test_asset_markdown_image(self):
        refs = extract_references('![alt](asset:hero-image-1)')
        self.assertEqual(refs[0].ref_type, "asset")
        self.assertEqual(refs[0].identifier, "hero-image-1")

    def test_default_resolver_urls(self):
        resolver = DefaultReferenceResolver()
        url = resolver.resolve(ContentReference("product", "h1"))
        self.assertEqual(url, "/products/h1")


class AssetResolverTests(SimpleTestCase):
    def test_passthrough_asset_url(self):
        asset = AssetRef.parse("asset:stable-1")
        self.assertIsNotNone(asset)
        url = PassthroughAssetResolver().url_for(asset)
        self.assertEqual(url, "/cdn/assets/stable-1")


class SecurityProfileTests(SimpleTestCase):
    def test_restricted_strips_script(self):
        dirty = '<p>ok</p><script>alert(1)</script>'
        clean = sanitize_html_for_profile(dirty, RenderProfile.RESTRICTED)
        self.assertNotIn("script", clean)

    def test_trusted_keeps_html(self):
        html = "<p onclick=\"x()\">x</p>"
        self.assertEqual(sanitize_html_for_profile(html, RenderProfile.TRUSTED_EDITORIAL), html)

    def test_ref_product_render(self):
        html = render_editorial_markdown(
            '{% product ref="product:safe-handle" label="Safe" %}'
        )
        self.assertIn("/products/safe-handle", html)

    def test_unknown_directive_raises(self):
        with self.assertRaises(MarkdownRenderError):
            render_editorial_markdown("{% unknown x=1 %}")

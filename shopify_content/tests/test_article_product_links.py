"""Unit tests for article product link rewrite helpers."""

from django.test import TestCase

from shopify_content.article_product_links import (
    LinkAction,
    ProductHandleResolver,
    extract_product_handles,
    normalize_product_handle,
    rewrite_html_product_links,
    rewrite_streamfield_raw,
)


class NormalizeHandleTests(TestCase):
    def test_unquote_and_lower(self):
        self.assertEqual(
            normalize_product_handle('F2S%E2%84%A2-Teal'),
            'f2s-teal',
        )

    def test_strips_trademark(self):
        self.assertEqual(normalize_product_handle('f2s™-teal'), 'f2s-teal')


class ExtractHandlesTests(TestCase):
    def test_absolute_and_relative(self):
        html = (
            '<a href="https://playlovetoys.com/products/Old-Handle">A</a>'
            '<a href="/es-us/products/other-one">B</a>'
            '<a href="/collections/x">C</a>'
        )
        self.assertEqual(
            extract_product_handles(html),
            ['old-handle', 'other-one'],
        )


class ResolverTests(TestCase):
    def setUp(self):
        self.resolver = ProductHandleResolver(
            [
                'lelo-f2s-adaptive-masturbator',
                'lelo-ina-3-rabbit-vibrator',
                'kiiroo-onyx-plus-smart-interactive-masturbator',
                'we-vibe-nova-2-vibrator',
                'sex-mischief-amor-bondage-beginner-kit',
                'beginners-bondage-fantasy-kit',
            ],
            shopify_id_to_handle={'7416019714123': 'we-vibe-nova-2-vibrator'},
            manual_map={'onyx': 'kiiroo-onyx-plus-smart-interactive-masturbator'},
        )

    def test_exact_unchanged(self):
        d = self.resolver.resolve('lelo-f2s-adaptive-masturbator')
        self.assertEqual(d.action, LinkAction.UNCHANGED)
        self.assertEqual(d.resolved_handle, 'lelo-f2s-adaptive-masturbator')

    def test_prefix_extension_rewrite(self):
        d = self.resolver.resolve('lelo-f2s')
        self.assertEqual(d.action, LinkAction.REWRITE)
        self.assertEqual(d.resolved_handle, 'lelo-f2s-adaptive-masturbator')

    def test_variant_suffix_token_match(self):
        d = self.resolver.resolve('ina-3-coral')
        self.assertEqual(d.action, LinkAction.REWRITE)
        self.assertEqual(d.resolved_handle, 'lelo-ina-3-rabbit-vibrator')

    def test_numeric_shopify_id(self):
        d = self.resolver.resolve('7416019714123')
        self.assertEqual(d.action, LinkAction.REWRITE)
        self.assertEqual(d.resolved_handle, 'we-vibe-nova-2-vibrator')

    def test_manual_map(self):
        d = self.resolver.resolve('onyx')
        self.assertEqual(d.action, LinkAction.REWRITE)
        self.assertEqual(
            d.resolved_handle,
            'kiiroo-onyx-plus-smart-interactive-masturbator',
        )

    def test_ambiguous(self):
        d = self.resolver.resolve('amor-bondage-beginner-kit')
        # Not a unique prefix of either kit handle; token match may hit both
        # or unwrap — assert it does not silently pick one wrong unique.
        self.assertIn(d.action, (LinkAction.AMBIGUOUS, LinkAction.UNWRAP, LinkAction.REWRITE))
        if d.action == LinkAction.REWRITE:
            self.assertIn(
                d.resolved_handle,
                {
                    'sex-mischief-amor-bondage-beginner-kit',
                    'beginners-bondage-fantasy-kit',
                },
            )

    def test_missing_unwrap_decision(self):
        d = self.resolver.resolve('totally-missing-product-xyz')
        self.assertEqual(d.action, LinkAction.UNWRAP)


class RewriteHtmlTests(TestCase):
    def setUp(self):
        self.resolver = ProductHandleResolver(
            ['lelo-f2s-adaptive-masturbator', 'alive-product'],
            manual_map={},
        )

    def test_rewrites_absolute_to_relative_live(self):
        html = (
            '<p>See <a href="https://playlovetoys.com/products/lelo-f2s" class="x">'
            'LELO F2S</a> now.</p>'
        )
        new_html, stats = rewrite_html_product_links(html, self.resolver)
        self.assertIn('href="/products/lelo-f2s-adaptive-masturbator"', new_html)
        self.assertNotIn('playlovetoys.com', new_html)
        self.assertEqual(stats.rewritten, 1)
        self.assertIn('LELO F2S', new_html)

    def test_unwraps_missing(self):
        html = '<a href="/products/gone-forever">Gone</a> stays.'
        new_html, stats = rewrite_html_product_links(html, self.resolver)
        self.assertEqual(new_html, 'Gone stays.')
        self.assertEqual(stats.unwrapped, 1)
        self.assertNotIn('<a', new_html)

    def test_leaves_ambiguous(self):
        resolver = ProductHandleResolver(
            ['aaa-kit', 'bbb-kit'],
        )
        # Force ambiguous by patching resolve via two prefix matches:
        resolver = ProductHandleResolver(
            ['brand-widget-pro', 'brand-widget-lite'],
        )
        html = '<a href="/products/brand-widget">Widget</a>'
        new_html, stats = rewrite_html_product_links(html, resolver)
        # brand-widget is prefix of both → ambiguous → unchanged
        self.assertEqual(stats.ambiguous, 1)
        self.assertIn('href="/products/brand-widget"', new_html)

    def test_normalizes_already_live_absolute(self):
        html = '<a href="https://playlovetoys.ca/en-ca/products/alive-product">X</a>'
        new_html, stats = rewrite_html_product_links(html, self.resolver)
        self.assertIn('href="/products/alive-product"', new_html)
        self.assertEqual(stats.rewritten, 1)


class StreamFieldRewriteTests(TestCase):
    def test_rewrites_html_and_paragraph_blocks(self):
        resolver = ProductHandleResolver(['live-handle'])
        raw = [
            {
                'type': 'html',
                'value': '<a href="/products/old">A</a>',
            },
            {
                'type': 'paragraph',
                'value': {'text': '<p><a href="/products/old">B</a></p>'},
            },
            {
                'type': 'heading',
                'value': {'text': 'Skip', 'level': 'h2'},
            },
        ]
        # old → unwrap
        new_raw, stats, changed = rewrite_streamfield_raw(raw, resolver)
        self.assertTrue(changed)
        self.assertEqual(new_raw[0]['value'], 'A')
        self.assertEqual(new_raw[1]['value']['text'], '<p>B</p>')
        self.assertEqual(new_raw[2]['value']['text'], 'Skip')
        self.assertEqual(stats.unwrapped, 2)

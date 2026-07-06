from unittest.mock import MagicMock, patch

from django.test import TestCase
from wagtail.models import Locale, Page

from core.models import ShopConfig
from shopify_content.models import GlossaryTermPage, ProductPage, ShopifyRootPage
from shopify_content.models.blog import ArticlePage, BlogPage
from shopify_content.sync.outbound import (
    _glossary_term_definition,
    ensure_glossary_term_definition,
    sync_glossary_term_page,
)
from metaobjects.shopify_metaobjects.metaobject import Metaobject


class GlossaryTermDefinitionTests(TestCase):
    def test_definition_includes_fields_and_renderable_keys(self):
        spec = _glossary_term_definition()
        field_keys = {field.key for field in spec.fields}
        self.assertEqual(spec.display_name_field, 'term')
        self.assertEqual(
            field_keys,
            {
                'term', 'definition', 'image', 'locale', 'meta_title', 'meta_description',
                'related_links', 'external_links',
                'synonyms', 'same_as',
                'related_products', 'related_collections', 'related_articles',
            },
        )

    def test_definition_includes_glossary_terms_field_with_gid(self):
        gid = 'gid://shopify/MetaobjectDefinition/99'
        spec = _glossary_term_definition(gid)
        field_keys = {field.key for field in spec.fields}
        self.assertIn('related_glossary_terms', field_keys)

        renderable = spec.capabilities['renderable']['data']
        self.assertEqual(renderable['metaTitleKey'], 'meta_title')
        self.assertEqual(renderable['metaDescriptionKey'], 'meta_description')

        online_store = spec.capabilities['onlineStore']['data']
        self.assertEqual(online_store['urlHandle'], 'glossary')

        payload = spec.to_shopify_input()
        renderable_data = payload['capabilities']['renderable']['data']
        self.assertEqual(renderable_data['metaTitleKey'], 'meta_title')
        self.assertEqual(renderable_data['metaDescriptionKey'], 'meta_description')

    def test_native_reference_fields_include_metaobject_validation(self):
        gid = 'gid://shopify/MetaobjectDefinition/99'
        fields = _glossary_term_definition(gid).fields
        glossary_field = next(f for f in fields if f.key == 'related_glossary_terms')
        self.assertEqual(glossary_field.type, 'list.metaobject_reference')
        self.assertEqual(
            glossary_field.validations,
            [{'name': 'metaobject_definition_id', 'value': gid}],
        )

    def test_native_reference_fields_include_article_reference(self):
        fields = _glossary_term_definition().fields
        article_field = next(f for f in fields if f.key == 'related_articles')
        self.assertEqual(article_field.type, 'list.article_reference')

    def test_definition_includes_image_field_with_image_validation(self):
        fields = _glossary_term_definition().fields
        image_field = next(f for f in fields if f.key == 'image')
        self.assertEqual(image_field.type, 'file_reference')
        self.assertEqual(
            image_field.validations,
            [{'name': 'file_type_options', 'value': ['Image']}],
        )
        payload = image_field.to_shopify_input()
        self.assertEqual(
            payload['validations'],
            [{'name': 'file_type_options', 'value': '["Image"]'}],
        )


class EnsureGlossaryTermDefinitionTests(TestCase):
    @patch('shopify_content.sync.outbound._glossary_term_definition')
    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient.get_definition')
    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient.ensure_definition')
    def test_two_pass_ensure_adds_self_reference_after_create(
        self, mock_ensure, mock_get_definition, mock_spec_fn,
    ):
        from metaobjects.shopify_metaobjects.definition import MetaobjectDefinitionSpec

        mock_get_definition.return_value = None
        created = MetaobjectDefinitionSpec(
            type='glossary_term',
            name='Glossary Term',
            description='',
            fields=[],
            id='gid://shopify/MetaobjectDefinition/1',
        )
        mock_ensure.side_effect = [created, created]
        mock_spec_fn.side_effect = (
            lambda gid=None, include_self_reference=True: MetaobjectDefinitionSpec(
                type='glossary_term',
                name='Glossary Term',
                description='',
                fields=[],
                id=gid,
            )
        )

        client = MagicMock()
        client.get_definition = mock_get_definition
        client.ensure_definition = mock_ensure

        result = ensure_glossary_term_definition(client)

        self.assertEqual(result.id, 'gid://shopify/MetaobjectDefinition/1')
        self.assertEqual(mock_ensure.call_count, 2)
        mock_spec_fn.assert_any_call(None, include_self_reference=False)
        mock_spec_fn.assert_any_call(
            'gid://shopify/MetaobjectDefinition/1',
            include_self_reference=True,
        )


class SyncGlossaryTermPageTests(TestCase):
    def setUp(self):
        ShopConfig.objects.create(shop='test-shop.myshopify.com', access_token='tok')
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.parent = ShopifyRootPage(title='Glossary', slug='glossary', locale=locale)
        home.add_child(instance=self.parent)
        self.parent.save_revision().publish()

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_sync_includes_core_fields(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.sync.return_value = Metaobject(
            type='glossary_term',
            handle='vibrator',
            id='gid://shopify/Metaobject/1',
        )
        mock_client_cls.return_value = mock_client

        page = GlossaryTermPage(
            title='Vibrator',
            term='Vibrator',
            definition='<p>A device that vibrates.</p>',
            shopify_image_id='gid://shopify/MediaImage/10',
            locale_code='en',
            slug='vibrator',
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()

        success, message = sync_glossary_term_page(page)

        self.assertTrue(success)
        self.assertIn('successfully', message)
        mock_client.sync.assert_called_once()
        data = mock_client.sync.call_args.args[0]
        self.assertEqual(data['term'], 'Vibrator')
        self.assertEqual(data['locale'], 'en')
        self.assertEqual(data['definition'], '<p>A device that vibrates.</p>')
        self.assertEqual(data['image'], 'gid://shopify/MediaImage/10')
        self.assertEqual(data['meta_title'], 'Vibrator')
        self.assertEqual(data['meta_description'], 'A device that vibrates.')

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_sync_uses_explicit_seo_fields(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.sync.return_value = Metaobject(
            type='glossary_term',
            handle='vibrator',
            id='gid://shopify/Metaobject/6',
        )
        mock_client_cls.return_value = mock_client

        page = GlossaryTermPage(
            title='Vibrator',
            term='Vibrator',
            definition='<p>A device that vibrates.</p>',
            seo_title='Best Vibrator Guide',
            search_description='Learn about vibrators.',
            locale_code='en',
            slug='vibrator',
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()

        success, _ = sync_glossary_term_page(page)

        self.assertTrue(success)
        data = mock_client.sync.call_args.args[0]
        self.assertEqual(data['meta_title'], 'Best Vibrator Guide')
        self.assertEqual(data['meta_description'], 'Learn about vibrators.')

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_handle_defaults_to_slugified_term(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.sync.return_value = Metaobject(
            type='glossary_term',
            handle='satisfyer-pro-2',
            id='gid://shopify/Metaobject/2',
        )
        mock_client_cls.return_value = mock_client

        page = GlossaryTermPage(
            title='Satisfyer Pro 2',
            term='Satisfyer Pro 2',
            locale_code='en',
            slug='satisfyer-pro-2',
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()

        success, _ = sync_glossary_term_page(page)

        self.assertTrue(success)
        data = mock_client.sync.call_args.args[0]
        self.assertEqual(data['handle'], 'satisfyer-pro-2')

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_sync_includes_json_links_when_present(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.sync.return_value = Metaobject(
            type='glossary_term',
            handle='term-with-links',
            id='gid://shopify/Metaobject/3',
        )
        mock_client_cls.return_value = mock_client

        related_links = [{
            'type': 'product',
            'handle': 'satisfyer-pro-2',
            'label': 'Satisfyer Pro 2',
        }]
        external_links = [{
            'url': 'https://example.com/fda',
            'label': 'FDA Guidelines on Materials',
        }]
        page = GlossaryTermPage(
            title='Term With Links',
            term='Term With Links',
            locale_code='es',
            related_links=related_links,
            external_links=external_links,
            slug='term-with-links',
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()

        success, _ = sync_glossary_term_page(page)

        self.assertTrue(success)
        data = mock_client.sync.call_args.args[0]
        self.assertEqual(data['related_links'], related_links)
        self.assertEqual(data['external_links'], external_links)

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_sync_includes_synonyms_and_same_as_when_present(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.sync.return_value = Metaobject(
            type='glossary_term',
            handle='vibrator',
            id='gid://shopify/Metaobject/5',
        )
        mock_client_cls.return_value = mock_client

        synonyms = ['Vibrator', 'Personal massager']
        same_as = ['https://en.wikipedia.org/wiki/Vibrator_(sex_toy)']
        page = GlossaryTermPage(
            title='Vibrator',
            term='Vibrator',
            locale_code='en',
            synonyms=synonyms,
            same_as=same_as,
            slug='vibrator',
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()

        success, _ = sync_glossary_term_page(page)

        self.assertTrue(success)
        data = mock_client.sync.call_args.args[0]
        self.assertEqual(data['synonyms'], synonyms)
        self.assertEqual(data['same_as'], same_as)

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_sync_includes_native_reference_fields_from_fk(self, mock_client_cls):
        locale = Locale.get_default()
        root = self.parent.get_parent()
        target = ProductPage(
            title='Linked',
            slug='linked',
            handle='linked',
            shopify_id='gid://shopify/Product/99',
            locale=locale,
        )
        root.add_child(instance=target)
        target.save_revision().publish()

        blog = BlogPage(
            title='Linked Blog',
            slug='linked-blog',
            handle='linked-blog',
            shopify_id='gid://shopify/Blog/99',
            locale=locale,
        )
        root.add_child(instance=blog)
        blog.save_revision().publish()

        article = ArticlePage(
            title='Linked Article',
            slug='linked-article',
            handle='linked-article',
            shopify_id='gid://shopify/Article/99',
            locale=locale,
        )
        blog.add_child(instance=article)
        article.save_revision().publish()

        mock_client = MagicMock()
        mock_client.sync.return_value = Metaobject(
            type='glossary_term',
            handle='vibrator',
            id='gid://shopify/Metaobject/1',
        )
        mock_client_cls.return_value = mock_client

        page = GlossaryTermPage(
            title='Vibrator',
            term='Vibrator',
            slug='vibrator',
            locale=locale,
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()
        page.related_products.create(related_page=target, is_auto=False, sort_order=0)
        page.related_articles.create(related_page=article, is_auto=False, sort_order=1)

        success, _ = sync_glossary_term_page(page)

        self.assertTrue(success)
        data = mock_client.sync.call_args.args[0]
        self.assertEqual(data['related_products'], ['gid://shopify/Product/99'])
        self.assertEqual(data['related_articles'], ['gid://shopify/Article/99'])

    @patch('metaobjects.shopify_metaobjects.client.MetaobjectClient')
    def test_sync_skips_empty_json_fields(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.sync.return_value = Metaobject(
            type='glossary_term',
            handle='plain-term',
            id='gid://shopify/Metaobject/4',
        )
        mock_client_cls.return_value = mock_client

        page = GlossaryTermPage(
            title='Plain Term',
            term='Plain Term',
            locale_code='fr',
            slug='plain-term',
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()

        success, _ = sync_glossary_term_page(page)

        self.assertTrue(success)
        data = mock_client.sync.call_args.args[0]
        self.assertNotIn('related_links', data)
        self.assertNotIn('external_links', data)
        self.assertNotIn('synonyms', data)
        self.assertNotIn('same_as', data)

    def test_sync_aborts_without_term(self):
        page = GlossaryTermPage(
            title='Placeholder',
            term='Placeholder',
            slug='empty-term',
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()
        page.term = ''

        success, message = sync_glossary_term_page(page)

        self.assertFalse(success)
        self.assertIn('term is required', message)

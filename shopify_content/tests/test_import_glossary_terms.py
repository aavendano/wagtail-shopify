from unittest.mock import patch

from django.test import TestCase, override_settings
from wagtail.models import Locale, Page

from core.models import ShopConfig
from shopify_content.models import GlossaryTermPage, ShopifyRootPage
from shopify_content.sync.inbound import import_glossary_terms


def _make_glossary_node(
    gid,
    handle,
    term,
    *,
    locale='en',
    image_url='https://cdn.shopify.com/lingerie.jpg',
    alt_text='Lingerie alt',
    publishable_status='ACTIVE',
):
    return {
        'id': gid,
        'handle': handle,
        'capabilities': {'publishable': {'status': publishable_status}},
        'fields': [
            {'key': 'term', 'value': term},
            {'key': 'locale', 'value': locale},
            {
                'key': 'definition',
                'value': '{"type":"root","children":[{"type":"paragraph","children":[{"type":"text","value":"Shopify definition"}]}]}',
            },
            {
                'key': 'image',
                'value': 'gid://shopify/MediaImage/99',
                'reference': {
                    'id': 'gid://shopify/MediaImage/99',
                    'image': {'url': image_url, 'altText': alt_text},
                },
            },
        ],
    }


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class ImportGlossaryTermsTests(TestCase):
    def setUp(self):
        ShopConfig.objects.create(
            shop='test-shop.myshopify.com',
            access_token='tok',
        )
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.parent = ShopifyRootPage(title='Glossary', slug='glossary', locale=locale)
        home.add_child(instance=self.parent)
        self.parent.save_revision().publish()

    @patch('shopify_content.sync.inbound._paginate')
    @patch('shopify_content.tasks.sync_glossary_index_task.delay')
    def test_import_glossary_terms_creates_new(self, mock_index_delay, mock_paginate):
        gid = 'gid://shopify/Metaobject/100'
        mock_paginate.return_value = iter([
            _make_glossary_node(gid, 'lingerie', 'Lingerie'),
        ])

        stats = import_glossary_terms(
            'test-shop.myshopify.com',
            self.parent,
            queue_index_rebuild=False,
        )

        self.assertEqual(stats['created'], 1)
        self.assertEqual(stats['updated'], 0)
        self.assertEqual(stats['skipped'], 0)
        self.assertEqual(stats['errors'], 0)

        page = GlossaryTermPage.objects.get(shopify_id=gid)
        self.assertEqual(page.term, 'Lingerie')
        self.assertEqual(page.handle, 'lingerie')
        self.assertEqual(page.image_url, 'https://cdn.shopify.com/lingerie.jpg')
        self.assertEqual(page.image_alt_text, 'Lingerie alt')
        self.assertIn('<p>Shopify definition</p>', page.definition)
        mock_index_delay.assert_not_called()

    @patch('shopify_content.sync.inbound._paginate')
    def test_import_glossary_terms_updates_image_only(self, mock_paginate):
        gid = 'gid://shopify/Metaobject/200'
        existing = GlossaryTermPage(
            title='Lingerie',
            term='Lingerie',
            locale_code='en',
            shopify_id=gid,
            handle='lingerie',
            slug='lingerie',
            definition='<p>Wagtail definition</p>',
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=existing)
        existing.save_revision().publish()

        mock_paginate.return_value = iter([
            _make_glossary_node(
                gid,
                'lingerie',
                'Lingerie Renamed',
                image_url='https://cdn.shopify.com/new.jpg',
                alt_text='New alt',
            ),
        ])

        stats = import_glossary_terms(
            'test-shop.myshopify.com',
            self.parent,
            queue_index_rebuild=False,
        )

        self.assertEqual(stats['created'], 0)
        self.assertEqual(stats['updated'], 1)
        self.assertEqual(stats['skipped'], 0)

        page = GlossaryTermPage.objects.get(shopify_id=gid)
        self.assertEqual(page.term, 'Lingerie')
        self.assertEqual(page.definition, '<p>Wagtail definition</p>')
        self.assertEqual(page.image_url, 'https://cdn.shopify.com/new.jpg')
        self.assertEqual(page.image_alt_text, 'New alt')
        self.assertEqual(page.shopify_image_id, 'gid://shopify/MediaImage/99')

    @patch('shopify_content.sync.inbound._paginate')
    def test_import_glossary_terms_skips_existing_when_new_only(self, mock_paginate):
        gid = 'gid://shopify/Metaobject/300'
        existing = GlossaryTermPage(
            title='Existing',
            term='Existing',
            locale_code='en',
            shopify_id=gid,
            handle='existing',
            slug='existing',
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=existing)
        existing.save_revision().publish()

        mock_paginate.return_value = iter([
            _make_glossary_node(
                gid,
                'existing',
                'Existing',
                image_url='https://cdn.shopify.com/should-not-apply.jpg',
            ),
        ])

        stats = import_glossary_terms(
            'test-shop.myshopify.com',
            self.parent,
            new_only=True,
            queue_index_rebuild=False,
        )

        self.assertEqual(stats['created'], 0)
        self.assertEqual(stats['updated'], 0)
        self.assertEqual(stats['skipped'], 1)

        page = GlossaryTermPage.objects.get(shopify_id=gid)
        self.assertEqual(page.image_url, '')

    @patch('shopify_content.sync.inbound._paginate')
    def test_import_glossary_terms_matches_existing_by_slug_when_shopify_id_stale(self, mock_paginate):
        old_gid = 'gid://shopify/Metaobject/240123576395'
        new_gid = 'gid://shopify/Metaobject/240247701579'
        existing = GlossaryTermPage(
            title='Lenceria',
            term='Lenceria',
            locale_code='en',
            shopify_id=old_gid,
            handle='lenceria',
            slug='lenceria',
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=existing)
        existing.save_revision().publish()

        mock_paginate.return_value = iter([
            _make_glossary_node(new_gid, 'lenceria', 'Lenceria'),
        ])

        stats = import_glossary_terms(
            'test-shop.myshopify.com',
            self.parent,
            queue_index_rebuild=False,
        )

        self.assertEqual(stats['created'], 0)
        self.assertEqual(stats['updated'], 1)
        self.assertEqual(stats['errors'], 0)

        page = GlossaryTermPage.objects.get(pk=existing.pk)
        self.assertEqual(page.shopify_id, new_gid)
        self.assertEqual(GlossaryTermPage.objects.filter(slug='lenceria').count(), 1)

    @patch('shopify_content.sync.inbound._paginate')
    @patch('shopify_content.tasks.sync_glossary_index_task.delay')
    def test_import_queues_index_rebuild_on_success(self, mock_index_delay, mock_paginate):
        mock_paginate.return_value = iter([
            _make_glossary_node('gid://shopify/Metaobject/400', 'alpha', 'Alpha'),
        ])

        import_glossary_terms('test-shop.myshopify.com', self.parent)

        mock_index_delay.assert_called_once()

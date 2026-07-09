from django.test import TestCase
from wagtail.models import Locale, Page

from shopify_content.models import (
    ArticlePage,
    BlogPage,
    CollectionPage,
    GlossaryTermPage,
    HomePage,
    LocationPage,
    ProductPage,
    ShopifyRootPage,
)
from shopify_content.storefront_urls import (
    all_paths_for_page,
    article_path,
    glossary_term_path,
    location_page_path,
    page_content_type_key,
    storefront_path_for_page,
)


def _locale(code: str) -> Locale:
    locale, _ = Locale.objects.get_or_create(language_code=code)
    return locale


class StorefrontUrlsTests(TestCase):
    def setUp(self):
        locale = _locale('en-US')
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title='Home', slug='home', locale=locale))
        self.root = home

    def _add_child(self, page):
        self.root.add_child(instance=page)
        return page

    def test_product_path(self):
        page = ProductPage(
            title='Toy',
            slug='toy',
            handle='toy',
            shopify_id='gid://shopify/Product/1',
            locale=_locale('en-US'),
        )
        self._add_child(page)
        self.assertEqual(storefront_path_for_page(page), '/products/toy')
        self.assertEqual(page_content_type_key(page), 'product')

    def test_collection_path(self):
        page = CollectionPage(
            title='Vibrators',
            slug='vibrators',
            handle='vibrators',
            shopify_id='gid://shopify/Collection/1',
            locale=_locale('en-US'),
        )
        self._add_child(page)
        self.assertEqual(storefront_path_for_page(page), '/collections/vibrators')

    def test_article_path_requires_blog_parent(self):
        blog = BlogPage(
            title='News',
            slug='news',
            handle='news',
            shopify_id='gid://shopify/Blog/1',
            locale=_locale('en-US'),
        )
        self._add_child(blog)
        article = ArticlePage(
            title='Post',
            slug='post',
            handle='post',
            shopify_id='gid://shopify/Article/1',
            locale=_locale('en-US'),
        )
        blog.add_child(instance=article)
        self.assertEqual(storefront_path_for_page(article), article_path('news', 'post'))

    def test_glossary_term_path(self):
        glossary_root = ShopifyRootPage(title='Glossary', slug='glossary', locale=_locale('en-US'))
        self._add_child(glossary_root)
        term = GlossaryTermPage(
            title='Alpha',
            term='Alpha',
            slug='alpha',
            handle='alpha',
            locale_code='en',
            shopify_id='gid://shopify/Metaobject/1',
            locale=_locale('en-US'),
        )
        glossary_root.add_child(instance=term)
        self.assertEqual(storefront_path_for_page(term), glossary_term_path('alpha'))

    def test_location_path_uses_canonical_slug(self):
        loc_root = ShopifyRootPage(title='Locations', slug='local-us', locale=_locale('en-US'))
        self._add_child(loc_root)
        page = LocationPage(
            title='LA Store',
            titulo='LA Store',
            slug='en-us-los-angeles-california',
            handle='en-us-los-angeles-california',
            city='Los Angeles',
            state='California',
            shopify_id='gid://shopify/Metaobject/2',
            locale=_locale('en-US'),
        )
        loc_root.add_child(instance=page)
        self.assertEqual(
            storefront_path_for_page(page),
            location_page_path('en-us-los-angeles-california'),
        )

    def test_root_index_paths(self):
        for slug, expected in (
            ('glossary', '/pages/glossary'),
            ('local-us', '/pages/locations'),
            ('blogs', '/pages/blogs'),
        ):
            root = ShopifyRootPage(
                title=slug,
                slug=slug,
                shopify_id='gid://shopify/Metaobject/root',
                locale=_locale('en-US'),
            )
            self._add_child(root)
            self.assertEqual(storefront_path_for_page(root), expected)

    def test_home_page_path(self):
        home_root = ShopifyRootPage(title='CMS Home', slug='cms-home', locale=_locale('en-US'))
        self._add_child(home_root)
        page = HomePage(
            title='Home EN US',
            slug='home-en-us',
            handle='home-en-us',
            hero_heading='Welcome',
            shopify_id='gid://shopify/Metaobject/home',
            locale=_locale('en-US'),
        )
        home_root.add_child(instance=page)
        self.assertEqual(storefront_path_for_page(page), '/pages/home-en-us')

    def test_all_paths_includes_locale_prefix(self):
        page = ProductPage(
            title='Toy',
            slug='toy-es',
            handle='toy-es',
            shopify_id='gid://shopify/Product/1',
            locale=_locale('es-US'),
        )
        self._add_child(page)
        paths = all_paths_for_page(page)
        self.assertIn('/products/toy-es', paths)
        self.assertIn('/es-us/products/toy-es', paths)

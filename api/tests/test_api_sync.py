import api.ninja_compat  # noqa: F401 — must run before any ninja import

from unittest.mock import patch

from django.test import TestCase
from ninja.openapi import get_schema
from ninja.testing import TestClient
from wagtail.models import Locale, Page

from api.main import api
from api.models import ApiKey
from api.agent_registry import CAPABILITIES, WORKFLOWS
from shopify_content.models import GlossaryTermPage, LocationPage, ShopifyRootPage


def _auth_headers(key: str) -> dict:
    return {"Authorization": f"Bearer {key}"}


class ApiAuthTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)
        self.key = ApiKey.objects.create(name="test-agent")

    def test_missing_api_key_returns_401(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 401)

    def test_invalid_api_key_returns_401(self):
        response = self.client.get("/products/", headers=_auth_headers("invalid-key"))
        self.assertEqual(response.status_code, 401)

    def test_valid_api_key_allows_access(self):
        response = self.client.get("/products/", headers=_auth_headers(self.key.key))
        self.assertEqual(response.status_code, 200)


class PullSyncTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)
        self.key = ApiKey.objects.create(name="pull-agent")

    @patch("api.sync.run_shopify_import_for_api")
    def test_pull_products_returns_200_with_import_stats(self, mock_import):
        mock_import.return_value = {
            "created": 2,
            "updated": 5,
            "skipped": 0,
            "errors": 0,
            "message": "Products — Creados: 2, Actualizados: 5, Errores: 0",
        }
        response = self.client.post(
            "/products/pull",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["created"], 2)
        self.assertEqual(data["updated"], 5)
        self.assertEqual(data["errors"], 0)
        mock_import.assert_called_once_with("products", new_only=False)

    @patch("shopify_content.sync.task_dispatch.enqueue_shopify_import")
    @patch("api.sync.run_shopify_import_for_api")
    def test_pull_does_not_enqueue_celery(self, mock_import, mock_enqueue):
        mock_import.return_value = {
            "created": 0,
            "updated": 0,
            "skipped": 0,
            "errors": 0,
            "message": "ok",
        }
        self.client.post("/products/pull", headers=_auth_headers(self.key.key))
        mock_enqueue.assert_not_called()


class LocationApiTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)
        self.key = ApiKey.objects.create(name="location-agent")
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title="Home", slug="home", locale=locale))
        self.products_parent = ShopifyRootPage(title="Root", slug="root", locale=locale)
        home.add_child(instance=self.products_parent)
        self.products_parent.save_revision().publish()
        self.locales_parent = ShopifyRootPage(title="Local US", slug="local-us", locale=locale)
        home.add_child(instance=self.locales_parent)
        self.locales_parent.save_revision().publish()
        # Kept for push tests that attach locations manually.
        self.parent = self.locales_parent

    def test_create_and_get_location(self):
        response = self.client.post(
            "/locations/",
            json={
                "titulo": "Austin Store",
                "city": "Austin",
                "country": "United States",
            },
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 201)
        page_id = response.json()["id"]
        self.assertEqual(response.json()["titulo"], "Austin Store")

        page = LocationPage.objects.get(pk=page_id)
        self.assertEqual(page.get_parent().pk, self.locales_parent.pk)
        self.assertNotEqual(page.get_parent().pk, self.products_parent.pk)

    def test_create_location_with_explicit_parent_page_id(self):
        response = self.client.post(
            "/locations/",
            json={
                "titulo": "Nashville Store",
                "city": "Nashville",
                "parent_page_id": self.locales_parent.pk,
            },
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 201)
        page = LocationPage.objects.get(pk=response.json()["id"])
        self.assertEqual(page.get_parent().pk, self.locales_parent.pk)

    def test_create_location_invalid_parent_page_id_returns_400(self):
        response = self.client.post(
            "/locations/",
            json={
                "titulo": "Bad Parent Store",
                "city": "Nowhere",
                "parent_page_id": 999999,
            },
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("not found", response.json()["detail"])

        get_response = self.client.get(
            f"/locations/{page_id}",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()["city"], "Austin")

    def test_create_location_with_seo_fields(self):
        response = self.client.post(
            "/locations/",
            json={
                "titulo": "Miami Store",
                "city": "Miami",
                "seo_title": "Miami SEO Title",
                "search_description": "Visit our Miami location.",
            },
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["seo_title"], "Miami SEO Title")
        self.assertEqual(data["search_description"], "Visit our Miami location.")

        page = LocationPage.objects.get(pk=data["id"])
        self.assertEqual(page.seo_title, "Miami SEO Title")
        self.assertEqual(page.search_description, "Visit our Miami location.")

    def test_patch_location_seo_fields(self):
        create_response = self.client.post(
            "/locations/",
            json={"titulo": "Seattle Store", "city": "Seattle"},
            headers=_auth_headers(self.key.key),
        )
        page_id = create_response.json()["id"]

        patch_response = self.client.patch(
            f"/locations/{page_id}",
            json={
                "seo_title": "Seattle SEO",
                "search_description": "Pacific Northwest store.",
            },
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(patch_response.status_code, 200)
        self.assertEqual(patch_response.json()["seo_title"], "Seattle SEO")
        self.assertEqual(
            patch_response.json()["search_description"],
            "Pacific Northwest store.",
        )

    @patch(
        "api.routers.locations.sync_location_page",
        return_value=(True, "Location synced to Shopify metaobject successfully."),
    )
    def test_push_location_returns_sync_result(self, mock_sync):
        page = LocationPage(
            title="Denver",
            titulo="Denver",
            slug="denver",
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()
        page.shopify_id = "gid://shopify/Metaobject/99"
        page.save()

        response = self.client.post(
            f"/locations/{page.pk}/push",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        mock_sync.assert_called_once()

    @patch(
        "api.routers.locations.sync_location_page",
        return_value=(False, "Shopify metaobject error: missing access token"),
    )
    def test_push_location_returns_metaobject_error_message(self, mock_sync):
        page = LocationPage(
            title="Denver",
            titulo="Denver",
            slug="denver",
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()

        response = self.client.post(
            f"/locations/{page.pk}/push",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertIn("Shopify metaobject error", data["message"])
        mock_sync.assert_called_once()


class GlossaryApiTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)
        self.key = ApiKey.objects.create(name="glossary-agent")
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title="Home", slug="home", locale=locale))
        self.products_parent = ShopifyRootPage(title="Root", slug="root", locale=locale)
        home.add_child(instance=self.products_parent)
        self.products_parent.save_revision().publish()
        self.glossary_parent = ShopifyRootPage(title="Glossary", slug="glossary", locale=locale)
        home.add_child(instance=self.glossary_parent)
        self.glossary_parent.save_revision().publish()
        self.parent = self.glossary_parent

    def test_create_and_get_glossary_term(self):
        response = self.client.post(
            "/glossary/",
            json={
                "term": "Vibrator",
                "locale_code": "en",
                "definition": "<p>A device that vibrates.</p>",
            },
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 201)
        page_id = response.json()["id"]
        self.assertEqual(response.json()["term"], "Vibrator")

        page = GlossaryTermPage.objects.get(pk=page_id)
        self.assertEqual(page.get_parent().pk, self.glossary_parent.pk)
        self.assertNotEqual(page.get_parent().pk, self.products_parent.pk)

        get_response = self.client.get(
            f"/glossary/{page_id}",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()["definition"], "<p>A device that vibrates.</p>")

    def test_create_with_explicit_parent_page_id(self):
        response = self.client.post(
            "/glossary/",
            json={
                "term": "Lubricant",
                "locale_code": "en",
                "parent_page_id": self.glossary_parent.pk,
            },
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 201)
        page = GlossaryTermPage.objects.get(pk=response.json()["id"])
        self.assertEqual(page.get_parent().pk, self.glossary_parent.pk)

    def test_create_invalid_parent_returns_400(self):
        response = self.client.post(
            "/glossary/",
            json={
                "term": "Bad Term",
                "parent_page_id": 999999,
            },
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("not found", response.json()["detail"])

    def test_patch_glossary_term(self):
        create_response = self.client.post(
            "/glossary/",
            json={"term": "Original Term", "locale_code": "en"},
            headers=_auth_headers(self.key.key),
        )
        page_id = create_response.json()["id"]

        patch_response = self.client.patch(
            f"/glossary/{page_id}",
            json={
                "definition": "<p>Updated definition.</p>",
                "locale_code": "es",
            },
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(patch_response.status_code, 200)
        self.assertEqual(patch_response.json()["locale_code"], "es")
        self.assertEqual(patch_response.json()["definition"], "<p>Updated definition.</p>")

    def test_get_glossary_term_locale_returns_locale_code(self):
        create_response = self.client.post(
            "/glossary/",
            json={"term": "Spanish Term", "locale_code": "es"},
            headers=_auth_headers(self.key.key),
        )
        page_id = create_response.json()["id"]

        get_response = self.client.get(
            f"/glossary/{page_id}",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(get_response.status_code, 200)
        data = get_response.json()
        self.assertEqual(data["locale_code"], "es")
        self.assertEqual(data["locale"], "es")
        self.assertNotIn("United States", data["locale"])

    def test_get_glossary_term_after_push_includes_timestamps(self):
        from shopify_content.sync.outbound import _mark_synced

        create_response = self.client.post(
            "/glossary/",
            json={"term": "Synced Term", "locale_code": "en"},
            headers=_auth_headers(self.key.key),
        )
        page_id = create_response.json()["id"]
        self.client.patch(
            f"/glossary/{page_id}",
            json={"publish": True},
            headers=_auth_headers(self.key.key),
        )

        def _sync_and_mark(page):
            _mark_synced(type(page), page.pk)
            return True, "Glossary term synced to Shopify metaobject successfully."

        with patch(
            "api.routers.glossary.sync_glossary_term_page",
            side_effect=_sync_and_mark,
        ):
            push_response = self.client.post(
                f"/glossary/{page_id}/push",
                headers=_auth_headers(self.key.key),
            )
        self.assertTrue(push_response.json()["success"])

        get_response = self.client.get(
            f"/glossary/{page_id}",
            headers=_auth_headers(self.key.key),
        )
        data = get_response.json()
        self.assertIsNotNone(data["last_synced_at"])
        self.assertIsNotNone(data["first_published_at"])
        self.assertIsNotNone(data["last_published_at"])

    @patch(
        "api.routers.glossary.sync_glossary_term_page",
        return_value=(True, "Glossary term synced to Shopify metaobject successfully."),
    )
    def test_push_glossary_term_returns_sync_result(self, mock_sync):
        page = GlossaryTermPage(
            title="Massager",
            term="Massager",
            slug="massager",
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()
        page.shopify_id = "gid://shopify/Metaobject/88"
        page.save()

        response = self.client.post(
            f"/glossary/{page.pk}/push",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        mock_sync.assert_called_once()

    @patch(
        "api.routers.glossary.sync_glossary_term_page",
        return_value=(False, "Shopify metaobject error: term is required"),
    )
    def test_push_glossary_term_returns_error_message(self, mock_sync):
        page = GlossaryTermPage(
            title="Empty Term",
            term="Empty Term",
            slug="empty-term",
            locale=Locale.get_default(),
        )
        self.parent.add_child(instance=page)
        page.save_revision().publish()

        response = self.client.post(
            f"/glossary/{page.pk}/push",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertIn("Shopify metaobject error", data["message"])
        mock_sync.assert_called_once()

    def test_list_filter_by_locale_code(self):
        self.client.post(
            "/glossary/",
            json={"term": "English Term", "locale_code": "en"},
            headers=_auth_headers(self.key.key),
        )
        self.client.post(
            "/glossary/",
            json={"term": "Spanish Term", "locale_code": "es"},
            headers=_auth_headers(self.key.key),
        )

        response = self.client.get(
            "/glossary/?locale_code=es",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        terms = [item["term"] for item in response.json()]
        self.assertEqual(terms, ["Spanish Term"])

    def test_capabilities_includes_glossary(self):
        response = self.client.get(
            "/capabilities/",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        tool_ids = {tool["operation_id"] for tool in response.json()["tools"]}
        self.assertIn("create_glossary_term", tool_ids)
        self.assertIn("push_glossary_term", tool_ids)
        self.assertIn(
            "glossary_wagtail_origin",
            response.json()["workflows"],
        )


class CapabilitiesTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)
        self.key = ApiKey.objects.create(name="capabilities-agent")

    def test_capabilities_returns_200_with_expected_tools(self):
        response = self.client.get(
            "/capabilities/",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["api_version"], "1.1.0")
        self.assertEqual(data["auth"]["type"], "bearer")

        tool_ids = {tool["operation_id"] for tool in data["tools"]}
        self.assertIn("pull_products_sync_post", tool_ids)
        self.assertIn("push_location", tool_ids)
        self.assertIn("push_glossary_term", tool_ids)
        self.assertNotIn("list_agent_capabilities", tool_ids)

        expected_ops = {
            op_id for op_id in CAPABILITIES if op_id != "list_agent_capabilities"
        }
        self.assertEqual(tool_ids, expected_ops)

    def test_capabilities_includes_workflows(self):
        response = self.client.get(
            "/capabilities/",
            headers=_auth_headers(self.key.key),
        )
        workflows = response.json()["workflows"]
        self.assertEqual(
            workflows["products_existing_store"],
            list(WORKFLOWS["products_existing_store"]),
        )
        self.assertIn("locations_wagtail_origin", workflows)
        self.assertIn("glossary_wagtail_origin", workflows)


class SearchEndpointTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)
        self.key = ApiKey.objects.create(name="search-agent")
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title="Home", slug="home", locale=locale))
        from shopify_content.models import BlogPage, ArticlePage
        self.blog_parent = ShopifyRootPage(title="Root", slug="root-se", locale=locale)
        home.add_child(instance=self.blog_parent)
        self.blog_parent.save_revision().publish()
        self.blog = BlogPage(title="Test Blog", slug="test-blog-se", locale=locale)
        self.blog_parent.add_child(instance=self.blog)
        self.blog.save_revision().publish()
        self.article = ArticlePage(
            title="Guía completa de vibradores",
            slug="guia-vibradores",
            locale=locale,
            seo_title="SEO: Guía de vibradores",
        )
        self.blog.add_child(instance=self.article)
        self.article.save_revision().publish()

    def test_search_returns_200(self):
        response = self.client.get(
            "/search/?q=vibradores",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("total", data)
        self.assertIn("results", data)

    def test_search_returns_matching_article(self):
        response = self.client.get(
            "/search/?q=vibradores",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        titles = [r["title"] for r in response.json()["results"]]
        self.assertIn("Guía completa de vibradores", titles)

    def test_search_with_resource_filter(self):
        response = self.client.get(
            "/search/?q=vibradores&resource=articles",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        for r in response.json()["results"]:
            self.assertEqual(r["resource"], "article")

    def test_search_respects_limit(self):
        response = self.client.get(
            "/search/?q=test&limit=1",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response.json()["results"]), 1)

    def test_search_result_has_expected_fields(self):
        response = self.client.get(
            "/search/?q=vibradores",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        results = response.json()["results"]
        if results:
            item = results[0]
            self.assertIn("resource", item)
            self.assertIn("page_id", item)
            self.assertIn("title", item)
            self.assertIn("slug", item)
            self.assertIn("locale", item)
            self.assertIn("live", item)

    def test_search_requires_auth(self):
        response = self.client.get("/search/?q=test")
        self.assertEqual(response.status_code, 401)


class LinksIndexTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)
        self.key = ApiKey.objects.create(name="links-agent")
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title="Home", slug="home", locale=locale))
        from shopify_content.models import BlogPage, ArticlePage
        self.root = ShopifyRootPage(title="Root", slug="root-li", locale=locale)
        home.add_child(instance=self.root)
        self.root.save_revision().publish()
        self.blog = BlogPage(title="Blog A", slug="blog-a-li", locale=locale)
        self.root.add_child(instance=self.blog)
        self.blog.save_revision().publish()
        self.article = ArticlePage(
            title="Article One",
            slug="article-one",
            locale=locale,
            handle="article-one",
        )
        self.blog.add_child(instance=self.article)
        self.article.save_revision().publish()

    def test_links_index_returns_200(self):
        response = self.client.get(
            "/links/index/",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("generated_at", data)
        self.assertIn("total", data)
        self.assertIn("index", data)

    def test_links_index_contains_article(self):
        response = self.client.get(
            "/links/index/?resource=articles",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        slugs = [item["slug"] for item in response.json()["index"]]
        self.assertIn("article-one", slugs)

    def test_links_index_resource_filter(self):
        response = self.client.get(
            "/links/index/?resource=articles",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        for item in response.json()["index"]:
            self.assertEqual(item["resource"], "article")

    def test_links_index_requires_auth(self):
        response = self.client.get("/links/index/")
        self.assertEqual(response.status_code, 401)

    def test_links_index_item_has_expected_fields(self):
        response = self.client.get(
            "/links/index/?resource=articles",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        items = response.json()["index"]
        if items:
            item = items[0]
            self.assertIn("resource", item)
            self.assertIn("page_id", item)
            self.assertIn("title", item)
            self.assertIn("slug", item)
            self.assertIn("locale", item)
            self.assertIn("shopify_handle", item)


class BulkUpdateTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)
        self.key = ApiKey.objects.create(name="bulk-agent")
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title="Home", slug="home", locale=locale))
        from shopify_content.models import BlogPage, ArticlePage
        self.root = ShopifyRootPage(title="Root", slug="root-bu", locale=locale)
        home.add_child(instance=self.root)
        self.root.save_revision().publish()
        self.blog = BlogPage(title="Test Blog", slug="test-blog-bulk", locale=locale)
        self.root.add_child(instance=self.blog)
        self.blog.save_revision().publish()
        self.article = ArticlePage(
            title="Bulk Article",
            slug="bulk-article",
            locale=locale,
        )
        self.blog.add_child(instance=self.article)
        self.article.save_revision().publish()

    def test_bulk_update_happy_path(self):
        response = self.client.post(
            "/bulk/update/",
            json={
                "operations": [
                    {
                        "resource": "article",
                        "page_id": self.article.pk,
                        "fields": {"seo_title": "Updated SEO Title"},
                        "publish": False,
                    }
                ]
            },
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total"], 1)
        self.assertEqual(data["succeeded"], 1)
        self.assertEqual(data["failed"], 0)
        self.assertEqual(data["results"][0]["status"], "ok")

    def test_bulk_update_nonexistent_page_returns_error_in_result(self):
        response = self.client.post(
            "/bulk/update/",
            json={
                "operations": [
                    {
                        "resource": "article",
                        "page_id": 999999,
                        "fields": {"seo_title": "x"},
                        "publish": False,
                    }
                ]
            },
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["failed"], 1)
        self.assertEqual(data["results"][0]["status"], "error")
        self.assertIsNotNone(data["results"][0]["error"])

    def test_bulk_update_over_50_returns_400(self):
        ops = [
            {"resource": "article", "page_id": i + 1, "fields": {}, "publish": False}
            for i in range(51)
        ]
        response = self.client.post(
            "/bulk/update/",
            json={"operations": ops},
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 400)

    def test_bulk_update_partial_failure_does_not_stop_others(self):
        response = self.client.post(
            "/bulk/update/",
            json={
                "operations": [
                    {
                        "resource": "article",
                        "page_id": 999999,
                        "fields": {"seo_title": "Bad"},
                        "publish": False,
                    },
                    {
                        "resource": "article",
                        "page_id": self.article.pk,
                        "fields": {"seo_title": "Good"},
                        "publish": False,
                    },
                ]
            },
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total"], 2)
        self.assertEqual(data["succeeded"], 1)
        self.assertEqual(data["failed"], 1)

    def test_bulk_update_requires_auth(self):
        response = self.client.post("/bulk/update/", json={"operations": []})
        self.assertEqual(response.status_code, 401)


class BodyPatchTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)
        self.key = ApiKey.objects.create(name="bodypatch-agent")
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title="Home", slug="home", locale=locale))
        from shopify_content.models import BlogPage, ArticlePage
        self.root = ShopifyRootPage(title="Root", slug="root-bp", locale=locale)
        home.add_child(instance=self.root)
        self.root.save_revision().publish()
        self.blog = BlogPage(title="Blog BP", slug="blog-bp", locale=locale)
        self.root.add_child(instance=self.blog)
        self.blog.save_revision().publish()
        self.article = ArticlePage(
            title="Body Article",
            slug="body-article",
            locale=locale,
        )
        self.blog.add_child(instance=self.article)
        self.article.save_revision().publish()

    def test_append_operation(self):
        response = self.client.post(
            f"/articles/{self.article.pk}/body/patch/",
            json={
                "operations": [
                    {"op": "append", "content": "<p>New paragraph</p>"}
                ],
                "publish": False,
            },
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)

    def test_empty_operations_returns_400(self):
        response = self.client.post(
            f"/articles/{self.article.pk}/body/patch/",
            json={"operations": [], "publish": False},
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 400)

    def test_nonexistent_article_returns_404(self):
        response = self.client.post(
            "/articles/999999/body/patch/",
            json={
                "operations": [{"op": "append", "content": "<p>x</p>"}],
                "publish": False,
            },
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 404)

    def test_insert_after_missing_target_returns_400(self):
        response = self.client.post(
            f"/articles/{self.article.pk}/body/patch/",
            json={
                "operations": [
                    {"op": "insert_after", "target": "h2:Nonexistent Heading", "content": "<p>x</p>"}
                ],
                "publish": False,
            },
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 400)

    def test_body_patch_requires_auth(self):
        response = self.client.post(
            f"/articles/{self.article.pk}/body/patch/",
            json={"operations": [{"op": "append", "content": "<p>x</p>"}]},
        )
        self.assertEqual(response.status_code, 401)


class ArticleVersionsTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)
        self.key = ApiKey.objects.create(name="versions-agent")
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title="Home", slug="home", locale=locale))
        from shopify_content.models import BlogPage, ArticlePage
        self.root = ShopifyRootPage(title="Root", slug="root-v", locale=locale)
        home.add_child(instance=self.root)
        self.root.save_revision().publish()
        self.blog = BlogPage(title="Blog V", slug="blog-v", locale=locale)
        self.root.add_child(instance=self.blog)
        self.blog.save_revision().publish()
        self.article = ArticlePage(
            title="Versioned Article",
            slug="versioned-article",
            locale=locale,
        )
        self.blog.add_child(instance=self.article)
        rev1 = self.article.save_revision()
        rev1.publish()
        self.article.title = "Versioned Article v2"
        rev2 = self.article.save_revision()
        rev2.publish()
        self.article.refresh_from_db()

    def test_list_versions_returns_200(self):
        response = self.client.get(
            f"/articles/{self.article.pk}/versions/",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_list_versions_has_expected_fields(self):
        response = self.client.get(
            f"/articles/{self.article.pk}/versions/",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        item = response.json()[0]
        self.assertIn("revision_id", item)
        self.assertIn("created_at", item)
        self.assertIn("is_latest", item)

    def test_list_versions_latest_flag(self):
        response = self.client.get(
            f"/articles/{self.article.pk}/versions/",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        items = response.json()
        latest_flags = [item["is_latest"] for item in items if item["is_latest"]]
        self.assertEqual(len(latest_flags), 1)

    def test_list_versions_nonexistent_returns_404(self):
        response = self.client.get(
            "/articles/999999/versions/",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 404)

    def test_get_specific_version(self):
        versions_response = self.client.get(
            f"/articles/{self.article.pk}/versions/",
            headers=_auth_headers(self.key.key),
        )
        revision_id = versions_response.json()[0]["revision_id"]

        response = self.client.get(
            f"/articles/{self.article.pk}/versions/{revision_id}/",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json())

    def test_get_nonexistent_version_returns_404(self):
        response = self.client.get(
            f"/articles/{self.article.pk}/versions/999999/",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 404)

    def test_revert_article_version(self):
        versions_response = self.client.get(
            f"/articles/{self.article.pk}/versions/",
            headers=_auth_headers(self.key.key),
        )
        items = versions_response.json()
        oldest_revision_id = items[-1]["revision_id"]

        response = self.client.post(
            f"/articles/{self.article.pk}/revert/{oldest_revision_id}/",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json())

    def test_revert_nonexistent_revision_returns_404(self):
        response = self.client.post(
            f"/articles/{self.article.pk}/revert/999999/",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 404)

    def test_versions_require_auth(self):
        response = self.client.get(f"/articles/{self.article.pk}/versions/")
        self.assertEqual(response.status_code, 401)


class ArticleListFiltersTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)
        self.key = ApiKey.objects.create(name="filter-agent")
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title="Home", slug="home", locale=locale))
        from shopify_content.models import BlogPage, ArticlePage
        self.root = ShopifyRootPage(title="Root", slug="root-flt", locale=locale)
        home.add_child(instance=self.root)
        self.root.save_revision().publish()
        self.blog = BlogPage(title="Filter Blog", slug="filter-blog", locale=locale)
        self.root.add_child(instance=self.blog)
        self.blog.save_revision().publish()
        self.article = ArticlePage(
            title="Tagged Article",
            slug="tagged-article",
            locale=locale,
        )
        self.blog.add_child(instance=self.article)
        rev = self.article.save_revision()
        rev.publish()
        self.article.tags.add("test-tag")
        self.article.save()

    def test_filter_by_live_true(self):
        response = self.client.get(
            "/articles/?live=true",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        for item in response.json():
            self.assertTrue(item["live"])

    def test_filter_by_tag(self):
        response = self.client.get(
            "/articles/?tag=test-tag",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        titles = [item["title"] for item in response.json()]
        self.assertIn("Tagged Article", titles)

    def test_filter_by_search_shorthand(self):
        response = self.client.get(
            "/articles/?search=Tagged",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        titles = [item["title"] for item in response.json()]
        self.assertIn("Tagged Article", titles)

    def test_ordering_by_title(self):
        response = self.client.get(
            "/articles/?ordering=title",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)

    def test_capabilities_includes_new_workflows(self):
        response = self.client.get(
            "/capabilities/",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        workflows = response.json()["workflows"]
        self.assertIn("search_and_link", workflows)
        self.assertIn("bulk_meta_update", workflows)
        self.assertIn("body_surgery", workflows)
        self.assertEqual(workflows["search_and_link"], ["search_content", "links_index", "update_article"])
        self.assertEqual(workflows["bulk_meta_update"], ["links_index", "bulk_update"])
        self.assertEqual(workflows["body_surgery"], ["get_article", "body_patch_article", "push_article"])

    def test_capabilities_includes_new_tool_ids(self):
        response = self.client.get(
            "/capabilities/",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        tool_ids = {t["operation_id"] for t in response.json()["tools"]}
        for op_id in [
            "search_content",
            "links_index",
            "bulk_update",
            "body_patch_article",
            "list_article_versions",
            "get_article_version",
            "revert_article_version",
        ]:
            self.assertIn(op_id, tool_ids)


class OpenAPIAgentMetadataTests(TestCase):
    def test_pull_products_has_x_agent_fields(self):
        schema = get_schema(api=api, path_prefix="")
        operation = schema["paths"]["/products/pull"]["post"]
        self.assertEqual(operation["x-agent-capability-type"], "sync_inbound")
        self.assertEqual(operation["x-agent-resource"], "products")
        self.assertEqual(operation["x-agent-sync-direction"], "shopify_to_wagtail")
        self.assertIn("list_products", operation["x-agent-next-tools"])

    def test_openapi_tags_have_descriptions(self):
        schema = get_schema(api=api, path_prefix="")
        tag_names = {tag["name"] for tag in schema["tags"]}
        self.assertIn("Products", tag_names)
        self.assertIn("Capabilities", tag_names)
        products_tag = next(t for t in schema["tags"] if t["name"] == "Products")
        self.assertIn("sync_inbound", products_tag["description"])

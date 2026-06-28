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
                "state": "Texas",
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
        self.assertEqual(page.slug, "en-us-austin-texas")
        self.assertEqual(page.handle, "en-us-austin-texas")
        self.assertEqual(response.json()["slug"], "en-us-austin-texas")
        self.assertEqual(response.json()["handle"], "en-us-austin-texas")

    def test_patch_city_recalculates_slug_and_handle(self):
        create_response = self.client.post(
            "/locations/",
            json={"titulo": "Texas Store", "city": "Austin", "state": "Texas"},
            headers=_auth_headers(self.key.key),
        )
        page_id = create_response.json()["id"]

        patch_response = self.client.patch(
            f"/locations/{page_id}",
            json={"city": "Dallas"},
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(patch_response.status_code, 200)
        self.assertEqual(patch_response.json()["slug"], "en-us-dallas-texas")
        self.assertEqual(patch_response.json()["handle"], "en-us-dallas-texas")

        page = LocationPage.objects.get(pk=page_id)
        self.assertEqual(page.slug, "en-us-dallas-texas")
        self.assertEqual(page.handle, "en-us-dallas-texas")

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
            city="Denver",
            slug="en-us-denver",
            handle="en-us-denver",
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
            city="Denver",
            slug="en-us-denver",
            handle="en-us-denver",
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

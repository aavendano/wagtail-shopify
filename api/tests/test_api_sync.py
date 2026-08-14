import api.ninja_compat  # noqa: F401 — must run before any ninja import

from unittest.mock import patch

from django.test import TestCase
from ninja.openapi import get_schema
from ninja.testing import TestClient
from wagtail.models import Locale, Page

from api.main import api
from api.models import ApiKey
from api.agent_registry import CAPABILITIES, WORKFLOWS
from shopify_content.models import (
    GlossaryTermPage,
    HomePage,
    LocationPage,
    ProductPage,
    ShopifyRootPage,
)


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

    @patch("api.sync.run_shopify_import_for_api")
    def test_pull_glossary_returns_200_with_import_stats(self, mock_import):
        mock_import.return_value = {
            "created": 1,
            "updated": 3,
            "skipped": 0,
            "errors": 0,
            "message": "Glosario — Creados: 1, Actualizados: 3, Errores: 0",
        }
        response = self.client.post(
            "/glossary/pull",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["created"], 1)
        self.assertEqual(data["updated"], 3)
        self.assertEqual(data["errors"], 0)
        mock_import.assert_called_once_with("glossary", new_only=False)

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
        Locale.objects.get_or_create(language_code="es-US")
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

    def test_create_without_synonyms_or_same_as_defaults_to_empty_lists(self):
        response = self.client.post(
            "/glossary/",
            json={
                "term": "Libido",
                "locale_code": "en",
            },
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 201)
        body = response.json()
        self.assertEqual(body["synonyms"], [])
        self.assertEqual(body["same_as"], [])

        page = GlossaryTermPage.objects.get(pk=body["id"])
        self.assertEqual(page.synonyms, [])
        self.assertEqual(page.same_as, [])

    def test_patch_and_get_same_as(self):
        create_response = self.client.post(
            "/glossary/",
            json={"term": "Libido", "locale_code": "en"},
            headers=_auth_headers(self.key.key),
        )
        page_id = create_response.json()["id"]
        same_as = ["https://en.wikipedia.org/wiki/Libido"]

        patch_response = self.client.patch(
            f"/glossary/{page_id}",
            json={"same_as": same_as, "synonyms": ["Sex drive"]},
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(patch_response.status_code, 200)
        self.assertEqual(patch_response.json()["same_as"], same_as)
        self.assertEqual(patch_response.json()["synonyms"], ["Sex drive"])

        get_response = self.client.get(
            f"/glossary/{page_id}",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()["same_as"], same_as)

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

    def test_patch_related_links_persists_as_manual_fks(self):
        locale = Locale.get_default()
        product = ProductPage(
            title="Satisfyer Pro 2",
            slug="satisfyer-pro-2",
            handle="satisfyer-pro-2",
            locale=locale,
        )
        self.products_parent.add_child(instance=product)
        product.save_revision().publish()

        create_response = self.client.post(
            "/glossary/",
            json={"term": "Vibrator", "locale_code": "en", "handle": "vibrator"},
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(create_response.status_code, 201)
        page_id = create_response.json()["id"]

        related = [
            {
                "type": "product",
                "handle": "satisfyer-pro-2",
                "label": "Satisfyer Pro 2",
            }
        ]
        patch_response = self.client.patch(
            f"/glossary/{page_id}",
            json={"related_links": related},
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(patch_response.status_code, 200)
        body_links = patch_response.json()["related_links"]
        self.assertEqual(len(body_links), 1)
        self.assertEqual(body_links[0]["type"], "product")
        self.assertEqual(body_links[0]["handle"], "satisfyer-pro-2")

        page = GlossaryTermPage.objects.get(pk=page_id)
        self.assertTrue(
            page.related_products.filter(related_page=product, is_auto=False).exists()
        )
        self.assertEqual(len(page.related_links), 1)

        get_response = self.client.get(
            f"/glossary/{page_id}",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()["related_links"][0]["handle"], "satisfyer-pro-2")

    def test_create_with_related_links_persists_manual_fks(self):
        locale = Locale.get_default()
        product = ProductPage(
            title="Linked Product",
            slug="linked-product",
            handle="linked-product",
            locale=locale,
        )
        self.products_parent.add_child(instance=product)
        product.save_revision().publish()

        response = self.client.post(
            "/glossary/",
            json={
                "term": "Massager",
                "locale_code": "en",
                "related_links": [
                    {
                        "type": "product",
                        "handle": "linked-product",
                        "label": "Linked Product",
                    }
                ],
            },
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 201)
        page = GlossaryTermPage.objects.get(pk=response.json()["id"])
        self.assertTrue(
            page.related_products.filter(related_page=product, is_auto=False).exists()
        )
        self.assertEqual(response.json()["related_links"][0]["handle"], "linked-product")

    def test_patch_related_links_unresolved_returns_400(self):
        create_response = self.client.post(
            "/glossary/",
            json={"term": "Broken Links", "locale_code": "en"},
            headers=_auth_headers(self.key.key),
        )
        page_id = create_response.json()["id"]

        patch_response = self.client.patch(
            f"/glossary/{page_id}",
            json={
                "related_links": [
                    {
                        "type": "product",
                        "handle": "does-not-exist",
                        "label": "Missing",
                    }
                ]
            },
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(patch_response.status_code, 400)
        self.assertIn("could not resolve", patch_response.json()["detail"])

    def test_patch_related_links_empty_clears_manuals(self):
        locale = Locale.get_default()
        product = ProductPage(
            title="Clear Me",
            slug="clear-me",
            handle="clear-me",
            locale=locale,
        )
        self.products_parent.add_child(instance=product)
        product.save_revision().publish()

        create_response = self.client.post(
            "/glossary/",
            json={
                "term": "Clear Links",
                "locale_code": "en",
                "related_links": [
                    {"type": "product", "handle": "clear-me", "label": "Clear Me"}
                ],
            },
            headers=_auth_headers(self.key.key),
        )
        page_id = create_response.json()["id"]
        page = GlossaryTermPage.objects.get(pk=page_id)
        self.assertEqual(page.related_products.filter(is_auto=False).count(), 1)

        patch_response = self.client.patch(
            f"/glossary/{page_id}",
            json={"related_links": []},
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(patch_response.status_code, 200)
        self.assertEqual(patch_response.json()["related_links"], [])
        page.refresh_from_db()
        self.assertEqual(page.related_products.filter(is_auto=False).count(), 0)

    def test_create_and_patch_glossary_seo_fields(self):
        create_response = self.client.post(
            "/glossary/",
            json={
                "term": "Orgasm",
                "locale_code": "en",
                "seo_title": "Orgasm SEO Title",
                "search_description": "Orgasm meta description.",
            },
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(create_response.status_code, 201)
        page_id = create_response.json()["id"]
        self.assertEqual(create_response.json()["seo_title"], "Orgasm SEO Title")
        self.assertEqual(
            create_response.json()["search_description"],
            "Orgasm meta description.",
        )

        page = GlossaryTermPage.objects.get(pk=page_id)
        self.assertEqual(page.seo_title, "Orgasm SEO Title")
        self.assertEqual(page.search_description, "Orgasm meta description.")

        patch_response = self.client.patch(
            f"/glossary/{page_id}",
            json={
                "seo_title": "Updated SEO Title",
                "search_description": "Updated meta description.",
            },
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(patch_response.status_code, 200)
        self.assertEqual(patch_response.json()["seo_title"], "Updated SEO Title")
        self.assertEqual(
            patch_response.json()["search_description"],
            "Updated meta description.",
        )

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
        self.assertIn("pull_glossary_sync", tool_ids)
        self.assertIn(
            "glossary_wagtail_origin",
            response.json()["workflows"],
        )
        self.assertIn(
            "glossary_shopify_images",
            response.json()["workflows"],
        )


class HomeApiTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)
        self.key = ApiKey.objects.create(name="home-agent")
        locale = Locale.get_default()
        site_root = Page.get_first_root_node()
        if site_root is None:
            site_root = Page.add_root(instance=Page(title="Site Home", slug="site-home", locale=locale))

        self.home_parent = ShopifyRootPage.objects.filter(slug='cms-home').first()
        if self.home_parent is None:
            self.home_parent = ShopifyRootPage(title="CMS Home", slug="cms-home", locale=locale)
            site_root.add_child(instance=self.home_parent)
            self.home_parent.save_revision().publish()

    def test_create_and_get_home_page(self):
        response = self.client.post(
            "/home/",
            json={
                "hero_heading": "Shop Bold.",
                "hero_subheading": "Curated products.",
                "locale": "en-US",
            },
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 201)
        page_id = response.json()["id"]
        self.assertEqual(response.json()["hero_heading"], "Shop Bold.")
        self.assertEqual(response.json()["slug"], "home-en-us")
        self.assertEqual(response.json()["handle"], "home-en-us")
        sections = response.json()["sections_json"]["sections"]
        self.assertEqual(response.json()["sections_json"]["version"], 1)
        self.assertEqual(len(sections), 13)
        self.assertEqual(
            [section["type"] for section in sections],
            [
                "promo_gateway",
                "nav_collection_pills",
                "trust_bar",
                "featured_collections",
                "editorial_intro",
                "best_sellers",
                "shop_by_need",
                "educational_hub",
                "brand_values",
                "market_block",
                "faq",
                "internal_links",
                "seo_schema",
            ],
        )

        page = HomePage.objects.get(pk=page_id)
        self.assertEqual(page.get_parent().pk, self.home_parent.pk)
        self.assertEqual(len(page.body), 13)
        self.assertEqual(
            [block.block_type for block in page.body],
            [section["type"] for section in sections],
        )

        get_response = self.client.get(
            f"/home/{page_id}",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()["hero_subheading"], "Curated products.")

    def test_patch_typed_section_merges_and_keeps_envelope(self):
        create_response = self.client.post(
            "/home/",
            json={"hero_heading": "Shop Bold.", "locale": "en-US"},
            headers=_auth_headers(self.key.key),
        )
        page_id = create_response.json()["id"]

        patch_response = self.client.patch(
            f"/home/{page_id}",
            json={
                "editorial_intro": {
                    "heading": "Pleasure, made clear",
                    "body": "<p>Guides and body-safe picks.</p>",
                }
            },
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(patch_response.status_code, 200)
        by_type = {
            section["type"]: section["value"]
            for section in patch_response.json()["sections_json"]["sections"]
        }
        self.assertEqual(len(by_type), 13)
        self.assertEqual(by_type["editorial_intro"]["heading"], "Pleasure, made clear")
        self.assertEqual(by_type["editorial_intro"]["alignment"], "left")
        self.assertEqual(by_type["faq"]["heading"], "Frequently asked questions")
        self.assertTrue(by_type["seo_schema"]["include_faq_schema"])

        page = HomePage.objects.get(pk=page_id)
        self.assertEqual(len(page.body), 13)
        intro = next(block for block in page.body if block.block_type == "editorial_intro")
        self.assertEqual(intro.value["heading"], "Pleasure, made clear")
        faq = next(block for block in page.body if block.block_type == "faq")
        self.assertEqual(faq.value["heading"], "Frequently asked questions")

    @patch(
        "api.routers.home.sync_home_page",
        return_value=(True, "Home page synced to Shopify metaobject successfully."),
    )
    def test_push_home_page(self, mock_sync):
        create_response = self.client.post(
            "/home/",
            json={"hero_heading": "Shop Bold.", "locale": "en-US"},
            headers=_auth_headers(self.key.key),
        )
        page_id = create_response.json()["id"]

        push_response = self.client.post(
            f"/home/{page_id}/push",
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(push_response.status_code, 200)
        self.assertTrue(push_response.json()["success"])
        mock_sync.assert_called_once()


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
        self.assertIn("pull_glossary_sync", tool_ids)
        self.assertIn("push_location", tool_ids)
        self.assertIn("push_glossary_term", tool_ids)
        self.assertIn("push_home_page", tool_ids)
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
        self.assertIn("glossary_shopify_images", workflows)
        self.assertIn("home_wagtail_origin", workflows)


class OpenAPIAgentMetadataTests(TestCase):
    def test_pull_glossary_has_x_agent_fields(self):
        schema = get_schema(api=api, path_prefix="")
        operation = schema["paths"]["/glossary/pull"]["post"]
        self.assertEqual(operation["x-agent-capability-type"], "sync_inbound")
        self.assertEqual(operation["x-agent-resource"], "glossary")
        self.assertEqual(operation["x-agent-sync-direction"], "shopify_to_wagtail")

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

    def test_openapi_servers_has_absolute_url(self):
        """ChatGPT Actions rejects specs with empty/missing servers URLs."""
        schema = get_schema(api=api, path_prefix="/api/v1")
        servers = schema.get("servers") or []
        self.assertTrue(servers, "servers must not be empty")
        url = servers[0].get("url", "")
        self.assertTrue(
            url.startswith(("http://", "https://")),
            f"servers[0].url must be absolute, got {url!r}",
        )
        self.assertFalse(
            url.rstrip("/").endswith("/api/v1"),
            "server URL must be origin only; paths already include /api/v1",
        )

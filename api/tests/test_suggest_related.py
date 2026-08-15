import api.ninja_compat  # noqa: F401 — must run before any ninja import

from unittest.mock import patch

from django.test import TestCase, override_settings
from ninja.testing import TestClient
from wagtail.models import Locale, Page

from api.main import api
from api.models import ApiKey
from shopify_content.models import GlossaryTermPage, ShopifyRootPage


def _auth_headers(key: str) -> dict:
    return {"Authorization": f"Bearer {key}"}


class SuggestRelatedPagesApiTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)
        self.key = ApiKey.objects.create(name="suggest-agent")
        locale = Locale.get_default()
        home = Page.objects.first()
        if home is None:
            home = Page.add_root(instance=Page(title="Home", slug="home", locale=locale))
        glossary_parent = ShopifyRootPage(title="Glossary", slug="glossary", locale=locale)
        home.add_child(instance=glossary_parent)
        glossary_parent.save_revision().publish()
        self.term = GlossaryTermPage(
            title="Riding Crop",
            term="Riding Crop",
            slug="riding-crop",
            handle="riding-crop",
            locale=locale,
        )
        glossary_parent.add_child(instance=self.term)
        self.term.save_revision().publish()

    def test_requires_origin(self):
        response = self.client.post(
            "/semantic-links/suggest",
            json={"locale": "en-US"},
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 400)

    def test_rejects_page_id_and_text(self):
        response = self.client.post(
            "/semantic-links/suggest",
            json={
                "locale": "en-US",
                "page_id": self.term.pk,
                "text": "Chastity Belt",
                "page_type": "glossary",
            },
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 400)

    def test_requires_page_type_for_text(self):
        response = self.client.post(
            "/semantic-links/suggest",
            json={"locale": "en-US", "text": "Chastity Belt"},
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 400)

    def test_unknown_page_id_returns_404(self):
        response = self.client.post(
            "/semantic-links/suggest",
            json={"locale": "en-US", "page_id": 999999},
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 404)

    @override_settings(WAGTAIL_AI_PGVECTOR=True)
    @patch("api.routers.semantic_links.suggest_related_with_scores")
    def test_text_preview_returns_scored_candidates(self, mock_suggest):
        mock_suggest.return_value = {
            "product": [],
            "collection": [
                {
                    "id": 12,
                    "type": "collection",
                    "title": "BDSM",
                    "handle": "bdsm",
                    "score": 0.81,
                }
            ],
            "article": [],
            "glossary": [],
        }
        response = self.client.post(
            "/semantic-links/suggest",
            json={
                "locale": "en-US",
                "page_type": "glossary",
                "title": "Chastity Belt",
                "types": ["collection"],
                "limit_per_type": 20,
            },
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["page_type"], "glossary")
        self.assertEqual(body["limit_per_type"], 20)
        self.assertEqual(body["candidates"]["collection"][0]["score"], 0.81)
        kwargs = mock_suggest.call_args.kwargs
        self.assertEqual(kwargs["allowed_types"], ["collection"])
        self.assertEqual(kwargs["limit_per_type"], 20)
        self.assertIn("Chastity Belt", kwargs["content"])

    @override_settings(WAGTAIL_AI_PGVECTOR=True)
    @patch("api.routers.semantic_links.suggest_related_with_scores")
    def test_page_id_extracts_content_and_excludes_self(self, mock_suggest):
        mock_suggest.return_value = {
            "product": [],
            "collection": [],
            "article": [],
            "glossary": [],
        }
        response = self.client.post(
            "/semantic-links/suggest",
            json={"locale": "en-US", "page_id": self.term.pk, "exclude_page_id": 7},
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 200)
        kwargs = mock_suggest.call_args.kwargs
        self.assertIn(self.term.pk, kwargs["exclude_pks"])
        self.assertIn(7, kwargs["exclude_pks"])
        self.assertIn("Riding Crop", kwargs["content"])

    @override_settings(WAGTAIL_AI_PGVECTOR=False)
    def test_unavailable_index_returns_503(self):
        response = self.client.post(
            "/semantic-links/suggest",
            json={
                "locale": "en-US",
                "page_type": "glossary",
                "text": "Chastity Belt",
            },
            headers=_auth_headers(self.key.key),
        )
        self.assertEqual(response.status_code, 503)
        self.assertIn("detail", response.json())

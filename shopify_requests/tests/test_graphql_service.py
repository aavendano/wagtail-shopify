from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from django.test import TestCase, override_settings

from core.models import ShopConfig
from shopify_requests.graphql_service import AdminGraphqlResult, execute_admin_graphql


def _ok_gql_response(shop="s-test"):
    return SimpleNamespace(
        ok=True,
        shop=shop,
        data={"shop": {"id": "gid://shopify/Shop/1"}},
        extensions=None,
        log=SimpleNamespace(code="success", detail="ok"),
        response=SimpleNamespace(status=200, body="", headers={}),
    )


@override_settings(SHOPIFY_ADMIN_API_VERSION="2025-04")
class ExecuteAdminGraphqlTests(TestCase):
    @patch("shopify_requests.graphql_client.raw_admin_graphql")
    def test_uses_persisted_token_and_returns_data(self, mock_raw):
        ShopConfig.objects.create(
            shop="s-test",
            is_online=False,
            access_token="tok",
        )
        mock_raw.return_value = _ok_gql_response()

        app = MagicMock()
        result = execute_admin_graphql(
            "{ shop { id } }",
            shop="s-test",
            shopify_app=app,
        )

        self.assertIsInstance(result, AdminGraphqlResult)
        self.assertTrue(result.ok)
        self.assertEqual(result.data["shop"]["id"], "gid://shopify/Shop/1")
        mock_raw.assert_called_once()
        call_kw = mock_raw.call_args.kwargs
        self.assertEqual(call_kw["access_token"], "tok")
        self.assertEqual(call_kw["api_version"], "2025-04")

    def test_missing_token_without_verification(self):
        result = execute_admin_graphql(
            "{ shop { id } }",
            shop="s-test",
            shopify_app=MagicMock(),
        )
        self.assertFalse(result.ok)
        self.assertEqual(result.error_code, "missing_access_token")
        self.assertTrue(result.reauthorization_required)
        self.assertIsNone(result.raw)

    @patch("shopify_requests.graphql_client.raw_admin_graphql")
    def test_unauthorized_clears_local_tokens(self, mock_raw):
        ShopConfig.objects.create(
            shop="s-test",
            is_online=False,
            access_token="bad",
            refresh_token="r",
        )
        mock_raw.return_value = SimpleNamespace(
            ok=False,
            shop="s-test",
            data=None,
            extensions=None,
            log=SimpleNamespace(code="unauthorized", detail="nope"),
            response=SimpleNamespace(status=401, body="", headers={}),
        )

        execute_admin_graphql(
            "{ shop { id } }",
            shop="s-test",
            shopify_app=MagicMock(),
        )

        record = ShopConfig.objects.get(shop="s-test")
        self.assertIsNone(record.access_token)
        self.assertIsNone(record.refresh_token)

    @patch("shopify_requests.graphql_client.raw_admin_graphql")
    def test_propagates_invalid_token_response_to_client(self, mock_raw):
        ShopConfig.objects.create(
            shop="s-test",
            is_online=False,
            access_token="tok",
        )
        mock_raw.return_value = _ok_gql_response()
        retry = SimpleNamespace(status=401, body="", headers={})

        execute_admin_graphql(
            "{ shop { id } }",
            shop="s-test",
            invalid_token_response=retry,
            shopify_app=MagicMock(),
        )

        self.assertEqual(mock_raw.call_args.kwargs["invalid_token_response"], retry)

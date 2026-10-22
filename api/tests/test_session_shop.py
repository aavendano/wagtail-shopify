from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from shopify_config.membership import ensure_membership
from shopify_config.models import SHOP_MEMBERSHIP_ROLE_ADMIN, ShopConfig
from shopify_config.tenancy import SESSION_SHOP

User = get_user_model()


class SessionShopEndpointTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="editor", password="x", is_staff=True
        )
        ShopConfig.objects.create(shop="own.myshopify.com", access_token="tok")
        ensure_membership(
            self.user, "own.myshopify.com", role=SHOP_MEMBERSHIP_ROLE_ADMIN
        )
        self.client.force_login(self.user)

    def test_get_auto_seeds_sole_membership_shop(self):
        response = self.client.get("/api/v1/session-shop/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["shop"], "own.myshopify.com")
        self.assertEqual(data["shops"], ["own.myshopify.com"])
        self.assertEqual(self.client.session[SESSION_SHOP], "own.myshopify.com")

    def test_post_sets_session_shop(self):
        ShopConfig.objects.create(shop="other.myshopify.com", access_token="o")
        ensure_membership(self.user, "other.myshopify.com")
        response = self.client.post(
            "/api/v1/session-shop/",
            data={"shop": "other.myshopify.com"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["shop"], "other.myshopify.com")
        self.assertEqual(self.client.session[SESSION_SHOP], "other.myshopify.com")

    def test_post_forbidden_without_membership(self):
        ShopConfig.objects.create(shop="other.myshopify.com", access_token="o")
        response = self.client.post(
            "/api/v1/session-shop/",
            data={"shop": "other.myshopify.com"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)


class SessionEditorMembershipGateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="staff", password="x", is_staff=True
        )
        ShopConfig.objects.create(shop="own.myshopify.com", access_token="tok")
        self.client.force_login(self.user)

    def test_content_api_denied_without_membership(self):
        response = self.client.get("/api/v1/products/")
        self.assertEqual(response.status_code, 401)

    def test_content_api_allowed_with_membership(self):
        ensure_membership(self.user, "own.myshopify.com")
        response = self.client.get("/api/v1/products/")
        self.assertEqual(response.status_code, 200)

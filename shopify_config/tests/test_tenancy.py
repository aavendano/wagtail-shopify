from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase, override_settings

from shopify_config.membership import ensure_membership
from shopify_config.models import SHOP_MEMBERSHIP_ROLE_ADMIN, ShopConfig
from shopify_config.tenancy import (
    SESSION_SHOP,
    ShopUnresolvedError,
    ensure_session_shop,
    installed_shop_domains,
    is_installed_shop,
    normalize_shop,
    resolve_current_shop,
    resolve_shop_for_command,
    resolve_shop_for_command_or_sole,
    resolve_sole_installed_shop,
    set_session_shop,
)

User = get_user_model()


class NormalizeShopTests(TestCase):
    def test_normalize_handle_and_url(self):
        self.assertEqual(normalize_shop("Demo"), "demo.myshopify.com")
        self.assertEqual(
            normalize_shop("https://Demo.myshopify.com/admin"),
            "demo.myshopify.com",
        )
        self.assertEqual(normalize_shop(""), "")


class SoleInstalledShopTests(TestCase):
    def test_zero_shops_raises(self):
        with self.assertRaises(ShopUnresolvedError):
            resolve_sole_installed_shop()

    def test_one_shop(self):
        ShopConfig.objects.create(shop="solo", access_token="tok")
        self.assertEqual(resolve_sole_installed_shop(), "solo.myshopify.com")

    def test_two_shops_raises(self):
        ShopConfig.objects.create(shop="a.myshopify.com", access_token="a")
        ShopConfig.objects.create(shop="b.myshopify.com", access_token="b")
        with self.assertRaises(ShopUnresolvedError) as ctx:
            resolve_sole_installed_shop()
        self.assertIn("Multiple", str(ctx.exception))

    def test_installed_shop_domains_dedupes_handle_and_domain(self):
        ShopConfig.objects.create(shop="demo", access_token="tok")
        ShopConfig.objects.create(shop="demo.myshopify.com", access_token="tok2")
        self.assertEqual(installed_shop_domains(), ["demo.myshopify.com"])
        self.assertTrue(is_installed_shop("demo"))


class SessionShopTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="ed", password="x", is_staff=True)
        ShopConfig.objects.create(shop="own.myshopify.com", access_token="tok")
        ensure_membership(self.user, "own.myshopify.com", role=SHOP_MEMBERSHIP_ROLE_ADMIN)

    def test_resolve_current_shop_from_session(self):
        request = self.factory.get("/")
        request.session = {SESSION_SHOP: "own.myshopify.com"}
        request.user = self.user
        self.assertEqual(resolve_current_shop(request), "own.myshopify.com")

    def test_resolve_current_shop_raises_without_session(self):
        request = self.factory.get("/")
        request.session = {}
        request.user = self.user
        with self.assertRaises(ShopUnresolvedError):
            resolve_current_shop(request)

    def test_ensure_session_shop_sole_membership(self):
        request = self.factory.get("/")
        request.session = {}
        request.user = self.user
        self.assertEqual(ensure_session_shop(request), "own.myshopify.com")
        self.assertEqual(request.session[SESSION_SHOP], "own.myshopify.com")

    def test_ensure_session_shop_clears_unauthorized(self):
        ShopConfig.objects.create(shop="other.myshopify.com", access_token="o")
        request = self.factory.get("/")
        request.session = {SESSION_SHOP: "other.myshopify.com"}
        request.user = self.user
        self.assertEqual(ensure_session_shop(request), "own.myshopify.com")
        self.assertEqual(request.session[SESSION_SHOP], "own.myshopify.com")

    def test_set_session_shop_rejects_foreign(self):
        ShopConfig.objects.create(shop="other.myshopify.com", access_token="o")
        request = self.factory.get("/")
        request.session = {}
        request.user = self.user
        self.assertEqual(set_session_shop(request, "other.myshopify.com"), "")
        self.assertNotIn(SESSION_SHOP, request.session)

    def test_superuser_may_set_any_installed(self):
        ShopConfig.objects.create(shop="other.myshopify.com", access_token="o")
        admin = User.objects.create_superuser("su", "su@ex.com", "x")
        request = self.factory.get("/")
        request.session = {}
        request.user = admin
        self.assertEqual(set_session_shop(request, "other.myshopify.com"), "other.myshopify.com")


class CommandShopResolutionTests(TestCase):
    def test_explicit_shop(self):
        self.assertEqual(
            resolve_shop_for_command(shop="Acme"),
            "acme.myshopify.com",
        )

    @override_settings(SHOPIFY_PUBLICATION_SHOP="from-settings.myshopify.com")
    def test_settings_fallback(self):
        self.assertEqual(resolve_shop_for_command(), "from-settings.myshopify.com")

    @override_settings(SHOPIFY_PUBLICATION_SHOP="")
    def test_command_or_sole(self):
        ShopConfig.objects.create(shop="only.myshopify.com", access_token="t")
        self.assertEqual(resolve_shop_for_command_or_sole(), "only.myshopify.com")

from django.contrib.auth import get_user_model
from django.test import TestCase

from shopify_config.membership import (
    delete_memberships_for_shop,
    ensure_installer_user_and_membership,
    ensure_membership,
    staff_identity_from_claims,
    user_is_shop_admin,
    user_may_access_shop,
    user_shops,
)
from shopify_config.models import (
    SHOP_MEMBERSHIP_ROLE_ADMIN,
    SHOP_MEMBERSHIP_ROLE_EDITOR,
    ShopConfig,
    ShopMembership,
)

User = get_user_model()


class MembershipHelperTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ed", password="x", is_staff=True)
        ShopConfig.objects.create(shop="own.myshopify.com", access_token="tok")

    def test_ensure_membership_upgrades_not_downgrades(self):
        m = ensure_membership(self.user, "own.myshopify.com", role=SHOP_MEMBERSHIP_ROLE_ADMIN)
        self.assertEqual(m.role, SHOP_MEMBERSHIP_ROLE_ADMIN)
        m2 = ensure_membership(self.user, "own.myshopify.com", role=SHOP_MEMBERSHIP_ROLE_EDITOR)
        self.assertEqual(m2.role, SHOP_MEMBERSHIP_ROLE_ADMIN)

    def test_user_shops_and_access(self):
        ensure_membership(self.user, "own.myshopify.com")
        self.assertEqual(user_shops(self.user), ["own.myshopify.com"])
        self.assertTrue(user_may_access_shop(self.user, "own.myshopify.com"))
        self.assertFalse(user_may_access_shop(self.user, "other.myshopify.com"))
        self.assertFalse(user_is_shop_admin(self.user, "own.myshopify.com"))
        ensure_membership(self.user, "own.myshopify.com", role=SHOP_MEMBERSHIP_ROLE_ADMIN)
        self.assertTrue(user_is_shop_admin(self.user, "own.myshopify.com"))

    def test_superuser_sees_all_installed(self):
        ShopConfig.objects.create(shop="other.myshopify.com", access_token="o")
        admin = User.objects.create_superuser("su", "su@ex.com", "x")
        self.assertEqual(
            user_shops(admin),
            ["other.myshopify.com", "own.myshopify.com"],
        )

    def test_staff_identity_from_claims(self):
        self.assertEqual(
            staff_identity_from_claims({"email": "Ed@Shop.COM"}),
            ("ed@shop.com", "ed@shop.com"),
        )
        username, email = staff_identity_from_claims({"sub": "gid://shopify/User/99"})
        self.assertTrue(username.startswith("shopify:"))
        self.assertEqual(email, "")
        self.assertEqual(staff_identity_from_claims({}), ("", ""))

    def test_ensure_installer_user_and_membership(self):
        user = ensure_installer_user_and_membership(
            shop="own.myshopify.com",
            claims={"email": "installer@example.com"},
        )
        self.assertIsNotNone(user)
        self.assertTrue(user.is_staff)
        self.assertTrue(
            ShopMembership.objects.filter(
                user=user,
                shop="own.myshopify.com",
                role=SHOP_MEMBERSHIP_ROLE_ADMIN,
            ).exists()
        )
        self.assertIsNone(
            ensure_installer_user_and_membership(
                shop="own.myshopify.com",
                claims={},
            )
        )

    def test_delete_memberships_for_shop(self):
        ensure_membership(self.user, "own.myshopify.com")
        self.assertEqual(delete_memberships_for_shop("own"), 1)
        self.assertFalse(ShopMembership.objects.exists())

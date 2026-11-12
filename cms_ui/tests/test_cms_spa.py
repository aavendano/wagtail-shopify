import api.ninja_compat  # noqa: F401

from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import Client, TestCase, override_settings

from api.auth import user_is_cms_editor
from cms_ui.models import CmsSpaMount, default_cms_layout
from cms_ui.shop_auth import ensure_shop_editor_user, shop_editor_username


User = get_user_model()


class CmsSpaMountTests(TestCase):
    def test_bootstrap_includes_api_base_and_resources(self):
        mount = CmsSpaMount.objects.create(
            slug="cms",
            title="Merchant CMS",
            url_prefix="cms",
            layout=default_cms_layout(),
        )
        data = mount.get_bootstrap()
        self.assertEqual(data["apiBase"], "/api/v1")
        self.assertTrue(any(r["key"] == "glossary" for r in data["resources"]))
        self.assertIn("/glossary", data["layout"]["pages"])


class ShopEditorUserTests(TestCase):
    def test_ensure_shop_editor_user_creates_non_staff_editor(self):
        user = ensure_shop_editor_user("Test-Shop.myshopify.com")
        self.assertEqual(user.username, "shop_test-shop.myshopify.com")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.groups.filter(name="cms_editors").exists())

    def test_normalize_short_subdomain(self):
        user = ensure_shop_editor_user("demo")
        self.assertEqual(user.username, shop_editor_username("demo.myshopify.com"))


class CmsSpaShellTests(TestCase):
    def setUp(self):
        CmsSpaMount.objects.create(
            slug="cms",
            title="Merchant CMS",
            url_prefix="cms",
            layout=default_cms_layout(),
        )
        self.user = User.objects.create_user(
            username="editor",
            password="pass",
            is_staff=True,
        )

    def test_cms_requires_login(self):
        client = Client()
        response = client.get("/cms/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin-django/login/", response["Location"])

    def test_cms_shell_for_staff(self):
        client = Client()
        client.force_login(self.user)
        response = client.get("/cms/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cms-spa-root")
        self.assertContains(response, "__CMS_BOOTSTRAP__")
        self.assertContains(response, "shopifycloud/app-bridge.js")
        self.assertContains(response, 'href="/cms/"')

    @override_settings(SHOPIFY_API_KEY="test-key", SHOPIFY_API_SECRET="test-secret")
    @patch("cms_ui.views.get_shopify_app")
    def test_cms_shell_from_app_home_verify(self, mocked_get_shopify_app):
        mocked_get_shopify_app.return_value.verify_app_home_req.return_value = SimpleNamespace(
            ok=True,
            shop="test-shop.myshopify.com",
            response=SimpleNamespace(
                headers={
                    "Content-Security-Policy": (
                        "frame-ancestors https://test-shop.myshopify.com;"
                    ),
                }
            ),
        )
        client = Client()
        response = client.get("/cms/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cms-spa-root")
        self.assertContains(response, "shopifycloud/app-bridge.js")
        self.assertEqual(
            response["Content-Security-Policy"],
            "frame-ancestors https://test-shop.myshopify.com;",
        )

        user = User.objects.get(username="shop_test-shop.myshopify.com")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.groups.filter(name="cms_editors").exists())
        self.assertEqual(int(client.session["_auth_user_id"]), user.pk)

        api_response = client.get("/api/v1/capabilities/")
        self.assertEqual(api_response.status_code, 200)
        self.assertIn("tools", api_response.json())

    @override_settings(SHOPIFY_API_KEY="test-key", SHOPIFY_API_SECRET="test-secret")
    @patch("cms_ui.views.get_shopify_app")
    def test_cms_verify_failure_redirects_to_login(self, mocked_get_shopify_app):
        mocked_get_shopify_app.return_value.verify_app_home_req.return_value = SimpleNamespace(
            ok=False,
            response=SimpleNamespace(status=401, headers={}, body="unauthorized"),
        )
        client = Client()
        response = client.get("/cms/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin-django/login/", response["Location"])


class SessionEditorAuthTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            username="staff",
            password="pass",
            is_staff=True,
        )
        self.editor = User.objects.create_user(username="editor", password="pass")
        group = Group.objects.create(name="cms_editors")
        self.editor.groups.add(group)
        self.anon = User.objects.create_user(username="anon", password="pass")

    def test_user_is_cms_editor_helpers(self):
        self.assertTrue(user_is_cms_editor(self.staff))
        self.assertTrue(user_is_cms_editor(self.editor))
        self.assertFalse(user_is_cms_editor(self.anon))

    def test_session_auth_lists_capabilities(self):
        django_client = Client()
        django_client.force_login(self.staff)
        response = django_client.get("/api/v1/capabilities/")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("tools", payload)


@override_settings(CMS_RESTRICT_WAGTAIL_ADMIN=True)
class RestrictWagtailAdminTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            username="staff",
            password="pass",
            is_staff=True,
        )
        self.ops = User.objects.create_user(
            username="ops",
            password="pass",
            is_staff=True,
            is_superuser=True,
        )

    def test_staff_blocked_from_wagtail_admin(self):
        client = Client()
        client.force_login(self.staff)
        response = client.get("/admin/")
        self.assertEqual(response.status_code, 403)

    def test_superuser_allowed(self):
        client = Client()
        client.force_login(self.ops)
        response = client.get("/admin/")
        # Wagtail may redirect to login dashboard; not 403
        self.assertNotEqual(response.status_code, 403)

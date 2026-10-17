import os
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase


class EnsureSuperuserCommandTests(TestCase):
    def tearDown(self):
        for key in (
            "ADMIN_USERNAME",
            "ADMIN_PASSWORD",
            "ADMIN_EMAIL",
            "ADMIN_UPDATE_PASSWORD",
            "DJANGO_SUPERUSER_USERNAME",
            "DJANGO_SUPERUSER_PASSWORD",
            "DJANGO_SUPERUSER_EMAIL",
            "DJANGO_SUPERUSER_UPDATE_PASSWORD",
        ):
            os.environ.pop(key, None)

    def test_creates_superuser_from_admin_env(self):
        os.environ["ADMIN_USERNAME"] = "plt-admin"
        os.environ["ADMIN_PASSWORD"] = "plt-pass"
        os.environ["ADMIN_EMAIL"] = "plt@example.com"
        out = StringIO()
        call_command("ensure_superuser", stdout=out)
        user = get_user_model().objects.get(username="plt-admin")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.check_password("plt-pass"))
        self.assertIn("Created superuser", out.getvalue())

    def test_prefers_admin_over_django_superuser(self):
        os.environ["ADMIN_USERNAME"] = "from-admin"
        os.environ["ADMIN_PASSWORD"] = "admin-pass"
        os.environ["DJANGO_SUPERUSER_USERNAME"] = "from-django"
        os.environ["DJANGO_SUPERUSER_PASSWORD"] = "django-pass"
        call_command("ensure_superuser")
        User = get_user_model()
        self.assertTrue(User.objects.filter(username="from-admin").exists())
        self.assertFalse(User.objects.filter(username="from-django").exists())

    def test_update_password_when_flag_set(self):
        User = get_user_model()
        User.objects.create_superuser(
            username="alejandro", email="a@localhost", password="old-pass"
        )
        os.environ["ADMIN_USERNAME"] = "alejandro"
        os.environ["ADMIN_PASSWORD"] = "new-pass"
        out = StringIO()
        call_command("ensure_superuser", update_password=True, stdout=out)
        user = User.objects.get(username="alejandro")
        self.assertTrue(user.check_password("new-pass"))
        self.assertIn("Updated superuser", out.getvalue())

    def test_noop_when_env_missing(self):
        out = StringIO()
        call_command("ensure_superuser", stdout=out)
        self.assertIn("skipped", out.getvalue())
        self.assertFalse(get_user_model().objects.exists())

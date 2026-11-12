"""Create or update the Django superuser from environment variables (deploy bootstrap)."""

from __future__ import annotations

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


def _truthy(name: str) -> bool:
    return os.environ.get(name, "").lower() in {"1", "true", "yes", "on"}


def _env(*names: str) -> str:
    for name in names:
        value = (os.environ.get(name) or "").strip()
        if value:
            return value
    return ""


class Command(BaseCommand):
    help = (
        "Ensure a superuser exists using ADMIN_* (preferred) or DJANGO_SUPERUSER_* "
        "env vars, or --username / --password flags."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            help="Override ADMIN_USERNAME / DJANGO_SUPERUSER_USERNAME",
        )
        parser.add_argument(
            "--password",
            help="Override ADMIN_PASSWORD / DJANGO_SUPERUSER_PASSWORD",
        )
        parser.add_argument(
            "--email",
            help="Override ADMIN_EMAIL / DJANGO_SUPERUSER_EMAIL",
        )
        parser.add_argument(
            "--update-password",
            action="store_true",
            help="Reset password when the user already exists",
        )

    def handle(self, *args, **options):
        username = (
            (options.get("username") or "").strip()
            or _env("ADMIN_USERNAME", "DJANGO_SUPERUSER_USERNAME")
        )
        password = options.get("password") or _env(
            "ADMIN_PASSWORD", "DJANGO_SUPERUSER_PASSWORD"
        )
        update_password = bool(options.get("update_password")) or _truthy(
            "ADMIN_UPDATE_PASSWORD"
        ) or _truthy("DJANGO_SUPERUSER_UPDATE_PASSWORD")

        if not username or not password:
            self.stdout.write(
                "ensure_superuser: skipped (set ADMIN_USERNAME and ADMIN_PASSWORD, "
                "or DJANGO_SUPERUSER_USERNAME / DJANGO_SUPERUSER_PASSWORD, "
                "or pass --username / --password)."
            )
            return

        email = (
            (options.get("email") or "").strip()
            or _env("ADMIN_EMAIL", "DJANGO_SUPERUSER_EMAIL")
            or f"{username}@localhost"
        )
        User = get_user_model()

        existing = User.objects.filter(username=username).first()
        if existing is not None:
            changed = False
            if update_password:
                existing.set_password(password)
                changed = True
            if not existing.is_staff:
                existing.is_staff = True
                changed = True
            if not existing.is_superuser:
                existing.is_superuser = True
                changed = True
            if not existing.is_active:
                existing.is_active = True
                changed = True
            if email and existing.email != email:
                existing.email = email
                changed = True
            if changed:
                existing.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Updated superuser {username!r}.")
                )
            else:
                self.stdout.write(
                    f"Superuser {username!r} already exists; set "
                    "ADMIN_UPDATE_PASSWORD=true or --update-password to reset password."
                )
            return

        User.objects.create_superuser(
            username=username, email=email, password=password
        )
        self.stdout.write(self.style.SUCCESS(f"Created superuser {username!r}."))

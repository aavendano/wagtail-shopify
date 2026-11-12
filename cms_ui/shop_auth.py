from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

CMS_EDITORS_GROUP = "cms_editors"


def normalize_shop_domain(shop: str) -> str:
    """Normalize a shop identifier to lowercase ``*.myshopify.com``."""
    value = (shop or "").strip().lower()
    value = value.replace("https://", "").replace("http://", "").split("/")[0]
    if not value:
        return ""
    if not value.endswith(".myshopify.com"):
        value = f"{value}.myshopify.com"
    return value


def shop_editor_username(shop: str) -> str:
    domain = normalize_shop_domain(shop)
    return f"shop_{domain}"


def ensure_shop_editor_user(shop: str):
    """
    Get or create a non-staff Django user for a verified Shopify shop.

    Username: ``shop_<domain>``. Ensures membership in ``cms_editors``.
    """
    domain = normalize_shop_domain(shop)
    if not domain:
        raise ValueError("shop domain is required")

    User = get_user_model()
    username = shop_editor_username(domain)
    user, _created = User.objects.get_or_create(
        username=username,
        defaults={
            "is_staff": False,
            "is_superuser": False,
        },
    )
    group, _ = Group.objects.get_or_create(name=CMS_EDITORS_GROUP)
    if not user.groups.filter(pk=group.pk).exists():
        user.groups.add(group)
    return user

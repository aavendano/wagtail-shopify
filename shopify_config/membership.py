"""User↔shop membership helpers (deploy-per-shop tenancy).

Editorial Django permissions stay global; membership gates the shop tenant.
"""

from __future__ import annotations

import re
from typing import Any

from django.contrib.auth import get_user_model
from django.db import transaction

from shopify_config.models import (
    SHOP_MEMBERSHIP_ROLE_ADMIN,
    SHOP_MEMBERSHIP_ROLE_EDITOR,
    ShopMembership,
)
from shopify_config.tenancy import installed_shop_domains, is_installed_shop, normalize_shop

User = get_user_model()

_ROLE_RANK = {
    SHOP_MEMBERSHIP_ROLE_EDITOR: 1,
    SHOP_MEMBERSHIP_ROLE_ADMIN: 2,
}


def user_shops(user) -> list[str]:
    """Normalized shops the user may access (sorted). Superuser → all installed."""
    if user is None or not getattr(user, "is_authenticated", False):
        return []
    if getattr(user, "is_superuser", False):
        return installed_shop_domains()
    return sorted(
        {
            normalize_shop(raw)
            for raw in ShopMembership.objects.filter(user=user).values_list("shop", flat=True)
            if normalize_shop(raw)
        }
    )


def user_may_access_shop(user, shop: str | None) -> bool:
    """True when the user may operate on ``shop`` (superuser or membership)."""
    normalized = normalize_shop(shop)
    if not normalized:
        return False
    if user is None or not getattr(user, "is_authenticated", False):
        return False
    if getattr(user, "is_superuser", False):
        return True
    return ShopMembership.objects.filter(user=user, shop=normalized).exists()


def user_is_shop_admin(user, shop: str | None) -> bool:
    """True when the user is shop admin or Django superuser."""
    normalized = normalize_shop(shop)
    if not normalized:
        return False
    if user is None or not getattr(user, "is_authenticated", False):
        return False
    if getattr(user, "is_superuser", False):
        return True
    return ShopMembership.objects.filter(
        user=user,
        shop=normalized,
        role=SHOP_MEMBERSHIP_ROLE_ADMIN,
    ).exists()


def ensure_membership(
    user, shop: str | None, *, role: str = SHOP_MEMBERSHIP_ROLE_EDITOR
) -> ShopMembership:
    """Create or upgrade membership. Never downgrade admin → editor."""
    normalized = normalize_shop(shop)
    if user is None or not normalized:
        raise ValueError("user and shop are required")
    if role not in _ROLE_RANK:
        role = SHOP_MEMBERSHIP_ROLE_EDITOR

    with transaction.atomic():
        membership, created = ShopMembership.objects.select_for_update().get_or_create(
            user=user,
            shop=normalized,
            defaults={"role": role},
        )
        if created:
            return membership
        if _ROLE_RANK.get(role, 0) > _ROLE_RANK.get(membership.role, 0):
            membership.role = role
            membership.save(update_fields=["role", "updated_at"])
        return membership


def staff_identity_from_claims(claims: dict[str, Any] | None) -> tuple[str, str]:
    """Extract (username, email) from Shopify session-token claims.

    Returns ("", "") when no usable staff identity is present.
    Prefer email when present; otherwise a stable ``shopify:{sub}`` username.
    """
    if not isinstance(claims, dict):
        return "", ""
    email = str(claims.get("email") or "").strip().lower()
    sub = str(claims.get("sub") or "").strip()
    if email and "@" in email:
        username = re.sub(r"[^a-z0-9._+-@]", "-", email)[:150]
        return username, email
    if not sub:
        return "", ""
    slug = re.sub(r"[^a-zA-Z0-9._-]", "-", sub).strip("-")[:120]
    if not slug:
        return "", ""
    return f"shopify:{slug}"[:150], ""


def ensure_installer_user_and_membership(
    *,
    shop: str | None,
    claims: dict[str, Any] | None,
) -> User | None:
    """Upsert Django user + admin membership from App Home staff claims.

    Returns None when claims lack a staff identity (no invented membership).
    Marks the user as staff so they satisfy CMS session auth.
    """
    normalized = normalize_shop(shop)
    username, email = staff_identity_from_claims(claims)
    if not normalized or not username:
        return None

    with transaction.atomic():
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_active": True,
                "is_staff": True,
            },
        )
        update_fields: list[str] = []
        if not created and email and not user.email:
            user.email = email
            update_fields.append("email")
        if not user.is_staff:
            user.is_staff = True
            update_fields.append("is_staff")
        if not user.is_active:
            user.is_active = True
            update_fields.append("is_active")
        if update_fields:
            user.save(update_fields=update_fields)
        ensure_membership(user, normalized, role=SHOP_MEMBERSHIP_ROLE_ADMIN)
    return user


def delete_memberships_for_shop(shop: str | None) -> int:
    """Delete all memberships for ``shop`` (and handle variants). Returns count."""
    normalized = normalize_shop(shop)
    if not normalized:
        return 0
    handle = normalized.removesuffix(".myshopify.com")
    deleted, _ = ShopMembership.objects.filter(shop__in=[normalized, handle]).delete()
    return deleted

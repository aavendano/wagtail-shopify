from django.conf import settings
from django.db import models

SHOP_MEMBERSHIP_ROLE_EDITOR = "editor"
SHOP_MEMBERSHIP_ROLE_ADMIN = "admin"
SHOP_MEMBERSHIP_ROLE_CHOICES = (
    (SHOP_MEMBERSHIP_ROLE_EDITOR, "Editor"),
    (SHOP_MEMBERSHIP_ROLE_ADMIN, "Admin"),
)


class ShopConfig(models.Model):
    shop = models.CharField(max_length=255, unique=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    is_online = models.BooleanField(default=False)
    scope = models.TextField(blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    access_token = models.CharField(max_length=255, null=True, blank=True)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)
    refresh_token_expires = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "core_shopconfig"

    def __str__(self):
        return self.shop


class ShopMembership(models.Model):
    """N:M link between a Django user and a Shopify shop tenant.

    Editorial Django permissions stay global; membership authorizes the tenant only.
    AUTH_USER_MODEL is unchanged (default Django User).
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="shop_memberships",
        verbose_name="User",
    )
    shop = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name="Shop",
        help_text="Normalized shop domain (same value as ShopConfig.shop).",
    )
    role = models.CharField(
        max_length=32,
        choices=SHOP_MEMBERSHIP_ROLE_CHOICES,
        default=SHOP_MEMBERSHIP_ROLE_EDITOR,
        verbose_name="Role",
        help_text="editor: CMS on this shop; admin: installer / shop operator.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Shop membership"
        verbose_name_plural = "Shop memberships"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "shop"],
                name="shopify_config_shopmembership_user_shop_uniq",
            ),
        ]
        indexes = [
            models.Index(
                fields=["shop", "role"],
                name="sc_shopmem_shop_role_idx",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user_id}@{self.shop} ({self.role})"

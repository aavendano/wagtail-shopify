# ShopMembership + sole-shop staff backfill

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def backfill_sole_shop_staff_memberships(apps, schema_editor):
    """If exactly one ShopConfig exists, grant admin membership to is_staff users."""
    ShopConfig = apps.get_model("shopify_config", "ShopConfig")
    ShopMembership = apps.get_model("shopify_config", "ShopMembership")
    User = apps.get_model(settings.AUTH_USER_MODEL)

    shops = list(ShopConfig.objects.values_list("shop", flat=True))
    # Normalize like tenancy.normalize_shop (inline to avoid import during migrate).
    normalized = []
    for raw in shops:
        value = (raw or "").strip().lower()
        if not value:
            continue
        value = value.removeprefix("https://").removeprefix("http://").split("/")[0]
        if value and not value.endswith(".myshopify.com"):
            value = f"{value}.myshopify.com"
        if value:
            normalized.append(value)
    unique = sorted(set(normalized))
    if len(unique) != 1:
        return
    shop = unique[0]
    for user in User.objects.filter(is_staff=True, is_active=True):
        ShopMembership.objects.get_or_create(
            user_id=user.pk,
            shop=shop,
            defaults={"role": "admin"},
        )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("shopify_config", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ShopMembership",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "shop",
                    models.CharField(
                        db_index=True,
                        help_text="Normalized shop domain (same value as ShopConfig.shop).",
                        max_length=255,
                        verbose_name="Shop",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[("editor", "Editor"), ("admin", "Admin")],
                        default="editor",
                        help_text="editor: CMS on this shop; admin: installer / shop operator.",
                        max_length=32,
                        verbose_name="Role",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shop_memberships",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "Shop membership",
                "verbose_name_plural": "Shop memberships",
            },
        ),
        migrations.AddConstraint(
            model_name="shopmembership",
            constraint=models.UniqueConstraint(
                fields=("user", "shop"),
                name="shopify_config_shopmembership_user_shop_uniq",
            ),
        ),
        migrations.AddIndex(
            model_name="shopmembership",
            index=models.Index(
                fields=["shop", "role"],
                name="sc_shopmem_shop_role_idx",
            ),
        ),
        migrations.RunPython(backfill_sole_shop_staff_memberships, noop_reverse),
    ]

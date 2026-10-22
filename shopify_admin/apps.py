from django.apps import AppConfig


class ShopifyAdminConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shopify_admin"
    verbose_name = "Shopify Admin (embedded UI)"

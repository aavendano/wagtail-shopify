from django.apps import AppConfig


class ShopifyConfigConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shopify_config"
    label = "shopify_config"
    verbose_name = "Shopify shop config (tokens)"

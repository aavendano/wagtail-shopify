from django.apps import AppConfig


class ShopifyContentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shopify_content'
    verbose_name = 'Shopify Content'

    def ready(self):
        import shopify_content.wagtail_hooks  # noqa: F401

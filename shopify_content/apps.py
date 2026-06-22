from django.apps import AppConfig


class ShopifyContentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shopify_content'
    verbose_name = 'Shopify Content'

    def ready(self):
        import shopify_content.wagtail_hooks  # noqa: F401
        from shopify_content.signals import register_publish_signals
        from shopify_content.publish_debug import register_publish_debug_handlers

        register_publish_signals()
        register_publish_debug_handlers()

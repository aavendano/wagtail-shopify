from django.apps import AppConfig


class ShopifyContentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shopify_content'
    verbose_name = 'Shopify Content'

    def ready(self):
        import shopify_content.wagtail_ai_setup  # noqa: F401
        import shopify_content.indexes  # noqa: F401
        from shopify_content.wagtail_ai_fixes import install_suggested_content_fallback

        install_suggested_content_fallback()
        import shopify_content.wagtail_hooks  # noqa: F401
        from shopify_content.signals import register_publish_signals

        register_publish_signals()

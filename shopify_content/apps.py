from django.apps import AppConfig


class ShopifyContentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shopify_content'
    verbose_name = 'Shopify Content'

    def ready(self):
        import shopify_content.wagtail_ai_setup  # noqa: F401
        # Patch django-ai-core before PageIndex registration / indexing runs.
        from shopify_content.vector_index_tracking_fix import (
            install_stable_index_name_fix,
        )

        install_stable_index_name_fix()
        import shopify_content.indexes  # noqa: F401
        from shopify_content.wagtail_ai_fixes import install_suggested_content_fallback

        install_suggested_content_fallback()
        import shopify_content.wagtail_hooks  # noqa: F401
        from shopify_content.signals import register_publish_signals

        register_publish_signals()

        from shopify_content.content_store.signals import (
            register_content_store_signals,
        )

        register_content_store_signals()

        # Phase E: keep the public outbound function stable while making
        # LocationPage RichText publication consume page.editorial.<field>.
        from shopify_content.sync.location_editorial import (
            install_location_editorial_sync,
        )

        install_location_editorial_sync()

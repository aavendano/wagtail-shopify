from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Django platform ops only (e.g. ensure_superuser).

    Shopify UI lives in ``shopify_admin``; ShopConfig/tokens in ``shopify_config``.
    This app must not import or depend on the Shopify graph.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Django platform"

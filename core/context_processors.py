from django.conf import settings

from .embedded_urls import embedded_app_home_url, embedded_cms_url


def shopify_context(request):
    return {
        "SHOPIFY_API_KEY": settings.SHOPIFY_API_KEY,
        "SHOPIFY_API_SECRET": settings.SHOPIFY_API_SECRET,
        "embedded_home_url": embedded_app_home_url(request, ops=False),
        "embedded_ops_url": embedded_app_home_url(request, ops=True),
        "embedded_cms_url": embedded_cms_url(request),
    }

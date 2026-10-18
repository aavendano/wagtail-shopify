from django.conf import settings


def shopify_context(request):
    return {
        "SHOPIFY_API_KEY": settings.SHOPIFY_API_KEY,
        "SHOPIFY_API_SECRET": settings.SHOPIFY_API_SECRET,
    }

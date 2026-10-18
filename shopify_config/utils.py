import logging
from functools import lru_cache

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from shopify_app import ShopifyApp

logger = logging.getLogger(__name__)


def _get_attr(value, key, default=None):
    if isinstance(value, dict):
        return value.get(key, default)
    return getattr(value, key, default)


@lru_cache(maxsize=1)
def get_shopify_app():
    if not settings.SHOPIFY_API_KEY:
        raise ImproperlyConfigured("SHOPIFY_API_KEY is required.")
    if not settings.SHOPIFY_API_SECRET:
        raise ImproperlyConfigured("SHOPIFY_API_SECRET is required.")

    return ShopifyApp(
        client_id=settings.SHOPIFY_API_KEY,
        client_secret=settings.SHOPIFY_API_SECRET,
    )


def request_to_shopify_req(request):
    body = request.body.decode("utf-8") if request.body else ""
    return {
        "method": request.method,
        "headers": dict(request.headers),
        "url": request.build_absolute_uri(),
        "body": body,
    }


def shopify_result_to_django_response(result):
    response_payload = _get_attr(result, "response", {})
    status = _get_attr(response_payload, "status", 200)
    body = _get_attr(response_payload, "body", "")
    headers = _get_attr(response_payload, "headers", {}) or {}

    response = HttpResponse(body, status=status)
    for key, value in headers.items():
        response[key] = value
    return response


def log_shopify_result(result):
    log_payload = _get_attr(result, "log", {})
    code = _get_attr(log_payload, "code", "unknown")
    detail = _get_attr(log_payload, "detail", "")
    logger.info("shopify_oauth_result code=%s detail=%s", code, detail)


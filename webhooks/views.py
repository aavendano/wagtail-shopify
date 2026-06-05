import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from core.utils import (
    get_shopify_app,
    log_shopify_result,
    request_to_shopify_req,
    shopify_result_to_django_response,
)

from .handlers import handle_app_scopes_update, handle_app_uninstalled

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def app_uninstalled(request):
    shopify_app = get_shopify_app()
    req = request_to_shopify_req(request)
    result = shopify_app.verify_webhook_req(req)
    log_shopify_result(result)
    if not getattr(result, "ok", False):
        return shopify_result_to_django_response(result)
    shop = getattr(result, "shop", None)
    logger.info("shopify_webhook topic=app/uninstalled shop=%s", shop)
    handle_app_uninstalled(shop, request.body)
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
def app_scopes_update(request):
    shopify_app = get_shopify_app()
    req = request_to_shopify_req(request)
    result = shopify_app.verify_webhook_req(req)
    log_shopify_result(result)
    if not getattr(result, "ok", False):
        return shopify_result_to_django_response(result)
    shop = getattr(result, "shop", None)
    logger.info("shopify_webhook topic=app/scopes_update shop=%s", shop)
    handle_app_scopes_update(shop, request.body)
    return HttpResponse(status=200)

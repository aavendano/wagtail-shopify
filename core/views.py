from urllib.parse import urlencode

import json
import logging
import time

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from shopify_content.sync.service import VALID_IMPORT_RESOURCES
from shopify_content.sync.task_dispatch import enqueue_shopify_import

from .embedded_redirects import (
    validate_parent_redirect_url,
    validate_relative_app_path,
)
from .forms import ShopConfigForm
from .shop_config_lookup import get_shop_config, shop_has_access_token
from .mixins import AppHomeVerifiedMixin
from .utils import (
    get_shopify_app,
    log_shopify_result,
    request_to_shopify_req,
    shopify_result_to_django_response,
)
from .token_service import ensure_offline_token_lifecycle
from shopify_requests.domains.shop import fetch_shop_admin_graphql

logger = logging.getLogger(__name__)

# #region agent log
_DEBUG_LOG_PATH = "/home/alejandro/apps/wagtail-shopify/.cursor/debug-e48ec5.log"


def _agent_log(location, message, data=None, hypothesis_id=""):
    try:
        with open(_DEBUG_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {
                        "sessionId": "e48ec5",
                        "timestamp": int(time.time() * 1000),
                        "location": location,
                        "message": message,
                        "data": data or {},
                        "hypothesisId": hypothesis_id,
                        "runId": "pre-fix",
                    }
                )
                + "\n"
            )
    except OSError:
        pass


# #endregion


SYNC_RESOURCES = [
    ('products', 'Importar productos nuevos'),
    ('collections', 'Importar colecciones nuevas'),
    ('blogs', 'Importar blogs y artículos nuevos'),
    ('all', 'Importar todo lo nuevo'),
]


def _redirect_home_preserving_query(request):
    url = reverse('home')
    if request.GET:
        url = f'{url}?{request.GET.urlencode()}'
    return redirect(url)


def _shop_config_context(shop=None):
    config = get_shop_config(shop)
    return {
        'shop_configured': shop_has_access_token(shop),
        'shop_domain': config.shop if config else None,
    }


class PublicEntryView(TemplateView):
    template_name = "core/public_entry.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = context.get("form") or ShopConfigForm()
        return context


class AuthLoginView(TemplateView):
    template_name = "core/public_entry.html"

    def _oauth_install_redirect(self, shop):
        querystring = urlencode({"client_id": settings.SHOPIFY_API_KEY})
        shop_name = shop.replace(".myshopify.com", "")
        shop_name = shop_name.replace("https://", "")
        shop_name = shop_name.replace("/", "")
        return redirect(f"https://admin.shopify.com/store/{shop_name}/oauth/install?{querystring}")

    def _handle_login_request(self, data):
        form = ShopConfigForm(data=data or None)
        if form.is_valid():
            return self._oauth_install_redirect(form.cleaned_data["shop"])
        return self.render_to_response(self.get_context_data(form=form))



    def post(self, request, *args, **kwargs):
        return self._handle_login_request(request.POST)


class HomeView(AppHomeVerifiedMixin, TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        # #region agent log
        _agent_log("core/views.py:HomeView:get_context_data:entry", "Building home context", {}, "H2")
        # #endregion
        try:
            context = super().get_context_data(**kwargs)
            verification_result = getattr(self, "_verification_result", None)
            verified_shop = (
                getattr(verification_result, "shop", None) if verification_result else None
            )
            context.update(_shop_config_context(verified_shop))
            context['sync_resources'] = SYNC_RESOURCES
            self._admin_graphql_halt = None
            shop = verified_shop
            if shop:
                gql = fetch_shop_admin_graphql(
                    shop,
                    verification_result=verification_result,
                    invalid_token_response=getattr(
                        verification_result, "new_id_token_response", None
                    ),
                    shopify_app=getattr(self, "_shopify_app", None),
                )
                # #region agent log
                _agent_log(
                    "core/views.py:HomeView:get_context_data:graphql",
                    "Shop admin GraphQL result",
                    {"ok": gql.ok, "has_data": bool(gql.data), "has_halt": gql.raw is not None},
                    "H2",
                )
                # #endregion
                if not gql.ok and gql.raw is not None:
                    self._admin_graphql_halt = gql.raw
                elif gql.ok and gql.data:
                    shop_node = gql.data.get("shop") or {}
                    context["shopify_admin_shop_id"] = shop_node.get("id")
                    context["shopify_admin_shop_name"] = shop_node.get("name")
            # #region agent log
            _agent_log(
                "core/views.py:HomeView:get_context_data:exit",
                "Home context ready",
                {"shop_configured": context.get("shop_configured"), "shop": verified_shop},
                "H2",
            )
            # #endregion
            return context
        except Exception as exc:
            # #region agent log
            _agent_log(
                "core/views.py:HomeView:get_context_data:exception",
                "Exception in get_context_data",
                {"type": type(exc).__name__, "error": str(exc)},
                "H2",
            )
            # #endregion
            raise

    def dispatch_after_verified(self, request, *args, **kwargs):
        # #region agent log
        _agent_log(
            "core/views.py:HomeView:dispatch_after_verified:entry",
            "Ensuring offline token lifecycle",
            {"shop": getattr(self._verification_result, "shop", None)},
            "H1",
        )
        # #endregion
        try:
            token_result = ensure_offline_token_lifecycle(
                self._verification_result, self._shopify_app
            )
            # #region agent log
            _agent_log(
                "core/views.py:HomeView:dispatch_after_verified:token",
                "Token lifecycle result",
                {
                    "has_token_result": token_result is not None,
                    "token_ok": getattr(token_result, "ok", None) if token_result else None,
                },
                "H1",
            )
            # #endregion
            if token_result is not None:
                # #region agent log
                _resp = getattr(token_result, "response", None)
                _log = getattr(token_result, "log", None)
                _agent_log(
                    "core/views.py:HomeView:dispatch_after_verified:return_token",
                    "Returning SDK token failure response",
                    {
                        "token_ok": getattr(token_result, "ok", None),
                        "log_code": getattr(_log, "code", None)
                        if not isinstance(_log, dict)
                        else _log.get("code"),
                        "response_status": getattr(_resp, "status", None)
                        if _resp is not None
                        else None,
                        "response_body_len": len(getattr(_resp, "body", "") or ""),
                        "headers_type": type(getattr(_resp, "headers", None)).__name__,
                    },
                    "H1",
                )
                # #endregion
                try:
                    django_resp = shopify_result_to_django_response(token_result)
                    # #region agent log
                    _agent_log(
                        "core/views.py:HomeView:dispatch_after_verified:django_resp",
                        "Converted token result to Django response",
                        {"status_code": django_resp.status_code, "body_len": len(django_resp.content)},
                        "H2",
                    )
                    # #endregion
                    return django_resp
                except Exception as conv_exc:
                    # #region agent log
                    _agent_log(
                        "core/views.py:HomeView:dispatch_after_verified:conv_exc",
                        "shopify_result_to_django_response failed",
                        {"type": type(conv_exc).__name__, "error": str(conv_exc)},
                        "H2",
                    )
                    # #endregion
                    raise
            return super(AppHomeVerifiedMixin, self).dispatch(request, *args, **kwargs)
        except Exception as exc:
            # #region agent log
            _agent_log(
                "core/views.py:HomeView:dispatch_after_verified:exception",
                "Exception in dispatch_after_verified",
                {"type": type(exc).__name__, "error": str(exc)},
                "H1",
            )
            # #endregion
            raise

    def render_to_response(self, context, **response_kwargs):
        halt = getattr(self, "_admin_graphql_halt", None)
        if halt is not None:
            return shopify_result_to_django_response(halt)
        response = super().render_to_response(context, **response_kwargs)
        verification_result = getattr(self, "_verification_result", None)
        verification_response = getattr(verification_result, "response", None)
        response_headers = getattr(verification_response, "headers", {})
        if isinstance(response_headers, dict):
            for key, value in response_headers.items():
                response[key] = value
        return response


class EmbeddedShopifySyncView(AppHomeVerifiedMixin, View):
    """
    Import new Shopify content into Wagtail from the embedded app home.
    """

    http_method_names = ['post']

    def dispatch_after_verified(self, request, *args, **kwargs):
        token_result = ensure_offline_token_lifecycle(
            self._verification_result, self._shopify_app
        )
        if token_result is not None:
            return shopify_result_to_django_response(token_result)
        return super(AppHomeVerifiedMixin, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        resource = request.POST.get('resource')
        if resource not in VALID_IMPORT_RESOURCES:
            messages.error(request, 'Recurso de importación no válido.')
            return _redirect_home_preserving_query(request)

        try:
            sync_run = enqueue_shopify_import(resource, new_only=True)
            messages.success(
                request,
                (
                    f'Importación en cola (id={sync_run.pk}). '
                    'Se procesará en segundo plano.'
                ),
            )
        except RuntimeError as exc:
            messages.error(request, str(exc))
        except Exception:
            logger.exception('Embedded Shopify sync failed resource=%s', resource)
            messages.error(
                request,
                'Error inesperado durante la importación. Consulta los logs del servidor.',
            )

        return _redirect_home_preserving_query(request)


class AuthPatchIdTokenView(TemplateView):
    def get(self, request, *args, **kwargs):
        result = get_shopify_app().app_home_patch_id_token(
            request_to_shopify_req(request)
        )
        log_shopify_result(result)
        return shopify_result_to_django_response(result)


class EmbeddedInAppRedirectView(AppHomeVerifiedMixin, View):
    """
    In-iframe redirect. Pass destination as query or form param `next` (relative path, e.g. /app/extra).
    """

    http_method_names = ["get", "post"]

    def dispatch_after_verified(self, request, *args, **kwargs):
        next_path = (request.GET.get("next") or request.POST.get("next") or "").strip()
        err = validate_relative_app_path(next_path)
        if err:
            return HttpResponseBadRequest(err)
        shop = self._verification_result.shop
        result = self._shopify_app.app_home_redirect(
            request_to_shopify_req(request),
            next_path,
            shop,
        )
        log_shopify_result(result)
        return shopify_result_to_django_response(result)


class EmbeddedParentRedirectView(AppHomeVerifiedMixin, View):
    """
    Break out of the embedded iframe. Pass full URL as `url` (https://...); optional `target` _top or _blank.
    Host must be in SHOPIFY_PARENT_REDIRECT_ALLOWED_HOSTS (plus admin.shopify.com and app URL hosts).
    """

    http_method_names = ["get", "post"]

    def dispatch_after_verified(self, request, *args, **kwargs):
        target = request.GET.get("target") or request.POST.get("target")
        if target and target not in ("_top", "_blank"):
            return HttpResponseBadRequest("target must be _top or _blank.")
        url = (request.GET.get("url") or request.POST.get("url") or "").strip()
        err = validate_parent_redirect_url(url)
        if err:
            return HttpResponseBadRequest(err)
        shop = self._verification_result.shop
        result = self._shopify_app.app_home_parent_redirect(
            request_to_shopify_req(request),
            url,
            shop,
            target=target or None,
        )
        log_shopify_result(result)
        return shopify_result_to_django_response(result)

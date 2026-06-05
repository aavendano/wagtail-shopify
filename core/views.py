from urllib.parse import urlencode

from django.conf import settings
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

from .embedded_redirects import (
    validate_parent_redirect_url,
    validate_relative_app_path,
)
from .forms import ShopConfigForm
from .mixins import AppHomeVerifiedMixin
from .utils import (
    get_shopify_app,
    log_shopify_result,
    request_to_shopify_req,
    shopify_result_to_django_response,
)
from .token_service import ensure_offline_token_lifecycle
from shopify_requests.domains.shop import fetch_shop_admin_graphql


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
        context = super().get_context_data(**kwargs)
        verification_result = getattr(self, "_verification_result", None)
        shop = getattr(verification_result, "shop", None) if verification_result else None
        self._admin_graphql_halt = None
        if shop:
            gql = fetch_shop_admin_graphql(
                shop,
                verification_result=verification_result,
                invalid_token_response=getattr(
                    verification_result, "new_id_token_response", None
                ),
                shopify_app=getattr(self, "_shopify_app", None),
            )
            if not gql.ok and gql.raw is not None:
                self._admin_graphql_halt = gql.raw
            elif gql.ok and gql.data:
                shop_node = gql.data.get("shop") or {}
                context["shopify_admin_shop_id"] = shop_node.get("id")
        return context

    def dispatch_after_verified(self, request, *args, **kwargs):
        token_result = ensure_offline_token_lifecycle(
            self._verification_result, self._shopify_app
        )
        if token_result is not None:
            return shopify_result_to_django_response(token_result)
        return super(AppHomeVerifiedMixin, self).dispatch(request, *args, **kwargs)

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

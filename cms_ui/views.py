from __future__ import annotations

from django.conf import settings
from django.contrib.auth import login
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.urls import reverse

from api.auth import user_is_cms_editor
from core.utils import (
    get_shopify_app,
    log_shopify_result,
    request_to_shopify_req,
)
from django_react_ui_editor.views import SpaShellView

from .shop_auth import ensure_shop_editor_user
from .spa_assets import cms_spa_asset_version


class CmsShellView(SpaShellView):
    """
    Serve the CMS SPA shell for staff/cms_editors or Shopify App Home sessions.

    Website staff can open /cms/ with a Django session. Merchants in the Shopify
    Admin iframe are authenticated via App Home verify → shop editor user.
    """

    mount_slug = "cms"
    template_name = "django_react_ui_editor/spa_shell.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["spa_asset_version"] = cms_spa_asset_version()
        return context

    def get_app_home_patch_id_token_path(self):
        return reverse("core:patch-id-token")

    def dispatch(self, request, *args, **kwargs):
        if user_is_cms_editor(request.user):
            self._verification_result = None
            return super().dispatch(request, *args, **kwargs)

        try:
            shopify_app = get_shopify_app()
        except ImproperlyConfigured:
            return self._redirect_to_login(request)

        verification_result = shopify_app.verify_app_home_req(
            request_to_shopify_req(request),
            app_home_patch_id_token_path=self.get_app_home_patch_id_token_path(),
        )
        self._verification_result = verification_result
        log_shopify_result(verification_result)

        if not getattr(verification_result, "ok", False):
            # Outside Shopify (or without a session token), send ops to Django login.
            # Embedded merchants reach /cms/ after App Home already bootstrapped.
            return self._redirect_to_login(request)

        shop = getattr(verification_result, "shop", None)
        if not shop:
            return self._redirect_to_login(request)

        user = ensure_shop_editor_user(shop)
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return super().dispatch(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        verification_result = getattr(self, "_verification_result", None)
        verification_response = getattr(verification_result, "response", None)
        response_headers = getattr(verification_response, "headers", {})
        if isinstance(response_headers, dict):
            for key, value in response_headers.items():
                response[key] = value
        return response

    def _redirect_to_login(self, request):
        login_url = settings.LOGIN_URL or "/admin-django/login/"
        return redirect(f"{login_url}?next={request.path}")

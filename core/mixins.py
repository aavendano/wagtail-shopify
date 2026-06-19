from .utils import (
    get_shopify_app,
    log_shopify_result,
    request_to_shopify_req,
    shopify_result_to_django_response,
)


class AppHomeVerifiedMixin:
    """
    Verifies the request with Shopify App Home (embedded) before running the view.
    Subclasses implement dispatch_after_verified() for post-verification logic.
    """


    def get_app_home_patch_id_token_path(self):
        from django.urls import reverse
        return reverse("core:patch-id-token")

    def dispatch(self, request, *args, **kwargs):
        shopify_app = get_shopify_app()
        self._shopify_app = shopify_app
        verification_result = shopify_app.verify_app_home_req(
            request_to_shopify_req(request),
            app_home_patch_id_token_path=self.get_app_home_patch_id_token_path(),
        )
        self._verification_result = verification_result
        log_shopify_result(verification_result)
        if not getattr(verification_result, "ok", False):
            return shopify_result_to_django_response(verification_result)
        return self.dispatch_after_verified(request, *args, **kwargs)

    def dispatch_after_verified(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

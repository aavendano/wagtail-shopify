import json
import time

from .utils import (
    get_shopify_app,
    log_shopify_result,
    request_to_shopify_req,
    shopify_result_to_django_response,
)

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


class AppHomeVerifiedMixin:
    """
    Verifies the request with Shopify App Home (embedded) before running the view.
    Subclasses implement dispatch_after_verified() for post-verification logic.
    """


    def get_app_home_patch_id_token_path(self):
        from django.urls import reverse
        return reverse("core:patch-id-token")

    def dispatch(self, request, *args, **kwargs):
        # #region agent log
        _agent_log(
            "core/mixins.py:dispatch:entry",
            "AppHomeVerifiedMixin dispatch",
            {
                "path": request.path,
                "method": request.method,
                "has_embedded": request.GET.get("embedded"),
                "has_shop": bool(request.GET.get("shop")),
                "host": request.META.get("HTTP_HOST"),
                "x_forwarded_proto": request.META.get("HTTP_X_FORWARDED_PROTO"),
            },
            "H4",
        )
        # #endregion
        try:
            shopify_app = get_shopify_app()
            self._shopify_app = shopify_app
            verification_result = shopify_app.verify_app_home_req(
                request_to_shopify_req(request),
                app_home_patch_id_token_path=self.get_app_home_patch_id_token_path(),
            )
            self._verification_result = verification_result
            log_shopify_result(verification_result)
            # #region agent log
            _agent_log(
                "core/mixins.py:dispatch:verified",
                "Shopify verification result",
                {
                    "ok": getattr(verification_result, "ok", False),
                    "shop": getattr(verification_result, "shop", None),
                    "log_code": getattr(getattr(verification_result, "log", None), "code", None)
                    if not isinstance(getattr(verification_result, "log", None), dict)
                    else getattr(verification_result, "log", {}).get("code"),
                },
                "H1",
            )
            # #endregion
            if not getattr(verification_result, "ok", False):
                return shopify_result_to_django_response(verification_result)
            return self.dispatch_after_verified(request, *args, **kwargs)
        except Exception as exc:
            # #region agent log
            _agent_log(
                "core/mixins.py:dispatch:exception",
                "Unhandled exception in dispatch",
                {"type": type(exc).__name__, "error": str(exc)},
                "H1",
            )
            # #endregion
            raise

    def dispatch_after_verified(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

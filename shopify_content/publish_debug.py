"""Debug instrumentation for publish failures (session fdc58d)."""

import json
import time
import traceback

LOG_PATH = "/home/alejandro/apps/wagtail-shopify/.cursor/debug-fdc58d.log"
SESSION_ID = "fdc58d"


def debug_log(hypothesis_id, location, message, data=None, run_id="pre-fix"):
    payload = {
        "sessionId": SESSION_ID,
        "runId": run_id,
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data or {},
        "timestamp": int(time.time() * 1000),
    }
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as log_file:
            log_file.write(json.dumps(payload) + "\n")
    except OSError:
        pass


def register_publish_debug_handlers():
    from django.core.signals import got_request_exception

    def on_request_exception(sender, request, **kwargs):
        path = getattr(request, "path", "")
        if "/admin/pages/" not in path and "/api/v1/locations" not in path:
            return
        exc = sys_exc_info()
        debug_log(
            "E",
            "publish_debug:on_request_exception",
            "Unhandled exception during publish-related request",
            {
                "path": path,
                "method": getattr(request, "method", ""),
                "exc_type": type(exc).__name__ if exc else "Unknown",
                "exc": str(exc) if exc else "",
                "traceback": traceback.format_exc(),
            },
        )

    got_request_exception.connect(on_request_exception, dispatch_uid="shopify_publish_debug_exc")


def sys_exc_info():
    import sys

    exc = sys.exc_info()[1]
    return exc

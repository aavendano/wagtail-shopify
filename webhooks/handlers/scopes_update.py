import json
import logging

logger = logging.getLogger(__name__)


def handle_app_scopes_update(shop: str, raw_body: bytes) -> None:
    payload_preview = None
    if raw_body:
        try:
            payload_preview = json.loads(raw_body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            payload_preview = "<non-json body>"

    logger.info(
        "shopify_webhook topic=app/scopes_update shop=%s payload=%s",
        shop,
        payload_preview,
    )

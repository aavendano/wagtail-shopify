"""Location index export_config consumer (root_page metaobject per locale)."""

from django.db import transaction

from shopify_content.export_config.base import RootIndexConsumer
from shopify_content.locations.index import build_location_index_json

LOCATION_ROOT_SLUG = 'local-us'


class LocationIndexConsumer(RootIndexConsumer):
    root_slug = LOCATION_ROOT_SLUG
    handle_prefix = 'locations'
    config_key = 'location_index'

    def build_payload(self, locale_code: str) -> dict:
        return build_location_index_json(locale_code)

    def locale_codes_for_page(self, page) -> list[str] | None:
        from shopify_content.models import LocationPage

        specific = page.specific if hasattr(page, 'specific') else page
        if not isinstance(specific, LocationPage):
            return None
        if specific.shopify_locale:
            return [specific.shopify_locale]
        if not specific.locale_id:
            return None
        return [specific.locale.language_code]

    def queue_sync(self, *, locale_codes: list[str] | None = None) -> None:
        from shopify_content.tasks import sync_location_index_task

        def dispatch():
            sync_location_index_task.delay()

        transaction.on_commit(dispatch)


location_index_consumer = LocationIndexConsumer()
# Back-compat alias used by older imports/tests.
location_listings_consumer = location_index_consumer

"""Location index listings export_config consumer."""

from django.db import transaction

from shopify_content.export_config.single_page import SinglePageListingsConsumer
from shopify_content.locations.index import build_location_index_listings

LOCATION_ROOT_SLUG = 'local-us'


class LocationListingsConsumer(SinglePageListingsConsumer):
    root_slug = LOCATION_ROOT_SLUG
    config_key = 'location_index'

    def build_payload(self) -> dict:
        return build_location_index_listings()

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


location_listings_consumer = LocationListingsConsumer()
location_index_consumer = location_listings_consumer

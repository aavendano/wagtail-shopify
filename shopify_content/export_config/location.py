"""Location index export_config consumer."""

from django.db import transaction

from shopify_content.export_config.base import IndexMetafieldSpec, PageIndexConsumer
from shopify_content.locations.index import build_location_index_json

LOCATION_ROOT_SLUG = 'local-us'


class LocationIndexConsumer(PageIndexConsumer):
    root_slug = LOCATION_ROOT_SLUG
    config_key = 'location_index'
    index_metafields = IndexMetafieldSpec(
        locale_key='location_locale',
        index_key='location_index',
    )

    def build_payload(self, locale_code: str) -> dict:
        return build_location_index_json(locale_code)

    def locale_codes_for_page(self, page) -> list[str] | None:
        if page.shopify_locale:
            return [page.shopify_locale]
        return [page.locale.language_code]

    def queue_sync(self, *, locale_codes: list[str] | None = None) -> None:
        from shopify_content.tasks import sync_location_index_task

        def dispatch():
            sync_location_index_task.delay(locale_codes=locale_codes)

        transaction.on_commit(dispatch)


location_index_consumer = LocationIndexConsumer()

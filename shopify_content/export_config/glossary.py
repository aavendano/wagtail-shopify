"""Glossary index export_config consumer (root_page metaobject per locale)."""

from django.db import transaction

from shopify_content.export_config.base import RootIndexConsumer
from shopify_content.glossary.index import build_glossary_index_json

GLOSSARY_ROOT_SLUG = 'glossary'


class GlossaryIndexConsumer(RootIndexConsumer):
    root_slug = GLOSSARY_ROOT_SLUG
    handle_prefix = 'glossary'
    config_key = 'glossary_index'

    def build_payload(self, locale_code: str) -> dict:
        return build_glossary_index_json(locale_code)

    def locale_codes_for_page(self, page) -> list[str] | None:
        from shopify_content.models import GlossaryTermPage

        specific = page.specific if hasattr(page, 'specific') else page
        if not isinstance(specific, GlossaryTermPage):
            return None
        if not specific.locale_id:
            return None
        return [specific.locale.language_code]

    def queue_sync(self, *, locale_codes: list[str] | None = None) -> None:
        from shopify_content.tasks import sync_glossary_index_task

        def dispatch():
            sync_glossary_index_task.delay()

        transaction.on_commit(dispatch)


glossary_index_consumer = GlossaryIndexConsumer()
# Back-compat alias used by older imports/tests.
glossary_listings_consumer = glossary_index_consumer

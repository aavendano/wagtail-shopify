"""Glossary index listings export_config consumer."""

from django.db import transaction

from shopify_content.export_config.single_page import SinglePageListingsConsumer
from shopify_content.glossary.index import build_glossary_index_listings

GLOSSARY_ROOT_SLUG = 'glossary'


class GlossaryListingsConsumer(SinglePageListingsConsumer):
    root_slug = GLOSSARY_ROOT_SLUG
    config_key = 'glossary_index'

    def build_payload(self) -> dict:
        return build_glossary_index_listings()

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


glossary_listings_consumer = GlossaryListingsConsumer()
glossary_index_consumer = glossary_listings_consumer

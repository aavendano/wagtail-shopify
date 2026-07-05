"""Glossary index export_config consumer."""

from django.db import transaction

from shopify_content.export_config.base import IndexMetafieldSpec, PageIndexConsumer
from shopify_content.glossary.index import build_glossary_index_json

GLOSSARY_ROOT_SLUG = 'glossary'


class GlossaryIndexConsumer(PageIndexConsumer):
    root_slug = GLOSSARY_ROOT_SLUG
    config_key = 'glossary_index'
    index_metafields = IndexMetafieldSpec(
        locale_key='glossary_locale',
        index_key='glossary_index',
    )

    def build_payload(self, locale_code: str) -> dict:
        return build_glossary_index_json(locale_code)

    def locale_codes_for_page(self, page) -> list[str] | None:
        locale_code = getattr(page, 'locale_code', None)
        if not locale_code:
            return None
        return [locale_code]

    def queue_sync(self, *, locale_codes: list[str] | None = None) -> None:
        from shopify_content.tasks import sync_glossary_index_task

        def dispatch():
            sync_glossary_index_task.delay(locale_codes=locale_codes)

        transaction.on_commit(dispatch)


glossary_index_consumer = GlossaryIndexConsumer()

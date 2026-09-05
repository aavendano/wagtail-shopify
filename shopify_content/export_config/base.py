"""Base types for export_config index consumers.

`RootIndexConsumer` builds precomputed index payloads and hreflang/noindex
contracts for glossary/locations. It never talks to Shopify; the writer is
`shopify_content.sync.outbound.sync_root_index_locales`.

`LISTINGS_KEY` / alternates constants remain for the blog single-Page path
(`SinglePageListingsConsumer` in single_page.py).
"""

from __future__ import annotations


METAFIELD_NAMESPACE = 'custom'
LISTINGS_KEY = 'index_listings'

# Deprecated metafield keys from the multi-page index architecture (blog still
# uses LISTINGS_KEY; glossary/locations moved to root_page metaobject fields).
ALTERNATES_KEY = 'index_alternates'
NOINDEX_KEY = 'index_noindex'


class RootIndexConsumer:
    """
    Build precomputed index payloads and their hreflang/noindex contract for a
    ShopifyRootPage family (e.g. glossary, locations).

    Subclasses set root_slug, handle_prefix, and config_key.
    """

    root_slug: str
    handle_prefix: str
    config_key: str

    def get_root_page(self):
        from shopify_content.models import ShopifyRootPage

        return (
            ShopifyRootPage.objects.live()
            .filter(slug=self.root_slug)
            .first()
        )

    def get_config(self, root=None) -> dict | None:
        root = root or self.get_root_page()
        if root is None:
            return None
        export_config = root.export_config or {}
        section = export_config.get(self.config_key) or {}
        if not section.get('enabled'):
            return None
        locales = section.get('locales') or []
        if not isinstance(locales, list) or not locales:
            return None
        return section

    def configured_locales(self, config: dict, locale_codes: list[str] | None) -> list[str]:
        available = list(config.get('locales') or [])
        if locale_codes:
            return [code for code in locale_codes if code in available]
        return available

    def build_payload(self, locale_code: str) -> dict:
        raise NotImplementedError

    def locale_codes_for_page(self, page) -> list[str] | None:
        return None

    def hreflang_for_locale(self, locale_code: str) -> str:
        """Map an internal locale code (e.g. 'en-US') to an hreflang value."""
        return locale_code.replace('_', '-')

    def entry_handle(self, locale_code: str) -> str:
        """Deterministic root_page metaobject handle for this family + locale."""
        return f'{self.handle_prefix}-{locale_code.lower()}'

    def is_noindex(self, config: dict, locale_code: str) -> bool:
        """Whether the index entry for this locale should get a noindex robots meta."""
        if config.get('noindex') is True:
            return True
        noindex_locales = config.get('noindex_locales') or []
        return any(str(entry).lower() == locale_code.lower() for entry in noindex_locales)

    def build_alternates_payload(self, config: dict, all_locales: list[str]) -> dict:
        """
        Build the index_alternates JSON shared by every sibling root_page entry.

        Handles are deterministic (this.entry_handle), so no Shopify lookup is needed.
        """
        x_default_locale = config.get('x_default_locale') or (all_locales[0] if all_locales else None)

        alternates = [
            {
                'hreflang': self.hreflang_for_locale(locale_code),
                'label': locale_code,
                'handle': self.entry_handle(locale_code),
            }
            for locale_code in all_locales
        ]

        x_default_handle = self.entry_handle(x_default_locale) if x_default_locale else None

        return {
            'version': 1,
            'x_default': x_default_handle,
            'x_default_locale': x_default_locale,
            'alternates': alternates,
        }

    def queue_sync(self, *, locale_codes: list[str] | None = None) -> None:
        raise NotImplementedError(f'queue_sync not implemented for {self.config_key}')

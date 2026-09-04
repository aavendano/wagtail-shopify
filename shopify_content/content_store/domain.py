"""Canonical editorial domain API: ``page.editorial.description`` (D-012).

This is a domain concept, not a Django field (D-011): it performs no ORM
masquerading, no hidden mutation, and no Git commands. Reading an attribute
resolves the authoritative value through the ContentRepository per the active
mode, raising explicit domain errors when authoritative content is unavailable.
"""

from __future__ import annotations

from .accessors import MIRRORED_FIELDS, resolve_editorial


class EditorialAccessor:
    """Read-facing accessor bound to one page instance.

    Attribute access (e.g. ``.description``, ``.definition``) resolves the
    authoritative editorial value for any field registered as editorial for the
    page's type. Unknown attributes raise AttributeError so the accessor can
    never be mistaken for arbitrary model state.
    """

    __slots__ = ("_page",)

    def __init__(self, page):
        self._page = page

    def __getattr__(self, name: str) -> str:
        # __getattr__ only runs when normal lookup fails; _page is a slot and
        # never routes here, so there is no recursion risk.
        if (self._page._meta.label_lower, name) in MIRRORED_FIELDS:
            return resolve_editorial(self._page, name)
        raise AttributeError(
            f"{name!r} is not a migrated editorial field for "
            f"{self._page._meta.label_lower}"
        )

    def __repr__(self) -> str:  # pragma: no cover - debug aid
        return f"<EditorialAccessor page={self._page!r}>"


class EditorialMixin:
    """Exposes ``.editorial`` on a domain object. Not a Django model field."""

    @property
    def editorial(self) -> EditorialAccessor:
        return EditorialAccessor(self)

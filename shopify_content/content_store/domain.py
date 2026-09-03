"""Canonical editorial domain API: ``page.editorial.description`` (D-012).

This is a domain concept, not a Django field (D-011): it performs no ORM
masquerading, no hidden mutation, and no Git commands. Reading an attribute
resolves the authoritative value through the ContentRepository per the active
mode, raising explicit domain errors when authoritative content is unavailable.
"""

from __future__ import annotations

from .accessors import resolve_editorial


class EditorialAccessor:
    """Read-facing accessor bound to one page instance."""

    __slots__ = ("_page",)

    def __init__(self, page):
        self._page = page

    @property
    def description(self) -> str:
        return resolve_editorial(self._page, "description")

    def __repr__(self) -> str:  # pragma: no cover - debug aid
        return f"<EditorialAccessor page={self._page!r}>"


class EditorialMixin:
    """Exposes ``.editorial`` on a domain object. Not a Django model field."""

    @property
    def editorial(self) -> EditorialAccessor:
        return EditorialAccessor(self)

"""Canonical editorial domain API: ``page.editorial.<field>`` (D-012).

This is a domain concept, not a Django field (D-011): it performs no ORM
masquerading, hidden mutation, or Git commands. Attribute access resolves a
registered editorial field through the ContentRepository and active authority
mode.
"""

from __future__ import annotations

from .accessors import EDITORIAL_FIELDS, resolve_editorial


class EditorialAccessor:
    """Read-facing accessor bound to one page instance."""

    __slots__ = ("_page",)

    def __init__(self, page):
        self._page = page

    def __getattr__(self, name: str) -> str:
        if (self._page._meta.label_lower, name) in EDITORIAL_FIELDS:
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

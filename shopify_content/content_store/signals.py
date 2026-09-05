"""Content-write workflow wiring (independent of Shopify publish — C-004).

Editorial mirroring is triggered by content saves (``post_save``), never by the
``page_published`` publish signal. Mirroring runs after the DB transaction
commits so the authoritative row is durable first.

The receiver is registry-driven: every model/field pair in ``MIRRORED_FIELDS``
gets the same transition behavior without adding page-specific signal handlers.
"""

from __future__ import annotations

from collections import defaultdict

from django.apps import apps
from django.db import transaction
from django.db.models.signals import post_save

from .accessors import MIRRORED_FIELDS, mirror_editorial_content


def _fields_by_content_type() -> dict[str, tuple[str, ...]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    for content_type, field_key in sorted(MIRRORED_FIELDS):
        grouped[content_type].append(field_key)
    return {content_type: tuple(fields) for content_type, fields in grouped.items()}


def _on_editorial_page_saved(sender, instance, **kwargs):
    page_id = instance.pk
    field_keys = _fields_by_content_type().get(sender._meta.label_lower, ())
    if not field_keys:
        return

    def dispatch():
        try:
            page = sender.objects.get(pk=page_id)
        except sender.DoesNotExist:
            return
        for field_key in field_keys:
            mirror_editorial_content(page, field_key)

    transaction.on_commit(dispatch)


def register_content_store_signals() -> None:
    for content_type in _fields_by_content_type():
        app_label, model_name = content_type.split('.', 1)
        model = apps.get_model(app_label, model_name)
        post_save.connect(
            _on_editorial_page_saved,
            sender=model,
            dispatch_uid=f"content_store_mirror_{content_type}",
            weak=False,
        )

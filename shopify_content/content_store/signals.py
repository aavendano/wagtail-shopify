"""Content-write workflow wiring (independent of Shopify publish — C-004).

Editorial mirroring is triggered by content saves (``post_save``), never by the
``page_published`` publish signal. Mirroring runs after the DB transaction
commits so the authoritative row is durable first.
"""

from __future__ import annotations

from django.db import transaction
from django.db.models.signals import post_save

from .accessors import mirror_editorial_content


def _on_blogpage_saved(sender, instance, **kwargs):
    page_id = instance.pk

    def dispatch():
        from shopify_content.models import BlogPage

        try:
            page = BlogPage.objects.get(pk=page_id)
        except BlogPage.DoesNotExist:
            return
        mirror_editorial_content(page, "description")

    transaction.on_commit(dispatch)


def register_content_store_signals() -> None:
    from shopify_content.models import BlogPage

    post_save.connect(
        _on_blogpage_saved,
        sender=BlogPage,
        dispatch_uid="content_store_mirror_blogpage_description",
    )

"""Rebuild derived ContentIndex tables from the deployed content tree."""

from __future__ import annotations

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from shopify_content.content_store.content_index_service import rebuild_content_index


class Command(BaseCommand):
    help = "Rebuild ContentIndex / ContentReferenceIndex from CONTENT_STORE_ROOT."

    def add_arguments(self, parser):
        parser.add_argument("--root", default=None, help="Override CONTENT_STORE_ROOT.")

    def handle(self, *args, **options):
        root = options["root"] or getattr(settings, "CONTENT_STORE_ROOT", None)
        if not root:
            raise CommandError("CONTENT_STORE_ROOT is not configured.")
        stats = rebuild_content_index(root)
        self.stdout.write(
            f"Indexed {stats['files']} document(s), {stats['references']} reference(s)."
        )

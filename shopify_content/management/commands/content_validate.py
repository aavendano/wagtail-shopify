"""Validate Git-backed editorial content (read-only, deterministic)."""

from __future__ import annotations

import sys

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from shopify_content.content_store.validation_runner import validate_content_tree


class Command(BaseCommand):
    help = "Validate editorial Markdown under CONTENT_STORE_ROOT (no Git or DB writes)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--json",
            action="store_true",
            help="Emit machine-readable JSON report on stdout.",
        )
        parser.add_argument(
            "--root",
            default=None,
            help="Override CONTENT_STORE_ROOT for this run.",
        )

    def handle(self, *args, **options):
        root = options["root"] or getattr(settings, "CONTENT_STORE_ROOT", None)
        if not root:
            raise CommandError("CONTENT_STORE_ROOT is not configured.")

        report = validate_content_tree(root)
        if options["json"]:
            self.stdout.write(report.to_json())
        else:
            self.stdout.write(
                f"Checked {report.checked} file(s); ok={report.ok}"
            )
            for issue in report.issues:
                self.stderr.write(f"{issue.code} {issue.path}: {issue.message}")

        if not report.ok:
            sys.exit(1)

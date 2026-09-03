"""Materialize existing BlogPage.description values into the Git content tree.

Controlled, idempotent migration tool (NOT a schema migration, NOT run at
startup, NOT triggered by Model.save()). Operators run this once to seed the
authoritative worktree, then commit the result through the normal Git workflow.

    python manage.py materialize_editorial_content [--locale en-US] [--force] [--dry-run]

Scope (HG-003): BlogPage.description only.
"""

from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError

from shopify_content.content_store.accessors import MIRRORED_FIELDS, get_repository
from shopify_content.content_store.locales import UnsupportedLocale
from shopify_content.content_store.refs import ref_for
from shopify_content.content_store.serializers import checksum
from shopify_content.models import BlogPage

SUPPORTED_FIELDS = {"description"}


class Command(BaseCommand):
    help = "Materialize BlogPage.description into the Git-authoritative content tree."

    def add_arguments(self, parser):
        parser.add_argument("--field", default="description", choices=sorted(SUPPORTED_FIELDS))
        parser.add_argument("--locale", default=None, help="Filter by Wagtail locale code (e.g. en-US).")
        parser.add_argument("--force", action="store_true", help="Overwrite divergent existing files.")
        parser.add_argument("--dry-run", action="store_true", help="Report actions without writing.")

    def handle(self, *args, **opts):
        field = opts["field"]
        if ("shopify_content.blogpage", field) not in MIRRORED_FIELDS:
            raise CommandError(f"Field {field!r} is not a migrated editorial field.")

        repo = get_repository()
        if repo is None:
            raise CommandError("CONTENT_STORE_ROOT is not configured.")

        force = opts["force"]
        dry_run = opts["dry_run"]
        locale_filter = opts["locale"]

        qs = BlogPage.objects.select_related("locale").all()
        if locale_filter:
            qs = qs.filter(locale__language_code=locale_filter)

        stats = {
            "examined": 0,
            "created": 0,
            "identical": 0,
            "divergent_skipped": 0,
            "overwritten": 0,
            "unsupported_locale": 0,
            "errors": 0,
        }

        for page in qs:
            stats["examined"] += 1
            value = getattr(page, field, "") or ""
            try:
                ref = ref_for(page, field)
                rel = self._safe_relative(ref)
            except UnsupportedLocale:
                stats["unsupported_locale"] += 1
                self.stderr.write(
                    f"[unsupported-locale] pk={page.pk} locale="
                    f"{getattr(page.locale, 'language_code', '?')} (skipped)"
                )
                continue

            try:
                if repo.exists(ref):
                    existing = repo.read(ref).body
                    if existing == value:
                        stats["identical"] += 1
                        continue
                    if not force:
                        stats["divergent_skipped"] += 1
                        self.stderr.write(
                            f"[divergent] pk={page.pk} {rel} differs "
                            f"(db={checksum(value)[:12]} file={checksum(existing)[:12]}); "
                            f"use --force to overwrite"
                        )
                        continue
                    if not dry_run:
                        repo.write(ref, value)
                    stats["overwritten"] += 1
                    self.stdout.write(f"[overwrite] pk={page.pk} {rel}")
                else:
                    if not dry_run:
                        repo.write(ref, value)
                    stats["created"] += 1
                    self.stdout.write(f"[create] pk={page.pk} {rel}")
            except Exception as exc:  # noqa: BLE001 - report and continue
                stats["errors"] += 1
                self.stderr.write(f"[error] pk={page.pk}: {exc}")

        prefix = "DRY-RUN " if dry_run else ""
        self.stdout.write(
            self.style.SUCCESS(
                f"{prefix}materialize_editorial_content({field}): "
                f"examined={stats['examined']} created={stats['created']} "
                f"identical={stats['identical']} overwritten={stats['overwritten']} "
                f"divergent_skipped={stats['divergent_skipped']} "
                f"unsupported_locale={stats['unsupported_locale']} errors={stats['errors']}"
            )
        )

    @staticmethod
    def _safe_relative(ref):
        from shopify_content.content_store.refs import relative_path

        return relative_path(ref).as_posix()

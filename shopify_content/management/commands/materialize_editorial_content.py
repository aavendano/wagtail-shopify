"""Materialize migrated editorial fields into the Git content tree.

Controlled, idempotent migration tool (NOT a schema migration, NOT run at
startup, NOT triggered by Model.save()). Operators run this once per field to
seed the authoritative worktree, then commit the result through the normal Git
workflow.

    python manage.py materialize_editorial_content [--field description|definition]
                                                   [--locale en-US] [--force] [--dry-run]

Migrated fields (scoped, per HumanGate):
  BlogPage.description        (HG-003)
  GlossaryTermPage.definition (HG-004)

Content is preserved VERBATIM (lossless). Existing HTML (e.g. Wagtail RichText
``.source``) is written as-is inside the ``.md`` body; no HTML->Markdown
conversion is performed.
"""

from __future__ import annotations

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError

from shopify_content.content_store.accessors import MIRRORED_FIELDS, db_text, get_repository
from shopify_content.content_store.locales import UnsupportedLocale
from shopify_content.content_store.refs import ref_for, relative_path
from shopify_content.content_store.serializers import checksum


def _targets(field_filter):
    for content_type, field_key in sorted(MIRRORED_FIELDS):
        if field_filter and field_key != field_filter:
            continue
        app_label, model_name = content_type.split(".", 1)
        model = apps.get_model(app_label, model_name)
        yield model, field_key


class Command(BaseCommand):
    help = "Materialize migrated editorial fields into the Git-authoritative content tree."

    def add_arguments(self, parser):
        field_choices = sorted({fk for _, fk in MIRRORED_FIELDS})
        parser.add_argument("--field", default=None, choices=field_choices,
                            help="Only materialize this editorial field (default: all).")
        parser.add_argument("--locale", default=None, help="Filter by Wagtail locale code (e.g. en-US).")
        parser.add_argument("--force", action="store_true", help="Overwrite divergent existing files.")
        parser.add_argument("--dry-run", action="store_true", help="Report actions without writing.")

    def handle(self, *args, **opts):
        repo = get_repository()
        if repo is None:
            raise CommandError("CONTENT_STORE_ROOT is not configured.")

        field_filter = opts["field"]
        force = opts["force"]
        dry_run = opts["dry_run"]
        locale_filter = opts["locale"]

        targets = list(_targets(field_filter))
        if not targets:
            raise CommandError(f"No migrated editorial field matches --field={field_filter!r}.")

        stats = {
            "examined": 0, "created": 0, "identical": 0,
            "divergent_skipped": 0, "overwritten": 0,
            "unsupported_locale": 0, "errors": 0,
        }

        for model, field_key in targets:
            qs = model.objects.select_related("locale").all()
            if locale_filter:
                qs = qs.filter(locale__language_code=locale_filter)

            for page in qs:
                stats["examined"] += 1
                value = db_text(page, field_key)
                ref = ref_for(page, field_key)
                try:
                    rel = relative_path(ref).as_posix()
                except UnsupportedLocale:
                    stats["unsupported_locale"] += 1
                    self.stderr.write(
                        f"[unsupported-locale] {model._meta.label_lower}#{page.pk} "
                        f"locale={getattr(page.locale, 'language_code', '?')} field={field_key} (skipped)"
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
                                f"[divergent] {rel} differs "
                                f"(db={checksum(value)[:12]} file={checksum(existing)[:12]}); "
                                f"use --force to overwrite"
                            )
                            continue
                        if not dry_run:
                            repo.write(ref, value)
                        stats["overwritten"] += 1
                        self.stdout.write(f"[overwrite] {rel}")
                    else:
                        if not dry_run:
                            repo.write(ref, value)
                        stats["created"] += 1
                        self.stdout.write(f"[create] {rel}")
                except Exception as exc:  # noqa: BLE001 - report and continue
                    stats["errors"] += 1
                    self.stderr.write(f"[error] {model._meta.label_lower}#{page.pk} {field_key}: {exc}")

        scope = field_filter or "all"
        prefix = "DRY-RUN " if dry_run else ""
        self.stdout.write(
            self.style.SUCCESS(
                f"{prefix}materialize_editorial_content(field={scope}): "
                f"examined={stats['examined']} created={stats['created']} "
                f"identical={stats['identical']} overwritten={stats['overwritten']} "
                f"divergent_skipped={stats['divergent_skipped']} "
                f"unsupported_locale={stats['unsupported_locale']} errors={stats['errors']}"
            )
        )

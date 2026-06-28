from django.core.management.base import BaseCommand

from shopify_content.models import LocationPage
from shopify_content.richtext_sanitize import (
    LOCATION_RICHTEXT_FIELDS,
    _richtext_source,
    sanitize_richtext_html,
    validate_richtext_html,
)


class Command(BaseCommand):
    help = "Repair malformed RichTextField HTML on LocationPage records."

    def add_arguments(self, parser):
        parser.add_argument(
            "--page-id",
            type=int,
            action="append",
            dest="page_ids",
            help="Only fix the given page ID (repeatable).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report changes without saving.",
        )

    def handle(self, *args, **options):
        qs = LocationPage.objects.all()
        page_ids = options.get("page_ids")
        if page_ids:
            qs = qs.filter(pk__in=page_ids)

        fixed_pages = 0
        fixed_fields = 0

        for page in qs.iterator():
            page_changed = False
            for field in LOCATION_RICHTEXT_FIELDS:
                raw = _richtext_source(getattr(page, field, ""))
                if not raw.strip():
                    continue
                if validate_richtext_html(raw) is None:
                    continue

                cleaned = sanitize_richtext_html(raw)
                if cleaned == raw or validate_richtext_html(cleaned) is not None:
                    self.stderr.write(
                        f"Page {page.pk} field {field}: could not auto-repair"
                    )
                    continue

                self.stdout.write(f"Page {page.pk} field {field}: repaired")
                if not options["dry_run"]:
                    setattr(page, field, cleaned)
                page_changed = True
                fixed_fields += 1

            if page_changed and not options["dry_run"]:
                page.save()
                fixed_pages += 1
            elif page_changed:
                fixed_pages += 1

        mode = "would fix" if options["dry_run"] else "fixed"
        self.stdout.write(
            self.style.SUCCESS(
                f"Done — {mode} {fixed_fields} field(s) across {fixed_pages} page(s)."
            )
        )

"""Seed Git-native ArticlePage.body Markdown documents from legacy StreamField.

This is an operational migration command, never a runtime side effect. It
preserves the currently rendered storefront HTML verbatim inside ``body.md``.
Raw HTML is valid inside Markdown, so authority can move to Git without first
performing a lossy HTML->Markdown conversion. Editors/agents may then normalize
individual documents to semantic Markdown and custom directives over time.

Usage:

    python manage.py materialize_article_markdown
    python manage.py materialize_article_markdown --locale en-US --dry-run
    python manage.py materialize_article_markdown --force
"""

from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError

from shopify_content.content_store.accessors import get_repository
from shopify_content.content_store.locales import UnsupportedLocale
from shopify_content.content_store.refs import ref_for, relative_path
from shopify_content.content_store.serializers import checksum
from shopify_content.models import ArticlePage
from shopify_content.sync.outbound import _render_streamfield_html


class Command(BaseCommand):
    help = (
        "Materialize legacy ArticlePage StreamField output into Git-native body.md "
        "documents without semantic HTML->Markdown conversion."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--locale",
            default=None,
            help="Only materialize one Wagtail locale code (e.g. en-US).",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite divergent existing body.md files.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report actions without writing files.",
        )

    def handle(self, *args, **opts):
        repo = get_repository()
        if repo is None:
            raise CommandError("CONTENT_STORE_ROOT is not configured.")

        qs = ArticlePage.objects.select_related("locale").all()
        if opts["locale"]:
            qs = qs.filter(locale__language_code=opts["locale"])

        stats = {
            "examined": 0,
            "created": 0,
            "identical": 0,
            "overwritten": 0,
            "divergent_skipped": 0,
            "unsupported_locale": 0,
            "errors": 0,
        }

        for page in qs:
            stats["examined"] += 1
            ref = ref_for(page, "body")
            try:
                rel = relative_path(ref).as_posix()
            except UnsupportedLocale:
                stats["unsupported_locale"] += 1
                self.stderr.write(
                    f"[unsupported-locale] article#{page.pk} "
                    f"locale={getattr(page.locale, 'language_code', '?')} (skipped)"
                )
                continue

            try:
                # This is intentionally the existing storefront representation,
                # not an HTML->Markdown rewrite. It gives us a lossless authority
                # flip; semantic cleanup is an editorial migration afterwards.
                value = _render_streamfield_html(page.body)

                if repo.exists(ref):
                    existing = repo.read(ref).body
                    if existing == value:
                        stats["identical"] += 1
                        continue
                    if not opts["force"]:
                        stats["divergent_skipped"] += 1
                        self.stderr.write(
                            f"[divergent] {rel} differs "
                            f"(legacy={checksum(value)[:12]} file={checksum(existing)[:12]}); "
                            "use --force to overwrite"
                        )
                        continue
                    if not opts["dry_run"]:
                        repo.write(ref, value)
                    stats["overwritten"] += 1
                    self.stdout.write(f"[overwrite] {rel}")
                else:
                    if not opts["dry_run"]:
                        # Write even an empty body: existence is the authority
                        # invariant in git_authoritative mode.
                        repo.write(ref, value)
                    stats["created"] += 1
                    self.stdout.write(f"[create] {rel}")
            except Exception as exc:  # noqa: BLE001 - report and continue batch
                stats["errors"] += 1
                self.stderr.write(f"[error] article#{page.pk}: {exc}")

        prefix = "DRY-RUN " if opts["dry_run"] else ""
        self.stdout.write(
            self.style.SUCCESS(
                f"{prefix}materialize_article_markdown: "
                f"examined={stats['examined']} created={stats['created']} "
                f"identical={stats['identical']} overwritten={stats['overwritten']} "
                f"divergent_skipped={stats['divergent_skipped']} "
                f"unsupported_locale={stats['unsupported_locale']} errors={stats['errors']}"
            )
        )

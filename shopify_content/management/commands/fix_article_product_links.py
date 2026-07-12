"""Rewrite broken /products/{handle} links in ArticlePage StreamField HTML."""

from django.core.management.base import BaseCommand, CommandError

from shopify_content.article_product_links import (
    ProductHandleResolver,
    load_manual_map,
    rewrite_streamfield_raw,
)
from shopify_content.models import ArticlePage, BlogPage, ProductPage
from shopify_content.sync.outbound import sync_article_page


class Command(BaseCommand):
    help = (
        'Rewrite /products/{handle} hrefs in article bodies to live ProductPage '
        'handles (relative /products/{handle}). Unwrap unmapped links by default.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Report changes without saving or pushing.',
        )
        parser.add_argument(
            '--blog-handle',
            type=str,
            default=None,
            help='Limit to articles under this BlogPage.handle (e.g. sex-toys-artisans).',
        )
        parser.add_argument(
            '--page-id',
            type=int,
            action='append',
            dest='page_ids',
            help='Only fix the given ArticlePage ID (repeatable).',
        )
        parser.add_argument(
            '--map-file',
            type=str,
            default=None,
            help='JSON object mapping legacy_handle → live_handle for ambiguous cases.',
        )
        parser.add_argument(
            '--push',
            action='store_true',
            help='After saving, sync each changed article to Shopify (outbound).',
        )
        parser.add_argument(
            '--no-unwrap-missing',
            action='store_true',
            help='Leave unmapped product links unchanged instead of unwrapping <a> tags.',
        )
        parser.add_argument(
            '--include-drafts',
            action='store_true',
            help='Include non-live articles (default: live only).',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        unwrap_missing = not options['no_unwrap_missing']
        push = options['push'] and not dry_run

        try:
            manual_map = load_manual_map(options.get('map_file'))
        except (OSError, ValueError, TypeError) as exc:
            raise CommandError(str(exc)) from exc

        resolver = ProductHandleResolver.from_queryset(
            ProductPage.objects.live().exclude(handle=''),
            manual_map=manual_map,
        )
        self.stdout.write(
            f'Loaded {len(resolver.live_handles)} live product handles'
            + (f', {len(manual_map)} manual map entries' if manual_map else '')
        )

        qs = ArticlePage.objects.all().specific()
        if not options['include_drafts']:
            qs = qs.live()

        page_ids = options.get('page_ids')
        if page_ids:
            qs = qs.filter(pk__in=page_ids)

        blog_handle = options.get('blog_handle')
        if blog_handle:
            blogs = BlogPage.objects.filter(handle=blog_handle)
            if not blogs.exists():
                raise CommandError(f'No BlogPage with handle={blog_handle!r}')
            article_ids = []
            for blog in blogs:
                article_ids.extend(
                    ArticlePage.objects.child_of(blog).values_list('pk', flat=True)
                )
            qs = qs.filter(pk__in=article_ids)

        qs = qs.order_by('path')

        pages_changed = 0
        pages_scanned = 0
        total_rewritten = 0
        total_unwrapped = 0
        total_unchanged = 0
        total_ambiguous = 0
        ambiguous_handles: dict[str, list[str]] = {}
        pushed_ok = 0
        pushed_fail = 0

        for article in qs.iterator():
            pages_scanned += 1
            raw = list(article.body.raw_data) if article.body else []
            new_raw, stats, changed = rewrite_streamfield_raw(
                raw,
                resolver,
                unwrap_missing=unwrap_missing,
            )

            total_rewritten += stats.rewritten
            total_unwrapped += stats.unwrapped
            total_unchanged += stats.unchanged
            total_ambiguous += stats.ambiguous

            for decision in stats.decisions:
                if decision.action.value == 'ambiguous' and decision.candidates:
                    ambiguous_handles.setdefault(
                        decision.original_handle,
                        list(decision.candidates),
                    )

            if not changed:
                continue

            pages_changed += 1
            self.stdout.write(
                f'Article pk={article.pk} slug={article.slug}: '
                f'rewrite={stats.rewritten} unwrap={stats.unwrapped} '
                f'ambiguous={stats.ambiguous}'
            )

            if dry_run:
                continue

            article.body = new_raw
            revision = article.save_revision()
            if article.live:
                revision.publish()

            if push:
                ok = sync_article_page(article)
                if ok:
                    pushed_ok += 1
                    self.stdout.write(self.style.SUCCESS(f'  pushed pk={article.pk}'))
                else:
                    pushed_fail += 1
                    self.stderr.write(self.style.ERROR(f'  push failed pk={article.pk}'))

        mode = 'dry-run' if dry_run else 'applied'
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                f'Done ({mode}): scanned={pages_scanned} changed={pages_changed} '
                f'rewritten_hrefs={total_rewritten} unwrapped={total_unwrapped} '
                f'unchanged_hrefs={total_unchanged} ambiguous_hrefs={total_ambiguous}'
            )
        )
        if push:
            self.stdout.write(f'Push: ok={pushed_ok} failed={pushed_fail}')

        if ambiguous_handles:
            self.stdout.write('')
            self.stdout.write('Ambiguous handles (add to --map-file to resolve):')
            for handle, candidates in sorted(ambiguous_handles.items()):
                self.stdout.write(f'  {handle} -> {candidates}')

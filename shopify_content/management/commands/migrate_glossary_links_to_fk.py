"""Import existing glossary related_links JSON into manual typed semantic link FK rows."""

from django.core.management.base import BaseCommand

from shopify_content.models import GlossaryTermPage
from shopify_content.models.semantic_links import relation_for_page_type
from shopify_content.semantic_links.manual_links import resolve_related_link_target
from shopify_content.semantic_links.service import page_type_key_for, persist_semantic_links_revision


class Command(BaseCommand):
    help = (
        'Migrate GlossaryTermPage.related_links JSON entries to typed related_* FK rows '
        '(is_auto=False).'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Report matches without creating FK rows.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        created = 0
        skipped = 0
        terms_updated = set()

        for term_page in GlossaryTermPage.objects.all().iterator():
            links = term_page.related_links or []
            if not links:
                continue

            for link in links:
                try:
                    target = resolve_related_link_target(link, locale_id=term_page.locale_id)
                except Exception:
                    skipped += 1
                    continue
                if target is None:
                    skipped += 1
                    continue

                type_key = page_type_key_for(target)
                if type_key is None:
                    skipped += 1
                    continue

                relation_name = relation_for_page_type(type_key)
                manager = getattr(term_page, relation_name)
                if manager.filter(related_page=target).exists():
                    skipped += 1
                    continue

                sort_order = (
                    manager.order_by('-sort_order')
                    .values_list('sort_order', flat=True)
                    .first()
                )
                next_sort = (sort_order + 1) if sort_order is not None else 0

                if dry_run:
                    created += 1
                    continue

                manager.create(
                    related_page=target,
                    is_auto=False,
                    sort_order=next_sort,
                )
                created += 1
                terms_updated.add(term_page.pk)

        if not dry_run:
            for term_pk in terms_updated:
                persist_semantic_links_revision(
                    GlossaryTermPage.objects.get(pk=term_pk),
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Migration complete (created={created}, skipped={skipped}, dry_run={dry_run}).'
            )
        )

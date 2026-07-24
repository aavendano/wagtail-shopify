import logging
import re

from wagtail.fields import StreamField
from wagtail.models import Page

logger = logging.getLogger(__name__)

_PAGE_EDIT_RE = re.compile(r'.*/admin/pages/(?P<pk>\d+)/edit/?$')


def _streamfield_count(page, field_name):
    stream = getattr(page, field_name, None)
    if stream is None:
        return '0'
    try:
        return str(len(stream))
    except TypeError:
        return '0'


def _page_text_from_pk(page_pk):
    try:
        page = Page.objects.get(pk=page_pk).specific
    except Page.DoesNotExist:
        return ''

    parts = [page.title or '']
    if hasattr(page, 'search_description') and page.search_description:
        parts.append(page.search_description)
    if hasattr(page, 'summary') and page.summary:
        parts.append(page.summary)

    for field in page._meta.fields:
        if isinstance(field, StreamField):
            value = getattr(page, field.name, None)
            if value:
                parts.append(str(value))

    return '\n\n'.join(part for part in parts if part.strip())


class StreamFieldPreviewFixMiddleware:
    """Inject missing StreamField ``-count`` keys on page edit POSTs (preview flow)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            match = _PAGE_EDIT_RE.match(request.path)
            if match:
                self._inject_missing_streamfield_counts(request, match.group('pk'))
        return self.get_response(request)

    def _inject_missing_streamfield_counts(self, request, page_pk):
        try:
            page = Page.objects.get(pk=page_pk).specific
        except Page.DoesNotExist:
            return []

        post = request.POST.copy()
        injected = []
        for field in page._meta.fields:
            if not isinstance(field, StreamField):
                continue
            count_key = f'{field.name}-count'
            if count_key in post:
                continue
            post[count_key] = _streamfield_count(page, field.name)
            injected.append(count_key)

        if not injected:
            return []

        request.POST = post
        request._post = post
        if hasattr(request, '_load_post_and_files'):
            request._load_post_and_files()
        return injected


def install_source_result_stale_guard():
    """
    Avoid django-ai-core crash when pgvector still holds embeddings for deleted pages.

    Upstream uses zip(..., strict=True) in SourceResultMixin._documents_to_sources;
    objects_from_documents silently skips missing PKs, so lengths diverge.
    See: https://github.com/wagtail/django-ai-core/issues/13
    """
    from collections import defaultdict

    from django_ai_core.contrib.index.query import SourceResultMixin
    from django_ai_core.contrib.index.source import ObjectSource

    if getattr(SourceResultMixin._documents_to_sources, '_wai_stale_guard', False):
        return

    def _documents_to_sources(self, documents):
        if not documents:
            return

        sources_by_id = {source.source_id: source for source in self.sources}
        source_doc_mapping = defaultdict(list)
        mapped_objects = {}
        skipped = 0

        for document in documents:
            for source in self.sources:
                if source.provides_document(document):
                    source_doc_mapping[source.source_id].append(document)
                    break

        for source_id, docs in source_doc_mapping.items():
            source = sources_by_id[source_id]
            if isinstance(source, ObjectSource):
                pks = []
                for doc in docs:
                    meta = getattr(doc, 'metadata', None) or {}
                    pk = meta.get('pk')
                    if pk is None:
                        continue
                    try:
                        pks.append(int(pk))
                    except (TypeError, ValueError):
                        continue
                found = {
                    obj.pk: obj
                    for obj in source.model.objects.filter(pk__in=list(set(pks)))
                }
                for doc in docs:
                    meta = getattr(doc, 'metadata', None) or {}
                    pk = meta.get('pk')
                    try:
                        pk = int(pk)
                    except (TypeError, ValueError):
                        skipped += 1
                        continue
                    obj = found.get(pk)
                    if obj is None:
                        skipped += 1
                        continue
                    mapped_objects[doc.document_key] = obj
            else:
                for doc in docs:
                    mapped_objects[doc.document_key] = doc

        if skipped:
            logger.warning(
                'Skipped %s stale vector document(s) with no matching Wagtail page '
                '(mapped=%s). Re-run index_pages_batch to prune orphans.',
                skipped,
                len(mapped_objects),
            )

        for document in documents:
            obj = mapped_objects.get(document.document_key)
            if obj is not None:
                yield obj

    _documents_to_sources._wai_stale_guard = True
    SourceResultMixin._documents_to_sources = _documents_to_sources


def install_suggested_content_fallback():
    install_source_result_stale_guard()
    from wagtail_ai.agents.suggested_content import SuggestedContentAgent

    if getattr(SuggestedContentAgent.execute, '_wai_fallback_wrapped', False):
        return

    original_execute = SuggestedContentAgent.execute

    def execute_with_fallback(self, *args, **kwargs):
        allowed_types = kwargs.pop('allowed_types', None)
        content = kwargs.get('content') or ''
        exclude_pks = kwargs.get('exclude_pks') or []
        if not content.strip() and exclude_pks:
            fallback_content = _page_text_from_pk(exclude_pks[0])
            if fallback_content:
                kwargs = {**kwargs, 'content': fallback_content}

        requested_limit = int(kwargs.get('limit', 3) or 3)
        if allowed_types and requested_limit > 0:
            from django.conf import settings as django_settings

            multiplier = max(
                1,
                int(getattr(django_settings, 'SEMANTIC_LINKS_TYPE_OVERFETCH', 10)),
            )
            # Overfetch before type filter so mixed neighbors do not starve a bucket.
            max_fetch = max(1, 100 - len(exclude_pks))
            kwargs = {
                **kwargs,
                'limit': min(requested_limit * multiplier, max_fetch),
            }

        result = original_execute(self, *args, **kwargs)
        if not allowed_types:
            return result
        from shopify_content.semantic_links.service import page_type_key_for

        filtered = []
        for item in result or []:
            pk = item.get('id') if isinstance(item, dict) else getattr(item, 'pk', None)
            if pk is None:
                continue
            try:
                page = Page.objects.get(pk=int(pk))
            except (Page.DoesNotExist, TypeError, ValueError):
                continue
            if page_type_key_for(page) in allowed_types:
                filtered.append(item)
            if len(filtered) >= requested_limit:
                break
        return filtered

    execute_with_fallback._wai_fallback_wrapped = True
    SuggestedContentAgent.execute = execute_with_fallback

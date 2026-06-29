import re

from wagtail.fields import StreamField
from wagtail.models import Page

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


def install_suggested_content_fallback():
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
        result = original_execute(self, *args, **kwargs)
        if not allowed_types:
            return result
        from shopify_content.semantic_links.service import page_type_key_for

        limit = kwargs.get('limit', 3)
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
            if len(filtered) >= limit:
                break
        return filtered

    execute_with_fallback._wai_fallback_wrapped = True
    SuggestedContentAgent.execute = execute_with_fallback

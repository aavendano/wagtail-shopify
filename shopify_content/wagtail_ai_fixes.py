import json
import re
import time

from django.http import QueryDict
from wagtail.fields import StreamField
from wagtail.models import Page

DEBUG_LOG_PATH = '/home/alejandro/apps/wagtail-shopify/.cursor/debug-0938b0.log'
SESSION_ID = '0938b0'
_PAGE_EDIT_RE = re.compile(r'.*/admin/pages/(?P<pk>\d+)/edit/?$')


def _debug_log(*, hypothesis_id, location, message, data=None, run_id='pre-fix'):
    # #region agent log
    try:
        payload = {
            'sessionId': SESSION_ID,
            'runId': run_id,
            'hypothesisId': hypothesis_id,
            'location': location,
            'message': message,
            'data': data or {},
            'timestamp': int(time.time() * 1000),
        }
        with open(DEBUG_LOG_PATH, 'a', encoding='utf-8') as log_file:
            log_file.write(json.dumps(payload) + '\n')
    except OSError:
        pass
    # #endregion


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
                injected = self._inject_missing_streamfield_counts(request, match.group('pk'))
                if injected:
                    _debug_log(
                        hypothesis_id='A',
                        location='shopify_content/wagtail_ai_fixes.py:StreamFieldPreviewFixMiddleware',
                        message='Injected missing StreamField count keys',
                        data={'page_pk': match.group('pk'), 'fields': injected},
                    )
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
        content = kwargs.get('content') or ''
        exclude_pks = kwargs.get('exclude_pks') or []
        if not content.strip() and exclude_pks:
            fallback_content = _page_text_from_pk(exclude_pks[0])
            if fallback_content:
                kwargs = {**kwargs, 'content': fallback_content}
                _debug_log(
                    hypothesis_id='D',
                    location='shopify_content/wagtail_ai_fixes.py:execute_with_fallback',
                    message='Loaded page content from DB fallback',
                    data={
                        'page_pk': exclude_pks[0],
                        'content_len': len(fallback_content),
                    },
                )
        return original_execute(self, *args, **kwargs)

    execute_with_fallback._wai_fallback_wrapped = True
    SuggestedContentAgent.execute = execute_with_fallback

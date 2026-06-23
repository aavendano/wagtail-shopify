import json
import time
import traceback

DEBUG_LOG_PATH = '/home/alejandro/apps/wagtail-shopify/.cursor/debug-0938b0.log'
SESSION_ID = '0938b0'


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


def install_wagtail_ai_debug_hooks():
    from wagtail_ai.agents.suggested_content import SuggestedContentAgent

    if getattr(SuggestedContentAgent.execute, '_wai_debug_wrapped', False):
        return

    original_execute = SuggestedContentAgent.execute

    def execute_with_debug(self, *args, **kwargs):
        _debug_log(
            hypothesis_id='B',
            location='shopify_content/wagtail_ai_debug.py:execute_with_debug:entry',
            message='SuggestedContentAgent.execute called',
            data={
                'vector_index': kwargs.get('vector_index'),
                'exclude_pks_len': len(kwargs.get('exclude_pks') or []),
                'content_len': len(kwargs.get('content') or ''),
                'limit': kwargs.get('limit'),
            },
        )
        try:
            result = original_execute(self, *args, **kwargs)
            _debug_log(
                hypothesis_id='B',
                location='shopify_content/wagtail_ai_debug.py:execute_with_debug:success',
                message='SuggestedContentAgent.execute succeeded',
                data={'result_count': len(result) if isinstance(result, list) else None},
            )
            return result
        except Exception as exc:
            _debug_log(
                hypothesis_id='B',
                location='shopify_content/wagtail_ai_debug.py:execute_with_debug:error',
                message='SuggestedContentAgent.execute failed',
                data={
                    'error_type': type(exc).__name__,
                    'error': str(exc)[:500],
                    'traceback': traceback.format_exc()[-1500:],
                },
            )
            raise

    execute_with_debug._wai_debug_wrapped = True
    SuggestedContentAgent.execute = execute_with_debug


class WagtailAISuggestDebugMiddleware:
    """Log suggest-related admin API requests for debug session 0938b0."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        is_suggest = path.endswith('/admin/ai/suggested_content/')
        if is_suggest:
            body_preview = ''
            if request.method == 'POST' and request.body:
                try:
                    parsed = json.loads(request.body)
                    args = parsed.get('arguments', {})
                    body_preview = {
                        'vector_index': args.get('vector_index'),
                        'exclude_pks_len': len(args.get('exclude_pks') or []),
                        'content_len': len(args.get('content') or ''),
                        'limit': args.get('limit'),
                    }
                except json.JSONDecodeError:
                    body_preview = {'json_error': True}
            user = getattr(request, 'user', None)
            _debug_log(
                hypothesis_id='B',
                location='shopify_content/wagtail_ai_debug.py:WagtailAISuggestDebugMiddleware:request',
                message='suggested_content request received',
                data={
                    'method': request.method,
                    'user_authenticated': getattr(user, 'is_authenticated', False),
                    'user_is_staff': getattr(user, 'is_staff', False),
                    'arguments': body_preview,
                },
            )

        response = self.get_response(request)

        if is_suggest:
            _debug_log(
                hypothesis_id='B',
                location='shopify_content/wagtail_ai_debug.py:WagtailAISuggestDebugMiddleware:response',
                message='suggested_content response sent',
                data={
                    'status_code': response.status_code,
                    'content_type': response.get('Content-Type', ''),
                    'body_preview': (response.content[:300].decode('utf-8', errors='replace')
                                     if hasattr(response, 'content') else ''),
                },
            )
        return response

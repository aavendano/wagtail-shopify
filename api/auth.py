import hashlib

from django.conf import settings
from django.utils import timezone
from ninja.security import HttpBearer, SessionAuth as NinjaSessionAuth


def user_is_cms_editor(user) -> bool:
    if not user or not getattr(user, "is_authenticated", False):
        return False
    if user.is_superuser or user.is_staff:
        return True
    return user.groups.filter(name="cms_editors").exists()


class SessionEditorAuth(NinjaSessionAuth):
    """Allow authenticated staff / cms_editors via Django session (SPA same-origin)."""

    openapi_description = (
        "Django session authentication for the merchant CMS SPA at /cms/. "
        "Requires a logged-in staff user or membership in the cms_editors group. "
        "Same-origin requests send the session cookie; include the CSRF token for "
        "unsafe methods."
    )

    def authenticate(self, request, key=None):
        user = getattr(request, "user", None)
        if user_is_cms_editor(user):
            return user
        return None


class ApiKeyAuth(HttpBearer):
    openapi_description = (
        "Bearer token authentication. Pass either an API key or an OAuth access token in "
        "the Authorization header: 'Authorization: Bearer <token>'. API keys are managed "
        "in Django admin under API > API Keys. OAuth clients and tokens are managed under "
        "Django OAuth Toolkit and require the configured MCP scope."
    )

    def authenticate(self, request, token):
        api_key = self._authenticate_api_key(token)
        if api_key:
            return api_key
        return self._authenticate_oauth_token(token)

    def _authenticate_api_key(self, token):
        from .models import ApiKey

        try:
            key_obj = ApiKey.objects.get(key=token, is_active=True)
            ApiKey.objects.filter(pk=key_obj.pk).update(last_used_at=timezone.now())
            return key_obj
        except ApiKey.DoesNotExist:
            return None

    def _authenticate_oauth_token(self, token):
        from oauth2_provider.models import get_access_token_model

        AccessToken = get_access_token_model()
        token_checksum = hashlib.sha256(token.encode("utf-8")).hexdigest()
        required_scopes = getattr(settings, "MCP_OAUTH_REQUIRED_SCOPES", ["mcp"])
        if isinstance(required_scopes, str):
            required_scopes = [required_scopes]

        try:
            access_token = (
                AccessToken.objects.select_related("application", "user")
                .get(token_checksum=token_checksum)
            )
        except AccessToken.DoesNotExist:
            return None

        if not access_token.is_valid(required_scopes):
            return None
        return access_token


# Combined auth for /api/v1/: session editors (SPA) OR bearer API key / OAuth.
API_AUTH = [SessionEditorAuth(), ApiKeyAuth()]

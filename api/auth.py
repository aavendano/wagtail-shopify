import hashlib

from asgiref.sync import sync_to_async
from django.conf import settings
from django.utils import timezone
from ninja.security import HttpBearer


class ApiKeyAuth(HttpBearer):
    openapi_description = (
        "Bearer token authentication. Pass either an API key or an OAuth access token in "
        "the Authorization header: 'Authorization: Bearer <token>'. API keys are managed "
        "in Django admin under API > API Keys. OAuth clients and tokens are managed under "
        "Django OAuth Toolkit and require the configured MCP scope."
    )

    async def authenticate(self, request, token):
        return await sync_to_async(self._authenticate_token, thread_sensitive=True)(token)

    def _authenticate_token(self, token):
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

    async def __call__(self, request):
        auth_value = request.headers.get(self.header)
        if not auth_value:
            return None
        parts = auth_value.split(" ")
        if parts[0].lower() != self.openapi_scheme:
            return None
        token = " ".join(parts[1:])
        return await self.authenticate(request, token)

from asgiref.sync import sync_to_async
from django.utils import timezone
from ninja.security import HttpBearer


class ApiKeyAuth(HttpBearer):
    openapi_description = (
        "Bearer token authentication. Pass your API key in the Authorization header: "
        "'Authorization: Bearer <your_api_key>'. "
        "API keys are managed in Django admin under API > API Keys."
    )

    async def authenticate(self, request, token):
        return await sync_to_async(self._authenticate_token, thread_sensitive=True)(token)

    def _authenticate_token(self, token):
        from .models import ApiKey

        try:
            key_obj = ApiKey.objects.get(key=token, is_active=True)
            ApiKey.objects.filter(pk=key_obj.pk).update(last_used_at=timezone.now())
            return key_obj
        except ApiKey.DoesNotExist:
            return None

    async def __call__(self, request):
        auth_value = request.headers.get(self.header)
        if not auth_value:
            return None
        parts = auth_value.split(" ")
        if parts[0].lower() != self.openapi_scheme:
            return None
        token = " ".join(parts[1:])
        return await self.authenticate(request, token)

from ninja.security import HttpBearer
from django.utils import timezone


class ApiKeyAuth(HttpBearer):
    openapi_description = (
        "Bearer token authentication. Pass your API key in the Authorization header: "
        "'Authorization: Bearer <your_api_key>'. "
        "API keys are managed in Django admin under API > API Keys."
    )

    def authenticate(self, request, token):
        from .models import ApiKey
        try:
            key_obj = ApiKey.objects.get(key=token, is_active=True)
            ApiKey.objects.filter(pk=key_obj.pk).update(last_used_at=timezone.now())
            return key_obj
        except ApiKey.DoesNotExist:
            return None

from django.conf import settings
from django.http import JsonResponse
from django.views import View


def _public_base_url() -> str:
    base = (getattr(settings, "SHOPIFY_APP_URL", None) or settings.WAGTAILADMIN_BASE_URL).rstrip("/")
    return base


def oauth_authorization_server_metadata(request):
    base = _public_base_url()
    scopes = list(getattr(settings, "OAUTH2_PROVIDER", {}).get("SCOPES", {}).keys()) or ["mcp"]
    return JsonResponse(
        {
            "issuer": base,
            "authorization_endpoint": f"{base}/authorize",
            "token_endpoint": f"{base}/token",
            "response_types_supported": ["code"],
            "grant_types_supported": ["authorization_code", "refresh_token"],
            "code_challenge_methods_supported": ["S256"],
            "scopes_supported": scopes,
        }
    )


class OAuthProtectedResourceMetadataView(View):
    """MCP clients discover the authorization server from this document."""

    def get(self, request, *args, **kwargs):
        base = _public_base_url()
        return JsonResponse(
            {
                "resource": f"{base}/api/v1/mcp",
                "authorization_servers": [base],
                "scopes_supported": list(
                    getattr(settings, "OAUTH2_PROVIDER", {}).get("SCOPES", {}).keys()
                )
                or ["mcp"],
                "bearer_methods_supported": ["header"],
            }
        )

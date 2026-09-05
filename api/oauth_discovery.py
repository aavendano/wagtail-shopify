from django.conf import settings
from django.http import JsonResponse
from django.views import View


def _public_base_url() -> str:
    base = (getattr(settings, "SHOPIFY_APP_URL", None) or settings.WAGTAILADMIN_BASE_URL).rstrip("/")
    return base


def _cors(response):
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Authorization, Content-Type, MCP-Protocol-Version"
    return response


def oauth_authorization_server_metadata(request):
    base = _public_base_url()
    scopes = list(getattr(settings, "OAUTH2_PROVIDER", {}).get("SCOPES", {}).keys()) or ["mcp"]
    return _cors(
        JsonResponse(
            {
                "issuer": base,
                "authorization_endpoint": f"{base}/authorize",
                "token_endpoint": f"{base}/token",
                "registration_endpoint": f"{base}/register",
                "response_types_supported": ["code"],
                "grant_types_supported": ["authorization_code", "refresh_token"],
                "code_challenge_methods_supported": ["S256"],
                "token_endpoint_auth_methods_supported": ["none"],
                "scopes_supported": scopes,
            }
        )
    )


class OAuthProtectedResourceMetadataView(View):
    """MCP clients discover the authorization server from this document."""

    def get(self, request, *args, **kwargs):
        base = _public_base_url()
        return _cors(
            JsonResponse(
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
        )

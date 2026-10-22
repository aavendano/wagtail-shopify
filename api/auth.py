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


def user_has_shop_membership_access(request, user) -> bool:
    """Fail-closed membership gate for session CMS editors.

    Requires an authorized session shop (or sole-shop auto-seed). When shops
    are installed but the user has no membership and is not a superuser,
    access is denied. When no ShopConfig exists yet, staff editors may still
    authenticate (install/bootstrap flows).
    """
    from shopify_config.membership import user_may_access_shop
    from shopify_config.tenancy import (
        ShopUnresolvedError,
        ensure_session_shop,
        installed_shop_domains,
        resolve_sole_installed_shop,
    )

    if getattr(user, "is_superuser", False):
        shop = ensure_session_shop(request)
        if not shop:
            try:
                ensure_session_shop(request, resolve_sole_installed_shop())
            except ShopUnresolvedError:
                pass
        return True

    shop = ensure_session_shop(request)
    if shop:
        return user_may_access_shop(user, shop)

    try:
        sole = resolve_sole_installed_shop()
    except ShopUnresolvedError:
        # No installed shop yet — allow staff/editors for onboarding.
        return not bool(installed_shop_domains())

    if user_may_access_shop(user, sole):
        ensure_session_shop(request, sole)
        return True
    return False


class CmsEditorSessionAuth(NinjaSessionAuth):
    """Staff / cms_editors only — no shop membership gate (session-shop selector)."""

    openapi_description = (
        "Django session authentication for CMS editors selecting a shop. "
        "Requires staff or cms_editors; membership is checked when setting a shop."
    )

    def authenticate(self, request, key=None):
        user = getattr(request, "user", None)
        if user_is_cms_editor(user):
            return user
        return None


class SessionEditorAuth(NinjaSessionAuth):
    """Allow authenticated staff / cms_editors via Django session (SPA same-origin)."""

    openapi_description = (
        "Django session authentication for the merchant CMS SPA at /cms/. "
        "Requires a logged-in staff user or membership in the cms_editors group, "
        "plus ShopMembership for the session shop (or sole installed shop). "
        "Same-origin requests send the session cookie; include the CSRF token for "
        "unsafe methods."
    )

    def authenticate(self, request, key=None):
        user = getattr(request, "user", None)
        if not user_is_cms_editor(user):
            return None
        if not user_has_shop_membership_access(request, user):
            return None
        return user


class ApiKeyAuth(HttpBearer):
    openapi_description = (
        "Bearer token authentication. Pass either an API key or an OAuth access token in "
        "the Authorization header: 'Authorization: Bearer <token>'. API keys are managed "
        "in Django admin under API > API Keys. OAuth clients and tokens are managed under "
        "Django OAuth Toolkit and require the configured MCP scope. "
        "ApiKey is deploy-scoped (one shop per install); per-shop API key scope is a follow-up."
    )

    def authenticate(self, request, token):
        return self._authenticate_token(token)

    def _authenticate_token(self, token):
        """Validate API key or OAuth access token (used by MCP Streamable auth)."""
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

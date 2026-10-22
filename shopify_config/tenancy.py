"""Shop tenant resolution for deploy-per-shop Wagtail Shopify.

Tenant identity is the normalized Shopify shop domain string — the same value
stored on ``ShopConfig.shop`` (e.g. ``playlovetoys.myshopify.com``).

One process/DB = one merchant store. Session + membership gate which staff may
operate that store; pages stay shop-agnostic (no ``shop`` FK on Wagtail pages).
"""

from __future__ import annotations

from django.conf import settings
from django.http import HttpRequest

# Session key set by App Home / session-shop API.
SESSION_SHOP = "shopify_session_shop"

# Used only by management commands / local single-tenant tooling.
# Never used as a silent fallback on request-scoped paths.
LEGACY_PUBLICATION_SHOP_SETTING = "SHOPIFY_PUBLICATION_SHOP"


class ShopUnresolvedError(RuntimeError):
    """No shop tenant could be resolved for a tenant-scoped operation."""

    error_code = "shop_unresolved"


def normalize_shop(raw: str | None) -> str:
    """Normalize a shop domain to the canonical ``*.myshopify.com`` form."""
    value = (raw or "").strip().lower()
    if not value:
        return ""
    value = value.removeprefix("https://").removeprefix("http://")
    value = value.split("/")[0].strip()
    if not value:
        return ""
    if not value.endswith(".myshopify.com"):
        # Accept bare store handle from OAuth forms.
        value = f"{value}.myshopify.com"
    return value


def resolve_current_shop(request: HttpRequest) -> str:
    """Resolve the current shop tenant for a request.

    Order:
    1. Session ``SESSION_SHOP`` (set by embedded App Home / shop selection)
    2. Never ``SHOPIFY_PUBLICATION_SHOP`` — that setting is management-command only

    Raises :class:`ShopUnresolvedError` when no shop is available.
    """
    session = getattr(request, "session", None)
    if session is not None:
        session_shop = normalize_shop(session.get(SESSION_SHOP) or "")
        if session_shop:
            return session_shop
    raise ShopUnresolvedError(
        "shop tenant is not resolved; authenticate via Shopify or select a shop"
    )


def installed_shop_domains() -> list[str]:
    """Normalized shop domains from installed ``ShopConfig`` rows (sorted)."""
    from shopify_config.models import ShopConfig

    return sorted(
        {
            normalize_shop(raw)
            for raw in ShopConfig.objects.values_list("shop", flat=True)
            if normalize_shop(raw)
        }
    )


def is_installed_shop(shop: str | None) -> bool:
    """True when ``shop`` has a ShopConfig (the Shopify app is installed).

    ShopConfig rows may store either the bare handle or the full domain.
    """
    normalized = normalize_shop(shop)
    if not normalized:
        return False
    from shopify_config.models import ShopConfig

    handle = normalized.removesuffix(".myshopify.com")
    return ShopConfig.objects.filter(shop__in=[normalized, handle]).exists()


def resolve_sole_installed_shop() -> str:
    """Return the sole installed shop domain.

    Raises :class:`ShopUnresolvedError` when zero or more than one ShopConfig
    exists. Intended for Celery/hooks/sync without an HTTP request.
    """
    domains = installed_shop_domains()
    if len(domains) == 1:
        return domains[0]
    if not domains:
        raise ShopUnresolvedError(
            "No ShopConfig found. Install the app on a Shopify store first."
        )
    raise ShopUnresolvedError(
        f"Multiple ShopConfig rows ({len(domains)}); pass an explicit shop."
    )


def ensure_session_shop(request: HttpRequest, preferred: str | None = None) -> str:
    """Persist and return a shop tenant on the Django session when possible.

    Order (membership-gated):
    1. Explicit ``preferred`` when installed and the user may access it
    2. Existing ``SESSION_SHOP`` when still authorized; otherwise clear it
    3. Sole shop the user may access among installed tenants

    Returns "" when still unresolved (caller shows Connect shop / picker).
    Superusers may access any installed shop.
    """
    from shopify_config.membership import user_may_access_shop, user_shops

    session = getattr(request, "session", None)
    user = getattr(request, "user", None)

    def _try_set(shop: str) -> str:
        if not shop or not is_installed_shop(shop):
            return ""
        if not user_may_access_shop(user, shop):
            return ""
        if session is not None:
            session[SESSION_SHOP] = shop
        return shop

    preferred_shop = normalize_shop(preferred)
    if preferred_shop:
        accepted = _try_set(preferred_shop)
        if accepted:
            return accepted

    if session is None:
        return ""

    current = normalize_shop(session.get(SESSION_SHOP) or "")
    if current:
        if user_may_access_shop(user, current) and is_installed_shop(current):
            return current
        session.pop(SESSION_SHOP, None)

    allowed = [s for s in user_shops(user) if is_installed_shop(s)]
    if len(allowed) == 1:
        session[SESSION_SHOP] = allowed[0]
        return allowed[0]
    return ""


def set_session_shop(request: HttpRequest, shop: str | None) -> str:
    """Set ``SESSION_SHOP`` when installed and the user may access it.

    Unlike :func:`ensure_session_shop`, does **not** fall back to a sole
    allowed shop when ``shop`` is rejected. Returns "" when rejected.
    """
    from shopify_config.membership import user_may_access_shop

    session = getattr(request, "session", None)
    user = getattr(request, "user", None)
    normalized = normalize_shop(shop)
    if not normalized or not is_installed_shop(normalized):
        return ""
    if not user_may_access_shop(user, normalized):
        return ""
    if session is not None:
        session[SESSION_SHOP] = normalized
    return normalized


def resolve_shop_for_command(
    *, shop: str | None = None, allow_settings_fallback: bool = True
) -> str:
    """Resolve shop for management commands.

    Prefer an explicit ``--shop`` argument. Optionally fall back to
    ``SHOPIFY_PUBLICATION_SHOP`` for local single-tenant tooling.
    Does not fall back to sole-shop — callers use
    :func:`resolve_shop_for_command_or_sole`.
    """
    explicit = normalize_shop(shop)
    if explicit:
        return explicit
    if allow_settings_fallback:
        return normalize_shop(getattr(settings, LEGACY_PUBLICATION_SHOP_SETTING, "") or "")
    return ""


def resolve_shop_for_command_or_sole(*, shop: str | None = None) -> str:
    """Resolve ``--shop`` / settings, else the sole installed ShopConfig."""
    resolved = resolve_shop_for_command(shop=shop)
    if resolved:
        return resolved
    return resolve_sole_installed_shop()


def add_shop_argument(parser) -> None:
    """Add a shared ``--shop`` flag to a management command parser."""
    parser.add_argument(
        "--shop",
        default="",
        help=(
            "Shopify shop domain (e.g. store.myshopify.com). "
            "Defaults to SHOPIFY_PUBLICATION_SHOP or the sole installed ShopConfig."
        ),
    )


def require_shop(shop: str | None) -> str:
    """Normalize and require a non-empty shop string."""
    normalized = normalize_shop(shop)
    if not normalized:
        raise ShopUnresolvedError("shop tenant is required")
    return normalized

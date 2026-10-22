"""
Validation for embedded redirect targets (defense in depth before calling SDK helpers).
"""

from __future__ import annotations

from typing import Optional
from urllib.parse import urlparse

from django.conf import settings


def validate_relative_app_path(path: str) -> Optional[str]:
    """
    Return None if valid in-app redirect path (must start with '/', not '//').
    Otherwise return an error message for HTTP 400 bodies.
    """
    if not path or not isinstance(path, str):
        return "Missing or invalid path."
    stripped = path.strip()
    if not stripped.startswith("/"):
        return "Path must be a relative URL starting with '/'."
    if stripped.startswith("//"):
        return "Protocol-relative URLs are not allowed."
    return None


def parent_redirect_allowed_hosts() -> set[str]:
    hosts: set[str] = set()
    allowed = getattr(settings, "SHOPIFY_PARENT_REDIRECT_ALLOWED_HOSTS", None)
    if allowed:
        for h in allowed:
            if h:
                hosts.add(h.lower().strip())
    domain = getattr(settings, "SHOPIFY_APP_DOMAIN", None)
    if domain:
        hosts.add(domain.lower().strip())
    app_url = getattr(settings, "SHOPIFY_APP_URL", None)
    if app_url:
        try:
            parsed = urlparse(app_url if "://" in app_url else f"https://{app_url}")
            if parsed.hostname:
                hosts.add(parsed.hostname.lower())
        except Exception:
            pass
    hosts.add("admin.shopify.com")
    return hosts


def validate_parent_redirect_url(url: str) -> Optional[str]:
    """
    Return None if URL is allowed (https/http, host in allowlist).
    Otherwise return error message for 400 response.
    """
    if not url or not isinstance(url, str):
        return "Missing or invalid URL."
    stripped = url.strip()
    if not stripped:
        return "Missing or invalid URL."
    parsed = urlparse(stripped)
    if parsed.scheme not in ("http", "https"):
        return "URL must use http or https."
    host = (parsed.hostname or "").lower()
    if not host:
        return "URL must include a host."
    allowed = parent_redirect_allowed_hosts()
    if host not in allowed:
        return "Redirect host is not allowed."
    return None

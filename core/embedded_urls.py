"""
Build in-app URLs for the Shopify embedded surface while preserving query params.
"""

from __future__ import annotations

from urllib.parse import urlencode

from django.http import HttpRequest, QueryDict
from django.urls import reverse


def _query_with_ops(request: HttpRequest, *, ops: bool) -> QueryDict:
    query = request.GET.copy()
    if ops:
        query["ops"] = "1"
    elif "ops" in query:
        del query["ops"]
    return query


def embedded_app_home_url(request: HttpRequest, *, ops: bool = False) -> str:
    """Return /shopify-admin/ with request.GET, optionally forcing ops=1."""
    url = reverse("home")
    query = _query_with_ops(request, ops=ops)
    if not query:
        return url
    return f"{url}?{urlencode(query, doseq=True)}"


def embedded_cms_url(request: HttpRequest) -> str:
    """Return /cms/ with the same embedded query params (ops stripped)."""
    query = _query_with_ops(request, ops=False)
    if not query:
        return "/cms/"
    return f"/cms/?{urlencode(query, doseq=True)}"

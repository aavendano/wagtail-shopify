"""Wagtail-like HTML preview for Content API pages."""

from __future__ import annotations

from django.http import HttpResponse
from django.template.loader import render_to_string


def render_page_preview(request, page) -> HttpResponse:
    """Render a Wagtail page template using the latest revision when available."""
    revision = None
    try:
        revision = page.get_latest_revision()
    except Exception:
        revision = None

    preview_page = page
    if revision is not None:
        try:
            preview_page = revision.as_object()
        except Exception:
            preview_page = page

    template_name = getattr(preview_page, "template", None) or "shopify_content/root_page.html"
    context = {
        "page": preview_page,
        "self": preview_page,
        "request": request,
        "preview_mode": True,
    }
    html = render_to_string(template_name, context, request=request)
    return HttpResponse(html, content_type="text/html; charset=utf-8")


def save_page_draft(page):
    """Persist fields and create a Wagtail revision without publishing."""
    page.save()
    return page.save_revision()

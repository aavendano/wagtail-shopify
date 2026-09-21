"""Rendering security profiles for editorial HTML."""

from __future__ import annotations

import re
from enum import Enum

_SCRIPT_RE = re.compile(r"<script\b[^>]*>.*?</script>", re.IGNORECASE | re.DOTALL)
_ON_ATTR_RE = re.compile(r"\s+on\w+\s*=\s*[\"'][^\"']*[\"']", re.IGNORECASE)
_JAVASCRIPT_URL_RE = re.compile(r"(href|src)\s*=\s*[\"']\s*javascript:", re.IGNORECASE)


class RenderProfile(str, Enum):
    TRUSTED_EDITORIAL = "trusted_editorial"
    RESTRICTED = "restricted"


def sanitize_html_for_profile(html: str, profile: RenderProfile) -> str:
    if profile == RenderProfile.TRUSTED_EDITORIAL:
        return html
    cleaned = _SCRIPT_RE.sub("", html or "")
    cleaned = _ON_ATTR_RE.sub("", cleaned)
    cleaned = _JAVASCRIPT_URL_RE.sub("", cleaned)
    return cleaned

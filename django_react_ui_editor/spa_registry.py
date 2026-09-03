from __future__ import annotations

from dataclasses import dataclass
from typing import Type

from django.urls import include, path

_REGISTRY: dict[str, "SpaRegistration"] = {}


@dataclass(frozen=True)
class SpaRegistration:
    app_label: str
    url_prefix: str
    urlconf: str
    mount_model: Type
    mount_slug: str


def register_spa(
    *,
    app_label: str,
    url_prefix: str,
    urlconf: str,
    mount_model: Type,
    mount_slug: str,
) -> SpaRegistration:
    """Register a SPA mount so get_spa_urlpatterns() can wire it."""
    prefix = url_prefix.strip("/")
    reg = SpaRegistration(
        app_label=app_label,
        url_prefix=prefix,
        urlconf=urlconf,
        mount_model=mount_model,
        mount_slug=mount_slug,
    )
    _REGISTRY[app_label] = reg
    return reg


def get_registered_spas() -> dict[str, SpaRegistration]:
    return dict(_REGISTRY)


def get_spa_urlpatterns():
    """URL patterns for all registered SPAs (call after apps are ready)."""
    patterns = []
    for reg in _REGISTRY.values():
        patterns.append(
            path(f"{reg.url_prefix}/", include(reg.urlconf)),
        )
    return patterns

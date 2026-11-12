from __future__ import annotations

import hashlib
import os
from functools import lru_cache
from pathlib import Path

from django.conf import settings


@lru_cache(maxsize=1)
def cms_spa_asset_version() -> str:
    """Short cache-bust token for spa-public.js/css (deploy or file hash)."""
    env_version = os.environ.get("CMS_SPA_ASSET_VERSION", "").strip()
    if env_version:
        return env_version
    js_path = Path(settings.BASE_DIR) / "cms_ui" / "static" / "cms_ui" / "spa-public.js"
    if not js_path.is_file():
        return "0"
    digest = hashlib.sha256(js_path.read_bytes()).hexdigest()
    return digest[:12]

import api.ninja_compat  # noqa: F401 — patch URL converters before ninja import

from django.conf import settings
from ninja import NinjaAPI

from .auth import ApiKeyAuth
from .openapi_agent import build_openapi_tags
from .routers.products import router as products_router
from .routers.collections import router as collections_router
from .routers.blogs import router as blogs_router
from .routers.articles import router as articles_router
from .routers.locations import router as locations_router
from .routers.glossary import router as glossary_router
from .routers.home import router as home_router
from .routers.semantic_links import router as semantic_links_router
from .routers.capabilities import router as capabilities_router


def openapi_servers() -> list[dict[str, str]]:
    """Absolute public host for OpenAPI `servers` (ChatGPT Actions requires it).

    Paths in the mounted schema are `/api/v1/...`, so the server URL must be the
    origin only (no `/api/v1` suffix).
    """
    base = (
        getattr(settings, "SHOPIFY_APP_URL", None)
        or getattr(settings, "WAGTAILADMIN_BASE_URL", "")
        or ""
    ).rstrip("/")
    if not base.startswith(("http://", "https://")):
        return []
    return [{"url": base, "description": "Public CMS host"}]

API_DESCRIPTION = """
# Wagtail-Shopify Content API (AI Agent Tool Registry)

Autonomous content management across Wagtail CMS and Shopify. Every endpoint runs **synchronously**
and returns final results in the HTTP response — no Celery jobs, no polling.

OpenAPI spec: `/api/v1/openapi.json` · Agent catalog: `GET /api/v1/capabilities/` · Interactive docs: `/api/v1/docs/`

## Authentication

All endpoints require a bearer token. Existing API keys and OAuth access tokens issued
for MCP clients are both accepted:

```
Authorization: Bearer <api_key_or_oauth_access_token>
```

Create API keys in **Django Admin → API → API Keys** (`/admin-django/`). Create OAuth
clients in **Django Admin → Django OAuth Toolkit → Applications** and request the
`mcp` scope through `/o/authorize/` and `/o/token/`. Missing or invalid tokens return **401**.

## Tool Matrix

| Resource | List | Get | Create | Update | Delete | Pull (Shopify→Wagtail) | Push (Wagtail→Shopify) |
|----------|------|-----|--------|--------|--------|------------------------|------------------------|
| Products | GET /products/ | GET /products/{id} | POST /products/ | PATCH /products/{id} | DELETE /products/{id} | POST /products/pull | POST /products/{id}/push |
| Collections | GET /collections/ | GET /collections/{id} | POST /collections/ | PATCH /collections/{id} | DELETE /collections/{id} | POST /collections/pull | POST /collections/{id}/push |
| Blogs | GET /blogs/ | GET /blogs/{id} | POST /blogs/ | PATCH /blogs/{id} | DELETE /blogs/{id} | POST /blogs/pull | POST /blogs/{id}/push |
| Articles | GET /articles/ | GET /articles/{id} | POST /articles/ | PATCH /articles/{id} | DELETE /articles/{id} | POST /articles/pull | POST /articles/{id}/push |
| Locations | GET /locations/ | GET /locations/{id} | POST /locations/ | PATCH /locations/{id} | DELETE /locations/{id} | — (Wagtail-only) | POST /locations/{id}/push |
| Glossary | GET /glossary/ | GET /glossary/{id} | POST /glossary/ | PATCH /glossary/{id} | DELETE /glossary/{id} | POST /glossary/pull | POST /glossary/{id}/push |
| Home | GET /home/ | GET /home/{id} | POST /home/ | PATCH /home/{id} | DELETE /home/{id} | — (Wagtail-only) | POST /home/{id}/push |

**Semantic links (preview):** `POST /semantic-links/suggest` — nearest neighbors with similarity scores. Read-only; does not persist related-link FKs. Requires `locale` plus `page_id` or draft `text`/fields. Independent of the 5-per-type production cap.

**Pull** returns HTTP 200 with `{created, updated, skipped, errors, message}` immediately.
**Push** returns HTTP 200 with `{success, message, shopify_id}` immediately.

## Agent Workflows

### Products / Collections (existing Shopify catalog)

1. `POST /products/pull` — import all products; read stats in response body.
2. `GET /products/?locale=en-US` — list pages; note `id` and `shopify_id`.
3. `PATCH /products/{id}` with content + `"publish": true` — save and sync if `sync_enabled=true`.
4. `GET /products/{id}` — verify `last_synced_at` updated.

### Blogs and Articles

1. `POST /blogs/pull` — imports blogs **and** articles in one call.
2. `GET /articles/?blog_id={blog_page_id}` — filter articles by parent blog.
3. `PATCH /articles/{id}` with `"publish": true` — parent BlogPage must have `shopify_id`.

### Locations (Wagtail-origin metaobjects)

Locations have **no pull** — content is authored in Wagtail and pushed to Shopify metaobject type `local_page`.

1. `POST /locations/` with `titulo` and content fields.
2. `PATCH /locations/{id}` with `"publish": true` (optional).
3. `POST /locations/{id}/push` — upserts metaobject; `shopify_id` saved on first success.
4. `GET /locations/{id}` — verify `last_synced_at` and `shopify_id`.

### Glossary (Shopify metaobjects)

Pull syncs **images from Shopify** into Wagtail (`image_url`, `shopify_image_id`, `image_alt_text`) without overwriting existing term text or definitions.

1. `POST /glossary/pull` — import metaobjects; existing pages get image fields only.
2. `GET /glossary/?locale_code=en&full=true` — verify `image_url` populated.
3. Index rebuild runs automatically after pull (`custom.index_listings` on Page handle `glossary`).
4. `POST /glossary/{id}/push` — push Wagtail-authored content when needed.

Note: `locale_code` (en/es/fr) is the Shopify metaobject locale, distinct from Wagtail `locale`.

### Home (Wagtail-origin metaobjects)

Home pages have **no pull** — content is authored via this API (AI agents) and pushed to Shopify metaobject type `home_page` (one metaobject per locale). `sections_json` is always normalized to 13 section types; send one typed field (e.g. `editorial_intro`) or a partial envelope.

1. `POST /home/` with `hero_heading` and locale (section skeleton is filled automatically).
2. `PATCH /home/{id}` with typed section fields and `"publish": true` (optional).
3. `POST /home/{id}/push` — upserts metaobject; `shopify_id` saved on first success.
4. `GET /home/{id}` — verify `sections_json` (13 types), `last_synced_at`, and `shopify_id`.

### Semantic related preview

1. `POST /semantic-links/suggest` with `locale` and either `page_id` or draft `text`/`title`/`definition` (set `page_type`).
2. Pass `types: ["collection"]` and a higher `limit_per_type` (default 20) for gap analysis; production publish still caps auto-links at 5.

Note: `WAGTAIL_AI_PGVECTOR` and a populated `PageIndex` are required. HTTP 503 if the vector index is unavailable.

## Sync Model

- `shopify_id` — Shopify GID linking Wagtail page to Shopify resource.
- `sync_enabled` — when true, `publish=true` triggers outbound sync via Wagtail publish hook.
- `last_synced_at` — UTC timestamp of last successful push; null if never synced.
- `translation_of` / `translation_page_ids` — link locale variants; shared `shopify_id` on translations.

## Localization

Markets: `en-US` (primary), `es-US`, `en-CA`, `fr-CA`. Filter lists with `?locale=es-US`.
Set `locale` on create; use `translation_of` (Wagtail page ID) to link variants.

## Common Errors

| Status | Meaning |
|--------|---------|
| 401 | Missing or invalid bearer token |
| 400 | ShopConfig/token missing, validation error, or sync failure detail |
| 404 | Page ID not found |

## Notes

- API operations are **synchronous only**. Wagtail admin and embedded app UI may still use background Celery jobs.
- DELETE removes Wagtail pages only — Shopify resources are not deleted.
- Use `operation_id` values in OpenAPI for stable AI tool names.
"""

_OPENAPI_SERVERS = openapi_servers()

# #region agent log
try:
    import json as _json
    import time as _time
    from pathlib import Path as _Path

    _Path("/home/alejandro/apps/.cursor/debug-d032c4.log").open("a").write(
        _json.dumps(
            {
                "sessionId": "d032c4",
                "runId": "post-fix",
                "hypothesisId": "A",
                "location": "api/main.py:openapi_servers",
                "message": "NinjaAPI servers configured",
                "data": {
                    "servers": _OPENAPI_SERVERS,
                    "has_valid_absolute_url": bool(_OPENAPI_SERVERS),
                },
                "timestamp": int(_time.time() * 1000),
            }
        )
        + "\n"
    )
except Exception:
    pass
# #endregion

api = NinjaAPI(
    title="Wagtail-Shopify Content API",
    version="1.1.0",
    urls_namespace="wagtail_shopify_api",
    description=API_DESCRIPTION,
    auth=ApiKeyAuth(),
    docs_url="/docs/",
    openapi_url="/openapi.json",
    servers=_OPENAPI_SERVERS,
    openapi_extra={"tags": build_openapi_tags()},
)

api.add_router('/products/', products_router, tags=['Products'])
api.add_router('/collections/', collections_router, tags=['Collections'])
api.add_router('/blogs/', blogs_router, tags=['Blogs'])
api.add_router('/articles/', articles_router, tags=['Articles'])
api.add_router('/locations/', locations_router, tags=['Locations'])
api.add_router('/glossary/', glossary_router, tags=['Glossary'])
api.add_router('/home/', home_router, tags=['Home'])
api.add_router('/semantic-links/', semantic_links_router, tags=['Semantic Links'])
api.add_router('/capabilities/', capabilities_router, tags=['Capabilities'])

from .mcp import setup_mcp  # noqa: E402

setup_mcp(api, API_DESCRIPTION)

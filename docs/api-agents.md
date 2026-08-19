# Wagtail-Shopify Content API — Agent Guide

API autodescriptiva para agentes AI que gestionan contenido entre Wagtail CMS y Shopify.
Todas las operaciones de la API son **síncronas**: la respuesta HTTP contiene el resultado final.

> **Mantener actualizada:** cualquier cambio en `/api/v1/` debe reflejarse en la documentación en el mismo cambio.
> Política y checklist: [`.cursor/rules/api-documentation.mdc`](../.cursor/rules/api-documentation.mdc).
> Fuente única de verdad de capacidades: `api/agent_registry.py`.

## Quick start

### 1. Crear credencial

Opción API key:

1. Abre **Django Admin** en `/admin-django/` (no confundir con Wagtail en `/admin/`)
2. Ve a **API → API Keys → Add**  
   Atajo desde Wagtail: **Settings → API Keys**
3. Pon un nombre descriptivo (p.ej. `Production Agent`)
4. Guarda — la key se genera automáticamente (cópiala; no se vuelve a mostrar completa)

Opción OAuth para clientes MCP:

1. Ejecuta migraciones de OAuth Toolkit: `python3 manage.py migrate oauth2_provider`
2. En Django Admin (`/admin-django/`), ve a **Django OAuth Toolkit → Applications → Add**  
   Atajo desde Wagtail: **Settings → OAuth Applications**  
   URL directa: `/admin-django/oauth2_provider/application/add/`
3. Crea el cliente MCP con su redirect URI y el grant type apropiado para el cliente
4. Autoriza el cliente en `/authorize` (o `/o/authorize/`) y canjea el code en `/token` (o `/o/token/`) solicitando scope `mcp`

### 2. Primera request

```bash
export API_KEY="tu-key-aqui"
export BASE="https://wagtail-dev.aadigitalbusiness.com/api/v1"

curl -s -H "Authorization: Bearer $API_KEY" "$BASE/openapi.json" | head
```

### 3. Documentación interactiva

- OpenAPI JSON: `/api/v1/openapi.json` (incluye `servers` con URL absoluta del host público)
- **Catálogo de capacidades (agentes):** `GET /api/v1/capabilities/`
- Swagger UI: `/api/v1/docs/`
- **ChatGPT Actions (import inmediato):** pegar `docs/openapi-chatgpt.json` (OpenAPI 3.0.3 + `servers`). Auth: API Key → Bearer.

Usa los `operation_id` del OpenAPI como nombres estables de herramientas (p.ej. `pull_products_sync_post`, `push_location`).

---

## Catálogo de capacidades

**Entry point recomendado para agentes:** `GET /api/v1/capabilities/`

Devuelve un JSON con todas las herramientas, prerequisitos, `next_tools` sugeridos y workflows predefinidos. Comparte la misma metadata que OpenAPI (`x-agent-*`).

```bash
curl -s -H "Authorization: Bearer $API_KEY" "$BASE/capabilities/" | jq '.tools | length'
curl -s -H "Authorization: Bearer $API_KEY" "$BASE/capabilities/" | jq '.workflows.products_existing_store'
```

### Tipos de capacidad (`capability_type`)

| Valor | Significado |
|-------|-------------|
| `discover` | Listar o descubrir recursos (p.ej. `list_products`) |
| `read` | Leer un recurso por ID |
| `create` | Crear página en Wagtail |
| `update` | Actualizar parcialmente; `publish=true` puede disparar sync |
| `delete` | Eliminar solo en Wagtail |
| `sync_inbound` | Pull Shopify → Wagtail (respuesta `ImportResultSchema`) |
| `sync_outbound` | Push Wagtail → Shopify (respuesta `SyncResultSchema`) |

### Extensiones OpenAPI (`x-agent-*`)

Cada operación en `/openapi.json` incluye:

| Campo | Descripción |
|-------|-------------|
| `x-agent-capability-type` | Tipo de capacidad (ver tabla anterior) |
| `x-agent-resource` | Recurso: `products`, `collections`, `blogs`, `articles`, `locations`, `glossary` |
| `x-agent-sync-direction` | `shopify_to_wagtail` o `wagtail_to_shopify` (solo sync) |
| `x-agent-prerequisites` | Lista de condiciones previas |
| `x-agent-next-tools` | `operation_id` sugeridos tras éxito |

La fuente única de verdad es `api/agent_registry.py` — OpenAPI y `/capabilities/` se generan desde ahí.


## Autenticación

| Header | Valor |
|--------|-------|
| `Authorization` | `Bearer <api_key>` o `Bearer <oauth_access_token>` |

| Respuesta | Causa |
|-----------|-------|
| 401 | Sin header, API key inválida/desactivada, token OAuth expirado o sin scope `mcp` |

---

## Matriz de herramientas

| Recurso | List | Get | Create | Update | Delete | Pull | Push |
|---------|------|-----|--------|--------|--------|------|------|
| Products | `GET /products/` | `GET /products/{id}` | `POST /products/` | `PATCH /products/{id}` | `DELETE /products/{id}` | `POST /products/pull` | `POST /products/{id}/push` |
| Collections | `GET /collections/` | `GET /collections/{id}` | `POST /collections/` | `PATCH /collections/{id}` | `DELETE /collections/{id}` | `POST /collections/pull` | `POST /collections/{id}/push` |
| Blogs | `GET /blogs/` | `GET /blogs/{id}` | `POST /blogs/` | `PATCH /blogs/{id}` | `DELETE /blogs/{id}` | `POST /blogs/pull` | `POST /blogs/{id}/push` |
| Articles | `GET /articles/` | `GET /articles/{id}` | `POST /articles/` | `PATCH /articles/{id}` | `DELETE /articles/{id}` | `POST /articles/pull` | `POST /articles/{id}/push` |
| Locations | `GET /locations/` | `GET /locations/{id}` | `POST /locations/` | `PATCH /locations/{id}` | `DELETE /locations/{id}` | — | `POST /locations/{id}/push` |
| Glossary | `GET /glossary/` | `GET /glossary/{id}` | `POST /glossary/` | `PATCH /glossary/{id}` | `DELETE /glossary/{id}` | `POST /glossary/pull` | `POST /glossary/{id}/push` |
| Home | `GET /home/` | `GET /home/{id}` | `POST /home/` | `PATCH /home/{id}` | `DELETE /home/{id}` | — | `POST /home/{id}/push` |
| Semantic links | `POST /semantic-links/suggest` (preview only; no persist) | — | — | — | — | — | — |

---

## Respuestas de sync

### Pull (Shopify → Wagtail) — HTTP 200

```json
{
  "created": 12,
  "updated": 45,
  "skipped": 0,
  "errors": 1,
  "message": "Products — Creados: 12, Actualizados: 45, Errores: 1"
}
```

La request **bloquea** hasta completar la importación. No hay polling ni Celery en la API.

### Push (Wagtail → Shopify) — HTTP 200

```json
{
  "success": true,
  "message": "Product synced to Shopify successfully.",
  "shopify_id": "gid://shopify/Product/12345678"
}
```

---

## Workflows

### Productos (catálogo existente en Shopify)

```bash
# 1. Importar
curl -X POST -H "Authorization: Bearer $API_KEY" "$BASE/products/pull"

# 2. Listar
curl -H "Authorization: Bearer $API_KEY" "$BASE/products/?locale=en-US&limit=10"

# 3. Actualizar y publicar
curl -X PATCH -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"seo_title":"New SEO Title","publish":true}' \
  "$BASE/products/42"

# 4. Verificar sync
curl -H "Authorization: Bearer $API_KEY" "$BASE/products/42"
# Comprobar last_synced_at no es null
```

### Artículos (requiere blog padre)

1. `POST /blogs/pull` — importa blogs y artículos.
2. `GET /blogs/` — obtener `id` del blog padre.
3. `POST /articles/` con `"blog_id": <id>`.
4. `PATCH /articles/{id}` con `"publish": true`.

El blog padre debe tener `shopify_id` antes de que los artículos se sincronicen.

### Locations (solo Wagtail → Shopify)

Locations **no tienen pull**. El contenido se crea en Wagtail y se empuja a metaobject Shopify `local_page`.

```bash
# 1. Crear
curl -X POST -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Austin Store",
    "city": "Austin",
    "state": "TX",
    "country": "United States",
    "intro": "<p>Welcome to our Austin location.</p>"
  }' \
  "$BASE/locations/"

# 2. Publicar (opcional)
curl -X PATCH -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"publish": true}' \
  "$BASE/locations/7"

# 3. Push a Shopify
curl -X POST -H "Authorization: Bearer $API_KEY" "$BASE/locations/7/push"

# 4. Verificar shopify_id y last_synced_at
curl -H "Authorization: Bearer $API_KEY" "$BASE/locations/7"
```

Campos rich text (`intro`, `content_2`, etc.) se envían y reciben como **HTML string**.

### Home (solo Wagtail → Shopify)

Home pages **no tienen pull**. Un metaobject `home_page` por locale (`home-en-us`, …). El hero va en campos top-level; las 13 secciones se editan por campos tipados (recomendado) o `sections_json` parcial. El servidor siempre normaliza a `{version: 1, sections: [13 types]}`.

```bash
# 1. Crear (esqueleto de 13 secciones automático)
curl -X POST -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"hero_heading": "Adult Toys for Every Body", "locale": "en-US"}' \
  "$BASE/home/"

# 2. PATCH de una sección (merge por type; no borra el resto)
curl -X PATCH -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "editorial_intro": {
      "heading": "Pleasure, made clear",
      "body": "<p>Guides and body-safe picks.</p>"
    },
    "publish": true
  }' \
  "$BASE/home/42"

# 3. Push a Shopify
curl -X POST -H "Authorization: Bearer $API_KEY" "$BASE/home/42/push"

# 4. Verificar sections_json (siempre 13 types), shopify_id, last_synced_at
curl -H "Authorization: Bearer $API_KEY" "$BASE/home/42"
```

Campos de sección de primer nivel: `promo_gateway`, `nav_collection_pills`, `trust_bar`, `featured_collections`, `editorial_intro`, `best_sellers`, `shop_by_need`, `educational_hub`, `brand_values`, `market_block`, `faq`, `internal_links`, `seo_schema`. Referencias usan `page_id` (Wagtail FK).

#### Rellenar contenido por locale (agentes)

No hay auto-copia `en-US` → otros locales. Cada `HomePage` (`home-en-us`, `home-es-us`, `home-en-ca`, `home-fr-ca`) se edita aparte. El servidor solo garantiza el sobre canónico de 13 tipos.

| Locale | Source of truth | `market_block.market_code` | Copy |
|--------|-----------------|----------------------------|------|
| `en-US` | Baseline editorial (seed / live) | `US` | Inglés US |
| `es-US` | Adaptar desde `en-US` | `US` | Español US |
| `en-CA` | Adaptar desde `en-US` | `CA` | Inglés Canadá |
| `fr-CA` | Adaptar desde `en-CA` (o `en-US` + market CA) | `CA` | Francés Canadá |

**Refs**

- `CollectionPage` / `ProductPage`: mismos `page_id` en todos los locales (catálogo compartido).
- `ArticlePage`: solo si existe en el mismo locale Wagtail del Home; si no hay traducción, omitir el ítem (p. ej. grupo Guides).
- `GlossaryTermPage`: remapear por `locale_code` (`en-US`/`en-CA` → `en`, `es-US` → `es`, `fr-CA` → `fr`).

**Workflow**

1. `GET /home/` → mapear `locale` → `id`.
2. `GET /home/{en_us_id}` → baseline (hero + `sections_json`).
3. Resolver collections por handle; articles/glossary del locale destino.
4. `PATCH /home/{id}` por lotes (merge tipado; omitidos se conservan):
   - Lote A (refs): `promo_gateway`, `nav_collection_pills`, `featured_collections`, `best_sellers`, `shop_by_need`
   - Lote B (copy): `trust_bar`, `editorial_intro`, `brand_values`, `market_block`, `faq`
   - Lote C (discovery + SEO): `educational_hub`, `internal_links`, `seo_schema` + hero/`seo_title`/`search_description`
5. `publish: true` en el PATCH y/o `POST /home/{id}/push`.
6. Verificar: `GET` con 13 types; listas con ≥1 ítem donde el diseño lo espera; `market_code` correcto; `shopify_id` / `last_synced_at` actualizados.

Criterio “locale completo”: hero (`hero_eyebrow`, heading, CTAs, SEO) + las 13 secciones con copy no vacío en headings y listas mínimas (promo cards, trust, FAQ, nav pills, etc.). Refs sin equivalente de locale se omiten a propósito.

### Glossary (Wagtail ↔ Shopify)

El contenido editorial (`term`, `definition`, SEO, links) se crea y edita en Wagtail y se empuja a metaobject Shopify `glossary_term`. Las **imágenes** se cargan en Shopify Admin; el pull inbound sincroniza solo campos de imagen en términos existentes y crea páginas nuevas si faltan en Wagtail.

La página listado `/pages/glossary` la gestiona el theme en Liquid (no hay endpoint para ella). Tras pull, Wagtail reconstruye `custom.index_listings` con `image_url` / `image_alt` por término.

#### Sincronizar imágenes desde Shopify

```bash
# Pull: metaobjects glossary_term → GlossaryTermPage (imagen en existentes; creación si falta)
curl -X POST -H "Authorization: Bearer $API_KEY" "$BASE/glossary/pull"
```

Comportamiento del pull:

| Caso | Acción |
|------|--------|
| Término nuevo en Wagtail (por `shopify_id`) | Crear `GlossaryTermPage` con campos básicos + imagen |
| Término existente | Solo `image_url`, `shopify_image_id`, `image_alt_text` — no toca `definition`, `term` ni SEO |

Tras import exitoso con cambios, se encola rebuild de `index_listings` automáticamente.

#### Crear y publicar desde Wagtail

```bash
# 1. Crear término
curl -X POST -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "term": "Vibrator",
    "locale_code": "en",
    "definition": "<p>A device that vibrates.</p>",
    "synonyms": ["Personal massager"],
    "same_as": ["https://en.wikipedia.org/wiki/Vibrator_(sex_toy)"],
    "related_links": [
      {"type": "product", "handle": "satisfyer-pro-2", "label": "Satisfyer Pro 2"}
    ]
  }' \
  "$BASE/glossary/"
```

`synonyms` y `same_as` son opcionales: omitir o enviar `[]` deja listas vacías (default). `same_as` son URLs externas schema.org (Wikipedia/Wikidata), distintas de `translation_of` (variantes Wagtail por locale).

`related_links` en POST/PATCH se persisten como **FKs tipadas manuales** (`is_auto=False` en `related_products` / `related_collections` / `related_articles` / `related_glossary_terms`). El JSONField `related_links` es **cache derivado** (se reescribe al aplicar el PATCH y en `refresh_semantic_links`). Tipos soportados: `product`, `collection`, `article`, `metaobject`. Un handle no resoluble en el mismo locale → `400`. `[]` borra solo los manuales; los auto (`is_auto=True`) los gestiona el enrich al publicar.

```bash
# Crear término mínimo (sin synonyms/same_as)
curl -X POST -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"term": "Libido", "locale_code": "en"}' \
  "$BASE/glossary/"

# 2. Publicar (opcional)
curl -X PATCH -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"publish": true}' \
  "$BASE/glossary/12"

# 3. Push a Shopify
curl -X POST -H "Authorization: Bearer $API_KEY" "$BASE/glossary/12/push"

# 4. Verificar shopify_id y last_synced_at
curl -H "Authorization: Bearer $API_KEY" "$BASE/glossary/12"
```

Filtrar por locale Shopify del metaobject: `GET /glossary/?locale_code=es` (distinto de `?locale=` que filtra Wagtail locale).
El listado es compacto por defecto (sin `definition`). Pasar `?full=true` para `GlossaryTermOut` completo, o usar `GET /glossary/{id}`.

### Preview semántico (related links)

`POST /semantic-links/suggest` (`suggest_related_pages`) es **solo lectura**: no escribe FK ni llama a `refresh_semantic_links`. El auto-link de publish sigue capado a 5 por tipo.

```bash
# Draft que aún no existe
curl -X POST -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "locale": "en-US",
    "page_type": "glossary",
    "title": "Chastity Belt",
    "definition": "<p>A locking device worn to restrict genital access.</p>",
    "types": ["collection"],
    "limit_per_type": 20
  }' \
  "$BASE/semantic-links/suggest"

# Página existente (el servidor extrae el texto)
curl -X POST -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"locale": "en-US", "page_id": 12, "limit_per_type": 20}' \
  "$BASE/semantic-links/suggest"
```

Requisitos: `WAGTAIL_AI_PGVECTOR=true`, `GEMINI_API_KEY`, `PageIndex` poblado (`index_pages_batch`). Sin índice: HTTP 503.

Cada candidato incluye `score` (similitud coseno, más alto = más cercano).

---

## Localización

| Código | Mercado |
|--------|---------|
| `en-US` | English (United States) — primary |
| `es-US` | Spanish (United States) |
| `en-CA` | English (Canada) |
| `fr-CA` | French (Canada) |

- Filtrar listados: `?locale=es-US`
- Crear variante: `"locale": "es-US", "translation_of": <page_id_en_us>`

---

## Campos de sync comunes

| Campo | Descripción |
|-------|-------------|
| `shopify_id` | GID Shopify del recurso vinculado |
| `sync_enabled` | Si true, publish dispara sync outbound |
| `last_synced_at` | UTC del último push exitoso; null = nunca sincronizado |
| `live` | true si la página está publicada en Wagtail |

---

## Errores frecuentes

| HTTP | Detalle típico | Acción del agente |
|------|----------------|-------------------|
| 400 | ShopConfig / token missing | Verificar instalación OAuth de la app |
| 400 | No shopify_id on push | Hacer pull primero o setear shopify_id |
| 404 | Page not found | Verificar page_id de GET list |
| 401 | Unauthorized | Verificar API key |

---

## Notas

- La API es **100% síncrona**. Wagtail admin y app embebida pueden seguir usando Celery en background.
- DELETE solo afecta Wagtail; Shopify no se modifica.
- Para Locations, `shopify_locale` es el locale empujado al metaobject (distinto de Wagtail `locale`).
- Para Glossary, `locale_code` (`en` / `es` / `fr`) es el locale empujado al metaobject (distinto de Wagtail `locale`).

---

## MCP (Model Context Protocol)

Expone la API como **tools MCP** vía Server-Sent Events (SSE) para clientes como Claude Desktop o Cursor.

### Requisitos

- Servidor **ASGI con Daphne** (no `runserver` WSGI). En dev con Shopify CLI:

  ```toml
  # shopify.web.toml
  dev = ".venv/bin/daphne -b 0.0.0.0 -p 8000 config.asgi:application"
  ```

- **Fork de django-ninja** (requerido por `django-ninja-mcp` para `@event_source`). Ver `requirements.txt`.
- Paquete **alpha** (`django-ninja-mcp==0.0.1a2`) — API inestable.

### Endpoint

| Recurso | URL |
|---------|-----|
| Conexión SSE | `GET /api/v1/mcp` |
| Mensajes JSON-RPC | `POST /api/v1/{session_uuid}` |

Las tools MCP corresponden a los `operation_id` del OpenAPI (~36 operaciones).

### Autenticación MCP

1. **Conexión SSE:** header `Authorization: Bearer <api_key>` o `Authorization: Bearer <oauth_access_token>`.
2. **Tool calls internos:** el servidor reenvía ese header a las llamadas HTTP internas.
3. **Fallback opcional:** variable de entorno `MCP_DEFAULT_API_KEY` si el cliente MCP no envía headers.
4. **OAuth:** los access tokens deben incluir el scope `mcp` (configurable con `MCP_OAUTH_REQUIRED_SCOPES`).

```bash
export MCP_DEFAULT_API_KEY="tu-key"  # opcional, solo para tool calls sin header SSE
```

### Configuración cliente MCP

```json
{
  "mcpServers": {
    "wagtail-shopify": {
      "url": "https://wagtail-dev.aadigitalbusiness.com/api/v1/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY_OR_OAUTH_ACCESS_TOKEN"
      }
    }
  }
}
```

### Verificación manual

1. Arrancar con Daphne y crear API key o aplicación OAuth en `/admin-django/`.
2. Conectar cliente MCP a `/api/v1/mcp` con header Bearer.
3. `list_tools` → debe listar tools como `list_products`, `pull_blogs_sync`, etc.
4. `call_tool("list_products", {})` → JSON de productos, no 401.

Alternativa sin MCP: usar `GET /capabilities/` o `/openapi.json` directamente.

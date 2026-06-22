# Wagtail-Shopify Content API — Agent Guide

API autodescriptiva para agentes AI que gestionan contenido entre Wagtail CMS y Shopify.
Todas las operaciones de la API son **síncronas**: la respuesta HTTP contiene el resultado final.

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

- OpenAPI JSON: `/api/v1/openapi.json`
- **Catálogo de capacidades (agentes):** `GET /api/v1/capabilities/`
- Swagger UI: `/api/v1/docs/`

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
| Glossary | `GET /glossary/` | `GET /glossary/{id}` | `POST /glossary/` | `PATCH /glossary/{id}` | `DELETE /glossary/{id}` | — | `POST /glossary/{id}/push` |

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

### Glossary (solo Wagtail → Shopify)

Los términos del glosario **no tienen pull**. El contenido se crea en Wagtail y se empuja a metaobject Shopify `glossary_term`.
La página listado `/pages/glossary` la gestiona el theme en Liquid (no hay endpoint para ella).

```bash
# 1. Crear término
curl -X POST -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "term": "Vibrator",
    "locale_code": "en",
    "definition": "<p>A device that vibrates.</p>",
    "related_links": [
      {"type": "product", "handle": "satisfyer-pro-2", "label": "Satisfyer Pro 2"}
    ]
  }' \
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

# BigQuery GSC Analytics API — Agent Guide

API autodescriptiva para agentes AI que consultan datos de Google Search Console vía BigQuery.
Los reportes pueden leer **snapshots cacheados** (PostgreSQL) o consultar **BigQuery en vivo**.

> **Mantener actualizada:** cualquier cambio en `/api/gsc/` debe reflejarse en la documentación en el mismo cambio.
> Política y checklist: [`.cursor/rules/api-documentation.mdc`](../.cursor/rules/api-documentation.mdc).
> Fuente única de verdad de capacidades: `services/bigquery_gsc/bigquery_gsc/api/agent_registry.py`.

## Quick start

### 1. Credencial (mismo esquema que `/api/v1/`)

La API GSC comparte autenticación con la API de contenido cuando está montada en cms-shop:

1. Abre **Django Admin** en `/admin-django/`
2. Ve a **API → API Keys → Add**
3. Guarda y copia la key generada

### 2. Primera request

```bash
export API_KEY="tu-key-aqui"
export BASE="https://wagtail-dev.aadigitalbusiness.com/api/gsc"

curl -s -H "Authorization: Bearer $API_KEY" "$BASE/health"
curl -s -H "Authorization: Bearer $API_KEY" "$BASE/reports/declining-urls?market=CA&period=28d&source=cached"
```

### 3. Documentación interactiva

- OpenAPI JSON: `/api/gsc/openapi.json`
- **Catálogo de capacidades (agentes):** `GET /api/gsc/capabilities/`
- Swagger UI: `/api/gsc/docs/`

Usa los `operation_id` del OpenAPI como nombres estables de herramientas (p.ej. `list_gsc_declining_urls`).

---

## Catálogo de capacidades

**Entry point recomendado para agentes:** `GET /api/gsc/capabilities/`

```bash
curl -s -H "Authorization: Bearer $API_KEY" "$BASE/capabilities/" | jq '.tools | length'
curl -s -H "Authorization: Bearer $API_KEY" "$BASE/capabilities/" | jq '.workflows.seo_audit_cached'
```

### Tipos de capacidad (`capability_type`)

| Valor | Significado |
|-------|-------------|
| `discover` | Health, datasets, inventario de snapshots, catálogo |
| `read` | Reportes de tráfico (URLs, queries, device, country) |
| `analyze` | Reportes SEO (oportunidades, declining URLs, cannibalization) |

### Extensiones OpenAPI (`x-agent-*`)

| Campo | Descripción |
|-------|-------------|
| `x-agent-capability-type` | Tipo de capacidad (ver tabla anterior) |
| `x-agent-resource` | Recurso: `gsc_traffic`, `gsc_reports`, etc. |
| `x-agent-prerequisites` | Condiciones previas (snapshots, credenciales GCP) |
| `x-agent-next-tools` | `operation_id` sugeridos tras éxito |

---

## Autenticación

| Header | Valor |
|--------|-------|
| `Authorization` | `Bearer <api_key>` o `Bearer <oauth_access_token>` |

| Respuesta | Causa |
|-----------|-------|
| 401 | Sin header o token inválido (solo en host cms-shop con app `api`) |

---

## Parámetros comunes

| Parámetro | Valores | Descripción |
|-----------|---------|-------------|
| `market` | `CA`, `US` | Mercado configurado en `BIGQUERY_GSC.GSC_DATASETS` |
| `period` | `28d`, `90d` | Ventana rolling con lag de exportación (`LAG_DAYS`, default 3) |
| `source` | `auto`, `cached`, `live` | Origen de datos (ver tabla siguiente) |
| `limit` | 1–500 | Máximo de filas en `data` |
| `dataset_key` | `ca`, `us` | Opcional; filtra dataset BigQuery |

### Modos `source`

| Valor | Comportamiento |
|-------|----------------|
| `auto` | Cache si hay snapshots; si no, BigQuery live |
| `cached` | Solo `GscSnapshot` en PostgreSQL (rápido) |
| `live` | Consulta BigQuery directa |

Importar snapshots:

```bash
python manage.py import_gsc_snapshots --days 28 --lag-days 3
```

---

## Matriz de herramientas

| Grupo | Endpoint | `operation_id` |
|-------|----------|------------------|
| Health | `GET /health` | `gsc_health` |
| Datasets | `GET /datasets` | `list_gsc_datasets` |
| Snapshots | `GET /snapshots/status` | `gsc_snapshots_status` |
| Traffic | `GET /traffic/urls` | `list_gsc_url_traffic` |
| Traffic | `GET /traffic/queries` | `list_gsc_query_traffic` |
| Traffic | `GET /traffic/country-device` | `list_gsc_country_device_traffic` |
| Traffic | `GET /traffic/device` | `list_gsc_device_traffic` |
| Reports | `GET /reports/collection-opportunities` | `list_gsc_collection_opportunities` |
| Reports | `GET /reports/striking-distance` | `list_gsc_striking_distance` |
| Reports | `GET /reports/declining-urls` | `list_gsc_declining_urls` |
| Reports | `GET /reports/query-comparison` | `list_gsc_query_comparison` |
| Reports | `GET /reports/product-opportunities` | `list_gsc_product_opportunities` |
| Reports | `GET /reports/page-opportunities` | `list_gsc_page_opportunities` |
| Reports | `GET /reports/low-ctr-pages` | `list_gsc_low_ctr_pages` |
| Reports | `GET /reports/cannibalization-risk` | `list_gsc_cannibalization_risk` |

---

## Formato de respuesta

Todos los endpoints de tráfico y reportes devuelven:

```json
{
  "meta": {
    "market": "CA",
    "period": "28d",
    "source": "cached",
    "count": 25
  },
  "data": [
    {
      "url": "https://playlovetoys.ca/collections/example",
      "cur_clicks": 0,
      "prev_clicks": 1,
      "clicks_delta_pct": -1
    }
  ]
}
```

---

## Workflows

### Auditoría SEO (cached)

```bash
curl -s -H "Authorization: Bearer $API_KEY" "$BASE/snapshots/status"
curl -s -H "Authorization: Bearer $API_KEY" "$BASE/reports/declining-urls?market=CA&source=cached"
curl -s -H "Authorization: Bearer $API_KEY" "$BASE/reports/low-ctr-pages?market=CA&source=cached"
curl -s -H "Authorization: Bearer $API_KEY" "$BASE/reports/cannibalization-risk?market=CA&source=cached"
```

### Oportunidades SEO

```bash
curl -s -H "Authorization: Bearer $API_KEY" "$BASE/datasets"
curl -s -H "Authorization: Bearer $API_KEY" "$BASE/reports/collection-opportunities?market=CA"
curl -s -H "Authorization: Bearer $API_KEY" "$BASE/reports/striking-distance?market=CA"
curl -s -H "Authorization: Bearer $API_KEY" "$BASE/reports/product-opportunities?market=CA"
```

### Comparación cross-market

```bash
curl -s -H "Authorization: Bearer $API_KEY" "$BASE/reports/query-comparison?period=28d"
curl -s -H "Authorization: Bearer $API_KEY" "$BASE/traffic/queries?market=CA"
```

---

## Configuración

Variables en `backend/.env`:

| Variable | Descripción |
|----------|-------------|
| `BIGQUERY_PROJECT_ID` | Proyecto GCP |
| `GOOGLE_APPLICATION_CREDENTIALS` | Ruta al JSON de service account |
| `BIGQUERY_LOCATION` | Región BigQuery (default `US`) |

Bloque Django `BIGQUERY_GSC` en `backend/config/settings.py` — datasets CA/US, umbrales de scoring, `LAG_DAYS`.

Credenciales: `backend/secrets/` (gitignored).

---

## Errores frecuentes

| Status | Causa |
|--------|-------|
| 401 | Token ausente o inválido |
| 422 | Parámetro requerido faltante (p.ej. `market`) |
| 500 | Error BigQuery, credenciales GCP, o export GSC desactualizado |

Verificar salud de exports: `GET /health`

---

## Relación con `/api/v1/`

| API | Base path | Propósito |
|-----|-----------|-----------|
| Content API | `/api/v1/` | CRUD y sync Wagtail ↔ Shopify |
| GSC API | `/api/gsc/` | Analytics SEO desde BigQuery |

Misma autenticación, procesos Django compartidos, paquete fuente en `services/bigquery_gsc/`.

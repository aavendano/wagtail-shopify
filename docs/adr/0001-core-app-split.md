# ADR 0001: Split de `core` en `shopify_admin`, `shopify_config` y `core` ops

## Status

Accepted (rama `refactor/shopify-core-split`; no merge a `production` sin human gate).

## Context

La app `core` mezclaba UI embebida de Shopify Admin, `ShopConfig`/tokens (hub de todo el backend) y bootstrap Django (`ensure_superuser`). El nombre ya no reflejaba el dominio del producto (CMS headless + múltiples superficies).

## Decision

| App | Responsabilidad |
|-----|-----------------|
| `shopify_admin` | UI embebida; rutas bajo `/shopify-admin/` |
| `shopify_config` | `ShopConfig`, lookup, tokens, helpers SDK |
| `core` | Solo plataforma Django (`ensure_superuser`) |

Reglas de dependencia: las capas solo importan hacia abajo; nadie de dominio importa `shopify_admin`; `shopify_config` no importa UI ni content; `core` no participa en el grafo Shopify.

`ShopConfig` conserva `db_table = "core_shopconfig"` para no renombrar la tabla física.

## Consequences

- Claridad de ownership y PRs acotados.
- Migración de app label y unificación de URLs requieren redirects y checklist Partners.
- Human gate antes de merge a `production` o migrate en Postgres de prod.

## Partners checklist (human)

Antes de cutover en Partners Dashboard, verificar y actualizar si aplica:

1. **App URL** — preferir `https://<host>/shopify-admin/` (aliases legacy: `/app/`, redirects `/core/…`).
2. **Allowed redirection URL(s)** — que no apunten solo a `/core/auth/…` o `/core/install`.
3. Tras cambio de URLs, smoke install/login embebido en staging (no prod sin gate).

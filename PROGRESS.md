# Progreso del proyecto

## Plan activo

- **Archivo:** [`theme-root-page-verification.plan.md`](.cursor/plans/theme-root-page-verification.plan.md)
- **Última fase completada:** implementación del cambio de arquitectura (`root_page` metaobject unificado, commit `a07f224` en este repo, `3416eb0` en `plt-frontend`) — verificado solo de forma estática, sin Django ni Shopify CLI disponibles (2026-07-06)
- **Siguiente:** Fase 1 — ejecutar el "Prompt de implementación" del plan activo en una sesión de `plt-frontend` con `shopify theme dev` real, contra una tienda de prueba con el backend desplegado

## Planes relacionados (no activos)

| Archivo | Estado | Notas |
|---------|--------|-------|
| [`root-export-config-admin.plan.md`](.cursor/plans/root-export-config-admin.plan.md) | Estratégico, pendiente | UI tipada + pickers Shopify sobre `export_config` |
| [`theme-index-pages.plan.md`](.cursor/plans/theme-index-pages.plan.md) | Superseded | Implementación Liquid original basada en Pages nativas |
| [`wagtail-root-index-section.plan.md`](.cursor/plans/wagtail-root-index-section.plan.md) | Superseded | Diseño SEO original basado en Pages nativas |

## Historial reciente

| Fecha | Plan | Fase | Notas |
|-------|------|------|-------|
| 2026-07-05 | root-export-platform | 1 | Migración 0021 aplicada; rollout glosario verificado (`rebuild_glossary_index --dry-run`) |
| 2026-07-05 | root-export-platform | 2 | Paquete `export_config/` + registry; glossary refactorizado |
| 2026-07-05 | root-export-platform | 3 | `location_index` builder/sync/signals/comando + tests |
| 2026-07-05 | root-export-platform | 4 | `theme_config` Product/Collection + migración 0022 + sync metafields |
| 2026-07-05 | root-export-platform | 5 | Docs plataforma export_config; `make test` 170 passed |
| 2026-07-05 | glossary-index-sync | 1–3 | v1 base (root_page, glossary index, tests) |
| 2026-07-05 | root-export-config-admin | — | Plan estratégico UI export_config |
| 2026-07-06 | theme-root-page-verification | 0 | Migración a `root_page` metaobject unificado (elimina dualidad Page/metaobject); backend + theme implementados y commiteados, pendiente verificación real end-to-end |

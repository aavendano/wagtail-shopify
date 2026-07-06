# Progreso del proyecto

## Plan activo

- **Archivo:** [`.cursor/plans/theme-index-pages.plan.md`](.cursor/plans/theme-index-pages.plan.md) (copia en `active.plan.md`)
- **Última fase completada:** theme-index-pages Fase 3 — índices glosario y locations vía `wagtail-root-index` (2026-07-05)
- **Siguiente:** Fase 4 — plantilla detalle metaobject `glossary_term`

## Convención de planes (2026-07-06)

Planes actualizados a modelo **agnóstico de tienda**: sin dominios ni GIDs de una instalación concreta. Handles canónicos y contratos JSON son estables; GIDs viven en `export_config` por instalación.

**Si hay 404 en índices CMS** (`/pages/glossary-en`, etc.): suele ser `export_config` con GIDs de otra tienda. Re-bootstrap en la tienda conectada:

```bash
python manage.py ensure_page_metafield_definitions
python manage.py bootstrap_index_pages --apply-export-config
python manage.py rebuild_glossary_index
python manage.py rebuild_location_index
```

Ver troubleshooting en [`theme-index-pages.plan.md`](.cursor/plans/theme-index-pages.plan.md).

## Planes relacionados (no activos)

| Archivo | Estado | Notas |
|---------|--------|-------|
| [`root-export-config-admin.plan.md`](.cursor/plans/root-export-config-admin.plan.md) | Estratégico, pendiente | UI tipada + pickers Shopify sobre `export_config` |
| [`wagtail-root-index-section.plan.md`](.cursor/plans/wagtail-root-index-section.plan.md) | Completado | Section unificada + SEO hreflang vía metafields |

## Historial reciente

| Fecha | Plan | Fase | Notas |
|-------|------|------|-------|
| 2026-07-06 | planes-genéricos-tienda | — | Convención agnóstica de tienda en plans/README, plans-convention, theme-index-pages |
| 2026-07-05 | root-export-platform | 1 | Migración 0021 aplicada; rollout glosario verificado (`rebuild_glossary_index --dry-run`) |
| 2026-07-05 | root-export-platform | 2 | Paquete `export_config/` + registry; glossary refactorizado |
| 2026-07-05 | root-export-platform | 3 | `location_index` builder/sync/signals/comando + tests |
| 2026-07-05 | root-export-platform | 4 | `theme_config` Product/Collection + migración 0022 + sync metafields |
| 2026-07-05 | root-export-platform | 5 | Docs plataforma export_config; `make test` 170 passed |
| 2026-07-05 | glossary-index-sync | 1–3 | v1 base (root_page, glossary index, tests) |
| 2026-07-05 | root-export-config-admin | — | Plan estratégico UI export_config |

# Progreso del proyecto

## Plan activo

- **Archivo:** ninguno (último plan de implementación completado: `root-export-platform`)
- **Última fase completada:** root-export-platform Fase 5 — docs, `make test` 170 passed (2026-07-05)
- **Siguiente:** Operación manual en Shopify Admin (metafields PAGE + GIDs en `export_config` de roots glossary/local-us) o activar `root-export-config-admin`

## Planes relacionados (no activos)

| Archivo | Estado | Notas |
|---------|--------|-------|
| [`root-export-config-admin.plan.md`](.cursor/plans/root-export-config-admin.plan.md) | Estratégico, pendiente | UI tipada + pickers Shopify sobre `export_config` |

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

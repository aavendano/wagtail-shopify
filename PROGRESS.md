# Progreso del proyecto

## Plan activo

- **Archivo:** [`plan.md`](plan.md) (Puck CMS Headless)
- **Última fase completada:** Fases 0–4 — SPA `/cms/`, auth sesión, CRUD recursos, preview HTML, restricción Wagtail Admin + docs (2026-09-03)
- **Siguiente:** QA manual en tienda conectada (`ensure_cms_spa`, build frontend, smoke `/cms/#/glossary`)

## Convención de planes (2026-07-06)

Planes actualizados a modelo **agnóstico de tienda**: sin dominios ni GIDs de una instalación concreta. Handles canónicos y contratos JSON son estables; GIDs viven en `export_config` por instalación.

**Arquitectura de índices (canónica):** una sola Shopify Page por tipo — handles `glossary`, `locations`, `blogs` — con metafield `custom.index_listings` (envelope multi-locale). **No** usar handles legacy `glossary-en` / `locations-en-us` en docs nuevas.

**Si hay 404 en índices CMS** (`/pages/glossary`, `/pages/locations`, `/pages/blogs`): suele ser `export_config` con GIDs de otra tienda. Re-bootstrap en la tienda conectada:

```bash
python manage.py ensure_page_metafield_definitions
python manage.py bootstrap_index_pages --apply-export-config
python manage.py rebuild_glossary_index
python manage.py rebuild_location_index
python manage.py rebuild_blog_index
```

Ver troubleshooting en [`theme-index-pages.plan.md`](.cursor/plans/theme-index-pages.plan.md) y [`docs/shopify_content.md`](docs/shopify_content.md).

## Planes relacionados (no activos)

| Archivo | Estado | Notas |
|---------|--------|-------|
| [`theme-index-pages.plan.md`](.cursor/plans/theme-index-pages.plan.md) | Pausado (QA theme pendiente) | Fase 7 Lighthouse/docs theme |
| [`root-export-config-admin.plan.md`](.cursor/plans/root-export-config-admin.plan.md) | Estratégico, pendiente | UI tipada + pickers Shopify sobre `export_config` |
| [`wagtail-root-index-section.plan.md`](.cursor/plans/wagtail-root-index-section.plan.md) | Completado | Section unificada + SEO hreflang vía metafields |

## Historial reciente

| Fecha | Plan | Fase | Notas |
|-------|------|------|-------|
| 2026-09-03 | puck-cms-headless | 0–4 | `django_react_ui_editor` + `/cms/` SPA, session auth, preview endpoints, docs roles |
| 2026-07-11 | theme-index-pages | 4–5 | Detalle glossary/local: synonyms, DefinedTerm, related_links fallback, LocalBusiness; FAQs CMS en PDP/PLP; batch 65 ciudades COMPLETED; home gates A/B closed |
| 2026-07-06 | planes-genéricos-tienda | — | Convención agnóstica de tienda en plans/README, plans-convention, theme-index-pages |
| 2026-07-05 | root-export-platform | 1–5 | export_config platform + tests |
| 2026-07-05 | glossary-index-sync | 1–3 | v1 base (root_page, glossary index, tests) |

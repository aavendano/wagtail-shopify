# Progreso del proyecto

## Plan activo

- **Archivo:** [`plan.md`](plan.md) (Puck CMS Headless)
- **Última fase completada:** content-store Phase E+F cerradas en `settings_dev` + `git_authoritative` (2026-09-05)
- **Siguiente:** materialize/flip en prod **solo tras** `ShopConfig` + import + PR de `content/`; y/o theme-index-pages Fase 7

### Content-store E → F → git_authoritative (dev, 2026-09-05)

| Paso | Resultado |
|------|-----------|
| pytest location + article markdown (+ blog/glossary/git) | 79 passed (`settings_test` aisla `CONTENT_STORE_*`) |
| `materialize_editorial_content` | location pk=3 campos espejo + blog description |
| `materialize_article_markdown` | article pk=5 `body.md` (creado mínimo en SQLite) |
| `.env.dev` flip | `CONTENT_STORE_MODE=git_authoritative`, `GIT_FALLBACK_TO_DB=false` |
| Smoke editorial | `page.editorial.*` desde archivo; edit `.md` sin DB; missing → `ContentNotFound`; forms read-only |

**Prod** (`:8082` / `.env`) sigue en `db`/`mirror` hasta checklist de rollout del contrato F. No flip ahí.

### Resultado QA smoke (2026-09-05)

| Paso | Resultado |
|------|-----------|
| `npm run build` (`cms_ui/frontend`) | OK → `cms_ui/static/cms_ui/` + collectstatic |
| `ensure_cms_spa` | OK — `CmsSpaMount` + grupo `cms_editors` |
| `/cms/` anon | 302 → `/admin-django/login/?next=/cms/` |
| `/cms/` staff (`admin`) | 200 — `cms-spa-root`, `__CMS_BOOTSTRAP__`, resources glossary…locations |
| static `spa-public.js` | 200 |
| API list glossary/products/collections/blogs/articles/locations | 200 (catálogo vacío al inicio; sin `ShopConfig`) |
| glossary detail + preview | detail 200; preview **bloqueado** por `Invalid filter: richtext` → fix `{% load wagtailcore_tags %}` en `glossary_term_page.html` → preview **200** |
| Enlace `/cms/` desde `shopify-admin` / root menu | Presente en templates |

Notas: Postgres sin tienda OAuth ni páginas importadas; se creó `ShopifyRootPage` + término `qa-smoke-term` solo para ejercitar preview. Daphne `:8082` reiniciado vía proceso local (sin `sudo systemctl`).

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
| 2026-09-05 | content-store E/F | cerrar + git_auth | pytest OK; materialize location/article en SQLite; `.env.dev` `git_authoritative`; smoke editorial/fail-missing; prod sin flip |
| 2026-09-05 | puck-cms-headless | QA smoke | build SPA, ensure_cms_spa, shell/API OK; fix preview glossary `wagtailcore_tags`; DB sin ShopConfig/import |
| 2026-09-03 | puck-cms-headless | 0–4 | `django_react_ui_editor` + `/cms/` SPA, session auth, preview endpoints, docs roles |
| 2026-07-11 | theme-index-pages | 4–5 | Detalle glossary/local: synonyms, DefinedTerm, related_links fallback, LocalBusiness; FAQs CMS en PDP/PLP; batch 65 ciudades COMPLETED; home gates A/B closed |
| 2026-07-06 | planes-genéricos-tienda | — | Convención agnóstica de tienda en plans/README, plans-convention, theme-index-pages |
| 2026-07-05 | root-export-platform | 1–5 | export_config platform + tests |
| 2026-07-05 | glossary-index-sync | 1–3 | v1 base (root_page, glossary index, tests) |

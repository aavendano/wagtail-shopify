---
name: theme-root-page-verification
overview: Verificar end-to-end en shopify theme dev la migración de índices CMS a entradas del metaobjeto root_page (glosario/locations), después de eliminar la dualidad con Pages nativas.
active: true
created: 2026-07-06
---

# Verificación theme — root_page metaobject (glosario/locations)

Plan completo: [`theme-root-page-verification.plan.md`](theme-root-page-verification.plan.md)

## Fases

- [ ] Fase 1 — Setup backend (`ensure_metaobject_definitions`, confirmar `onlineStore` + campos nuevos)
- [ ] Fase 2 — Poblar entradas reales (publicar contenido o `rebuild_*_index`)
- [ ] Fase 3 — Confirmar URL de storefront en Admin
- [ ] Fase 4 — `shopify theme dev`: listado, layout, buscador, selector de idioma
- [ ] Fase 5 — Verificar `<head>` (hreflang/noindex) y confirmar `template.name` real en contexto metaobject
- [ ] Fase 6 — Navbar/breadcrumb activos + regresión `glossary_term`/`local_page`
- [ ] Fase 7 — `shopify theme check` + reporte pass/fail
- [ ] Fase 8 — Limpieza final (si todo OK) o prompt(s) de cambio de backend (si no)

## Estado

Backend (`a07f224`) y theme (`3416eb0`) implementados y commiteados en
`claude/wagtail-root-page-integration-05i6m1`. Pendiente verificación real en un
entorno con Shopify CLI — este repo (wagtail-shopify) no puede ejecutarla, el trabajo
continúa en `plt-frontend`.

## Prompt rápido

Copiar el bloque **"Prompt de implementación"** de
[`theme-root-page-verification.plan.md`](theme-root-page-verification.plan.md) a la
sesión/agente que trabaje en `plt-frontend` con acceso a `shopify theme dev`.

---
name: theme-index-pages
overview: Implementar plantillas Liquid del theme Shopify para consumir índices precomputados (index_listings) y páginas de detalle de metaobjects.
active: true
created: 2026-07-05
---

# Theme — índices A–Z y páginas CMS (Liquid)

Plan completo: [`theme-index-pages.plan.md`](theme-index-pages.plan.md)

## Fases

- [x] Fase 1 — Snippet compartido parseo JSON de índice (`cms-index-listings-parse` / legacy parse)
- [x] Fase 2 — Índice glosario (`page.glossary.json` + `wagtail-root-index`) — Page única `glossary` + `custom.index_listings`
- [x] Fase 3 — Índice locations (`page.locations.json` + `wagtail-root-index`) — Page única `locations`
- [x] Fase 4 — Plantilla detalle `glossary_term` (H1, definition, image, synonyms, native related + `related_links` fallback, JSON-LD `DefinedTerm`)
- [x] Fase 5 — Plantilla detalle `local_page` (secciones + FAQs + JSON-LD `LocalBusiness`)
- [x] Fase 6 — Navegación global, SEO e i18n (nav CMS + hreflang índices vía `index_alternates`; verificado en smoke 2026-07-11)
- [ ] Fase 7 — QA formal (Theme check / Lighthouse) y documentación theme restante

## Modelo de despliegue

**No es multi-tenant.** Una instalación Wagtail = una tienda Shopify (`ShopConfig`). El dominio de la tienda activa vive en configuración (`.env`, OAuth, `.shopify/project.json` o flag CLI) — **no en este plan**.

Los GIDs en `export_config` son exclusivos de esa instalación; nunca copiar entre merchants.

Al instalar en una tienda nueva, seguir el checklist **Onboarding nueva tienda** en [`theme-index-pages.plan.md`](theme-index-pages.plan.md) (bootstrap + rebuild en la tienda conectada).

## Estado

Backend listo. **Índices (1–3) y detalle metaobject (4–5) completados** en el theme. Nav + hreflang de índices (6) en producción. Pendiente: Fase 7 QA formal.

## Prompt rápido

Copiar el bloque **"Prompt de implementación"** de [`theme-index-pages.plan.md`](theme-index-pages.plan.md) al agente o dev del theme.

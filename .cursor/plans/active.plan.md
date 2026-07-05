---
name: theme-index-pages
overview: Implementar plantillas Liquid del theme Shopify para consumir índices precomputados (glossary_index, location_index) y páginas de detalle de metaobjects.
active: true
created: 2026-07-05
---

# Theme — índices A–Z y páginas CMS (Liquid)

Plan completo: [`theme-index-pages.plan.md`](theme-index-pages.plan.md)

## Fases

- [ ] Fase 1 — Snippet compartido parseo JSON de índice
- [ ] Fase 2 — Plantilla índice glosario (`page.glossary-index.liquid`)
- [ ] Fase 3 — Plantilla índice locations (`page.location-index.liquid`)
- [ ] Fase 4 — Plantilla detalle `glossary_term`
- [ ] Fase 5 — Plantilla detalle `local_page`
- [ ] Fase 6 — Navegación, SEO e i18n
- [ ] Fase 7 — QA y documentación theme

## Estado

Backend listo (`rebuild_glossary_index` y `rebuild_location_index` con `pushed` OK). Implementación pendiente en **repo del theme Shopify**.

## Prompt rápido

Copiar el bloque **"Prompt de implementación"** de [`theme-index-pages.plan.md`](theme-index-pages.plan.md) al agente o dev del theme.

---
name: theme-index-pages
overview: Implementar plantillas Liquid del theme Shopify para consumir índices precomputados (glossary_index, location_index) y páginas de detalle de metaobjects.
active: true
created: 2026-07-05
---

# Theme — índices A–Z y páginas CMS (Liquid)

Plan completo: [`theme-index-pages.plan.md`](theme-index-pages.plan.md)

## Fases

- [x] Fase 1 — Snippet compartido parseo JSON de índice (`wagtail-root-index-parse`)
- [x] Fase 2 — Índice glosario (`page.glossary.json` + `wagtail-root-index`)
- [x] Fase 3 — Índice locations (`page.locations.json` + `wagtail-root-index`)
- [ ] Fase 4 — Plantilla detalle `glossary_term`
- [ ] Fase 5 — Plantilla detalle `local_page`
- [ ] Fase 6 — Navegación global, SEO e i18n (parcial: hreflang vía metafields hecho)
- [ ] Fase 7 — QA y documentación theme

## Modelo de despliegue

**No es multi-tenant.** Una instalación Wagtail = una tienda Shopify (`ShopConfig`). El dominio de la tienda activa vive en configuración (`.env`, OAuth, `.shopify/project.json` o flag CLI) — **no en este plan**.

Los GIDs en `export_config` son exclusivos de esa instalación; nunca copiar entre merchants.

Al instalar en una tienda nueva, seguir el checklist **Onboarding nueva tienda** en [`theme-index-pages.plan.md`](theme-index-pages.plan.md) (bootstrap + rebuild en la tienda conectada).

## Estado

Backend listo. **Índices (fases 1–3) completados** en theme vía `wagtail-root-index`. Pendiente: detalle metaobject (fases 4–5), nav global y QA (fases 6–7).

## Prompt rápido

Copiar el bloque **"Prompt de implementación"** de [`theme-index-pages.plan.md`](theme-index-pages.plan.md) al agente o dev del theme.

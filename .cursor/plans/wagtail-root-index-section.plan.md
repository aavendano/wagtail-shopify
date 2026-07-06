---
name: wagtail-root-index-section
overview: Section Liquid unificada wagtail-root-index para índices CMS. Head SEO (hreflang/noindex) lee Page metafields, no section settings.
active: true
created: 2026-07-05
supersedes: theme-index-pages (fases 2–3 como templates separados)
---

# Section `wagtail-root-index` — arquitectura SEO v1

## Restricción OS 2.0 (confirmada)

`layout/theme.liquid` renderiza `<head>` **antes** que las sections. Los `settings` y `blocks` de una section **no existen** en ese momento.

**Consecuencia:** `wagtail-root-index-head.liquid` no puede leer configuración del Theme Editor de la section. Hreflang y noindex configurables en v1 deben venir del objeto global **`page`** (y metafields de esa Page).

## Fuente de verdad v1 — Page metafields

| Metafield | Namespace | Tipo | Quién lo escribe | Consumido por |
|-----------|-----------|------|------------------|---------------|
| `glossary_locale` / `location_locale` | `custom` | text | Wagtail (`rebuild_*_index`) | head (gate) + section |
| `glossary_index` / `location_index` | `custom` | json | Wagtail | section (listado) |
| **`index_alternates`** | `custom` | json | Wagtail bootstrap/sync (`PageIndexConsumer.sync`) o Admin manual | **head + section** (switcher) |
| **`index_noindex`** | `custom` | boolean | Admin manual o Wagtail (`export_config`) | **head** |

### Gate en `theme.liquid`

```liquid
{% if page.metafields.custom.glossary_locale != blank
   or page.metafields.custom.location_locale != blank %}
  {% render 'wagtail-root-index-head' %}
{% endif %}
```

### Contrato `custom.index_alternates`

JSON en cada Page índice (misma fuente para `<head>` y switcher de idioma en la section):

```json
{
  "version": 1,
  "include_self": true,
  "x_default_handle": "glossary-en",
  "alternates": [
    { "hreflang": "en", "label": "English", "handle": "glossary-en" },
    { "hreflang": "es", "label": "Español", "handle": "glossary-es" },
    { "hreflang": "fr", "label": "Français", "handle": "glossary-fr" }
  ]
}
```

**Head snippet** resuelve URLs con el global Liquid `pages[handle].url` (no GIDs, no section settings):

```liquid
{% assign cfg = page.metafields.custom.index_alternates.value | parse_json %}
{% if cfg.alternates %}
  {% for alt in cfg.alternates %}
    {% assign alt_page = pages[alt.handle] %}
    {% if alt_page %}
      <link rel="alternate" hreflang="{{ alt.hreflang }}" href="{{ shop.url }}{{ alt_page.url }}">
    {% endif %}
  {% endfor %}
{% endif %}
{% if cfg.x_default_handle %}
  {% assign xd = pages[cfg.x_default_handle] %}
  {% if xd %}
    <link rel="alternate" hreflang="x-default" href="{{ shop.url }}{{ xd.url }}">
  {% endif %}
{% endif %}
```

### Contrato `custom.index_noindex`

- `true` → `<meta name="robots" content="noindex, follow">` (o `nofollow` si se añade `index_noindex_nofollow` en v1.1).
- `false` / ausente → no emitir meta robots (dejar al theme default).

Configurable por Page en **Shopify Admin → Custom data** sin tocar código.

## División de responsabilidades v1

| Concern | Fuente | Theme Editor |
|---------|--------|--------------|
| hreflang | `page.metafields.custom.index_alternates` | No (Admin metafields o Wagtail push) |
| noindex | `page.metafields.custom.index_noindex` | No |
| switcher idioma (UI) | **mismo** `index_alternates` | Section solo renderiza; no define alternates |
| búsqueda, layout, nav A–Z | section settings | Sí |
| listado items | `glossary_index` / `location_index` | No |

La section **relee** `index_alternates` para pintar tabs/links — una sola fuente. Los blocks `alternate_locale` / `noindex_locale` del schema **fueron eliminados** (no usar Theme Editor para hreflang).

## Fallback v1 (sin `index_alternates` poblado)

Si el metafield está vacío, `wagtail-root-index-head.liquid` usa mapa estático por `page.handle`. Los handles son **convención de bootstrap** ([`index_pages_bootstrap.py`](../../shopify_content/sync/index_pages_bootstrap.py)), válidos en cualquier tienda que haya ejecutado bootstrap — no están atados a un merchant concreto.

| `page.handle` | Hermanas |
|---------------|----------|
| `glossary-en` | `glossary-es`, `glossary-fr` |
| `glossary-es` | `glossary-en`, `glossary-fr` |
| `glossary-fr` | `glossary-en`, `glossary-es` |
| `locations-en-us` | `locations-es-us` |
| `locations-es-us` | `locations-en-us` |

Hreflang derivado de `glossary_locale` / `location_locale` de cada hermana. **No configurable** desde Theme Editor; suficiente para rollout inicial.

## Qué NO usar para head ni switcher

| Fuente | Motivo |
|--------|--------|
| Section settings/blocks (`alternate_locale`, `hreflang` en schema) | Inaccesibles en `theme.liquid`; eliminados del schema |
| Links hardcoded (`/pages/glossary-en`, etc.) | Drift con handles; duplica `index_alternates` |
| `shop.metaobjects.root_page.config` | Tiene GIDs, no URLs; Liquid no resuelve GID → URL |
| `seo.hreflang_*` por recurso | Patrón válido para **detalle** CMS, no índices A–Z |
| Duplicar config en section + metafield | Dos fuentes, drift seguro |
| Campos `seo` / `locales[]` en JSON de índice | Nunca se generan en backend |

## Backend — `index_alternates` / `index_noindex` (implementado)

`PageIndexConsumer.sync()` en [`export_config/base.py`](../../shopify_content/export_config/base.py) empuja `custom.index_alternates` derivado de `export_config.*.pages` + resolución de handles vía GraphQL. Opcional: `index_noindex` desde `export_config.<key>.noindex` / `noindex_locales`.

Definiciones en [`page_metafield_definitions.py`](../../shopify_content/sync/page_metafield_definitions.py) (`ensure_page_metafield_definitions`).

## Prompt de implementación (resumen)

Ver plan completo en conversación / iteraciones. Puntos clave SEO:

1. `wagtail-root-index-head.liquid` — solo `page` metafields + fallback handle map.
2. `wagtail-root-index.liquid` — UI; switcher lee `index_alternates`; settings solo para presentación.
3. Hook en `theme.liquid` gated por `glossary_locale` / `location_locale`.

## Criterios de aceptación SEO

- [x] hreflang en `<head>` sin depender de section settings.
- [x] Cambiar alternates en Admin metafield → head y switcher actualizan sin redeploy theme.
- [x] `index_noindex: true` en una Page índice → meta robots en head.
- [x] Fallback handle map funciona si `index_alternates` vacío (solo `<head>`, no switcher).
- [x] Tras bootstrap en tienda B, `index_alternates` se empuja con handles de B; el fallback solo aplica si el metafield está vacío.
- [x] Blocks `alternate_locale` / `noindex_locale` eliminados del schema de section.

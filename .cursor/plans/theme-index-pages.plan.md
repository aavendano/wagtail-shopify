---
name: theme-index-pages
overview: Implementar plantillas Liquid del theme Shopify para consumir índices precomputados (glossary_index, location_index) y páginas de detalle de metaobjects glossary_term / local_page.
active: true
created: 2026-07-05
---

# Theme — índices A–Z y páginas CMS (Liquid)

## Prompt de implementación

> Implementa en el **theme Shopify** (repo del theme, fuera de wagtail-shopify) las plantillas Liquid que consumen los datos que el backend Wagtail ya empuja a Shopify. El backend **no renderiza HTML**; solo precomputa JSON en metafields de Pages y sincroniza metaobjects merchant-owned. Tu trabajo es leer esos datos en Liquid, renderizar UI accesible y SEO-friendly, y conectar navegación entre locales.
>
> **Prerrequisitos operativos ya resueltos en backend:**
> - `python manage.py ensure_page_metafield_definitions`
> - `python manage.py bootstrap_index_pages --apply-export-config`
> - `python manage.py rebuild_glossary_index` → `pushed=3` (en, es, fr)
> - `python manage.py rebuild_location_index` → `pushed=2` (en-US, es-US)
>
> **Referencias de contrato:** [`docs/shopify_content.md`](../../docs/shopify_content.md), builders en [`shopify_content/glossary/index.py`](../../shopify_content/glossary/index.py) y [`shopify_content/locations/index.py`](../../shopify_content/locations/index.py).

## Contexto arquitectónico

```mermaid
flowchart TB
    subgraph wagtail [Wagtail CMS — hecho]
        Term[GlossaryTermPage]
        Loc[LocationPage]
        BuilderG[build_glossary_index_json]
        BuilderL[build_location_index_json]
        Term --> BuilderG
        Loc --> BuilderL
    end

    subgraph shopify [Shopify Storefront — a implementar]
        PageG[glossary-en / es / fr Pages]
        PageL[locations-en-us / es-us Pages]
        MOTerm[metaobject glossary_term]
        MOLoc[metaobject local_page]
        LiquidG[page.glossary-index.liquid]
        LiquidL[page.location-index.liquid]
        LiquidTerm[metaobject/glossary_term.liquid]
        LiquidLoc[metaobject/local_page.liquid]
    end

    BuilderG -->|custom.glossary_index| PageG
    BuilderL -->|custom.location_index| PageL
    PageG --> LiquidG
    PageL --> LiquidL
    MOTerm --> LiquidTerm
    MOLoc --> LiquidLoc
```

| Recurso Shopify | Origen Wagtail | Rol en theme |
|-----------------|----------------|--------------|
| Page `glossary-{locale}` | `export_config.glossary_index.pages` | Listado A–Z por idioma |
| Page `locations-{locale}` | `export_config.location_index.pages` | Listado por estado |
| Metaobject `glossary_term` | `GlossaryTermPage` | Detalle de término |
| Metaobject `local_page` | `LocationPage` | Detalle de ubicación |
| Metaobject `root_page` | `ShopifyRootPage` | Config mirror (opcional v1) |

## Contratos de datos (backend → theme)

### Metafields en Shopify Pages (owner `PAGE`, namespace `custom`)

| Key | Tipo | Consumer |
|-----|------|----------|
| `glossary_locale` | `single_line_text_field` | Código locale del índice: `en`, `es`, `fr` |
| `glossary_index` | `json` | Payload precomputado del listado glosario |
| `location_locale` | `single_line_text_field` | Código locale: `en-US`, `es-US` |
| `location_index` | `json` | Payload precomputado del listado locations |

**Handles de Pages creadas por bootstrap** (tienda `asgiti-0w`):

| Handle | Locale metafield | GID (ejemplo) |
|--------|------------------|---------------|
| `glossary-en` | `en` | `gid://shopify/Page/290003157067` |
| `glossary-es` | `es` | `gid://shopify/Page/290003189835` |
| `glossary-fr` | `fr` | `gid://shopify/Page/290003222603` |
| `locations-en-us` | `en-US` | `gid://shopify/Page/290003255371` |
| `locations-es-us` | `es-US` | `gid://shopify/Page/290003288139` |

### JSON `custom.glossary_index`

```json
{
  "version": 1,
  "locale": "es",
  "generated_at": "2026-07-05T12:00:00+00:00",
  "count": 70,
  "sections": [
    {
      "key": "A",
      "items": [
        {
          "term": "Afrodisíaco",
          "handle": "afrodisiaco",
          "path": "/pages/glossary/afrodisiaco"
        }
      ]
    }
  ]
}
```

**Reglas del builder (no reimplementar en Liquid):**

- Solo términos **live** con `shopify_id` en Wagtail.
- Agrupación por `key`: `A`–`Z`, `0-9`, `#` (orden fijo en `sections[]`).
- `path` siempre `/pages/glossary/{handle}`.
- `locale` en metafield y en JSON deben coincidir.

### JSON `custom.location_index`

```json
{
  "version": 1,
  "locale": "en-US",
  "generated_at": "2026-07-05T12:00:00+00:00",
  "count": 42,
  "sections": [
    {
      "key": "California",
      "items": [
        {
          "titulo": "Los Angeles Store",
          "handle": "los-angeles-store",
          "path": "/pages/location/los-angeles-store",
          "city": "Los Angeles",
          "state": "California"
        }
      ]
    }
  ]
}
```

**Reglas del builder:**

- Solo locations **live** con `shopify_id`.
- Agrupación por `state`; sin estado → sección `#` al final.
- `path` siempre `/pages/location/{handle}`.
- Filtrado por locale Wagtail/Shopify (`en-US`, `es-US`).

### Metaobject `glossary_term` (detalle)

| Campo metaobject | Tipo | Uso en theme |
|------------------|------|--------------|
| `term` | single line | H1, breadcrumb |
| `definition` | rich text | Cuerpo principal |
| `image` | file reference | Hero / OG image |
| `locale` | single line | Selector de idioma (`en`/`es`/`fr`) |
| `meta_title` | single line | `<title>` (capability renderable) |
| `meta_description` | multi line | meta description |
| `related_links` | json | Enlaces internos legacy |
| `external_links` | json | Enlaces externos |
| `synonyms` | list.single_line_text_field | Chips / SEO |
| `same_as` | list.url | Schema.org `sameAs` |
| `related_products` | list.product_reference | Bloque relacionados |
| `related_collections` | list.collection_reference | Bloque relacionados |
| `related_articles` | list.article_reference | Bloque relacionados |
| `related_glossary_terms` | list.metaobject_reference | Términos relacionados |

**URL de detalle:** capability `onlineStore` del metaobject (handle por término). El índice enlaza vía `path` precomputado.

### Metaobject `local_page` (detalle)

| Campo | Sección UI sugerida |
|-------|---------------------|
| `titulo`, `subtitulo`, `intro` | Hero |
| `country`, `state`, `city`, `locale` | Localización / breadcrumb |
| `titulo_2`, `subtitulo_h2`, `content_2` | Sección 2 |
| `titulo_3`, `subtitulo_3`, `content_3` | Sección 3 |
| `brand_section_*` | Brand |
| `map_title`, `map_content` | Mapa |
| `after_page_content` | Cierre |
| `faqs` | json → accordion FAQ |

Capability `onlineStore` con `urlHandle: local-page` → URLs `/pages/location/{handle}`.

## Fases de implementación

### Fase 1 — Snippet compartido: parseo JSON de índice

- [ ] Crear `snippets/wagtail-index-parse.liquid` (o equivalente) que:
  - Lea `page.metafields.custom.glossary_index.value` o `location_index.value`.
  - Parsee JSON con `| parse_json` (Shopify 2.x) o fallback seguro si vacío.
  - Exponga variables: `index.version`, `index.locale`, `index.count`, `index.sections`.
  - Maneje gracefully: metafield ausente → mensaje “índice no disponible” + log en theme check.
- [ ] Validar `index.version === 1`; ignorar versiones futuras con aviso en comentario Liquid.

### Fase 2 — Plantilla índice glosario

- [ ] Asignar `templateSuffix: glossary-index` a Pages `glossary-en`, `glossary-es`, `glossary-fr` (Admin o `pageUpdate`).
- [ ] Crear `templates/page.glossary-index.liquid`:
  - **SEO:** `page.title`, `page.content` mínimo; canonical a la URL actual.
  - **Nav A–Z:** anclas `#section-A` … `#section-Z`, `0-9`, `#` (solo letras con items).
  - **Listado:** loop `sections` → `items` → `<a href="{{ item.path }}">{{ item.term }}</a>`.
  - **Switcher idioma:** links hardcoded o desde metaobject `root_page` slug=glossary config (v2); v1: links a `/pages/glossary-en`, `/pages/glossary-es`, `/pages/glossary-fr`.
  - **Accesibilidad:** `<nav aria-label="Glossary index">`, listas semánticas `<ul>/<li>`.
- [ ] Estilos coherentes con design system del theme (CSS existente, BEM o utilidades del theme).

### Fase 3 — Plantilla índice locations

- [ ] Asignar `templateSuffix: location-index` a Pages `locations-en-us`, `locations-es-us`.
- [ ] Crear `templates/page.location-index.liquid`:
  - Agrupar por `section.key` (estado).
  - Mostrar `titulo`, `city`, `state`; enlace vía `item.path`.
  - Switcher `en-US` / `es-US`.
  - Nav jump por estado (opcional si muchos estados).

### Fase 4 — Plantilla detalle `glossary_term`

- [ ] Crear/actualizar plantilla metaobject `glossary_term` en theme:
  - H1 = `metaobject.term`.
  - Cuerpo = `metaobject.definition` (rich text ya viene HTML).
  - Imagen si `metaobject.image`.
  - Bloque synonyms como lista.
  - **Enlaces relacionados:** preferir refs nativas:
    ```liquid
    {% for product in metaobject.related_products.value %}
      <a href="{{ product.url }}">{{ product.title }}</a>
    {% endfor %}
    ```
  - Fallback a `related_links` JSON si refs vacías.
  - Breadcrumb: índice locale → término (`/pages/glossary-{locale}` → término).
  - JSON-LD `DefinedTerm` con `sameAs` desde `metaobject.same_as`.

### Fase 5 — Plantilla detalle `local_page`

- [ ] Crear/actualizar plantilla metaobject `local_page`:
  - Secciones según tabla de campos.
  - FAQs desde `metaobject.faqs` (parse json).
  - Breadcrumb: índice locations → ciudad/estado → título.
  - JSON-LD `LocalBusiness` o `Store` según datos disponibles.

### Fase 6 — Navegación, SEO e i18n

- [ ] Añadir enlaces en header/footer al índice glosario del locale activo de la tienda.
- [ ] Mapeo locale Shopify Markets ↔ `glossary_locale` / `location_locale`:
  - Glosario: `en` / `es` / `fr` (no incluye sufijo país).
  - Locations: `en-US` / `es-US`.
- [ ] `hreflang` entre Pages índice hermanas (manual v1).
- [ ] Verificar que `path` del JSON coincide con rutas reales del metaobject (smoke test 3 términos + 3 locations).

### Fase 7 — QA y documentación theme

- [ ] Theme check / Lighthouse en Pages índice y 2 detalles por tipo.
- [ ] Documentar en README del theme: handles, templateSuffix, dependencia de metafields.
- [ ] Checklist post-deploy Wagtail: publish término → índice se actualiza en ≤ Celery latency; refresh storefront.

## Patrones Liquid recomendados

### Leer índice glosario en page template

```liquid
{% assign index_raw = page.metafields.custom.glossary_index.value %}
{% if index_raw != blank %}
  {% assign index = index_raw | parse_json %}
  {% assign locale = page.metafields.custom.glossary_locale.value | default: index.locale %}
{% endif %}
```

### Loop secciones

```liquid
{% if index.sections %}
  <nav aria-label="Alphabetical index">
    {% for section in index.sections %}
      <a href="#glossary-{{ section.key }}">{{ section.key }}</a>
    {% endfor %}
  </nav>
  {% for section in index.sections %}
    <section id="glossary-{{ section.key }}">
      <h2>{{ section.key }}</h2>
      <ul>
        {% for item in section.items %}
          <li><a href="{{ item.path }}">{{ item.term }}</a></li>
        {% endfor %}
      </ul>
    </section>
  {% endfor %}
{% endif %}
```

## Criterios de aceptación

- [ ] `/pages/glossary-en` (y es/fr) renderizan listado A–Z desde `custom.glossary_index` sin llamadas AJAX al backend Wagtail.
- [ ] `/pages/locations-en-us` (y es-us) renderizan listado por estado desde `custom.location_index`.
- [ ] Detalle de término metaobject muestra `term`, `definition`, SEO y al menos un bloque de enlaces relacionados.
- [ ] Detalle `local_page` renderiza hero, secciones rich text y FAQs.
- [ ] Enlaces del índice resuelven a URLs 200 (no 404).
- [ ] Tras `rebuild_glossary_index` en Wagtail, un refresh del storefront refleja cambios (sin redeploy theme).
- [ ] Mobile-first, contraste WCAG AA en nav A–Z.

## Fuera de alcance v1

- Crear o editar Pages/metafields desde el theme (solo lectura).
- Lógica de agrupación A–Z o por estado en Liquid (ya viene en JSON).
- Consumo de `root_page.config` para routing dinámico (v2).
- `theme_config` en productos/colecciones (plan separado).
- App embed / Storefront API proxy a Wagtail.
- Traducciones Shopify Translate & Adapt de metafields JSON.

## Dependencias backend (no tocar en este plan)

| Comando | Cuándo |
|---------|--------|
| `rebuild_glossary_index` | Tras bulk import o si índice desincronizado |
| `rebuild_location_index` | Idem locations |
| `bootstrap_index_pages --apply-export-config` | Nueva tienda |
| Publish/unpublish término o location | Sync automático vía Celery |

## Verificación cruzada con backend

```bash
# Wagtail — regenerar índices
python manage.py rebuild_glossary_index --dry-run   # inspeccionar JSON
python manage.py rebuild_glossary_index
python manage.py rebuild_location_index

# Shopify Admin API — confirmar metafield poblado (desde wagtail-shopify)
python manage.py shell -c "
from core.models import ShopConfig
from shopify_requests.graphql_service import execute_admin_graphql
shop = ShopConfig.objects.first().shop
q = '''query(\$id: ID!) { node(id: \$id) { ... on Page { handle metafield(namespace:\"custom\", key:\"glossary_index\") { value } } } }'''
print(execute_admin_graphql(q, shop=shop, variables={'id': 'gid://shopify/Page/290003157067'}).data)
"
```

## Estado

**Backend completado.** Theme Liquid pendiente — este plan es el prompt de implementación para el repo del theme.

## Planes relacionados

- [`glossary-index-sync.plan.md`](glossary-index-sync.plan.md) — backend índice glosario (completado)
- [`root-export-config-admin.plan.md`](root-export-config-admin.plan.md) — UI Wagtail para `export_config` (futuro)

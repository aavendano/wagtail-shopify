# Inventario de contenido PlayLoveToys

Mapa canónico **schema → proyección Shopify → Wagtail → canal**, anclado en
`plt-editorial-schema` `contractVersion` **1.1.0** y en evidencia de repos
(no Admin live). Arquitectura: [ADR 0003](adr/0003-dual-channel-storefronts.md).

**Leyenda de estado**

| Etiqueta | Significado |
|----------|-------------|
| **en código** | Modelo/sync o loader presente en el repo citado |
| **en tienda** | Inventario merchant (handles/títulos reportados); no implica smoke E2E |
| **pendiente** | Decisión o verificación abierta (P0–P4) |

---

## Matriz schema → Shopify → Wagtail

| Schema `document.type` | Path `plt-content` | Shopify (proyección típica) | Wagtail | Estado |
|------------------------|--------------------|-----------------------------|---------|--------|
| `home` | `{m}/{l}/index.md` | metaobject `home_page` | `HomePage` | **en código** (sync Wagtail; H2 loader) |
| `page` | `{m}/{l}/pages/{slug}.md` | Online Store Page | — (sin tipo sync prioritario) | **en tienda** (23 handles); **pendiente** P2 |
| `product` | `…/products/{handle}.md` | Product | `ProductPage` | **en código** |
| `collection` | `…/collections/{handle}.md` | Collection (+ meta `seo_collection` en tienda) | `CollectionPage` | **en código** Collection; `seo_collection` **pendiente** P3 |
| `blog` | `…/blogs/{blogHandle}.md` | Blog nativo | `BlogPage` | **en código**; 12 blogs **en tienda** |
| `article` | `…/blogs/{blog}/{slug}.md` | Article **nativo** | `ArticlePage` | **en código**; ≠ metaobjeto merchant `article` (P3) |
| `glossary_term` | `…/glossary/{slug}.md` | `glossary_term` + índices `root_page` / Page metafields | `GlossaryTermPage` + `ShopifyRootPage` | **en código**; canales divergen (P4) |
| `location` | `…/local/{slug}.md` `_template: location` | H2: `location_page`; Wagtail sync: **`local_page`** | `LocationPage` → `local_page` | **P1** naming triangle |
| `region` | `…/local/{slug}.md` `_template: region` | H2: `region` | **sin** `RegionPage` | **P1** |
| _(índices Liquid)_ | — | `root_page` / Page `custom.index_listings` | `ShopifyRootPage` | **en código** rebuild; smoke **pendiente** P4 |
| _(funcionales)_ | — | plantillas tema (cart, account, 404) | — | no editorial |

Bloques reutilizables (no páginas): en tienda aparecen piezas tipo
`content_group`, `faq`, `link_card`, `multicolumn_block`, `social_media`,
`html_pages`. El schema registra bloques `commerce_page` / `cms_home` /
`editorial` — no confundir con document types.

---

## Triángulo de nombres geo (P1)

El contrato editorial **no** define tipos document `local_page` ni
`location_page`. Las capas usan identificadores distintos:

| Capa | Ciudad | Región |
|------|--------|--------|
| `plt-editorial-schema` / Tina / `plt-content` | document **`location`** | document **`region`** |
| Shopify Admin (loaders H2) | metaobject **`location_page`** | metaobject **`region`** |
| Wagtail sync outbound | metaobject **`local_page`** | sin sync |
| Tema Liquid | templates `metaobject/local_page.json` y `metaobject/location.json` → sección `local-page`; índices vía `root_page` / `custom.index_listings` | sin alias canónico en registry hacia `location`/`region` |

URLs públicas del schema: location → `/pages/canada-location/{slug}`; region →
`/pages/canada/{slug}` (coinciden con rutas H2 documentadas).

**Decisiones abiertas (no implementar sync masivo aquí):**

1. ¿Canonicalizar metaobjetos Shopify a nombres del schema o mantener aliases por consumidor?
2. ¿Wagtail deja `local_page` por `location_page` (o dual-write)?
3. ¿Añadir `RegionPage` + sync a `region`, o regiones solo Admin / Tina fallback?
4. ¿Liquid Online Store lee detalle `local_page` / `location` además del índice?
5. Hasta cerrar: **no** declarar geo “E2E sync” en ningún canal.

---

## Canal Hydrogen — consumo (evidencia de repo)

Fuente: sibling `tina-hydrogen-frontstore` (`AGENTS.md`, `README.md`,
`.env.example`, loaders bajo `app/lib/`, rutas `app/routes/`).

### Dominios / entorno (solo lo documentado)

| Qué | Evidencia | Valor |
|-----|-----------|--------|
| Staging hostname | `AGENTS.md`, `README.md` | `h2-dev.aadigitalbusiness.com` → Oxygen `*.o2.myshopify.dev` |
| Shopify store (dev) | `README.md`, `.env.example` | `aadigital-dev-02.myshopify.com` |
| Storefront name | `README.md` | Hydrogen storefront **"tina"** |
| Canonical prod origin | `.env.example` | `PUBLIC_CANONICAL_ORIGIN` comentado (`https://www.example.com`) — **no** inventar dominio de producción PlayLoveToys |
| Oxygen workflow | `AGENTS.md` | `.github/workflows/oxygen-deployment-1000181004.yml`; `main`→prod, `ai-dev`→staging |

### Tabla consume hoy / no / desconocido

| Tipo (schema / recurso) | H2 consume hoy? | Evidencia | Notas |
|-------------------------|-----------------|-----------|-------|
| `home` / `home_page` | **consume hoy** | `app/lib/shopify-home.server.ts`; ruta `($locale)._index.tsx`; `AGENTS.md` | Tina fallback si falta metaobject |
| `glossary_term` | **consume hoy** | `shopify-editorial.server.ts` queries `glossary_term`; rutas `/glossary/:handle`, hub `/pages/glossary` | **No** usa `root_page` |
| Índice glosario | **consume hoy** (lista metaobjects) | `loadShopifyGlossaryIndex` en hub `pages/glossary` | Distinto del índice Liquid `root_page` |
| `location` vía `location_page` | **consume hoy** | queries `location_page`; ruta `/pages/canada-location/:handle` | No lee Wagtail `local_page` |
| `region` | **consume hoy** | queries `region`; ruta `/pages/canada/:handle` | Sin modelo Wagtail |
| Índice locations | **consume hoy** | `loadShopifyLocationIndex` (`location_page` + `region`) | Hub `/pages/locations` |
| Blog / Article nativos | **consume hoy** | rutas `($locale).blogs.*` vía Storefront API Blog | No metaobjeto `article` |
| Online Store Page (`page`) | **consume hoy** (fallback) | `($locale).pages.$handle.tsx`: Tina → editorial hub → `PAGE_QUERY` Shopify Page | Corporativas dependen de datos en shop |
| `local_page` (Wagtail) | **no consume** | ningún query `type: "local_page"` en `app/` | Gap P1 |
| `root_page` | **no consume** | sin referencias en loaders H2 | Solo contrato Liquid |
| `seo_collection` | **desconocido** | sin hit en loaders H2 revisados | P3 |
| Metaobjeto merchant `article` | **no consume** (blogs usan Article nativo) | rutas blog Storefront | P3 naming |

Orden de fallback documentado en H2: Shopify metaobject → Tina/`plt-content` →
(home) secciones featured-collection built-in.

---

## Glosario y ubicaciones — Liquid vs Hydrogen (P4)

| Paso | Liquid (Online Store) | Hydrogen |
|------|----------------------|----------|
| Autoría detalle | Wagtail `GlossaryTermPage` / `LocationPage` → Shopify | Hoy: editar metaobjects en Admin (guía H2); Tina frozen fallback |
| Índice | `root_page` por locale y/o Page + `custom.index_listings` → `sections/wagtail-root-index.liquid` | Lista directa de `glossary_term` / `location_page`+`region` |
| URL índice (doc backend) | `/pages/index/glossary-*`, `/pages/index/locations-*`, hubs Page | `/pages/glossary`, `/pages/locations` |
| URL detalle | tema + metaobject templates (`glossary_term`, `local_page` / `location`) | `/glossary/:handle`, `/pages/canada-location/:handle`, `/pages/canada/:handle` |

### Smoke checklist (Liquid / Wagtail) — ejecutar y registrar evidencia

No marcar “verificado en producción” sin pegar resultado de un run.

1. `python manage.py ensure_metaobject_definitions` (incluye `root_page` + `onlineStore`).
2. Roots Wagtail `glossary`, `local-us` (y `blogs` si aplica) con `export_config.locales`.
3. `python manage.py rebuild_glossary_index` (+ `--dry-run` opcional).
4. `python manage.py rebuild_location_index`.
5. GraphQL Admin: `metaobjectByHandle` `root_page` / `glossary-en-us` (y locations) con campo `index` poblado — ver snippet en `docs/shopify_content.md`.
6. Storefront Liquid: HTTP 200 en `/pages/index/glossary-en-us`, `/pages/index/locations-en-us` (y locales configurados).
7. Theme: template metaobject `root_page` + sección `wagtail-root-index` (o Page hubs con `custom.index_listings` según rollout documentado en tema).

### Smoke checklist (Hydrogen) — solo lectura

1. Staging documentado: `h2-dev.aadigitalbusiness.com` (login Shopify / bypass CI según `AGENTS.md`).
2. `/` carga `home_page` o fallback Tina.
3. `/glossary/{handle}` y `/pages/glossary` con datos `glossary_term`.
4. `/pages/canada-location/{handle}`, `/pages/canada/{handle}`, `/pages/locations`.
5. Confirmar que **no** se espera `root_page` ni `local_page` en Network/GraphQL del storefront H2.

---

## 12 blogs (evidencia de tienda)

Títulos reportados en inventario merchant (handles Shopify no verificados en este doc):

1. Playful Connections  
2. The Pleasure Lab  
3. Sexual Wellness Revealed  
4. Sex Toys Artisans  
5. After Page Content — uso en navegación **pendiente** (P3)  
6. Unbound Binary  
7. Erotic Stories  
8. Sexual Fantasies & Desire  
9. Sexual Practices  
10. Adult Lifestyle & Swingers  
11. Erotic Play  
12. B  

Wagtail: `BlogPage` / `ArticlePage` ↔ Blog / Article nativos (**en código**).

---

## 23 Pages Online Store (evidencia de tienda)

Registros de contenido; no implica visibilidad en nav. Schema type: `page`.
Ownership CMS: **decisión abierta** (P2) — no import masivo en este ciclo.

| Clase | Título (handle) |
|-------|-----------------|
| Corporativas | About Us (`about-us`), Our Values (`values`) |
| Atención y ayuda | Contact us (`contact-us`), Frequently Asked Questions (`faq`), Shipping Info (`shipping-info`), Shipping Info - Lingerie (`shipping-info-lingerie`), Return & Refund Policy (`return-refund-policy`) |
| Confianza / avisos | Reviews (`reviews`), Your Privacy Choices (`data-sharing-opt-out`), Website Disclaimer (`website-disclaimer`), Age Restricted (`age-restricted`), Image Credits (`image-credits`) |
| Funcionalidad / programas | My Wishlist (`wishlist`), Shared Wishlists (`shared-wishlists`), Manage Subscription (`joy-subscription`), Join Our Affiliate Program (`affiliate-program`) |
| Portales de contenido | Blog (`blogs`), Glossary (`glossary`), Locations (`locations`), Our Service Areas (`our-locations`) |
| Guías e informes | Which Lubricant Works With Your Toy? (`lube-toy-compatibility-guide`), Manufacturer Warranty Guide (`manufacturer-warranty-guide`), Global Sexual Wellness Market Report (`sexual-wellness-online-market-report-2025`) |

Portales `blogs` / `glossary` / `locations` solapan con índices CMS
(`ShopifyRootPage` + Liquid / hubs H2); no fusionar ownership sin decisión P2/P4.

---

## Backlog P0–P4 (decisions-open)

Cerrado como **documentación de pendientes**. Sin implementación de sync masivo
ni cambio de `contractVersion` del schema en esta entrega.

### P0 — Canal Hydrogen (verificar, no asumir)

- Dominios: solo los citados arriba; prod canonical **desconocido** hasta
  `PUBLIC_CANONICAL_ORIGIN` real en Oxygen.
- Tabla de consumo rellenada con evidencia de repo (sección anterior).
- **Abierto:** smoke staging con run log / captura humana.

### P1 — Geo naming triangle

- Documentado arriba; decisión de producto pendiente (aliases vs unificar;
  `RegionPage` sí/no; qué lee Liquid en detalle).

### P2 — Pages corporativas / ayuda (23)

- Existen en tienda; Wagtail no las modela como sync prioritario.
- **Abierto:** import Page + sync vs solo Admin Shopify vs solo tema/Tina.

### P3 — Naming traps

- Metaobjeto merchant `article` ≠ Article nativo (`ArticlePage`).
- `seo_collection`: en tienda; consumo en plantilla Liquid/H2 **desconocido**.
- Blog “After Page Content”: rol en tema/nav **pendiente**.

### P4 — Contrato glosario/ubicaciones

- Liquid: `root_page` / `index_listings` (checklist arriba).
- H2: `glossary_term` / `location_page` / `region` directo — divergencia
  documentada; smoke con evidencia aún **abierto**.

**Orden sugerido de resolución:** P0 evidencia staging → P1 geo → P3 naming →
P2 pages → P4 smoke Liquid con run registrado.

---

## Referencias

- [ADR 0003 dual-channel](adr/0003-dual-channel-storefronts.md)
- [ADR 0002 tenancy](adr/0002-shop-tenancy-membership.md)
- [docs/shopify_content.md](shopify_content.md) — modelos y rebuild de índices
- `plt-editorial-schema` `registry.json` (`contractVersion` 1.1.0)
- `tina-hydrogen-frontstore` `AGENTS.md`, `docs/user-guide/`
- `plt-frontend-liquid` `sections/wagtail-root-index.liquid`, templates
  `metaobject/root_page.json`, `local_page.json`, `location.json`

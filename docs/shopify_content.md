# App `shopify_content`

App principal del CMS. Gestiona los modelos de página Wagtail que se sincronizan automáticamente con Shopify Admin vía GraphQL al publicar.

---

## Rol de la app

`shopify_content` convierte Wagtail en un CMS headless para Shopify:

- Los editores crean y editan contenido en Wagtail Admin.
- Al publicar una página, el hook `after_publish_page` **encola** la sincronización outbound vía Celery (no bloquea el publish).
- Las importaciones inbound (Wagtail admin, app embebida, API `POST */pull`) también se ejecutan en background.
- El estado de cada job se registra en `ShopifySyncRun` (Django Admin). Ver README → sección Celery para worker/beat.
- El storefront de Shopify sigue sirviendo al cliente final.

El proyecto es **single-tenant**: una instalación Wagtail = una tienda Shopify. El `shop` se resuelve desde `ShopConfig.objects.first().shop`; no se almacena en cada página.

---

## Modelos de página

| Modelo Wagtail | Recurso Shopify | Operación de sync |
|----------------|-----------------|-------------------|
| `ShopifyRootPage` | — | Página raíz; no tiene sync propio |
| `ProductPage` | Product | `productUpdate` |
| `CollectionPage` | Collection | `collectionUpdate` |
| `BlogPage` | Blog | `blogCreate` / `blogUpdate` |
| `ArticlePage` | Article | `articleCreate` / `articleUpdate` |
| `LocationPage` | Metaobject merchant-owned (`local_page`) | `metaobjectUpsert` vía `MetaobjectClient` |
| `GlossaryTermPage` | Metaobject merchant-owned (`glossary_term`) | `metaobjectUpsert` vía `MetaobjectClient` |

### Jerarquía de páginas

```
ShopifyRootPage
├── ProductPage  (slug = handle Shopify)
├── CollectionPage
├── BlogPage
│   └── ArticlePage
├── LocationPage  (bajo root slug=local-us)
└── GlossaryTermPage  (bajo root slug=glossary)
```

---

## Mixin base — `models/mixins.py`

Todos los modelos de página (excepto `ShopifyRootPage`) heredan de `ShopifyPageMixin`:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `shopify_id` | CharField(255) | GID completo del recurso en Shopify (poblado tras el primer sync) |
| `handle` | SlugField(255) | Handle de Shopify (por defecto usa el `slug` de la página) |
| `sync_enabled` | BooleanField | Activa/desactiva el sync para esta página |
| `last_synced_at` | DateTimeField | Timestamp del último sync exitoso |

`FAQItem` (abstract + `Orderable`) define el schema de preguntas frecuentes reutilizado como InlinePanel en cada tipo de página.

---

## ProductPage — `models/product.py`

| Campo Wagtail | Campo Shopify | Notas |
|---------------|---------------|-------|
| `title` (Page) | `title` | Campo built-in de Wagtail |
| `handle` (mixin) | `handle` | |
| `vendor` | `vendor` | |
| `product_type` | `productType` | |
| `tags` | `tags` | ClusterTaggableManager |
| `status` | `status` | Choices: ACTIVE / DRAFT / ARCHIVED |
| `body` | `descriptionHtml` | StreamField → HTML renderizado |
| `seo_title` (Page) | `seo.title` | Campo SEO built-in de Wagtail |
| `search_description` (Page) | `seo.description` | Campo SEO built-in de Wagtail |
| `shopify_images` | `images` (pull) | InlinePanel → URLs absolutas CDN (máx. 10) |
| `metafields` | `metafields` | InlinePanel → `metafieldsSet` (solo outbound / edición manual) |
| `faqs` | metafield `custom.faqs` | InlinePanel → JSON |

---

## CollectionPage — `models/collection.py`

| Campo Wagtail | Campo Shopify | Notas |
|---------------|---------------|-------|
| `title` (Page) | `title` | |
| `handle` (mixin) | `handle` | |
| `sort_order` | `sortOrder` | Choices: MANUAL / BEST\_SELLING / TITLE\_ASC / etc. |
| `description` | `descriptionHtml` | StreamField → HTML |
| `seo_title` (Page) | `seo.title` | |
| `search_description` (Page) | `seo.description` | |
| `image_url` | `image.url` (pull) | URL absoluta CDN |
| `image_alt_text` | `image.altText` (pull) | |
| `metafields` | `metafields` | Solo outbound / edición manual en pull |
| `faqs` | metafield `custom.faqs` | |

---

## BlogPage — `models/blog.py`

| Campo Wagtail | Campo Shopify | Notas |
|---------------|---------------|-------|
| `title` (Page) | `title` | |
| `handle` (mixin) | `handle` | |
| `comment_policy` | `commentPolicy` | Choices: AUTO\_PUBLISHED / CLOSED / MODERATED |
| `description` | metafield `custom.description` | No hay campo nativo en la API |
| `seo_title` (Page) | metafield `global.title_tag` | La API Blog no tiene campo `seo` nativo |
| `search_description` (Page) | metafield `global.description_tag` | |
| `faqs` | metafield `custom.faqs` | |

`BlogPage` es el padre de `ArticlePage`. Al crear un `BlogPage` sin `shopify_id`, el sync llama `blogCreate`; si ya tiene ID, llama `blogUpdate`.

---

## ArticlePage — `models/blog.py`

| Campo Wagtail | Campo Shopify | Notas |
|---------------|---------------|-------|
| `title` (Page) | `title` | |
| `handle` (mixin) | `handle` | |
| `author` | `author.name` | CharField; AuthorInput en la API |
| `body` | `body` | StreamField → HTML (campo `body`, no `bodyHtml`) |
| `summary` | `summary` | TextField HTML |
| `published_at` | `publishedAt` | DateTimeField |
| `tags` | `tags` | |
| `featured_image_url` | `image.url` (pull) | URL absoluta CDN |
| `featured_image_alt` | `image.altText` (pull) | |
| `featured_image` | — | FK Wagtail Image (manual/API; pull no lo toca) |
| `seo_title` (Page) | metafield `global.title_tag` | No se importa en pull |
| `search_description` (Page) | metafield `global.description_tag` | No se importa en pull |
| `metafields` | `metafields` | Solo outbound / edición manual en pull |
| `faqs` | metafield `custom.faqs` | |

El `blogId` del padre (`ArticlePage.get_parent().specific.shopify_id`) se pasa en `articleCreate`.

---

## LocationPage — `models/location_page.py`

Implementada como **merchant-owned metaobject** (tipo `local_page`) en Shopify. La definición se crea en el store vía `metaobjectDefinitionCreate`; no requiere TOML ni `shopify app deploy`.

| Campo Wagtail | Campo Shopify (metaobject field) | Sección |
|---------------|----------------------------------|---------|
| `titulo` (requerido) | `titulo` | Hero |
| `subtitulo` | `subtitulo` | Hero |
| `intro` (RichTextField) | `intro` | Hero |
| `country` | `country` | Localización |
| `state` | `state` | Localización |
| `city` | `city` | Localización |
| `titulo_2` | `titulo_2` | Sección 2 |
| `subtitulo_h2` | `subtitulo_h2` | Sección 2 |
| `content_2` (RichTextField) | `content_2` | Sección 2 |
| `titulo_3` | `titulo_3` | Sección 3 |
| `subtitulo_3` | `subtitulo_3` | Sección 3 |
| `content_3` (RichTextField) | `content_3` | Sección 3 |
| `brand_section_title` | `brand_section_title` | Brand |
| `brand_section_subtitle` | `brand_section_subtitle` | Brand |
| `brand_section_content` (RichTextField) | `brand_section_content` | Brand |
| `map_title` | `map_title` | Mapa |
| `map_content` (RichTextField) | `map_content` | Mapa |
| `after_page_content` (RichTextField) | `after_page_content` | Cierre |
| `faqs` (InlinePanel) | `faqs` (tipo `json`) | FAQs |
| `shopify_locale` | `locale` | Locale |

Adicionalmente, `seo_title` y `search_description` de Wagtail se usan como `metaTitleField` y `metaDescriptionField` en las capabilities `renderable` de la definición.

### Capacidades (`capabilities`)

```python
capabilities={
    'publishable': {'enabled': True},
    'onlineStore': {'enabled': True, 'data': {'urlHandle': 'local-page'}},
    'renderable': {'enabled': True, 'data': {
        'metaTitleField': 'titulo',
        'metaDescriptionField': 'subtitulo',
    }},
}
```

### Bootstrap de la definición

```bash
python manage.py ensure_metaobject_definitions
```

Esto llama `MetaobjectClient.ensure_definition()` — idempotente; no falla si la definición ya existe.

---

## GlossaryTermPage — `models/glossary.py`

Implementada como **merchant-owned metaobject** (tipo `glossary_term`) en Shopify. Los términos viven bajo un `ShopifyRootPage` con slug `glossary` (solo organizacional). La página listado `/pages/glossary` la gestiona el theme en Liquid.

| Campo Wagtail | Campo Shopify (metaobject field) |
|---------------|----------------------------------|
| `term` (requerido) | `term` |
| `definition` (RichTextField) | `definition` |
| `locale_code` (`en`/`es`/`fr`) | `locale` |
| `related_links` (JSONField) | `related_links` |
| `external_links` (JSONField) | `external_links` |

Sin campos SEO dedicados — `renderable` usa `term` y `definition` como fallback.

### API REST

Endpoints en `/api/v1/glossary/` (CRUD + push). Ver `docs/api-agents.md` → sección Glossary.

---

## Flujo de sincronización outbound

```
Editor publica en Wagtail Admin
         │
         ▼
after_publish_page hook  (wagtail_hooks.py)
         │
         ├─ ProductPage    → sync_product_page(page)
         ├─ CollectionPage → sync_collection_page(page)
         ├─ BlogPage       → sync_blog_page(page)
         ├─ ArticlePage    → sync_article_page(page)
         ├─ LocationPage   → sync_location_page(page)
         └─ GlossaryTermPage → sync_glossary_term_page(page)
                  │
                  ▼
         shopify_content/sync/outbound.py
                  │
                  ▼
         execute_admin_graphql(query, shop=shop, variables=vars)
         (para LocationPage: MetaobjectClient.sync())
                  │
                  ▼
         Shopify Admin API (GraphQL 2026-07)
```

Todas las funciones de sync fallan silenciosamente: loguean el error pero no bloquean el publish de Wagtail.

### Funciones principales en `sync/outbound.py`

| Función | Descripción |
|---------|-------------|
| `sync_product_page(page)` | `productUpdate` con body HTML, SEO, metafields, tags |
| `sync_collection_page(page)` | `collectionUpdate` con body HTML, SEO, metafields |
| `sync_blog_page(page)` | `blogCreate` o `blogUpdate`; luego `metafieldsSet` para SEO y description |
| `sync_article_page(page)` | `articleCreate` o `articleUpdate`; luego metafields SEO + hreflang |
| `sync_location_page(page)` | `MetaobjectClient.sync()` con `ensure_definition=True` |
| `sync_glossary_term_page(page)` | `MetaobjectClient.sync()` tipo `glossary_term` |
| `_glossary_term_definition()` | Constructor lazy del `MetaobjectDefinitionSpec` glossary_term |
| `_render_streamfield_html(value)` | Convierte StreamField value → HTML string |
| `_push_metafields(shop, owner_gid, inputs)` | `metafieldsSet` para metafields personalizados |
| `_push_hreflang_metafields(page, shop, gid)` | Metafields `seo.hreflang_*` para tema Liquid |
| `_push_translations(page, shop, gid, fields)` | `translationsRegister` para contenido localizado |
| `_location_page_definition()` | Constructor lazy del `MetaobjectDefinitionSpec` completo |

---

## SEO

### Products y Collections

Los campos `seo_title` y `search_description` de Wagtail (built-ins de `Page`) se mapean directamente a `seo.title` y `seo.description` en `ProductInput` / `CollectionInput`.

### Blogs y Articles

La API de Shopify para Blog y Article **no tiene campo `seo` nativo**. El SEO se envía como metafields:

| Namespace | Key | Tipo | Contenido |
|-----------|-----|------|-----------|
| `global` | `title_tag` | `single_line_text_field` | `seo_title` del Page |
| `global` | `description_tag` | `single_line_text_field` | `search_description` del Page |

---

## FAQs

Cada tipo de página incluye un `InlinePanel('faqs')` con modelo `*FAQItem(Orderable)`:

| Campo | Tipo |
|-------|------|
| `question` | CharField(500) |
| `answer` | TextField |
| `sort_order` | IntegerField |

Al sincronizar, los FAQs se serializan como JSON y se envían como metafield:

```
namespace: "custom"
key: "faqs"
type: "json"
value: [{"question": "...", "answer": "..."}, ...]
```

---

## Traducciones y hreflang

### Traducciones en Shopify (`translationsRegister`)

Al publicar una página con locale distinto de `en-US`, `sync/outbound.py` llama `translationsRegister` para registrar el contenido en el idioma correcto dentro de Shopify.

Mapa de locales Wagtail → Shopify:

| Locale Wagtail | Locale Shopify |
|----------------|----------------|
| `en-US` | (no se registra como traducción; es el locale base) |
| `es-US` | `es` |
| `en-CA` | `en-CA` |
| `fr-CA` | `fr-CA` |

### hreflang para el tema Liquid

Para que el tema Liquid pueda emitir `<link rel="alternate" hreflang="...">`, se envían metafields por recurso:

| Namespace | Key | Tipo | Valor |
|-----------|-----|------|-------|
| `seo` | `hreflang_en_us` | `url` | URL canónica en-US |
| `seo` | `hreflang_es_us` | `url` | URL canónica es-US |
| `seo` | `hreflang_en_ca` | `url` | URL canónica en-CA |
| `seo` | `hreflang_fr_ca` | `url` | URL canónica fr-CA |

El tema Liquid lee estos metafields para emitir las etiquetas de hreflang dinámicamente.

---

## Import inbound — Shopify → Wagtail

Los management commands de import crean páginas Wagtail desde recursos existentes en Shopify. El body HTML se importa como un único `HtmlBlock` en el StreamField. Los editores pueden convertirlo a bloques estructurados posteriormente.

**Pull ligero:** el import inbound no descarga imágenes a `wagtailimages` ni importa metafields. Las imágenes se guardan como URLs absolutas en base de datos local:

| Recurso | Almacenamiento | Límite |
|---------|----------------|--------|
| `ProductPage` | `ProductPageImage` (InlinePanel `shopify_images`) | Máx. 10 URLs por producto |
| `CollectionPage` | `image_url`, `image_alt_text` | 1 imagen destacada |
| `ArticlePage` | `featured_image_url`, `featured_image_alt` | 1 imagen destacada |

El FK `ArticlePage.featured_image` a `wagtailimages.Image` se conserva para uso manual o vía API; el pull no lo modifica.

Los metafields (`ProductPageMetafield`, `CollectionPageMetafield`, artículos) **no se importan** en el pull. Los paneles del editor y el sync outbound al publicar siguen disponibles para metafields editados en Wagtail.

El SEO de artículos (`seo_title`, `search_description`) **no** se rellena automáticamente en el pull (antes venía de metafields `global.title_tag` / `global.description_tag`).

### `sync/inbound.py`

| Función | Descripción |
|---------|-------------|
| `import_products(shop, parent_page)` | Importa productos → `ProductPage` |
| `import_collections(shop, parent_page)` | Importa colecciones → `CollectionPage` |
| `import_blogs_and_articles(shop, parent_page)` | Importa blogs → `BlogPage` con `ArticlePage` hijos |
| `_paginate(shop, query, data_path, variables)` | Generator con cursor pagination |

---

## Management commands

| Comando | Descripción |
|---------|-------------|
| `import_shopify_products` | Importa productos de Shopify → `ProductPage` en Wagtail |
| `import_shopify_collections` | Importa colecciones → `CollectionPage` |
| `import_shopify_blogs` | Importa blogs y artículos → `BlogPage` / `ArticlePage` |
| `setup_locales` | Crea los 4 objetos `Locale` de Wagtail (en-US, es-US, en-CA, fr-CA) |
| `setup_celery_beat_schedules` | Crea la tarea periódica de importación inbound (deshabilitada por defecto) |
| `ensure_metaobject_definitions` | Crea o verifica definiciones de metaobjetos merchant-owned en Shopify (idempotente) |

---

## Configuración requerida

### `config/settings.py`

```python
INSTALLED_APPS = [
    # ...
    'wagtail_localize',
    'wagtail_localize.locales',
    # ... apps wagtail ...
    'shopify_content',
]

WAGTAIL_I18N_ENABLED = True

WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ('en-US', 'English (United States)'),
    ('es-US', 'Spanish (United States)'),
    ('en-CA', 'English (Canada)'),
    ('fr-CA', 'French (Canada)'),
]
LANGUAGE_CODE = 'en-US'
```

### Scopes de Shopify (`shopify.app.wagtail-cms.toml`)

```
read_content, write_content
read_online_store_pages, write_online_store_pages
read_products, write_products
read_metaobjects, write_metaobjects
read_metaobject_definitions, write_metaobject_definitions
```

---

## Estructura de archivos

```
shopify_content/
├── apps.py
├── wagtail_hooks.py          # Hook after_publish_page → dispatch sync
├── models/
│   ├── __init__.py
│   ├── mixins.py             # ShopifyPageMixin, FAQItem, SHOPIFY_SYNC_PANELS
│   ├── root.py               # ShopifyRootPage
│   ├── product.py            # ProductPage, ProductPageFAQ, ProductPageMetafield
│   ├── collection.py         # CollectionPage, CollectionPageFAQ, CollectionPageMetafield
│   ├── blog.py               # BlogPage, BlogPageFAQ, ArticlePage, ArticlePageFAQ, ArticlePageMetafield
│   ├── location_page.py      # LocationPage, LocationPageFAQ
│   └── glossary.py           # GlossaryTermPage
├── blocks/
│   ├── __init__.py
│   ├── content.py            # HeadingBlock, ParagraphBlock, HtmlBlock, CalloutBlock
│   ├── media.py              # ImageBlock, VideoEmbedBlock
│   └── product.py            # ProductFeatureBlock
├── sync/
│   ├── __init__.py
│   ├── queries.py            # GraphQL queries (GET_PRODUCT, LIST_BLOGS, etc.)
│   ├── mutations.py          # GraphQL mutations (PRODUCT_UPDATE, ARTICLE_CREATE, etc.)
│   ├── inbound.py            # Shopify → Wagtail import
│   └── outbound.py           # Wagtail → Shopify push
└── management/commands/
    ├── import_shopify_products.py
    ├── import_shopify_collections.py
    ├── import_shopify_blogs.py
    ├── setup_locales.py
    └── ensure_metaobject_definitions.py
```

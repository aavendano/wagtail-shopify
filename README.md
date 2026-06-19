# wagtail-shopify

Shopify Embedded App (Django + Wagtail) que usa Wagtail como CMS headless para gestionar el contenido de una tienda Shopify. Los editores trabajan en Wagtail admin; al publicar, el contenido se sincroniza automáticamente con Shopify Admin vía GraphQL. El storefront de Shopify sigue sirviendo al cliente final.

---

## Arquitectura

```
Wagtail Admin
     │
     │  after_publish_page hook
     ▼
shopify_content/sync/outbound.py
     │
     │  execute_admin_graphql  (shopify_requests)
     ▼
Shopify Admin API (GraphQL)
     │
     ▼
Shopify Storefront → Cliente final
```

**Single-tenant:** una instalación Wagtail = una tienda Shopify. El `shop` se resuelve desde `ShopConfig.objects.first().shop`; no se almacena en cada página.

---

## Apps del proyecto

| App | Descripción |
|-----|-------------|
| `core` | OAuth, `ShopConfig`, middleware de proxy local |
| `shopify_requests` | Cliente GraphQL centralizado; ver [`docs/shopify_requests.md`](docs/shopify_requests.md) |
| `metaobjects` | Toolkit para metaobjetos Shopify; ver [`docs/Documentation.txt`](docs/Documentation.txt) |
| `shopify_content` | Páginas Wagtail sincronizadas a Shopify; ver [`docs/shopify_content.md`](docs/shopify_content.md) |
| `webhooks` | Receptores de webhooks Shopify |
| `api` | API interna django-ninja para agentes AI — ver [`docs/api-agents.md`](docs/api-agents.md) |

---

## Tipos de página (`shopify_content`)

| Página Wagtail | Recurso Shopify | Operación de sync |
|----------------|-----------------|-------------------|
| `ProductPage` | Product | `productUpdate` |
| `CollectionPage` | Collection | `collectionUpdate` |
| `BlogPage` | Blog | `blogCreate` / `blogUpdate` |
| `ArticlePage` | Article | `articleCreate` / `articleUpdate` |
| `LocationPage` | Metaobject merchant-owned (`local_page`) | `metaobjectUpsert` |

---

## Setup inicial

```bash
# 1. Migraciones
python manage.py migrate

# 2. Crear locales (en-US, es-US, en-CA, fr-CA)
python manage.py setup_locales

# 3. Crear definición de metaobject merchant-owned en Shopify
python manage.py ensure_metaobject_definitions

# 4. En Wagtail admin: crear ShopifyRootPage como hija del root del sitio

# 5. Importar contenido existente desde Shopify
python manage.py import_shopify_blogs
python manage.py import_shopify_products
python manage.py import_shopify_collections
```

---

## Management commands

| Comando | Descripción |
|---------|-------------|
| `ensure_metaobject_definitions` | Crea o verifica las definiciones de metaobjetos merchant-owned en Shopify (idempotente) |
| `import_shopify_products` | Importa productos de Shopify → `ProductPage` en Wagtail |
| `import_shopify_collections` | Importa colecciones → `CollectionPage` |
| `import_shopify_blogs` | Importa blogs y artículos → `BlogPage` / `ArticlePage` |
| `setup_locales` | Crea los 4 objetos `Locale` de Wagtail (en-US, es-US, en-CA, fr-CA) |
| `setup_celery_beat_schedules` | Crea la tarea periódica de importación (deshabilitada por defecto) |

---

## Celery (sync asíncrono)

Las importaciones inbound (Wagtail admin, app embebida, API `POST */pull`) y el sync outbound al publicar páginas se ejecutan en **background** vía Celery. El estado de cada job se guarda en `ShopifySyncRun` (Django Admin → Shopify sync runs).

### Variables de entorno

```env
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
# CELERY_TASK_ALWAYS_EAGER=true   # dev sin worker (ejecuta inline)
```

### Procesos

```bash
# Redis debe estar corriendo
redis-server

# Worker
celery -A config worker -l info

# Beat (tareas periódicas en DB)
celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

# Desarrollo: worker + beat en un solo proceso
celery -A config worker --beat --scheduler django --loglevel=info
```

### Setup

```bash
python manage.py migrate django_celery_beat
python manage.py migrate
python manage.py setup_celery_beat_schedules
```

Habilita la tarea periódica en **Django Admin → Periodic tasks** (`Importar contenido nuevo desde Shopify`, cron 03:00 America/Toronto).

Los management commands `import_shopify_*` siguen siendo **síncronos** (útiles para ops sin worker).

---

## Scopes requeridos (`shopify.app.wagtail-cms.toml`)

```
read_content, write_content
read_online_store_pages, write_online_store_pages
read_products, write_products
read_metaobjects, write_metaobjects
read_metaobject_definitions, write_metaobject_definitions
```

---

## Módulo `metaobjects` — Shopify Metaobjects Toolkit

Toolkit modular para gestionar metaobjetos de Shopify vía Admin GraphQL API. Usa `shopify_requests.execute_admin_graphql` (mismo flujo de tokens que el resto del proyecto).

### Uso básico — definición con capacidades de storefront

```python
from metaobjects import MetaobjectClient, MetaobjectDefinitionSpec, MetaobjectFieldSpec

definition = MetaobjectDefinitionSpec(
    type='local_page',
    name='Location Page',
    description='Página de ubicación gestionada en Wagtail',
    display_name_field='titulo',
    capabilities={
        'publishable': {'enabled': True},
        'onlineStore': {'enabled': True, 'data': {'urlHandle': 'local-page'}},
        'renderable': {'enabled': True, 'data': {
            'metaTitleField': 'titulo',
            'metaDescriptionField': 'subtitulo',
        }},
    },
    access={'storefront': 'PUBLIC_READ'},
    fields=[
        MetaobjectFieldSpec(key='titulo', name='Título', type='single_line_text_field', required=True),
        MetaobjectFieldSpec(key='city',   name='City',   type='single_line_text_field'),
    ],
)

client = MetaobjectClient('mi-tienda.myshopify.com')
client.sync({'handle': 'austin-tx', 'titulo': 'Austin', 'city': 'Austin'}, definition=definition)
```

### Uso básico — desde un dataclass

```python
from dataclasses import dataclass
from metaobjects import MetaobjectClient, MetaobjectDefinitionSpec

@dataclass
class FabricSpec:
    handle: str
    fabric_name: str
    stretch_level: int
    is_organic: bool

client = MetaobjectClient('mi-tienda.myshopify.com')
definition = MetaobjectDefinitionSpec.from_dataclass(
    FabricSpec, type='fabric', name='Fabric', description='Material specs',
)
client.sync(FabricSpec('cotton-1', 'Cotton', 2, True), definition=definition)
```

### Estructura del paquete

```
metaobjects/
  shopify_metaobjects/
    client.py        # MetaobjectClient
    definition.py    # MetaobjectDefinitionSpec, MetaobjectFieldSpec
    metaobject.py    # Metaobject
    serialization.py # Mapeo Python type → Shopify field type
    mutations.py     # METAOBJECT_UPSERT, METAOBJECT_DEFINITION_CREATE
    queries.py       # METAOBJECT_BY_HANDLE, METAOBJECT_DEFINITION_BY_TYPE
    validation.py    # Validación pre-upsert
    exceptions.py    # MetaobjectError, DefinitionError, UpsertError
```

### Override de tipo Shopify en dataclass

```python
from dataclasses import dataclass, field

@dataclass
class ArticleTeaser:
    handle: str
    body: str = field(metadata={'shopify_type': 'rich_text_field'})
```

### Errores

- `DefinitionError` — fallo en fetch/create de definición; expone `.error_code` y `.user_errors`
- `UpsertError` — fallo en upsert; ídem

### Tests

```bash
python manage.py test metaobjects.shopify_metaobjects.tests
```

### Referencia completa

Ver [`docs/Documentation.txt`](docs/Documentation.txt).

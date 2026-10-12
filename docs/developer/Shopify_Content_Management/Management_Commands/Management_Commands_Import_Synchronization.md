# Comandos de Gestión de Importación y Sincronización

Este módulo contiene varios comandos de gestión de Django que facilitan la importación de contenido desde Shopify a Wagtail, la materialización de contenido editorial y la sincronización de enlaces semánticos y referencias nativas de Shopify. Estos comandos son esenciales para mantener la coherencia y la actualidad del contenido entre las plataformas Shopify y Wagtail.

## Comandos

### `backfill_shopify_native_references`

Este comando es responsable de rellenar los metacampos de referencia nativos de Shopify a partir de las filas de claves foráneas (FK) de enlaces semánticos tipados existentes. Asegura que las referencias internas dentro de Wagtail se reflejen correctamente como metacampos de referencia de lista en Shopify, lo que es crucial para la integración del escaparate.

**Propósito:** Sincronizar las referencias internas de las páginas de Wagtail (Productos, Colecciones, Artículos, Glosarios) con los metacampos de referencia nativos de Shopify.

**Uso:**

```bash
python manage.py backfill_shopify_native_references [--model {product,collection,article,glossary,all}] [--dry-run]
```

**Argumentos:**

*   `--model`: Especifica el tipo de página a rellenar (por defecto: `all`). Las opciones son `product`, `collection`, `article`, `glossary` o `all`.
*   `--dry-run`: Si se activa, informa de la cobertura sin poner en cola las tareas de sincronización, útil para previsualizar los cambios.

**Flujo de Proceso (`backfill_shopify_native_references`):**

```mermaid
graph TD
    A[Inicio Comando] --> B{Seleccionar Modelos de Página};
    B --> C{Iterar sobre Páginas Vivas};
    C --> D{Página tiene Enlaces Semánticos?};
    D -- No --> C;
    D -- Sí --> E{Serializar Referencias Nativas};
    E --> F{Referencias Resueltas?};
    F -- No --> G[Incrementar Contador Sin GIDs Resueltos];
    F -- Sí --> H[Incrementar Contador Con GIDs Resueltos];
    G --> I{Omitir Destinos Calculados?};
    H --> I;
    I --> J{Modo Dry-Run?};
    J -- Sí --> K[Saltar Encolado];
    J -- No --> L{Página Habilitada para Sincronización y con shopify_id (excepto Glosario)?};
    L -- No --> C;
    L -- Sí --> M[Encolar Sincronización de Página Saliente];
    M --> C;
    K --> C;
    C -- Fin Iteración --> N[Reportar Estadísticas];
```

**Componentes Clave:**

*   `shopify_content.models`: Modelos de Wagtail como `CollectionPage`, `GlossaryTermPage`, `ProductPage`, `ArticlePage`.
*   `shopify_content.models.semantic_links`: Funciones como `page_has_semantic_links` para verificar la existencia de enlaces semánticos.
*   `shopify_content.semantic_links.references`: `serialize_native_references` para convertir enlaces semánticos en referencias nativas de Shopify.
*   `shopify_content.sync.task_dispatch`: `enqueue_page_outbound_sync` para poner en cola las tareas de sincronización saliente.

### `import_shopify_blogs`

Importa todos los blogs y artículos de Shopify en instancias de `BlogPage` y `ArticlePage` de Wagtail, respectivamente.

**Propósito:** Sincronizar blogs y artículos desde Shopify a Wagtail.

**Uso:**

```bash
python manage.py import_shopify_blogs [--parent-page-id PAGE_ID]
```

**Argumentos:**

*   `--parent-page-id`: El ID de la página de Wagtail que se utilizará como padre para los blogs importados. Por defecto, utiliza el slug "blogs" de `ShopifyRootPage` (se crea automáticamente si no existe).

**Componentes Clave:**

*   `shopify_content.sync.inbound`: `import_blogs_and_articles` y `_get_shop` para la lógica de importación y la obtención de la tienda Shopify.
*   `shopify_content.sync.import_parents`: `resolve_shopify_import_parent` para determinar la página padre en Wagtail.
*   `shopify_content.models.ShopifyRootPage`: La página raíz de Shopify en Wagtail.

### `import_shopify_collections`

Importa todas las colecciones de Shopify en instancias de `CollectionPage` de Wagtail.

**Propósito:** Sincronizar colecciones desde Shopify a Wagtail.

**Uso:**

```bash
python manage.py import_shopify_collections [--parent-page-id PAGE_ID]
```

**Argumentos:**

*   `--parent-page-id`: El ID de la página de Wagtail que se utilizará como padre para las colecciones importadas. Por defecto, utiliza el slug "collections" de `ShopifyRootPage` (se crea automáticamente si no existe).

**Componentes Clave:** (Similar a `import_shopify_blogs`)

*   `shopify_content.sync.inbound`: `import_collections` y `_get_shop`.
*   `shopify_content.sync.import_parents`: `resolve_shopify_import_parent`.
*   `shopify_content.models.ShopifyRootPage`.

### `import_shopify_glossary`

Importa todos los metaobjetos de `glossary_term` de Shopify en instancias de `GlossaryTermPage` de Wagtail.

**Propósito:** Sincronizar términos de glosario desde Shopify a Wagtail.

**Uso:**

```bash
python manage.py import_shopify_glossary [--parent-page-id PAGE_ID] [--new-only]
```

**Argumentos:**

*   `--parent-page-id`: El ID de la página de Wagtail que se utilizará como padre para los términos de glosario importados. Por defecto, utiliza el slug "glossary" de `ShopifyRootPage`.
*   `--new-only`: Si se activa, solo se crearán términos que no existen en Wagtail; se omitirán las actualizaciones.

**Componentes Clave:** (Similar a `import_shopify_blogs`)

*   `shopify_content.sync.inbound`: `import_glossary_terms` y `_get_shop`.
*   `shopify_content.sync.import_parents`: `resolve_shopify_import_parent`.
*   `shopify_content.models.ShopifyRootPage`.

### `import_shopify_products`

Importa todos los productos de Shopify en instancias de `ProductPage` de Wagtail.

**Propósito:** Sincronizar productos desde Shopify a Wagtail.

**Uso:**

```bash
python manage.py import_shopify_products [--parent-page-id PAGE_ID]
```

**Argumentos:**

*   `--parent-page-id`: El ID de la página de Wagtail que se utilizará como padre para los productos importados. Por defecto, utiliza el slug "products" de `ShopifyRootPage` (se crea automáticamente si no existe).

**Componentes Clave:** (Similar a `import_shopify_blogs`)

*   `shopify_content.sync.inbound`: `import_products` y `_get_shop`.
*   `shopify_content.sync.import_parents`: `resolve_shopify_import_parent`.
*   `shopify_content.models.ShopifyRootPage`.

**Diagrama de Flujo General de Comandos de Importación:**

```mermaid
graph TD
    A[Inicio Comando de Importación] --> B{Obtener Tienda Shopify};
    B --> C{Resolver Página Padre en Wagtail};
    C --> D[Llamar Función de Importación (ej. import_blogs_and_articles)];
    D --> E[Procesar Datos de Shopify];
    E --> F{Crear/Actualizar Páginas en Wagtail};
    F --> G[Registrar Estadísticas];
    G --> H[Fin Comando];
```

### `materialize_article_markdown`

Este comando se utiliza para materializar el contenido del campo `body` de `ArticlePage` basado en `StreamField` en documentos Markdown nativos de Git (`body.md`). Esta es una migración operativa que preserva el HTML renderizado del escaparate tal cual, permitiendo una transición sin pérdidas hacia un control de autoridad basado en Git.

**Propósito:** Migrar el contenido de `StreamField` de `ArticlePage` a archivos Markdown en el repositorio de Git.

**Uso:**

```bash
python manage.py materialize_article_markdown [--locale LOCALE_CODE] [--force] [--dry-run]
```

**Argumentos:**

*   `--locale`: Materializa solo un código de idioma de Wagtail específico (ej. `en-US`).
*   `--force`: Sobrescribe archivos `body.md` existentes que difieran.
*   `--dry-run`: Informa las acciones sin escribir archivos.

**Componentes Clave:**

*   `shopify_content.content_store.accessors`: `get_repository` para interactuar con el repositorio de contenido.
*   `shopify_content.content_store.refs`: `ref_for`, `relative_path` para construir referencias a archivos de contenido.
*   `shopify_content.models.ArticlePage`.
*   `shopify_content.sync.outbound`: `_render_streamfield_html` para obtener el HTML renderizado del `StreamField`.

### `materialize_editorial_content`

Materializa campos editoriales migrados (definidos en `MIRRORED_FIELDS`) en el árbol de contenido de Git. Es una herramienta de migración controlada e idempotente, diseñada para sembrar el `worktree` autoritativo con contenido existente de la base de datos de Wagtail. El contenido se preserva literalmente (sin pérdidas), incluyendo el HTML existente dentro del cuerpo del archivo `.md`.

**Propósito:** Migrar contenido de campos editoriales específicos de Wagtail a archivos Markdown en el repositorio de Git.

**Uso:**

```bash
python manage.py materialize_editorial_content [--field FIELD] [--locale LOCALE_CODE] [--force] [--dry-run]
```

**Argumentos:**

*   `--field`: Materializa solo un campo editorial específico (por defecto: `all`). Las opciones se derivan de `MIRRORED_FIELDS`.
*   `--locale`: Filtra por un código de idioma de Wagtail específico (ej. `en-US`).
*   `--force`: Sobrescribe archivos existentes que difieran.
*   `--dry-run`: Informa las acciones sin escribir archivos.

**Componentes Clave:**

*   `shopify_content.content_store.accessors`: `MIRRORED_FIELDS`, `db_text`, `get_repository`.
*   `shopify_content.content_store.refs`: `ref_for`, `relative_path`.
*   Modelos de Wagtail relevantes (ej. `BlogPage`, `GlossaryTermPage`, `LocationPage`).

### `sync_semantic_links_revisions`

Sincroniza las filas de claves foráneas (FK) de enlaces semánticos tipados existentes en las revisiones de Wagtail. Esto es una solución para la visibilidad en la interfaz de administración de Wagtail, asegurando que los enlaces semánticos persistan en las revisiones de las páginas después de su creación inicial.

**Propósito:** Asegurar la visibilidad de los enlaces semánticos existentes en el editor de Wagtail guardándolos en las revisiones de las páginas.

**Uso:**

```bash
python manage.py sync_semantic_links_revisions [--model {article,product,collection,glossary,all}]
```

**Argumentos:**

*   `--model`: El tipo de página a sincronizar (por defecto: `all`). Las opciones son `article`, `product`, `collection`, `glossary` o `all`.

**Componentes Clave:**

*   `shopify_content.indexing`: `INDEX_MODELS`, `live_queryset_for` para obtener consultas de páginas vivas.
*   `shopify_content.models.semantic_links`: `page_has_semantic_links`.
*   `shopify_content.semantic_links.service`: `persist_semantic_links_revision` para guardar los enlaces en las revisiones de Wagtail.

**Diagrama de Flujo General de Comandos de Materialización/Sincronización:**

```mermaid
graph TD
    A[Inicio Comando Materializar/Sincronizar] --> B{Obtener Repositorio/Modelos de Wagtail};
    B --> C{Filtrar Páginas (por idioma, etc.)};
    C --> D{Iterar sobre Páginas};
    D --> E{Obtener Contenido/Referencias};
    E --> F{Verificar Existencia del Archivo/Revisión};
    F -- Existe y es Idéntico --> D;
    F -- Existe y Diverge (sin --force) --> D;
    F -- No Existe o Diverge (con --force) --> G{Escribir Archivo/Persistir Revisión};
    G --> D;
    D -- Fin Iteración --> H[Reportar Estadísticas];
```

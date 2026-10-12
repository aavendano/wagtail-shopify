# Módulo Shopify_API___Schemas_Article_Content

Este módulo define los esquemas de datos (schemas) para la representación de artículos de Shopify dentro del sistema, facilitando la validación de entrada, la actualización y la serialización de datos de salida para la API. Es una parte fundamental de la integración con Shopify para la gestión de contenido de artículos, permitiendo la interacción estructurada con los datos de artículos.

## Funcionalidad Principal

El módulo `Shopify_API___Schemas_Article_Content` se centra en tres componentes clave que actúan como contratos de datos para las operaciones CRUD (Crear, Leer, Actualizar, Borrar) de artículos: `ArticleIn`, `ArticleOut` y `ArticlePatch`.

### `ArticleIn`

Este esquema se utiliza para la creación de nuevos artículos. Define los campos requeridos y opcionales para la entrada de datos al crear un artículo en el sistema.

**Campos Clave:**

*   **`title` (str)**: Título del artículo, requerido.
*   **`blog_id` (int)**: ID de la página Wagtail del BlogPage padre, requerido.
*   **`shopify_id` (Optional[str])**: GID de Shopify para el artículo. Generalmente nulo en la creación.
*   **`handle` (Optional[str])**: Handle de URL de Shopify.
*   **`author` (Optional[str])**: Nombre completo del autor.
*   **`published_at` (Optional[datetime])**: Fecha y hora de publicación.
*   **`summary` (Optional[str])**: Resumen corto del artículo.
*   **`tags` (Optional[List[str]])**: Lista de etiquetas.
*   **`featured_image_id` (Optional[int])**: ID de la imagen destacada de Wagtail.
*   **`body` (Optional[List[Dict[str, Any]]])**: Contenido del cuerpo del artículo (StreamField heredado). Su uso depende del modo de autoridad de contenido (`CONTENT_STORE_MODE`).
*   **`seo_title` (Optional[str])**: Título SEO.
*   **`search_description` (Optional[str])**: Meta descripción SEO.
*   **`metafields` (Optional[List[MetafieldSchema]])**: Metafields de Shopify.
*   **`sync_enabled` (Optional[bool])**: Habilita/deshabilita la sincronización con Shopify.
*   **`available_locales` (Optional[List[str]])**: Códigos de localización de Wagtail donde el artículo está disponible.

### `ArticlePatch`

Este esquema se utiliza para la actualización parcial de artículos existentes. Todos sus campos son opcionales, permitiendo la modificación de atributos específicos sin afectar el resto.

**Campos Clave (todos opcionales):**

*   **`title` (Optional[str])**: Actualiza el título del artículo.
*   **`shopify_id` (Optional[str])**: Establece o actualiza el GID de Shopify.
*   **`handle` (Optional[str])**: Actualiza el handle de URL de Shopify.
*   **`author` (Optional[str])**: Actualiza el nombre completo del autor.
*   **`published_at` (Optional[datetime])**: Actualiza la fecha y hora de publicación.
*   **`summary` (Optional[str])**: Actualiza el resumen del artículo.
*   **`tags` (Optional[List[str]])**: Reemplaza la lista completa de etiquetas.
*   **`featured_image_id` (Optional[int])**: Actualiza la imagen destacada.
*   **`body` (Optional[List[Dict[str, Any]]])**: Reemplazo del StreamField heredado. Su uso depende del modo de autoridad de contenido.
*   **`seo_title` (Optional[str])**: Actualiza el título SEO.
*   **`search_description` (Optional[str])**: Actualiza la meta descripción SEO.
*   **`metafields` (Optional[List[MetafieldSchema]])**: Reemplaza todos los metafields.
*   **`sync_enabled` (Optional[bool])**: Habilita o deshabilita la sincronización.
*   **`publish` (bool)**: Si es `true`, publica la página después de guardar los cambios.
*   **`available_locales` (Optional[List[str]])**: Actualiza los códigos de localización de Wagtail.

### `ArticleOut`

Este esquema representa la salida de datos de un artículo, utilizado cuando se recupera un artículo a través de la API. Incluye todos los campos relevantes de un artículo, así como campos resueltos dinámicamente.

**Campos Clave:**

*   **`id` (int)**: ID de la página Wagtail.
*   **`shopify_id` (str)**: GID de Shopify para este artículo.
*   **`title` (str)**: Título del artículo.
*   **`handle` (str)**: Handle de URL de Shopify.
*   **`slug` (str)**: Slug de la página Wagtail (refleja el handle).
*   **`author` (str)**: Nombre completo del autor.
*   **`published_at` (Optional[datetime])**: Fecha y hora de publicación UTC.
*   **`summary` (str)**: Resumen corto del artículo.
*   **`tags` (List[str])**: Lista de etiquetas.
*   **`featured_image_id` (Optional[int])**: ID de la imagen destacada de Wagtail.
*   **`featured_image_url` (str)**: URL absoluta de la imagen destacada de Shopify.
*   **`featured_image_alt` (str)**: Texto alternativo para la imagen destacada.
*   **`body` (List[Dict[str, Any]])**: Estado de retroceso del StreamField heredado.
*   **`seo_title` (str)**: Título SEO.
*   **`search_description` (str)**: Meta descripción SEO.
*   **`metafields` (List[Dict[str, Any]])**: Metafields de Shopify adjuntos.
*   **`related_links` (List[RelatedLinkSchema])**: Enlaces internos semánticos.
*   **`sync_enabled` (bool)**: Indica si la sincronización con Shopify está habilitada.
*   **`last_synced_at` (Optional[datetime])**: Marca de tiempo UTC de la última sincronización exitosa.
*   **`live` (bool)**: `True` si la página está publicada en Wagtail.
*   **`locale` (str)**: Código de localización de Wagtail.
*   **`url` (Optional[str])**: URL pública completa de la página.
*   **`first_published_at` (Optional[datetime])**: Marca de tiempo UTC de la primera publicación.
*   **`last_published_at` (Optional[datetime])**: Marca de tiempo UTC de la publicación más reciente.
*   **`blog_id` (Optional[int])**: ID de la página Wagtail del BlogPage padre.
*   **`blog_title` (Optional[str])**: Título del BlogPage padre.
*   **`available_locales` (List[str])**: Códigos de localización de Wagtail donde el artículo está disponible.

Este esquema incluye varios métodos estáticos `resolve_` para poblar campos a partir de un objeto Wagtail (probablemente `ArticlePage`), como `resolve_available_locales`, `resolve_translation_page_ids`, `resolve_tags`, `resolve_body`, `resolve_metafields`, `resolve_related_links`, `resolve_featured_image_id`, `resolve_locale`, `resolve_url`, `resolve_blog_id`, y `resolve_blog_title`.

## Arquitectura y Relaciones entre Componentes

Los esquemas de artículos se integran dentro de la arquitectura de la API de Shopify y el sistema de gestión de contenido Wagtail.

### Diagrama de Clases de Esquemas de Artículos

\`\`\`mermaid
classDiagram
    direction LR
    class Schema {
        # ...
    }
    class LocaleCreateFields {
        + str locale
        + List~str~ translation_page_ids
    }
    class LocalePatchFields {
        + str locale
        + List~str~ translation_page_ids
    }
    class LocaleOutFields {
        + str locale
        + List~str~ translation_page_ids
    }
    class StorefrontUrlOutFields {
        + Optional~str~ storefront_url
        + Optional~str~ preview_url
    }
    class MetafieldSchema {
        + str namespace
        + str key
        + str type
        + Any value
    }
    class RelatedLinkSchema {
        + str type
        + str title
        + str url
    }

    ArticleIn --|> LocaleCreateFields
    ArticleIn : + str title
    ArticleIn : + int blog_id
    ArticleIn : + Optional~str~ shopify_id
    ArticleIn : + Optional~str~ handle
    ArticleIn : + Optional~List~Dict~str, Any~~ body
    ArticleIn : + Optional~List~MetafieldSchema~ metafields
    ArticleIn : + Optional~List~str~ available_locales

    ArticlePatch --|> LocalePatchFields
    ArticlePatch : + Optional~str~ title
    ArticlePatch : + Optional~str~ shopify_id
    ArticlePatch : + Optional~str~ handle
    ArticlePatch : + Optional~List~Dict~str, Any~~ body
    ArticlePatch : + Optional~List~MetafieldSchema~ metafields
    ArticlePatch : + bool publish
    ArticlePatch : + Optional~List~str~ available_locales

    ArticleOut --|> StorefrontUrlOutFields
    ArticleOut --|> LocaleOutFields
    ArticleOut : + int id
    ArticleOut : + str shopify_id
    ArticleOut : + str title
    ArticleOut : + str handle
    ArticleOut : + str slug
    ArticleOut : + Optional~datetime~ published_at
    ArticleOut : + List~str~ tags
    ArticleOut : + List~Dict~str, Any~~ body
    ArticleOut : + List~Dict~str, Any~~ metafields
    ArticleOut : + List~RelatedLinkSchema~ related_links
    ArticleOut : + bool sync_enabled
    ArticleOut : + bool live
    ArticleOut : + List~str~ available_locales

    MetafieldSchema .. ArticleIn
    MetafieldSchema .. ArticlePatch
    RelatedLinkSchema .. ArticleOut
\`\`\`

### Diagrama de Flujo de Datos para la Gestión de Artículos

\`\`\`mermaid
graph TD
    subgraph Cliente API
        A[Solicitud de Creación/Actualización] --> B{Datos ArticleIn/ArticlePatch}
        C{Solicitud de Lectura} --> D[Respuesta ArticleOut]
    end

    subgraph Módulo Shopify_API___Schemas_Article_Content
        B --> |Validación| E(Esquemas ArticleIn/ArticlePatch)
        E --> |Serialización/Deserialización| F[Servicio de Artículos/ORM]
        F --> |Datos del Artículo| G(Esquema ArticleOut)
        G --> |Serialización| D
    end

    subgraph Base de Datos / Wagtail
        F <--> H[Modelos Wagtail (e.g., ArticlePage)]
        H <--> I[Almacén de Contenido (Git/DB)]
    end

    subgraph Shopify
        F <--> J[API de Shopify]
    end

    E -- "Hereda campos de" --> K[Esquemas Comunes (LocaleCreateFields, LocalePatchFields)]
    G -- "Hereda campos de" --> L[Esquemas Comunes (StorefrontUrlOutFields, LocaleOutFields)]
    F -- "Utiliza" --> M[Serialización de Enlaces Semánticos]
    F -- "Utiliza" --> N[Utilidades de Localización]

    click H "Shopify_Content_Management/Shopify_Content_Models.md" "Ver Modelos Wagtail"
    click K "Shopify_API___Schemas/Shopify_API___Schemas_Common_Data_Models.md" "Ver Esquemas Comunes"
    click L "Shopify_API___Schemas/Shopify_API___Schemas_Common_Data_Models.md" "Ver Esquemas Comunes"
\`\`\`

## Integración en el Sistema General

Este módulo se integra con varias partes del sistema para proporcionar una gestión completa de los artículos de Shopify:

*   **API de Shopify:** Los esquemas `ArticleIn`, `ArticleOut` y `ArticlePatch` son fundamentales para la comunicación con la API de Shopify. Permiten que la aplicación envíe y reciba datos de artículos en un formato estandarizado. El campo `shopify_id` en estos esquemas es la clave para vincular los artículos de Wagtail con sus contrapartes en Shopify.

*   **[Shopify_Content_Management](../Shopify_Content_Management.md):** Los esquemas de artículos interactúan estrechamente con el módulo `shopify_content`. Específicamente, se espera que `ArticleOut` serialice datos de modelos Wagtail como `ArticlePage` (definido en [Shopify_Content_Management/Shopify_Content_Models.md](../Shopify_Content_Management/Shopify_Content_Models.md)). La lógica de sincronización (`sync_enabled`, `last_synced_at`) y la gestión del cuerpo del artículo (que puede ser un StreamField o un archivo Markdown en modo `git_authoritative`) son manejadas por el módulo de gestión de contenido.

*   **[Shopify_API___Schemas_Common_Data_Models](Shopify_API___Schemas_Common_Data_Models.md):** Los esquemas de artículos heredan y utilizan componentes de este módulo, como `LocaleCreateFields`, `LocalePatchFields`, `LocaleOutFields`, `StorefrontUrlOutFields`, `MetafieldSchema` y `RelatedLinkSchema`. Esto asegura la coherencia y la reutilización de la estructura de datos en toda la API de Shopify.

*   **Gestión de Localización:** Los campos `locale` y `available_locales` en los esquemas `ArticleIn`, `ArticlePatch` y `ArticleOut` son cruciales para soportar contenido multilingüe. El sistema puede manejar la disponibilidad de artículos en diferentes configuraciones regionales (ej. `en-US`, `es-US`).

*   **SEO y Metadatos:** Los campos `seo_title`, `search_description` y `metafields` permiten la gestión de información de SEO y metadatos personalizados para los artículos, que se sincronizan con Shopify.

En resumen, `Shopify_API___Schemas_Article_Content` actúa como la capa de interfaz de datos para la gestión de artículos, asegurando que los datos sean validados y estructurados correctamente para la interacción entre la API, Wagtail y Shopify.

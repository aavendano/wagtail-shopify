# Modelos de Contenido del Glosario

El módulo `Glossary_Content_Models` define los modelos de contenido de Wagtail para gestionar términos de glosario. Estos modelos están diseñados para sincronizarse con los metaobjetos de Shopify, permitiendo una gestión unificada del contenido del glosario.

## Propósito y Funcionalidad Principal

El componente central de este módulo es `GlossaryTermPage`, una página de Wagtail que representa un término de glosario individual. Su objetivo principal es:

1.  **Gestión de Contenido:** Proporcionar una interfaz en Wagtail para que los editores creen, editen y organicen términos de glosario, incluyendo su definición, imágenes, enlaces relacionados y sinónimos.
2.  **Sincronización con Shopify:** Facilitar la sincronización bidireccional de los términos del glosario con metaobjetos (`glossary_term`) en la plataforma Shopify, asegurando que el contenido esté disponible para los temas y la API de Shopify.
3.  **Capacidades SEO:** Ofrecer campos y métodos para optimizar los términos del glosario para motores de búsqueda, controlando el título SEO y la descripción de búsqueda.
4.  **Localización:** Permitir la especificación del código de configuración regional para cada término del glosario, lo que respalda el contenido multilingüe.

## Arquitectura y Relaciones de Componentes

El módulo `Glossary_Content_Models` se integra estrechamente con el marco de Wagtail y el sistema de gestión de contenido de Shopify. El componente principal, `GlossaryTermPage`, hereda funcionalidades clave y se relaciona con varios otros módulos:

### `GlossaryTermPage`

`GlossaryTermPage` es una clase de modelo de Django y Wagtail que representa un único término de glosario.

*   **Herencia:**
    *   `wagtail.models.Page`: Proporciona la estructura fundamental de la página en el CMS de Wagtail.
    *   `shopify_content.content_store.domain.EditorialMixin`: Aporta funcionalidades relacionadas con el contenido editorial y su gestión.

*   **Campos Clave:**
    *   `shopify_id`: Identificador GID del metaobjeto de Shopify (para sincronización).
    *   `handle`: Identificador de Shopify (por defecto, el slug del término).
    *   `sync_enabled`: Bandera para habilitar/deshabilitar la sincronización con Shopify.
    *   `term`: El término del glosario en sí.
    *   `definition`: Campo de texto enriquecido para la definición del término.
    *   `image`, `image_alt_text`, `image_url`, `shopify_image_id`: Campos para la gestión de imágenes asociadas al término, con un enfoque en la propiedad de Shopify para los medios.
    *   `locale_code`: Código de la configuración regional del término.
    *   `related_links`, `external_links`, `synonyms`, `same_as`: Campos JSON para almacenar enlaces internos, enlaces externos, sinónimos y URLs canónicas.

*   **Paneles de Administración (Wagtail):**
    *   `content_panels`: Incluye campos como `term`, `definition`, `image`, `locale_code`, `external_links`, `synonyms`, `same_as` y paneles de enlaces semánticos (`semantic_links_panels`).
    *   `promote_panels`: Incluye campos SEO (`SHOPIFY_SEO_PANELS`) y el `slug` de la página.
    *   `settings_panels`: Incluye configuraciones de sincronización con Shopify (`SHOPIFY_SYNC_PANELS`).

*   **Métodos Personalizados:**
    *   `save()`: Sobrescribe el método `save` para establecer automáticamente el `title` de la página basándose en el `term`, derivar el `locale_code` de la configuración regional de Wagtail y asegurar que los campos JSON se inicialicen como listas vacías si son `None`.
    *   `get_seo_title()`: Devuelve el título SEO o el término/título de la página.
    *   `get_seo_description()`: Devuelve la descripción de búsqueda, o una versión de texto plano de la definición.

### Relaciones con otros Módulos

*   **[Content_Base_Models___Mixins](Content_Base_Models___Mixins.md):** `GlossaryTermPage` hereda de `ShopifyRootPage` como su tipo de página padre y utiliza `FAQItem` y `ShopifyMetafield` a través de los mixins `SHOPIFY_SEO_PANELS` y `SHOPIFY_SYNC_PANELS`.
*   **[Content_Forms](Content_Forms.md):** Utiliza `GlossaryTermPageForm` para la validación y presentación de formularios en el administrador de Wagtail.
*   **[Admin___Wagtail_UI_Integration](Admin___Wagtail_UI_Integration.md):** Integra los paneles de administración (`semantic_links_panels`, `SHOPIFY_SEO_PANELS`, `SHOPIFY_SYNC_PANELS`) para la interfaz de usuario de Wagtail.
*   **[Content_Export_Configuration](Content_Export_Configuration.md):** El `GlossaryIndexConsumer` se encarga de la configuración de exportación para los índices del glosario.
*   **[Metaobject_Definition___Setup_Commands](Metaobject_Definition___Setup_Commands.md):** El comando `ensure_metaobject_definitions` es crucial para inicializar la definición de metaobjetos de `glossary_term` en Shopify, que luego `GlossaryTermPage` utilizará para la sincronización.
*   **[Content_Import___Materialization_Commands](Content_Import___Materialization_Commands.md):** El comando `import_shopify_glossary` se utiliza para importar términos de glosario existentes de Shopify.
*   **[Content_Indexing___Semantic_Link_Commands](Content_Indexing___Semantic_Link_Commands.md):** Comandos como `rebuild_glossary_index` son relevantes para mantener el índice de búsqueda del glosario.
*   **Shopify Content API:** La API (`api/schemas/glossary.py`) proporciona esquemas para la entrada y salida de datos de los términos del glosario, permitiendo la interacción programática con estos recursos.

### Diagrama de Clases

\`\`\`mermaid
classDiagram
    direction LR
    class Page {
        +title: str
        +slug: str
        +search_description: str
        +locale_id: int
    }
    class EditorialMixin {
        +editorial_content: RichTextField
    }
    class GlossaryTermPage {
        +shopify_id: str
        +handle: str
        +sync_enabled: bool
        +last_synced_at: datetime
        +term: str
        +definition: RichTextField
        +image: ForeignKey(Image)
        +image_alt_text: str
        +image_url: URLField
        +shopify_image_id: str
        +locale_code: str
        +related_links: JSONField
        +external_links: JSONField
        +synonyms: JSONField
        +same_as: JSONField
        +save()
        +get_seo_title() str
        +get_seo_description() str
    }
    class GlossaryTermPageForm
    class ShopifyRootPage

    Page <|-- GlossaryTermPage
    EditorialMixin <|-- GlossaryTermPage
    GlossaryTermPage ..> GlossaryTermPageForm : utiliza
    GlossaryTermPage ..> ShopifyRootPage : parent_page_types
    GlossaryTermPage ..> wagtailimages.Image : ForeignKey
    GlossaryTermPage ..> shopify_content.admin_panels.semantic_links_panels
    GlossaryTermPage ..> shopify_content.models.mixins.SHOPIFY_SEO_PANELS
    GlossaryTermPage ..> shopify_content.models.mixins.SHOPIFY_SYNC_PANELS
    GlossaryTermPage ..> shopify_content.glossary_locale_utils.glossary_locale_code_for_wagtail
\`\`\`

### Diagrama de Componentes

\`\`\`mermaid
componentDiagram
    [CMS Wagtail] --> [Glossary_Content_Models] : Gestiona
    [Glossary_Content_Models] --> [Content_Base_Models___Mixins] : Hereda/Usa
    [Glossary_Content_Models] --> [Content_Forms] : Usa
    [Glossary_Content_Models] --> [Admin___Wagtail_UI_Integration] : Integra Paneles
    [Glossary_Content_Models] --> [Shopify API] : Sincronización Metaobjetos
    [Glossary_Content_Models] --> [Shopify CDN] : Almacenamiento Imágenes
    [Glossary_Content_Models] --> [Content_Export_Configuration] : Define Exportación
    [Glossary_Content_Models] --> [Metaobject_Definition___Setup_Commands] : Requiere Configuración
    [Glossary_Content_Models] --> [Content_Import___Materialization_Commands] : Importa Datos
    [Glossary_Content_Models] --> [Content_Indexing___Semantic_Link_Commands] : Indexación
    [Shopify Content API] <-- [Glossary_Content_Models] : Expone Esquemas
\`\`\`

## Encaje en el Sistema General

El módulo `Glossary_Content_Models` es un componente vital dentro de la arquitectura más amplia de gestión de contenido de Wagtail para Shopify.

*   **Integración de Contenido:** Permite que los términos del glosario se gestionen como páginas de Wagtail, aprovechando las capacidades del CMS para la edición y organización, mientras que los datos residen en Shopify como metaobjetos. Esto desacopla la presentación del contenido de su almacenamiento, permitiendo flexibilidad en el front-end de Shopify.
*   **Experiencia del Usuario Final:** Los términos del glosario creados y sincronizados a través de este módulo son consumidos por el front-end de Shopify (a través de temas que acceden a los metaobjetos) y potencialmente por otras aplicaciones a través de la API.
*   **Flujo de Datos:** El contenido se crea o actualiza en Wagtail, luego se sincroniza con Shopify. Shopify es la fuente de verdad para los medios asociados (imágenes) y sus identificadores. Los procesos de importación y exportación gestionan el movimiento inicial y masivo de datos.
*   **Comandos de Gestión:** Varios comandos de `manage.py` de la sección [Metaobject_Definition___Setup_Commands](Metaobject_Definition___Setup_Commands.md) y [Content_Import___Materialization_Commands](Content_Import___Materialization_Commands.md) orquestan la configuración inicial de las definiciones de metaobjetos de Shopify y la importación/exportación de términos de glosario.
*   **API:** Los esquemas definidos en `api/schemas/glossary.py` permiten a otros servicios o interfaces de usuario interactuar con los datos del glosario de manera programática, facilitando la integración con sistemas externos o herramientas personalizadas.

### Diagrama de Flujo de Datos del Glosario

\`\`\`mermaid
graph TD
    subgraph Wagtail CMS
        A[Editor Wagtail] --> B(Crear/Editar GlossaryTermPage)
        B --> C{Guardar Página}
        C --> D[Modelo GlossaryTermPage]
    end

    subgraph Procesos de Sincronización
        D -- Sincronización Automática/Manual --> E(Servicio de Sincronización de Shopify)
        E -- bootstrap_metaobject_definitions --> F[Definiciones de Metaobjetos Shopify]
        E -- Upsert --> G[Metaobjeto 'glossary_term' en Shopify]
    end

    subgraph Shopify Storefront/API
        G -- Consumido por --> H[Tema de Shopify]
        G -- Acceso API --> I[Shopify Content API]
        I -- Datos de Glosario --> J[Aplicaciones Externas/Front-end]
    end

    subgraph Comandos de Gestión
        K[Comandos Django (p.ej., import_shopify_glossary)] --> D
        K --> G
    end

    D -- Actualiza índice de búsqueda --> L[Índice de Búsqueda de Wagtail]

    style A fill:#bbf,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style C fill:#bbf,stroke:#333,stroke-width:2px
    style D fill:#bbf,stroke:#333,stroke-width:2px
    style E fill:#f9f,stroke:#333,stroke-width:2px
    style F fill:#9cf,stroke:#333,stroke-width:2px
    style G fill:#9cf,stroke:#333,stroke-width:2px
    style H fill:#f66,stroke:#333,stroke-width:2px
    style I fill:#f66,stroke:#333,stroke-width:2px
    style J fill:#f66,stroke:#333,stroke-width:2px
    style K fill:#bbf,stroke:#333,stroke-width:2px
    style L fill:#bbf,stroke:#333,stroke-width:2px
\`\`\`

# Migración de Base de Datos 0010: Puesta al Día del Esquema

Esta documentación detalla la migración de base de datos `0010_catch_up_schema.py`, un componente esencial dentro del módulo `Shopify Content Management`. Esta migración introduce cambios significativos en el esquema de la base de datos para soportar nuevas funcionalidades, mejorar la internacionalización, la gestión de contenido y la integración con Shopify.

## Propósito y Funcionalidad Principal

La migración `0010_catch_up_schema.py` tiene como objetivo principal actualizar el esquema de la base de datos para habilitar características avanzadas dentro del sistema de gestión de contenido Wagtail y su integración con Shopify. Las funcionalidades clave introducidas o modificadas incluyen:

*   **Gestión de Comandos Embebidos:** Creación de un modelo `EmbeddedCommandRun` para rastrear la ejecución de comandos asíncronos dentro del sistema.
*   **Soporte de Localizaciones (i18n):** Adición de campos `available_locales` a `ArticlePage` y `BlogPage` para especificar las configuraciones regionales donde se publica el contenido en la tienda.
*   **Configuración Temática de Shopify:** Introducción de campos `theme_config` en `CollectionPage` y `ProductPage` para permitir anulaciones de configuración de la tienda Shopify que se sincronizan como metafields.
*   **Enriquecimiento del Contenido de Wagtail:** Modificación del `StreamField` `body` de `ArticlePage` para incluir nuevos tipos de bloques de contenido.
*   **Habilitación de Sincronización por Defecto:** Establecimiento del valor por defecto `True` para el campo `sync_enabled` en varias páginas (`ArticlePage`, `BlogPage`, `CollectionPage`, `LocationPage`, `ProductPage`).
*   **Indexación y Resolución de URLs de Contenido:** Creación del modelo `ContentUrlIndex` para mapear rutas de la tienda a páginas de Wagtail, facilitando la gestión de URLs y la localización.
*   **Nuevos Tipos de Página Wagtail:** Introducción de `GlossaryTermPage` y `HomePage` para la gestión de términos de glosario y el contenido de la página de inicio, respectivamente.
*   **Gestión de Enlaces Semánticos:** Establecimiento de una infraestructura robusta para gestionar enlaces relacionados entre diferentes tipos de contenido (artículos, colecciones, términos de glosario, productos) a través de varios modelos `*Related*Link`.

## Arquitectura y Relaciones entre Componentes

Esta migración afecta y extiende varios modelos clave dentro del ecosistema de gestión de contenido de Shopify. A continuación, se detalla la arquitectura de los nuevos componentes y sus relaciones con los existentes.

### `EmbeddedCommandRun`

Este nuevo modelo está diseñado para monitorear y registrar el estado de los comandos asíncronos o procesos de larga duración que se ejecutan en el sistema.

\`\`\`mermaid
graph TD
    A[Sistema de Gestión de Contenido Wagtail] --> B(Ejecución de Comando Asíncrono);
    B --> C[Modelo EmbeddedCommandRun];
    C -- Registra Estado --> D{Base de Datos};
    C -- Contiene: command_id, status, message, stdout, stderr --> D;
\`\`\`

### Campos de Localización y Configuración Temática

Los campos `available_locales` y `theme_config` se añaden a modelos de contenido existentes, mejorando su integración con las capacidades de internacionalización y personalización de temas de Shopify.

\`\`\`mermaid
graph TD
    subgraph Modelos de Contenido Shopify
        AP(ArticlePage)
        BP(BlogPage)
        CP(CollectionPage)
        PP(ProductPage)
    end

    AP -- JSONField --> AL[available_locales];
    BP -- JSONField --> AL;

    CP -- JSONField --> TC[theme_config];
    PP -- JSONField --> TC;

    TC -- Esquema: Metafields Shopify --> S[Shopify Storefront];
    AL -- Códigos de Locale Wagtail --> S;
\`\`\`

### `ContentUrlIndex`

Este modelo es fundamental para la resolución de URLs y la gestión de contenido localizado, sirviendo como un índice para las rutas de la tienda.

\`\`\`mermaid
graph TD
    WagtailPage[wagtailcore.Page] --> CUI[ContentUrlIndex];
    CUI -- mapea: normalized_path, content_type, handle, locale, locale_prefix --> Tienda[Shopify Storefront];
    CUI -- Restricción Única --> UP[uniq_content_url_index_path_prefix];
\`\`\`

### Nuevos Tipos de Página: `GlossaryTermPage` y `HomePage`

Estos modelos extienden las capacidades de Wagtail para gestionar contenido específico como términos de glosario y la estructura de la página de inicio.

\`\`\`mermaid
graph TD
    WagtailCorePage[wagtailcore.Page] --> GTP[GlossaryTermPage];
    WagtailCorePage --> HP[HomePage];

    GTP -- Incluye: term, definition, image, locale_code, related_links, external_links, synonyms, same_as --> D[Base de Datos];
    HP -- Incluye: shopify_locale, hero_eyebrow, hero_heading, body (StreamField), sections_json --> D;

    GTP -- EditorialMixin --> EM[shopify_content.content_store.domain.EditorialMixin];
\`\`\`

### Modelos de Enlaces Relacionados

Una serie de nuevos modelos de "enlaces relacionados" (`*Related*Link`) se introducen para definir relaciones semánticas entre diferentes tipos de contenido. Esto permite la autogeneración de enlaces y mejora la navegación contextual.

\`\`\`mermaid
graph TD
    subgraph Páginas de Contenido
        ArticlePage
        CollectionPage
        GlossaryTermPage
        ProductPage
        WagtailPage[wagtailcore.Page]
    end

    ArticlePage -- tiene muchos --> ARAL[ArticleRelatedArticleLink];
    ArticlePage -- tiene muchos --> ARCL[ArticleRelatedCollectionLink];
    ArticlePage -- tiene muchos --> ARGTL[ArticleRelatedGlossaryTermLink];
    ArticlePage -- tiene muchos --> ARPL[ArticleRelatedProductLink];

    CollectionPage -- tiene muchos --> CRAL[CollectionRelatedArticleLink];
    CollectionPage -- tiene muchos --> CRCL[CollectionRelatedCollectionLink];
    CollectionPage -- tiene muchos --> CRGTL[CollectionRelatedGlossaryTermLink];
    CollectionPage -- tiene muchos --> CRPL[CollectionRelatedProductLink];

    GlossaryTermPage -- tiene muchos --> GTRAL[GlossaryTermRelatedArticleLink];
    GlossaryTermPage -- tiene muchos --> GTRCL[GlossaryTermRelatedCollectionLink];
    GlossaryTermPage -- tiene muchos --> GTRGTL[GlossaryTermRelatedGlossaryTermLink];
    GlossaryTermPage -- tiene muchos --> GTRPL[GlossaryTermRelatedProductLink];

    ProductPage -- tiene muchos --> PRAL[ProductRelatedArticleLink];
    ProductPage -- tiene muchos --> PRCL[ProductRelatedCollectionLink];
    ProductPage -- tiene muchos --> PRGTL[ProductRelatedGlossaryTermLink];
    ProductPage -- tiene muchos --> PRPL[ProductRelatedProductLink];

    ARAL -- ForeignKey --> WagtailPage;
    ARCL -- ForeignKey --> WagtailPage;
    ARGTL -- ForeignKey --> WagtailPage;
    ARPL -- ForeignKey --> WagtailPage;
    CRAL -- ForeignKey --> WagtailPage;
    CRCL -- ForeignKey --> WagtailPage;
    CRGTL -- ForeignKey --> WagtailPage;
    CRPL -- ForeignKey --> WagtailPage;
    GTRAL -- ForeignKey --> WagtailPage;
    GTRCL -- ForeignKey --> WagtailPage;
    GTRGTL -- ForeignKey --> WagtailPage;
    GTRPL -- ForeignKey --> WagtailPage;
    PRAL -- ForeignKey --> WagtailPage;
    PRCL -- ForeignKey --> WagtailPage;
    PRGTL -- ForeignKey --> WagtailPage;
    PRPL -- ForeignKey --> WagtailPage;

    style ARAL fill:#f9f,stroke:#333,stroke-width:2px
    style ARCL fill:#f9f,stroke:#333,stroke-width:2px
    style ARGTL fill:#f9f,stroke:#333,stroke-width:2px
    style ARPL fill:#f9f,stroke:#333,stroke-width:2px
    style CRAL fill:#f9f,stroke:#333,stroke-width:2px
    style CRCL fill:#f9f,stroke:#333,stroke-width:2px
    style CRGTL fill:#f9f,stroke:#333,stroke-width:2px
    style CRPL fill:#f9f,stroke:#333,stroke-width:2px
    style GTRAL fill:#f9f,stroke:#333,stroke-width:2px
    style GTRCL fill:#f9f,stroke:#333,stroke-width:2px
    style GTRGTL fill:#f9f,stroke:#333,stroke-width:2px
    style GTRPL fill:#f9f,stroke:#333,stroke-width:2px
    style PRAL fill:#f9f,stroke:#333,stroke-width:2px
    style PRCL fill:#f9f,stroke:#333,stroke-width:2px
    style PRGTL fill:#f9f,stroke:#333,stroke-width:2px
    style PRPL fill:#f9f,stroke:#333,stroke-width:2px
\`\`\`

## Cómo se integra el Módulo en el Sistema General

La migración `0010_catch_up_schema` es fundamental para la evolución del sistema de gestión de contenido.

1.  **Soporte de Contenido Multilingüe y Multimercado:** Los campos `available_locales` en `ArticlePage` y `BlogPage`, junto con `shopify_locale` en `HomePage`, son clave para la estrategia de internacionalización del sistema. Esto permite que el contenido sea adaptado y publicado para diferentes mercados y lenguajes en Shopify, en línea con el componente [Home Page Locale Validation](../Home_Page_Locale_Validation.md).

2.  **Sincronización Avanzada con Shopify:** La introducción de `theme_config` en `CollectionPage` y `ProductPage` proporciona un mecanismo para que los administradores de contenido definan y sincronicen configuraciones específicas del tema directamente desde Wagtail a Shopify, utilizando metafields. Esto se alinea con los servicios de sincronización de contenido descritos en [Content Synchronization Services](../Content_Synchronization_Services.md).

3.  **Gestión Centralizada de URLs:** El modelo `ContentUrlIndex` centraliza la gestión de las URLs del contenido, lo cual es vital para el SEO y la correcta navegación en la tienda Shopify. Trabaja en conjunto con el módulo [Content URL & Link Management](../Content_URL___Link_Management.md).

4.  **Extensión de Capacidades de Contenido:** La adición de `GlossaryTermPage` y `HomePage` como tipos de página de Wagtail enriquece las herramientas de los editores para crear y administrar una gama más amplia de contenido directamente en Wagtail, integrándose con [Glossary Content Models](../Glossary_Content_Models.md) y [Home Page Models](../Home_Page_Models.md).

5.  **Contenido Interconectado (Enlaces Semánticos):** La creación de numerosos modelos de `*Related*Link` permite al sistema construir una red de contenido semánticamente relacionada, lo cual puede ser utilizado para recomendaciones, navegación contextual y mejoras de SEO. Esto potencia las características de [Content URL & Link Management](../Content_URL___Link_Management.md).

6.  **Automatización y Monitoreo de Tareas:** El modelo `EmbeddedCommandRun` sienta las bases para la ejecución y el seguimiento de comandos asíncronos, que son esenciales para operaciones como la importación de datos, la sincronización en segundo plano y las tareas de mantenimiento. Este componente es esencial para la robustez de los procesos de [Content Synchronization Services](../Content_Synchronization_Services.md) y [Embedded Commands Registry](../Embedded_Commands_Registry.md).

En resumen, esta migración consolida y expande la integración entre Wagtail y Shopify, habilitando un sistema de gestión de contenido más potente, flexible y adaptado a las necesidades de un entorno de comercio electrónico moderno y globalizado.

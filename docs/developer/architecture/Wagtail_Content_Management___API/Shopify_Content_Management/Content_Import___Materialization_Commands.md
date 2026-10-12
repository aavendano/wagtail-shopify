# Comandos de Importación y Materialización de Contenido

Este módulo (`Content_Import___Materialization_Commands`) es una parte fundamental del sistema de gestión de contenido de Wagtail, enfocado en la interacción con Shopify. Su propósito principal es gestionar la importación de diversos tipos de contenido desde Shopify hacia Wagtail y la materialización de contenido editorial existente en un formato compatible con Git.

## Propósito y Funcionalidad Principal

El módulo facilita la sincronización de contenido entre Shopify y Wagtail, permitiendo:
*   Importar blogs, artículos, colecciones, productos y términos de glosario desde Shopify.
*   Materializar el contenido de `StreamField` de Wagtail y campos editoriales específicos en archivos Markdown, sentando las bases para una gestión de contenido autoritativa basada en Git.

Estos comandos están diseñados para ser ejecutados manualmente o a través de tareas programadas para mantener la coherencia del contenido entre las dos plataformas.

## Arquitectura

El módulo `Content_Import___Materialization_Commands` se compone principalmente de una serie de comandos de gestión de Django, cada uno con una responsabilidad específica para la importación o materialización de contenido. Estos comandos interactúan con los servicios de sincronización (`shopify_content.sync.inbound`, `shopify_content.sync.outbound`), el repositorio de contenido (`shopify_content.content_store`), y los modelos de Wagtail para manipular el contenido.

```mermaid
graph TD
    A[Comandos de Importación y Materialización] --> B{Comandos de Gestión Django};
    B --> C[Importar Blogs y Artículos];
    B --> D[Importar Colecciones];
    B --> E[Importar Productos];
    B --> F[Importar Términos de Glosario];
    B --> G[Materializar Markdown de Artículos];
    B --> H[Materializar Contenido Editorial];

    C --> I[Servicios de Sincronización (Inbound)];
    D --> I;
    E --> I;
    F --> I;
    G --> J[Servicios de Sincronización (Outbound)];
    H --> K[Repositorio de Contenido (Git)];

    I --> L[Modelos de Contenido de Wagtail];
    J --> L;
    K --> L;
```

## Sub-módulos

A continuación, se describen los sub-módulos y sus funcionalidades:

*   **[Comandos de Importación de Contenido Shopify](Content_Import___Materialization_Commands/Content_Import___Materialization_Commands_comandos_importacion.md)**: Encargado de importar diversos tipos de contenido desde Shopify a Wagtail.
*   **[Comandos de Materialización de Contenido Editorial](Content_Import___Materialization_Commands/Content_Import___Materialization_Commands_comandos_materializacion.md)**: Responsable de transformar el contenido de Wagtail a un formato de archivo Git-nativo.

## Relación con otros Módulos

Este módulo depende en gran medida de los siguientes módulos dentro del sistema Wagtail Content Management & API:

*   **[Modelos Base de Contenido y Mixins](Content_Base_Models___Mixins.md)**: Define las estructuras de datos fundamentales para el contenido de Wagtail, como `ShopifyRootPage`, `FAQItem`, `ShopifyMetafield`, `ContentIndex`, `ContentUrlIndex`, `SemanticPageLink` y `ShopifySyncRun`.
*   **[Servicios de Sincronización de Contenido](Content_Synchronization_Services.md)**: Proporciona la lógica central para la importación y sincronización de contenido desde Shopify, incluyendo la definición de meta-campos y el orquestador de importación.
*   **[Almacén de Contenido y Lógica Editorial](Content_Store___Editorial_Logic.md)**: Gestiona el almacenamiento y acceso al contenido editorial, incluyendo el repositorio de archivos, contratos, lógica de dominio y procesamiento de Markdown.
*   **[Modelos de Contenido de Blog](Blog_Content_Models.md)**: Define los modelos específicos para blogs y artículos en Wagtail.
*   **[Modelos de Contenido de Colección](Collection_Content_Models.md)**: Define los modelos específicos para colecciones en Wagtail.
*   **[Modelos de Contenido de Glosario](Glossary_Content_Models.md)**: Define los modelos específicos para términos de glosario en Wagtail.
*   **[Modelos de Contenido de Página de Inicio](Home_Page_Models.md)**: Define los modelos específicos para páginas de inicio en Wagtail.
*   **[Modelos de Contenido de Ubicación](Location_Content_Models.md)**: Define los modelos específicos para páginas de ubicación en Wagtail.
*   **[Modelos de Contenido de Producto](Product_Content_Models.md)**: Define los modelos específicos para productos en Wagtail.

# Definiciones de Metafields de Recurso para Servicios de Sincronización de Contenido

Este módulo (`shopify_content/sync/resource_metafield_definitions.py`) es fundamental para la gestión de definiciones de metafields en Shopify. Asegura que los recursos como blogs y artículos, así como las páginas de índice de blogs, tengan las definiciones de metafields necesarias para la sincronización y el manejo del contenido editorial desde Wagtail.

## Propósito y Funcionalidad Principal

El propósito principal de este módulo es definir y asegurar la existencia de metafields específicos en Shopify para diferentes tipos de recursos (`BLOG`, `ARTICLE`). Esto es crucial para almacenar metadatos adicionales asociados con el contenido de Wagtail que se sincroniza con Shopify. La funcionalidad es idempotente, lo que significa que se puede ejecutar varias veces sin causar efectos secundarios no deseados si las definiciones ya existen.

## Arquitectura y Componentes Clave

El módulo se compone de una clase de especificación y varias funciones que interactúan con la API de Shopify para gestionar las definiciones de metafields.

### `ResourceMetafieldDefinitionSpec`

Esta es una clase de datos (`dataclass`) inmutable que encapsula las especificaciones de una definición de metafield de Shopify. Los atributos clave incluyen:

*   **`name`**: El nombre legible del metafield.
*   **`namespace`**: El espacio de nombres del metafield, que ayuda a organizar los metafields.
*   **`key`**: La clave única del metafield dentro de su espacio de nombres.
*   **`type`**: El tipo de datos del metafield (por ejemplo, `'list.single_line_text_field'`).
*   **`description`**: Una descripción clara del propósito del metafield.
*   **`owner_type`**: El tipo de recurso de Shopify al que pertenece el metafield (por ejemplo, `'BLOG'`, `'ARTICLE'`).

### Definiciones Predefinidas de Metafields

El módulo define varias constantes que utilizan `ResourceMetafieldDefinitionSpec` para especificar los metafields requeridos:

*   **`BLOG_INDEX_PAGE_METAFIELD_DEFINITION`**: Reutiliza la definición de metafield de lista de índices de página de [Definiciones de Metafields de Página](Content_Synchronization_Services_Page_Metafield_Definitions.md).
*   **`BLOG_RESOURCE_METAFIELD_DEFINITIONS`**: Una tupla que contiene especificaciones para los metafields asociados con los recursos de `BLOG`. Incluye, por ejemplo, el metafield `custom.available_locales` para indicar los idiomas disponibles del blog.
*   **`ARTICLE_RESOURCE_METAFIELD_DEFINITIONS`**: Similar a las definiciones de blog, pero para recursos de `ARTICLE`. También incluye el metafield `custom.available_locales` para los idiomas disponibles del artículo.

### Funciones Principales

*   **`_existing_definitions(shop: str, owner_type: str) -> dict`**:
    Realiza una consulta a la API de GraphQL de Shopify (`METAFIELD_DEFINITIONS_QUERY`) para recuperar todas las definiciones de metafields existentes para un `owner_type` específico. Esto permite al sistema verificar si una definición ya existe antes de intentar crearla.

*   **`_ensure_resource_definitions(shop: str, specs: tuple[ResourceMetafieldDefinitionSpec, ...]) -> dict`**:
    Esta función itera sobre una tupla de especificaciones de metafields (`ResourceMetafieldDefinitionSpec`). Para cada especificación, verifica si el metafield ya existe en Shopify utilizando `_existing_definitions`. Si no existe, envía una mutación a la API de GraphQL de Shopify (`METAFIELD_DEFINITION_CREATE`) para crear la definición del metafield. Retorna un diccionario con estadísticas de las operaciones realizadas (creadas, omitidas, errores).

*   **`ensure_index_metafield_definitions(shop: str) -> dict`**:
    La función principal que orquesta el proceso de garantizar la existencia de las definiciones de metafields necesarias. Invoca a `ensure_page_metafield_definitions` (del módulo de definiciones de metafields de página) para los metafields a nivel de página, y luego a `_ensure_resource_definitions` para los metafields de recursos de `BLOG` y `ARTICLE`.

*   **`ensure_blog_metafield_definitions(shop: str) -> dict`**:
    Un alias de compatibilidad con versiones anteriores para `ensure_index_metafield_definitions`.

## Relaciones entre Componentes y Arquitectura

El módulo interactúa estrechamente con la API de Shopify a través del servicio GraphQL, como se detalla en [Shopify API Client](../../../Application_Core___Shopify_Integration_Platform/Shopify_API_Client.md).

```mermaid
graph TD
    subgraph shopify_content/sync
        A[ensure_index_metafield_definitions] --> B[_ensure_resource_definitions (BLOG_RESOURCE_METAFIELD_DEFINITIONS)]
        A --> C[_ensure_resource_definitions (ARTICLE_RESOURCE_METAFIELD_DEFINITIONS)]
        A --> D[ensure_page_metafield_definitions (PAGE_INDEX_LISTINGS_DEFINITION)]
    end

    subgraph External Dependencies
        D --> E[Content_Synchronization_Services_Page_Metafield_Definitions.md]
        B & C --> F[Shopify GraphQL API]
        F --> G[shopify_requests/graphql_service.py::execute_admin_graphql]
    end

    subgraph Data Structures
        H[ResourceMetafieldDefinitionSpec]
        B & C --> H
    end

    style A fill:#cef,stroke:#333,stroke-width:2px;
    style D fill:#cef,stroke:#333,stroke-width:2px;
    style F fill:#fcc,stroke:#333,stroke-width:2px;
    style G fill:#bbf,stroke:#333,stroke-width:2px;
    style H fill:#f9f,stroke:#333,stroke-width:2px;
```

## Flujo del Proceso para Asegurar Definiciones de Metafields

El siguiente diagrama ilustra el flujo de alto nivel cuando se llama a `ensure_index_metafield_definitions`:

```mermaid
graph TD
    A[Inicio: Llamada a ensure_index_metafield_definitions(shop)] --> B{Asegurar Definiciones de Metafields para Páginas (vía Content_Synchronization_Services_Page_Metafield_Definitions.md)};
    B --> C{Asegurar Definiciones de Metafields para Recursos de BLOG};
    C --> D{Asegurar Definiciones de Metafields para Recursos de ARTICLE};
    D --> E[Retornar Estadísticas Combinadas (creadas, omitidas, errores)];
    E --> F[Fin];

    subgraph Detalle de "Asegurar Definiciones de Metafields para Recursos"
        G[Para cada ResourceMetafieldDefinitionSpec en la tupla] --> H{Consultar _existing_definitions para owner_type};
        H --> I{Metafield Existe?};
        I -- Sí --> J[Marcar como 'omitido'];
        I -- No --> K{Enviar mutación METAFIELD_DEFINITION_CREATE a Shopify GraphQL API};
        K -- Éxito --> L[Marcar como 'creado'];
        K -- Fallo --> M[Marcar como 'error'];
        J --> G;
        L --> G;
        M --> G;
    end

    C --> G;
    D --> G;
```

## Integración con el Sistema General

Este módulo es una parte integral de los [Servicios de Sincronización de Contenido](../Content_Synchronization_Services.md) que conectan Wagtail con Shopify. Su función principal es preparar el entorno de Shopify garantizando que los metafields necesarios para almacenar los metadatos de Wagtail estén correctamente definidos.

Se apoya en gran medida en el módulo [Shopify API Client](../../../Application_Core___Shopify_Integration_Platform/Shopify_API_Client.md) para realizar todas las operaciones de GraphQL con Shopify. Además, trabaja en conjunto con el módulo de [Definiciones de Metafields de Página](Content_Synchronization_Services_Page_Metafield_Definitions.md) para una gestión completa de las definiciones de metafields en Shopify, tanto a nivel de página como de recurso.

La existencia de estos metafields es vital para funcionalidades como la internacionalización, permitiendo que el contenido de Wagtail se sincronice con Shopify y que los diferentes locales estén correctamente gestionados y presentados en la tienda online.

# Definiciones de Metafields de Página para Servicios de Sincronización de Contenido

Este módulo, `Content_Synchronization_Services_Page_Metafield_Definitions`, es fundamental para la gestión y sincronización de contenido entre Wagtail y Shopify. Su propósito principal es asegurar que las definiciones de los metafields necesarios para las páginas de Shopify (con `ownerType: PAGE`) estén correctamente configuradas en la plataforma Shopify, facilitando así el almacenamiento de datos precalculados y de indexación generados por Wagtail.

## Propósito y Funcionalidad Principal

El módulo se encarga de definir y, si es necesario, crear metafields específicos en Shopify que son utilizados por los consumidores de sincronización de índices. Esto permite que el contenido editorial complejo o la información de indexación generada en Wagtail se almacene de manera estructurada en Shopify, lista para ser utilizada por el storefront.

### Componentes Clave

-   `PageMetafieldDefinitionSpec`: Una clase de datos (`dataclass`) que encapsula la especificación de un metafield de página de Shopify. Incluye atributos como `name`, `namespace`, `key`, `type` y `description`. Esta especificación es crucial para la creación y validación de los metafields.

    ```python
    @dataclass(frozen=True)
    class PageMetafieldDefinitionSpec:
        name: str
        namespace: str
        key: str
        type: str
        description: str
    ```

-   `_existing_page_definitions(shop: str) -> dict[tuple[str, str], dict]`: Esta función auxiliar se conecta a la API Admin de Shopify para recuperar todas las definiciones de metafields existentes para el tipo de propietario `PAGE`. Retorna un diccionario donde la clave es una tupla `(namespace, key)` y el valor es el nodo de la definición del metafield, permitiendo una rápida verificación de si un metafield ya existe.

-   `ensure_page_metafield_definitions(shop: str, *, specs: tuple[PageMetafieldDefinitionSpec, ...] | None = None) -> dict`: La función principal del módulo. Recibe el nombre de la tienda (`shop`) y una tupla de especificaciones de metafields (`specs`). Por defecto, utiliza `PAGE_INDEX_METAFIELD_DEFINITIONS`.
    -   Consulta las definiciones existentes de Shopify utilizando `_existing_page_definitions`.
    -   Itera sobre cada `PageMetafieldDefinitionSpec` proporcionada.
    -   Si la definición del metafield ya existe en Shopify (verificado por `namespace` y `key`), se omite y se registra como "skipped".
    -   Si no existe, intenta crear la definición del metafield en Shopify utilizando una mutación GraphQL (`METAFIELD_DEFINITION_CREATE`).
    -   Registra los metafields creados, omitidos y los errores encontrados durante el proceso.
    -   Retorna un diccionario con las estadísticas de la operación (`created`, `skipped`, `errors`).

### Definiciones de Metafields Predefinidas

El módulo incluye definiciones de metafields estándar para la sincronización:

-   `PAGE_INDEX_LISTINGS_DEFINITION`:
    ```python
    PAGE_INDEX_LISTINGS_DEFINITION = PageMetafieldDefinitionSpec(
        name='Index listings',
        namespace='custom',
        key='index_listings',
        type='json',
        description=(
            'Precomputed multi-locale index listings JSON from Wagtail '
            '(blog, glossary, locations).'
        ),
    )
    ```
    Este metafield está diseñado para almacenar listados de índices precalculados y multi-locale en formato JSON, abarcando blogs, glosarios y ubicaciones.

-   `LEGACY_PAGE_INDEX_METAFIELD_DEFINITIONS`: Una tupla de definiciones de metafields que corresponden a una arquitectura de índice multi-página ya **deprecada**. Estas definiciones no se crean por defecto, pero se mantienen por compatibilidad. Incluyen metafields para `glossary_locale`, `glossary_index`, `location_locale`, `location_index`, `index_alternates` y `index_noindex`.

## Arquitectura y Relaciones

Este módulo se integra dentro de los [Servicios de Sincronización de Contenido](../Content_Synchronization_Services.md) y depende fuertemente del [Cliente API de Shopify](../../../Application_Core___Shopify_Integration_Platform/Shopify_API_Client.md) para sus interacciones con la plataforma Shopify.

El flujo de operación y sus relaciones se pueden visualizar de la siguiente manera:

```mermaid
graph TD
    subgraph "Sistema de Gestión de Contenido Wagtail"
        subgraph "Gestión de Contenido Shopify"
            subgraph "Servicios de Sincronización de Contenido"
                Module[Definiciones de Metafields de Página]
                PageMetafieldDefinitionSpec(PageMetafieldDefinitionSpec)
                ExistingDefsFn[_existing_page_definitions()]
                EnsureDefsFn[ensure_page_metafield_definitions()]
            end
        end
    end

    Module --> PageMetafieldDefinitionSpec
    Module --> ExistingDefsFn
    Module --> EnsureDefsFn

    subgraph "Plataforma de Integración Shopify"
        GraphQLService[Shopify_API_Client/Shopify_API_Client_Servicio_GraphQL]
        ShopifyAdminAPI[API Admin de Shopify]
    end

    ExistingDefsFn -- "Consulta Metafields Existentes (METAFIELD_DEFINITIONS_QUERY)" --> GraphQLService
    EnsureDefsFn -- "Crea Metafields Faltantes (METAFIELD_DEFINITION_CREATE)" --> GraphQLService
    GraphQLService -- "Comunicación GraphQL" --> ShopifyAdminAPI

    style Module fill:#f9f,stroke:#333,stroke-width:2px
    style PageMetafieldDefinitionSpec fill:#bbf,stroke:#333,stroke-width:2px
    style ExistingDefsFn fill:#ccf,stroke:#333,stroke-width:2px
    style EnsureDefsFn fill:#ccf,stroke:#333,stroke-width:2px
    style GraphQLService fill:#fcc,stroke:#333,stroke-width:2px
    style ShopifyAdminAPI fill:#ffc,stroke:#333,stroke-width:2px
```

### Componentes Relacionados

-   **`shopify_requests.graphql_service.execute_admin_graphql`**: Este módulo utiliza esta función para todas sus operaciones de GraphQL, tanto para consultar definiciones existentes como para crear nuevas. Se encuentra en el módulo [Shopify_API_Client/Shopify_API_Client_Servicio_GraphQL](../../../Application_Core___Shopify_Integration_Platform/Shopify_API_Client/Shopify_API_Client_Servicio_GraphQL.md).
-   **Comandos de Gestión de Django**: Este módulo es invocado por comandos de gestión de Django, como `ensure_page_metafield_definitions`, para configurar las definiciones de metafields al desplegar o inicializar el sistema. Puedes encontrar más detalles en los [Comandos de Configuración de Metaobjects y Definiciones](../Metaobject_Definition___Setup_Commands.md).
-   **Modelos de Contenido de Wagtail**: Los datos almacenados en estos metafields de página provienen del contenido gestionado en Wagtail, como las [Páginas de Blog](../Blog_Content_Models.md), [Páginas de Glosario](../Glossary_Content_Models.md) y [Páginas de Ubicación](../Location_Content_Models.md).

## Cómo el Módulo Encaja en el Sistema General

El módulo `Content_Synchronization_Services_Page_Metafield_Definitions` es una pieza esencial en la estrategia de sincronización bidireccional entre Wagtail y Shopify. Permite que el contenido enriquecido y estructurado que reside en Wagtail sea representado adecuadamente en Shopify a través de metafields. Estos metafields son luego consumidos por el storefront de Shopify para renderizar páginas de contenido dinámico y localizado.

Forma parte de la capa de servicios de sincronización, asegurando la infraestructura de datos en Shopify antes de que los procesos de importación o materialización de contenido comiencen a poblar estos metafields con datos reales de Wagtail. Sin las definiciones de metafields adecuadas, el sistema no podría almacenar la información necesaria para los listados de índices o el contenido localizado en Shopify.

Este módulo contribuye a la robustez del sistema al automatizar la configuración de la estructura de datos en Shopify, reduciendo errores manuales y facilitando el despliegue y la evolución del esquema de contenido.

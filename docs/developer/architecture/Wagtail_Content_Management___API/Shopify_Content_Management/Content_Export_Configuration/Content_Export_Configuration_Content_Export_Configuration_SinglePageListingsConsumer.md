# SinglePageListingsConsumer

El módulo `SinglePageListingsConsumer` es responsable de exportar configuraciones de listados de índice personalizados a una página específica de Shopify a través de metafields. Actúa como una clase base para consumidores más específicos que necesitan empujar datos estructurados a Shopify.

## Funcionalidad Principal

El componente `SinglePageListingsConsumer` en `shopify_content/export_config/single_page.py` facilita la sincronización de listados de contenido con Shopify. Su propósito principal es obtener una configuración específica de una `ShopifyRootPage`, construir una carga útil de datos y luego empujar esta carga útil como un metafield JSON a una página de Shopify designada.

### `SinglePageListingsConsumer`

Esta clase es una base abstracta que define la interfaz para los consumidores de listados de páginas únicas. Contiene la lógica común para recuperar la configuración de exportación y sincronizar los datos con Shopify.

**Atributos clave:**

*   `root_slug`: El slug de la página raíz de Shopify desde donde se obtiene la configuración de exportación.
*   `config_key`: La clave dentro del diccionario `export_config` de la página raíz que contiene la configuración específica para este consumidor.

**Métodos clave:**

*   `get_root_page()`: Recupera la instancia de `ShopifyRootPage` viva basándose en `root_slug`.
*   `get_config(root=None)`: Obtiene la configuración de exportación específica para este consumidor de la `ShopifyRootPage` proporcionada o de la recuperada. Verifica si la exportación está habilitada y si se ha proporcionado un `page_gid`.
*   `build_payload()`: Un método abstracto que debe ser implementado por las subclases para construir la carga útil de datos que se enviará a Shopify. Se espera que devuelva un diccionario.
*   `locale_codes_for_page(page)`: Un método para obtener los códigos de locale para una página específica. Por defecto, devuelve `None`.
*   `sync(*, dry_run: bool = False)`: El método principal para ejecutar la sincronización. Recupera la configuración, construye la carga útil y la empuja como un metafield JSON a la página de Shopify especificada por `page_gid`. También gestiona el modo de simulación (`dry_run`) y recopila estadísticas de la operación.
*   `queue_sync(*, locale_codes: list[str] | None = None)`: Un método abstracto para encolar la operación de sincronización, que debe ser implementado por las subclases.

## Arquitectura y Relaciones de Componentes

El `SinglePageListingsConsumer` interactúa con varios componentes clave dentro de la aplicación:

### Dependencias Directas

*   **[ShopifyRootPage](../Content_Base_Models___Mixins/Content_Base_Models___Mixins_ShopifyRootPage_Modelo.md)**: El consumidor se basa en `ShopifyRootPage` para obtener su configuración de exportación. Esta página Wagtail almacena un diccionario `export_config` que define cómo y qué contenido debe exportarse.
*   `_get_shop()` y `_push_metafields()`: Funciones auxiliares de `shopify_content.sync.outbound` que manejan la interacción directa con la API de Shopify para obtener la instancia de la tienda y empujar metafields.

### Patrón de Extensión

`SinglePageListingsConsumer` está diseñado para ser extendido por otras clases (por ejemplo, `BlogListingsConsumer`, `GlossaryIndexConsumer`, `LocationIndexConsumer`) que implementarán la lógica específica en `build_payload()` y `queue_sync()` para generar los datos de listados apropiados para sus respectivos tipos de contenido.

### Diagrama de Clases

```mermaid
classDiagram
    direction LR
    class SinglePageListingsConsumer {
        +root_slug: str
        +config_key: str
        +get_root_page()
        +get_config(root)
        +build_payload() dict
        +locale_codes_for_page(page) list~str~
        +sync(dry_run) dict
        +queue_sync(locale_codes) void
    }

    class ShopifyRootPage {
        +export_config: dict
    }

    class _get_shop <<Function>>
    class _push_metafields <<Function>>

    SinglePageListingsConsumer ..> ShopifyRootPage : obtiene configuración de
    SinglePageListingsConsumer ..> _get_shop : utiliza
    SinglePageListingsConsumer ..> _push_metafields : empuja metafields a

    Note over SinglePageListingsConsumer:
        Clase base abstracta
        para consumidores de listados
        de una sola página.
    

```

## Flujo de Datos

1.  **Configuración**: El `SinglePageListingsConsumer` recupera la configuración de exportación relevante de la `ShopifyRootPage` usando `root_slug` y `config_key`.
2.  **Construcción de Carga Útil**: Se llama a `build_payload()` (implementado por una subclase) para generar un diccionario con los datos de los listados de índice.
3.  **Obtención de Tienda Shopify**: La función `_get_shop()` es invocada para obtener la instancia de la tienda Shopify, necesaria para la comunicación con la API.
4.  **Envío a Shopify**: La carga útil se serializa a JSON y se envía a Shopify como un metafield (`custom.index_listings`) a la `page_gid` especificada en la configuración, utilizando la función `_push_metafields()`.
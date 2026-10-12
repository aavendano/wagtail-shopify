# Ayudantes de URL de Storefront

Este módulo, `Content_URL___Semantic_Linking_Logic_Storefront_URL_Helpers`, proporciona un conjunto de funciones auxiliares esenciales para construir y gestionar URLs canónicas de la tienda Shopify para páginas de contenido de Wagtail. Su propósito principal es garantizar la coherencia y corrección en la generación de URLs para diversos tipos de contenido, lo que es fundamental para la indexación, el enlazado interno y el SEO en el storefront de Shopify.

## Propósito y Funcionalidad Principal

El módulo centraliza la lógica para construir rutas de URL relativas al storefront para productos, colecciones, blogs, artículos, términos de glosario, páginas de ubicación, páginas de inicio y metaobjetos generales. También maneja la incorporación de prefijos de localización de Shopify Markets y determina los metadatos de tipo de contenido para las entradas del índice de URL.

El componente clave `PathVariant` encapsula las diferentes representaciones de una URL (canónica y con prefijo de localización) para facilitar la indexación y el enrutamiento.

### Funciones y Componentes Clave

*   **Generación de Rutas Específicas:**
    *   `product_path(handle: str)`: Genera la ruta para un producto.
    *   `collection_path(handle: str)`: Genera la ruta para una colección.
    *   `blog_path(handle: str)`: Genera la ruta para un blog.
    *   `article_path(blog_handle: str, article_handle: str)`: Genera la ruta para un artículo dentro de un blog.
    *   `glossary_term_path(handle: str)`: Genera la ruta para un término de glosario (metaobjeto).
    *   `location_page_path(handle: str)`: Genera la ruta para una página de ubicación (metaobjeto).
    *   `home_page_path(handle: str)`: Genera la ruta para una página de inicio.
    *   `metaobject_page_path(url_handle: str, handle: str)`: Genera una ruta general para páginas de metaobjetos.
    *   `root_index_path(slug: str)`: Devuelve la ruta de índice para slugs de páginas raíz específicos.

*   **`related_link_path(link: dict[str, Any])`:** Construye una URL relativa al storefront a partir de un diccionario serializado de enlaces relacionados, manejando diferentes tipos de enlaces (producto, colección, artículo, metaobjeto, blog).

*   **`page_content_type_key(page)`:** Retorna una clave de tipo de contenido estable para las filas del índice de URL, identificando si una página de Wagtail es un producto, colección, blog, artículo, término de glosario, ubicación, página de inicio, o página raíz.

*   **`storefront_path_for_page(page)`:** La función principal que devuelve la ruta canónica relativa al storefront para una página de Wagtail dada, delegando a las funciones de ruta específicas según el tipo de página.

*   **`locale_prefix_for_page(page)`:** Determina y devuelve el prefijo de URL de Shopify Markets correspondiente al código de idioma de la página.

*   **`page_index_metadata(page)`:** Extrae metadatos clave (tipo de contenido, handle, blog_handle) de una página para su uso en la indexación de URLs.

*   **`PathVariant` (dataclass):**
    ```python
    @dataclass(frozen=True)
    class PathVariant:
        normalized_path: str
        locale_prefix: str
        is_canonical: bool
    ```
    Este dataclass representa una variante de ruta para una página. `normalized_path` es la ruta base, `locale_prefix` es el prefijo de localización (si existe) y `is_canonical` indica si esta variante es la URL canónica.

*   **`path_variants_for_index(page)`:** Genera una lista de objetos `PathVariant` para una página, incluyendo la variante canónica y, si aplica, una variante con prefijo de localización. Estas variantes son utilizadas por el `ContentUrlIndex`.

*   **`all_paths_for_page(page)`:** Devuelve una lista de todas las rutas relativas completas al storefront para una página, incluyendo la canónica y cualquier variante con prefijo de localización.

### Constantes Clave

*   `GLOSSARY_METAOBJECT_URL_HANDLE`, `LOCATION_METAOBJECT_URL_HANDLE`: Handles predefinidos para URLs de metaobjetos específicos.
*   `KNOWN_LOCALE_PREFIXES`: Una tupla de prefijos de localización conocidos para Shopify Markets.
*   `LOCALE_CODE_TO_PREFIX`: Un mapeo de códigos de localización a sus prefijos de URL correspondientes.
*   `ROOT_SLUG_TO_INDEX_PATH`: Un mapeo de slugs de páginas raíz a sus rutas de índice.

## Arquitectura y Relaciones de Componentes

Este módulo se integra con el sistema Wagtail y los modelos de contenido de Shopify, actuando como un puente para la generación de URLs amigables para el storefront. Depende en gran medida de los modelos de página definidos en el módulo [Shopify_Content_Models](../Shopify_Content_Models.md) para determinar el tipo de contenido y extraer los handles necesarios para construir las URLs. También utiliza funciones de slugificación de Django (`django.utils.text.slugify`).

A continuación, se presenta un diagrama de componentes que ilustra las dependencias y el flujo de datos para la generación de URLs:

```mermaid
graph TD
    subgraph shopify_content/storefront_urls.py
        A[storefront_path_for_page(page)] --> B{Tipo de Página?}
        B -- ProductPage --> C[product_path(handle)]
        B -- CollectionPage --> D[collection_path(handle)]
        B -- BlogPage --> E[blog_path(handle)]
        B -- ArticlePage --> F[article_path(blog_handle, article_handle)]
        B -- GlossaryTermPage --> G[glossary_term_path(handle)]
        B -- LocationPage --> H[location_page_path(handle)]
        B -- HomePage --> I[home_page_path(handle)]
        B -- ShopifyRootPage --> J[root_index_path(slug)]
        K[page_content_type_key(page)]
        L[locale_prefix_for_page(page)]
        M[page_index_metadata(page)]
        N[PathVariant]
        O[path_variants_for_index(page)]
        P[all_paths_for_page(page)]

        A --> K
        A --> M
        O --> N
        P --> O
    end

    subgraph Shopify_Content_Models
        Q[ProductPage]
        R[CollectionPage]
        S[BlogPage]
        T[ArticlePage]
        U[GlossaryTermPage]
        V[LocationPage]
        W[HomePage]
        X[ShopifyRootPage]
    end

    subgraph Otros Módulos
        Y[shopify_content.location_slug::location_page_slug]
        Z[shopify_content.home_slug::home_page_handle]
        AA[django.utils.text::slugify]
        BB[wagtail.models::Page]
    end

    B --> Q
    B --> R
    B --> S
    B --> T
    B --> U
    B --> V
    B --> W
    B --> X

    F --> T
    G --> U
    H --> V
    I --> W

    C -- usa --> AA
    D -- usa --> AA
    E -- usa --> AA
    F -- usa --> AA
    G -- usa --> AA
    H -- usa --> Y
    I -- usa --> Z
    J -- usa --> X

    K --> Q
    K --> R
    K --> S
    K --> T
    K --> U
    K --> V
    K --> W
    K --> X

    L --> BB
    M --> BB

    A --> BB
    O --> BB
    P --> BB
```

## Cómo Encaja en el Sistema General

Este módulo es un componente fundamental dentro de la estrategia de gestión de contenido de Shopify, particularmente para la indexación y el enrutamiento de URLs en el storefront.

1.  **Generación de URLs Canónicas:** Proporciona las URLs canónicas para todo el contenido de Wagtail que se sincroniza con Shopify, lo que es crucial para evitar problemas de contenido duplicado y mejorar el SEO.
2.  **Soporte de Localización:** Facilita la implementación de Shopify Markets al permitir la generación de URLs con prefijos de localización, asegurando que el contenido se sirva correctamente a audiencias en diferentes regiones e idiomas.
3.  **Integración con `ContentUrlIndex`:** Las funciones `page_index_metadata` y `path_variants_for_index` están diseñadas específicamente para alimentar el `ContentUrlIndex` (definido en [Shopify_Content_Management/Content_Models.md](../Shopify_Content_Models.md)), que es responsable de mantener un registro de todas las URLs de contenido y sus variantes. Esto permite una búsqueda y resolución de URLs eficiente en todo el sistema.
4.  **Enlaces Semánticos y Resolución de Enlaces:** Las funciones de este módulo son utilizadas por la lógica de enlaces semánticos y de resolución de enlaces para construir URLs internas precisas y mantener la integridad de los enlaces a través de las actualizaciones de contenido. Consulte [Content_URL___Semantic_Linking_Logic_Article_Product_Linking](Content_URL___Semantic_Linking_Logic_Article_Product_Linking.md) y [Content_URL___Semantic_Linking_Logic_URL_Resolution](Content_URL___Semantic_Linking_Logic_URL_Resolution.md) para más detalles sobre cómo se utilizan estas URLs en la lógica de enlace y resolución.

En resumen, `storefront_urls.py` es el motor detrás de la construcción de URLs amigables para el SEO y localizadas para el storefront de Shopify, asegurando que el contenido gestionado en Wagtail sea accesible y esté correctamente indexado.

# Gestión de URLs y Enlaces de Tienda (shopify_content/storefront_urls)

Este módulo, `shopify_content/storefront_urls.py`, proporciona un conjunto de utilidades y funciones auxiliares para la construcción y gestión de rutas URL canónicas para el *storefront* de Shopify, basadas en el contenido administrado en Wagtail. Facilita la generación de URLs consistentes y localizadas para diferentes tipos de páginas de contenido, asegurando una correcta indexación y navegación en el entorno de Shopify.

## Propósito y Funcionalidad Principal

El objetivo principal de este módulo es centralizar la lógica para determinar las rutas relativas de Shopify para las páginas de contenido de Wagtail. Esto incluye:
*   Generar rutas específicas para productos, colecciones, blogs, artículos, términos de glosario, páginas de ubicación y páginas de inicio.
*   Determinar prefijos de localización (locale prefixes) para URLs, lo que es crucial para Shopify Markets.
*   Proveer una interfaz para obtener metadatos de indexación de URLs para el sistema de gestión de contenido.
*   Definir variantes de rutas (canónicas y con prefijo de locale) para cada página.

## Arquitectura y Relaciones de Componentes

El módulo `shopify_content/storefront_urls.py` se compone de varias funciones auxiliares y una clase de datos clave para la gestión de URLs.

### Clase Principal: `PathVariant`

`PathVariant` es un dataclass inmutable que encapsula una variante de una ruta URL, incluyendo si es la canónica y el prefijo de localización aplicado.

```python
@dataclass(frozen=True)
class PathVariant:
    normalized_path: str
    locale_prefix: str
    is_canonical: bool
```

*   `normalized_path`: La ruta URL normalizada, sin el prefijo de localización.
*   `locale_prefix`: El prefijo de localización de Shopify Markets (ej. 'es-us').
*   `is_canonical`: Un booleano que indica si esta variante es la ruta URL canónica.

### Constantes Globales

*   `GLOSSARY_METAOBJECT_URL_HANDLE`: Manejador URL para metaobjetos de glosario ('glossary').
*   `LOCATION_METAOBJECT_URL_HANDLE`: Manejador URL para metaobjetos de ubicación ('location').
*   `KNOWN_LOCALE_PREFIXES`: Una tupla de prefijos de localización conocidos para Shopify Markets.
*   `LOCALE_CODE_TO_PREFIX`: Un diccionario que mapea códigos de locale de Django a prefijos de URL de Shopify Markets.
*   `ROOT_SLUG_TO_INDEX_PATH`: Un diccionario que mapea slugs de páginas raíz de Wagtail a sus rutas de índice correspondientes en Shopify.

### Funciones de Generación de Rutas Específicas

Este módulo define funciones para construir rutas para tipos de contenido específicos:

*   `product_path(handle: str)`: Genera la ruta para un producto.
*   `collection_path(handle: str)`: Genera la ruta para una colección.
*   `blog_path(handle: str)`: Genera la ruta para un blog.
*   `article_path(blog_handle: str, article_handle: str)`: Genera la ruta para un artículo dentro de un blog.
*   `glossary_term_path(handle: str)`: Genera la ruta para un término de glosario.
*   `location_page_path(handle: str)`: Genera la ruta para una página de ubicación.
*   `home_page_path(handle: str)`: Genera la ruta para una página de inicio.
*   `metaobject_page_path(url_handle: str, handle: str)`: Genera una ruta general para una página de metaobjeto.
*   `root_index_path(slug: str)`: Retorna la ruta de índice para un slug de página raíz conocido.

### Funciones Auxiliares Internas

Estas funciones se utilizan internamente para extraer información de las páginas de Wagtail:

*   `_page_handle(page)`: Extrae el 'handle' o slug de una página de Wagtail.
*   `_article_blog_handle(page)`: Obtiene el 'handle' del blog padre de una `ArticlePage`.
*   `_location_handle(page)`: Obtiene el 'handle' de una `LocationPage`.
*   `_home_handle(page)`: Obtiene el 'handle' de una `HomePage`.

### Funciones Principales de Utilidad

*   `related_link_path(link: dict[str, Any]) -> str`: Construye una URL relativa al storefront a partir de un diccionario de enlace serializado.
*   `page_content_type_key(page) -> str | None`: Retorna una clave de tipo de contenido estable para filas de `ContentUrlIndex`.
*   `storefront_path_for_page(page) -> str | None`: Retorna la ruta canónica relativa al *storefront* para una página de Wagtail. Es la función central para determinar la URL base.
*   `locale_prefix_for_page(page) -> str`: Retorna el prefijo de URL de Shopify Markets para el locale de la página.
*   `page_index_metadata(page) -> tuple[str, str, str]`: Retorna una tupla con el tipo de contenido, el 'handle' y el 'handle' del blog (si aplica) para propósitos de indexación.
*   `path_variants_for_index(page) -> list[PathVariant]`: Retorna una lista de objetos `PathVariant` para una página, incluyendo la canónica y las variantes con prefijo de locale.
*   `all_paths_for_page(page) -> list[str]`: Retorna todas las rutas relativas completas del *storefront* para una página (canónicas y con prefijo de locale).

### Diagrama de Componentes del Módulo

```mermaid
graph TD
    subgraph shopify_content/storefront_urls.py
        A[PathVariant (dataclass)]
        B[Funciones de Generación de Rutas]
        C[Funciones Auxiliares Internas]
        D[Funciones Principales de Utilidad]
        E[Constantes Globales]

        E --> B
        C --> B
        D --> B
        D --> C
        D --> A

        subgraph Funciones de Generación de Rutas
            B1(product_path)
            B2(collection_path)
            B3(blog_path)
            B4(article_path)
            B5(glossary_term_path)
            B6(location_page_path)
            B7(home_page_path)
            B8(metaobject_page_path)
            B9(root_index_path)
        end

        subgraph Funciones Auxiliares Internas
            C1(_page_handle)
            C2(_article_blog_handle)
            C3(_location_handle)
            C4(_home_handle)
        end

        subgraph Funciones Principales de Utilidad
            D1(related_link_path)
            D2(page_content_type_key)
            D3(storefront_path_for_page)
            D4(locale_prefix_for_page)
            D5(page_index_metadata)
            D6(path_variants_for_index)
            D7(all_paths_for_page)
        end
    end
```

### Diagrama de Flujo de Datos para la Generación de URLs

Este diagrama ilustra cómo `storefront_path_for_page` utiliza otras funciones y los objetos de página de Wagtail para determinar la URL canónica.

```mermaid
graph TD
    A[Página de Wagtail] -->|get_specific()| B(Página Específica de Wagtail)
    B -->|Tipo de Página| C{Es ProductPage?}
    C -- Sí --> D1[Obtener handle del producto]
    D1 --> E1[Llamar product_path()]
    C -- No --> F{Es CollectionPage?}
    F -- Sí --> D2[Obtener handle de colección]
    D2 --> E2[Llamar collection_path()]
    F -- No --> G{Es BlogPage?}
    G -- Sí --> D3[Obtener handle del blog]
    D3 --> E3[Llamar blog_path()]
    G -- No --> H{Es ArticlePage?}
    H -- Sí --> D4[Obtener handle del artículo]
    H -- Sí --> D5[Obtener handle del blog padre]
    D4 & D5 --> E4[Llamar article_path()]
    H -- No --> I{Es GlossaryTermPage?}
    I -- Sí --> D6[Obtener handle del término]
    D6 --> E5[Llamar glossary_term_path()]
    I -- No --> J{Es LocationPage?}
    J -- Sí --> D7[Obtener handle de ubicación]
    D7 --> E6[Llamar location_page_path()]
    J -- No --> K{Es HomePage?}
    K -- Sí --> D8[Obtener handle de inicio]
    D8 --> E7[Llamar home_page_path()]
    K -- No --> L{Es ShopifyRootPage?}
    L -- Sí --> D9[Obtener slug de la raíz]
    D9 --> E8[Llamar root_index_path()]
    L -- No --> M[Retornar None]

    E1 --> N(Ruta Canónica)
    E2 --> N
    E3 --> N
    E4 --> N
    E5 --> N
    E6 --> N
    E7 --> N
    E8 --> N

    N --> O[storefront_path_for_page]
```

## Integración con el Sistema General

Este módulo es una parte fundamental de la gestión de contenido de Wagtail para Shopify en el contexto de `Wagtail_Content_Management___API/Shopify_Content_Management/Content_URL___Link_Management`. Su rol es crucial para:

*   **Coherencia de URLs**: Asegura que las URLs generadas para el *storefront* de Shopify sean consistentes con los patrones de URL esperados por Shopify, evitando problemas de SEO y navegación.
*   **Soporte de Shopify Markets**: A través de las funciones `locale_prefix_for_page` y el manejo de `PathVariant`, permite la generación de URLs que respetan las configuraciones de internacionalización de Shopify Markets, facilitando la entrega de contenido localizado.
*   **Indexación de Contenido**: Las funciones como `page_content_type_key` y `page_index_metadata` son esenciales para construir y mantener el índice de URLs de contenido (ver [Modelo Indice URL Contenido](../Content_Base_Models___Mixins/Content_Base_Models___Mixins_ModeloIndiceURLContenido.md)), que es utilizado por el sistema para resolver y gestionar enlaces.
*   **Materialización de Contenido**: Las URLs generadas por este módulo son utilizadas por los comandos de materialización para construir las representaciones finales del contenido que se exportan a Shopify.

Las páginas de Wagtail referenciadas en este módulo incluyen:
*   `ProductPage`
*   `CollectionPage`
*   `BlogPage`
*   `ArticlePage`
*   `GlossaryTermPage` (ver [Modelos de Contenido del Glosario](../Glossary_Content_Models.md))
*   `LocationPage` (ver [Modelos de Contenido de Ubicación](../Location_Content_Models.md))
*   `HomePage` (ver [Modelos de Página de Inicio](../Home_Page_Models.md))
*   `ShopifyRootPage` (ver [ShopifyRootPage Modelo](../Content_Base_Models___Mixins/Content_Base_Models___Mixins_ShopifyRootPage_Modelo.md))

Este módulo colabora estrechamente con el [Resolutor de URLs de Contenido (content_url_resolver)](Content_URL___Link_Management_resolucion_urls.md) para garantizar una gestión integral de los enlaces.
# Esquemas Comunes de la API de Contenido de Shopify

El módulo `Shopify_Content_API_EsquemasComunes` (`api/schemas/common.py`) define una colección de esquemas de datos reutilizables que son fundamentales para la comunicación de la API dentro de la integración de Shopify. Estos esquemas estandarizan los formatos de datos para referencias de contenido, enlaces, información de localización, metacampos, resultados de sincronización e importación, y manejo de errores, asegurando consistencia y claridad en todo el sistema.

## Propósito y Funcionalidad Principal

Este módulo actúa como una biblioteca central de definiciones de tipos para la API de contenido de Shopify, facilitando la creación y validación de datos complejos que se intercambian entre el sistema de gestión de contenido (Wagtail) y Shopify, así como con otros servicios internos. Al definir estos esquemas comunes, se promueve la interoperabilidad y se reduce la duplicación de código en la definición de estructuras de datos.

Los esquemas cubren aspectos críticos como:
*   **Referencias de Contenido y Enlaces:** Definiciones para referenciar contenido interno (páginas de Wagtail) y enlaces externos.
*   **Gestión de Localización:** Campos comunes para manejar la información de idioma y traducción de contenido.
*   **Metacampos de Shopify:** Estructuras para interactuar con los metacampos personalizados de Shopify.
*   **Resultados de Operaciones:** Esquemas para reportar el éxito o fracaso de operaciones de sincronización e importación.
*   **Manejo de Errores:** Un esquema uniforme para comunicar mensajes de error.
*   **Imágenes de Shopify:** Estructura para representar URLs de imágenes de Shopify.

## Arquitectura y Relaciones de Componentes

Los esquemas definidos en `api/schemas/common.py` son objetos Pydantic que extienden `ninja.Schema`, lo que les permite ser utilizados para la serialización y validación de datos en los endpoints de la API. Estos esquemas son utilizados por otros esquemas de la API que representan tipos de contenido específicos (por ejemplo, `ArticleIn`, `ProductOut`) y por la lógica de negocio que interactúa con la API de Shopify y el CMS de Wagtail.

### Diagrama de Clases de Esquemas Comunes

```mermaid
classDiagram
    direction LR

    Schema <|-- RelatedLinkSchema
    Schema <|-- ContentReferenceSchema
    Schema <|-- ExternalLinkSchema
    Schema <|-- LocaleCreateFields
    Schema <|-- LocalePatchFields
    Schema <|-- LocaleOutFields
    Schema <|-- StorefrontUrlOutFields
    Schema <|-- FAQSchema
    Schema <|-- MetafieldSchema
    Schema <|-- SyncResultSchema
    Schema <|-- ImportResultSchema
    Schema <|-- ImportTaskSchema
    Schema <|-- ErrorSchema
    Schema <|-- ShopifyImageUrlSchema

    RelatedLinkSchema : +type: Literal
    RelatedLinkSchema : +handle: str
    RelatedLinkSchema : +label: str
    RelatedLinkSchema : +blog_handle: Optional[str]
    RelatedLinkSchema : +url_handle: Optional[str]
    RelatedLinkSchema : +shopify_id: Optional[str]

    ContentReferenceSchema : +page_id: int
    ContentReferenceSchema : +label: Optional[str]
    ContentReferenceSchema : +override_title: Optional[str]
    ContentReferenceSchema : +override_label: Optional[str]
    ContentReferenceSchema : +description: Optional[str]
    ContentReferenceSchema : +type: Optional[str]
    ContentReferenceSchema : +shopify_id: Optional[str]

    ExternalLinkSchema : +url: str
    ExternalLinkSchema : +label: str

    LocaleCreateFields : +locale: Optional[str]
    LocaleCreateFields : +translation_of: Optional[int]

    LocalePatchFields : +locale: Optional[str]
    LocalePatchFields : +translation_of: Optional[int]

    LocaleOutFields : +translation_page_ids: List[int]

    StorefrontUrlOutFields : +storefront_path: Optional[str]
    StorefrontUrlOutFields : +storefront_urls: List[str]
    StorefrontUrlOutFields : +resolve_storefront_path()
    StorefrontUrlOutFields : +resolve_storefront_urls()

    FAQSchema : +question: str
    FAQSchema : +answer: str

    MetafieldSchema : +namespace: str
    MetafieldSchema : +key: str
    MetafieldSchema : +type: str
    MetafieldSchema : +value: str

    SyncResultSchema : +success: bool
    SyncResultSchema : +message: str
    SyncResultSchema : +shopify_id: Optional[str]

    ImportResultSchema : +created: int
    ImportResultSchema : +updated: int
    ImportResultSchema : +skipped: int
    ImportResultSchema : +errors: int
    ImportResultSchema : +message: str

    ImportTaskSchema : +sync_run_id: int
    ImportTaskSchema : +celery_task_id: str
    ImportTaskSchema : +status: str
    ImportTaskSchema : +message: str

    ErrorSchema : +detail: str

    ShopifyImageUrlSchema : +shopify_id: str
    ShopifyImageUrlSchema : +url: str
    ShopifyImageUrlSchema : +alt_text: str
    ShopifyImageUrlSchema : +sort_order: int
```

### Descripción de Esquemas Individuales

*   **`RelatedLinkSchema`**: Define la estructura para un enlace a un recurso de Shopify relacionado (producto, colección, blog, artículo, página, metaobjeto). Incluye el tipo de recurso, el `handle`, una etiqueta para mostrar, y campos condicionales como `blog_handle` o `url_handle` según el `type`.
*   **`ContentReferenceSchema`**: Representa una referencia a una página de Wagtail. Se utiliza en las secciones de la página de inicio para vincular a contenido interno como `CollectionPage` o `ProductPage`. Contiene el `page_id` de Wagtail, una etiqueta opcional y un `shopify_id` resuelto.
*   **`ExternalLinkSchema`**: Estructura simple para enlaces externos, incluyendo la URL absoluta y una etiqueta para mostrar.
*   **`LocaleCreateFields` y `LocalePatchFields`**: Esquemas que definen los campos relacionados con la localización (`locale` y `translation_of`) para la creación y actualización de contenido, respectivamente. Utilizan descripciones detalladas de `LOCALE_FIELD_DESCRIPTION` y `TRANSLATION_OF_FIELD_DESCRIPTION` que se asumen definidas en `../locale_utils.py`.
*   **`LocaleOutFields`**: Define los campos de localización para la salida de datos, incluyendo una lista de `translation_page_ids` para agrupar variantes de traducción.
*   **`StorefrontUrlOutFields`**: Proporciona información sobre las URLs del storefront de Shopify, incluyendo la ruta canónica (`storefront_path`) y una lista de `storefront_urls` con variantes de prefijo de localización. Utiliza métodos estáticos para resolver estas URLs, que dependen de `shopify_content.storefront_urls` y `shopify_content.content_url_index`.
*   **`FAQSchema`**: Estructura para preguntas frecuentes, con campos para la pregunta (`question`) y la respuesta (`answer`).
*   **`MetafieldSchema`**: Define un metamétodo de Shopify, incluyendo `namespace`, `key`, `type` (por ejemplo, `single_line_text_field`, `rich_text_field`, `json`), y `value`. Es crucial para la extensibilidad del contenido de Shopify.
*   **`SyncResultSchema`**: Se utiliza para informar el resultado de una operación de sincronización con Shopify, indicando `success`, un `message` descriptivo y el `shopify_id` del recurso sincronizado.
*   **`ImportResultSchema`**: Detalla el resultado de una operación de importación de contenido, incluyendo el número de páginas creadas, actualizadas, saltadas y con errores, junto con un `message` de resumen.
*   **`ImportTaskSchema`**: Esquema para tareas de importación asíncronas, utilizado principalmente por trabajos de Celery. Incluye `sync_run_id`, `celery_task_id`, `status` y `message`.
*   **`ErrorSchema`**: Un esquema genérico para devolver mensajes de error legibles.
*   **`ShopifyImageUrlSchema`**: Define la estructura para una URL de imagen de Shopify, incluyendo su `shopify_id`, la `url` del CDN, el `alt_text` y el `sort_order`.

## Integración en el Sistema General

Los esquemas comunes son la columna vertebral de la comunicación de datos para la [API de Contenido de Shopify](../Shopify_Content_API.md). Son importados y utilizados por otros módulos de esquemas específicos de contenido como `api/schemas/article.py`, `api/schemas/blog.py`, `api/schemas/product.py`, entre otros, para construir payloads de solicitud y respuesta.

Por ejemplo, un esquema para una página de artículo podría incluir un `MetafieldSchema` para metacampos específicos, `RelatedLinkSchema` para enlaces a productos o colecciones, y `LocaleCreateFields` para manejar la localización durante la creación de un artículo. De manera similar, los resultados de la API para operaciones como la sincronización de contenido se estructuran utilizando `SyncResultSchema` o `ImportResultSchema`.

Además, el `StorefrontUrlOutFields` se integra con la lógica de resolución de URLs de Wagtail (`shopify_content.storefront_urls` y `shopify_content.content_url_index`) para proporcionar información coherente sobre las URLs de cara al público del contenido.

En resumen, este módulo proporciona un vocabulario de datos compartido que garantiza que todos los componentes que interactúan con la API de contenido de Shopify hablen el mismo idioma, mejorando la robustez y la facilidad de mantenimiento de la integración.

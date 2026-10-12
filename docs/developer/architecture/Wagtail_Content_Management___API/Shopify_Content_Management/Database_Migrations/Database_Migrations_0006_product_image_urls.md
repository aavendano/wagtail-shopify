# Migración 0006: URLs de Imágenes de Producto

## Introducción

Este documento detalla la migración de base de datos `0006_product_image_urls` dentro del módulo `shopify_content`. Esta migración introduce cambios fundamentales en la forma en que el sistema maneja las imágenes de productos y colecciones, permitiendo una integración más robusta con las URLs de imágenes y los IDs de medios de Shopify. Se añaden campos a los modelos `ArticlePage` y `CollectionPage` y se crea un nuevo modelo `ProductPageImage` para gestionar múltiples imágenes asociadas a `ProductPage`.

## Arquitectura y Componentes

La migración `0006_product_image_urls.py` es una operación de base de datos estándar de Django que altera el esquema de la base de datos. Sus componentes principales incluyen la clase `Migration` y las operaciones definidas dentro de ella.

### Clase `Migration`

La clase `Migration` orquesta los cambios en la base de datos.

*   **Dependencias**: Esta migración depende de:
    *   `shopify_content.0005_alter_locationpage_shopify_locale`: La migración anterior del mismo módulo, asegurando que los cambios de esquema se apliquen en el orden correcto.
    *   `wagtailimages.0027_image_description`: Una migración del módulo `wagtailimages`, lo que indica que esta migración interactúa con o asume la existencia de la funcionalidad de imágenes de Wagtail.

*   **Operaciones (`operations`)**:
    *   **`AddField` a `ArticlePage`**:
        *   `featured_image_alt` (CharField): Almacena el texto alternativo para la imagen destacada del artículo.
        *   `featured_image_url` (URLField): Almacena la URL absoluta de la imagen destacada del artículo en Shopify.
        *   `shopify_featured_image_id` (CharField): Almacena el GID (Global ID) de `MediaImage` de Shopify para la imagen destacada del artículo.
    *   **`AddField` a `CollectionPage`**:
        *   `image_alt_text` (CharField): Almacena el texto alternativo para la imagen de la colección.
        *   `image_url` (URLField): Almacena la URL absoluta de la imagen de la colección en Shopify.
        *   `shopify_image_id` (CharField): Almacena el GID de `MediaImage` de Shopify para la imagen de la colección.
    *   **`AlterField` en `ArticlePage`**:
        *   Se modifica el campo `featured_image` para añadir un `help_text` aclaratorio sobre el uso de `featured_image_url` cuando la imagen proviene de Shopify en lugar de una subida manual de Wagtail.
    *   **`CreateModel` `ProductPageImage`**:
        *   Crea una tabla para el nuevo modelo `ProductPageImage`, que permite asociar múltiples imágenes a una `ProductPage`.
        *   Campos:
            *   `id`: Clave primaria automática.
            *   `shopify_id` (CharField): GID de `MediaImage` de Shopify para la imagen del producto.
            *   `url` (URLField): URL absoluta de la CDN para la imagen del producto.
            *   `alt_text` (CharField): Texto alternativo para la imagen del producto.
            *   `sort_order` (PositiveSmallIntegerField): Define el orden de visualización de las imágenes.
            *   `page` (ParentalKey): Una clave foránea que enlaza esta imagen con una `ProductPage` (relación `shopify_images`).

### Relación con otros módulos y componentes

Esta migración interactúa con varios modelos existentes y sienta las bases para la sincronización de imágenes desde Shopify.

*   **Modelos de Contenido**:
    *   [shopify_content/models/blog.py::ArticlePage](../Blog_Content_Models.md): Se actualiza para incluir información detallada de la imagen destacada de Shopify.
    *   [shopify_content/models/collection.py::CollectionPage](../Collection_Content_Models.md): Se actualiza para incluir información de la imagen de la colección de Shopify.
    *   [shopify_content/models/product.py::ProductPage](../Product_Content_Models.md): Se convierte en el padre del nuevo modelo `ProductPageImage`, lo que permite una gestión flexible de múltiples imágenes por producto.
*   **Wagtail Images**:
    *   La dependencia de `wagtailimages` y la modificación del campo `featured_image` en `ArticlePage` indican una coexistencia entre las imágenes gestionadas directamente por Wagtail y las imágenes referenciadas por URL desde Shopify. Para más detalles sobre la gestión de imágenes de Wagtail, consulte la documentación de `wagtailimages`.

## Diagramas

### Diagrama de Relación de Modelos

El siguiente diagrama ilustra las relaciones entre los modelos de contenido afectados por esta migración.

```mermaid
erDiagram
    ArticlePage {
        uuid id PK
        CharField title
        URLField featured_image_url
        CharField featured_image_alt
        CharField shopify_featured_image_id
        ForeignKey featured_image
    }

    CollectionPage {
        uuid id PK
        CharField title
        URLField image_url
        CharField image_alt_text
        CharField shopify_image_id
    }

    ProductPage {
        uuid id PK
        CharField title
    }

    ProductPageImage {
        id PK
        CharField shopify_id
        URLField url
        CharField alt_text
        PositiveSmallIntegerField sort_order
        ParentalKey page FK
    }

    wagtailimages.Image {
        id PK
        CharField title
        FileField file
    }

    ArticlePage ||--o{ wagtailimages.Image : "featured_image (opcional)"
    ProductPage ||--o{ ProductPageImage : "shopify_images"
```

### Flujo de Datos (Conceptual) para Imágenes de Shopify

Este diagrama conceptual muestra cómo la información de la imagen podría fluir desde Shopify hacia los modelos de Wagtail, habilitado por los campos introducidos en esta migración.

```mermaid
graph TD
    A[Shopify Product/Collection Data] -->|Contiene URLs de Imagen y GIDs| B(Servicio de Sincronización de Contenido)
    B -->|Mapea y Almacena| C{Base de Datos Wagtail}

    C --> C1[ArticlePage]
    C --> C2[CollectionPage]
    C --> C3[ProductPage]
    C3 --> C4[ProductPageImage]

    C1 -- Datos de Imagen --> D[Campo: featured_image_url]
    C1 -- Datos de Imagen --> E[Campo: featured_image_alt]
    C1 -- Datos de Imagen --> F[Campo: shopify_featured_image_id]

    C2 -- Datos de Imagen --> G[Campo: image_url]
    C2 -- Datos de Imagen --> H[Campo: image_alt_text]
    C2 -- Datos de Imagen --> I[Campo: shopify_image_id]

    C4 -- Datos de Imagen --> J[Campo: url]
    C4 -- Datos de Imagen --> K[Campo: alt_text]
    C4 -- Datos de Imagen --> L[Campo: shopify_id]

    subgraph Legado Wagtail
        C1 -- Imagen Subida Manualmente --> M[Campo: featured_image (ForeignKey a wagtailimages.Image)]
    end

    style B fill:#f9f,stroke:#333,stroke-width:2px
    style C fill:#ccf,stroke:#333,stroke-width:2px
    style D fill:#ddf,stroke:#333,stroke-width:1px
    style E fill:#ddf,stroke:#333,stroke-width:1px
    style F fill:#ddf,stroke:#333,stroke-width:1px
    style G fill:#ddf,stroke:#333,stroke-width:1px
    style H fill:#ddf,stroke:#333,stroke-width:1px
    style I fill:#ddf,stroke:#333,stroke-width:1px
    style J fill:#ddf,stroke:#333,stroke-width:1px
    style K fill:#ddf,stroke:#333,stroke-width:1px
    style L fill:#ddf,stroke:#333,stroke-width:1px
    style M fill:#eee,stroke:#333,stroke-width:1px

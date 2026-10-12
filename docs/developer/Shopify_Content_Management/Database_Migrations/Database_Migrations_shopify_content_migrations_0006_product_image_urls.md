# Migración 0006_product_image_urls

La migración `0006_product_image_urls.py` es una migración de base de datos dentro del módulo `Shopify_Content_Management` que introduce mejoras significativas en la gestión de imágenes para `ArticlePage`, `CollectionPage` y `ProductPage`. Esta migración se enfoca en integrar directamente las URL e IDs de imágenes de Shopify, facilitando una sincronización más robusta y mejorando las capacidades de contenido.

## Propósito y Funcionalidad

Esta migración tiene como objetivo principal:

1.  **Extender los modelos `ArticlePage` y `CollectionPage`**: Añade campos para almacenar URL de imágenes, textos alternativos (alt text) e IDs de Shopify para las imágenes destacadas de artículos y las imágenes de colecciones.
2.  **Introducir el modelo `ProductPageImage`**: Crea un nuevo modelo para gestionar múltiples imágenes asociadas a una `ProductPage`, incluyendo sus URLs, IDs de Shopify y orden de visualización.
3.  **Optimizar la integración de imágenes con Shopify**: Permite que las páginas de contenido hagan referencia directa a imágenes alojadas en Shopify, lo que simplifica la gestión de activos y garantiza la coherencia con el catálogo de productos de Shopify.

## Arquitectura y Relaciones de Componentes

La migración modifica y extiende los modelos de la siguiente manera:

### Modelos Modificados

*   **`ArticlePage`**:
    *   `featured_image_alt` (CharField): Texto alternativo para la imagen destacada.
    *   `featured_image_url` (URLField): URL absoluta de la imagen destacada del artículo en Shopify.
    *   `shopify_featured_image_id` (CharField): GID (Global ID) de `MediaImage` de Shopify para la imagen destacada del artículo.
    *   `featured_image` (ForeignKey a `wagtailimages.Image`): Se ajusta el `help_text` para aclarar su uso en relación con `featured_image_url`, indicando que las imágenes importadas de Shopify usarán la URL directamente.

*   **`CollectionPage`**:
    *   `image_alt_text` (CharField): Texto alternativo para la imagen de la colección.
    *   `image_url` (URLField): URL absoluta de la imagen de la colección en Shopify.
    *   `shopify_image_id` (CharField): GID de `MediaImage` de Shopify para la imagen de la colección.

### Nuevo Modelo

*   **`ProductPageImage`**: Este nuevo modelo permite que una `ProductPage` tenga múltiples imágenes asociadas.
    *   `shopify_id` (CharField): GID de `MediaImage` de Shopify para la imagen del producto.
    *   `url` (URLField): URL CDN absoluta para usar en el atributo `img src`.
    *   `alt_text` (CharField): Texto alternativo para la imagen.
    *   `sort_order` (PositiveSmallIntegerField): Orden de clasificación de la imagen, con un valor predeterminado de 0.
    *   `page` (ParentalKey a `shopify_content.ProductPage`): Establece una relación uno a muchos, vinculando cada imagen a una `ProductPage` específica a través de `related_name='shopify_images'`.

### Diagrama de Relación de Modelos

El siguiente diagrama de Mermaid ilustra las modificaciones y la nueva relación de modelos introducidas por esta migración:

```mermaid
erDiagram
    ArticlePage {
        ...
        CharField featured_image_alt
        URLField featured_image_url
        CharField shopify_featured_image_id
        ForeignKey featured_image
    }
    CollectionPage {
        ...
        CharField image_alt_text
        URLField image_url
        CharField shopify_image_id
    }
    ProductPage {
        ...
    }
    ProductPageImage {
        BigAutoField id
        CharField shopify_id
        URLField url
        CharField alt_text
        PositiveSmallIntegerField sort_order
        ParentalKey page
    }

    ArticlePage ||--o{ wagtailimages.Image : "featured_image"
    ProductPage ||--o{ ProductPageImage : "shopify_images"
```

## Dependencias

Esta migración depende de:

*   `shopify_content.0005_alter_locationpage_shopify_locale`: Asegura que las migraciones del módulo `shopify_content` se apliquen en el orden correcto.
*   `wagtailimages.0027_image_description`: Indica que se basa en el esquema de imágenes de Wagtail, lo que sugiere una interacción con la gestión de imágenes base de Wagtail.

## Integración con el Sistema General

Esta migración es fundamental para la sección [Shopify_Content_Management](../Shopify_Content_Management.md) al fortalecer la capacidad del CMS para manejar activos de imagen de productos de Shopify de manera más eficiente y con mayor detalle. Al añadir campos explícitos para URLs de Shopify y GIDs, se mejora la:

*   **Coherencia de datos**: Se asegura que la información de la imagen en el CMS refleje con precisión los datos de Shopify.
*   **Capacidad SEO**: Los campos de texto alternativo contribuyen directamente a una mejor optimización para motores de búsqueda.
*   **Experiencia del usuario**: La capacidad de mostrar múltiples imágenes para productos a través de `ProductPageImage` enriquece el contenido de las páginas de productos.

Esta integración reduce la duplicación de datos de imagen y mejora el flujo de trabajo para la publicación de contenido que incluye imágenes gestionadas por Shopify. Los modelos afectados se describen en detalle en la documentación de [Content_Page_Models](../Content_Page_Models.md).
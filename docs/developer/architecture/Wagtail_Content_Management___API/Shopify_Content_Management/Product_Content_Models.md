# Modelos de Contenido de Producto

Este módulo define los modelos de Wagtail para gestionar el contenido de los productos de Shopify, permitiendo la sincronización bidireccional de datos entre Wagtail y Shopify. Extiende las capacidades de Wagtail para representar productos, sus imágenes, preguntas frecuentes, meta campos y etiquetas de forma estructurada.

## Arquitectura y Componentes

El módulo `Product_Content_Models` se compone de varias clases de modelos de Django que, en conjunto, forman la representación de un producto de Shopify dentro del sistema de gestión de contenido de Wagtail. Estos modelos heredan de `wagtail.models.Page` o `django.db.models.Model` y utilizan `modelcluster` para manejar relaciones complejas y etiquetas.

```mermaid
C4Context
    title Diagrama de Clases del Módulo Product_Content_Models

    class ProductPage {
        + shopify_id: CharField
        + handle: SlugField
        + sync_enabled: BooleanField
        + last_synced_at: DateTimeField
        + theme_config: JSONField
        + vendor: CharField
        + product_type: CharField
        + tags: ClusterTaggableManager
        + status: CharField
        + body: StreamField
    }

    class ProductPageTag {
        + content_object: ParentalKey (a ProductPage)
    }

    class ProductPageFAQ {
        + page: ParentalKey (a ProductPage)
    }

    class ProductPageMetafield {
        + page: ParentalKey (a ProductPage)
    }

    class ProductPageImage {
        + page: ParentalKey (a ProductPage)
        + shopify_id: CharField
        + url: URLField
        + alt_text: CharField
        + sort_order: PositiveSmallIntegerField
    }

    ProductPage --|> Page : hereda
    ProductPage "1" -- "*" ProductPageTag : tiene
    ProductPage "1" -- "*" ProductPageFAQ : tiene
    ProductPage "1" -- "*" ProductPageMetafield : tiene
    ProductPage "1" -- "*" ProductPageImage : tiene
    ProductPageTag --|> TaggedItemBase : hereda
    ProductPageFAQ --|> FAQItem : hereda
    ProductPageMetafield --|> ShopifyMetafield : hereda
    ProductPageImage --|> models.Model : hereda

    note for ProductPage
        Página principal de Wagtail para representar un producto de Shopify.
        Gestiona la sincronización, detalles del producto y contenido editorial.
    end note
    note for ProductPageImage
        Almacena la URL de la imagen del producto Shopify localmente.
    end note
```

### Relación con otros módulos

Este módulo se integra con varios otros módulos clave dentro del sistema:

*   **`shopify_content.models.mixins`**: `ProductPageFAQ` y `ProductPageMetafield` heredan de `FAQItem` y `ShopifyMetafield` respectivamente, lo que proporciona una estructura común para los elementos de preguntas frecuentes y los meta campos en todas las páginas de contenido de Shopify. Más detalles en [Mixins Base de Contenido](Content_Base_Models___Mixins/Content_Base_Models___Mixins_MixinsBase.md).
*   **`wagtail.models.Page`**: `ProductPage` hereda directamente de la clase `Page` de Wagtail, lo que le permite funcionar como una página en el CMS de Wagtail con todas las características asociadas, como la gestión de versiones, la publicación y la estructura jerárquica. Esto se alinea con la [Aplicación Central de Wagtail y la Integración de la UI](Admin___Wagtail_UI_Integration.md).
*   **`modelcluster.contrib.taggit.ClusterTaggableManager`**: Utilizado por `ProductPage` para la gestión de etiquetas a través de `ProductPageTag`, permitiendo una categorización flexible de productos. Esta es una integración estándar de Django con `django-taggit` y `django-modelcluster`.
*   **`shopify_content.blocks`**: El campo `body` de `ProductPage` utiliza `StreamField` con bloques definidos en `PRODUCT_BODY_BLOCKS`. Estos bloques estructuran el contenido enriquecido del producto para su renderizado en Shopify. Véase [Bloques StreamField de Wagtail](Wagtail_StreamField_Blocks.md) para más información.
*   **`shopify_content.admin_panels`**: Los paneles de administración para `ProductPage` utilizan `semantic_links_panels`, `SHOPIFY_SYNC_PANELS` y `SHOPIFY_SEO_PANELS` para organizar la interfaz de usuario en el CMS de Wagtail. Estos paneles son cruciales para la experiencia de edición del contenido de Shopify. Más detalles sobre la configuración de paneles se encuentran en [Integración UI de Administración y Wagtail](Admin___Wagtail_UI_Integration.md).

## Componentes del Módulo

### `ProductPage`

Representa un producto de Shopify dentro de Wagtail. Actúa como el modelo central para gestionar todos los aspectos del contenido de un producto, incluyendo datos sincronizados desde Shopify y contenido editorial enriquecido gestionado en Wagtail.

*   **Campos de sincronización de Shopify**: `shopify_id`, `handle`, `sync_enabled`, `last_synced_at` y `theme_config` facilitan la sincronización bidireccional de datos con Shopify.
*   **Campos específicos del producto**: `vendor`, `product_type`, `tags` y `status` almacenan información detallada del producto.
*   **Contenido del cuerpo**: El `StreamField` `body` permite a los editores construir descripciones de productos ricas y estructuradas utilizando varios bloques de contenido definidos en `PRODUCT_BODY_BLOCKS`.
*   **Paneles de administración**: Organiza la interfaz de edición de Wagtail en pestañas para Contenido, SEO/Promoción y Shopify, mejorando la usabilidad para los editores.

### `ProductPage.Meta`

Define las opciones de metadatos para el modelo `ProductPage`, incluyendo `verbose_name` y `verbose_name_plural` para una mejor representación en la interfaz de administración de Django y Wagtail.

### `ProductPageFAQ`

Modelo en línea para gestionar las preguntas frecuentes (FAQ) asociadas a una `ProductPage`. Hereda de `FAQItem`, proporcionando campos para preguntas y respuestas.

### `ProductPageMetafield`

Modelo en línea para gestionar los meta campos de Shopify asociados a una `ProductPage`. Hereda de `ShopifyMetafield`, permitiendo la extensión flexible de los datos del producto con meta campos personalizados de Shopify.

### `ProductPageImage`

Almacena la información de la imagen del producto de Shopify, específicamente la URL del CDN y el texto alternativo. No descarga la imagen, sino que hace referencia a ella a través de la URL.

*   **Campos**: `shopify_id`, `url`, `alt_text`, `sort_order`.
*   **Meta**: Define el orden por `sort_order` y `id`.
*   **Paneles**: `url`, `alt_text`, `sort_order` para la edición en el administrador.

### `ProductPageImage.Meta`

Define las opciones de metadatos para el modelo `ProductPageImage`, especificando el ordenamiento y los nombres detallados para las imágenes del producto.

### `ProductPageTag`

Modelo de unión para gestionar las relaciones de etiquetas con `ProductPage` utilizando `django-taggit` y `django-modelcluster`.
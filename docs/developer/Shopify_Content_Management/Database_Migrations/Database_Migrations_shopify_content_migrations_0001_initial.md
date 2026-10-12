# Migración Inicial de Base de Datos de Contenido de Shopify (0001)

## Introducción

Este documento detalla la migración inicial `0001_initial.py` para el módulo `shopify_content`. Esta migración es fundamental para establecer la estructura base de la base de datos necesaria para gestionar diversos tipos de contenido en Shopify, incluyendo páginas de blogs, colecciones, productos y artículos, así como la página raíz de Shopify y los metacampos asociados.

## Arquitectura y Componentes

El componente principal de este módulo es la clase `Migration`, que define las operaciones de la base de datos para crear las tablas iniciales y sus campos. Esta migración establece la base para los siguientes modelos de contenido de Wagtail integrados con Shopify:

*   **BlogPage**: Representa una página de blog en Shopify.
*   **CollectionPage**: Representa una página de colección de productos en Shopify.
*   **ProductPage**: Representa una página de producto en Shopify.
*   **ShopifyRootPage**: Una página raíz que sirve como contenedor para todo el contenido de Shopify.
*   **ArticlePage**: Representa un artículo dentro de un blog de Shopify.
*   **Metafield Models (ArticlePageMetafield, CollectionPageMetafield, ProductPageMetafield)**: Modelos para almacenar metacampos personalizados asociados a las páginas de artículos, colecciones y productos.
*   **Tag Models (ArticlePageTag, ProductPageTag)**: Modelos para gestionar las etiquetas asociadas a las páginas de artículos y productos.

### Dependencias de Migración

Esta migración tiene dependencias de otras migraciones de Django y Wagtail para asegurar que las tablas base existan antes de su ejecución:

*   `taggit.0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx`
*   `wagtailcore.0097_baselogentry_uuid_action_timestamp_indexes`
*   `wagtailimages.0027_image_description`

## Relaciones con Otros Módulos

Esta migración define la estructura de la base de datos para los modelos que se describen en detalle en el módulo [Content_Page_Models](../Content_Page_Models.md). Los `StreamField` utilizados en `CollectionPage`, `ProductPage` y `ArticlePage` hacen uso de los bloques definidos en [Wagtail_StreamField_Blocks](../../Wagtail_StreamField_Blocks.md), especialmente `shopify_content.blocks.content.HtmlBlock` y los bloques estándar de Wagtail.

## Diagramas

### Diagrama de Entidad-Relación (ERD) de Modelos de Contenido Iniciales

```mermaid
erDiagram
    Page ||--o{ BlogPage : "hereda de"
    Page ||--o{ CollectionPage : "hereda de"
    Page ||--o{ ProductPage : "hereda de"
    Page ||--o{ ShopifyRootPage : "hereda de"
    Page ||--o{ ArticlePage : "hereda de"

    BlogPage { 
        CharField shopify_id 
        SlugField handle 
        BooleanField sync_enabled 
        DateTimeField last_synced_at 
        CharField comment_policy 
    }
    CollectionPage {
        CharField shopify_id
        SlugField handle
        BooleanField sync_enabled
        DateTimeField last_synced_at
        CharField sort_order
        StreamField description
    }
    ProductPage {
        CharField shopify_id
        SlugField handle
        BooleanField sync_enabled
        DateTimeField last_synced_at
        CharField vendor
        CharField product_type
        CharField status
        StreamField body
    }
    ShopifyRootPage {
        (hereda de Page)
    }
    ArticlePage {
        CharField shopify_id
        SlugField handle
        BooleanField sync_enabled
        DateTimeField last_synced_at
        CharField author
        DateTimeField published_at
        TextField summary
        StreamField body
        ForeignKey featured_image
    }

    ArticlePage ||--o{ ArticlePageMetafield : "tiene muchos"
    ArticlePage ||--o{ ArticlePageTag : "tiene muchos"
    CollectionPage ||--o{ CollectionPageMetafield : "tiene muchos"
    ProductPage ||--o{ ProductPageMetafield : "tiene muchos"
    ProductPage ||--o{ ProductPageTag : "tiene muchos"

    ArticlePageMetafield {
        CharField namespace
        CharField key
        CharField type
        TextField value
    }
    CollectionPageMetafield {
        CharField namespace
        CharField key
        CharField type
        TextField value
    }
    ProductPageMetafield {
        CharField namespace
        CharField key
        CharField type
        TextField value
    }
    ArticlePageTag {
        ForeignKey tag
    }
    ProductPageTag {
        ForeignKey tag
    }
    Image ||--o{ ArticlePage : "imagen destacada"
    Tag ||--o{ ArticlePageTag : "utilizado por"
    Tag ||--o{ ProductPageTag : "utilizado por"

```

### Diagrama de Bloques StreamField

Este diagrama ilustra los tipos de bloques de contenido que pueden ser utilizados dentro de los `StreamField` de los modelos de páginas, según lo definido en esta migración. Estos bloques son fundamentales para la creación de contenido rico y estructurado.

```mermaid
C4Context
    title Diagrama de Bloques StreamField

    System_Ext(wagtail_blocks, "Bloques Estándar de Wagtail", "Bloques fundamentales proporcionados por Wagtail para la estructuración de contenido.")
    System(shopify_content_blocks, "Bloques de Contenido de Shopify", "Bloques personalizados para el contenido de Shopify.")

    Container(html_block, "HtmlBlock", "Permite insertar HTML arbitrario.", "shopify_content.blocks.content")

    Rel(wagtail_blocks, html_block, "Define un bloque básico de texto enriquecido usado por")

    Container(heading_block, "HeadingBlock", "Bloques para títulos (h2, h3, h4).", "wagtail.blocks.StructBlock")
    Container(paragraph_block, "ParagraphBlock", "Bloques para párrafos de texto enriquecido.", "wagtail.blocks.StructBlock")
    Container(image_block, "ImageBlock", "Bloques para la inclusión de imágenes con texto alternativo y subtítulos.", "wagtail.blocks.StructBlock")
    Container(video_embed_block, "VideoEmbedBlock", "Bloques para incrustar videos de YouTube/Vimeo.", "wagtail.blocks.StructBlock")
    Container(callout_block, "CalloutBlock", "Bloques para citas o avisos destacados.", "wagtail.blocks.StructBlock")
    Container(product_feature_block, "ProductFeatureBlock", "Bloques para destacar características de productos con íconos, títulos y descripciones.", "wagtail.blocks.StructBlock")
    Container(metafield_block, "MetafieldBlock", "Bloques para gestionar metacampos de Shopify.", "wagtail.blocks.StructBlock")

    Rel(wagtail_blocks, heading_block, "Proporciona")
    Rel(wagtail_blocks, paragraph_block, "Proporciona")
    Rel(wagtail_blocks, image_block, "Proporciona")
    Rel(wagtail_blocks, video_embed_block, "Proporciona")
    Rel(wagtail_blocks, callout_block, "Proporciona")
    Rel(wagtail_blocks, product_feature_block, "Proporciona")
    Rel(wagtail_blocks, metafield_block, "Proporciona")

    Boundary(blog_streamfield, "BlogPage.body StreamField") {
        Rel(blog_streamfield, heading_block, "Utiliza")
        Rel(blog_streamfield, paragraph_block, "Utiliza")
        Rel(blog_streamfield, image_block, "Utiliza")
        Rel(blog_streamfield, video_embed_block, "Utiliza")
        Rel(blog_streamfield, callout_block, "Utiliza")
        Rel(blog_streamfield, html_block, "Utiliza")
    }

    Boundary(collection_streamfield, "CollectionPage.description StreamField") {
        Rel(collection_streamfield, heading_block, "Utiliza")
        Rel(collection_streamfield, paragraph_block, "Utiliza")
        Rel(collection_streamfield, image_block, "Utiliza")
        Rel(collection_streamfield, callout_block, "Utiliza")
        Rel(collection_streamfield, html_block, "Utiliza")
    }

    Boundary(product_streamfield, "ProductPage.body StreamField") {
        Rel(product_streamfield, heading_block, "Utiliza")
        Rel(product_streamfield, paragraph_block, "Utiliza")
        Rel(product_streamfield, image_block, "Utiliza")
        Rel(product_streamfield, video_embed_block, "Utiliza")
        Rel(product_streamfield, product_feature_block, "Utiliza")
        Rel(product_streamfield, callout_block, "Utiliza")
        Rel(product_streamfield, html_block, "Utiliza")
        Rel(product_streamfield, metafield_block, "Utiliza")
    }

```

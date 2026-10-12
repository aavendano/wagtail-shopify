# Migración Database_Migrations_0001_initial

## Introducción

Este documento detalla la migración inicial `0001_initial.py` del módulo `shopify_content`, que establece la estructura fundamental de la base de datos para la integración de contenido de Shopify dentro del CMS Wagtail. Esta migración crea las tablas iniciales para gestionar blogs, colecciones, productos y artículos, junto con sus metacampos y etiquetas asociados.

## Propósito y Funcionalidad Principal

El propósito principal de esta migración es inicializar el esquema de la base de datos para la aplicación `shopify_content`. Define los modelos Django que representan las páginas de contenido de Shopify (Blogs, Colecciones, Productos y Artículos) y sus componentes relacionados, como metacampos y etiquetas, lo que permite su almacenamiento y gestión dentro de Wagtail.

Las funcionalidades clave habilitadas por esta migración incluyen:
*   **Gestión de Páginas de Contenido**: Creación de tipos de página específicos de Shopify que heredan de `wagtailcore.Page`.
*   **Sincronización con Shopify**: Campos para almacenar identificadores de Shopify (GID), handles (slugs), estado de sincronización y fecha de la última sincronización.
*   **Metacampos Personalizables**: Soporte para metacampos asociados a Artículos, Colecciones y Productos, permitiendo almacenar datos adicionales específicos de Shopify.
*   **Etiquetado**: Implementación de un sistema de etiquetado para Artículos y Productos utilizando `django-taggit`.
*   **Contenido Estructurado**: Utilización de `StreamField` de Wagtail para definir el cuerpo de las páginas de Colección, Producto y Artículo, permitiendo contenido rico y flexible.

## Arquitectura y Relaciones de Componentes

La migración `0001_initial.py` establece las siguientes tablas y relaciones en la base de datos. Los modelos de contenido heredan de `wagtailcore.Page`, lo que los integra en la jerarquía de páginas de Wagtail.

### Diagrama de Entidad-Relación Inicial

```mermaid
erDiagram
    "wagtailcore.Page" {
        id PK
        title VARCHAR
        slug VARCHAR
        path VARCHAR
        depth INTEGER
        numchild INTEGER
        url_path TEXT
    }
    "wagtailimages.Image" {
        id PK
        file VARCHAR
        title VARCHAR
        width INTEGER
        height INTEGER
    }
    "taggit.Tag" {
        id PK
        name VARCHAR
        slug VARCHAR
    }

    "shopify_content.ShopifyRootPage" {
        page_ptr_id PK, FK "wagtailcore.Page"
    }
    "shopify_content.BlogPage" {
        page_ptr_id PK, FK "wagtailcore.Page"
        shopify_id VARCHAR "GID de Shopify, ej. gid://shopify/Blog/12345678"
        handle VARCHAR "Handle de Shopify"
        sync_enabled BOOLEAN "Habilitar sincronización con Shopify"
        last_synced_at DATETIME "Marca de tiempo de la última sincronización"
        comment_policy VARCHAR "Política de comentarios del blog"
    }
    "shopify_content.CollectionPage" {
        page_ptr_id PK, FK "wagtailcore.Page"
        shopify_id VARCHAR "GID de Shopify, ej. gid://shopify/Collection/12345678"
        handle VARCHAR "Handle de Shopify"
        sync_enabled BOOLEAN "Habilitar sincronización con Shopify"
        last_synced_at DATETIME "Marca de tiempo de la última sincronización"
        sort_order VARCHAR "Orden de clasificación de la colección"
        description JSON "Contenido StreamField de la descripción"
    }
    "shopify_content.ProductPage" {
        page_ptr_id PK, FK "wagtailcore.Page"
        shopify_id VARCHAR "GID de Shopify, ej. gid://shopify/Product/12345678"
        handle VARCHAR "Handle de Shopify"
        sync_enabled BOOLEAN "Habilitar sincronización con Shopify"
        last_synced_at DATETIME "Marca de tiempo de la última sincronización"
        vendor VARCHAR "Vendedor del producto"
        product_type VARCHAR "Tipo de producto"
        status VARCHAR "Estado del producto"
        body JSON "Contenido StreamField del cuerpo"
    }
    "shopify_content.ArticlePage" {
        page_ptr_id PK, FK "wagtailcore.Page"
        shopify_id VARCHAR "GID de Shopify, ej. gid://shopify/Article/12345678"
        handle VARCHAR "Handle de Shopify"
        sync_enabled BOOLEAN "Habilitar sincronización con Shopify"
        last_synced_at DATETIME "Marca de tiempo de la última sincronización"
        author VARCHAR "Autor del artículo"
        published_at DATETIME "Fecha de publicación"
        summary TEXT "Resumen del artículo"
        body JSON "Contenido StreamField del cuerpo"
        featured_image_id FK "wagtailimages.Image" "Imagen destacada"
    }

    "shopify_content.ArticlePageMetafield" {
        id PK
        page_id FK "shopify_content.ArticlePage"
        namespace VARCHAR "Namespace del metafield"
        key VARCHAR "Clave del metafield"
        type VARCHAR "Tipo de datos del metafield"
        value TEXT "Valor del metafield"
    }
    "shopify_content.ArticlePageTag" {
        id PK
        content_object_id FK "shopify_content.ArticlePage" "Artículo asociado"
        tag_id FK "taggit.Tag" "Etiqueta asociada"
    }
    "shopify_content.CollectionPageMetafield" {
        id PK
        page_id FK "shopify_content.CollectionPage"
        namespace VARCHAR "Namespace del metafield"
        key VARCHAR "Clave del metafield"
        type VARCHAR "Tipo de datos del metafield"
        value TEXT "Valor del metafield"
    }
    "shopify_content.ProductPageMetafield" {
        id PK
        page_id FK "shopify_content.ProductPage"
        namespace VARCHAR "Namespace del metafield"
        key VARCHAR "Clave del metafield"
        type VARCHAR "Tipo de datos del metafield"
        value TEXT "Valor del metafield"
    }
    "shopify_content.ProductPageTag" {
        id PK
        content_object_id FK "shopify_content.ProductPage" "Producto asociado"
        tag_id FK "taggit.Tag" "Etiqueta asociada"
    }

    "wagtailcore.Page" ||--o{ "shopify_content.ShopifyRootPage" : "hereda"
    "wagtailcore.Page" ||--o{ "shopify_content.BlogPage" : "hereda"
    "wagtailcore.Page" ||--o{ "shopify_content.CollectionPage" : "hereda"
    "wagtailcore.Page" ||--o{ "shopify_content.ProductPage" : "hereda"
    "wagtailcore.Page" ||--o{ "shopify_content.ArticlePage" : "hereda"

    "wagtailimages.Image" ||--o{ "shopify_content.ArticlePage" : "tiene imagen destacada"

    "shopify_content.ArticlePage" ||--o{ "shopify_content.ArticlePageMetafield" : "tiene metacampos"
    "shopify_content.ArticlePage" ||--o{ "shopify_content.ArticlePageTag" : "está etiquetado con"
    "taggit.Tag" ||--o{ "shopify_content.ArticlePageTag" : "asocia"

    "shopify_content.CollectionPage" ||--o{ "shopify_content.CollectionPageMetafield" : "tiene metacampos"

    "shopify_content.ProductPage" ||--o{ "shopify_content.ProductPageMetafield" : "tiene metacampos"
    "shopify_content.ProductPage" ||--o{ "shopify_content.ProductPageTag" : "está etiquetado con"
    "taggit.Tag" ||--o{ "shopify_content.ProductPageTag" : "asocia"
```

### Descripción de los Componentes Creados

Esta migración crea las siguientes tablas en la base de datos:

*   **`shopify_content_blogpage`**: Representa una página de blog importada o gestionada para Shopify. Incluye campos para el GID de Shopify, el handle, la política de comentarios y el estado de sincronización.
*   **`shopify_content_collectionpage`**: Representa una página de colección de productos de Shopify. Incluye campos para el GID de Shopify, el handle, el orden de clasificación y un `StreamField` para la descripción de la colección.
*   **`shopify_content_productpage`**: Representa una página de producto de Shopify. Incluye campos para el GID de Shopify, el handle, el vendedor, el tipo de producto, el estado y un `StreamField` para el cuerpo del producto.
*   **`shopify_content_shopifyrootpage`**: Una página raíz especial en Wagtail que sirve como contenedor para todas las páginas de contenido relacionadas con Shopify.
*   **`shopify_content_articlepage`**: Representa un artículo de blog importado o gestionado para Shopify. Incluye campos para el GID de Shopify, el handle, autor, fecha de publicación, un resumen, un `StreamField` para el cuerpo del artículo y una imagen destacada.
*   **`shopify_content_articlepagemetafield`**: Una tabla intermedia para almacenar metacampos personalizados asociados a una `ArticlePage`.
*   **`shopify_content_articlepagetag`**: Una tabla intermedia para gestionar las relaciones muchos a muchos entre `ArticlePage` y `taggit.Tag`.
*   **`shopify_content_collectionpagemetafield`**: Una tabla intermedia para almacenar metacampos personalizados asociados a una `CollectionPage`.
*   **`shopify_content_productpagemetafield`**: Una tabla intermedia para almacenar metacampos personalizados asociados a una `ProductPage`.
*   **`shopify_content_productpagetag`**: Una tabla intermedia para gestionar las relaciones muchos a muchos entre `ProductPage` y `taggit.Tag`.

## Integración en el Sistema General

Esta migración es un componente fundacional del módulo [Shopify Content Management](../../Shopify_Content_Management.md). Al establecer el esquema de la base de datos para los tipos de contenido de Shopify, permite que el sistema Wagtail almacene, edite y sincronice de manera efectiva el contenido con la plataforma Shopify.

Las tablas creadas por esta migración son utilizadas por:
*   **Modelos de Contenido**: Los modelos definidos aquí (`BlogPage`, `CollectionPage`, etc.) son la base para la gestión de contenido en [Blog Content Models](../Blog_Content_Models.md), [Collection Content Models](../Collection_Content_Models.md), [Product Content Models](../Product_Content_Models.md), y [Home Page Models](../Home_Page_Models.md) (aunque `HomePage` no se define en esta migración inicial, `ShopifyRootPage` proporciona la raíz para estas páginas).
*   **Administración Wagtail**: La interfaz de administración de Wagtail utiliza estos modelos para permitir a los editores crear y gestionar el contenido de Shopify.
*   **Sincronización de Contenido**: Los campos `shopify_id`, `handle`, `sync_enabled` y `last_synced_at` son cruciales para los servicios de sincronización que interactúan con la API de Shopify, como se detalla en [Content Synchronization Services](../Content_Synchronization_Services.md).
*   **API de Contenido Shopify**: La [Shopify Content API](../../Shopify_Content_API.md) expone y consume datos basados en el esquema definido en esta migración.

Sin esta migración, el módulo de gestión de contenido de Shopify no podría persistir los datos en la base de datos, lo que haría inoperable gran parte de la funcionalidad de integración con Shopify. Esta migración sirve como el punto de partida para la evolución del esquema de la base de datos de contenido de Shopify, con migraciones posteriores que agregan más campos y funcionalidades, como se ve en [Database Migrations](../Database_Migrations.md).

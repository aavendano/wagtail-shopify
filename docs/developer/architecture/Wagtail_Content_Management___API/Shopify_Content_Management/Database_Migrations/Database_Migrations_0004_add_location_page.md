# Migración de Base de Datos 0004: Añadir Página de Localización

Este módulo de migración de Django (`0004_add_location_page.py`) es responsable de introducir los modelos `LocationPage` y `LocationPageFAQ` en la base de datos. Estos modelos están diseñados para gestionar contenido relacionado con ubicaciones dentro del sistema de gestión de contenido de Wagtail, integrándose con la plataforma Shopify.

## Propósito y Funcionalidad Principal

La migración `0004_add_location_page` extiende el esquema de la base de datos para soportar la creación y gestión de páginas de localización. Permite a los administradores de contenido definir páginas específicas para diferentes ubicaciones, con campos para títulos, subtítulos, contenido enriquecido, información geográfica (país, estado, ciudad) y secciones de marca, así como preguntas frecuentes asociadas a cada página de localización.

### Componentes Principales

El componente principal en este módulo es la clase `Migration`:

*   `shopify_content/migrations/0004_add_location_page.py::Migration`: Define las operaciones de base de datos para crear los modelos `LocationPage` y `LocationPageFAQ` y sus campos asociados.

## Arquitectura y Relaciones entre Componentes

Esta migración introduce dos modelos clave:

1.  **`LocationPage`**: Hereda de `wagtailcore.page`, lo que la convierte en una página de Wagtail estándar. Incluye campos para la integración con Shopify (ID de Shopify, handle, estado de sincronización, última sincronización) y varios campos de contenido localizable para describir una ubicación.
2.  **`LocationPageFAQ`**: Un modelo de `ClusterableModel` que permite adjuntar múltiples preguntas frecuentes a una `LocationPage` específica. Contiene campos para la pregunta, la respuesta y el orden de clasificación.

### Diagrama de Relación de Modelos

```mermaid
ERD
    LocationPage {
        page_ptr PK, FK 
        shopify_id varchar
        handle varchar
        sync_enabled boolean
        last_synced_at datetime
        titulo varchar
        subtitulo varchar
        intro richtext
        country varchar
        state varchar
        city varchar
        titulo_2 varchar
        subtitulo_h2 varchar
        content_2 richtext
        titulo_3 varchar
        subtitulo_3 varchar
        content_3 richtext
        brand_section_title varchar
        brand_section_subtitle varchar
        brand_section_content richtext
        map_title varchar
        map_content richtext
        after_page_content richtext
        shopify_locale varchar
    }
    LocationPageFAQ {
        id PK
        sort_order integer
        question varchar
        answer text
        page_id FK "relates to"
    }
    wagtailcore.page { 
        id PK 
    }

    LocationPage ||--o{ LocationPageFAQ : "contiene FAQs"
    LocationPage }|--|| wagtailcore.page : "hereda de"
```

## Cómo encaja el módulo en el sistema general

Esta migración es una parte integral del sistema de [Gestión de Contenido de Shopify](../../Shopify_Content_Management.md) basado en Wagtail. Facilita la creación de una rica experiencia de usuario para páginas de localización, permitiendo a los equipos de contenido gestionar información específica de la ubicación directamente desde el CMS de Wagtail. Los datos de estas páginas pueden ser sincronizados con Shopify para su uso en la tienda online.

La `LocationPage` se integra con el ecosistema de Wagtail como un tipo de página más, permitiendo la gestión de su estructura en el árbol de páginas. La integración con Shopify se realiza a través de los campos `shopify_id`, `handle`, `sync_enabled` y `last_synced_at`, que permiten la sincronización bidireccional de metadatos y contenido entre Wagtail y Shopify.

Este módulo depende de la migración anterior `0003_add_faq_items` (ver [Migración 0003](Database_Migrations_0003_add_faq_items.md)) para los elementos base de FAQ, y de `wagtailcore` para la funcionalidad de página básica. Las páginas de localización se utilizan en el [Sistema de Exportación de Contenido](../Content_Export_Configuration.md) para generar listados específicos de ubicaciones (`LocationIndexConsumer`). También se relaciona con los [Modelos de Contenido de Localización](../Location_Content_Models.md) donde `LocationPage` y `LocationPageFAQ` son definidos como modelos ORM.
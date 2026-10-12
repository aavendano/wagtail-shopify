# Modelo ShopifyRootPage

El módulo `Content_Base_Models___Mixins_ShopifyRootPage_Modelo` define la `ShopifyRootPage`, una página central en Wagtail que sirve como la raíz para todos los tipos de contenido sincronizados con Shopify. Este modelo es fundamental para establecer la jerarquía del contenido y facilitar la sincronización bidireccional entre el CMS de Wagtail y los metaobjects de Shopify.

## Funcionalidad Principal

La `ShopifyRootPage` extiende la funcionalidad básica de una página de Wagtail para incluir atributos específicos necesarios para la integración con Shopify y la gestión de contenido editorial.

*   **Página Raíz de Contenido Shopify**: Actúa como el contenedor principal para diversas páginas de contenido relacionadas con Shopify, incluyendo productos, colecciones, blogs, ubicaciones, términos de glosario y la página de inicio. Esto asegura una estructura organizada para el contenido integrado.
*   **Sincronización con Metaobjects de Shopify**: Cada instancia de `ShopifyRootPage` está diseñada para sincronizarse con un metaobject de Shopify de tipo `root_page`. Esto se gestiona a través de los siguientes campos:
    *   `shopify_id`: El ID de GID del metaobject de Shopify, que se rellena después de la primera operación de upsert (crear/actualizar).
    *   `handle`: El "handle" del metaobject de Shopify, que por defecto utiliza el slug de la página de Wagtail si no se proporciona explícitamente.
    *   `sync_enabled`: Un campo booleano que permite habilitar o deshabilitar la sincronización de esta página raíz y, por extensión, de su contenido hijo con Shopify.
    *   `last_synced_at`: Una marca de tiempo que registra la última vez que la página fue sincronizada con Shopify.
*   **Configuración de Exportación (`export_config`)**: Un campo JSON que permite definir configuraciones específicas para temas o escaparates. Esta configuración se envía como parte del payload al campo `config` del metaobject de Shopify, permitiendo una personalización flexible de cómo el contenido se presenta en el storefront.
*   **Gestión de Jerarquía de Páginas**: Define explícitamente los tipos de páginas padre (`parent_page_types`) y los tipos de subpáginas (`subpage_types`) que puede contener, asegurando una estructura de contenido coherente y controlada dentro de Wagtail.
*   **Interfaz de Administración Wagtail**: Utiliza paneles de Wagtail (`content_panels`, `promote_panels`, `settings_panels`) y un `TabbedInterface` (`edit_handler`) para organizar la edición del contenido, SEO y configuraciones de sincronización en la interfaz de administración.
*   **Funcionalidades SEO**: Proporciona métodos (`get_seo_title`, `get_seo_description`) para recuperar metadatos SEO, utilizando los campos de SEO de Wagtail o los títulos y descripciones de la página si no se especifican metadatos SEO explícitos.

## Arquitectura y Relaciones de Componentes

El modelo `ShopifyRootPage` se integra en la arquitectura de Wagtail como una `Page` y establece relaciones clave con otros componentes del sistema para lograr su funcionalidad de gestión y sincronización de contenido.

### Diagrama de Clases

```mermaid
classDiagram
    direction LR
    class Page {
        +content_panels
    }
    class ShopifyRootPage {
        +shopify_id: CharField
        +handle: SlugField
        +sync_enabled: BooleanField
        +last_synced_at: DateTimeField
        +export_config: JSONField
        +parent_page_types: list
        +subpage_types: list
        +template: str
        +save()
        +get_resource_type()
        +get_seo_title()
        +get_seo_description()
    }
    class ProductPage {
        // ...
    }
    class CollectionPage {
        // ...
    }
    class BlogPage {
        // ...
    }
    class LocationPage {
        // ...
    }
    class GlossaryTermPage {
        // ...
    }
    class HomePage {
        // ...
    }

    Page <|-- ShopifyRootPage
    ShopifyRootPage --> ProductPage : Puede contener
    ShopifyRootPage --> CollectionPage : Puede contener
    ShopifyRootPage --> BlogPage : Puede contener
    ShopifyRootPage --> LocationPage : Puede contener
    ShopifyRootPage --> GlossaryTermPage : Puede contener
    ShopifyRootPage --> HomePage : Puede contener

    note for ShopifyRootPage "Gestiona la UI del administrador con:\n- content_panels (extendido de Page)\n- promote_panels (usa SHOPIFY_SEO_PANELS)\n- settings_panels (usa SHOPIFY_SYNC_PANELS)\n- edit_handler (TabbedInterface)" as WagtailUI
    ShopifyRootPage .. WagtailUI

    link ProductPage "Wagtail_Content_Management___API/Shopify_Content_Management/Product_Content_Models.md" "Ver Modelo Producto"
    link CollectionPage "Wagtail_Content_Management___API/Shopify_Content_Management/Collection_Content_Models.md" "Ver Modelo Colección"
    link BlogPage "Wagtail_Content_Management___API/Shopify_Content_Management/Blog_Content_Models.md" "Ver Modelo Blog"
    link LocationPage "Wagtail_Content_Management___API/Shopify_Content_Management/Location_Content_Models.md" "Ver Modelo Ubicación"
    link GlossaryTermPage "Wagtail_Content_Management___API/Shopify_Content_Management/Glossary_Content_Models.md" "Ver Modelo Glosario"
    link HomePage "Wagtail_Content_Management___API/Shopify_Content_Management/Home_Page_Models.md" "Ver Modelo Página Principal"
```

### Componentes Clave y Relaciones

*   **Herencia de `wagtail.models.Page`**: `ShopifyRootPage` hereda todas las características base de una página de Wagtail, lo que le permite encajar perfectamente en la estructura de árbol del CMS y utilizar las funcionalidades administrativas estándar.
*   **Relación con Modelos de Contenido Específicos**: A través de `subpage_types`, `ShopifyRootPage` define qué otros modelos de contenido de Shopify puede contener directamente. Esto incluye:
    *   `shopify_content.ProductPage`: Para la gestión de contenido relacionado con productos.
    *   `shopify_content.CollectionPage`: Para la gestión de contenido relacionado con colecciones.
    *   `shopify_content.BlogPage`: Para la gestión de blogs y artículos.
    *   `shopify_content.LocationPage`: Para páginas de contenido geolocalizado.
    *   `shopify_content.GlossaryTermPage`: Para términos de glosario.
    *   `shopify_content.HomePage`: Para la página de inicio del sitio.
    Estas relaciones establecen una estructura de contenido clara y modular, donde la `ShopifyRootPage` actúa como un orquestador para el contenido específico de Shopify. Cada uno de estos modelos se documenta en su respectivo módulo: [Modelo Producto](../Product_Content_Models.md), [Modelo Colección](../Collection_Content_Models.md), [Modelo Blog](../Blog_Content_Models.md), [Modelo Ubicación](../Location_Content_Models.md), [Modelo Glosario](../Glossary_Content_Models.md), [Modelo Página Principal](../Home_Page_Models.md).
*   **Uso de Mixins para Paneles Administrativos**: La `ShopifyRootPage` utiliza `SHOPIFY_SEO_PANELS` y `SHOPIFY_SYNC_PANELS` definidos en `shopify_content/models/mixins.py`. Estos mixins proporcionan un conjunto estandarizado de paneles de administración para configurar opciones de SEO y de sincronización con Shopify, promoviendo la consistencia en la interfaz de usuario. Puede encontrar más detalles en la documentación del módulo [Mixins Base](Content_Base_Models___Mixins_MixinsBase.md).
*   **Integración con el Servicio de Sincronización**: El método `get_resource_type()` interactúa con la lógica de importación y sincronización (`shopify_content.sync.import_parents.resource_type_for_root_slug`) para determinar el tipo de recurso de Shopify correspondiente al slug de la página raíz. Esto es crucial para la correcta identificación y mapeo de contenido durante las operaciones de sincronización.

## Cómo Encaja en el Sistema General

La `ShopifyRootPage` es un componente arquitectónico clave dentro del sistema de gestión de contenido. Su papel es dual:

1.  **Fundamento para el Contenido Integrado con Shopify**: Sirve como el punto de partida y la organización estructural para todo el contenido editorial que se desea sincronizar y gestionar en Wagtail y Shopify. Al agrupar diferentes tipos de contenido bajo una raíz común, facilita la administración y la aplicación de políticas de sincronización uniformes.
2.  **Puente entre Wagtail y Shopify**: Actúa como el principal conector a nivel de contenido entre el CMS de Wagtail y la plataforma de Shopify. A través de sus campos de sincronización y su relación con los metaobjects, permite que el contenido creado y gestionado en Wagtail se refleje de manera coherente en la storefront de Shopify, aprovechando las capacidades de metaobjects para una mayor flexibilidad.

Esta página raíz es un pilar central del módulo [Shopify Content Management](../../Shopify_Content_Management.md), asegurando que el contenido sea fácilmente administrable dentro de Wagtail mientras mantiene una estrecha integración con el ecosistema de Shopify.

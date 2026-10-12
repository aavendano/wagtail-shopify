# Paneles de UI de Admin y Editorial

El módulo `Admin_and_Editorial_UI_UI_Panels` proporciona componentes de interfaz de usuario para mejorar la experiencia de administración y edición de contenido en Wagtail, específicamente en el contexto de la gestión de contenido de Shopify. Se centra en la visualización de información relevante para el storefront de Shopify directamente dentro de la interfaz de administración de Wagtail.

## Propósito y Funcionalidad Principal

Este módulo define paneles de UI que se utilizan en el backend de Wagtail para mostrar información adicional sobre las páginas de contenido de Shopify. El componente principal es `StorefrontUrlsPanel`, que ofrece una vista de solo lectura de las URL del storefront de Shopify asociadas a una página.

### `StorefrontUrlsPanel`

El `StorefrontUrlsPanel` es un panel de solo lectura diseñado para mostrar las rutas públicas de una página en la tienda Shopify. Su objetivo es proporcionar a los editores y administradores una visibilidad clara de cómo se accederá a una página particular en el frontend de Shopify, lo cual es crucial para correlacionar con herramientas como Google Search Console (GSC) y entender el impacto de las configuraciones de Markets.

*   **`StorefrontUrlsPanel`**: Este panel es una extensión de `wagtail.admin.panels.Panel` y se inicializa con un encabezado por defecto de "Storefront URLs" y un texto de ayuda que explica su propósito.
*   **`StorefrontUrlsPanel.BoundPanel`**: Esta clase anidada es responsable de renderizar el panel. Utiliza la plantilla `shopify_content/panels/storefront_urls.html` y obtiene los datos de las URL del storefront a través de la función `get_storefront_url_display` (definida en `shopify_content.storefront_url_display`), que se aplica a la instancia de la página actual.

### Paneles de Enlaces Semánticos

La función `semantic_links_panels()` genera un `MultiFieldPanel` que contiene paneles para gestionar los enlaces internos semánticos. Dependiendo de la configuración de `WAGTAIL_AI_PGVECTOR`, puede utilizar `AIMultipleChooserPanel` de `wagtail_ai` para sugerencias de enlaces basadas en IA o un `InlinePanel` estándar.

*   **`_typed_ai_chooser_panel`**: Una función auxiliar que crea paneles `TypedAIMultipleChooserPanel` configurados para manejar enlaces semánticos con filtrado por tipo y un índice vectorial específico, si la integración con Wagtail AI está habilitada.
*   **`semantic_links_panels`**: Esta función itera sobre una lista predefinida de nombres de relaciones para enlaces semánticos (`SEMANTIC_LINK_RELATION_NAMES`) y, para cada relación, configura un panel (ya sea `TypedAIMultipleChooserPanel` o `InlinePanel`) dentro de un `MultiFieldPanel` general titulado "Internal Links".

## Arquitectura y Relaciones entre Componentes

Los paneles de UI se integran directamente con la interfaz de administración de Wagtail. `StorefrontUrlsPanel` extiende la clase base `Panel` de Wagtail, lo que le permite ser utilizado en la configuración `edit_handler` de cualquier modelo de página de Wagtail.

El `StorefrontUrlsPanel` depende de la lógica de presentación de URL de storefront, que se espera que sea proporcionada por la función `get_storefront_url_display` del módulo `shopify_content.storefront_url_display`. Esta función toma una instancia de página de Wagtail y devuelve datos que se utilizan para renderizar las URL del storefront.

Los paneles de enlaces semánticos (`semantic_links_panels`) se basan en la configuración de las relaciones de enlaces semánticos y pueden interactuar con la funcionalidad de IA de Wagtail si está activada, aprovechando las capacidades de `wagtail_ai.panels.AIMultipleChooserPanel`.

```mermaid
classDiagram
    direction LR
    class Panel {
        +__init__()
    }
    class BoundPanel {
        +get_context_data()
    }
    class StorefrontUrlsPanel {
        +__init__(**kwargs)
    }
    class StorefrontUrlsPanel_BoundPanel {
        +template_name: str
        +get_context_data(parent_context)
    }
    class AIMultipleChooserPanel {
        +__init__()
    }
    class TypedAIMultipleChooserPanel {
        -_relation_name: str
        -_heading: str
        -_label: str
        -_type_key: str
        -_vector_index: str
        +__init__()
    }
    class InlinePanel {
        +__init__()
    }
    class MultiFieldPanel {
        +__init__()
    }

    Panel <|-- StorefrontUrlsPanel : hereda
    BoundPanel <|-- StorefrontUrlsPanel_BoundPanel : hereda
    StorefrontUrlsPanel ..> StorefrontUrlsPanel_BoundPanel : contiene
    StorefrontUrlsPanel_BoundPanel --|> get_storefront_url_display : usa
    AIMultipleChooserPanel <|-- TypedAIMultipleChooserPanel : hereda
    semantic_links_panels --|> TypedAIMultipleChooserPanel : crea
    semantic_links_panels --|> InlinePanel : crea
    semantic_links_panels --|> MultiFieldPanel : retorna

    note for StorefrontUrlsPanel
        Panel de solo lectura para
        mostrar las URL del storefront
        de Shopify de una página.
    end note

    note for StorefrontUrlsPanel_BoundPanel
        Renderiza el contenido del panel
        obteniendo datos de
        get_storefront_url_display.
    end note

    note for TypedAIMultipleChooserPanel
        Panel de selección múltiple con IA
        para enlaces semánticos,
        con filtro por tipo.
    end note

    note for semantic_links_panels
        Genera paneles para gestionar
        enlaces internos semánticos,
        condicionalmente con soporte AI.
    end note
```
*Diagrama de Clases: Relaciones de los Paneles de UI de Administración*

## Cómo se integra el módulo en el sistema general

Estos paneles son una parte fundamental de la experiencia de edición de contenido en Wagtail para el sistema de gestión de contenido de Shopify.

*   **Visualización de URL del Storefront**: El `StorefrontUrlsPanel` proporciona una vista crucial para los editores. Al mostrar las URL reales del storefront de Shopify directamente en el CMS de Wagtail, facilita la comprensión de cómo se publicará y accederá al contenido. Esto es especialmente útil para la optimización SEO y la depuración, ya que permite a los editores verificar rápidamente las rutas de sus páginas en la tienda en vivo. Este panel actúa como un puente visual entre el entorno de edición de Wagtail y el frontend de Shopify.

*   **Gestión de Enlaces Semánticos**: La función `semantic_links_panels` permite a los editores gestionar los enlaces internos entre el contenido de forma más eficiente. Si la integración con Wagtail AI está habilitada, esto ofrece sugerencias inteligentes para enlaces, mejorando la coherencia y la navegabilidad del sitio. Esto es vital para la estrategia de contenido y SEO, asegurando que las páginas estén bien interconectadas y sean fáciles de descubrir tanto para los usuarios como para los motores de búsqueda.

En resumen, los paneles definidos en este módulo mejoran la usabilidad y la eficiencia del flujo de trabajo de gestión de contenido, conectando las funcionalidades de Wagtail con las necesidades específicas del storefront de Shopify y las capacidades de Wagtail AI para la gestión de enlaces.

Para obtener más información sobre los modelos de contenido y la sincronización de Shopify, consulte las páginas de documentación de [Modelos de Contenido de Shopify](../Shopify_Content_Models.md) y [Sincronización de Contenido y Comandos de Gestión](../Content_Synchronization___Management_Commands.md).
# Ganchos de Wagtail para la Integración de la UI de Administración

Este módulo (`shopify_content/wagtail_hooks.py`) contiene una serie de ganchos (hooks) de Wagtail que extienden y personalizan la interfaz de administración de Wagtail para integrar funcionalidades específicas de gestión de contenido de Shopify. Su objetivo principal es mejorar la experiencia del editor de contenido al gestionar páginas y procesos de sincronización con Shopify, especialmente en entornos multilenguaje.

## Propósito y Funcionalidad Principal

El módulo `ganchos_wagtail` facilita la integración profunda entre el CMS Wagtail y la plataforma Shopify, permitiendo:

1.  **Sincronización de Contenido**: Proporciona retroalimentación en la UI de administración sobre el estado de la sincronización de páginas con Shopify después de acciones de publicación, tanto individuales como masivas.
2.  **Navegación en la Administración**: Agrega un elemento de menú dedicado para la sincronización de Shopify.
3.  **Personalización de la UI**: Inyecta JavaScript para parchear selectores de página y adaptar el comportamiento de la UI.
4.  **Gestión de Localización**: Implementa una vista de edición personalizada para las páginas de inicio (`HomePage`) y un filtro en los selectores de página para asegurar que los enlaces a términos de glosario sean conscientes del locale (idioma y región) de la página que se está editando.

## Arquitectura y Relaciones de Componentes

Este módulo se relaciona estrechamente con varios componentes de `Shopify_Content_Management` y de la aplicación `Application_Core___Shopify_Integration_Platform`.

### Ganchos de Wagtail Registrados

Los ganchos (`@hooks.register`) son el mecanismo principal para extender la funcionalidad de Wagtail.

#### `shopify_wai_chooser_patch_js`

Este gancho inyecta un archivo JavaScript estático (`shopify_content/wai_chooser_patch.js`) en la interfaz de administración global de Wagtail.
Su propósito es aplicar parches o modificaciones al comportamiento predeterminado de los selectores de página (page choosers) o a otras funcionalidades de la UI para adaptarlas a los requisitos específicos de Shopify o de la integración.

#### `register_shopify_sync_urls`

Registra una URL en el panel de administración de Wagtail para la vista de sincronización de Shopify.

*   **URL Registrada**: `shopify-sync/`
*   **Vista Asociada**: `ShopifySyncView` (definida en [Vistas de Sincronización de Shopify](Admin___Wagtail_UI_Integration_vistas_sincronizacion_shopify.md)).
    Esta vista proporciona la lógica para iniciar y monitorear las operaciones de sincronización.

#### `register_shopify_sync_menu_item`

Añade un elemento al menú de configuración del panel de administración de Wagtail.

*   **Nombre**: "Shopify Sync"
*   **Icono**: `download`
*   **Enlace**: Dirige a la URL registrada por `register_shopify_sync_urls`.
    Este elemento de menú proporciona un acceso fácil a la funcionalidad de sincronización de Shopify para los administradores.

#### `notify_shopify_sync_on_publish`

Este gancho se ejecuta `after_publish_page` (después de publicar una página individual).
Comprueba si la página es sincronizable con Shopify (usando `is_syncable_page` y el atributo `sync_enabled` de la página) y notifica al usuario en la interfaz de administración sobre el estado de la cola de sincronización.
Utiliza el modelo `ShopifySyncRun` para obtener información sobre la ejecución de sincronización más reciente.

#### `notify_shopify_sync_after_bulk_publish`

Este gancho se activa `after_bulk_action` (después de una acción masiva). Específicamente, maneja las acciones de publicación masiva.
Itera sobre las páginas afectadas por la publicación masiva, verifica su capacidad de sincronización y proporciona un resumen de cuántas páginas se han encolado para sincronización con Shopify y cuántas han fallado.

### Gestión de Localización en `HomePage`

Este módulo introduce lógica específica para manejar la localización en las `HomePage` y en los selectores de página.

#### `HomePageEditView`

Esta es una vista de edición personalizada que extiende `wagtail.admin.views.pages.edit.EditView`.
Su propósito es interceptar la edición de una `HomePage` para almacenar el locale (código de idioma) de la página en el objeto `request`. Esto es crucial para que los bloques `LocaleAwarePageChooserBlock` puedan acceder a esta información al renderizar `StreamField` y filtrar opciones de páginas relacionadas, como `GlossaryTermPage`.

#### `use_home_page_edit_view`

Este gancho (`register_page_editing_view`) asocia `HomePageEditView` con las instancias del modelo `HomePage` (definido en [Modelos de Página de Inicio](../Home_Page_Models.md)).
Asegura que cuando un editor accede a la página de edición de una `HomePage`, se utilice la vista personalizada que establece el locale.

#### `filter_page_chooser_by_locale`

Este gancho (`construct_page_chooser_queryset`) modifica el queryset de páginas disponibles en los selectores de página de Wagtail.
Cuando se edita una `HomePage`, este gancho filtra las `GlossaryTermPage` (definidas en [Modelos de Contenido del Glosario](../Glossary_Content_Models.md)) para que solo muestre términos de glosario que coincidan con el locale de la `HomePage` que se está editando.
Depende de `homepage_locale` establecido por `HomePageEditView` y utiliza funciones de `shopify_content/page_chooser_locale.py` para la lógica de filtrado y overrides.

## Flujo de Sincronización de Contenido

\`\`\`mermaid
sequenceDiagram
    actor Editor
    participant WagtailAdmin as Interfaz de Administración de Wagtail
    participant WagtailHooks as Ganchos de Wagtail (`wagtail_hooks.py`)
    participant ShopifySyncView as Vista de Sincronización de Shopify
    participant ShopifySyncService as Servicio de Sincronización de Shopify
    participant Shopify as Plataforma Shopify

    Editor->>WagtailAdmin: Publica/Actualiza una página (individual o masiva)
    WagtailAdmin->>WagtailHooks: Señal `after_publish_page` / `after_bulk_action`
    WagtailHooks->>WagtailHooks: Llama `_notify_sync_queued` (para páginas individuales)
    WagtailHooks->>ShopifySyncService: Encola la página para sincronización
    WagtailHooks-->>WagtailAdmin: Muestra mensaje de éxito/error (e.g., "Página encolada para sincronizar")

    Editor->>WagtailAdmin: Navega al menú "Shopify Sync"
    WagtailAdmin->>ShopifySyncView: Accede a la vista de sincronización
    ShopifySyncView->>ShopifySyncService: Inicia/Monitorea procesos de sincronización
    ShopifySyncService->>Shopify: Realiza operaciones de API (GraphQL, REST)
    Shopify-->>ShopifySyncService: Responde con estado/datos
    ShopifySyncService-->>ShopifySyncView: Actualiza el estado de sincronización
    ShopifySyncView-->>WagtailAdmin: Muestra el estado actual de la sincronización
\`\`\`

## Diagrama de Clases

\`\`\`mermaid
classDiagram
    class EditView {
        +get_edit_handler_class()
    }

    class HomePageEditView {
        +get_edit_handler_class()
    }

    class ShopifySyncView {
        +as_view()
    }

    class WagtailHooks {
        +shopify_wai_chooser_patch_js()
        +register_shopify_sync_urls()
        +register_shopify_sync_menu_item()
        +notify_shopify_sync_on_publish(request, page)
        +notify_shopify_sync_after_bulk_publish(request, action_type, objects, action_class_instance)
        +use_home_page_edit_view(page)
        +filter_page_chooser_by_locale(pages, request)
        -_latest_outbound_sync_run(page)
        -_notify_sync_queued(request, page)
    }

    class ShopifySyncRun {
        +KIND_OUTBOUND
        +STATUS_PENDING
        +STATUS_RUNNING
        +STATUS_SUCCESS
        +created_at
        +pk
        +status
        +shopify_sync_runs
    }

    class Page {
        +specific
        +pk
        +title
        +locale
    }

    class HomePage {
        +locale
    }

    class GlossaryTermPage {
    }

    WagtailHooks ..> ShopifySyncView : utiliza
    WagtailHooks ..> ShopifySyncRun : gestiona estado
    WagtailHooks ..> Page : interactúa con
    WagtailHooks ..> HomePage : extiende vista
    WagtailHooks ..> GlossaryTermPage : filtra en selectores
    HomePageEditView --|> EditView : hereda de
    WagtailHooks ..> HomePageEditView : registra
    Page <|-- HomePage
    Page <|-- GlossaryTermPage
\`\`\`

## Integración con el Sistema General

El módulo `Admin___Wagtail_UI_Integration_ganchos_wagtail` es un componente vital de la integración de Shopify Content Management con Wagtail. Se ubica dentro del sub-módulo [Admin___Wagtail_UI_Integration](../Admin___Wagtail_UI_Integration.md), el cual forma parte del módulo principal [Shopify_Content_Management](../../Shopify_Content_Management.md).

*   **Configuración y Modelos**: Depende de los modelos de páginas como `HomePage`, `GlossaryTermPage`, y `ShopifySyncRun` definidos en los respectivos módulos de modelos dentro de `Shopify_Content_Management`.
*   **Vistas de Administración**: Hace uso de `ShopifySyncView` ([Vistas de Sincronización de Shopify](Admin___Wagtail_UI_Integration_vistas_sincronizacion_shopify.md)) para exponer la funcionalidad de sincronización.
*   **Gestión de Locales**: Trabaja en conjunto con la lógica de localización definida en `shopify_content/page_chooser_locale.py` para proporcionar una experiencia de edición consistente y localizada.
*   **Wagtail Core**: Se basa en la arquitectura de ganchos de Wagtail para extender y personalizar el comportamiento del CMS sin modificar directamente su código fuente.

Este módulo asegura que las funcionalidades clave relacionadas con Shopify, como la sincronización y la gestión de contenido multi-locale, estén perfectamente integradas en la interfaz de usuario de administración de Wagtail, proporcionando una experiencia fluida para los editores.

## Referencias

*   [Modelos de Página de Inicio](../Home_Page_Models.md)
*   [Modelos de Contenido del Glosario](../Glossary_Content_Models.md)
*   [Vistas de Sincronización de Shopify](Admin___Wagtail_UI_Integration_vistas_sincronizacion_shopify.md)
*   [Shopify Content Management](../../Shopify_Content_Management.md)
*   [Admin___Wagtail_UI_Integration](../Admin___Wagtail_UI_Integration.md)

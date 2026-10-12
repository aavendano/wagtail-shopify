# Vistas de Sincronización de Shopify

El submódulo `Admin___Wagtail_UI_Integration_vistas_sincronizacion_shopify` proporciona la funcionalidad para la sincronización manual de contenido entrante desde Shopify a Wagtail. La pieza central de este submódulo es la vista `ShopifySyncView`.

## `ShopifySyncView`

Esta vista se encarga de mostrar una página de configuración en la interfaz de administración de Wagtail, permitiendo a los usuarios iniciar manualmente el proceso de importación de contenido de Shopify. Incluye la siguiente funcionalidad:

*   **Verificación de Configuración**: Comprueba si la tienda Shopify está configurada correctamente y tiene un token de acceso válido utilizando `get_shop_config` y `shop_has_access_token` del módulo `Application_Core___Shopify_Integration_Platform/Core_Application___Shopify_Embedded_App`.
*   **Recursos de Importación**: Presenta una lista de recursos disponibles para importar (productos, colecciones, blogs, glosario o todos) definidos en `VALID_IMPORT_RESOURCES` del módulo `Wagtail_Content_Management___API/Shopify_Content_Management/Content_Synchronization_Services`.
*   **Encolado de Tareas**: Cuando el usuario envía una solicitud de importación (POST), la vista encola una tarea de importación utilizando `enqueue_shopify_import` del módulo `Wagtail_Content_Management___API/Shopify_Content_Management/Content_Synchronization_Services`.
*   **Retroalimentación al Usuario**: Muestra mensajes de éxito o error en la interfaz de administración de Wagtail utilizando `wagtail.admin.messages` para informar al usuario sobre el estado de la operación de sincronización.

### Diagrama de Flujo de Sincronización Manual

```mermaid
graph TD
    A["Usuario Wagtail"] --> B["Accede a Shopify Sync View"];
    B --> C{"Shop configurada y con token de acceso?"};
    C -- Sí --> D["Muestra opciones de recursos (productos, colecciones, etc.)"];
    D --> E["Usuario selecciona recurso y envía"];
    E --> F{"Recurso de importación válido?"};
    F -- Sí --> G["Encola tarea de importación (enqueue_shopify_import)"];
    G --> H["Muestra mensaje de éxito con ID de tarea"];
    H --> I["Redirige a Shopify Sync View"];
    F -- No --> J["Muestra mensaje de error: Recurso no válido"];
    J --> I;
    G -- Error --> K["Muestra mensaje de error: Fallo en encolado/inesperado"];
    K --> I;
    C -- No --> L["Muestra estado: Shop no configurada"];
    L --> D;
```

---

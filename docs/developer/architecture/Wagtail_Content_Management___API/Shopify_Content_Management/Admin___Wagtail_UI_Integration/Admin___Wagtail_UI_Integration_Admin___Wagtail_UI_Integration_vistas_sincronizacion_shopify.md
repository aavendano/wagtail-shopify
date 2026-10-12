# Vistas de Sincronización de Shopify en el Admin de Wagtail

Este documento describe el módulo `Admin___Wagtail_UI_Integration_Admin___Wagtail_UI_Integration_vistas_sincronizacion_shopify`, que proporciona la interfaz de usuario para la sincronización manual de contenido desde Shopify hacia Wagtail. Se centra en la vista `ShopifySyncView`, su propósito, arquitectura y cómo interactúa con otros componentes del sistema para facilitar la importación de datos de Shopify.

## Propósito y Funcionalidad Principal

El módulo tiene como objetivo principal ofrecer una forma intuitiva para que los administradores de contenido inicien procesos de sincronización desde Shopify directamente desde la interfaz de administración de Wagtail. Permite la importación de recursos específicos (productos, colecciones, blogs, glosario) o de todos los recursos nuevos, asegurando que el contenido del CMS esté actualizado con los datos de Shopify.

La `ShopifySyncView` es la vista principal que gestiona:
*   La presentación de la página de configuración de sincronización.
*   La validación de la configuración de la tienda Shopify (si tiene un token de acceso).
*   La lista de recursos disponibles para la importación.
*   El manejo de las solicitudes POST para iniciar las tareas de sincronización.
*   La retroalimentación al usuario mediante mensajes de éxito o error de Wagtail.

## Arquitectura

La `ShopifySyncView` es una clase basada en vistas de Django que se integra con el sistema de administración de Wagtail. Extiende `WagtailAdminTemplateMixin` para heredar funcionalidades y estilos comunes del panel de administración de Wagtail, y `TemplateView` para renderizar un template específico (`wagtailadmin/shopify_sync.html`).

### Componentes Clave

*   **`ShopifySyncView`**: La vista principal que orquesta la interfaz de usuario y las llamadas al servicio de sincronización.
*   **`core.shop_config_lookup.get_shop_config` y `core.shop_config_lookup.shop_has_access_token`**: Utilizados para verificar si la tienda Shopify está configurada correctamente y tiene las credenciales necesarias para la sincronización. (Ver [Configuración y Modelos de la Aplicación Core de Shopify Embedded](../../../Application_Core___Shopify_Integration_Platform/Core_Application___Shopify_Embedded_App/Core_Application___Shopify_Embedded_App_configuracion_modelos.md)).
*   **`shopify_content.sync.service.VALID_IMPORT_RESOURCES`**: Una lista de los tipos de recursos que pueden ser importados desde Shopify. (Ver [Servicios de Sincronización de Contenido](../Content_Synchronization_Services.md)).
*   **`shopify_content.sync.task_dispatch.enqueue_shopify_import`**: Una función clave que encola la tarea de importación real en un sistema de colas (como Celery), permitiendo que la operación se ejecute en segundo plano. (Ver [Servicios de Sincronización de Contenido](../Content_Synchronization_Services.md)).
*   **`wagtail.admin.messages`**: Utilizado para mostrar mensajes de éxito o error al usuario en la interfaz de administración de Wagtail.

### Diagrama de Componentes

```mermaid
graph TD
    A[Usuario de Admin de Wagtail] -->|Accede a /admin/shopify-sync/| B(ShopifySyncView)
    B -->|get_context_data()| C{Configuración de la Tienda?}
    C -->|Consulta| D[core.shop_config_lookup]
    D -->|Devuelve estado de configuración| C
    B -->|Renderiza| E[wagtailadmin/shopify_sync.html]
    E -->|Muestra opciones de recursos| B
    A -->|Envía formulario POST (resource)| B
    B -->|post()| F{Valida Recurso (VALID_IMPORT_RESOURCES)}
    F -- Inválido --> G[wagtail_messages.error]
    F -- Válido --> H(enqueue_shopify_import)
    H -->|Encola tarea de sincronización| I[Servicio de Sincronización de Contenido]
    I --> J[ShopifySyncRun Model]
    H -- Éxito --> K[wagtail_messages.success]
    H -- Error --> L[wagtail_messages.error]
    G --> M[Redirección a Shopify Sync]
    K --> M
    L --> M
```

## Flujo de Datos

El flujo de datos para la sincronización de Shopify se inicia con una interacción del usuario en la interfaz de administración de Wagtail y sigue los siguientes pasos:

1.  **Solicitud de Página**: El usuario navega a la URL de sincronización de Shopify en el administrador de Wagtail.
2.  **Preparación del Contexto**: `ShopifySyncView.get_context_data()` se ejecuta para preparar los datos a mostrar en la plantilla. Esto incluye verificar la configuración de la tienda Shopify.
3.  **Renderizado de la Interfaz**: La plantilla `wagtailadmin/shopify_sync.html` se renderiza, mostrando las opciones de importación (productos, colecciones, blogs, glosario, todo).
4.  **Envío del Formulario**: El usuario selecciona un tipo de recurso y envía el formulario (método POST).
5.  **Procesamiento de la Solicitud**: `ShopifySyncView.post()` recibe la solicitud.
6.  **Validación**: Se valida el recurso seleccionado contra una lista de recursos permitidos (`VALID_IMPORT_RESOURCES`).
7.  **Encolamiento de Tarea**: Si el recurso es válido, se llama a `enqueue_shopify_import` para añadir una tarea de sincronización a una cola de procesamiento en segundo plano. Esta función también crea un registro `ShopifySyncRun` para rastrear el estado de la sincronización.
8.  **Retroalimentación al Usuario**: Se muestra un mensaje de éxito o error en la interfaz de Wagtail, informando al usuario sobre el estado de la operación (tarea encolada o error).
9.  **Redirección**: La vista redirige al usuario de nuevo a la página de sincronización de Shopify.

### Diagrama de Flujo de Proceso

```mermaid
graph TD
    A[Usuario accede a la página de Sincronización en Wagtail Admin] --> B{ShopifySyncView.get_context_data()}
    B --> C{Verificar shop_config y access_token}
    C --> D[Renderizar formulario con opciones de recursos]
    D --> E[Usuario selecciona recurso y envía formulario POST]
    E --> F{ShopifySyncView.post()}
    F --> G{Validar recurso seleccionado}
    G -- Recurso inválido --> H[Mostrar mensaje de error en Wagtail]
    G -- Recurso válido --> I[Llamar a enqueue_shopify_import(resource, new_only=True)]
    I --> J[Crear registro ShopifySyncRun]
    J --> K[Encolar tarea de importación en segundo plano]
    K -- Éxito --> L[Mostrar mensaje de éxito en Wagtail (ID de tarea)]
    K -- Error --> M[Mostrar mensaje de error en Wagtail]
    H --> N[Redireccionar a la página de Sincronización]
    L --> N
    M --> N
```

## Relaciones con Otros Componentes

Este módulo tiene dependencias clave con los siguientes componentes y módulos:

*   **[Servicios de Sincronización de Contenido](../Content_Synchronization_Services.md)**: El módulo `shopify_content.sync` es fundamental, ya que proporciona la lógica para definir los recursos importables (`VALID_IMPORT_RESOURCES`) y la función para encolar las tareas de importación (`enqueue_shopify_import`).
*   **[Configuración y Modelos de la Aplicación Core de Shopify Embedded](../../../Application_Core___Shopify_Integration_Platform/Core_Application___Shopify_Embedded_App/Core_Application___Shopify_Embedded_App_configuracion_modelos.md)**: El submódulo `core.shop_config_lookup` es utilizado para verificar la configuración actual de la tienda Shopify, lo cual es crucial antes de iniciar cualquier sincronización.
*   **[Administración de Modelos en Wagtail Admin](Admin___Wagtail_UI_Integration_administracion_modelos.md)**: Los registros de `ShopifySyncRun` (gestionados por `ShopifySyncRunAdmin`) son donde los usuarios pueden consultar el estado y los detalles de las importaciones encoladas por esta vista.

La integración de `ShopifySyncView` en la administración de Wagtail a través de `WagtailAdminTemplateMixin` asegura una experiencia de usuario consistente con el resto del CMS.

# Modelos de Montaje SPA del Framework Editor UI de Django-React

## Introducción

Este documento describe el módulo `Django_React_UI_Editor_Framework_Modelos_Montaje_SPA`, que define el modelo `SpaMount`. Este modelo es fundamental para la integración de aplicaciones de una sola página (SPA) en el entorno Django y Wagtail, proporcionando un mecanismo para montar y configurar dinámicamente las SPAs bajo prefijos URL específicos.

## Propósito y Funcionalidad Principal

El modelo `SpaMount` actúa como una base abstracta para la configuración de SPAs dentro de la plataforma. Permite a los desarrolladores definir puntos de montaje para SPAs, especificando el slug, el prefijo URL, la aplicación de editor frontend, el diseño (layout) y el estado de actividad. Esto desacopla la configuración de la SPA de la lógica de negocio principal, permitiendo una mayor flexibilidad y personalización por producto o por contexto.

### `SpaMount`

La clase `SpaMount` es un modelo abstracto de Django que sirve como plantilla para montar SPAs. Las subclases concretas de `SpaMount` gestionan sus propias tablas de base de datos, lo que permite la personalización del bootstrap y el layout de la SPA sin acoplamientos multitenant.

**Campos:**

*   **`slug`**: Un identificador único (SlugField) para el montaje de la SPA. `max_length=64`.
*   **`title`**: Un campo de texto para el título del montaje de la SPA. `max_length=255`, opcional.
*   **`url_prefix`**: El prefijo de la URL bajo el cual se montará la SPA (por ejemplo, 'cms'). `max_length=64`.
*   **`editor_app`**: La clave de la aplicación de editor frontend utilizada por `VisualEditorAdminMixin`. `max_length=64`, por defecto 'cms'.
*   **`layout`**: Un campo JSON que almacena el layout de Puck para la SPA, con una estructura por defecto `{"root": {"props": {}}, "content": [], "zones": {}, "pages": {"/": {"version": 1, "content": []}}}`. Opcional.
*   **`is_active`**: Un booleano que indica si el montaje de la SPA está activo. Por defecto `True`.
*   **`created_at`**: Fecha y hora de creación del montaje (se establece automáticamente al crear).
*   **`updated_at`**: Fecha y hora de la última actualización del montaje (se actualiza automáticamente en cada guardado).

**Métodos:**

*   **`default_layout()`**: Una función que retorna una estructura de layout de Puck por defecto para una SPA de Workbench.
*   **`get_bootstrap(request=None)`**: Retorna un payload JSON que se inyecta en el shell de la SPA, conteniendo información esencial como el `slug`, `urlPrefix` y `layout` actual para inicializar la aplicación frontend.

### `SpaMount.Meta`

La clase `Meta` anidada en `SpaMount` define metadatos para el modelo:

*   **`abstract = True`**: Indica que `SpaMount` es una clase abstracta y no se creará una tabla de base de datos para ella directamente. Sirve como base para otros modelos.
*   **`ordering = ["slug"]`**: Define el orden por defecto de los objetos `SpaMount` por el campo `slug`.

## Arquitectura y Relaciones de Componentes

El módulo `Django_React_UI_Editor_Framework_Modelos_Montaje_SPA` es una parte fundamental del marco del editor de UI de Django-React. Se relaciona directamente con otros componentes del framework:

*   **[Configuración de Aplicación](Django_React_UI_Editor_Framework_Configuracion_Aplicacion.md)** (`django_react_ui_editor/apps.py::DjangoReactUiEditorConfig`): Registra la aplicación y sus modelos, incluyendo las subclases de `SpaMount`.
*   **[Integración del Editor Visual en Admin](Django_React_UI_Editor_Framework_Integracion_Editor_Visual_Admin.md)** (`django_react_ui_editor/admin.py::VisualEditorAdminMixin`): Utiliza el campo `editor_app` de `SpaMount` para integrar el editor visual en la interfaz de administración de Django.
*   **[Registro y URL de SPA](Django_React_UI_Editor_Framework_Registro_y_URL_de_SPA.md)** (`django_react_ui_editor/spa_registry.py::SpaRegistration`): Registra las SPAs disponibles en el sistema, que pueden basarse en las configuraciones de `SpaMount`.
*   **[Vistas de Shell de SPA](Django_React_UI_Editor_Framework_Vistas_Shell_de_SPA.md)** (`django_react_ui_editor/views.py::SpaShellView`): Renderiza el shell de la SPA, utilizando la información de `get_bootstrap` de una instancia de `SpaMount` para inicializar la aplicación frontend.
*   **[CMS UI Integration - CmsSpaMount](../CMS_UI_Integration/CMS_UI_Integration_CmsSpaMount.md)** (`cms_ui/models.py::CmsSpaMount`): Una subclase concreta de `SpaMount` que extiende su funcionalidad para la integración específica del CMS UI.

### Diagrama de Relaciones de Componentes

```mermaid
graph TD
    subgraph Django_React_UI_Editor_Framework
        A[django_react_ui_editor/models.py::SpaMount]:::main
        B[django_react_ui_editor/apps.py::DjangoReactUiEditorConfig]
        C[django_react_ui_editor/admin.py::VisualEditorAdminMixin]
        D[django_react_ui_editor/spa_registry.py::SpaRegistration]
        E[django_react_ui_editor/views.py::SpaShellView]
    end

    subgraph CMS_UI_Integration
        F[cms_ui/models.py::CmsSpaMount]
    end

    A -- "es configurado por" --> B
    C -- "utiliza editor_app de" --> A
    D -- "registra SPAs basadas en" --> A
    E -- "obtiene bootstrap de" --> A
    F -- "hereda de" --|> A

    classDef main fill:#f9f,stroke:#333,stroke-width:2px;
```

## Flujo de Datos y Proceso

1.  **Definición de SPA**: Un desarrollador define una subclase concreta de `SpaMount` (como `CmsSpaMount`) en su aplicación Django, especificando `slug`, `url_prefix`, `editor_app`, y un `layout` inicial.
2.  **Registro de la Aplicación**: `DjangoReactUiEditorConfig` se asegura de que los modelos del framework, incluidas las subclases de `SpaMount`, sean reconocidos por Django.
3.  **Configuración del Admin**: `VisualEditorAdminMixin` utiliza la información de `SpaMount` para habilitar funcionalidades de edición visual en el panel de administración de Wagtail, utilizando la clave `editor_app`.
4.  **Acceso a la SPA**: Cuando un usuario navega a un `url_prefix` configurado para una `SpaMount`, `SpaShellView` se encarga de servir la aplicación frontend.
5.  **Inicialización del Frontend**: `SpaShellView` recupera el bootstrap JSON a través del método `get_bootstrap()` de la instancia de `SpaMount` correspondiente. Este JSON contiene los datos iniciales necesarios para que la aplicación React se monte y configure correctamente, incluyendo el layout de Puck.
6.  **Edición de Contenido**: El frontend, posiblemente a través de un editor como Puck, interactúa con la API para modificar el `layout` JSON almacenado en `SpaMount`, persistiendo los cambios en la base de datos.

## Integración con el Sistema General

El módulo `Django_React_UI_Editor_Framework_Modelos_Montaje_SPA` es un pilar para la extensibilidad y la gestión de contenido dinámico en la plataforma.

*   **Wagtail Content Management**: Proporciona el mecanismo para que el CMS Wagtail monte y gestione SPAs que pueden ser utilizadas como interfaces de edición o visualización de contenido. Por ejemplo, `CmsSpaMount` en [CMS UI Integration](../CMS_UI_Integration.md) es una implementación directa.
*   **API**: Las configuraciones de las SPAs definidas por `SpaMount` pueden ser expuestas o consumidas por las APIs (ver [Shopify Content API](../Shopify_Content_API.md)) para permitir la interacción programática o la sincronización de estados.
*   **Desarrollo Frontend**: Facilita la integración de aplicaciones React al proporcionar un punto de montaje y un mecanismo de inicialización claro, desacoplando el desarrollo frontend del backend de Django.

Este modelo es clave para crear una experiencia de usuario fluida y unificada, donde las capacidades de gestión de contenido de Wagtail se extienden a través de interfaces de usuario modernas y dinámicas construidas con React.
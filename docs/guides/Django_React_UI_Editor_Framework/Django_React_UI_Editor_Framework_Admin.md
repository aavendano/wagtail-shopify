# Administración del Framework de Editor de UI Django-React

El módulo `Django_React_UI_Editor_Framework_Admin` proporciona funcionalidades para integrar un editor de interfaz de usuario visual basado en React dentro del panel de administración de Django. El componente principal, `VisualEditorAdminMixin`, permite a los administradores editar el diseño (layout) de las páginas SPA (Single Page Application) directamente desde la interfaz de administración de Django.

## `VisualEditorAdminMixin`

Este mixin de administración está diseñado para ser utilizado con modelos que gestionan el `layout` de una SPA, como el modelo `SpaMount` (ver [Modelos del Framework de Editor de UI Django-React](Django_React_UI_Editor_Framework_Modelos.md)). Su propósito principal es inyectar un editor visual de React, específicamente un entorno de trabajo Puck, en la página de edición de un objeto en el panel de administración de Django. Esto permite una edición intuitiva y en tiempo real del JSON que define la estructura del `layout`.

### Funcionalidad Principal

El `VisualEditorAdminMixin` extiende el comportamiento predeterminado del `ModelAdmin` de Django para:

*   **Inyectar el Editor Visual**: Sobrescribe el `change_form_template` para incluir un contenedor `div` (`visual-editor-root`) donde se montará la aplicación React del editor. Este contenedor recibe datos esenciales a través de atributos `data-*`, como el ID de la instancia del modelo y el JSON del `layout` actual.
*   **Campos de Solo Lectura**: Asegura que el campo `layout_editor` se agregue a los `readonly_fields` para que no sea un campo de formulario editable directamente, sino que se muestre como el editor visual.
*   **Visualización del Editor**: El método `layout_editor` genera el HTML necesario para incrustar el editor. Esto incluye enlaces a los archivos CSS y JavaScript de la aplicación React, y un mensaje de ayuda.

### Configuración

El mixin utiliza la configuración de Django `settings.VISUAL_EDITOR` para determinar las rutas a los archivos JavaScript y CSS del editor. Por defecto, estos son `cms_ui/editor.js` y `cms_ui/editor.css`, que corresponden a la aplicación frontend (ver [Aplicación Frontend del CMS UI](../CMS_UI___Frontend/CMS_UI___Frontend_Aplicacion_Frontend.md)).

```python
# settings.py
VISUAL_EDITOR = {
    "EDITOR_JS": "path/to/your/editor.js",
    "EDITOR_CSS": "path/to/your/editor.css",
}
```

### Relaciones y Dependencias

El `VisualEditorAdminMixin` tiene las siguientes dependencias clave:

*   **Modelo `SpaMount`**: Se espera que el modelo al que se aplica este mixin tenga un campo `layout` donde se almacenará la configuración JSON del diseño de la SPA. Este modelo es definido en [Modelos del Framework de Editor de UI Django-React](Django_React_UI_Editor_Framework_Modelos.md).
*   **Aplicación Frontend React**: El editor visual en sí es una aplicación frontend de React (por ejemplo, basada en Puck) que consume el JSON del `layout` y lo presenta de forma interactiva. Esta aplicación es provista por el módulo `CMS_UI___Frontend`, específicamente sus componentes de aplicación frontend (ver [Aplicación Frontend del CMS UI](../CMS_UI___Frontend/CMS_UI___Frontend_Aplicacion_Frontend.md)).
*   **Plantilla de Administración Personalizada**: Utiliza la plantilla `django_react_ui_editor/admin_change_form.html` para insertar el editor en el lugar correcto dentro del formulario de cambio de administración.

### Diagrama de Arquitectura

El siguiente diagrama ilustra cómo `VisualEditorAdminMixin` interactúa con otros componentes del sistema para proporcionar una experiencia de edición visual en el panel de administración de Django.

```mermaid
graph TD
    A[ModelAdmin de Django] --> B{VisualEditorAdminMixin}
    B --> C[Modelo de la SPA (e.g., SpaMount)]
    B -- "Inyecta HTML y JS" --> D[Navegador del Usuario]
    C -- "JSON del Layout" --> D
    D -- "Renderiza Editor React" --> E[Editor Visual (Puck)]
    E -- "Actualiza JSON del Layout" --> C
    D -- "Carga estáticos" --> F[Servidor de Archivos Estáticos]

    subgraph Panel de Administración de Django
        A
        B
        C
    end

    subgraph Frontend de la Aplicación
        D
        E
        F
    end

    style C fill:#f9f,stroke:#333,stroke-width:2px
    style E fill:#bbf,stroke:#333,stroke-width:2px
    style B fill:#ccf,stroke:#333,stroke-width:2px

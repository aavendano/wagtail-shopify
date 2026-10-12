# Integración del Editor Visual en el Admin de Django React UI Editor

Este módulo, `Django_React_UI_Editor_Framework_Integracion_Editor_Visual_Admin`, facilita la integración de un editor visual basado en React (Puck) directamente en el panel de administración de Django para la gestión de layouts de aplicaciones de una sola página (SPA). Su componente principal es `VisualEditorAdminMixin`, que transforma la interfaz de edición de los modelos `SpaMount` (o sus subclases) en una experiencia de edición visual rica.

## Propósito y Funcionalidad Principal

El objetivo primordial de este módulo es permitir a los administradores de contenido diseñar y modificar visualmente la estructura y el contenido de las páginas de las SPA directamente desde el backend de Django, sin necesidad de manipular código JSON manualmente. Esto mejora significativamente la usabilidad y la eficiencia en la gestión del contenido y la interfaz de usuario.

`VisualEditorAdminMixin` inyecta un editor de flujo de trabajo de Puck en el `change_form_template` de los modelos `ModelAdmin` que lo utilicen. Este editor permite la manipulación del campo `layout` (un campo `JSONField`) del modelo `SpaMount`, que almacena la configuración de los componentes de la interfaz de usuario.

### `django_react_ui_editor/admin.py::VisualEditorAdminMixin`

Este mixin extiende la funcionalidad de `django.contrib.admin.ModelAdmin` para añadir un editor visual a la interfaz de administración de los modelos `SpaMount`. Key functionalities include:

*   **`editor_app`**: Define la clave de la aplicación frontend del editor, por defecto "cms". Esta clave se utiliza para referenciar los activos de JavaScript y CSS del editor.
*   **`change_form_template`**: Sobrescribe la plantilla de formulario de cambio predeterminada a `"django_react_ui_editor/admin_change_form.html"`, que contiene el punto de montaje para la aplicación React del editor.
*   **`get_readonly_fields`**: Asegura que el campo `layout_editor` se trate como de solo lectura en la interfaz de administración de Django, ya que su contenido se genera dinámicamente y se edita a través del editor visual, no directamente en un campo de texto.
*   **`get_fieldsets`**: Se asegura de que `layout_editor` esté presente en los fieldsets, incluso si el `ModelAdmin` utiliza los campos predeterminados.
*   **`layout_editor(self, obj)`**: Esta es la función principal que renderiza el editor visual. Si el objeto (`SpaMount` o subclase) no ha sido guardado, solicita al usuario que lo haga. De lo contrario, genera un `div` HTML (`#visual-editor-root`) que sirve como punto de montaje para la aplicación React del editor. Este `div` recibe datos importantes como el ID del mount, la aplicación del editor (`editor_app`) y el JSON del layout actual a través de atributos `data-`. También inyecta los archivos CSS y JavaScript del editor (`editor.css`, `editor.js`) utilizando `settings.STATIC_URL`.

## Arquitectura y Relaciones de Componentes

Este módulo se integra estrechamente con el framework de Django y las aplicaciones frontend de React. La `VisualEditorAdminMixin` actúa como un puente entre el backend de Django y la aplicación React del editor visual.

### Relación con `SpaMount`

La mixin `VisualEditorAdminMixin` está diseñada para ser utilizada con modelos que hereden de [SpaMount](Django_React_UI_Editor_Framework_Modelos_Montaje_SPA.md). El campo `layout` de `SpaMount`, un `JSONField`, es el que almacena la configuración de los componentes de la interfaz de usuario que el editor visual manipula. El editor visual lee este JSON, lo presenta en una interfaz gráfica y guarda los cambios de nuevo en este campo.

### Flujo de Datos para la Edición Visual

```mermaid
graph TD
    A[Usuario de Admin de Django] -->|Accede a la página de edición de SpaMount| B(Admin de Django: ModelAdmin con VisualEditorAdminMixin)
    B -->|Solicita renderización de layout_editor| C{VisualEditorAdminMixin.layout_editor}
    C -->|Genera HTML con data-atributos y scripts| D[Página HTML del Admin]
    D -->|Navegador carga editor.js y editor.css| E(Aplicación React del Editor Visual (Puck))
    E -->|Lee data-layout-json de #visual-editor-root| F[Estado Interno del Editor]
    F -->|Renderiza UI interactiva| E
    E -->|Usuario edita layout| G[Cambios en el Layout (JSON)]
    G -->|El editor guarda cambios automáticamente vía AJAX/formulario| H(Backend de Django: Vista de Guardado de ModelAdmin)
    H -->|Actualiza SpaMount.layout| I[Base de Datos (SpaMount)]
```

### Dependencias con el Frontend

La integración depende de la existencia de una aplicación frontend del editor (por ejemplo, `cms_ui`) que proporcione los archivos `editor.js` y `editor.css`. Estos archivos se especifican en las `settings` de Django bajo `VISUAL_EDITOR` y se cargan dinámicamente en el formulario de administración.

*   **`cms_ui/editor.js` y `cms_ui/editor.css`**: Estos son los activos de la aplicación React que implementa la interfaz del editor visual. Se cargan en el navegador para activar el editor en la página de administración. Ver [CMS_UI_Integration](../CMS_UI_Integration.md) para más detalles.

## Cómo encaja en el Sistema General

`Django_React_UI_Editor_Framework_Integracion_Editor_Visual_Admin` es un componente clave para el sistema de gestión de contenido, especialmente en un entorno donde se utilizan SPA y Wagtail para la creación de experiencias de usuario ricas y dinámicas. Proporciona una forma intuitiva para que los equipos no técnicos modifiquen layouts complejos sin intervenir en el código fuente.

Se integra con:

*   **[Django_React_UI_Editor_Framework_Modelos_Montaje_SPA](Django_React_UI_Editor_Framework_Modelos_Montaje_SPA.md)**: Provee el modelo base (`SpaMount`) para los puntos de montaje de las SPA y sus layouts asociados.
*   **[Wagtail_Content_Management___API/CMS_UI_Integration](../CMS_UI_Integration.md)**: Esta aplicación probablemente proporciona la implementación real del editor visual de React (Puck) y sus activos estáticos (`editor.js`, `editor.css`) que son referenciados y cargados por este módulo. La `CmsSpaMount` es una subclase concreta de `SpaMount` que se beneficia directamente de esta integración.
# Framework del Editor UI Django React

Este módulo (`django_react_ui_editor`) proporciona un framework robusto para integrar aplicaciones de una sola página (SPA) basadas en React con Django y el CMS Wagtail. Facilita la creación y gestión de contenido interactivo y visualmente editable a través de un editor de interfaz de usuario de tipo "workbench", como Puck.

## Propósito

El objetivo principal de este framework es permitir a los desarrolladores:
*   Montar SPAs de React dentro de una aplicación Django existente.
*   Proporcionar un mecanismo para editar visualmente el diseño y el contenido de estas SPAs a través del panel de administración de Django/Wagtail.
*   Gestionar la configuración y el estado inicial (bootstrap) de las SPAs, incluyendo la autenticación del usuario.

## Arquitectura

El `Django_React_UI_Editor_Framework` se compone de varios componentes clave que trabajan juntos para lograr la integración de SPAs y la edición visual.

```mermaid
graph TD
    A[Navegador del Usuario] -->|Solicitud SPA| B(SpaShellView);
    B -->|Obtiene Configuración y Layout| C[SpaMount Model];
    C -->|Layout y Datos de Bootstrap| B;
    B -->|Renderiza Plantilla HTML con JS/CSS| A;
    A -->|Interacciones del Editor| D(VisualEditorAdminMixin);
    D -->|Actualiza Layout JSON| C;
    C --o|Define Estructura y Comportamiento| E[SpaRegistration];

    subgraph Django Backend
        subgraph django_react_ui_editor
            B
            C
            D
            E
        end
        subgraph Wagtail Admin
            D
        end
    end

    subgraph Frontend (React SPA)
        F[Editor de Interfaz de Usuario (Puck Workbench)]
        G[Aplicación React Pública]
    end

    A -- "Acceso al Admin" --> D;
    D -- "Carga Editor JS/CSS" --> A;
    A -- "Carga SPA Pública JS/CSS" --> A;
    B -.-> E;
    D -.-> E;
    F -.-> D;
    G -.-> B;
```

*Diagrama 1: Visión General de la Arquitectura del Framework del Editor UI Django React*

La arquitectura se centra en la separación de las preocupaciones, donde el backend de Django gestiona la configuración de las SPAs y su contenido estructurado, mientras que el frontend de React se encarga de la renderización de la interfaz de usuario y la experiencia de edición visual.

## Componentes del Módulo

Este módulo se desglosa en los siguientes sub-módulos para una mejor organización y comprensión:

*   **[Configuración de la Aplicación](Django_React_UI_Editor_Framework/Configuracion_Aplicacion.md)**: Define la configuración básica de la aplicación Django para el framework.
*   **[Modelos de Montaje SPA](Django_React_UI_Editor_Framework/Modelos_Montaje_SPA.md)**: Contiene el modelo base para el montaje de SPAs, gestionando el slug, el prefijo de URL y el diseño (layout) de la SPA.
*   **[Registro y URL de SPA](Django_React_UI_Editor_Framework/Registro_y_URL_de_SPA.md)**: Se encarga del registro de las SPAs y la generación de patrones de URL dinámicos.
*   **[Vistas de Shell de SPA](Django_React_UI_Editor_Framework/Vistas_Shell_de_SPA.md)**: Proporciona la vista para servir el shell público de una SPA registrada, inyectando datos de bootstrap.
*   **[Integración del Editor Visual en el Admin](Django_React_UI_Editor_Framework/Integracion_Editor_Visual_Admin.md)**: Facilita la integración del editor visual de interfaz de usuario (Puck workbench) en el panel de administración de Django/Wagtail.

## Relación con Otros Módulos

Este framework se integra con:
*   **[Wagtail_Content_Management___API/CMS_UI_Integration.md](CMS_UI_Integration.md)**: Este módulo probablemente proporciona los archivos `editor.js`, `editor.css`, `spa-public.js`, y `spa-public.css` referenciados en las configuraciones, actuando como la implementación concreta del frontend del editor y la SPA pública.
*   **Django Admin**: Utiliza las capacidades del panel de administración de Django para la edición visual del layout de las SPAs.
*   **Configuración de Django (`settings.py`)**: Depende de la configuración `VISUAL_EDITOR` para las rutas de los activos del editor.
*   **Modelos de Aplicaciones Concretas**: Subclases de `SpaMount` (como `CmsSpaMount` en `CMS_UI_Integration`) son utilizadas por este framework para manejar instancias específicas de SPAs.

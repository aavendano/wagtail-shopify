# Vistas del Shell de SPA del Framework Editor UI de Django React


## Introducción

El módulo `Django_React_UI_Editor_Framework_Vistas_Shell_de_SPA` es una parte fundamental del marco de trabajo del editor de UI de Django React, encargándose de servir el shell (caparazón) de las Single Page Applications (SPA) registradas. La vista principal, `SpaShellView`, actúa como el punto de entrada para las aplicaciones React incrustadas, gestionando la carga de los recursos estáticos y la inyección de datos de inicialización necesarios para el frontend.

## Propósito y Funcionalidad

La `SpaShellView` tiene como objetivo principal proporcionar una vista genérica que pueda renderizar un *shell* HTML para cualquier SPA registrada en el sistema. Esto permite que diferentes aplicaciones frontend basadas en React puedan ser servidas desde el mismo backend de Django, utilizando un mecanismo unificado para la carga inicial.

Las responsabilidades clave de `SpaShellView` incluyen:
*   **Identificación del SPA**: Determinar qué SPA debe ser servida basándose en el slug de montaje proporcionado en la URL o configurado en la vista.
*   **Recuperación de la Configuración del Montaje**: Obtener la instancia de `SpaMount` y `SpaRegistration` asociada al slug, lo que proporciona información crucial sobre la SPA (título, prefijo de URL, etc.).
*   **Inyección de Datos de Bootstrap**: Preparar y serializar datos iniciales (bootstrap data) que la aplicación React utilizará al cargarse. Esto incluye información del usuario autenticado si aplica, y cualquier otra configuración específica del montaje.
*   **Carga de Recursos Estáticos**: Configurar las rutas para los archivos CSS y JavaScript públicos del SPA, permitiendo que el navegador los cargue correctamente.

## Arquitectura y Relaciones de Componentes

La `SpaShellView` se integra con varios componentes dentro del `Django_React_UI_Editor_Framework` y el ecosistema de Django/Wagtail.

### Componentes Clave:

*   **`SpaShellView` (django_react_ui_editor/views.py)**: La clase de vista principal que extiende `django.views.generic.TemplateView`.
*   **`SpaMount` (django_react_ui_editor/models.py)**: Modelo de Django que representa una instancia de un SPA montado en el sistema, incluyendo su slug, título y métodos para obtener datos de bootstrap.
*   **`SpaRegistration` (django_react_ui_editor/spa_registry.py)**: Un registro que asocia un slug de SPA con su modelo de montaje (`SpaMount`) y otras configuraciones. Proporciona una forma centralizada de acceder a las SPAs disponibles.

### Diagrama de Relaciones:

```mermaid
graph TD
    A[Navegador del Usuario] -->|Solicitud HTTP| B(SpaShellView)
    B -->|Llamada a get_mount()| C{get_registered_spas()}
    C -->|Retorna Registros de SPA| D[SpaRegistration]
    D -->|Define mount_model| E[SpaMount Model]
    B -->|Consulta SpaMount.objects.get()| E
    E -->|Retorna Instancia de SpaMount| B
    B -->|Llamada a get_context_data()| F{Obtener datos de Bootstrap}
    F -->|get_bootstrap()| E
    F -->|Información de Usuario| G[request.user]
    B -->|Renderiza Plantilla HTML| H[spa_shell.html]
    H -->|Carga de Recursos| I[Archivos JS/CSS Públicos del SPA]
    I --> A
```

**Descripción del Flujo:**
1.  El **Navegador del Usuario** realiza una solicitud HTTP a una URL que coincide con la `SpaShellView`.
2.  `SpaShellView` invoca `get_mount()` para identificar la SPA solicitada.
3.  `get_mount()` utiliza `get_registered_spas()` (definido en [Registro y URL de SPA](Django_React_UI_Editor_Framework_Registro_y_URL_de_SPA.md)) para obtener los registros de SPA.
4.  Con la información del registro (`SpaRegistration`), se consulta el modelo `SpaMount` (definido en [Modelos de Montaje SPA](Django_React_UI_Editor_Framework_Modelos_Montaje_SPA.md)) para obtener la instancia específica del montaje (`mount`).
5.  `SpaShellView` luego llama a `get_context_data()` para preparar los datos.
6.  Dentro de `get_context_data()`, se obtienen los datos de bootstrap del objeto `mount` y se añade información del usuario autenticado de `self.request.user`.
7.  Finalmente, la `SpaShellView` renderiza la plantilla `spa_shell.html`, inyectando los datos de bootstrap serializados en JSON y las rutas a los archivos JS/CSS públicos del SPA.
8.  El navegador carga los recursos estáticos (JS/CSS) y la aplicación React se inicializa con los datos proporcionados.

## Integración en el Sistema General

Este módulo se sitúa en el corazón de la integración de las aplicaciones frontend de React con el backend de Django/Wagtail. Proporciona el "caparazón" inicial que aloja la aplicación React, permitiendo que las herramientas de edición de UI basadas en React se incrusten y funcionen dentro del entorno de Wagtail.

Su uso es crucial para módulos como [CMS UI Integration](../CMS_UI_Integration.md), donde la interfaz de usuario para la gestión de contenido se construye como una SPA de React. La `SpaShellView` facilita que estas SPAs se carguen, se inicialicen con los datos correctos y accedan a la API de backend según sea necesario.

### Dependencias Externas:

*   **Django Settings (`django.conf.settings`)**: Utilizado para configurar `VISUAL_EDITOR` y obtener las rutas de los archivos JS/CSS públicos.
*   **JSON (`import json`)**: Para serializar los datos de bootstrap.
*   **`Http404` (django.http)**: Para manejar casos donde el slug de montaje de la SPA no se encuentra.

### Diagrama de Flujo de Datos para la Inicialización de un SPA:

```mermaid
graph TD
    A[Solicitud de Navegador] --> B(Django URL Router)
    B --> C{SpaShellView.dispatch()}
    C --> D[SpaShellView.get_mount()]
    D --> E{spa_registry.get_registered_spas()}
    E --> F[SpaRegistration]
    F --> G[SpaMount Model]
    G --> H[SpaMount Instance (DB)]
    H --> D
    D --> C
    C --> I[SpaShellView.get_context_data()]
    I --> J{mount.get_bootstrap(request)}
    J --> H
    J --> K[request.user (Authentication)]
    K --> I
    I --> L[Context Data]
    L --> M(django_react_ui_editor/spa_shell.html)
    M --> N[JSON.dumps(bootstrap)]
    N --> O[HTML Renderizado]
    O --> P[Referencia a spa-public.js/css]
    P --> Q(Navegador Carga JS/CSS)
    Q --> R[Aplicación React Inicializada]
    R --> S[Interacción con API de Backend]
```

# Módulo Principal del Núcleo de la Aplicación de Contenido de Shopify

## Introducción y Propósito

El módulo `Shopify_Content_Application_Core` es el corazón del sistema de gestión de contenido para las tiendas Shopify. Proporciona la infraestructura esencial para la configuración de la aplicación, la validación de la localización de las páginas de inicio, la generación de URLs para el escaparate y la integración con las funcionalidades de IA de Wagtail, incluyendo correcciones y mejoras. Su propósito principal es asegurar que el contenido publicado en Shopify sea coherente, localizable y optimizado para la plataforma.

## Visión General de la Arquitectura

Este módulo se integra con el marco de trabajo de Django y Wagtail para extender sus capacidades en la gestión de contenido específico de Shopify. Interactúa con varios componentes del sistema, incluyendo modelos de datos, servicios de sincronización y la interfaz de administración.

```mermaid
C4Context
    title Diagrama de Contexto del Núcleo de la Aplicación de Contenido de Shopify

    System_Boundary(shopify_content_application_core_module, "Módulo Núcleo de la Aplicación de Contenido de Shopify") {
        Component(app_config, "Configuración de la Aplicación", "Configura la aplicación Django y registra señales y parches.")
        Component(home_locale_validation, "Validación de Localización de Páginas de Inicio", "Valida las referencias de páginas en las secciones de la página de inicio según la localización.")
        Component(storefront_url_generation, "Generación de URLs de Escaparate", "Gestiona la creación de URLs canónicas y con prefijo de localización para el escaparate de Shopify.")
        Component(wagtail_ai_fixes, "Integraciones y Correcciones de IA de Wagtail", "Middleware y parches para mejorar la funcionalidad de IA de Wagtail y la vista previa de StreamField.")
    }

    System(shopify_app_core, "Núcleo de la Aplicación Shopify", "Módulo principal de la aplicación Shopify, incluyendo configuración y gestión general.")
    System(content_page_models, "Modelos de Páginas de Contenido", "Define la estructura de los datos para las diferentes páginas de contenido (artículos, productos, colecciones, etc.).")
    System(wagtail_streamfield_blocks, "Bloques de StreamField de Wagtail", "Define los componentes de contenido reutilizables para el editor de Wagtail.")
    System(content_store_markdown, "Almacén de Contenido y Procesamiento de Markdown", "Gestiona el almacenamiento y renderizado del contenido en formato Markdown.")
    System(admin_interface, "Interfaz de Administración", "Proporciona las vistas y paneles de administración para la gestión del contenido.")
    System(wagtail_ai_core, "Núcleo de IA de Wagtail", "Componente externo de Wagtail para funcionalidades de IA, como sugerencias de contenido.")

    Rel(shopify_app_core, shopify_content_application_core_module, "Configura y se integra con")
    Rel(shopify_content_application_core_module, content_page_models, "Utiliza modelos para la validación y generación de URLs")
    Rel(shopify_content_application_core_module, wagtail_streamfield_blocks, "Se integra para correcciones de vista previa")
    Rel(shopify_content_application_core_module, wagtail_ai_core, "Aplica parches y extiende funcionalidades de IA")
    Rel(shopify_content_application_core_module, admin_interface, "Influye en la presentación y validación en el admin")
    Rel(wagtail_streamfield_blocks, shopify_content_application_core_module, "Bloques definidos utilizados por la validación de StreamField")
```

## Sub-módulos y Funcionalidad de Alto Nivel

El módulo `Shopify_Content_Application_Core` se compone de los siguientes sub-módulos, cada uno con responsabilidades específicas:

### [Configuración de la Aplicación](Shopify_Content_Application_Core/Shopify_Content_Application_Core_Application_Configuration.md)
Gestiona la configuración inicial de la aplicación, incluyendo el registro de señales de Django y Wagtail, y la aplicación de parches necesarios para la sincronización de contenido y la gestión de artículos en Markdown.

### [Validación de Localización de Páginas de Inicio](Shopify_Content_Application_Core/Shopify_Content_Application_Core_Home_Page_Locale_Validation.md)
Se encarga de asegurar que todas las referencias de páginas dentro de la estructura de la página de inicio (`sections_json`) sean consistentes con la localización de la página de inicio. Esto evita referencias cruzadas incorrectas entre diferentes idiomas o mercados.

### [Generación de URLs de Escaparate](Shopify_Content_Application_Core/Shopify_Content_Application_Core_Storefront_URL_Generation.md)
Proporciona utilidades para construir rutas de URL canónicas y con prefijo de localización para las diferentes páginas de contenido (productos, colecciones, blogs, artículos, términos de glosario, etc.) que se muestran en el escaparate de Shopify.

### [Integraciones y Correcciones de IA de Wagtail](Shopify_Content_Application_Core/Shopify_Content_Application_Core_Wagtail_AI_Integrations_and_Fixes.md)
Incluye middleware y funciones para corregir comportamientos específicos de Wagtail, especialmente en relación con la vista previa de `StreamField` y las funcionalidades de IA, como la sugerencia de contenido. También implementa guardias para evitar errores relacionados con documentos vectoriales obsoletos.


# Validación de Localización para Contenido de la Página de Inicio

Este módulo, `Content_URL___Semantic_Linking_Logic_Home_Locale_Validation`, se encarga de asegurar la coherencia de la localización para las referencias de páginas dentro de las secciones de las páginas de inicio de Wagtail (`HomePage`). Su función principal es validar que cualquier página enlazada o referenciada dentro de la estructura `sections_json` de una `HomePage` coincida con la localización de la propia página de inicio, evitando así referencias cruzadas de contenido entre diferentes localizaciones.

## Propósito y Funcionalidad Principal

La lógica de validación de localización es crucial para mantener la integridad del contenido localizado en el sistema Shopify. Cuando un editor crea o actualiza una `HomePage`, es posible que, de manera inadvertida, se incluyan enlaces a páginas (como artículos o términos de glosario) que pertenecen a una localización diferente. Este módulo previene tales inconsistencias, lo que garantiza que los usuarios finales vean contenido relevante para su configuración regional.

Los componentes clave en este módulo son:

*   **`HomePageLocaleSource`**: Un protocolo que define la interfaz esperada para un objeto de página de inicio, requiriendo atributos `locale` y `sections_json` para la validación.
*   **`collect_sections_page_ids(sections_json: dict | None) -> list[int]`**: Esta función itera sobre la estructura `sections_json` de una `HomePage` y recopila todos los IDs de las páginas de Wagtail que están referenciadas dentro de las diferentes secciones (por ejemplo, colecciones destacadas, enlaces internos, módulos educativos).
*   **`is_page_valid_for_home_locale(home_page: HomePageLocaleSource, page: Page) -> bool`**: Determina si una página referenciada específica es válida para la localización de la página de inicio dada. Realiza comprobaciones específicas para tipos de página como `ArticlePage` y `GlossaryTermPage` para asegurar que su localización coincida con la de la `HomePage`.
*   **`validate_sections_json_locale(home_page: HomePageLocaleSource) -> list[ValidationError]`**: La función principal de validación. Utiliza `collect_sections_page_ids` para obtener todos los IDs referenciados, luego recupera esas páginas de la base de datos y, para cada una, invoca `is_page_valid_for_home_locale`. Si se encuentra alguna inconsistencia en la localización, se genera una `ValidationError`.

## Arquitectura y Relaciones de Componentes

El módulo `HomePageLocaleSource` interactúa principalmente con los modelos de página de Wagtail, específicamente con [ArticlePage](../Shopify_Content_Models.md#ArticlePage) y [GlossaryTermPage](../Shopify_Content_Models.md#GlossaryTermPage), para validar sus localizaciones. También depende de utilidades de localización como `glossary_locale_code_for_wagtail` para manejar las particularidades de los códigos de localización del glosario.

La lógica de validación se aplica a la estructura de datos `sections_json` de la `HomePage`, que define el diseño y el contenido dinámico de la página de inicio. Esta estructura es un diccionario que contiene diferentes bloques de contenido, cada uno de los cuales puede hacer referencia a otras páginas de Wagtail por su ID.

### Diagrama de Flujo de Validación de Localización de Página de Inicio

```mermaid
graph TD
    A[HomePage con sections_json] --> B{Llamar a validate_sections_json_locale};
    B --> C{collect_sections_page_ids};
    C --> D{Extraer IDs de páginas referenciadas};
    D --> E{Consultar Páginas de Wagtail por IDs};
    E --> F{Iterar sobre cada Página Referenciada};
    F --> G{Llamar a is_page_valid_for_home_locale(HomePage, Página Referenciada)};
    G -- Es ArticlePage --> H{Comparar locale de ArticlePage con locale de HomePage};
    G -- Es GlossaryTermPage --> I{Comparar locale_code de GlossaryTermPage con locale esperado de HomePage};
    G -- Otra Página Válida --> K[Página Válida];
    H -- locales coinciden --> K;
    I -- locales coinciden --> K;
    H -- locales no coinciden --> J[Añadir ValidationError: Inconsistencia de Localización];
    I -- locales no coinciden --> J;
    F --> L{Página Desconocida?};
    L -- Sí --> M[Añadir ValidationError: Referencia de Página Desconocida];
    L -- No --> F;
    J --> N[Lista de Errores de Validación];
    M --> N;
    K --> F;
    F -- Todas las páginas procesadas --> N;
    N --> O[Devolver Lista de Errores de Validación];
```

## Cómo encaja en el Sistema General

Este módulo es un componente crítico dentro del proceso de gestión de contenido de Shopify, particularmente para las `HomePage` que actúan como puntos de entrada multilingües. Es probable que esta validación se ejecute en los siguientes contextos:

1.  **Guardado de `HomePage`**: Cuando un editor intenta guardar una instancia de `HomePage` en la interfaz de administración de Wagtail, esta validación se ejecuta para asegurar que el contenido referenciado sea localmente consistente antes de que los cambios se persistan en la base de datos. Esto previene la publicación de páginas con enlaces rotos o inapropiados para la localización.
2.  **Sincronización de Contenido**: Durante los procesos de sincronización de contenido o las tareas de importación, este módulo puede ser invocado para auditar y validar la coherencia de localización de las `HomePage` existentes, marcando cualquier discrepancia que deba ser corregida manualmente o a través de herramientas de corrección.

Este módulo se apoya en los modelos definidos en [Shopify_Content_Models.md](../Shopify_Content_Models.md) y en la lógica de localización de glosarios, lo que lo convierte en una pieza fundamental para la robustez del sistema de gestión de contenido localizado.
# Validación de Localización para Páginas de Inicio

Este módulo, `Home_Page_Locale_Validation`, es responsable de asegurar la coherencia de las referencias de página dentro del `sections_json` de una `HomePage` con la localización asignada a dicha página. Garantiza que el contenido editorial referenciado sea apropiado para el locale de la página de inicio, previniendo así la visualización de contenido en idiomas incorrectos o de páginas inexistentes.

## Propósito y Funcionalidad Principal

El módulo se centra en la validación de las referencias a otras páginas de Wagtail incrustadas en el JSON de secciones de una página de inicio. Su función principal es:

1.  **Extraer IDs de páginas referenciadas**: Recopila todos los identificadores de páginas de Wagtail que están vinculados desde los diferentes bloques de contenido en el `sections_json` de una `HomePage`.
2.  **Validar la localización de las páginas referenciadas**: Comprueba que las páginas de `ArticlePage` y `GlossaryTermPage` referenciadas coincidan con la localización de la `HomePage` principal.
3.  **Generar errores de validación**: Reporta cualquier inconsistencia de localización o referencia a páginas inexistentes como errores de validación.

### Componentes Principales

#### `HomePageLocaleSource`

Es un protocolo (`Protocol`) que define la interfaz esperada para cualquier objeto que represente una página de inicio a los efectos de este módulo de validación. Requiere los atributos `locale` (que contendrá el objeto de localización de Django/Wagtail) y `sections_json` (un diccionario que describe la estructura de las secciones de la página de inicio).

#### `collect_sections_page_ids(sections_json: dict | None) -> list[int]`

Esta función utilitaria se encarga de recorrer el diccionario `sections_json` de una `HomePage` y extraer todos los IDs de las páginas de Wagtail a las que se hace referencia. Analiza varios tipos de bloques de contenido como `featured_collections`, `nav_collection_pills`, `best_sellers`, `shop_by_need`, `educational_hub`, `internal_links` y `promo_gateway` para encontrar los `page_id` o `collection_page_id` incrustados.

#### `is_page_valid_for_home_locale(home_page: HomePageLocaleSource, page: Page) -> bool`

Esta función determina si una página de Wagtail específica (`page`) es válida para la localización de la `home_page` proporcionada. Realiza una verificación de localización para `ArticlePage` y `GlossaryTermPage`, comparando sus códigos de idioma con el de la página de inicio. Para otros tipos de páginas, asume que son válidas por defecto en cualquier localización.

#### `validate_sections_json_locale(home_page: HomePageLocaleSource) -> list[ValidationError]`

La función central del módulo. Orquesta el proceso de validación:
1.  Utiliza `collect_sections_page_ids` para obtener todos los IDs de página referenciados.
2.  Recupera las instancias de `Page` correspondientes de la base de datos, optimizando la consulta con `select_related('locale')`.
3.  Itera sobre estas páginas y, para cada una, invoca `is_page_valid_for_home_locale` para verificar la compatibilidad de localización.
4.  Si se encuentra una inconsistencia de localización (para `ArticlePage` o `GlossaryTermPage`) o una referencia a una página inexistente, se genera un objeto `ValidationError` con un código y mensaje descriptivos.
5.  Devuelve una lista de todos los errores de validación encontrados.

## Arquitectura y Relaciones de Componentes

El módulo `Home_Page_Locale_Validation` se integra dentro del sistema de gestión de contenido de Wagtail/Shopify para aplicar reglas de negocio sobre la localización del contenido.

```mermaid
graph TD
    A[HomePage] -->|Contiene sections_json| B(HomePageLocaleSource)
    B -->|Llama a| C{validate_sections_json_locale}
    C -->|Obtiene IDs de páginas| D[collect_sections_page_ids]
    D -->|IDs de Páginas| C
    C -->|Consulta Páginas de Wagtail| E[Page.objects.filter()]
    E -->|Páginas recuperadas| C
    C -->|Valida cada página| F{is_page_valid_for_home_locale}
    F -->|Depende de| G[ArticlePage]
    F -->|Depende de| H[GlossaryTermPage]
    F -->|Utiliza| I[glossary_locale_code_for_wagtail]
    C -->|Reporta| J[ValidationError]

    subgraph shopify_content/home_locale_validation.py
        B
        C
        D
        F
    end

    subgraph shopify_content/models/blog.py
        G
    end

    subgraph shopify_content/models/glossary.py
        H
    end

    subgraph shopify_content/glossary_locale_utils.py
        I
    end

    subgraph wagtail.models
        E
    end
```

**Flujo de Datos y Control:**

1.  Una instancia de `HomePage` (que se ajusta al protocolo `HomePageLocaleSource`) pasa su `sections_json` y `locale` a la función `validate_sections_json_locale`.
2.  `validate_sections_json_locale` utiliza `collect_sections_page_ids` para extraer una lista de identificadores de páginas incrustados en `sections_json`.
3.  Con estos IDs, realiza una consulta a la base de datos (`Page.objects.filter()`) para obtener las instancias de `Page` correspondientes.
4.  Para cada página recuperada, `validate_sections_json_locale` invoca `is_page_valid_for_home_locale` para verificar si la página es válida para el locale de la `HomePage`.
5.  `is_page_valid_for_home_locale` examina el tipo específico de la página (`ArticlePage`, `GlossaryTermPage`) y compara su locale con el de la `HomePage`, utilizando `glossary_locale_code_for_wagtail` si es necesario.
6.  Si se detecta alguna discrepancia o referencia a una página inexistente, se crean y acumulan objetos `ValidationError`.
7.  Finalmente, `validate_sections_json_locale` devuelve la lista de errores.

## Integración en el Sistema General

Este módulo es una parte crucial del subsistema de [Shopify_Content_Management](../Shopify_Content_Management.md) dentro de la plataforma de [Wagtail_Content_Management___API](../../Wagtail_Content_Management___API.md).

*   **Validación de Modelos Wagtail**: La lógica de validación proporcionada por `validate_sections_json_locale` se invocaría típicamente como parte del proceso de limpieza o guardado de una `HomePage` en Wagtail, probablemente a través de un método `clean()` en el modelo o un `form` asociado. Esto asegura que los editores de contenido no puedan guardar una `HomePage` con referencias de localización inconsistentes.
*   **Coherencia del Contenido**: Al aplicar esta validación, el sistema garantiza que la `HomePage` presente contenido relevante para su localización, mejorando la experiencia del usuario y manteniendo la integridad de los datos editoriales.
*   **Dependencias de Modelos**: Depende directamente de los modelos de contenido [Blog_Content_Models](Blog_Content_Models.md) (para `ArticlePage`) y [Glossary_Content_Models](Glossary_Content_Models.md) (para `GlossaryTermPage`), así como de las capacidades de localización de Wagtail (`Page.locale`).
*   **Utilidades de Localización**: Se apoya en utilidades de localización como `glossary_locale_code_for_wagtail` para manejar las particularidades de los códigos de localización de los términos del glosario.

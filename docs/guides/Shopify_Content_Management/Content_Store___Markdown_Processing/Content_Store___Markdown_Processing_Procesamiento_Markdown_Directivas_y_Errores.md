# Procesamiento de Markdown: Directivas y Errores

Este módulo se encarga de la identificación y el procesamiento de directivas personalizadas incrustadas en el contenido Markdown, así como de la gestión de errores específicos que pueden surgir durante este proceso. Proporciona las herramientas necesarias para extender la funcionalidad de Markdown estándar, permitiendo la inclusión de componentes dinámicos como productos, colecciones y llamadas a la acción directamente en el contenido editorial.

## Componentes del Módulo

### shopify_content/content_store/markdown/directives.py

Este archivo define la estructura y la lógica para el análisis de directivas Markdown personalizadas, que permiten insertar componentes dinámicos en el contenido editorial. Estas directivas siguen una gramática similar a Markdoc y se definen en líneas separadas.

#### `Component`

```python
@dataclass(frozen=True)
class Component:
    kind: str
    attrs: dict[str, str]
```

La clase `Component` es un dataclass inmutable que representa una directiva Markdown analizada. Contiene los siguientes atributos:

*   `kind` (str): El tipo de componente (por ejemplo, "product", "collection", "page", "callout", "/callout").
*   `attrs` (dict[str, str]): Un diccionario de atributos clave-valor asociados con la directiva. Estos atributos se utilizan para configurar el comportamiento o la presentación del componente.

#### `parse_attrs(raw: str) -> dict[str, str]`

Esta función se encarga de analizar una cadena de atributos en bruto (`raw`) y convertirla en un diccionario de pares clave-valor. Utiliza `shlex.split` para manejar el análisis de la cadena, lo que permite el uso de comillas y espacios en los valores de los atributos.

**Manejo de Errores:**
*   Lanza `MarkdownRenderError` si la cadena de atributos es inválida (por ejemplo, formato incorrecto de clave=valor, nombres de atributos inválidos o atributos duplicados).

#### `parse_directive_line(stripped: str, *, line: int = 0) -> Optional[Component]`

Esta es la función principal para identificar y analizar una línea de directiva Markdown. Toma una línea de texto (`stripped`) y, si coincide con un patrón de directiva conocido, devuelve una instancia de `Component`.

**Tipos de Directivas Soportadas:**
*   `{% product ... %}`: Directiva para insertar un componente de producto.
*   `{% collection ... %}`: Directiva para insertar un componente de colección.
*   `{% page ... %}`: Directiva para insertar un componente de página.
*   `{% callout ... %}`: Directiva para iniciar un bloque de llamada a la acción.
*   `{% /callout %}`: Directiva para cerrar un bloque de llamada a la acción.

**Manejo de Errores:**
*   Lanza `MarkdownRenderError` si la directiva es desconocida o está mal formada.
*   Devuelve `None` si la línea no es una directiva válida.

#### `supports_ref_attribute(attrs: dict[str, str]) -> bool`

Esta función auxiliar verifica si un diccionario de atributos contiene una clave `ref` o alguna clave que comience con `ref=`. Aunque actualmente no es un requisito, está diseñada para soportar futuras funcionalidades de identificación de referencias junto con el manejo de `handle/path`.

### shopify_content/content_store/markdown/errors.py

Este archivo define una excepción personalizada utilizada específicamente para errores durante el procesamiento de directivas Markdown editoriales.

#### `MarkdownRenderError`

```python
class MarkdownRenderError(ValueError):
    """Raised when an editorial component directive is invalid."""
```

`MarkdownRenderError` es una subclase de `ValueError` que se lanza cuando una directiva de componente editorial en Markdown es inválida. Esto ayuda a capturar y manejar errores específicos relacionados con la sintaxis o el uso incorrecto de las directivas en el contenido.

## Arquitectura y Relaciones entre Componentes

El módulo `Procesamiento de Markdown: Directivas y Errores` es una parte fundamental del sistema de gestión de contenido Markdown. `directives.py` depende directamente de `errors.py` para reportar problemas encontrados durante el análisis de las directivas. Estas directivas se analizan como parte de un proceso más amplio de procesamiento de Markdown, probablemente orquestado por componentes en la ruta `shopify_content/content_store/markdown/parser.py`, el cual utiliza las directivas analizadas para construir bloques de contenido enriquecido.

```mermaid
graph TD
    subgraph Módulo de Procesamiento de Markdown
        A[shopify_content/content_store/markdown/directives.py] -- "Define Componentes y Lógica de Análisis" --> B(Component)
        A -- "Lanza" --> C(MarkdownRenderError)
        A -- "Usa" --> D[parse_attrs]
        A -- "Usa" --> E[parse_directive_line]
        A -- "Usa" --> F[supports_ref_attribute]
        C -- "Definida en" --> G[shopify_content/content_store/markdown/errors.py]
    end

    subgraph Flujo de Procesamiento de Contenido
        H[Contenido Markdown Raw] --> E
        E -- "Componente Analizado (si es válido)" --> I[Procesador de Bloques de Markdown (e.g., MarkdownBlock en parser.py)]
        E -- "Error de Directiva" --> J(Manejo de Errores)
    end

    G --- C
```

*   **`directives.py`**: Contiene la lógica para interpretar y estructurar las directivas. Define la clase `Component` que es la representación en memoria de una directiva parseada.
*   **`errors.py`**: Proporciona la excepción `MarkdownRenderError` que es utilizada por `directives.py` para señalar problemas con las directivas. Esto asegura una gestión de errores consistente y específica.
*   **`parser.py` (Referencia)**: Aunque no está en el ámbito de este documento, el archivo `shopify_content/content_store/markdown/parser.py` (con el componente `MarkdownBlock`) sería el consumidor principal de las funciones definidas en `directives.py`, utilizando los `Component`s para construir una representación estructurada del contenido Markdown.

## Integración en el Sistema General

Este módulo se integra en el sistema de gestión de contenido de Shopify para enriquecer el Markdown con capacidades dinámicas. Al permitir la incrustación de directivas como `product`, `collection` o `callout`, el sistema puede renderizar contenido que va más allá del texto estático. Esto es crucial para:

*   **Generación de Contenido Dinámico**: Insertar información actualizada de productos, colecciones o enlaces a páginas directamente en artículos o descripciones.
*   **Mejora de la Experiencia Editorial**: Proporcionar a los editores una forma sencilla de añadir elementos interactivos y ricos en datos sin necesidad de HTML complejo o lógica de programación.
*   **Validación Temprana de Contenido**: La detección temprana de errores de directiva a través de `MarkdownRenderError` asegura que el contenido mal formado no llegue a las etapas de renderizado final, mejorando la robustez del sistema.

Las directivas procesadas por este módulo probablemente se transforman en bloques de contenido (`StreamBlock` en Wagtail, como se ve en [Wagtail_Content_Blocks.md](../Wagtail_Content_Blocks.md)) que luego son renderizados en la interfaz de usuario. Esto permite una clara separación entre el contenido (Markdown con directivas) y su presentación (bloques de Wagtail).

# Almacenamiento y Serialización de Contenido Markdown

Este módulo es responsable del almacenamiento persistente y la serialización/deserialización del contenido editorial, utilizando un formato basado en Markdown con "frontmatter" YAML. Es un componente fundamental para la gestión de contenido, asegurando que los datos editoriales se puedan guardar, leer y procesar de manera consistente.

## Componentes Principales

Los componentes clave en este módulo son:

*   `FilesystemContentRepository`: Gestiona el almacenamiento y recuperación de contenido en el sistema de archivos.
*   `FrontmatterVerbatimSerializer`: Se encarga de la serialización y deserialización de contenido editorial en el formato Markdown con "frontmatter" YAML.

## Arquitectura y Relaciones

El módulo de Almacenamiento y Serialización de Contenido Markdown interactúa estrechamente con otros componentes del sistema de gestión de contenido. El `FilesystemContentRepository` utiliza el `FrontmatterVerbatimSerializer` para manejar el formato del contenido antes de almacenarlo o después de leerlo del disco. Ambos dependen de las definiciones de contratos (`ContentRef`, `ContentDocument`, `CanonicalDocument`, etc.) definidas en el módulo de Contratos.

```mermaid
graph TD
    subgraph Módulo de Almacenamiento y Serialización
        A[FilesystemContentRepository] --> B[FrontmatterVerbatimSerializer]
    end

    B --> C[Contratos de Contenido (ContentRef, ContentDocument, etc.)]
    A -- "Lee/Escribe archivos" --> D[Sistema de Archivos]
    C -- "Definiciones" --> E[shopify_content/content_store/contracts.py]

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style C fill:#ccf,stroke:#333,stroke-width:2px
    style D fill:#afa,stroke:#333,stroke-width:2px
    style E fill:#ccf,stroke:#333,stroke-width:2px

```

### FilesystemContentRepository

El `FilesystemContentRepository` es una implementación del contrato `ContentRepository` que persiste el contenido editorial como archivos individuales en el sistema de archivos. Opera puramente con `ContentRef` y texto serializado, sin conocimiento directo de los modelos de Django. Asegura escrituras atómicas para mantener la integridad de los datos.

#### Funcionalidades Clave:

*   **Inicialización**: Se configura con un directorio raíz (`root`) donde se almacenarán los archivos y un serializador (por defecto, `FrontmatterVerbatimSerializer`).
*   **`_abs(ref: ContentRef) -> Path`**: Convierte una referencia de contenido (`ContentRef`) en una ruta absoluta segura dentro del directorio raíz del repositorio, previniendo accesos a rutas fuera del directorio permitido.
*   **`exists(ref: ContentRef) -> bool`**: Verifica si un documento de contenido existe en la ruta especificada por `ContentRef`.
*   **`read(ref: ContentRef) -> ContentDocument`**: Lee el contenido de un archivo y lo deserializa en un objeto `ContentDocument`.
*   **`read_canonical(ref: ContentRef) -> CanonicalDocument`**: Lee el contenido de un archivo, lo deserializa en un `CanonicalDocument`, incluyendo metadatos, formato, checksum y referencias derivadas (si están disponibles).
*   **`write(ref: ContentRef, value: str, *, meta: Optional[Mapping[str, str]] = None, expected_version: Optional[str] = None) -> ContentDocument`**: Escribe el contenido en un archivo. Admite una `expected_version` para garantizar escrituras atómicas, previniendo conflictos si el contenido ha cambiado desde la última lectura. Utiliza `_atomic_write` para asegurar la integridad.
*   **`delete(ref: ContentRef) -> None`**: Elimina el archivo de contenido asociado a la referencia.
*   **`_atomic_write(path: Path, text: str) -> None`**: Un método estático que realiza una escritura atómica. Escribe el contenido en un archivo temporal dentro del mismo directorio y luego lo reemplaza por el archivo de destino, garantizando que el archivo nunca esté en un estado inconsistente.

#### Relación con otros módulos:

*   **[Contratos de Contenido (ContentRef, ContentDocument)](Content_Store___Markdown_Processing_Contratos.md)**: El `FilesystemContentRepository` depende fuertemente de las interfaces definidas en `contracts.py` para representar referencias, documentos y posibles conflictos de contenido.
*   **`FrontmatterVerbatimSerializer`**: Utiliza este serializador para convertir entre objetos `ContentDocument` y la representación en cadena de los archivos de contenido.
*   **`shopify_content/content_store/markdown/references.py`**: Importa opcionalmente `extract_reference_tokens` para procesar referencias dentro del cuerpo del Markdown al leer contenido canónico. Este módulo se detalla en [Procesamiento de Markdown](../Content_Store___Markdown_Processing.md).

### FrontmatterVerbatimSerializer

El `FrontmatterVerbatimSerializer` es responsable de serializar y deserializar el contenido editorial en un formato canónico que consta de un bloque "frontmatter" YAML seguido del cuerpo de Markdown. Este formato es legible por editores externos sin dependencias en tiempo de ejecución.

#### Funcionalidades Clave:

*   **`fmt`**: Define el formato como `"markdown"`.
*   **`checksum(value: str) -> str`**: Genera un hash SHA256 del valor del contenido para verificación de integridad (no autoridad de contenido).
*   **`_content_locale(ref: ContentRef) -> str`**: Convierte la configuración regional de `ContentRef` a un formato de configuración regional de contenido, manejando `UnsupportedLocale`.
*   **`_meta_to_strings(data: Mapping[str, Any]) -> dict[str, str]`**: Convierte los valores de metadatos a cadenas para su inclusión en el "frontmatter" YAML.
*   **`split_frontmatter(raw: str) -> tuple[dict[str, str], str, bool]`**: Una función auxiliar que analiza una cadena de contenido para extraer el "frontmatter" YAML y el cuerpo del contenido. Puede levantar `InvalidEditorialFrontmatter` si el "frontmatter" no es válido.
*   **`dumps(self, ref: ContentRef, value: str, *, meta: Mapping[str, str]) -> str`**: Serializa un `ContentRef`, el valor del cuerpo y los metadatos en una cadena con "frontmatter" YAML. Incluye `content_type`, `object_id`, `field_key`, `locale` y `format` en el "frontmatter".
*   **`loads(self, ref: ContentRef, raw: str) -> ContentDocument`**: Deserializa una cadena de contenido (con "frontmatter" YAML) en un objeto `ContentDocument`, extrayendo los metadatos y el cuerpo.

#### Relación con otros módulos:

*   **[Contratos de Contenido (ContentDocument, ContentRef, InvalidEditorialFrontmatter)](Content_Store___Markdown_Processing_Contratos.md)**: Utiliza las estructuras de datos definidas en `contracts.py` para representar el contenido deserializado y manejar errores de formato.
*   **`shopify_content/content_store/locales.py`**: Depende de `UnsupportedLocale` y `to_content_locale` para el manejo de la configuración regional del contenido.

## Integración en el Sistema General

El módulo `Content_Store___Markdown_Processing_Almacenamiento_y_Serializacion` es un pilar fundamental en la arquitectura de gestión de contenido de Shopify. Proporciona los mecanismos para la persistencia del contenido editorial, permitiendo a otros módulos:

*   **Guardar y Recuperar Contenido**: Otros servicios o interfaces de usuario pueden utilizar el `FilesystemContentRepository` para almacenar y recuperar el contenido generado o editado.
*   **Estandarización del Formato**: El `FrontmatterVerbatimSerializer` impone un formato consistente para el contenido editorial, lo que facilita la interoperabilidad con herramientas externas (como Keystatic y Obsidian) y garantiza la integridad de los datos.
*   **Procesamiento de Markdown**: Almacena el contenido en un formato Markdown que puede ser posteriormente procesado por el módulo padre [Procesamiento de Markdown](../Content_Store___Markdown_Processing.md) para renderizarlo o extraer información adicional.
*   **Sincronización de Contenido**: Sirve como una fuente de verdad para el contenido editorial en el sistema de archivos, que luego puede ser sincronizado con la base de datos de Django o con Shopify a través de procesos de sincronización (ver [Sincronización de Contenido y Comandos de Gestión](../Content_Synchronization___Management_Commands.md)).

En resumen, este módulo aísla la lógica de almacenamiento y serialización, proporcionando una capa robusta y desacoplada para manejar el contenido editorial subyacente. Su diseño se centra en la fidelidad del formato y la capacidad de edición externa, lo que es crucial para un sistema de gestión de contenido flexible y mantenible.

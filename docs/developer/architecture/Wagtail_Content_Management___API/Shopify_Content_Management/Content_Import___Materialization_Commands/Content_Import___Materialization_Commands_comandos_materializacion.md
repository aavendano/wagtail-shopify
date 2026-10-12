# Comandos de Materialización de Contenido

Este módulo proporciona comandos de administración de Django para materializar contenido desde la base de datos de Wagtail a un almacén de contenido autoritario de Git. Estos comandos son cruciales para migrar y mantener el contenido en un entorno con control de versiones, especialmente para el contenido editorial y los cuerpos de markdown de los artículos.

### Propósito y Funcionalidad Principal

El módulo `Content_Import___Materialization_Commands_comandos_materializacion` se encarga de transferir contenido existente en el sistema de gestión de contenido Wagtail (específicamente, los campos `StreamField` de artículos y campos editoriales designados) a un repositorio de contenido basado en Git. Esto permite que el contenido sea gestionado y versionado de manera nativa en Git, facilitando flujos de trabajo editoriales que involucran revisiones y despliegues controlados.

Los comandos principales son:

*   `materialize_article_markdown`: Transfiere el cuerpo de los artículos (`ArticlePage.body`) de Wagtail, que originalmente es un `StreamField`, a archivos Markdown nativos en Git (`body.md`). El HTML renderizado se conserva textualmente para evitar pérdidas durante la transición.
*   `materialize_editorial_content`: Materializa campos editoriales específicos de diferentes modelos de página de Wagtail (como descripciones de blogs, definiciones de glosarios, etc.) en el árbol de contenido de Git.

### Arquitectura y Relaciones de Componentes

Los comandos de materialización interactúan con los siguientes componentes clave:

*   **Modelos de Wagtail**: Los comandos consultan `ArticlePage`, `BlogPage`, `GlossaryTermPage`, `LocationPage` y otros modelos de contenido definidos en [Modelos Base de Contenido y Mixins](../Content_Base_Models___Mixins.md), [Modelos de Contenido de Blog](../Blog_Content_Models.md), [Modelos de Contenido de Glosario](../Glossary_Content_Models.md), y [Modelos de Contenido de Ubicación](../Location_Content_Models.md) para extraer el contenido a materializar.
*   **Repositorio de Contenido (Git)**: A través de `shopify_content.content_store.accessors.get_repository`, los comandos obtienen una instancia del repositorio de contenido (normalmente un `FilesystemContentRepository` para Git), que se encarga de leer y escribir archivos en el sistema de archivos. Ver [Lógica Editorial y Content Store](../Content_Store___Editorial_Logic.md).
*   **Resolución de Referencias y Localización**: `shopify_content.content_store.refs.ref_for` y `shopify_content.content_store.refs.relative_path` se utilizan para determinar las rutas de archivo dentro del repositorio de Git para el contenido materializado. La gestión de locales se realiza a través de `shopify_content.content_store.locales.UnsupportedLocale`.
*   **Serialización y Renderizado**:
    *   `shopify_content.sync.outbound._render_streamfield_html` se utiliza para renderizar el `StreamField` de `ArticlePage` a HTML.
    *   `shopify_content.content_store.accessors.db_text` se usa para extraer el texto de campos editoriales.
    *   `shopify_content.content_store.serializers.checksum` para comparar el contenido y detectar divergencias.
*   **Configuración del Sistema**: La existencia y ubicación del repositorio de contenido se define por `CONTENT_STORE_ROOT`, que se verifica al inicio de los comandos.

```mermaid
graph TD
    subgraph Comandos de Materialización
        A[Command: materialize_article_markdown] -->|Extrae contenido de| B(ArticlePage - Modelos Wagtail)
        C[Command: materialize_editorial_content] -->|Extrae contenido de| D(BlogPage, GlossaryTermPage, LocationPage - Modelos Wagtail)
    end

    B -- Renderiza StreamField a HTML --> E[Renderizador de StreamField]
    D -- Extrae texto de campo --> F[Accesor de Texto de Base de Datos]

    E --> G[Contenido HTML/Markdown]
    F --> G

    G -- Genera Referencias de Contenido --> H[Ref_for / Relative_path]
    H -- Accede al Repositorio de Contenido --> I[Content Repository (FilesystemContentRepository)]
    I -- Escribe/Actualiza Archivos --> J[Archivos .md en Git]

    subgraph Dependencias
        K(shopify_content.content_store.accessors)
        L(shopify_content.content_store.locales)
        M(shopify_content.content_store.refs)
        N(shopify_content.content_store.serializers)
        O(shopify_content.sync.outbound)
    end

    A -- Usa --> K
    A -- Usa --> L
    A -- Usa --> M
    A -- Usa --> N
    A -- Usa --> O
    C -- Usa --> K
    C -- Usa --> L
    C -- Usa --> M
    C -- Usa --> N

    I -- Configurado por --> P(CONTENT_STORE_ROOT)

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style C fill:#f9f,stroke:#333,stroke-width:2px
    style J fill:#ccf,stroke:#333,stroke-width:2px
    linkStyle 0 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 1 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 2 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 3 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 4 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 5 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 6 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 7 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 8 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 9 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 10 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 11 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 12 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 13 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 14 stroke:#666,stroke-width:1px,fill:none;
```
*Diagrama 1: Arquitectura de los Comandos de Materialización de Contenido.*

### Flujo de Ejecución y Proceso

#### Comando `materialize_article_markdown`

Este comando se utiliza para migrar el contenido de los `StreamField` de los artículos de Wagtail a archivos Markdown en el repositorio de Git. Es una migración operativa, no un efecto secundario en tiempo de ejecución. Su objetivo es mover la autoridad del contenido a Git sin realizar una conversión con pérdida de HTML a Markdown inicialmente, permitiendo que los editores o agentes normalicen el contenido semánticamente con el tiempo.

```mermaid
graph TD
    A[Inicio: materialize_article_markdown] --> B{CONTENT_STORE_ROOT configurado?};
    B -- No --> C[Error: CONTENT_STORE_ROOT no configurado];
    B -- Sí --> D[Obtener Repositorio de Contenido];
    D --> E[Consultar ArticlePage (opcionalmente por locale)];
    E --> F{Para cada ArticlePage en la consulta};
    F --> G[Incrementar stats.examined];
    G --> H[Generar ContentRef para 'body'];
    H --> I{Locale Soportado?};
    I -- No --> J[Incrementar stats.unsupported_locale, Saltar página];
    I -- Sí --> K[Renderizar StreamField de ArticlePage.body a HTML (_render_streamfield_html)];
    K --> L{Archivo .md existe en Repo?};
    L -- Sí --> M[Leer contenido existente];
    M --> N{Contenido existente == Contenido nuevo?};
    N -- Sí --> O[Incrementar stats.identical, Continuar];
    N -- No --> P{--force usado?};
    P -- No --> Q[Incrementar stats.divergent_skipped, Reportar divergencia, Continuar];
    P -- Sí --> R{--dry-run usado?};
    R -- No --> S[Escribir/Sobrescribir archivo en Repo];
    R -- Sí --> T[Reportar sobrescritura];
    S --> U[Incrementar stats.overwritten];
    T --> U;
    L -- No --> V{--dry-run usado?};
    V -- No --> W[Escribir archivo en Repo (incluso vacío)];
    V -- Sí --> X[Reportar creación];
    W --> Y[Incrementar stats.created];
    X --> Y;
    U --> F;
    Y --> F;
    F --> Z[Fin del bucle];
    Z --> AA[Reportar estadísticas finales];
    J --> F;
    Q --> F;
    O --> F;
```
*Diagrama 2: Flujo de Proceso del Comando `materialize_article_markdown`.*

#### Comando `materialize_editorial_content`

Este comando gestiona la materialización de campos editoriales específicos definidos en `MIRRORED_FIELDS` desde la base de datos de Wagtail hacia el árbol de contenido de Git. Es una herramienta de migración controlada e idempotente, diseñada para ser ejecutada una vez por campo para establecer el `worktree` autoritario.

```mermaid
graph TD
    A[Inicio: materialize_editorial_content] --> B{CONTENT_STORE_ROOT configurado?};
    B -- No --> C[Error: CONTENT_STORE_ROOT no configurado];
    B -- Sí --> D[Obtener Repositorio de Contenido];
    D --> E[Identificar modelos y campos de MIRRORED_FIELDS (filtrar por --field)];
    E --> F{Para cada modelo y campo objetivo};
    F --> G[Consultar páginas del modelo (opcionalmente por locale)];
    G --> H{Para cada página en la consulta};
    H --> I[Incrementar stats.examined];
    I --> J[Obtener valor del campo editorial (db_text)];
    J --> K[Generar ContentRef para el campo];
    K --> L{Locale Soportado?};
    L -- No --> M[Incrementar stats.unsupported_locale, Saltar página];
    L -- Sí --> N{Archivo .md existe en Repo?};
    N -- Sí --> O[Leer contenido existente];
    O --> P{Contenido existente == Contenido nuevo?};
    P -- Sí --> Q[Incrementar stats.identical, Continuar];
    P -- No --> R{--force usado?};
    R -- No --> S[Incrementar stats.divergent_skipped, Reportar divergencia, Continuar];
    R -- Sí --> T{--dry-run usado?};
    T -- No --> U[Escribir/Sobrescribir archivo en Repo];
    T -- Sí --> V[Reportar sobrescritura];
    U --> W[Incrementar stats.overwritten];
    V --> W;
    N -- No --> X{--dry-run usado?};
    X -- No --> Y[Escribir archivo en Repo];
    X -- Sí --> Z[Reportar creación];
    Y --> AA[Incrementar stats.created];
    Z --> AA;
    W --> H;
    AA --> H;
    H --> BB[Fin del bucle interno];
    BB --> F;
    M --> H;
    S --> H;
    Q --> H;
    F --> CC[Fin del bucle externo];
    CC --> DD[Reportar estadísticas finales];
```
*Diagrama 3: Flujo de Proceso del Comando `materialize_editorial_content`.*

### Cómo el Módulo Encaja en el Sistema General

Este módulo es una pieza fundamental en el puente entre el sistema de gestión de contenido de Wagtail y el repositorio de contenido basado en Git, que actúa como la fuente de verdad autoritaria para el contenido editorial y los artículos.

*   **Integración con Wagtail**: Los comandos interactúan directamente con los modelos de Wagtail y su `StreamField` para extraer el contenido. Esto permite a los editores seguir utilizando la interfaz de Wagtail para la creación de contenido, mientras que el resultado final es materializado en Git.
*   **Sistema de Contenido Autoritaro en Git**: Al materializar el contenido en Git, se habilita un flujo de trabajo de "Git-first" o "Git-authoritative" para el contenido, lo que es esencial para procesos de despliegue, revisión y colaboración que se basan en el control de versiones. Esto es particularmente importante para la renderización del `body.md` de los artículos, que luego puede ser procesado por otras herramientas o pipelines.
*   **Migración Operacional**: Estos comandos son herramientas de migración que se ejecutan una sola vez o bajo demanda para sincronizar la base de datos de Wagtail con el repositorio de Git, en lugar de ser parte del flujo de trabajo de ejecución normal de la aplicación.
*   **Extensibilidad**: El comando `materialize_editorial_content` está diseñado para ser extensible, permitiendo la adición de nuevos campos editoriales a la lista `MIRRORED_FIELDS` para su materialización futura.

Se relaciona estrechamente con:

*   [Comandos de Importación de Contenido](Content_Import___Materialization_Commands_comandos_importacion.md)
*   [Lógica Editorial y Content Store](../Content_Store___Editorial_Logic.md)
*   [Modelos Base de Contenido y Mixins](../Content_Base_Models___Mixins.md)
*   [Modelos de Contenido de Blog](../Blog_Content_Models.md)
*   [Modelos de Contenido de Glosario](../Glossary_Content_Models.md)
*   [Modelos de Contenido de Ubicación](../Location_Content_Models.md)
*   [Servicios de Sincronización de Contenido](../Content_Synchronization_Services.md)

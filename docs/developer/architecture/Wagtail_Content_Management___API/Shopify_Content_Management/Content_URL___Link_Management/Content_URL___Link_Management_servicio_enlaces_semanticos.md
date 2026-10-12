# Servicio de Enlaces Semánticos


Este módulo (`shopify_content/semantic_links/service.py`) gestiona la generación, sugerencia y persistencia de enlaces internos semánticos dentro del sistema de gestión de contenido de Wagtail, integrándose con el ecosistema de Shopify. Su función principal es automatizar la creación de enlaces relacionados entre diferentes tipos de páginas (productos, colecciones, artículos, términos de glosario) utilizando capacidades de búsqueda vectorial.

## 1. Propósito y Funcionalidad Principal

El servicio de enlaces semánticos tiene como objetivo mejorar la navegabilidad y el SEO del contenido gestionado en Wagtail al sugerir y mantener automáticamente enlaces relevantes entre páginas. Las funcionalidades clave incluyen:

*   **Sugerencia de Enlaces Relacionados**: Utiliza un índice vectorial (`PageIndex` de `django_ai_core`) para encontrar páginas semánticamente similares a una página de origen.
*   **Clasificación y Filtrado**: Las páginas sugeridas se clasifican por tipo (producto, colección, artículo, glosario) y se filtran por localidad y estado de publicación (`live`, `ACTIVE`).
*   **Gestión de Enlaces Híbridos**: Para las páginas de productos, el servicio combina la búsqueda vectorial con una búsqueda ORM inversa para identificar contenido que ya enlaza al producto.
*   **Persistencia de Enlaces**: Los enlaces semánticos generados se almacenan como `SemanticPageLink` en la base de datos y se integran en el gráfico de revisión de Wagtail.
*   **Manejo de Excepciones**: Define `SemanticSuggestUnavailable` para indicar cuando el servicio de sugerencia no puede operar, generalmente debido a la falta de configuración del índice vectorial.
*   **Comandos de Gestión**: Proporciona la lógica subyacente para los comandos de Django que permiten la reconstrucción y sincronización de los enlaces semánticos ([Content_Indexing___Semantic_Link_Commands.md](../Content_Indexing___Semantic_Link_Commands.md)).

## 2. Arquitectura y Relaciones entre Componentes

El módulo `Content_URL___Link_Management_servicio_enlaces_semanticos` interactúa con varias partes del sistema para cumplir su función:

### 2.1. Componentes Internos del Módulo

*   `SemanticSuggestUnavailable`: Esta excepción se lanza cuando el índice vectorial necesario para la sugerencia semántica no está configurado o no está disponible, lo que evita que el servicio de sugerencias funcione.

### 2.2. Dependencias Clave

*   **Modelos de Contenido Wagtail**: Interactúa con [Content_Base_Models___Mixins/Content_Base_Models___Mixins_ModelosEnlacesSemanticos.md](../Content_Base_Models___Mixins/Content_Base_Models___Mixins_ModelosEnlacesSemanticos.md) (específicamente `SemanticPageLink`), así como con modelos de página específicos como `ArticlePage`, `CollectionPage`, `GlossaryTermPage` y `ProductPage` definidos en [Blog_Content_Models.md](../Blog_Content_Models.md), [Collection_Content_Models.md](../Collection_Content_Models.md), [Glossary_Content_Models.md](../Glossary_Content_Models.md) y [Product_Content_Models.md](../Product_Content_Models.md).
*   **Indexación y Búsqueda Vectorial**: Depende de `django_ai_core.contrib.index.base.registry` y el `PageIndex` para realizar búsquedas de similitud. La disponibilidad de esta funcionalidad está controlada por el ajuste `settings.WAGTAIL_AI_PGVECTOR`.
*   **Configuración de Django**: Utiliza `django.conf.settings` para determinar si los enlaces semánticos están habilitados (`SEMANTIC_LINKS_ENABLED`) y para configurar límites de sugerencias (`SEMANTIC_LINKS_LIMIT_PER_TYPE`, `SEMANTIC_LINKS_TYPE_OVERFETCH`).
*   **Señales de Wagtail**: Se integra con `wagtail.signals.page_published` para evitar la sincronización recursiva y la actualización semántica al publicar desde trabajos por lotes a través del context manager `suppress_page_published_signals`.
*   **Agentes de IA de Wagtail**: Utiliza `wagtail_ai.agents.suggested_content.SuggestedContentAgent` para ejecutar búsquedas vectoriales.

### 2.3. Diagrama de Componentes

```mermaid
graph TD
    A[Servicio de Enlaces Semánticos] --> B(shopify_content/semantic_links/service.py)
    B --> C{Modelos de Contenido Wagtail}
    B --> D{PageIndex<br>(django_ai_core)}
    B --> E{Configuración de Django}
    B --> F{Señales de Wagtail}
    B --> G{SuggestedContentAgent<br>(wagtail_ai)}

    C --> C1[ArticlePage]
    C --> C2[CollectionPage]
    C --> C3[GlossaryTermPage]
    C --> C4[ProductPage]
    C --> C5[SemanticPageLink]

    D --> D1[Motor de Base de Datos<br>PGVector]

    F --> F1[page_published]

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
```

### 2.4. Diagrama de Flujo de Datos: Refresco de Enlaces Semánticos

```mermaid
graph TD
    A[Inicio: refresh_semantic_links(pagina)] --> B{¿Enlaces Semánticos Habilitados?}
    B -- No --> Z[Retornar 0 enlaces]
    B -- Sí --> C{Extraer Contenido de la Página}
    C --> D{Identificar PKs Manuales y a Excluir}
    D --> E{¿Página de Producto?}
    E -- Sí --> F[Sugerir Enlaces Híbridos<br>(ORM Inverso + Búsqueda Vectorial)]
    E -- No --> G[Sugerir Enlaces por Tipo<br>(Búsqueda Vectorial)]
    F --> H{Consolidar Enlaces Sugeridos}
    G --> H
    H --> I{¿Modo Dry Run?}
    I -- Sí --> Z
    I -- No --> J[Eliminar Enlaces Semánticos Automáticos Existentes]
    J --> K[Crear Nuevos Enlaces Semánticos Automáticos]
    K --> L{¿Página de Glosario?}
    L -- Sí --> M[Sincronizar Caché de Enlaces Relacionados]
    L -- No --> N[Continuar]
    M --> N
    N --> O{¿Actualizar Revisión Wagtail?}
    O -- Sí --> P[Persistir Revisión con Enlaces Actualizados]
    O -- No --> Z
    P --> Q[Publicar Revisión (si la página está en vivo)]
    Q --> Z
```

## 3. Cómo Encaja el Módulo en el Sistema General

El servicio de enlaces semánticos es un componente crucial dentro del subsistema de [Content_URL___Link_Management.md](../Content_URL___Link_Management.md) de [Shopify_Content_Management.md](../../Shopify_Content_Management.md). Su rol es enriquecer automáticamente el contenido editorial con conexiones relevantes, mejorando la experiencia del usuario y la optimización para motores de búsqueda.

Se integra estrechamente con:

*   **Modelos de Contenido de Wagtail**: Define cómo se relacionan las páginas entre sí a nivel semántico.
*   **Infraestructura de Búsqueda de IA**: Aprovecha las capacidades de búsqueda vectorial para la inteligencia de enlaces.
*   **Proceso de Publicación de Wagtail**: Asegura que los enlaces semánticos se actualicen y persistan correctamente con las revisiones de las páginas.
*   **API de Contenido de Shopify**: Indirectamente, al mejorar la estructura de enlaces del contenido gestionado en Wagtail, contribuye a la calidad del contenido que potencialmente se expone a través de la [Shopify_Content_API.md](../../Shopify_Content_API.md).

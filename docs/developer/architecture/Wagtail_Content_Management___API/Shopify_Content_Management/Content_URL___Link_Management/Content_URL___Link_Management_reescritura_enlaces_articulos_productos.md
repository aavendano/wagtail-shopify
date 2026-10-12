# Reescritura de Enlaces de Artículo a Producto

Este sub-módulo se encarga de reescribir y gestionar los enlaces de productos de Shopify dentro del contenido de los artículos de Wagtail. Su objetivo principal es asegurar que los enlaces a productos sean precisos y apunten a los handles de producto correctos y actualizados en la tienda.

## Componentes Principales

### `LinkAction`

Define las posibles acciones que se pueden tomar al resolver un enlace de producto. Estas acciones guían el proceso de reescritura para determinar si un enlace debe permanecer sin cambios, ser reescrito, desenlazado o si su resolución es ambigua.

```python
class LinkAction(str, Enum):
    UNCHANGED = 'unchanged'
    REWRITE = 'rewrite'
    UNWRAP = 'unwrap'
    AMBIGUOUS = 'ambiguous'
```

### `LinkDecision`

Representa la decisión tomada para un enlace de producto específico. Contiene el handle original del producto, la acción a realizar (`LinkAction`), el handle resuelto (si aplica) y una lista de handles candidatos en caso de ambigüedad.

```python
@dataclass
class LinkDecision:
    original_handle: str
    action: LinkAction
    resolved_handle: str | None = None
    candidates: tuple[str, ...] = ()
```

### `ProductHandleResolver`

Esta clase es responsable de resolver handles de productos heredados o problemáticos a sus handles de `ProductPage` en vivo y canónicos. Utiliza una combinación de handles en vivo, mapeos de IDs de Shopify a handles y un mapa manual de reescritura, junto con lógica de coincidencia difusa para encontrar el handle correcto.

**Características Clave:**

*   **Inicialización**: Se inicializa con una colección de handles de productos "en vivo", un mapeo opcional de IDs de Shopify a handles, y un mapa manual de handles antiguos a nuevos.
*   **Normalización de Handles**: `normalize_product_handle` decodifica la codificación de porcentaje y normaliza los handles a un formato de Shopify.
*   **Resolución**: El método `resolve` toma un handle de producto crudo y devuelve una `LinkDecision` basada en la lógica de resolución (mapa manual, handles en vivo, IDs de Shopify o coincidencia difusa).
*   **Coincidencia Difusa (`_fuzzy_unique`)**: Implementa una lógica sofisticada para encontrar handles coincidentes incluso cuando no hay una coincidencia exacta, considerando prefijos, extensiones, sufijos de variantes y contención de tokens.

```python
class ProductHandleResolver:
    # ... (código del componente) ...
```

### `RewriteStats`

Un dataclass simple para acumular estadísticas sobre el proceso de reescritura de enlaces. Incluye contadores para enlaces reescritos, desenlazados, sin cambios y ambiguos, así como una lista de todas las decisiones tomadas.

```python
@dataclass
class RewriteStats:
    rewritten: int = 0
    unwrapped: int = 0
    unchanged: int = 0
    ambiguous: int = 0
    decisions: list[LinkDecision] = field(default_factory=list)

    def merge(self, other: RewriteStats) -> None:
        self.rewritten += other.rewritten
        self.unwrapped += other.unwrapped
        self.unchanged += other.unchanged
        self.ambiguous += other.ambiguous
        self.decisions.extend(other.decisions)
```

## Flujo de Trabajo

El flujo de trabajo para la reescritura de enlaces de productos en el contenido de los artículos sigue estos pasos:

1.  **Extracción de Handles**: Se extraen los handles de los productos de los atributos `href` en el HTML de los artículos.
2.  **Resolución de Handles**: Cada handle extraído se pasa a `ProductHandleResolver` para determinar la `LinkDecision` (reescribir, desenlazar, etc.).
3.  **Reescritura de HTML**: Basándose en las decisiones, los enlaces en el HTML se modifican. Los enlaces a handles resueltos se actualizan con la ruta canónica del producto, los enlaces ambiguos se dejan como están, y los enlaces no mapeados pueden ser desenlazados (manteniendo el texto interno) si se configura.
4.  **Estadísticas**: Se recopilan estadísticas durante todo el proceso para proporcionar un resumen de los cambios realizados.

## Relación con otros módulos

Este sub-módulo interactúa estrechamente con:

*   **[Utilidades de URLs de Tienda](Content_URL___Link_Management_utilidades_urls_tienda.md)**: Utiliza funciones como `product_path` para construir las URLs canónicas de los productos.
*   **Modelos de Contenido (e.g., `ProductPage`)**: El `ProductHandleResolver` se inicializa a menudo a partir de consultas de `ProductPage` para obtener los handles de productos en vivo y sus IDs de Shopify.

```mermaid
graph TD
    A[Contenido HTML del Artículo] --> B{shopify_content/article_product_links.py::rewrite_html_product_links}
    B --> C{shopify_content/article_product_links.py::ProductHandleResolver}
    C --> D[Handles de Productos en Vivo (ProductPage)]
    C --> E[Mapeo Manual de Handles]
    C --> F[shopify_content/storefront_urls.py::product_path]
    C --> G[Handles Resueltos / Decisiones de Enlace]
    B --> H[HTML Reescrito]
    B --> I[Estadísticas de Reescritura (RewriteStats)]
    D --> |`from_queryset`| C
```

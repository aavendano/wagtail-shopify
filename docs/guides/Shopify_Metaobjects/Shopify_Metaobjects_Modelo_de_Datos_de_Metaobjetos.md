# Modelo de Datos de Metaobjetos de Shopify

El módulo `Shopify_Metaobjects_Modelo_de_Datos_de_Metaobjetos` define la estructura fundamental para interactuar con los metaobjetos de Shopify. Su componente principal, la clase `Metaobject`, encapsula la representación de un metaobjeto, facilitando su creación, manipulación y serialización hacia y desde el formato utilizado por la API de Shopify.

## Propósito y Funcionalidad Principal

La clase `Metaobject` sirve como el modelo central para los metaobjetos dentro del sistema. Proporciona una abstracción para trabajar con las propiedades clave de un metaobjeto de Shopify, incluyendo su tipo, identificador (handle), ID único, y sus campos y metacampos asociados. Esto permite a los desarrolladores gestionar los metaobjetos de forma estructurada y consistente.

Las funcionalidades principales de la clase `Metaobject` incluyen:

*   **Inicialización**: Permite crear instancias de `Metaobject` con sus propiedades esenciales.
*   **Conversión desde datos de Shopify**: Proporciona métodos de clase para construir objetos `Metaobject` a partir de las respuestas JSON de la API de Shopify, mapeando automáticamente los campos y metacampos.
*   **Conversión desde diccionarios y dataclasses de Python**: Facilita la creación de metaobjetos a partir de estructuras de datos Python existentes, lo que simplifica la integración con otras partes del sistema.
*   **Serialización a campos de Shopify**: Convierte los campos del metaobjeto en el formato que la API de Shopify espera para las operaciones de escritura.
*   **Acceso y modificación de campos y metacampos**: Ofrece métodos para leer y actualizar los valores de los campos y metacampos de un metaobjeto de manera individual.

## Arquitectura y Relaciones de Componentes

La clase `Metaobject` se encuentra en el archivo `metaobjects/shopify_metaobjects/metaobject.py` y es un componente clave dentro del módulo padre `Shopify_Metaobjects`. Depende directamente del módulo `Shopify_Metaobjects_Serializacion_de_Metaobjetos` para la correcta serialización de los valores de los campos al formato de Shopify, especialmente para tipos complejos como booleanos, JSON o rich text.

A continuación, se presenta un diagrama de clases que ilustra la estructura de la clase `Metaobject` y su relación con el serializador de campos:

```mermaid
classDiagram
    class Metaobject {
        +id: Optional[str]
        +type: str
        +handle: str
        +fields: dict[str, Any]
        +metafields: dict[str, dict[str, Any]]
        +__init__(type: str, handle: str, id: Optional[str], fields: Optional[dict], metafields: Optional[dict])
        +from_shopify_data(data: dict) Metaobject
        +from_dict(data: dict, type: str, handle_key: str) Metaobject
        +from_dataclass(instance: Any, type: str, handle_field: str) Metaobject
        +to_shopify_fields(field_types: dict) list[dict]
        +get_field(key: str) Any
        +set_field(key: str, value: Any)
        +get_metafield(key: str, namespace: str) dict
        +set_metafield(key: str, value: str, type: str, namespace: str) secreter
        +to_dict() dict
    }

    class _ShopifyRichTextHTMLParser {
        +handle_starttag(tag, attrs)
        +handle_endtag(tag)
        +handle_data(data)
    }

    Metaobject ..> _ShopifyRichTextHTMLParser : utiliza para serialización rich_text
    Metaobject --> serialize_field_value : utiliza para serialización de campos

    %% External dependency not fully detailed in this module's scope
    function serialize_field_value(value, shopify_type)
```

**Explicación del Diagrama:**

*   **`Metaobject`**: La clase central que representa un metaobjeto de Shopify, con sus atributos (`id`, `type`, `handle`, `fields`, `metafields`) y sus métodos principales para la creación, manipulación y serialización.
*   **`_ShopifyRichTextHTMLParser`**: Un parser HTML interno definido en `serialization.py` (parte del módulo `Shopify_Metaobjects_Serializacion_de_Metaobjetos`) que se utiliza para convertir contenido HTML enriquecido a un formato JSON estructurado que Shopify espera para los campos de tipo `rich_text_field`. La clase `Metaobject` indirectamente depende de esta funcionalidad a través de `serialize_field_value`.
*   **`serialize_field_value`**: Una función (también parte de `Shopify_Metaobjects_Serializacion_de_Metaobjetos`) que maneja la lógica de serialización de diferentes tipos de datos Python a sus representaciones de cadena esperadas por Shopify. La clase `Metaobject` invoca esta función en su método `to_shopify_fields`.

## Cómo el Módulo Encaja en el Sistema General

El módulo `Shopify_Metaobjects_Modelo_de_Datos_de_Metaobjetos` es fundamental para cualquier interacción con metaobjetos en Shopify. Proporciona la capa de abstracción necesaria para que otros módulos del sistema puedan crear, leer, actualizar y eliminar metaobjetos sin tener que lidiar directamente con los detalles de bajo nivel de la API de Shopify.

Por ejemplo, el [módulo `Shopify_Metaobjects_Cliente_Metaobjetos`](Shopify_Metaobjects_Cliente_Metaobjetos.md) utilizará la clase `Metaobject` para encapsular los datos antes de enviarlos a la API de Shopify y para interpretar las respuestas recibidas. De manera similar, los comandos de administración o las interfaces de usuario que necesiten trabajar con metaobjetos se basarán en esta clase para estructurar y manejar la información.

Además, el [módulo `Shopify_Metaobjects_Definiciones_de_Metaobjetos`](Shopify_Metaobjects_Definiciones_de_Metaobjetos.md) podría utilizar la clase `Metaobject` para validar la estructura de los datos de un metaobjeto contra su definición, asegurando la coherencia y el cumplimiento de los esquemas esperados.

Este módulo se integra con el resto del sistema de la siguiente manera:

```mermaid
graph TD
    A[Módulo Cliente de Metaobjetos] --> B[Clase Metaobject]
    C[Módulo Definiciones de Metaobjetos] --> B
    D[Módulos de Sincronización de Contenido] --> B
    E[Módulos de Gestión de Contenido (Wagtail)] --> B
    B --> F[API de Shopify]
    B --> G[Módulo Serialización de Metaobjetos]

    subgraph Shopify_Metaobjects
        B
        G
    end
```

**Explicación del Flujo:**

1.  **Módulo Cliente de Metaobjetos**: Este módulo (representado por `metaobjects/shopify_metaobjects/client.py`) interactúa directamente con la API de Shopify. Utiliza la clase `Metaobject` para construir las cargas útiles de datos para las solicitudes y para parsear las respuestas.
2.  **Módulo Definiciones de Metaobjetos**: Este módulo (representado por `metaobjects/shopify_metaobjects/definition.py`) define las estructuras y tipos de campos para los metaobjetos. Puede usar `Metaobject` para asegurar que los datos cumplen con la definición esperada.
3.  **Módulos de Sincronización de Contenido**: Componentes como los comandos de gestión en `Shopify_Content_Management/Content_Synchronization___Management_Commands.md` que importan o exportan datos de Shopify, harán uso de la clase `Metaobject` para representar los datos durante el proceso.
4.  **Módulos de Gestión de Contenido (Wagtail)**: Las páginas y bloques de contenido de Wagtail (ver `Shopify_Content_Management/Shopify_Content_Models.md` y `Shopify_Content_Management/Wagtail_Content_Blocks.md`) que necesitan almacenar o recuperar información en metaobjetos de Shopify interactuarán con este modelo.
5.  **Módulo Serialización de Metaobjetos**: La clase `Metaobject` delega la lógica de serialización específica de tipos de campo a este módulo (representado por `metaobjects/shopify_metaobjects/serialization.py`).

En resumen, la clase `Metaobject` es el pilar para la gestión de datos de metaobjetos en el sistema, asegurando una interacción robusta y estructurada con la plataforma Shopify.
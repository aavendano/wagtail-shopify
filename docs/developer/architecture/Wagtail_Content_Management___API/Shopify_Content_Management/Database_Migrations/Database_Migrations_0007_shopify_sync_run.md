# Migración de Base de Datos 0007: Shopify Sync Run

Esta documentación describe la migración de base de datos `0007_shopify_sync_run.py`, que es responsable de crear el modelo `ShopifySyncRun` dentro del módulo `shopify_content`.

## Propósito y Funcionalidad Principal

La migración `0007_shopify_sync_run` introduce el modelo `ShopifySyncRun`, una entidad crucial para el seguimiento y la gestión de las operaciones de sincronización de contenido entre Shopify y Wagtail. Este modelo almacena información detallada sobre cada ejecución de sincronización, incluyendo su tipo (entrada o salida), el recurso objetivo, el estado, los mensajes, las estadísticas y los detalles de cualquier error.

### Modelo ShopifySyncRun

El modelo `ShopifySyncRun` captura los siguientes atributos:

*   **`id`**: Identificador único para cada ejecución de sincronización.
*   **`kind`**: Tipo de sincronización, que puede ser `inbound` (Shopify → Wagtail) o `outbound` (Wagtail → Shopify).
*   **`resource`**: El recurso de Shopify que se está sincronizando (por ejemplo, `products`, `collections`, `blogs`, o `all` para sincronizaciones de entrada completas).
*   **`new_only`**: Un indicador booleano que especifica si la sincronización solo debe procesar elementos nuevos.
*   **`celery_task_id`**: El ID de la tarea de Celery asociada con esta ejecución de sincronización, si existe.
*   **`status`**: El estado actual de la ejecución de sincronización (por ejemplo, `pending`, `running`, `success`, `failed`).
*   **`message`**: Un mensaje general sobre el progreso o el resultado de la sincronización.
*   **`stats`**: Un campo JSON que almacena estadísticas detalladas de la sincronización (por ejemplo, número de elementos creados, actualizados, etc.).
*   **`error_detail`**: Detalles específicos del error si la sincronización falla.
*   **`created_at`**: Marca de tiempo de cuándo se creó la ejecución de sincronización.
*   **`started_at`**: Marca de tiempo de cuándo comenzó la ejecución de sincronización.
*   **`finished_at`**: Marca de tiempo de cuándo finalizó la ejecución de sincronización.
*   **`page`**: Una clave foránea a `wagtailcore.Page`, que enlaza la ejecución de sincronización con una página Wagtail específica si la sincronización está relacionada con una página.

## Arquitectura y Relaciones entre Componentes

El modelo `ShopifySyncRun` se encuentra en el módulo `shopify_content` y es una entidad independiente que registra eventos. Se relaciona con el módulo `wagtailcore` a través del campo `page`, lo que permite vincular una ejecución de sincronización a una página de Wagtail específica. Esta relación es opcional (`null=True, blank=True`) y se establece con `SET_NULL` en caso de que la página referenciada sea eliminada.

### Diagrama de Entidad-Relación

```mermaid
ERD
    ShopifySyncRun {
        bigint id PK "ID"
        varchar kind "Tipo de Sincronización (inbound/outbound)"
        varchar resource "Recurso de Shopify"
        boolean new_only "Solo nuevos elementos"
        varchar celery_task_id "ID de Tarea Celery"
        varchar status "Estado de Sincronización"
        text message "Mensaje"
        json stats "Estadísticas"
        text error_detail "Detalle de Error"
        datetime created_at "Fecha de Creación"
        datetime started_at "Fecha de Inicio"
        datetime finished_at "Fecha de Finalización"
        bigint page_id FK "Página Wagtail Asociada"
    }

    wagtailcore.Page {
        bigint id PK
        -- Otros campos de Page no relevantes para esta relación
    }

    ShopifySyncRun }|--o{ wagtailcore.Page : "asociado a"

```

## Cómo encaja el módulo en el sistema general

Esta migración es fundamental para la integración de Shopify en Wagtail, ya que establece la base de datos para el monitoreo y la auditoría de todas las operaciones de sincronización. El modelo `ShopifySyncRun` es utilizado por los comandos de gestión y los servicios de sincronización dentro del módulo [Shopify Content Management](../../Shopify_Content_Management.md) para registrar el progreso, los resultados y los errores de las importaciones y exportaciones de contenido entre Shopify y Wagtail. Esto proporciona visibilidad sobre el estado de las sincronizaciones y facilita la depuración y el mantenimiento del sistema.

Depende de la migración anterior `0006_product_image_urls` del mismo módulo `shopify_content`, lo que asegura el orden correcto de aplicación de los cambios en la base de datos. También tiene una dependencia de `wagtailcore` para la referencia a `wagtailcore.Page`.

Para una comprensión más profunda de los servicios que utilizan este modelo, consulte la documentación de [Servicios de Sincronización de Contenido](../Content_Synchronization_Services.md).

# Pruebas de Desinstalación de Webhooks

Este módulo, `Webhooks_Pruebas_Desinstalacion`, contiene las pruebas unitarias para asegurar el correcto procesamiento del webhook de desinstalación de aplicaciones de Shopify. Estas pruebas verifican que la aplicación responde adecuadamente a las notificaciones de desinstalación, incluyendo la validación de la firma HMAC y la eliminación de la configuración de la tienda asociada.

## Propósito y Funcionalidad Principal

La clase `WebhookUninstalledTests` se encarga de verificar que cuando una aplicación Shopify es desinstalada por un comerciante, el sistema:
1.  Valida correctamente la autenticidad del webhook recibido.
2.  Elimina los datos de configuración de la tienda (`ShopConfig`) de la base de datos local.

### Componentes de Prueba

El archivo `webhooks/tests.py` incluye la siguiente clase de prueba:

*   **`WebhookUninstalledTests`**: Contiene métodos de prueba para el manejo del webhook `app/uninstalled`.

## Arquitectura y Relaciones de Componentes

Las pruebas en `WebhookUninstalledTests` interactúan con los siguientes componentes principales (directamente o a través de mocks):

*   **`webhooks.views.get_shopify_app`**: Una función (mocked en las pruebas) que se espera que verifique la solicitud del webhook y extraiga la información de la tienda.
*   **`core.models.ShopConfig`**: El modelo de Django que almacena la configuración de las tiendas Shopify instaladas. Este modelo se crea y se verifica su eliminación durante las pruebas.

### Diagrama de Flujo de la Prueba de Desinstalación del Webhook

El siguiente diagrama ilustra el flujo de una prueba de desinstalación de un webhook:

```mermaid
graph TD
    A[Inicio de la Prueba] --> B{Envío de Solicitud POST a /webhooks/app/uninstalled};
    B --> C{Verificación de HMAC};
    C -- HMAC Válido --> D{Extracción de Información de la Tienda};
    C -- HMAC Inválido --> E{Respuesta 401 Unauthorized};
    D --> F{Eliminación de ShopConfig};
    F --> G{Verificación de Eliminación de ShopConfig};
    G --> H[Fin de la Prueba (Éxito)];
    E --> H;

    subgraph webhooks/tests.py
        B
        C
        D
        F
        G
    end

    subgraph core/models.py
        F
    end
```

## Cómo encaja el Módulo en el Sistema General

Este módulo de pruebas es crucial para la robustez del sistema de integración con Shopify. Asegura que la aplicación responde de manera confiable a los eventos de desinstalación, manteniendo la integridad de los datos al eliminar las configuraciones de tiendas que ya no están activas.

Estas pruebas son parte del módulo [Webhooks](../Webhooks.md), que gestiona todas las interacciones de webhook entre la aplicación y Shopify. La correcta gestión de la configuración de la tienda se basa en el módulo [Core_Shopify_App](../Core_Shopify_App.md), donde reside el modelo `ShopConfig`.

Las pruebas específicas incluyen:
*   **`test_invalid_hmac_returns_sdk_response`**: Asegura que las solicitudes con HMAC inválido sean rechazadas con un código de estado 401.
*   **`test_uninstalled_deletes_shop_config_by_short_shop`**: Confirma que la configuración de la tienda se elimina cuando se proporciona un nombre de tienda corto en el webhook.
*   **`test_uninstalled_deletes_shop_config_by_full_domain_row`**: Confirma que la configuración de la tienda se elimina cuando se proporciona un nombre de dominio completo en el webhook.

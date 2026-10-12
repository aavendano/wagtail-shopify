# AppHomeVerifiedMixin

## Descripción General

`AppHomeVerifiedMixin` es un mixin de Django diseñado para asegurar que las solicitudes HTTP dirigidas a las vistas de la aplicación incrustada de Shopify han sido verificadas y provienen de Shopify App Home. Este mixin es crucial para mantener la seguridad y la integridad de las interacciones dentro de la aplicación, garantizando que solo las solicitudes válidas de Shopify sean procesadas.

## Funcionalidad Principal

El `AppHomeVerifiedMixin` intercepta el método `dispatch` de una vista. Antes de que la lógica de la vista se ejecute, realiza los siguientes pasos:

1.  **Obtención de la aplicación Shopify**: Utiliza `get_shopify_app()` para acceder a la instancia de la aplicación Shopify configurada.
2.  **Verificación de la solicitud**: Llama a `shopify_app.verify_app_home_req()` para validar la solicitud. Esta verificación incluye la comprobación de los parámetros de la solicitud enviados por Shopify, como el `id_token`.
3.  **Manejo de la ruta del token de identificación**: Proporciona la ruta a la vista `AuthPatchIdTokenView` (obtenida mediante `get_app_home_patch_id_token_path()`) que Shopify utilizará para "parchear" el `id_token` si es necesario.
4.  **Registro del resultado**: Registra el resultado de la verificación utilizando `log_shopify_result()`.
5.  **Redirección o continuación**: Si la verificación falla, convierte el resultado de Shopify en una respuesta HTTP de Django y la devuelve. Si la verificación es exitosa, invoca el método `dispatch_after_verified()` de la clase que hereda, permitiendo que la lógica de negocio de la vista se ejecute.

## Uso

Para utilizar `AppHomeVerifiedMixin`, una vista de Django debe heredar de él e implementar el método `dispatch_after_verified(self, request, *args, **kwargs)`. Este método contendrá la lógica de negocio real de la vista, que solo se ejecutará una vez que la solicitud haya sido verificada por Shopify.

```python
from django.views import View
from .mixins import AppHomeVerifiedMixin

class MiVistaSegura(AppHomeVerifiedMixin, View):
    def dispatch_after_verified(self, request, *args, **kwargs):
        # Lógica de negocio segura aquí, solo se ejecuta después de la verificación de Shopify
        return super().dispatch_after_verified(request, *args, **kwargs)

```

## Componentes Clave

*   `get_shopify_app()`: Función utilitaria para obtener la instancia de la aplicación Shopify.
*   `request_to_shopify_req()`: Convierte una solicitud HTTP de Django a un formato compatible con el SDK de Shopify.
*   `shopify_result_to_django_response()`: Convierte un resultado del SDK de Shopify en una respuesta HTTP de Django.
*   `log_shopify_result()`: Registra el resultado de las operaciones de Shopify para depuración y monitoreo.

## Relación con Otros Componentes

Este mixin es utilizado por varias vistas en `core/views.py`, como `HomeView`, `EmbeddedShopifySyncView`, `EmbeddedCommandDispatchView`, `EmbeddedInAppRedirectView` y `EmbeddedParentRedirectView`, para aplicar la lógica de verificación de Shopify de manera consistente. También interactúa con `AuthPatchIdTokenView` para el manejo del `id_token`.
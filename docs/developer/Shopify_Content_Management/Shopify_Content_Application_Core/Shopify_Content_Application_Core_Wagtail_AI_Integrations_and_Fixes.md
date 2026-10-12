# Integraciones y Correcciones de Wagtail AI

Este módulo, `Shopify_Content_Application_Core_Wagtail_AI_Integrations_and_Fixes`, se enfoca en proporcionar mejoras y correcciones críticas para la integración de funcionalidades de inteligencia artificial (IA) dentro del sistema de gestión de contenido de Wagtail, específicamente en el contexto de la aplicación Shopify. Aborda problemas comunes relacionados con la previsualización de campos `StreamField` y la robustez de las sugerencias de contenido impulsadas por IA, garantizando una experiencia de usuario y un rendimiento del sistema más estables y fiables.

## Propósito y Funcionalidad Principal

El módulo tiene dos objetivos principales:

1.  **Corregir el procesamiento de `StreamField` en previsualizaciones de páginas**: Asegura que los datos de los campos `StreamField` se manejen correctamente durante el proceso de edición y previsualización de páginas en el administrador de Wagtail, evitando la pérdida de datos o el comportamiento inesperado.
2.  **Mejorar la estabilidad y la funcionalidad de las integraciones de Wagtail AI**: Proporciona correcciones para evitar fallos en los sistemas de IA relacionados con datos obsoletos y mejora la lógica de generación de contenido sugerido.

### Componentes Principales

El módulo incluye los siguientes componentes clave:

*   `StreamFieldPreviewFixMiddleware`: Un middleware de Django que inyecta las claves `-count` faltantes para los campos `StreamField` en las solicitudes POST de edición de páginas de Wagtail, lo que es crucial para el flujo de previsualización.
*   `install_source_result_stale_guard`: Una función que modifica el comportamiento de `django-ai-core` para evitar fallos cuando existen incrustaciones de `pgvector` para páginas que ya han sido eliminadas. Esto asegura que el sistema pueda manejar documentos vectoriales obsoletos sin interrupciones.
*   `install_suggested_content_fallback`: Una función que mejora el agente de contenido sugerido de `wagtail_ai` al proporcionar contenido de reserva cuando el contenido de entrada está vacío y permite el sobrefetching de resultados para una mejor filtración por tipo.

## Arquitectura y Relaciones de Componentes

Este módulo se integra en la aplicación central de Shopify Content Management actuando como un conjunto de mejoras y adaptaciones para el marco de Wagtail, especialmente en lo que respecta a sus capacidades de IA.

### `StreamFieldPreviewFixMiddleware`

Este middleware se inserta en la cadena de procesamiento de solicitudes de Django. Intercepta las solicitudes POST dirigidas a las páginas de edición de Wagtail (`/admin/pages/<pk>/edit/`). Si detecta que faltan las claves `-count` para los `StreamField` en los datos POST, las inyecta dinámicamente utilizando el recuento actual del `StreamField` de la página.

El flujo de `StreamFieldPreviewFixMiddleware` se puede describir de la siguiente manera:

1.  **Solicitud HTTP POST**: Se inicia una solicitud POST.
2.  **StreamFieldPreviewFixMiddleware**: El middleware intercepta la solicitud.
3.  **Ruta de edición coincide**: El middleware verifica si la ruta de la solicitud coincide con una página de edición de Wagtail (`/admin/pages/<pk>/edit/`).
4.  **Verificar campos StreamField**: Si la ruta coincide, el middleware examina los campos `StreamField` en los datos POST.
5.  **Claves -count faltantes**: Si faltan las claves `-count` para algún `StreamField`.
6.  **Inyectar claves -count en request.POST**: El middleware inyecta dinámicamente las claves `-count` faltantes en los datos POST.
7.  **Continuar procesamiento Wagtail**: El procesamiento de la solicitud continúa con Wagtail.
8.  **Claves -count presentes**: Si las claves `-count` ya están presentes, el procesamiento continúa directamente a "Continuar procesamiento Wagtail".
9.  **Respuesta HTTP**: Se genera una respuesta HTTP.

### `install_source_result_stale_guard`

Esta función modifica directamente el método `_documents_to_sources` de `SourceResultMixin` de `django-ai-core`. El objetivo es manejar de forma robusta los documentos vectoriales que no tienen una página Wagtail correspondiente, lo que podría causar un fallo debido al uso estricto de `zip` en la implementación original. Al sobrescribir este método, se permite que los documentos sin una clave primaria (PK) coincidente sean omitidos, registrando una advertencia en su lugar.

El flujo de `install_source_result_stale_guard` se puede describir de la siguiente manera:

1.  **Sistema de indexación de IA**: El proceso comienza con el sistema de indexación de IA.
2.  **Método Original de Documentos a Fuentes**: Se llama al método original `_documents_to_sources`.
3.  **Llamada a install_source_result_stale_guard()**: La función `install_source_result_stale_guard()` se ejecuta y sobrescribe el método.
4.  **Sobrescribir Método de Documentos a Fuentes**: El método `_documents_to_sources` es sobrescrito para incluir la lógica de manejo de documentos obsoletos.
5.  **Procesar Documentos Vectoriales**: Los documentos vectoriales se procesan.
6.  **Documento con PK faltante/obsoleta**: Si se encuentra un documento con una clave primaria (PK) faltante u obsoleta.
7.  **Omitir documento y registrar advertencia**: El documento es omitido y se registra una advertencia.
8.  **Documento válido**: Si el documento es válido.
9.  **Mapear a objeto de Wagtail**: El documento se mapea a un objeto de Wagtail.
10. **Generar Fuentes de Resultado**: Finalmente, se generan las fuentes de resultado.

### `install_suggested_content_fallback`

Esta función envuelve el método `execute` de `SuggestedContentAgent` de `wagtail_ai`. Realiza dos mejoras clave:

1.  **Contenido de Reserva**: Si la solicitud de sugerencia de contenido se realiza con un contenido vacío pero se proporciona `exclude_pks` (lo que implica que se está editando una página existente), intenta recuperar el texto de la página excluida como contenido de reserva para generar sugerencias más relevantes.
2.  **Sobrefetching y Filtrado por Tipo**: Cuando se especifican `allowed_types` para las sugerencias, la función aumenta el límite de búsqueda (`limit`) temporalmente (multiplicándolo por `SEMANTIC_LINKS_TYPE_OVERFETCH` configurado en `django_settings` o 10 por defecto) para asegurarse de que, después de filtrar por tipo, aún haya suficientes resultados que cumplan con los criterios. Luego, filtra los resultados por los tipos de página permitidos.

El flujo de `install_suggested_content_fallback` se puede describir de la siguiente manera:

1.  **Llamada a SuggestedContentAgent.execute**: Se inicia la ejecución del agente de contenido sugerido.
2.  **install_suggested_content_fallback()**: La función intercepta la llamada.
3.  **Envuelve**: La función `execute` original es envuelta por `execute_with_fallback`.
4.  **Contenido vacío y exclude_pks**: Si el contenido de entrada está vacío y se proporcionan `exclude_pks`.
5.  **Recuperar texto de página excluida**: Se intenta recuperar el texto de la página excluida como contenido de reserva.
6.  **Allowed_types**: Si se especifican tipos permitidos para la sugerencia.
7.  **Ajustar límite de búsqueda (sobrefetch)**: El límite de búsqueda se ajusta para sobrefetching.
8.  **Llamar a SuggestedContentAgent.execute original**: Se llama al método `execute` original con los parámetros posiblemente modificados.
9.  **Resultados de IA**: Se obtienen los resultados de la IA.
10. **Si allowed_types**: Si se especificaron `allowed_types`.
11. **Filtrar resultados por tipo de página**: Los resultados se filtran según los tipos de página permitidos.
12. **Devolver resultados finales**: Se devuelven los resultados finales.
13. **Si no allowed_types**: Si no se especificaron `allowed_types`, se devuelven los resultados originales.

## Cómo encaja el módulo en el sistema general

El módulo `Shopify_Content_Application_Core_Wagtail_AI_Integrations_and_Fixes` es un componente vital dentro de la arquitectura de [Shopify_Content_Application_Core.md](Shopify_Content_Application_Core.md), ya que garantiza la estabilidad y la fiabilidad de las características avanzadas de Wagtail que dependen de la integración con sistemas de IA.

*   **Estabilidad del CMS**: `StreamFieldPreviewFixMiddleware` contribuye a una experiencia de edición de contenido más fluida en Wagtail, evitando problemas durante la previsualización de contenido rico y estructurado.
*   **Fiabilidad de las Sugerencias de IA**: Las funciones `install_source_result_stale_guard` y `install_suggested_content_fallback` son cruciales para el subsistema de enlaces semánticos y sugerencias de contenido, evitando fallos relacionados con datos obsoletos y mejorando la calidad y relevancia de las sugerencias generadas por IA. Esto impacta directamente en cómo los editores pueden utilizar las capacidades de IA para mejorar el contenido de las páginas, como las [Content_Page_Models.md](../Content_Page_Models.md) y los [Wagtail_StreamField_Blocks.md](../Wagtail_StreamField_Blocks.md).
*   **Integración con APIs Externas**: Indirectamente, estas correcciones aseguran que los agentes de IA que interactúan con el sistema de contenido, posiblemente a través de la [Content_API.md](../../../Content_API.md), funcionen de manera predecible y sin errores, especialmente cuando se manejan datos de contenido complejos.

Este módulo es un ejemplo de cómo se abordan los desafíos de integración entre los diferentes marcos (Django, Wagtail, y las bibliotecas de IA) para proporcionar un sistema de gestión de contenido robusto y eficiente.

# Configuración de Pruebas

Este módulo (`Build,_CI___Configuration_configuracion_pruebas`) se encarga de la configuración fundamental del entorno de pruebas utilizando `pytest`. Define cómo se descubren, ejecutan y configuran los tests dentro del proyecto, asegurando un proceso de prueba consistente y efectivo para las diferentes partes de la aplicación.

## Arquitectura y Componentes

El módulo se compone de dos archivos principales: `conftest.py` y `pytest.ini`.

### `pytest.ini`

Este archivo contiene la configuración global de `pytest` y es crucial para definir el comportamiento del ejecutor de pruebas.

*   `DJANGO_SETTINGS_MODULE = config.settings_test`: Especifica el módulo de configuración de Django a utilizar durante la ejecución de las pruebas. Esto asegura que el entorno de pruebas se inicialice con las configuraciones adecuadas, como la base de datos de pruebas, las aplicaciones instaladas y otras configuraciones específicas para el testing.
*   `python_files = tests.py test_*.py *_tests.py`: Define los patrones de nombres de archivos que `pytest` debe considerar como archivos de prueba. Esto permite una flexibilidad en la organización de los tests, detectando archivos como `tests.py`, `test_something.py` o `module_tests.py`.
*   `testpaths`: Esta sección lista los directorios donde `pytest` buscará los tests.
    *   `shopify_content/tests`: Incluye las pruebas relacionadas con la gestión de contenido de Shopify.
    *   `metaobjects/shopify_metaobjects/tests`: Contiene las pruebas para la integración de metaobjetos de Shopify.
    *   `api/tests`: Abarca las pruebas para la capa de la API del sistema.

### `conftest.py`

Este archivo permite definir ganchos (hooks) y fixtures para `pytest` que pueden ser compartidos entre múltiples archivos de prueba, centralizando la lógica de configuración y preparación del entorno de pruebas.

*   `pytest_configure()`: Este es un hook de `pytest` que se ejecuta temprano en el proceso de recolección de tests.
    *   `os.environ.setdefault('NINJA_SKIP_REGISTRY', 'true')`: Establece la variable de entorno `NINJA_SKIP_REGISTRY` a `true`. Esta configuración es probable que afecte el comportamiento de un registro específico durante las pruebas, posiblemente para evitar interacciones externas o para habilitar un modo de prueba simulado.

## Relación con el Sistema General

Este módulo es una parte integral de la estrategia de calidad y CI/CD del proyecto. Al centralizar la configuración de pruebas, garantiza que todas las suites de pruebas se ejecuten en un entorno controlado y consistente.

*   **Integración Continua (CI)**: La configuración definida aquí es utilizada por los flujos de trabajo de CI (ver [Integración CI/CD](Build,_CI___Configuration_integracion_ci_cd.md)) para ejecutar las pruebas automáticamente tras cada cambio de código, asegurando que las nuevas funcionalidades o modificaciones no introduzcan regresiones.
*   **Gestión de Dependencias**: Aunque este módulo no gestiona directamente las dependencias, la ejecución de las pruebas se basa en las dependencias definidas en el módulo de [Gestión de Dependencias](Build,_CI___Configuration_gestion_dependencias.md).
*   **Módulos de Pruebas**: Los `testpaths` en `pytest.ini` señalan a los directorios de pruebas de otros módulos, como:
    *   [Shopify Content Management](../Wagtail_Content_Management___API/Shopify_Content_Management.md)
    *   [Shopify Metaobjects Integration](../Application_Core___Shopify_Integration_Platform/Shopify_Metaobjects_Integration.md)
    *   [Shopify Content API](../Wagtail_Content_Management___API/Shopify_Content_API.md)

## Diagrama de Flujo de Configuración de Pruebas

El siguiente diagrama ilustra cómo `pytest` interactúa con los archivos de configuración de pruebas.

```mermaid
graph TD
    A[Inicio Ejecución de Pytest] --> B(Carga pytest.ini)
    B --> C{Configuración de Entorno}
    C --> D[DJANGO_SETTINGS_MODULE = config.settings_test]
    C --> E[python_files = tests.py, test_*.py, *_tests.py]
    C --> F[testpaths = shopify_content/tests, metaobjects/shopify_metaobjects/tests, api/tests]
    F --> G(Descubre y Carga conftest.py)
    G --> H{Ejecuta pytest_configure()}
    H --> I[Configura NINJA_SKIP_REGISTRY]
    I --> J(Ejecuta Pruebas Descubiertas)
    J --> K[Genera Reporte de Pruebas]
```

# Configuración del Proyecto

Este submódulo se encarga de la configuración general del proyecto, incluyendo los archivos que definen el comportamiento de CodeWiki, las configuraciones web de Shopify y el bloqueo de habilidades (skills).

## Componentes Clave

### `.codewiki-refresh.json`

Este archivo de configuración (`.codewiki-refresh.json`) especifica cómo se deben generar y organizar los documentos de CodeWiki. Define el idioma de la documentación (`lang`), los patrones de exclusión de archivos (`exclude`) y una lista de trabajos (`jobs`) para la generación de diferentes tipos de documentación (arquitectura, guía de usuario, desarrollador, API) con sus respectivas rutas de salida. Este archivo es crucial para la automatización de la documentación del proyecto.

```json
{
  "lang": "es",
  "exclude": "**/static/**,docs/**",
  "jobs": [
    { "type": "architecture", "out": "docs/developer/architecture" },
    { "type": "user-guide", "out": "docs/guides" },
    { "type": "developer", "out": "docs/developer" },
    { "type": "api", "out": "docs/developer/api" }
  ]
}
```

### `shopify.web.toml`

Este archivo (`shopify.web.toml`) contiene la configuración específica de la aplicación web Shopify. Define el nombre de la aplicación, los roles (frontend, backend) y la ruta para los webhooks de desinstalación de la aplicación. También especifica el comando `dev` para iniciar el servidor de desarrollo usando `daphne`.

```toml
name = "My Python App"
roles = ["frontend", "backend"]
webhooks_path = "/webhooks/app/uninstalled"

[commands]
dev = ".venv/bin/daphne -b 0.0.0.0 -p 8000 config.asgi:application"
```

### `skills-lock.json`

El archivo `skills-lock.json` es un manifiesto que bloquea las versiones y los hashes de las habilidades (skills) utilizadas en el proyecto. Cada habilidad se define con su fuente (repositorio de GitHub), tipo de fuente, ruta dentro del repositorio y un hash calculado para asegurar la integridad de la habilidad. Esto es fundamental para entornos de agentes en la nube que dependen de habilidades externas.

```json
{
  "version": 1,
  "skills": {
    "ask-matt": {
      "source": "aavendano/skills",
      "sourceType": "github",
      "skillPath": "skills/engineering/ask-matt/SKILL.md",
      "computedHash": "0cd14026efa0330083cbc7adf590976c162b60e02f696a8dcce96f0b4dab8a72"
    },
    "claude-handoff": {
      "source": "aavendano/skills",
      "sourceType": "github",
      "skillPath": "skills/in-progress/claude-handoff/SKILL.md",
      "computedHash": "f8c4754a25aa4e12601ce69db4388bb0d30ca526b225351180c5b0d2a4649a95"
    }
    // ... (otras habilidades)
  }
}
```

## Relación con otros componentes

Estos archivos de configuración son utilizados por varios procesos dentro del módulo de Construcción, CI y Configuración:

*   `.codewiki-refresh.json` es procesado por el sistema de documentación para generar la wiki del proyecto.
*   `shopify.web.toml` es leído por el servidor de la aplicación para configurar el entorno web y los webhooks.
*   `skills-lock.json` es utilizado por los entornos de agentes en la nube para cargar y verificar las habilidades necesarias.

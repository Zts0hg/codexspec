# Configuracion

## Ubicacion del Archivo de Configuracion

`.codexspec/config.yml`

## Esquema de Configuracion

```yaml
version: "1.0"

language:
  output: "en"      # Idioma de salida para documentos
  templates: "en"   # Idioma de plantillas (mantener como "en")

project:
  ai: "claude"      # Asistente AI
  created: "2025-02-15"
```

## Configuracion de Idioma

### `language.output`

El idioma para interacciones con Claude y documentos generados.

**Valores soportados:** Ver [Internacionalizacion](../user-guide/i18n.md#idiomas-soportados)

### `language.templates`

Idioma de las plantillas. Debe permanecer como `"en"` para compatibilidad.

## Configuracion del Proyecto

### `project.ai`

El asistente AI que se esta utilizando. Actualmente soporta:

- `claude` (predeterminado)

### `project.created`

Fecha cuando el proyecto fue inicializado.

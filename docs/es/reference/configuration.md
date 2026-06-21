# Configuracion

## Ubicacion del Archivo de Configuracion

`.codexspec/config.yml`

## Esquema de Configuracion

```yaml
version: "1.0"

language:
  output: "zh-CN"        # Idioma base; los tres siguientes caen a el, luego a "en"
  interaction: "zh-CN"   # Dialogo LLM + salida del CLI codexspec (opcional → por defecto output)
  document: "en"         # requirements/spec/plan/tasks generados (opcional → por defecto output)
  commit: "en"           # Mensajes de commit de git (opcional → por defecto output)
  templates: "en"        # Idioma de plantillas (mantener como "en")

project:
  ai: "claude"      # Asistente AI
  created: "2025-02-15"
```

## Configuracion de Idioma

CodexSpec divide el idioma en cuatro dimensiones configurables de forma independiente. `output` es la base; `interaction`, `document` y `commit` la sobrescriben y caen a ella (luego a `en`) cuando no estan establecidas. Esto te permite, por ejemplo, conversar con Claude en un idioma mientras mantienes los artefactos generados o los mensajes de commit en otro.

| Dimension | Clave | Establecer en init | Establecer despues | Controla | Cae a |
|-----------|-------|---------------------|--------------------|----------|--------|
| Output (base) | `output` | `--lang` | `config --set-lang` | base para las otras tres | `en` |
| Interaction | `interaction` | `--interaction-lang` | `config --set-interaction-lang` | dialogo LLM + salida del CLI | output → `en` |
| Document | `document` | `--document-lang` | `config --set-document-lang` | spec/plan/tasks generados | output → `en` |
| Commit | `commit` | `--commit-lang` | `config --set-commit-lang` | mensajes de commit de git | output → `en` |
| Templates | `templates` | — | — | fuente de plantillas de comandos (siempre `en`) | — |

**Valores soportados:** Ver [Internacionalizacion](../user-guide/i18n.md#supported-languages)

### `language.output`

El idioma base de salida. Las otras dimensiones caen a el cuando no se establecen de forma explicita.

### `language.interaction`

Idioma para la conversacion entre tu y el LLM, ademas de la salida del CLI `codexspec` en terminal. Opcional — por defecto `output`.

### `language.document`

Idioma para los archivos de artefactos generados (requirements/spec/plan/tasks). Opcional — por defecto `output`.

### `language.commit`

Idioma para los mensajes de commit de git. Opcional — por defecto `output`.

### `language.templates`

Idioma de las plantillas. Debe permanecer como `"en"` para compatibilidad.

## Configuracion del Proyecto

### `project.ai`

El asistente AI que se esta utilizando. Actualmente soporta:

- `claude` (predeterminado)

### `project.created`

Fecha cuando el proyecto fue inicializado.

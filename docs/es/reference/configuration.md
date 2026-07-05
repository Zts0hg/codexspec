# Configuración

## Ubicación del archivo de configuración

`.codexspec/config.yml`

## Esquema de configuración

```yaml
version: "1.0"

language:
  output: "zh-CN"        # Idioma base; los tres siguientes caen a él, luego a "en"
  interaction: "zh-CN"   # Diálogo LLM + salida del CLI codexspec (opcional → por defecto output)
  document: "en"         # requirements/spec/plan/tasks generados (opcional → por defecto output)
  commit: "en"           # Mensajes de commit de git (opcional → por defecto output)
  templates: "en"        # Mantener como "en"

project:
  ai: "claude"
  created: "2025-02-15"

workflow:
  auto_next: false       # Avance automático entre etapas del flujo de trabajo (opt-in)
```

## Ajustes de idioma

CodexSpec divide el idioma en cuatro dimensiones configurables de forma independiente. `output` es la base; `interaction`, `document` y `commit` la sobrescriben y, si no están establecidas, caen a ella (y luego a `en`). Esto te permite, por ejemplo, conversar con Claude en un idioma mientras mantienes los artefactos generados o los mensajes de commit en otro.

| Dimensión | Clave | En init | Después | Controla | Cae a |
|-----------|-----|-------------|-----------|----------|---------------|
| Output (base) | `output` | `--lang` | `config --set-lang` | base de las otras tres | `en` |
| Interaction | `interaction` | `--interaction-lang` | `config --set-interaction-lang` | diálogo LLM + salida del CLI | output → `en` |
| Document | `document` | `--document-lang` | `config --set-document-lang` | spec/plan/tasks generados | output → `en` |
| Commit | `commit` | `--commit-lang` | `config --set-commit-lang` | mensajes de commit de git | output → `en` |
| Templates | `templates` | — | — | origen de las plantillas de comandos (siempre `en`) | — |

**Valores soportados:** consulta [Internacionalización](../user-guide/i18n.md#supported-languages)

### `language.output`

El idioma base de salida. Las demás dimensiones caen a él cuando no se establecen de forma explícita.

### `language.interaction`

Idioma de la conversación entre tú y el LLM, además de la salida en terminal de la CLI `codexspec`. Opcional: por defecto toma `output`.

### `language.document`

Idioma de los archivos de artefactos generados (requirements/spec/plan/tasks). Opcional: por defecto toma `output`.

### `language.commit`

Idioma de los mensajes de commit de git. Opcional: por defecto toma `output`.

### `language.templates`

Idioma de las plantillas. Debe permanecer como `"en"` por compatibilidad.

## Ajustes del proyecto

### `project.ai`

El asistente de IA en uso. Controla qué archivos de contexto para agentes deja `codexspec init`:

- `claude` (predeterminado): escribe `CLAUDE.md` (y `.claude/commands/`).
- `codex`: en su lugar escribe `AGENTS.md` y `.agents/skills/`.
- `both`: escribe todo lo anterior para que el proyecto quede listo tanto para Claude Code como para Codex CLI.

`CLAUDE.md` siempre se crea (de modo que el proyecto sigue siendo utilizable desde Claude Code); `AGENTS.md` y `.agents/skills/` se crean únicamente cuando `project.ai` es `codex` o `both`.

### `project.created`

Fecha en la que se inicializó el proyecto.

## Ajustes del flujo de trabajo

### `workflow.auto_next`

Controla si el pipeline de Requirements-First SDD **avanza automáticamente** a la siguiente etapa del flujo de trabajo una vez que la etapa actual pasa, en lugar de requerir que lances manualmente el siguiente comando.

- **Predeterminado:** `false` (opt-in). Únicamente el valor literal `true` habilita el avance automático.
- **Conmutar / establecer con:** `codexspec config --auto-next` (la flag a secas conmuta el valor actual; pasa `on`/`off` para fijarlo explícitamente).

**Cadena:**

```
specify → generate-spec → spec-to-plan → plan-to-tasks → implement-tasks
```

**Puerta de paso (pass gate):**

- `generate-spec`, `spec-to-plan`, `plan-to-tasks`: el bucle de revisión integrado en el comando debe reportar un Overall Status de `PASS` o `PASS_WITH_WARNINGS`.
- `specify`: no hay bucle de revisión, de modo que la puerta es tu confirmación explícita de que el descubrimiento de requisitos ha terminado (el resumen de la etapa **final**, no cada uno intermedio).
- `implement-tasks`: etapa terminal; nada se dispara automáticamente después.

Cuando el bucle de revisión reporta `NEEDS_REVISION` o `BLOCKED`, la cadena se detiene y el control regresa a ti. Antes de cada avance, el agente emite una línea de aviso (por ejemplo: `auto_next: review passed → invoking /codexspec:spec-to-plan`).

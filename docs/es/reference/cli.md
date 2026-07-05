# Referencia de la CLI

## Comandos

### `codexspec init`

Inicializa un nuevo proyecto CodexSpec.

```bash
codexspec init [PROJECT_NAME] [OPTIONS]
```

**Argumentos:**

| Argumento | Descripción |
|----------|-------------|
| `PROJECT_NAME` | Nombre del directorio del nuevo proyecto (usa `.` o `--here` para el directorio actual) |

**Opciones:**

| Opción | Corta | Descripción |
|--------|-------|-------------|
| `--here` | `-h` | Inicializar en el directorio actual |
| `--ai` | `-a` | Asistente de IA a usar: `claude`, `codex` o `both` (predeterminado: claude) |
| `--lang` | `-l` | Idioma base de output; interaction/document/commit caen a él (ej.: en, zh-CN, ja) |
| `--interaction-lang` | | Idioma de interacción (diálogo LLM + salida de la CLI `codexspec`); sobrescribe `--lang` |
| `--document-lang` | | Idioma de los documentos (requirements/spec/plan/tasks generados); sobrescribe `--lang` |
| `--commit-lang` | | Idioma de los mensajes de commit; sobrescribe `--lang` |
| `--force` | `-f` | Sobrescribe archivos existentes y autoconfirma los prompts; nunca regenera `config.yml` |
| `--no-git` | | Omitir la inicialización del repositorio git |
| `--debug` | `-d` | Habilita la salida de depuración |

`--lang` establece el idioma base de `output`; `--interaction-lang`, `--document-lang` y `--commit-lang` lo sobrescriben para su dimensión (cada uno cae a `output`, luego a `en`). Consulta [Internacionalización](../user-guide/i18n.md) para el modelo completo.

La primera inicialización en una TTY sin `--lang` (y sin las tres flags de dimensión) solicita un idioma base; en un entorno sin TTY (CI/scripts) el valor predeterminado es `en`, **totalmente no interactiva**. Volver a ejecutar `init` preserva cualquier clave de idioma que no hayas especificado; `--force` nunca regenera `config.yml`.

**Ejemplos:**

```bash
# Crear un proyecto nuevo
codexspec init my-project

# Inicializar en el directorio actual
codexspec init . --ai claude

# Uso puntual (sin instalación): inicializar para Codex CLI o ambos
uvx codexspec init . --ai codex
uvx codexspec init . --ai both

# Totalmente no interactivo: base zh-CN, mensajes de commit en inglés
codexspec init my-project --lang zh-CN --commit-lang en

# Establecer cada dimensión explícitamente (scriptable, sin prompts)
codexspec init my-project \
  --interaction-lang zh-CN --document-lang en --commit-lang en
```

---

### `codexspec check`

Comprueba las herramientas instaladas.

```bash
codexspec check
```

---

### `codexspec version`

Muestra información de versión.

```bash
codexspec version
```

---

### `codexspec config`

Ver o modificar la configuración del proyecto.

```bash
codexspec config [OPTIONS]
```

**Opciones:**

| Opción | Corta | Descripción |
|--------|-------|-------------|
| `--set-lang` | `-l` | Establece el idioma base de output |
| `--set-interaction-lang` | | Establece el idioma de interacción (diálogo LLM + salida de la CLI) |
| `--set-document-lang` | | Establece el idioma de los documentos (spec/plan/tasks generados) |
| `--set-commit-lang` | `-c` | Establece el idioma de los mensajes de commit |
| `--list-langs` | | Lista todos los idiomas soportados |
| `--auto-next` | | Conmuta/establece `workflow.auto_next` (la flag a secas conmuta; o pasa on/off) |

Cada `--set-*-lang` actualiza una [dimensión de idioma](../user-guide/i18n.md); cualquier dimensión que no establezcas cae a `output`, luego a `en`.

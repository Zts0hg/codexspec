# Referencia CLI

## Comandos

### `codexspec init`

Inicializar un nuevo proyecto CodexSpec.

```bash
codexspec init [NOMBRE_PROYECTO] [OPCIONES]
```

**Argumentos:**

| Argumento | Descripcion |
|----------|-------------|
| `NOMBRE_PROYECTO` | Nombre para tu nuevo directorio de proyecto (usa `.` o `--here` para el directorio actual) |

**Opciones:**

| Opcion | Corto | Descripcion |
|--------|-------|-------------|
| `--here` | `-h` | Inicializar en el directorio actual |
| `--ai` | `-a` | Asistente AI a usar (predeterminado: claude) |
| `--lang` | `-l` | Idioma base de salida; interaction/document/commit caen a el (ej., en, zh-CN, ja) |
| `--interaction-lang` | | Idioma de interaccion (dialogo LLM + salida del CLI `codexspec`); sobrescribe `--lang` |
| `--document-lang` | | Idioma de documentos (requirements/spec/plan/tasks generados); sobrescribe `--lang` |
| `--commit-lang` | | Idioma de mensajes de commit; sobrescribe `--lang` |
| `--force` | `-f` | Sobrescribir archivos existentes y autoconfirmar prompts; nunca regenera `config.yml` |
| `--no-git` | | Saltar inicializacion de git |
| `--debug` | `-d` | Habilitar salida de depuracion |

`--lang` establece el idioma base de `output`; `--interaction-lang`, `--document-lang` y `--commit-lang` lo sobrescriben para su dimension (cada uno cae a `output`, luego a `en`). Consulta [Internacionalizacion](../user-guide/i18n.md) para el modelo completo.

La primera inicializacion en una TTY sin `--lang` (y sin las tres flags de dimension) solicita un idioma base; en una no-TTY (CI/scripts) el valor predeterminado es `en` — **totalmente no interactiva**. Volver a ejecutar `init` preserva cualquier clave de idioma que no hayas especificado; `--force` nunca regenera `config.yml`.

**Ejemplos:**

```bash
# Crear nuevo proyecto
codexspec init my-project

# Inicializar en directorio actual
codexspec init . --ai claude

# Totalmente no interactivo: base zh-CN, mensajes de commit en ingles
codexspec init my-project --lang zh-CN --commit-lang en

# Establecer cada dimension explicitamente (scriptable, sin prompts)
codexspec init my-project \
  --interaction-lang zh-CN --document-lang en --commit-lang en
```

---

### `codexspec check`

Verificar herramientas instaladas.

```bash
codexspec check
```

---

### `codexspec version`

Mostrar informacion de version.

```bash
codexspec version
```

---

### `codexspec config`

Ver o modificar la configuracion del proyecto.

```bash
codexspec config [OPCIONES]
```

**Opciones:**

| Opcion | Corto | Descripcion |
|--------|-------|-------------|
| `--set-lang` | `-l` | Establecer el idioma base de salida |
| `--set-interaction-lang` | | Establecer el idioma de interaccion (dialogo LLM + salida del CLI) |
| `--set-document-lang` | | Establecer el idioma de documentos (spec/plan/tasks generados) |
| `--set-commit-lang` | `-c` | Establecer el idioma de mensajes de commit |
| `--list-langs` | | Listar todos los idiomas soportados |

Cada `--set-*-lang` actualiza una [dimension de idioma](../user-guide/i18n.md); cualquier dimension que no establezcas cae a `output`, luego a `en`.

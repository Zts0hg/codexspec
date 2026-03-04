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
| `NOMBRE_PROYECTO` | Nombre para tu nuevo directorio de proyecto |

**Opciones:**

| Opcion | Corto | Descripcion |
|--------|-------|-------------|
| `--here` | `-h` | Inicializar en el directorio actual |
| `--ai` | `-a` | Asistente AI a usar (predeterminado: claude) |
| `--lang` | `-l` | Idioma de salida (ej., en, es, ja) |
| `--force` | `-f` | Forzar sobrescritura de archivos existentes |
| `--no-git` | | Saltar inicializacion de git |
| `--debug` | `-d` | Habilitar salida de depuracion |

**Ejemplos:**

```bash
# Crear nuevo proyecto
codexspec init my-project

# Inicializar en directorio actual
codexspec init . --ai claude

# Con salida en espanol
codexspec init my-project --lang es
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
| `--set-lang` | `-l` | Establecer el idioma de salida |
| `--list-langs` | | Listar todos los idiomas soportados |

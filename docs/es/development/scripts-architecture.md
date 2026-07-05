# Arquitectura de scripts

Este documento detalla la lógica de flujo del código de los scripts en el proyecto CodexSpec y cómo se utilizan dentro de Claude Code.

## 1. Visión general de la arquitectura

CodexSpec es un toolkit de **Spec-Driven Development (SDD)** que adopta una arquitectura de tres capas: CLI + plantillas + scripts auxiliares:

```
┌─────────────────────────────────────────────────────────────────┐
│                        Capa de usuario (CLI)                    │
│  codexspec init | check | version | config                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Capa de interacción con Claude Code          │
│  /codexspec:specify | /codexspec:analyze | ...                  │
│  (.claude/commands/*.md)                                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Capa de scripts auxiliares                 │
│  .codexspec/scripts/*.sh (Bash) o *.ps1 (PowerShell)           │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Flujo de despliegue de los scripts

### Etapa 1: inicialización con `codexspec init`

En la función `init()` de `src/codexspec/__init__.py` (líneas 343-368), los scripts se copian automáticamente según el sistema operativo:

```python
# Copy helper scripts based on platform
scripts_source_dir = get_scripts_dir()
if scripts_source_dir.exists():
    if sys.platform == "win32":
        # Windows: copiar los scripts de PowerShell
        ps_scripts = scripts_source_dir / "powershell"
        for script_file in ps_scripts.glob("*.ps1"):
            dest_file = codexspec_dir / "scripts" / script_file.name
            dest_file.write_text(script_file.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        # macOS/Linux: copiar los scripts de Bash
        bash_scripts = scripts_source_dir / "bash"
        for script_file in bash_scripts.glob("*.sh"):
            dest_file = codexspec_dir / "scripts" / script_file.name
            dest_file.write_text(script_file.read_text(encoding="utf-8"), encoding="utf-8")
```

**Resultado**: según el sistema operativo, los scripts de `scripts/bash/` o `scripts/powershell/` se copian al directorio `.codexspec/scripts/` del proyecto.

### Mecanismo de resolución de rutas

La función `get_scripts_dir()` (líneas 71-90) cubre varios escenarios de instalación:

```python
def get_scripts_dir() -> Path:
    # Path 1: Wheel install - scripts packaged inside codexspec package
    installed_scripts = Path(__file__).parent / "scripts"
    if installed_scripts.exists():
        return installed_scripts

    # Path 2: Development/editable install - scripts in project root
    dev_scripts = Path(__file__).parent.parent.parent / "scripts"
    if dev_scripts.exists():
        return dev_scripts

    # Path 3: Fallback
    return installed_scripts
```

## 3. Cómo se invocan los scripts desde Claude Code

### Mecanismo central: declaración en el frontmatter YAML

Las plantillas declaran la dependencia de scripts mediante el frontmatter YAML:

```yaml
---
description: Descripción del comando
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---
```

### Sustitución de placeholders

Las plantillas usan el placeholder `{SCRIPT}`:

```markdown
### 1. Initialize Context

Run `{SCRIPT}` from repo root and parse JSON for:
- `FEATURE_DIR` - Feature directory path
- `AVAILABLE_DOCS` - Available documents list
```

### Flujo de invocación

1. El usuario escribe `/codexspec:analyze` en Claude Code
2. Claude lee la plantilla `.claude/commands/codexspec:analyze.md`
3. Según el sistema operativo, Claude sustituye `{SCRIPT}` por:
   - **macOS/Linux**: `.codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks`
   - **Windows**: `.codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks`
4. Claude ejecuta el script, parsea la salida JSON y continúa con los pasos siguientes

## 4. Detalle de los scripts

### 4.1 `check-prerequisites.sh/ps1`: script de comprobaciones previas

Es el script más importante: verifica el estado del entorno y devuelve información estructurada.

#### Funciones principales

- Verifica si te encuentras en una rama feature (formato: `2026-0613-1200ab-feature-name`)
- Detecta si existen los archivos necesarios (`plan.md`, `tasks.md`)
- Devuelve información de rutas en formato JSON

#### Opciones de parámetros

| Parámetro | Bash | PowerShell | Función |
|------|------|------------|------|
| Salida JSON | `--json` | `-Json` | Emite salida en formato JSON |
| Requerir tasks.md | `--require-tasks` | `-RequireTasks` | Verifica que exista tasks.md |
| Incluir tasks.md | `--include-tasks` | `-IncludeTasks` | Incluye tasks.md en AVAILABLE_DOCS |
| Solo rutas | `--paths-only` | `-PathsOnly` | Omite la validación y solo devuelve rutas |

#### Ejemplo de salida JSON

```json
{
  "FEATURE_DIR": "/path/to/.codexspec/specs/2026-0613-1200ab-my-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md", "tasks.md"]
}
```

### 4.2 `common.sh/ps1`: funciones utilitarias comunes

Proporciona utilidades comunes multiplataforma:

#### Funciones de la versión Bash

| Función | Función |
|------|------|
| `get_feature_id()` | Obtiene el feature ID desde la rama Git o variables de entorno |
| `get_specs_dir()` | Devuelve la ruta del directorio specs |
| `is_codexspec_project()` | Comprueba si estás en un proyecto CodexSpec |
| `require_codexspec_project()` | Garantiza que estás en un proyecto CodexSpec; si no, sale |
| `log_info/success/warning/error()` | Logs en color |
| `command_exists()` | Comprueba si un comando existe |

#### Funciones de la versión PowerShell

| Función | Función |
|------|------|
| `Get-RepoRoot` | Devuelve la raíz del repositorio Git |
| `Get-CurrentBranch` | Devuelve el nombre de la rama actual |
| `Test-HasGit` | Detecta si hay un repositorio Git |
| `Test-FeatureBranch` | Verifica si estás en una rama feature |
| `Get-FeaturePathsEnv` | Devuelve todas las rutas relacionadas con la feature |
| `Test-FileExists` | Comprueba si un archivo existe |
| `Test-DirHasFiles` | Comprueba si un directorio contiene archivos |

### 4.3 `create-new-feature.sh/ps1`: crear una nueva funcionalidad

#### Funcionalidad

- Genera automáticamente un feature ID con formato `YYYY-MMDD-HHMMxx`
- Crea el directorio de la feature y un `requirements.md` inicial
- Crea la rama Git correspondiente
- Exige que el short name, una vez saneado, contenga al menos una letra o dígito ASCII

#### Ejemplo de uso

```bash
./create-new-feature.sh -n "user authentication"
```

#### Contrato de nombrado de features

- Sequential `NNN-name` identifiers are not supported. Timestamp names are the
  only feature naming format.
- Legacy compatibility applies to artifacts: an existing `spec.md` may be used
  when `requirements.md` is absent. It does not enable alternate directory or
  branch naming formats.
- The full feature name identifies a workspace:
  `YYYY-MMDD-HHMMxx-short-name`. Independently created workspaces may share the
  timestamp ID when their short names differ.
- Short-ID lookup is a local convenience only. If more than one directory
  matches, resolution reports ambiguity instead of selecting or overwriting a
  workspace.

## 5. Comandos que usan scripts

Los cuatro comandos siguientes usan scripts:

| Comando | Parámetros de los scripts | Función |
|------|--------------|------|
| `/codexspec:clarify` | `--json --paths-only` | Obtiene rutas, sin validar archivos |
| `/codexspec:checklist` | `--json` | Verifica que exista plan.md |
| `/codexspec:analyze` | `--json --require-tasks --include-tasks` | Verifica plan.md + tasks.md |
| `/codexspec:tasks-to-issues` | `--json --require-tasks --include-tasks` | Verifica plan.md + tasks.md |

## 6. Diagrama completo del flujo de trabajo

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        Etapa de inicialización                           │
│                                                                          │
│  $ codexspec init my-project                                             │
│       │                                                                  │
│       ├── Crea la estructura de directorios .codexspec/                  │
│       ├── Copia scripts/*.sh → .codexspec/scripts/                      │
│       ├── Copia templates/commands/*.md → .claude/commands/             │
│       └── Crea constitution.md, config.yml, CLAUDE.md                   │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────┐
│                        Etapa de uso (Claude Code)                        │
│                                                                          │
│  Usuario: /codexspec:analyze                                             │
│       │                                                                  │
│       ├── Claude lee .claude/commands/codexspec:analyze.md              │
│       │                                                                  │
│       ├── Parsea la declaración scripts del frontmatter YAML             │
│       │   scripts:                                                       │
│       │     sh: .codexspec/scripts/check-prerequisites.sh --json ...    │
│       │                                                                  │
│       ├── Sustituye el placeholder {SCRIPT}                              │
│       │                                                                  │
│       ├── Ejecuta el script:                                             │
│       │   $ .codexspec/scripts/check-prerequisites.sh --json ...        │
│       │                                                                  │
│       ├── Procesa la salida JSON:                                        │
│       │   {"FEATURE_DIR": "...", "AVAILABLE_DOCS": [...]}               │
│       │                                                                  │
│       ├── Lee spec.md, plan.md, tasks.md                                │
│       │                                                                  │
│       └── Genera el informe de análisis                                  │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## 7. Destacados del diseño

### 7.1 Compatibilidad multiplataforma

Se mantienen versiones tanto en Bash como en PowerShell, y se selecciona automáticamente con `sys.platform`:

```python
if sys.platform == "win32":
    # Copiar los scripts de PowerShell
else:
    # Copiar los scripts de Bash
```

### 7.2 Configuración declarativa

La dependencia de scripts se declara en el frontmatter YAML, de forma clara y directa:

```yaml
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json
```

### 7.3 Salida JSON

Los scripts devuelven datos estructurados, fáciles de parsear por Claude:

```json
{
  "FEATURE_DIR": "/path/to/.codexspec/specs/2026-0613-1200ab-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md"]
}
```

### 7.4 Validación progresiva

Cada comando usa parámetros distintos y valida solo lo necesario:

| Etapa | Comando | Nivel de validación |
|------|------|----------|
| Antes de planificar | `/codexspec:clarify` | Solo rutas |
| Después de planificar | `/codexspec:checklist` | plan.md |
| Después de las tareas | `/codexspec:analyze` | plan.md + tasks.md |

### 7.5 Integración con Git

- Extrae automáticamente el feature ID a partir del nombre de la rama
- Soporta validación del nombre de rama (formato `^\d{3}-`)
- Soporta sobrescritura por variable de entorno (`CODEXSPEC_FEATURE`)

## 8. Rutas de código clave

| Archivo | Línea/posición | Función |
|------|-----------|------|
| `src/codexspec/__init__.py` | 343-368 | Lógica de copia de scripts |
| `src/codexspec/__init__.py` | 71-90 | Resolución de rutas en `get_scripts_dir()` |
| `scripts/bash/check-prerequisites.sh` | archivo completo | Script Bash principal de comprobaciones previas |
| `scripts/powershell/check-prerequisites.ps1` | 56-146 | Script PowerShell de comprobaciones previas |
| `scripts/bash/common.sh` | archivo completo | Funciones utilitarias comunes de Bash |
| `scripts/powershell/common.ps1` | archivo completo | Funciones utilitarias comunes de PowerShell |
| `templates/commands/*.md` | frontmatter YAML | Declaración de scripts |

## 9. Inventario de archivos de script

### Scripts Bash (`scripts/bash/`)

```
scripts/bash/
├── check-prerequisites.sh   # Script principal de comprobaciones previas
├── common.sh                # Funciones utilitarias comunes
└── create-new-feature.sh    # Crear nueva funcionalidad
```

### Scripts de PowerShell (`scripts/powershell/`)

```
scripts/powershell/
├── check-prerequisites.ps1  # Script principal de comprobaciones previas
├── common.ps1               # Funciones utilitarias comunes
└── create-new-feature.ps1   # Crear nueva funcionalidad
```

---

*Este documenta recoge la arquitectura completa y el flujo de uso de los scripts en el proyecto CodexSpec. Si se actualizan, modifica este documento en consecuencia.*

# Analisis de Arquitectura de Scripts

Este documento detalla el flujo logico de codigo de los scripts en el proyecto CodexSpec y como se utilizan en Claude Code.

## 1. Resumen de Arquitectura General

CodexSpec es un kit de herramientas **Spec-Driven Development (SDD)** que adopta una arquitectura de tres capas: CLI + plantillas + scripts auxiliares:

```
+-------------------------------------------------------------------------+
|                        Capa de Usuario (CLI)                             |
|  codexspec init | check | version | config                               |
+-------------------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------------------+
|                    Capa de Interaccion Claude Code                       |
|  /codexspec:specify | /codexspec:analyze | ...                           |
|  (.claude/commands/*.md)                                                 |
+-------------------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------------------+
|                      Capa de Scripts Auxiliares                          |
|  .codexspec/scripts/*.sh (Bash) o *.ps1 (PowerShell)                    |
+-------------------------------------------------------------------------+
```

## 2. Flujo de Despliegue de Scripts

### Fase 1: Inicializacion con `codexspec init`

En la funcion `init()` de `src/codexspec/__init__.py` (lineas 343-368), los scripts correspondientes se copian automaticamente segun el sistema operativo:

```python
# Copy helper scripts based on platform
scripts_source_dir = get_scripts_dir()
if scripts_source_dir.exists():
    if sys.platform == "win32":
        # Windows: copiar scripts PowerShell
        ps_scripts = scripts_source_dir / "powershell"
        for script_file in ps_scripts.glob("*.ps1"):
            dest_file = codexspec_dir / "scripts" / script_file.name
            dest_file.write_text(script_file.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        # macOS/Linux: copiar scripts Bash
        bash_scripts = scripts_source_dir / "bash"
        for script_file in bash_scripts.glob("*.sh"):
            dest_file = codexspec_dir / "scripts" / script_file.name
            dest_file.write_text(script_file.read_text(encoding="utf-8"), encoding="utf-8")
```

**Resultado**: Segun el sistema operativo, se copian los scripts de `scripts/bash/` o `scripts/powershell/` al directorio `.codexspec/scripts/` del proyecto.

### Mecanismo de Resolucion de Rutas

La funcion `get_scripts_dir()` (lineas 71-90) maneja multiples escenarios de instalacion:

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

## 3. Mecanismo de Invocacion de Scripts en Claude Code

### Mecanismo Principal: Declaracion en YAML Frontmatter

Los archivos de plantilla declaran dependencias de scripts mediante YAML frontmatter:

```yaml
---
description: Descripcion del comando
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---
```

### Reemplazo de Marcadores de Posicion

Usar el marcador de posicion `{SCRIPT}` en las plantillas:

```markdown
### 1. Initialize Context

Run `{SCRIPT}` from repo root and parse JSON for:
- `FEATURE_DIR` - Feature directory path
- `AVAILABLE_DOCS` - Available documents list
```

### Flujo de Invocacion

1. El usuario ingresa `/codexspec:analyze` en Claude Code
2. Claude lee la plantilla `.claude/commands/codexspec:analyze.md`
3. Segun el sistema operativo, Claude reemplaza `{SCRIPT}` con:
   - **macOS/Linux**: `.codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks`
   - **Windows**: `.codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks`
4. Claude ejecuta el script, analiza la salida JSON y continua con las operaciones siguientes

## 4. Detalles de Funciones de Scripts

### 4.1 `check-prerequisites.sh/ps1` - Script de Verificacion Previa

Este es el script mas importante, usado para verificar el estado del entorno y devolver informacion estructurada.

#### Funciones Principales

- Verificar si esta en una rama feature (formato: `001-feature-name`)
- Detectar si existen archivos requeridos (`plan.md`, `tasks.md`)
- Devolver informacion de rutas en formato JSON

#### Opciones de Parametros

| Parametro | Bash | PowerShell | Funcion |
|------|------|------------|------|
| Salida JSON | `--json` | `-Json` | Salida en formato JSON |
| Requerir tasks.md | `--require-tasks` | `-RequireTasks` | Verificar que tasks.md existe |
| Incluir tasks.md | `--include-tasks` | `-IncludeTasks` | Incluir tasks.md en AVAILABLE_DOCS |
| Solo rutas | `--paths-only` | `-PathsOnly` | Saltar verificacion, solo output de rutas |

#### Ejemplo de Salida JSON

```json
{
  "FEATURE_DIR": "/path/to/.codexspec/specs/001-my-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md", "tasks.md"]
}
```

### 4.2 `common.sh/ps1` - Funciones de Utilidad Generales

Proporciona funcionalidad general multiplataforma:

#### Funciones Version Bash

| Funcion | Funcion |
|------|------|
| `get_feature_id()` | Obtener feature ID desde rama Git o variable de entorno |
| `get_specs_dir()` | Obtener ruta del directorio specs |
| `is_codexspec_project()` | Verificar si esta en un proyecto CodexSpec |
| `require_codexspec_project()` | Asegurar que esta en un proyecto CodexSpec, sino salir |
| `log_info/success/warning/error()` | Salida de log con colores |
| `command_exists()` | Verificar si un comando existe |

#### Funciones Version PowerShell

| Funcion | Funcion |
|------|------|
| `Get-RepoRoot` | Obtener directorio raiz del repositorio Git |
| `Get-CurrentBranch` | Obtener nombre de la rama actual |
| `Test-HasGit` | Detectar si hay repositorio Git |
| `Test-FeatureBranch` | Verificar si esta en rama feature |
| `Get-FeaturePathsEnv` | Obtener todas las rutas relacionadas con feature |
| `Test-FileExists` | Verificar si un archivo existe |
| `Test-DirHasFiles` | Verificar si un directorio tiene archivos |

### 4.3 `create-new-feature.sh/ps1` - Crear Nueva Funcionalidad

#### Funciones

- Generar automaticamente ID de feature incremental (001, 002, ...)
- Crear directorio de feature y spec.md inicial
- Crear la rama Git correspondiente

#### Ejemplo de Uso

```bash
./create-new-feature.sh -n "user authentication" -i 001
```

## 5. Comandos que Usan Scripts

Los siguientes 4 comandos usan scripts:

| Comando | Parametros Scripts | Funcion |
|------|--------------|------|
| `/codexspec:clarify` | `--json --paths-only` | Obtener rutas, no verificar archivos |
| `/codexspec:checklist` | `--json` | Verificar que plan.md existe |
| `/codexspec:analyze` | `--json --require-tasks --include-tasks` | Verificar plan.md + tasks.md |
| `/codexspec:tasks-to-issues` | `--json --require-tasks --include-tasks` | Verificar plan.md + tasks.md |

## 6. Diagrama de Flujo de Trabajo Completo

```
+--------------------------------------------------------------------------+
|                        Fase de Inicializacion                             |
|                                                                          |
|  $ codexspec init my-project                                             |
|       |                                                                  |
|       |-- Crear estructura de directorios .codexspec/                    |
|       |-- Copiar scripts/*.sh -> .codexspec/scripts/                     |
|       |-- Copiar templates/commands/*.md -> .claude/commands/            |
|       |-- Crear constitution.md, config.yml, CLAUDE.md                   |
|                                                                          |
+--------------------------------------------------------------------------+
                                    |
                                    v
+--------------------------------------------------------------------------+
|                        Fase de Uso (Claude Code)                          |
|                                                                          |
|  Usuario: /codexspec:analyze                                             |
|       |                                                                  |
|       |-- Claude lee .claude/commands/codexspec:analyze.md              |
|       |                                                                  |
|       |-- Analiza declaracion de scripts en YAML frontmatter            |
|       |   scripts:                                                       |
|       |     sh: .codexspec/scripts/check-prerequisites.sh --json ...    |
|       |                                                                  |
|       |-- Reemplaza marcador de posicion {SCRIPT}                       |
|       |                                                                  |
|       |-- Ejecuta script:                                                |
|       |   $ .codexspec/scripts/check-prerequisites.sh --json ...        |
|       |                                                                  |
|       |-- Analiza salida JSON:                                          |
|       |   {"FEATURE_DIR": "...", "AVAILABLE_DOCS": [...]}               |
|       |                                                                  |
|       |-- Lee spec.md, plan.md, tasks.md                                |
|       |                                                                  |
|       |-- Genera reporte de analisis                                    |
|                                                                          |
+--------------------------------------------------------------------------+
```

## 7. Puntos Destacados de Diseno

### 7.1 Compatibilidad Multiplataforma

Mantiene versiones Bash y PowerShell simultaneamente, seleccion automatica via `sys.platform`:

```python
if sys.platform == "win32":
    # Copiar scripts PowerShell
else:
    # Copiar scripts Bash
```

### 7.2 Configuracion Declarativa

Declarar dependencias de scripts via YAML frontmatter, claro e intuitivo:

```yaml
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json
```

### 7.3 Salida JSON

Los scripts generan datos estructurados, faciles de analizar por Claude:

```json
{
  "FEATURE_DIR": "/path/to/.codexspec/specs/001-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md"]
}
```

### 7.4 Verificacion Progresiva

Diferentes comandos usan diferentes parametros, verificacion segun necesidad:

| Fase | Comando | Nivel de Verificacion |
|------|------|----------|
| Antes de planificar | `/codexspec:clarify` | Solo rutas |
| Despues de planificar | `/codexspec:checklist` | plan.md |
| Despues de tareas | `/codexspec:analyze` | plan.md + tasks.md |

### 7.5 Integracion con Git

- Extraccion automatica de feature ID desde nombre de rama
- Soporte para validacion de nomenclatura de ramas (formato `^\d{3}-`)
- Soporte para sobrescritura via variables de entorno (`SPECIFY_FEATURE` / `CODEXSPEC_FEATURE`)

## 8. Rutas de Codigo Clave

| Archivo | Linea/Posicion | Funcion |
|------|-----------|------|
| `src/codexspec/__init__.py` | 343-368 | Logica de copia de scripts |
| `src/codexspec/__init__.py` | 71-90 | `get_scripts_dir()` resolucion de rutas |
| `scripts/bash/check-prerequisites.sh` | Todo el archivo | Script principal de verificacion Bash |
| `scripts/powershell/check-prerequisites.ps1` | 56-146 | Script de verificacion PowerShell |
| `scripts/bash/common.sh` | Todo el archivo | Funciones de utilidad Bash |
| `scripts/powershell/common.ps1` | Todo el archivo | Funciones de utilidad PowerShell |
| `templates/commands/*.md` | YAML frontmatter | Declaracion de scripts |

## 9. Lista de Archivos de Scripts

### Scripts Bash (`scripts/bash/`)

```
scripts/bash/
+-- check-prerequisites.sh   # Script principal de verificacion
+-- common.sh                # Funciones de utilidad generales
+-- create-new-feature.sh    # Crear nueva funcionalidad
```

### Scripts PowerShell (`scripts/powershell/`)

```
scripts/powershell/
+-- check-prerequisites.ps1  # Script principal de verificacion
+-- common.ps1               # Funciones de utilidad generales
+-- create-new-feature.ps1   # Crear nueva funcionalidad
```

---

*Este documento registra la arquitectura completa y el flujo de uso de los scripts en el proyecto CodexSpec. Actualizar sincronizadamente si hay cambios.*

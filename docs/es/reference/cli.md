# Referencia de la CLI

<a id="cli-commands"></a>

## Comandos CLI

| Comando | Propósito |
|---------|---------|
| `codexspec init` | Inicializar o actualizar un proyecto para Claude, Codex o ambos |
| `codexspec check` | Comprobar las herramientas y dependencias instaladas |
| `codexspec version` | Mostrar la versión e información del sistema |
| `codexspec config` | Consultar o modificar la configuración del proyecto |
| `codexspec list-commands` | Mostrar los comandos de agente disponibles por categoría |
| `codexspec show-blueprint` | Mostrar el blueprint del worktree compartido sin modificarlo |

<a id="cli-installation"></a>

## Instalación de la CLI

```bash
uv tool install codexspec

# Or use pip
pip install codexspec

# Verify the CLI and inspect available commands
codexspec version
codexspec --help
codexspec list-commands
```

Para crear un proyecto, ejecuta `codexspec init my-project --ai claude`; para
inicializar el directorio actual, ejecuta `codexspec init . --ai codex`. Con
`--ai both` se instalan ambas integraciones. El asistente predeterminado es
`claude`: si quieres Codex o ambos, debes indicarlo explícitamente.

<details>
<summary>Otros métodos de instalación</summary>

<a id="one-time-initialization"></a>

### Inicialización puntual

```bash
uvx codexspec init my-project --ai claude
uvx codexspec init . --ai codex
```

La inicialización puntual instala los comandos del proyecto y el entorno de
ejecución independiente para commits. El enrutamiento de worktrees, los flujos
blueprint/auto-dev y la revisión manual del perfil siguen utilizando la CLI de
CodexSpec; asegúrate de que esté disponible si vas a utilizar esos flujos.

<a id="development-versions"></a>

### Versiones de desarrollo

```bash
uv tool install git+https://github.com/Zts0hg/codexspec.git
uv tool install git+https://github.com/Zts0hg/codexspec.git@main

# Replace <tag> with the version you want
uv tool install git+https://github.com/Zts0hg/codexspec.git@<tag>
```

</details>

<details>
<summary>Instalación en Windows</summary>

Utiliza PowerShell:

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
# Restart PowerShell, then:
uv tool install codexspec
codexspec version
```

La [Guía de resolución de problemas en Windows](../WINDOWS-TROUBLESHOOTING.md)
explica cómo resolver problemas de PATH y de instalación.

</details>

<a id="upgrade-and-refresh-a-project"></a>

## Actualizar CodexSpec y los archivos del proyecto

La actualización de la CLI y la de los comandos instalados en un proyecto se hacen por separado:

```bash
uv tool install codexspec --upgrade
# Or: pip install --upgrade codexspec

# In the project you want to refresh; select its desired integration(s)
codexspec init . --force --ai both
```

Utiliza `--ai claude` o `--ai codex` si solo necesitas una de las integraciones.
`--force` regenera los comandos y scripts distribuidos y actualiza los recursos
de revisión. También confirma automáticamente las solicitudes de migración,
actualización de comandos y cumplimiento de la constitución. Se conservan los
requisitos y los principios del proyecto. En los archivos de contexto se
actualizan las instrucciones gestionadas, pero se mantiene el cuerpo existente;
también se conservan las claves de configuración que no hayas establecido
explícitamente.

El comando de planificación es `design-to-plan`. Al actualizar la instalación
se elimina la antigua entrada `spec-to-plan`, sin conservarla como alias.

<details>
<summary>Opciones de inicialización de la CLI</summary>

| Opción | Significado |
|--------|---------|
| `PROJECT_NAME` | Nombre del nuevo directorio; utiliza `.` para el directorio actual |
| `--here`, `-h` | Inicializar el directorio actual |
| `--ai`, `-a` | `claude`, `codex` o `both`; valor predeterminado: `claude` |
| `--lang`, `-l` | Establecer el idioma base de salida |
| `--interaction-lang` | Establecer el idioma de interacción |
| `--document-lang` | Establecer el idioma de los documentos |
| `--commit-lang` | Establecer el idioma de los mensajes de commit |
| `--force`, `-f` | Regenerar los artefactos instalados y confirmar automáticamente las solicitudes de migración, actualización y cumplimiento; conservar el contexto creado para el proyecto y la configuración no relacionada |
| `--no-git` | Omitir la inicialización del repositorio de Git |
| `--debug`, `-d` | Mostrar información detallada de depuración |

</details>

<details>
<summary>Opciones de configuración de la CLI</summary>

| Opción | Significado |
|--------|---------|
| `--set-lang`, `-l` | Establecer el idioma base de salida |
| `--set-interaction-lang` | Establecer el idioma de interacción |
| `--set-document-lang` | Establecer el idioma de los documentos |
| `--set-commit-lang`, `-c` | Establecer el idioma de los mensajes de commit |
| `--list-langs` | Mostrar los códigos de idioma admitidos |
| `--auto-next` | Alternar o establecer el avance automático entre etapas |
| `--auto-distill` | Alternar o establecer la captura automática de conocimiento |
| `--auto-maintenance` | Alternar o establecer el mantenimiento incremental automático |
| `--worktrees` | Alternar o establecer el aislamiento por worktrees local a cada checkout |
| `--decided-by` | Establecer el modo de decisión de revisión en `reviewer` o `ask` |

</details>

## `codexspec show-blueprint`

Imprime el `.codexspec/blueprint.md` completo de la rama fija `codexspec/auto-dev` y
`worktree-for-codexspec-auto-dev` como contenido sin formato en la salida estándar. Si falta el repositorio, la rama, el worktree o el archivo, se informa por la salida
de error estándar y el comando termina con un código distinto de cero. El comando es de solo
lectura y no realiza fetch, merge, escrituras ni bloqueos.

```bash
codexspec show-blueprint
```

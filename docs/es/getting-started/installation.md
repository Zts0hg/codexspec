<a id="installation"></a>

# Instalación

<a id="install-with-the-codex-desktop-app"></a>

## Instalar desde la aplicación de escritorio de Codex

Desde la aplicación de escritorio puedes pedir a Codex que instale CodexSpec y configure tu proyecto directamente.

1. Añade un proyecto local en la aplicación de escritorio de Codex y selecciona la carpeta en la que quieras trabajar.
2. Abre un chat en ese proyecto y pega la instrucción que aparece a continuación.
3. Si la aplicación te pide permiso para descargar o instalar dependencias, aprueba la acción solicitada para continuar.

```text
Please install and initialize CodexSpec in the current project.
Project: https://github.com/Zts0hg/codexspec

Complete the setup directly instead of asking me to run terminal commands.

Check the environment. If uv or Python 3.11+ is missing, install the required
tools in my user directory using their official installation instructions.
Install the latest stable release of CodexSpec.

For a new setup, initialize the current project for Codex in English:
codexspec init . --ai codex --lang en

If CodexSpec is already configured, check its version and configuration before
updating. Preserve existing requirements, project principles, user files,
and configuration settings.

Verify that the CLI works and that AGENTS.md and the CodexSpec skill files
under .agents/skills/ are installed. Explain the result and how to start
describing my requirements in plain English. If the skills are not yet
available in this chat, tell me whether to start a new chat or restart the app.
```

Para recibir respuestas y documentos en chino, cambia `--lang en` por `--lang zh-CN` y pide a Codex que explique el resultado en chino.

Codex instala la misma CLI y las mismas habilidades del proyecto que se obtienen con la configuración manual descrita a continuación. Puedes empezar con una instrucción como `$codexspec:specify I want to build a todo application`. La [guía de habilidades de OpenAI](https://learn.chatgpt.com/docs/build-skills) explica cómo se detectan y actualizan las habilidades locales.

<a id="prerequisites"></a>

## Requisitos previos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recomendado) o pip
- El asistente que vayas a utilizar: Claude Code o Codex
- Git para desarrollar con worktrees y trabajar con Git

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

<a id="plugin-marketplace-installation"></a>

## Instalación desde el marketplace de plugins

En Claude Code, instala el plugin desde su marketplace:

```text
/plugin marketplace add Zts0hg/codexspec
/plugin install codexspec@codexspec-market
/codexspec:config
```

El plugin incluye comandos e instrucciones que se cargan al inicio de la
sesión, también al reanudarla, para analizar los cambios preparados para commit
y consultar los requisitos históricos. Instalar el plugin no inicializa el
proyecto. Utiliza `/codexspec:config` para crear o modificar los ajustes de
idioma, flujo de trabajo y revisión; si necesitas la estructura completa del
proyecto, inicialízalo mediante la CLI.

El entorno de ejecución incluido permite previsualizar commits directamente
y realizar commits autorizados en el directorio actual con Python 3.11+ y Git,
sin mantener instalada la CLI de CodexSpec. El enrutamiento de worktrees, los
flujos blueprint/auto-dev y la revisión manual del perfil siguen requiriendo
la CLI. El hook de inicio del plugin necesita Git en PATH y una versión de
Claude Code que admita `args` en los hooks de comandos (forma exec). Sus
instrucciones están dirigidas al agente; no intercepta los comandos Git que
se ejecutan manualmente.

Consulta [Instalación](installation.md) para conocer el procedimiento completo.

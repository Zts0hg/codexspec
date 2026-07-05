# Instalación

## Requisitos previos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recomendado) o pip

## Opción 1: Instalar con uv (recomendado)

La forma más sencilla de instalar CodexSpec es usar uv:

```bash
uv tool install codexspec
```

## Opción 2: Instalar con pip

Como alternativa, puedes usar pip:

```bash
pip install codexspec
```

## Opción 3: Uso puntual

Ejecútalo directamente sin instalar:

```bash
# Crear un proyecto nuevo
uvx codexspec init my-project

# Inicializar en un proyecto existente para Claude Code
cd your-existing-project
uvx codexspec init . --ai claude

# Inicializar para Codex CLI
uvx codexspec init . --ai codex

# Inicializar tanto para Claude Code como para Codex CLI (escribe .claude/ y .agents/)
uvx codexspec init . --ai both
```

## Opción 4: Instalar desde GitHub

Para obtener la última versión de desarrollo:

```bash
# Con uv
uv tool install git+https://github.com/Zts0hg/codexspec.git

# Con pip
pip install git+https://github.com/Zts0hg/codexspec.git

# Rama o etiqueta específica
uv tool install git+https://github.com/Zts0hg/codexspec.git@main
uv tool install git+https://github.com/Zts0hg/codexspec.git@v0.5.6
```

## Opción 5: Instalación desde el Plugin Marketplace (alternativa)

CodexSpec también está disponible como plugin de Claude Code. Este método es ideal si quieres usar los slash commands de CodexSpec directamente en Claude Code sin instalar la CLI. La CLI ofrece la experiencia completa de SDD Requirements-First; el plugin aporta el conjunto de slash commands sobre Claude Code.

### Pasos de instalación

En Claude Code:

```bash
# Añadir el marketplace
> /plugin marketplace add Zts0hg/codexspec

# Instalar el plugin
> /plugin install codexspec@codexspec-market
```

### Configuración de idioma para usuarios del plugin

Tras instalar vía el Plugin Marketplace, configura tu idioma preferido con el slash command `/codexspec:config` (el comando de la CLI `codexspec config` no está disponible sin la instalación de la CLI):

```bash
# Iniciar la configuración interactiva
> /codexspec:config

# O ver la configuración actual
> /codexspec:config --view
```

El comando de configuración te guía para elegir el idioma de salida (para los documentos generados) y el idioma de los mensajes de commit, y luego escribe `.codexspec/config.yml`. El soporte multilingüe usa la misma traducción dinámica con LLM que la CLI.

### Comparativa de métodos de instalación

| Método | Ideal para | Funciones |
|--------|----------|----------|
| **Instalación de la CLI** (`uv tool install` o `pip install`) | Flujo de desarrollo completo | Comandos de la CLI (`init`, `check`, `config`, `version`) + slash commands |
| **Plugin Marketplace** | Inicio rápido, proyectos existentes | Solo slash commands (usa `/codexspec:config` para configurar el idioma) |

**Nota**: El plugin usa el modo `strict: false` y reutiliza el soporte multilingüe existente mediante traducción dinámica con LLM.

## Verificar la instalación

```bash
codexspec --help
codexspec version
```

(Para instalaciones vía Plugin Marketplace, verifica ejecutando cualquier slash command, por ejemplo `/codexspec:config --view`, dentro de Claude Code.)

## Actualizar

```bash
# Con uv
uv tool install codexspec --upgrade

# Con pip
pip install --upgrade codexspec
```

(Las instalaciones del Plugin Marketplace se actualizan mediante el gestor de plugins de Claude Code.)

## Próximos pasos

[Inicio rápido](quick-start.md)

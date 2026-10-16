<a id="installation"></a>

# Instalação

<a id="install-with-the-codex-desktop-app"></a>

## Instalação pelo aplicativo desktop do Codex

Você pode pedir ao Codex para instalar o CodexSpec e configurar seu projeto
diretamente pelo aplicativo desktop.

1. Adicione um projeto local no aplicativo desktop do Codex e selecione a pasta em que deseja trabalhar.
2. Inicie uma conversa nesse projeto e cole a solicitação abaixo.
3. Se o aplicativo pedir permissão para baixar ou instalar dependências, aprove a ação solicitada para continuar.

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

Para respostas e documentos em chinês, substitua `--lang en` por `--lang zh-CN`
e peça ao Codex para explicar o resultado em chinês.

O Codex instala a mesma CLI e as mesmas skills de projeto usadas na configuração
manual abaixo. Depois, você pode começar com uma solicitação como
`$codexspec:specify I want to build a todo application`. O [guia de skills da OpenAI](https://learn.chatgpt.com/docs/build-skills)
explica como as skills locais são descobertas e atualizadas.

<a id="prerequisites"></a>

## Pré-requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recomendado) ou pip
- O assistente que você pretende usar: Claude Code ou Codex
- Git para o desenvolvimento com worktrees e os fluxos de trabalho Git

<a id="cli-installation"></a>

## Instalação da CLI

```bash
uv tool install codexspec

# Or use pip
pip install codexspec

# Verify the CLI and inspect available commands
codexspec version
codexspec --help
codexspec list-commands
```

Inicialize um novo projeto com `codexspec init my-project --ai claude` ou o
diretório atual com `codexspec init . --ai codex`. Use `--ai both` para as duas
integrações. O assistente padrão é `claude`; para usar Codex ou ambos, informe
essa escolha explicitamente.

<details>
<summary>Métodos alternativos de instalação</summary>

<a id="one-time-initialization"></a>

### Inicialização em uma única execução

```bash
uvx codexspec init my-project --ai claude
uvx codexspec init . --ai codex
```

A inicialização em uma única execução instala os comandos do projeto e o ambiente
independente de execução de commits. O roteamento de worktrees, blueprint/auto-dev
e a revisão manual do perfil continuam usando a CLI do CodexSpec. Deixe essa CLI
disponível para esses fluxos de trabalho.

<a id="development-versions"></a>

### Versões de desenvolvimento

```bash
uv tool install git+https://github.com/Zts0hg/codexspec.git
uv tool install git+https://github.com/Zts0hg/codexspec.git@main

# Replace <tag> with the version you want
uv tool install git+https://github.com/Zts0hg/codexspec.git@<tag>
```

</details>

<details>
<summary>Instalação no Windows</summary>

Use o PowerShell:

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
# Restart PowerShell, then:
uv tool install codexspec
codexspec version
```

Consulte o [Guia de solução de problemas no Windows](../WINDOWS-TROUBLESHOOTING.md)
para resolver problemas com PATH e instalação.

</details>

<a id="upgrade-and-refresh-a-project"></a>

## Atualizar a CLI e os comandos de um projeto

Atualizar a CLI e atualizar os comandos instalados em um projeto são duas etapas distintas:

```bash
uv tool install codexspec --upgrade
# Or: pip install --upgrade codexspec

# In the project you want to refresh; select its desired integration(s)
codexspec init . --force --ai both
```

Use `--ai claude` ou `--ai codex` se quiser apenas essa integração. `--force`
regenera os comandos e scripts distribuídos e atualiza os recursos de revisão.
Também confirma automaticamente as solicitações de migração, atualização de
comandos e conformidade com a Constituição do Projeto. Os requisitos e princípios
existentes são mantidos. Nos arquivos de contexto existentes, as orientações
gerenciadas são atualizadas e o restante do conteúdo é preservado. As chaves de
configuração que você não definir explicitamente também são mantidas.

O comando de planejamento é `design-to-plan`. As atualizações da instalação
removem a entrada antiga `spec-to-plan`, sem manter um alias.

<a id="plugin-marketplace-installation"></a>

## Instalação pelo marketplace de plugins

Para Claude Code, instale o plugin pelo marketplace:

```text
/plugin marketplace add Zts0hg/codexspec
/plugin install codexspec@codexspec-market
/codexspec:config
```

O plugin fornece comandos e orientações no início da sessão para a análise das
alterações na área de preparação e a consulta aos requisitos anteriores,
inclusive em sessões retomadas. A instalação do plugin não inicializa um projeto.
Use `/codexspec:config` para criar ou alterar configurações de idioma, fluxo de
trabalho e revisão. Quando precisar da estrutura completa do projeto, use a
inicialização pela CLI.

A prévia direta de commits e os commits autorizados no diretório de trabalho
atual podem usar o ambiente de execução incluído, com Python 3.11+ e Git, sem uma
CLI do CodexSpec instalada de forma permanente. O roteamento de worktrees,
blueprint/auto-dev e a revisão manual do perfil continuam exigindo a CLI. O hook
de inicialização do plugin requer Git no PATH e uma versão do Claude Code que
aceite `args` em hooks de comando (forma exec). As orientações são destinadas
ao agente; o hook não intercepta comandos Git executados manualmente.

Consulte [Instalação](installation.md) para ver os detalhes da configuração.

# Instalação

## Pré-requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recomendado) ou pip

## Opção 1: Instalar com uv (Recomendado)

A maneira mais fácil de instalar o CodexSpec é usando uv:

```bash
uv tool install codexspec
```

## Opção 2: Instalar com pip

Como alternativa, você pode usar pip:

```bash
pip install codexspec
```

## Opção 3: Uso único

Execute diretamente, sem instalar:

```bash
# Criar um novo projeto
uvx codexspec init my-project

# Inicializar em um projeto existente para o Claude Code
cd your-existing-project
uvx codexspec init . --ai claude

# Inicializar para o Codex CLI
uvx codexspec init . --ai codex

# Inicializar tanto para Claude Code quanto para Codex CLI (cria .claude/ e .agents/)
uvx codexspec init . --ai both
```

## Opção 4: Instalar a partir do GitHub

Para a versão de desenvolvimento mais recente:

```bash
# Usando uv
uv tool install git+https://github.com/Zts0hg/codexspec.git

# Usando pip
pip install git+https://github.com/Zts0hg/codexspec.git

# Branch ou tag específica
uv tool install git+https://github.com/Zts0hg/codexspec.git@main
uv tool install git+https://github.com/Zts0hg/codexspec.git@v0.5.6
```

## Opção 5: Instalação pelo Plugin Marketplace (alternativa)

O CodexSpec também está disponível como um plugin do Claude Code. Esse método é ideal se você quer usar os slash commands do CodexSpec diretamente no Claude Code sem instalar a CLI. A CLI é a experiência completa de Requirements-First SDD; o plugin traz o conjunto de slash commands sobre o Claude Code.

### Passos de instalação

No Claude Code:

```bash
# Adicionar o marketplace
> /plugin marketplace add Zts0hg/codexspec

# Instalar o plugin
> /plugin install codexspec@codexspec-market
```

### Configuração de idioma para usuários do plugin

Depois de instalar via Plugin Marketplace, configure o idioma preferido usando o slash command `/codexspec:config` (o comando da CLI `codexspec config` não está disponível sem a instalação da CLI):

```bash
# Iniciar configuração interativa
> /codexspec:config

# Ou visualizar a configuração atual
> /codexspec:config --view
```

O comando de configuração orienta você na seleção do idioma de saída (para documentos gerados) e do idioma das mensagens de commit, e em seguida grava o `.codexspec/config.yml`. O suporte a múltiplos idiomas usa a mesma tradução dinâmica por LLM que a CLI.

### Comparação dos métodos de instalação

| Método | Ideal para | Recursos |
|--------|------------|----------|
| **Instalação da CLI** (`uv tool install` ou `pip install`) | Fluxo de desenvolvimento completo | Comandos da CLI (`init`, `check`, `config`, `version`) + slash commands |
| **Plugin Marketplace** | Início rápido, projetos existentes | Apenas slash commands (use `/codexspec:config` para configurar o idioma) |

**Observação**: o plugin usa o modo `strict: false` e reaproveita o suporte existente a múltiplos idiomas via tradução dinâmica por LLM.

## Verificar a instalação

```bash
codexspec --help
codexspec version
```

(Para instalações via Plugin Marketplace, verifique executando qualquer slash command, como `/codexspec:config --view`, dentro do Claude Code.)

## Atualização

```bash
# Usando uv
uv tool install codexspec --upgrade

# Usando pip
pip install --upgrade codexspec
```

(Instalações via Plugin Marketplace são atualizadas pelo gerenciador de plugins do Claude Code.)

## Próximos passos

[Início rápido](quick-start.md)

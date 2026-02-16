# CodexSpec

[English](README.md) | [中文](README.zh-CN.md) | [日本語](README.ja.md) | [Español](README.es.md) | **Português** | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md)

[![PyPI version](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Um toolkit de Desenvolvimento Orientado a Especificações (SDD) para Claude Code**

CodexSpec é um toolkit que ajuda você a construir software de alta qualidade usando uma abordagem estruturada e orientada a especificações. Ele inverte o script do desenvolvimento tradicional, transformando especificações em artefatos executáveis que guiam diretamente a implementação.

## Funcionalidades

- **Fluxo de trabalho estruturado**: Comandos claros para cada fase do desenvolvimento
- **Integração com Claude Code**: Comandos slash nativos para Claude Code
- **Baseado em constituição**: Princípios do projeto guiam todas as decisões
- **Especificações primeiro**: Defina o quê e por quê antes do como
- **Orientado a planos**: Escolhas técnicas vêm depois dos requisitos
- **Orientado a tarefas**: Divida a implementação em tarefas acionáveis
- **Garantia de qualidade**: Comandos integrados de revisão, análise e checklists
- **Internacionalização (i18n)**: Suporte multilíngue via tradução dinâmica LLM
- **Multiplataforma**: Suporte para scripts Bash e PowerShell
- **Extensível**: Arquitetura de plugins para comandos personalizados

## Instalação

### Pré-requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recomendado) ou pip

### Opção 1: Instalar com uv (Recomendado)

A forma mais fácil de instalar o CodexSpec é usando uv:

```bash
uv tool install codexspec
```

### Opção 2: Instalar com pip

Alternativamente, você pode usar pip:

```bash
pip install codexspec
```

### Opção 3: Uso único

Execute diretamente sem instalar:

```bash
# Criar um novo projeto
uvx codexspec init my-project

# Inicializar em um projeto existente
cd your-existing-project
uvx codexspec init . --ai claude
```

### Opção 4: Instalar do GitHub (Versão de Desenvolvimento)

Para a versão de desenvolvimento mais recente ou uma branch específica:

```bash
# Usando uv
uv tool install git+https://github.com/Zts0hg/codexspec.git

# Usando pip
pip install git+https://github.com/Zts0hg/codexspec.git

# Branch ou tag específica
uv tool install git+https://github.com/Zts0hg/codexspec.git@main
uv tool install git+https://github.com/Zts0hg/codexspec.git@v0.2.0
```

## Início Rápido

Após a instalação, você pode usar o CLI:

```bash
# Criar novo projeto (saída em português)
codexspec init my-project --lang pt

# Inicializar em projeto existente
codexspec init . --ai claude

# Verificar ferramentas instaladas
codexspec check

# Ver versão
codexspec version
```

Para atualizar para a versão mais recente:

```bash
# Usando uv
uv tool install codexspec --upgrade

# Usando pip
pip install --upgrade codexspec
```

## Uso

### 1. Inicializar um Projeto

Após a [instalação](#instalação), crie ou inicialize seu projeto:

```bash
codexspec init my-awesome-project --lang pt
```

### 2. Estabelecer Princípios do Projeto

Inicie o Claude Code no diretório do projeto:

```bash
cd my-awesome-project
claude
```

Use o comando `/codexspec.constitution` para criar os princípios de governança do projeto:

```
/codexspec.constitution Criar princípios focados em qualidade de código, padrões de teste e arquitetura limpa
```

### 3. Clarificar Requisitos

Use `/codexspec.specify` para **explorar e clarificar** seus requisitos através de Q&A interativo:

```
/codexspec.specify Quero construir uma aplicação de gerenciamento de tarefas
```

Este comando irá:
- Fazer perguntas de clarificação para entender sua ideia
- Explorar casos de borda que você pode não ter considerado
- Co-criar requisitos de alta qualidade através de diálogo
- **NÃO** gerar arquivos automaticamente - você mantém o controle

### 4. Gerar Documento de Especificação

Uma vez que os requisitos estão clarificados, use `/codexspec.generate-spec` para criar o documento `spec.md`:

```
/codexspec.generate-spec
```

Este comando atua como um "compilador de requisitos" que transforma seus requisitos clarificados em um documento de especificação estruturado.

### 5. Criar um Plano Técnico

Use `/codexspec.spec-to-plan` para definir como implementar:

```
/codexspec.spec-to-plan Usar Python com FastAPI para o backend, PostgreSQL para o banco de dados e React para o frontend
```

### 6. Gerar Tarefas

Use `/codexspec.plan-to-tasks` para decompor o plano:

```
/codexspec.plan-to-tasks
```

### 7. Analisar (Opcional mas Recomendado)

Use `/codexspec.analyze` para verificação de consistência entre artefatos:

```
/codexspec.analyze
```

### 8. Implementar

Use `/codexspec.implement-tasks` para executar a implementação:

```
/codexspec.implement-tasks
```

## Comandos Disponíveis

### Comandos CLI

| Comando | Descrição |
|---------|-----------|
| `codexspec init` | Inicializar um novo projeto CodexSpec |
| `codexspec check` | Verificar ferramentas instaladas |
| `codexspec version` | Exibir informação de versão |
| `codexspec config` | Ver ou modificar configuração do projeto |

### Opções do `codexspec init`

| Opção | Descrição |
|-------|-----------|
| `PROJECT_NAME` | Nome do novo diretório do projeto |
| `--here`, `-h` | Inicializar no diretório atual |
| `--ai`, `-a` | Assistente de IA a usar (padrão: claude) |
| `--lang`, `-l` | Idioma de saída (ex: en, pt, zh-CN, ja) |
| `--force`, `-f` | Forçar sobrescrita de arquivos existentes |
| `--no-git` | Pular inicialização do git |
| `--debug`, `-d` | Habilitar saída de debug |

### Opções do `codexspec config`

| Opção | Descrição |
|-------|-----------|
| `--set-lang`, `-l` | Definir o idioma de saída |
| `--list-langs` | Listar todos os idiomas suportados |

### Comandos Slash

Após a inicialização, estes comandos slash estão disponíveis no Claude Code:

#### Comandos Principais

| Comando | Descrição |
|---------|-----------|
| `/codexspec.constitution` | Criar ou atualizar princípios de governança do projeto |
| `/codexspec.specify` | **Clarificar** requisitos através de Q&A interativo (sem geração de arquivo) |
| `/codexspec.generate-spec` | **Gerar** documento `spec.md` após clarificação de requisitos |
| `/codexspec.spec-to-plan` | Converter especificação em plano técnico |
| `/codexspec.plan-to-tasks` | Decompor plano em tarefas acionáveis |
| `/codexspec.implement-tasks` | Executar tarefas conforme decomposição |

#### Comandos de Revisão

| Comando | Descrição |
|---------|-----------|
| `/codexspec.review-spec` | Revisar completude da especificação |
| `/codexspec.review-plan` | Revisar viabilidade do plano técnico |
| `/codexspec.review-tasks` | Revisar completude da decomposição de tarefas |

#### Comandos Avançados

| Comando | Descrição |
|---------|-----------|
| `/codexspec.clarify` | Escanear spec.md existente por ambiguidades e atualizar com clarificações |
| `/codexspec.analyze` | Análise de consistência entre artefatos |
| `/codexspec.checklist` | Gerar checklists de qualidade para requisitos |
| `/codexspec.tasks-to-issues` | Converter tarefas em GitHub issues |

## Visão Geral do Fluxo de Trabalho

```
┌──────────────────────────────────────────────────────────────┐
│                    Fluxo de Trabalho CodexSpec               │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Constitution  ──►  Definir princípios do projeto         │
│         │                                                    │
│         ▼                                                    │
│  2. Specify  ───────►  Q&A interativo para clarificar        │
│         │             requisitos (sem criar arquivo)         │
│         │                                                    │
│         ▼                                                    │
│  3. Generate Spec  ─►  Criar documento spec.md               │
│         │             (usuário chama explicitamente)         │
│         │                                                    │
│         ▼                                                    │
│  4. Review Spec  ───►  Validar especificação                 │
│         │                                                    │
│         ▼                                                    │
│  5. Clarify  ───────►  Resolver ambiguidades (opcional)      │
│         │                                                    │
│         ▼                                                    │
│  6. Spec to Plan  ──►  Criar plano técnico                   │
│         │                                                    │
│         ▼                                                    │
│  7. Review Plan  ───►  Validar plano técnico                 │
│         │                                                    │
│         ▼                                                    │
│  8. Plan to Tasks  ─►  Gerar decomposição de tarefas         │
│         │                                                    │
│         ▼                                                    │
│  9. Analyze  ───────►  Consistência entre artefatos (opc.)   │
│         │                                                    │
│         ▼                                                    │
│  10. Review Tasks  ─►  Validar decomposição de tarefas       │
│         │                                                    │
│         ▼                                                    │
│  11. Implement  ─────►  Executar implementação               │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Conceito Chave: Fluxo de Trabalho de Clarificação de Requisitos

O CodexSpec fornece **dois comandos de clarificação distintos** para diferentes estágios do fluxo de trabalho:

#### specify vs clarify: Quando Usar Qual?

| Aspecto | `/codexspec.specify` | `/codexspec.clarify` |
|---------|----------------------|----------------------|
| **Propósito** | Exploração inicial de requisitos | Refinamento iterativo de specs existentes |
| **Quando Usar** | Começar com nova ideia, sem spec.md | spec.md existe, precisa preencher lacunas |
| **Entrada** | Sua ideia ou requisito inicial | Arquivo spec.md existente |
| **Saída** | Nenhuma (apenas diálogo) | Atualiza spec.md com clarificações |
| **Método** | Q&A aberto | Escaneamento de ambiguidade estruturado (6 categorias) |
| **Limite de Perguntas** | Ilimitado | Máximo 5 perguntas |
| **Uso Típico** | "Quero construir um app de tarefas" | "A spec carece de detalhes de tratamento de erros" |

#### Especificação em Duas Fases

Antes de gerar qualquer documentação:

| Fase | Comando | Propósito | Saída |
|------|---------|-----------|-------|
| **Exploração** | `/codexspec.specify` | Q&A interativo para explorar e refinar requisitos | Nenhuma (apenas diálogo) |
| **Geração** | `/codexspec.generate-spec` | Compilar requisitos clarificados em documento estruturado | `spec.md` |

#### Clarificação Iterativa

Após criar spec.md:

```
spec.md ──► /codexspec.clarify ──► spec.md atualizado (com seção Clarifications)
                │
                └── Escaneia ambiguidades em 6 categorias:
                    • Escopo funcional e comportamento
                    • Domínio e modelo de dados
                    • Interação e fluxo UX
                    • Atributos de qualidade não funcionais
                    • Casos de borda e tratamento de falhas
                    • Resolução de conflitos
```

#### Benefícios deste Design

- **Colaboração humano-AI**: Você participa ativamente da descoberta de requisitos
- **Controle explícito**: Arquivos só são criados quando você decide
- **Foco em qualidade**: Requisitos são completamente explorados antes da documentação
- **Refinamento iterativo**: Specs podem ser melhoradas incrementalmente

## Estrutura do Projeto

Após a inicialização, seu projeto terá esta estrutura:

```
my-project/
├── .codexspec/
│   ├── memory/
│   │   └── constitution.md    # Princípios de governança do projeto
│   ├── specs/
│   │   └── {feature-id}/
│   │       ├── spec.md        # Especificação de funcionalidade
│   │       ├── plan.md        # Plano técnico
│   │       ├── tasks.md       # Decomposição de tarefas
│   │       └── checklists/    # Checklists de qualidade
│   ├── templates/             # Templates personalizados
│   ├── scripts/               # Scripts auxiliares
│   │   ├── bash/              # Scripts Bash
│   │   └── powershell/        # Scripts PowerShell
│   └── extensions/            # Extensões personalizadas
├── .claude/
│   └── commands/              # Comandos slash para Claude Code
└── CLAUDE.md                  # Contexto para Claude Code
```

## Internacionalização (i18n)

CodexSpec suporta múltiplos idiomas através de **tradução dinâmica LLM**. Em vez de manter templates traduzidos, deixamos o Claude traduzir o conteúdo em tempo real com base na sua preferência de idioma.

### Definindo o Idioma

**Durante a inicialização:**
```bash
# Criar um projeto com saída em chinês
codexspec init my-project --lang zh-CN

# Criar um projeto com saída em japonês
codexspec init my-project --lang ja
```

**Após a inicialização:**
```bash
# Ver configuração atual
codexspec config

# Alterar configuração de idioma
codexspec config --set-lang zh-CN

# Listar idiomas suportados
codexspec config --list-langs
```

### Arquivo de Configuração

O arquivo `.codexspec/config.yml` armazena as configurações de idioma:

```yaml
version: "1.0"

language:
  # Idioma de saída para interações Claude e documentos gerados
  output: "zh-CN"

  # Idioma dos templates - mantenha como "en" para compatibilidade
  templates: "en"

project:
  ai: "claude"
  created: "2026-02-15"
```

### Idiomas Suportados

| Código | Idioma |
|--------|--------|
| `en` | English (padrão) |
| `zh-CN` | 中文（简体） |
| `zh-TW` | 中文（繁體） |
| `ja` | 日本語 |
| `ko` | 한국어 |
| `es` | Español |
| `fr` | Français |
| `de` | Deutsch |
| `pt` | Português |
| `ru` | Русский |
| `it` | Italiano |
| `ar` | العربية |
| `hi` | हिन्दी |

### Como Funciona

1. **Templates apenas em inglês**: Todos os templates de comando permanecem em inglês
2. **Configuração de idioma**: O projeto especifica o idioma de saída preferido
3. **Tradução dinâmica**: Claude lê instruções em inglês, produz saída no idioma alvo
4. **Consciente do contexto**: Termos técnicos (JWT, OAuth, etc.) permanecem em inglês quando apropriado

### Benefícios

- **Zero manutenção de tradução**: Não há necessidade de manter múltiplas versões de templates
- **Sempre atualizado**: Atualizações de templates beneficiam automaticamente todos os idiomas
- **Tradução consciente do contexto**: Claude fornece traduções naturais e apropriadas ao contexto
- **Idiomas ilimitados**: Qualquer idioma suportado pelo Claude funciona imediatamente

## Sistema de Extensões

CodexSpec suporta uma arquitetura de plugins para adicionar comandos personalizados:

### Estrutura de Extensão

```
my-extension/
├── extension.yml          # Manifesto da extensão
├── commands/              # Comandos slash personalizados
│   └── command.md
└── README.md
```

### Criando Extensões

1. Copie o template de `extensions/template/`
2. Modifique `extension.yml` com os detalhes da sua extensão
3. Adicione seus comandos personalizados em `commands/`
4. Teste localmente e publique

Veja `extensions/EXTENSION-DEVELOPMENT-GUIDE.md` para detalhes.

## Desenvolvimento

### Pré-requisitos

- Python 3.11+
- Gerenciador de pacotes uv
- Git

### Desenvolvimento Local

```bash
# Clonar o repositório
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Instalar dependências de desenvolvimento
uv sync --dev

# Executar localmente
uv run codexspec --help

# Executar testes
uv run pytest

# Verificar código com linter
uv run ruff check src/
```

### Build

```bash
# Construir o pacote
uv build
```

## Comparação com spec-kit

CodexSpec é inspirado no spec-kit do GitHub, mas com algumas diferenças importantes:

| Recurso | spec-kit | CodexSpec |
|---------|----------|-----------|
| Filosofia Principal | Desenvolvimento orientado a especificações | Desenvolvimento orientado a especificações |
| Nome do CLI | `specify` | `codexspec` |
| IA Principal | Suporte multi-agente | Focado em Claude Code |
| Prefixo de Comando | `/speckit.*` | `/codexspec.*` |
| Fluxo de Trabalho | specify → plan → tasks → implement | constitution → specify → generate-spec → plan → tasks → analyze → implement |
| Especificação em Duas Fases | Não | Sim (clarificação + geração) |
| Passos de Revisão | Opcional | Comandos de revisão integrados |
| Comando Clarify | Sim | Sim |
| Comando Analyze | Sim | Sim |
| Comando Checklist | Sim | Sim |
| Sistema de Extensões | Sim | Sim |
| Scripts PowerShell | Sim | Sim |
| Suporte i18n | Não | Sim (13+ idiomas via tradução LLM) |

## Filosofia

CodexSpec segue estes princípios fundamentais:

1. **Desenvolvimento orientado a intenções**: Especificações definem o "quê" antes do "como"
2. **Criação rica de especificações**: Usar guardrails e princípios organizacionais
3. **Refinamento em múltiplos passos**: Em vez de geração de código one-shot
4. **Alta dependência de IA**: Alavancar IA para interpretação de especificações
5. **Orientado a revisão**: Validar cada artefato antes de avançar
6. **Qualidade primeiro**: Checklists e análises integrados para qualidade de requisitos

## Contribuindo

Contribuições são bem-vindas! Por favor leia nossas diretrizes de contribuição antes de enviar um pull request.

## Licença

Licença MIT - veja [LICENSE](LICENSE) para detalhes.

## Agradecimentos

- Inspirado por [GitHub spec-kit](https://github.com/github/spec-kit)
- Construído para [Claude Code](https://claude.ai/code)

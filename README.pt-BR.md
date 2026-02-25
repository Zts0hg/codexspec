# CodexSpec

[English](README.md) | [中文](README.zh-CN.md) | [日本語](README.ja.md) | [Español](README.es.md) | **Português** | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md)

[![PyPI version](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**[📖 Documentação](https://zts0hg.github.io/codexspec/)**

**Um toolkit de Desenvolvimento Orientado a Especificações (SDD) para Claude Code**

CodexSpec e um toolkit que ajuda voce a construir software de alta qualidade usando uma abordagem estruturada e orientada a especificacoes. Ele inverte o script do desenvolvimento tradicional, transformando especificacoes em artefatos executaveis que guiam diretamente a implementacao.

## Filosofia de Design: Colaboracao Humano-AI

CodexSpec e construido sobre a crenca de que **o desenvolvimento assistido por AI efetivo requer participacao humana ativa em cada estagio**. O toolkit e desenvolvido em torno de um principio central:

> **Revisar e validar cada artefato antes de avancar.**

### Por Que a Supervisao Humana Importa

No desenvolvimento assistido por AI, pular estagios de revisao leva a:

| Problema | Consequencia |
|----------|--------------|
| Requisitos imprecisos | AI faz suposicoes que divergem de sua intecao |
| Especificacoes incompletas | Funcionalidades sao construidas sem casos de borda criticos |
| Planos tecnicos desalinhados | Arquitetura nao corresponde as necessidades do negocio |
| Decomposicoes de tarefas vagas | Implementacao sai dos trilhos, exigindo retrabalho caro |

### A Abordagem CodexSpec

CodexSpec estrutura o desenvolvimento em **pontos de verificacao revistaveis**:

```
Idea → Clarify → Review → Plan → Review → Tasks → Review → Analyze → Implement
               ↑              ↑              ↑
            Human checks    Human checks    Human checks
```

**Cada artefato tem um comando de revisao correspondente:**
- `spec.md` → `/codexspec.review-spec`
- `plan.md` → `/codexspec.review-plan`
- `tasks.md` → `/codexspec.review-tasks`
- Todos os artefatos → `/codexspec.analyze`

Este processo de revisao sistematica garante:
- **Deteccao precoce de erros**: Pegar mal-entendidos antes do codigo ser escrito
- **Verificacao de alinhamento**: Confirmar que a interpretacao da AI corresponde a sua intecao
- **Portoes de qualidade**: Validar completude, clareza e viabilidade em cada estagio
- **Reducao de retrabalho**: Investir minutos em revisao para economizar horas de reimplementacao

## Funcionalidades

### Workflow SDD Central
- **Baseado em Constituicao**: Estabelecer principios do projeto que guiam todas as decisoes subsequentes
- **Especificacao em Duas Fases**: Clarificacao interativa (`/specify`) seguida por geracao de documento (`/generate-spec`)
- **Desenvolvimento Orientado a Planos**: Escolhas tecnicas vem apos os requisitos serem validados
- **Tarefas Prontas para TDD**: Decomposicoes de tarefas impoem metodologia test-first

### Colaboracao Humano-AI
- **Comandos de Revisao**: Comandos de revisao dedicados para spec, plan e tasks para validar saida da AI
- **Clarificacao Interativa**: Refinamento de requisitos baseado em Q&A com feedback imediato
- **Analise Cross-Artefato**: Detectar inconsistencias entre spec, plan e tasks antes da implementacao
- **Checklists de Qualidade**: Avaliacao automatizada de qualidade para requisitos

### Experiencia do Desenvolvedor
- **Integracao com Claude Code**: Comandos slash nativos para Claude Code
- **Internacionalizacao (i18n)**: Suporte multilingue via traducao dinamica LLM
- **Multiplataforma**: Suporte para scripts Bash e PowerShell
- **Extensivel**: Arquitetura de plugins para comandos personalizados

## Instalacao

### Pre-requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recomendado) ou pip

### Opcao 1: Instalar com uv (Recomendado)

A forma mais facil de instalar o CodexSpec e usando uv:

```bash
uv tool install codexspec
```

### Opcao 2: Instalar com pip

Alternativamente, voce pode usar pip:

```bash
pip install codexspec
```

### Opcao 3: Uso unico

Execute diretamente sem instalar:

```bash
# Criar um novo projeto
uvx codexspec init my-project

# Inicializar em um projeto existente
cd your-existing-project
uvx codexspec init . --ai claude
```

### Opcao 4: Instalar do GitHub (Versao de Desenvolvimento)

Para a versao de desenvolvimento mais recente ou uma branch especifica:

```bash
# Usando uv
uv tool install git+https://github.com/Zts0hg/codexspec.git

# Usando pip
pip install git+https://github.com/Zts0hg/codexspec.git

# Branch ou tag especifica
uv tool install git+https://github.com/Zts0hg/codexspec.git@main
uv tool install git+https://github.com/Zts0hg/codexspec.git@v0.2.0
```

## Inicio Rapido

Apos a instalacao, voce pode usar o CLI:

```bash
# Criar novo projeto
codexspec init my-project

# Criar projeto com saida em portugues
codexspec init my-project --lang pt-BR

# Inicializar em projeto existente
codexspec init . --ai claude
# ou
codexspec init --here --ai claude

# Verificar ferramentas instaladas
codexspec check

# Ver versao
codexspec version
```

Para atualizar para a versao mais recente:

```bash
# Usando uv
uv tool install codexspec --upgrade

# Usando pip
pip install --upgrade codexspec
```

## Uso

### 1. Inicializar um Projeto

Apos a [instalacao](#instalacao), crie ou inicialize seu projeto:

```bash
codexspec init my-awesome-project
# ou no diretorio atual
codexspec init . --ai claude
```

### 2. Estabelecer Principios do Projeto

Inicie o Claude Code no diretorio do projeto:

```bash
cd my-awesome-project
claude
```

Use o comando `/codexspec.constitution` para criar os principios de governanca do projeto:

```
/codexspec.constitution Criar principios focados em qualidade de codigo, padroes de teste e arquitetura limpa
```

### 3. Clarificar Requisitos

Use `/codexspec.specify` para **explorar e clarificar** seus requisitos atraves de Q&A interativo:

```
/codexspec.specify Quero construir uma aplicacao de gerenciamento de tarefas
```

Este comando ira:
- Fazer perguntas de clarificacao para entender sua ideia
- Explorar casos de borda que voce pode nao ter considerado
- Co-criar requisitos de alta qualidade atraves de dialogo
- **NAO** gerar arquivos automaticamente - voce mantem o controle

### 4. Gerar Documento de Especificacao

Uma vez que os requisitos estao clarificados, use `/codexspec.generate-spec` para criar o documento `spec.md`:

```
/codexspec.generate-spec
```

Este comando atua como um "compilador de requisitos" que transforma seus requisitos clarificados em um documento de especificacao estruturado.

### 5. Revisar Especificacao (Recomendado)

**Antes de prosseguir para o planejamento, valide sua especificacao:**

```
/codexspec.review-spec
```

Este comando gera um relatorio de revisao detalhado com:
- Analise de completude de secoes
- Avaliacao de clareza e testabilidade
- Verificacao de alinhamento com a constituicao
- Recomendacoes priorizadas

### 6. Criar um Plano Tecnico

Use `/codexspec.spec-to-plan` para definir como implementar:

```
/codexspec.spec-to-plan Usar Python com FastAPI para o backend, PostgreSQL para o banco de dados e React para o frontend
```

O comando inclui **revisao de constitucionalidade** - verificando se seu plano esta alinhado com os principios do projeto.

### 7. Revisar Plano (Recomendado)

**Antes de decompor em tarefas, valide seu plano tecnico:**

```
/codexspec.review-plan
```

Isto verifica:
- Alinhamento com especificacao
- Solidez da arquitetura
- Adequacao da stack tecnologica
- Conformidade com a constituicao

### 8. Gerar Tarefas

Use `/codexspec.plan-to-tasks` para decompor o plano:

```
/codexspec.plan-to-tasks
```

As tarefas sao organizadas em fases padrao com:
- **Aplicacao de TDD**: Tarefas de teste precedem tarefas de implementacao
- **Marcadores paralelos `[P]`**: Identificam tarefas independentes
- **Especificacoes de caminho de arquivo**: Entregaveis claros por tarefa

### 9. Revisar Tarefas (Recomendado)

**Antes da implementacao, valide a decomposicao de tarefas:**

```
/codexspec.review-tasks
```

Isto verifica:
- Cobertura do plano
- Conformidade com TDD
- Correcao de dependencias
- Granularidade das tarefas

### 10. Analisar (Opcional mas Recomendado)

Use `/codexspec.analyze` para verificacao de consistencia entre artefatos:

```
/codexspec.analyze
```

Isto detecta problemas entre spec, plan e tasks:
- Lacunas de cobertura (requisitos sem tarefas)
- Duplicacoes e inconsistencias
- Violacoes da constituicao
- Itens subespecificados

### 11. Implementar

Use `/codexspec.implement-tasks` para executar a implementacao:

```
/codexspec.implement-tasks
```

A implementacao segue **workflow TDD condicional**:
- Tarefas de codigo: Test-first (Red → Green → Verify → Refactor)
- Tarefas nao testaveis (docs, config): Implementacao direta

## Comandos Disponiveis

### Comandos CLI

| Comando | Descricao |
|---------|-----------|
| `codexspec init` | Inicializar um novo projeto CodexSpec |
| `codexspec check` | Verificar ferramentas instaladas |
| `codexspec version` | Exibir informacao de versao |
| `codexspec config` | Ver ou modificar configuracao do projeto |

### Opcoes do `codexspec init`

| Opcao | Descricao |
|-------|-----------|
| `PROJECT_NAME` | Nome do novo diretorio do projeto |
| `--here`, `-h` | Inicializar no diretorio atual |
| `--ai`, `-a` | Assistente de IA a usar (padrao: claude) |
| `--lang`, `-l` | Idioma de saida (ex: en, pt, zh-CN, ja) |
| `--force`, `-f` | Forcar sobrescrita de arquivos existentes |
| `--no-git` | Pular inicializacao do git |
| `--debug`, `-d` | Habilitar saida de debug |

### Opcoes do `codexspec config`

| Opcao | Descricao |
|-------|-----------|
| `--set-lang`, `-l` | Definir o idioma de saida |
| `--set-commit-lang`, `-c` | Definir o idioma das mensagens de commit (padrao: idioma de saida) |
| `--list-langs` | Listar todos os idiomas suportados |

### Comandos Slash

Apos a inicializacao, estes comandos slash estao disponiveis no Claude Code:

#### Comandos de Workflow Central

| Comando | Descricao |
|---------|-----------|
| `/codexspec.constitution` | Criar ou atualizar constituicao do projeto com validacao cross-artefato e relatorio de impacto de sincronizacao |
| `/codexspec.specify` | **Clarificar** requisitos atraves de Q&A interativo (sem geracao de arquivo) |
| `/codexspec.generate-spec` | **Gerar** documento `spec.md` apos requisitos serem clarificados |
| `/codexspec.spec-to-plan` | Converter especificacao em plano tecnico com revisao de constitucionalidade e grafo de dependencia de modulos |
| `/codexspec.plan-to-tasks` | Decompor plano em tarefas atomicas com aplicacao TDD e marcadores paralelos `[P]` |
| `/codexspec.implement-tasks` | Executar tarefas com workflow TDD condicional (TDD para codigo, direto para docs/config) |

#### Comandos de Revisao (Portoes de Qualidade)

| Comando | Descricao |
|---------|-----------|
| `/codexspec.review-spec` | Validar especificacao para completude, clareza, consistencia e testabilidade com pontuacao |
| `/codexspec.review-plan` | Revisar plano tecnico para viabilidade, qualidade de arquitetura e alinhamento com a constituicao |
| `/codexspec.review-tasks` | Validar decomposicao de tarefas para cobertura do plano, conformidade TDD, dependencias e granularidade |

#### Comandos Avancados

| Comando | Descricao |
|---------|-----------|
| `/codexspec.clarify` | Escanear spec.md existente por ambiguidades usando 4 categorias focadas, integrar com achados de revisao |
| `/codexspec.analyze` | Analise cross-artefato nao destrutiva (spec, plan, tasks) com deteccao de problemas baseada em severidade |
| `/codexspec.checklist` | Gerar checklists de qualidade para validacao de requisitos |
| `/codexspec.tasks-to-issues` | Converter tarefas em GitHub issues para integracao com gerenciamento de projetos |

#### Comandos de Fluxo de Trabalho Git

| Comando | Descricao |
|---------|-----------|
| `/codexspec.commit` | Gerar mensagens de Conventional Commits com base no status do git e contexto da sessao |
| `/codexspec.commit-staged` | Gerar mensagem de commit apenas das alteracoes preparadas |

## Visao Geral do Fluxo de Trabalho

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    Fluxo de Trabalho de Colaboracao Humano-AI CodexSpec  │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. Constitution  ──►  Definir principios do projeto                     │
│         │                         com validacao cross-artefato           │
│         ▼                                                                │
│  2. Specify  ───────►  Q&A interativo para clarificar requisitos         │
│         │               (nenhum arquivo criado - controle humano)        │
│         ▼                                                                │
│  3. Generate Spec  ─►  Criar documento spec.md                           │
│         │                                                                │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ PORTAO DE REVISAO 1: /codexspec.review-spec ★                  ║   │
│  ║  Validar: Completude, Clareza, Testabilidade, Constituicao        ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  4. Clarify  ───────►  Resolver ambiguidades (iterativo)                 │
│         │               4 categorias focadas, max 5 perguntas            │
│         ▼                                                                │
│  5. Spec to Plan  ──►  Criar plano tecnico com:                         │
│         │               • Revisao de constitucionalidade (OBRIGATORIA)   │
│         │               • Grafo de dependencia de modulos                │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ PORTAO DE REVISAO 2: /codexspec.review-plan ★                  ║   │
│  ║  Validar: Alinhamento Spec, Arquitetura, Stack Tech, Fases        ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  6. Plan to Tasks  ─►  Gerar tarefas atomicas com:                       │
│         │               • Aplicacao TDD (testes antes de impl)          │
│         │               • Marcadores paralelos [P]                      │
│         │               • Especificacoes de caminho de arquivo          │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ PORTAO DE REVISAO 3: /codexspec.review-tasks ★                 ║   │
│  ║  Validar: Cobertura, Conformidade TDD, Dependencias, Granularidade║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  7. Analyze  ───────►  Verificacao de consistencia cross-artefato        │
│         │               Detectar lacunas, duplicacoes, problemas const. │
│         ▼                                                                │
│  8. Implement  ─────►  Executar com workflow TDD condicional             │
│                          Codigo: Test-first | Docs/Config: Direto        │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

**Insight Chave**: Cada portao de revisao (★) e um **ponto de verificacao humano** onde voce valida a saida da AI antes de investir mais tempo. Pular esses portoes frequentemente leva a retrabalho custoso.

### Conceito Chave: Fluxo de Trabalho de Clarificacao de Requisitos

O CodexSpec fornece **dois comandos de clarificacao distintos** para diferentes estagios do fluxo de trabalho:

#### specify vs clarify: Quando Usar Qual?

| Aspecto | `/codexspec.specify` | `/codexspec.clarify` |
|---------|----------------------|----------------------|
| **Proposito** | Exploracao inicial de requisitos | Refinamento iterativo de spec existente |
| **Quando Usar** | Comecando com nova ideia, sem spec.md | spec.md existe, precisa preencher lacunas |
| **Entrada** | Sua ideia ou requisito inicial | Arquivo spec.md existente |
| **Saida** | Nenhuma (apenas dialogo) | Atualiza spec.md com clarificacoes |
| **Metodo** | Q&A aberto | Escaneamento de ambiguidade estruturado (4 categorias) |
| **Limite de Perguntas** | Ilimitado | Maximo 5 perguntas |
| **Uso Tipico** | "Quero construir um app de tarefas" | "A spec carece de detalhes de tratamento de erros" |

#### Especificacao em Duas Fases

Antes de gerar qualquer documentacao:

| Fase | Comando | Proposito | Saida |
|------|---------|-----------|-------|
| **Exploracao** | `/codexspec.specify` | Q&A interativo para explorar e refinar requisitos | Nenhuma (apenas dialogo) |
| **Geracao** | `/codexspec.generate-spec` | Compilar requisitos clarificados em documento estruturado | `spec.md` |

#### Clarificacao Iterativa

Apos criar spec.md:

```
spec.md ──► /codexspec.clarify ──► spec.md atualizado (com secao Clarifications)
                │
                └── Escaneia ambiguidades em 4 categorias focadas:
                    • Lacunas de Completude - Secoes faltando, conteudo vazio
                    • Problemas de Especificidade - Termos vagos, restricoes indefinidas
                    • Clareza Comportamental - Tratamento de erros, transicoes de estado
                    • Problemas de Mensurabilidade - Requisitos nao-funcionais sem metricas
```

#### Beneficios deste Design

- **Colaboracao humano-AI**: Voce participa ativamente da descoberta de requisitos
- **Controle explicito**: Arquivos so sao criados quando voce decide
- **Foco em qualidade**: Requisitos sao completamente explorados antes da documentacao
- **Refinamento iterativo**: Specs podem ser melhoradas incrementalmente conforme o entendimento se aprofunda

## Estrutura do Projeto

Apos a inicializacao, seu projeto tera esta estrutura:

```
my-project/
├── .codexspec/
│   ├── memory/
│   │   └── constitution.md    # Principios de governanca do projeto
│   ├── specs/
│   │   └── {feature-id}/
│   │       ├── spec.md        # Especificacao de funcionalidade
│   │       ├── plan.md        # Plano tecnico
│   │       ├── tasks.md       # Decomposicao de tarefas
│   │       └── checklists/    # Checklists de qualidade
│   ├── templates/             # Templates personalizados
│   ├── scripts/               # Scripts auxiliares
│   │   ├── bash/              # Scripts Bash
│   │   └── powershell/        # Scripts PowerShell
│   └── extensions/            # Extensoes personalizadas
├── .claude/
│   └── commands/              # Comandos slash para Claude Code
└── CLAUDE.md                  # Contexto para Claude Code
```

## Internacionalizacao (i18n)

CodexSpec suporta multiplos idiomas atraves de **traducao dinamica LLM**. Em vez de manter templates traduzidos, deixamos o Claude traduzir o conteudo em tempo real com base na sua configuracao de idioma.

### Definindo o Idioma

**Durante a inicializacao:**
```bash
# Criar um projeto com saida em chines
codexspec init my-project --lang zh-CN

# Criar um projeto com saida em japones
codexspec init my-project --lang ja
```

**Apos a inicializacao:**
```bash
# Ver configuracao atual
codexspec config

# Alterar configuracao de idioma
codexspec config --set-lang zh-CN

# Listar idiomas suportados
codexspec config --list-langs
```

### Idioma das Mensagens de Commit

Voce pode configurar um idioma diferente para mensagens de commit do que o idioma de saida:

```bash
# Usar portugues para interacoes mas ingles para mensagens de commit
codexspec config --set-lang pt-BR
codexspec config --set-commit-lang en
```

**Prioridade de idioma para mensagens de commit:**
1. Configuracao `language.commit` (se especificado)
2. `language.output` (alternativa)
3. `"en"` (padrao)

**Nota:** O tipo de commit (feat, fix, docs, etc.) e o escopo sempre permanecem em ingles. Apenas a parte da descricao usa o idioma configurado.

### Arquivo de Configuracao

O arquivo `.codexspec/config.yml` armazena as configuracoes de idioma:

```yaml
version: "1.0"

language:
  # Idioma de saida para interacoes Claude e documentos gerados
  output: "zh-CN"

  # Idioma das mensagens de commit (padrao: idioma de saida)
  # Definir como "en" para mensagens de commit em ingles independentemente do idioma de saida
  commit: "zh-CN"

  # Idioma dos templates - mantenha como "en" para compatibilidade
  templates: "en"

project:
  ai: "claude"
  created: "2026-02-15"
```

### Idiomas Suportados

| Codigo | Idioma |
|--------|--------|
| `en` | English (padrao) |
| `zh-CN` | Chines (Simplificado) |
| `zh-TW` | Chines (Tradicional) |
| `ja` | Japones |
| `ko` | Coreano |
| `es` | Espanhol |
| `fr` | Frances |
| `de` | Alemao |
| `pt` | Portugues |
| `ru` | Russo |
| `it` | Italiano |
| `ar` | Arabico |
| `hi` | Hindi |

### Como Funciona

1. **Templates apenas em ingles**: Todos os templates de comando permanecem em ingles
2. **Configuracao de idioma**: O projeto especifica o idioma de saida preferido
3. **Traducao dinamica**: Claude le instrucoes em ingles, produz saida no idioma alvo
4. **Consciente do contexto**: Termos tecnicos (JWT, OAuth, etc.) permanecem em ingles quando apropriado

### Beneficios

- **Zero manutencao de traducao**: Nao ha necessidade de manter multiplas versoes de templates
- **Sempre atualizado**: Atualizacoes de templates beneficiam automaticamente todos os idiomas
- **Traducao consciente do contexto**: Claude fornece traducoes naturais e apropriadas ao contexto
- **Idiomas ilimitados**: Qualquer idioma suportado pelo Claude funciona imediatamente

### Constituicao e Documentos Gerados

Quando voce usa `/codexspec.constitution` para criar a constituicao do seu projeto, ela sera gerada no idioma especificado na sua configuracao:

- **Abordagem de Arquivo Unico**: A constituicao e gerada em apenas um idioma
- **Claude Entende Todos os Idiomas**: Claude pode trabalhar com arquivos de constituicao em qualquer idioma suportado
- **Colaboracao em Equipe**: Equipes devem usar um idioma de trabalho consistente

Este design evita problemas de sincronizacao entre multiplas versoes de idiomas e reduz a sobrecarga de manutencao.

## Sistema de Extensoes

CodexSpec suporta uma arquitetura de plugins para adicionar comandos personalizados:

### Estrutura de Extensao

```
my-extension/
├── extension.yml          # Manifesto da extensao
├── commands/              # Comandos slash personalizados
│   └── command.md
└── README.md
```

### Criando Extensoes

1. Copie o template de `extensions/template/`
2. Modifique `extension.yml` com os detalhes da sua extensao
3. Adicione seus comandos personalizados em `commands/`
4. Teste localmente e publique

Veja `extensions/EXTENSION-DEVELOPMENT-GUIDE.md` para detalhes.

## Desenvolvimento

### Pre-requisitos

- Python 3.11+
- Gerenciador de pacotes uv
- Git

### Desenvolvimento Local

```bash
# Clonar o repositorio
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Instalar dependencias de desenvolvimento
uv sync --dev

# Executar localmente
uv run codexspec --help

# Executar testes
uv run pytest

# Verificar codigo com linter
uv run ruff check src/
```

### Build

```bash
# Construir o pacote
uv build
```

## Comparacao com spec-kit

CodexSpec e inspirado no spec-kit do GitHub, mas com algumas diferencas importantes:

| Recurso | spec-kit | CodexSpec |
|---------|----------|-----------|
| Filosofia Principal | Desenvolvimento orientado a especificacoes | Desenvolvimento orientado a especificacoes + colaboracao humano-AI |
| Nome do CLI | `specify` | `codexspec` |
| IA Principal | Suporte multi-agente | Focado em Claude Code |
| Prefixo de Comando | `/speckit.*` | `/codexspec.*` |
| Sistema de Constituicao | Basico | Constituicao completa com validacao cross-artefato |
| Especificacao em Duas Fases | Nao | Sim (clarify + generate) |
| Comandos de Revisao | Opcional | 3 comandos de revisao dedicados com pontuacao |
| Comando Clarify | Sim | 4 categorias focadas, integracao com revisao |
| Comando Analyze | Sim | Somente leitura, baseado em severidade, consciente da constituicao |
| TDD em Tasks | Opcional | Aplicado (testes precedem implementacao) |
| Implementacao | Padrao | TDD condicional (codigo vs docs/config) |
| Sistema de Extensoes | Sim | Sim |
| Scripts PowerShell | Sim | Sim |
| Suporte i18n | Nao | Sim (13+ idiomas via traducao LLM) |

### Diferenciadores Chave

1. **Cultura Review-First**: Cada artefato principal tem um comando de revisao dedicado
2. **Governanca por Constituicao**: Principios sao validados, nao apenas documentados
3. **TDD por Padrao**: Metodologia test-first aplicada na geracao de tarefas
4. **Pontos de Verificacao Humanos**: Workflow desenvolvido em torno de portoes de validacao

## Filosofia

CodexSpec segue estes principios fundamentais:

### Fundamentos SDD

1. **Desenvolvimento orientado a intencoes**: Especificacoes definem o "que" antes do "como"
2. **Criacao rica de especificacoes**: Usar guardrails e principios organizacionais
3. **Refinamento em multiplos passos**: Em vez de geracao de codigo one-shot
4. **Governanca por Constituicao**: Principios do projeto guiam todas as decisoes

### Colaboracao Humano-AI

5. **Humano-no-loop**: AI gera artefatos, humanos validam
6. **Orientado a revisao**: Validar cada artefato antes de avancar
7. **Revelacao progressiva**: Informacao complexa revelada incrementalmente
8. **Explicito sobre implicito**: Requisitos devem ser claros, nao assumidos

### Garantia de Qualidade

9. **Test-driven por padrao**: Workflow TDD embutido na geracao de tarefas
10. **Consistencia cross-artefato**: Analisar spec, plan e tasks juntos
11. **Alinhamento com constituicao**: Todos os artefatos respeitam os principios do projeto

### Por Que Revisao Importa

| Sem Revisao | Com Revisao |
|-------------|-------------|
| AI faz suposicoes incorretas | Humano pega maus-entendidos cedo |
| Requisitos incompletos se propagam | Lacunas identificadas antes da implementacao |
| Arquitetura deriva da intecao | Alinhamento verificado em cada estagio |
| Tarefas perdem funcionalidade critica | Cobertura validada sistematicamente |
| **Resultado: Retrabalho, esforco desperdicado** | **Resultado: Certo na primeira vez** |

## Contribuindo

Contribuicoes sao bem-vindas! Por favor leia nossas diretrizes de contribuicao antes de enviar um pull request.

## Licenca

Licenca MIT - veja [LICENSE](LICENSE) para detalhes.

## Agradecimentos

- Inspirado por [GitHub spec-kit](https://github.com/github/spec-kit)
- Construido para [Claude Code](https://claude.ai/code)

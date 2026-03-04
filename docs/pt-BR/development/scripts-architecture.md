# Análise de Arquitetura de Scripts

Este documento detalha o fluxo lógico de código dos scripts no projeto CodexSpec e como eles são usados no Claude Code.

## 1. Visão Geral da Arquitetura

O CodexSpec é um kit de ferramentas **Spec-Driven Development (SDD)** que adota uma arquitetura de três camadas: CLI + templates + scripts auxiliares:

```
┌─────────────────────────────────────────────────────────────────┐
│                        Camada de Usuário (CLI)                   │
│  codexspec init | check | version | config                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Camada de Interação Claude Code               │
│  /codexspec.specify | /codexspec.analyze | ...                  │
│  (.claude/commands/*.md)                                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Camada de Scripts Auxiliares                │
│  .codexspec/scripts/*.sh (Bash) ou *.ps1 (PowerShell)          │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Fluxo de Implantação dos Scripts

### Fase 1: Inicialização `codexspec init`

Na função `init()` em `src/codexspec/__init__.py` (linhas 343-368), os scripts apropriados são copiados automaticamente com base no sistema operacional:

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

**Resultado**: Com base no sistema operacional, scripts de `scripts/bash/` ou `scripts/powershell/` são copiados para o diretório `.codexspec/scripts/` do projeto.

### Mecanismo de Resolução de Caminho

A função `get_scripts_dir()` (linhas 71-90) lida com múltiplos cenários de instalação:

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

## 3. Mecanismo de Invocação de Scripts no Claude Code

### Mecanismo Principal: Declaração YAML Frontmatter

Arquivos de template declaram dependências de scripts através do YAML frontmatter:

```yaml
---
description: Descrição do comando
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---
```

### Substituição de Placeholder

Use o placeholder `{SCRIPT}` nos templates:

```markdown
### 1. Initialize Context

Execute `{SCRIPT}` a partir da raiz do repo e analise o JSON para:
- `FEATURE_DIR` - Caminho do diretório da funcionalidade
- `AVAILABLE_DOCS` - Lista de documentos disponíveis
```

### Fluxo de Invocação

1. Usuário insere `/codexspec.analyze` no Claude Code
2. Claude lê o template `.claude/commands/codexspec.analyze.md`
3. Com base no sistema operacional, Claude substitui `{SCRIPT}` por:
   - **macOS/Linux**: `.codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks`
   - **Windows**: `.codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks`
4. Claude executa o script, analisa a saída JSON, continua operações subsequentes

## 4. Detalhes de Funcionalidade dos Scripts

### 4.1 `check-prerequisites.sh/ps1` - Script de Verificação de Pré-requisitos

Este é o script mais importante, usado para verificar o estado do ambiente e retornar informações estruturadas.

#### Funcionalidades Principais

- Verifica se está em uma branch feature (formato: `001-feature-name`)
- Detecta se arquivos obrigatórios existem (`plan.md`, `tasks.md`)
- Retorna informações de caminho em formato JSON

#### Opções de Parâmetros

| Parâmetro | Bash | PowerShell | Função |
|-----------|------|------------|--------|
| Saída JSON | `--json` | `-Json` | Saída em formato JSON |
| Exigir tasks.md | `--require-tasks` | `-RequireTasks` | Verifica se tasks.md existe |
| Incluir tasks.md | `--include-tasks` | `-IncludeTasks` | Incluir tasks.md em AVAILABLE_DOCS |
| Apenas caminhos | `--paths-only` | `-PathsOnly` | Pular verificação, apenas retornar caminhos |

#### Exemplo de Saída JSON

```json
{
  "FEATURE_DIR": "/caminho/para/.codexspec/specs/001-minha-funcionalidade",
  "AVAILABLE_DOCS": ["research.md", "data-model.md", "tasks.md"]
}
```

### 4.2 `common.sh/ps1` - Funções Utilitárias Comuns

Fornece funcionalidades comuns multiplataforma:

#### Funções da Versão Bash

| Função | Função |
|--------|--------|
| `get_feature_id()` | Obter feature ID da branch Git ou variável de ambiente |
| `get_specs_dir()` | Obter caminho do diretório specs |
| `is_codexspec_project()` | Verificar se está em um projeto CodexSpec |
| `require_codexspec_project()` | Garantir que está em um projeto CodexSpec, senão sai |
| `log_info/success/warning/error()` | Saída de log colorida |
| `command_exists()` | Verificar se comando existe |

#### Funções da Versão PowerShell

| Função | Função |
|--------|--------|
| `Get-RepoRoot` | Obter diretório raiz do repositório Git |
| `Get-CurrentBranch` | Obter nome da branch atual |
| `Test-HasGit` | Detectar se há repositório Git |
| `Test-FeatureBranch` | Verificar se está em branch feature |
| `Get-FeaturePathsEnv` | Obter todos os caminhos relacionados à feature |
| `Test-FileExists` | Verificar se arquivo existe |
| `Test-DirHasFiles` | Verificar se diretório tem arquivos |

### 4.3 `create-new-feature.sh/ps1` - Criar Nova Funcionalidade

#### Funcionalidades

- Gera automaticamente ID de feature incrementado (001, 002, ...)
- Cria diretório de feature e spec.md inicial
- Cria branch Git correspondente

#### Exemplo de Uso

```bash
./create-new-feature.sh -n "autenticação de usuário" -i 001
```

## 5. Comandos que Usam Scripts

Os seguintes 4 comandos usam scripts:

| Comando | Parâmetros de Scripts | Função |
|---------|----------------------|--------|
| `/codexspec.clarify` | `--json --paths-only` | Obter caminhos, não verificar arquivos |
| `/codexspec.checklist` | `--json` | Verificar se plan.md existe |
| `/codexspec.analyze` | `--json --require-tasks --include-tasks` | Verificar plan.md + tasks.md |
| `/codexspec.tasks-to-issues` | `--json --require-tasks --include-tasks` | Verificar plan.md + tasks.md |

## 6. Diagrama Completo do Fluxo de Trabalho

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        Fase de Inicialização                              │
│                                                                          │
│  $ codexspec init meu-projeto                                            │
│       │                                                                  │
│       ├── Criar estrutura de diretórios .codexspec/                      │
│       ├── Copiar scripts/*.sh → .codexspec/scripts/                      │
│       ├── Copiar templates/commands/*.md → .claude/commands/             │
│       └── Criar constitution.md, config.yml, CLAUDE.md                   │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────┐
│                        Fase de Uso (Claude Code)                          │
│                                                                          │
│  Usuário: /codexspec.analyze                                             │
│       │                                                                  │
│       ├── Claude lê .claude/commands/codexspec.analyze.md                │
│       │                                                                  │
│       ├── Analisa declaração de scripts no YAML frontmatter              │
│       │   scripts:                                                       │
│       │     sh: .codexspec/scripts/check-prerequisites.sh --json ...     │
│       │                                                                  │
│       ├── Substitui placeholder {SCRIPT}                                 │
│       │                                                                  │
│       ├── Executa script:                                                │
│       │   $ .codexspec/scripts/check-prerequisites.sh --json ...         │
│       │                                                                  │
│       ├── Analisa saída JSON:                                            │
│       │   {"FEATURE_DIR": "...", "AVAILABLE_DOCS": [...]}                │
│       │                                                                  │
│       ├── Lê spec.md, plan.md, tasks.md                                  │
│       │                                                                  │
│       └── Gera relatório de análise                                      │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## 7. Destaques de Design

### 7.1 Compatibilidade Multiplataforma

Mantém versões Bash e PowerShell simultaneamente, seleciona automaticamente via `sys.platform`:

```python
if sys.platform == "win32":
    # Copiar scripts PowerShell
else:
    # Copiar scripts Bash
```

### 7.2 Configuração Declarativa

Declara dependências de scripts via YAML frontmatter, claro e intuitivo:

```yaml
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json
```

### 7.3 Saída JSON

Scripts retornam dados estruturados, fáceis para Claude analisar:

```json
{
  "FEATURE_DIR": "/caminho/para/.codexspec/specs/001-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md"]
}
```

### 7.4 Verificação Progressiva

Diferentes comandos usam diferentes parâmetros, verificação sob demanda:

| Fase | Comando | Nível de Verificação |
|------|---------|---------------------|
| Antes do planejamento | `/codexspec.clarify` | Apenas caminhos |
| Depois do planejamento | `/codexspec.checklist` | plan.md |
| Depois das tarefas | `/codexspec.analyze` | plan.md + tasks.md |

### 7.5 Integração com Git

- Extração automática de feature ID do nome da branch
- Suporte a validação de nomenclatura de branch (formato `^\d{3}-`)
- Suporte a substituição por variável de ambiente (`SPECIFY_FEATURE` / `CODEXSPEC_FEATURE`)

## 8. Caminhos de Código Chave

| Arquivo | Linha/Posição | Função |
|---------|---------------|--------|
| `src/codexspec/__init__.py` | 343-368 | Lógica de cópia de scripts |
| `src/codexspec/__init__.py` | 71-90 | `get_scripts_dir()` resolução de caminho |
| `scripts/bash/check-prerequisites.sh` | arquivo completo | Script principal de verificação Bash |
| `scripts/powershell/check-prerequisites.ps1` | 56-146 | Script de verificação PowerShell |
| `scripts/bash/common.sh` | arquivo completo | Funções utilitárias Bash |
| `scripts/powershell/common.ps1` | arquivo completo | Funções utilitárias PowerShell |
| `templates/commands/*.md` | YAML frontmatter | Declaração de scripts |

## 9. Lista de Arquivos de Scripts

### Scripts Bash (`scripts/bash/`)

```
scripts/bash/
├── check-prerequisites.sh   # Script principal de verificação
├── common.sh                # Funções utilitárias comuns
└── create-new-feature.sh    # Criar nova funcionalidade
```

### Scripts PowerShell (`scripts/powershell/`)

```
scripts/powershell/
├── check-prerequisites.ps1  # Script principal de verificação
├── common.ps1               # Funções utilitárias comuns
└── create-new-feature.ps1   # Criar nova funcionalidade
```

---

*Este documento registra a arquitetura completa e fluxo de uso dos scripts no projeto CodexSpec. Se houver atualizações, modifique em conformidade.*

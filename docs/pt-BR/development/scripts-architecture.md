# Análise da arquitetura de scripts

Este documento detalha o fluxo lógico de código dos scripts no projeto CodexSpec e como eles são usados no Claude Code.

## 1. Visão geral da arquitetura

O CodexSpec é um kit de ferramentas de **Spec-Driven Development (SDD)** que adota uma arquitetura em três camadas: CLI + templates + scripts auxiliares:

```
┌─────────────────────────────────────────────────────────────────┐
│                        Camada do usuário (CLI)                   │
│  codexspec init | check | version | config                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Camada de interação com o Claude Code         │
│  /codexspec:specify | /codexspec:analyze | ...                  │
│  (.claude/commands/*.md)                                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Camada de scripts auxiliares                │
│  .codexspec/scripts/*.sh (Bash) ou *.ps1 (PowerShell)          │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Fluxo de implantação dos scripts

### Etapa 1: inicialização com `codexspec init`

Na função `init()` em `src/codexspec/__init__.py` (linhas 343-368), os scripts apropriados são copiados automaticamente conforme o sistema operacional:

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

**Resultado**: conforme o sistema operacional, os scripts de `scripts/bash/` ou `scripts/powershell/` são copiados para o diretório `.codexspec/scripts/` do projeto.

### Mecanismo de resolução de caminho

A função `get_scripts_dir()` (linhas 71-90) trata vários cenários de instalação:

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

## 3. Mecanismo de invocação dos scripts no Claude Code

### Mecanismo principal: declaração no YAML frontmatter

Os arquivos de template declaram dependências de scripts por meio do YAML frontmatter:

```yaml
---
description: Descrição do comando
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---
```

### Substituição de placeholder

Use o placeholder `{SCRIPT}` nos templates:

```markdown
### 1. Initialize Context

Execute `{SCRIPT}` a partir da raiz do repo e analise o JSON para:
- `FEATURE_DIR` - Caminho do diretório da funcionalidade
- `AVAILABLE_DOCS` - Lista de documentos disponíveis
```

### Fluxo de invocação

1. O usuário digita `/codexspec:analyze` no Claude Code
2. O Claude lê o template `.claude/commands/codexspec:analyze.md`
3. Conforme o sistema operacional, o Claude substitui `{SCRIPT}` por:
   - **macOS/Linux**: `.codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks`
   - **Windows**: `.codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks`
4. O Claude executa o script, analisa a saída JSON e prossegue com as ações seguintes

## 4. Detalhes das funcionalidades dos scripts

### 4.1 `check-prerequisites.sh/ps1` - script de verificação de pré-requisitos

Este é o script mais importante, usado para validar o estado do ambiente e retornar informações estruturadas.

#### Funcionalidades principais

- Verifica se você está em uma feature branch (formato: `2026-0613-1200ab-feature-name`)
- Detecta se os arquivos exigidos existem (`plan.md`, `tasks.md`)
- Retorna informações de caminho em formato JSON

#### Opções de parâmetros

| Parâmetro | Bash | PowerShell | Função |
|-----------|------|------------|--------|
| Saída JSON | `--json` | `-Json` | Emite em formato JSON |
| Exigir tasks.md | `--require-tasks` | `-RequireTasks` | Verifica se tasks.md existe |
| Incluir tasks.md | `--include-tasks` | `-IncludeTasks` | Inclui tasks.md em AVAILABLE_DOCS |
| Apenas caminhos | `--paths-only` | `-PathsOnly` | Pula validação, só retorna os caminhos |

#### Exemplo de saída JSON

```json
{
  "FEATURE_DIR": "/path/to/.codexspec/specs/2026-0613-1200ab-my-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md", "tasks.md"]
}
```

### 4.2 `common.sh/ps1` - funções utilitárias comuns

Fornece funcionalidades comuns multiplataforma:

#### Funções da versão Bash

| Função | Função |
|--------|--------|
| `get_feature_id()` | Obtém o feature ID a partir da branch Git ou de variável de ambiente |
| `get_specs_dir()` | Obtém o caminho do diretório specs |
| `is_codexspec_project()` | Verifica se está em um projeto CodexSpec |
| `require_codexspec_project()` | Garante que está em um projeto CodexSpec; caso contrário, sai |
| `log_info/success/warning/error()` | Logs coloridos no terminal |
| `command_exists()` | Verifica se um comando existe |

#### Funções da versão PowerShell

| Função | Função |
|--------|--------|
| `Get-RepoRoot` | Obtém o diretório raiz do repositório Git |
| `Get-CurrentBranch` | Obtém o nome da branch atual |
| `Test-HasGit` | Detecta se há um repositório Git |
| `Test-FeatureBranch` | Verifica se está em uma feature branch |
| `Get-FeaturePathsEnv` | Obtém todos os caminhos relacionados à funcionalidade |
| `Test-FileExists` | Verifica se um arquivo existe |
| `Test-DirHasFiles` | Verifica se um diretório contém arquivos |

### 4.3 `create-new-feature.sh/ps1` - criar nova funcionalidade

#### Funcionalidades

- Gera automaticamente um feature ID no formato `YYYY-MMDD-HHMMxx`
- Cria o diretório da funcionalidade e o `requirements.md` inicial
- Cria a branch Git correspondente
- Exige que o nome curto, após saneamento, contenha ao menos uma letra ou dígito ASCII

#### Exemplo de uso

```bash
./create-new-feature.sh -n "user authentication"
```

#### Contrato de nomenclatura de funcionalidades

- Identificadores sequenciais `NNN-name` não são suportados. Nomes com timestamp são
  o único formato de nomenclatura de funcionalidade.
- A compatibilidade legada se aplica aos artefatos: um `spec.md` existente pode ser
  usado quando `requirements.md` está ausente. Isso não habilita formatos alternativos
  de nomenclatura de diretório ou branch.
- O nome completo da funcionalidade identifica um workspace:
  `YYYY-MMDD-HHMMxx-short-name`. Workspaces criados independentemente podem
  compartilhar o ID de timestamp quando seus nomes curtos diferem.
- A busca por short-ID é apenas uma conveniência local. Se mais de um diretório
  corresponder, a resolução relata ambiguidade em vez de selecionar ou sobrescrever
  um workspace.

## 5. Comandos que usam scripts

Os quatro comandos a seguir usam scripts:

| Comando | Parâmetros de scripts | Função |
|---------|----------------------|--------|
| `/codexspec:clarify` | `--json --paths-only` | Obtém caminhos, sem validar arquivos |
| `/codexspec:checklist` | `--json` | Verifica se plan.md existe |
| `/codexspec:analyze` | `--json --require-tasks --include-tasks` | Verifica plan.md + tasks.md |
| `/codexspec:tasks-to-issues` | `--json --require-tasks --include-tasks` | Verifica plan.md + tasks.md |

## 6. Diagrama completo do fluxo de trabalho

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        Etapa de inicialização                            │
│                                                                          │
│  $ codexspec init my-project                                             │
│       │                                                                  │
│       ├── Cria a estrutura de diretórios .codexspec/                     │
│       ├── Copia scripts/*.sh → .codexspec/scripts/                       │
│       ├── Copia templates/commands/*.md → .claude/commands/              │
│       └── Cria constitution.md, config.yml, CLAUDE.md                    │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────┐
│                        Etapa de uso (Claude Code)                        │
│                                                                          │
│  Usuário: /codexspec:analyze                                             │
│       │                                                                  │
│       ├── Claude lê .claude/commands/codexspec:analyze.md                │
│       │                                                                  │
│       ├── Analisa a declaração de scripts no YAML frontmatter            │
│       │   scripts:                                                       │
│       │     sh: .codexspec/scripts/check-prerequisites.sh --json ...     │
│       │                                                                  │
│       ├── Substitui o placeholder {SCRIPT}                               │
│       │                                                                  │
│       ├── Executa o script:                                              │
│       │   $ .codexspec/scripts/check-prerequisites.sh --json ...         │
│       │                                                                  │
│       ├── Analisa a saída JSON:                                          │
│       │   {"FEATURE_DIR": "...", "AVAILABLE_DOCS": [...]}                │
│       │                                                                  │
│       ├── Lê spec.md, plan.md, tasks.md                                  │
│       │                                                                  │
│       └── Gera o relatório de análise                                    │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## 7. Destaques do design

### 7.1 Compatibilidade multiplataforma

Mantém versões em Bash e PowerShell simultaneamente, selecionando automaticamente via `sys.platform`:

```python
if sys.platform == "win32":
    # Copiar scripts PowerShell
else:
    # Copiar scripts Bash
```

### 7.2 Configuração declarativa

As dependências de scripts são declaradas via YAML frontmatter, de forma clara e intuitiva:

```yaml
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json
```

### 7.3 Saída JSON

Os scripts retornam dados estruturados, fáceis de o Claude analisar:

```json
{
  "FEATURE_DIR": "/path/to/.codexspec/specs/2026-0613-1200ab-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md"]
}
```

### 7.4 Validação progressiva

Comandos diferentes usam parâmetros diferentes, validando sob demanda:

| Etapa | Comando | Nível de validação |
|------|---------|--------------------|
| Pré-planejamento | `/codexspec:clarify` | Apenas caminhos |
| Pós-planejamento | `/codexspec:checklist` | plan.md |
| Pós-tarefas | `/codexspec:analyze` | plan.md + tasks.md |

### 7.5 Integração com Git

- Extração automática do feature ID a partir do nome da branch
- Suporte a validação de nomenclatura de branch (formato `^\d{3}-`)
- Suporte a sobrescrever via variável de ambiente (`CODEXSPEC_FEATURE`)

## 8. Caminhos de código relevantes

| Arquivo | Linha/posição | Função |
|---------|---------------|--------|
| `src/codexspec/__init__.py` | 343-368 | Lógica de cópia dos scripts |
| `src/codexspec/__init__.py` | 71-90 | Resolução de caminho em `get_scripts_dir()` |
| `scripts/bash/check-prerequisites.sh` | arquivo completo | Script Bash principal de verificação de pré-requisitos |
| `scripts/powershell/check-prerequisites.ps1` | 56-146 | Script PowerShell de verificação de pré-requisitos |
| `scripts/bash/common.sh` | arquivo completo | Funções utilitárias Bash comuns |
| `scripts/powershell/common.ps1` | arquivo completo | Funções utilitárias PowerShell comuns |
| `templates/commands/*.md` | YAML frontmatter | Declaração de scripts |

## 9. Lista de arquivos de scripts

### Scripts Bash (`scripts/bash/`)

```
scripts/bash/
├── check-prerequisites.sh   # Script principal de verificação de pré-requisitos
├── common.sh                # Funções utilitárias comuns
└── create-new-feature.sh    # Criar nova funcionalidade
```

### Scripts PowerShell (`scripts/powershell/`)

```
scripts/powershell/
├── check-prerequisites.ps1  # Script principal de verificação de pré-requisitos
├── common.ps1               # Funções utilitárias comuns
└── create-new-feature.ps1   # Criar nova funcionalidade
```

---

*Este documento registra a arquitetura completa e o fluxo de uso dos scripts no projeto CodexSpec. Se houver atualizações, ajuste este documento em conformidade.*

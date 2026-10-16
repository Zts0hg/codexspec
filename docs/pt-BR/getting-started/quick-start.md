# Início rápido

<a id="30-second-quick-start"></a>

## Início rápido em 30 segundos

Instale o CodexSpec e inicialize o projeto para o assistente que você usa:

```bash
uv tool install codexspec

# Create a new project for Claude Code
codexspec init my-project --ai claude

# Or initialize an existing project for Codex
cd your-existing-project
codexspec init . --ai codex

# Use --ai both when you want both integrations
```

Inicie o assistente instalado no projeto inicializado. O mesmo fluxo de trabalho
pode ser iniciado das seguintes formas:

| Assistente | Iniciar a descoberta de requisitos |
|-----------|------------------------------|
| Claude Code (`claude`) | `/codexspec:specify I want to build a todo application` |
| Codex (`codex`) | `$codexspec:specify I want to build a todo application` |

Personalize os princípios do projeto com `constitution` quando necessário.
Confirme o resumo final dos requisitos e continue no diretório da funcionalidade
e no espaço de trabalho retornados. Consulte o [Fluxo de trabalho principal](../user-guide/workflow.md#core-workflow)
para conhecer os comandos seguintes.

Se você usa o aplicativo desktop do Codex, pode [pedir ao Codex para instalar e inicializar seu projeto](installation.md#install-with-the-codex-desktop-app).

<a id="core-workflow"></a>

## Fluxo de trabalho principal

O fluxo de trabalho padrão de uma funcionalidade mantém uma sequência de
artefatos ligados por referências às fontes:

```text
/specify          → requirements.md
/generate-spec    → spec.md       → review-spec
/spec-to-design   → design.md     → review-design
/design-to-plan   → plan.md       → review-plan
/plan-to-tasks    → tasks.md      → review-tasks → analyze
/implement-tasks  → implementation and complete-feature code review
```

Os exemplos abaixo usam o prefixo `/codexspec:` do Claude. No Codex, use
`$codexspec:` com o mesmo nome de comando e os mesmos argumentos.

| Etapa | Comando | Finalidade e resultado |
|------|---------|--------------------|
| Princípios do projeto | `/codexspec:constitution` | Criar ou atualizar `constitution.md` e validar os artefatos afetados |
| Requisitos | `/codexspec:specify <idea>` | Discutir a intenção, confirmar o resumo final e salvar `requirements.md` |
| Especificação | `/codexspec:generate-spec <feature-dir>` | Transformar os requisitos confirmados em `spec.md`, com referências às fontes |
| Projeto técnico do sistema | `/codexspec:spec-to-design <feature-dir>` | Produzir `design.md` com componentes, interfaces e decisões importantes de projeto técnico |
| Plano de implementação | `/codexspec:design-to-plan <feature-dir>` | Produzir `plan.md` com fases, ordem e verificação |
| Tarefas | `/codexspec:plan-to-tasks <feature-dir>` | Produzir tarefas rastreáveis e verificáveis em `tasks.md` e executar a análise entre artefatos |
| Implementação | `/codexspec:implement-tasks <feature-dir>` | Executar as tarefas, verificar os resultados e corrigir os achados da revisão confirmados de forma independente |

Substitua `<feature-dir>` pelo diretório da funcionalidade retornado durante a
descoberta de requisitos. Continue no worktree correspondente ou informe seu
caminho explícito. Assim, os comandos e as sessões continuam trabalhando com a
mesma funcionalidade.

<a id="specify-clarify-and-analyze"></a>

### specify, clarify e analyze

- **specify** inicia ou retoma a descoberta de requisitos. O resumo dos requisitos
  só se torna vinculante após confirmação explícita.
- **clarify** resolve ambiguidades nos requisitos e na especificação existentes,
  com até cinco perguntas por execução, distribuídas em quatro categorias.
  Primeiro atualiza `requirements.md` e depois sincroniza `spec.md`.
- **analyze** verifica toda a sequência requisitos → especificação → projeto
  técnico → plano → tarefas. Aplica automaticamente correções determinísticas aos
  artefatos posteriores quando a correção decorre das fontes anteriores que os
  regem. Nunca edita `requirements.md`. Os achados não resolvidos são relatados.
  A análise é executada automaticamente após uma revisão de tarefas aprovada e
  tem caráter informativo; ela não é um critério de aprovação da implementação.

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

<a id="small-changes-with-quick"></a>

### Pequenas alterações com Quick

Use `quick` para uma alteração pequena e bem delimitada, como uma correção pontual:

```text
/codexspec:quick Fix the empty-state message on the task list
```

O Quick confirma e salva um resumo compacto dos requisitos. Em seguida, coordena
a especificação, o planejamento, as tarefas e a implementação, incluindo as
revisões dos comandos de geração. Alterações amplas ou decisões de produto e
projeto técnico ainda em aberto exigem o fluxo de trabalho padrão. O Quick pausa
quando precisa de uma nova decisão.

<a id="workflow-automation"></a>

### Automação do fluxo de trabalho

O padrão de `workflow.auto_next` é **false**. Se estiver definido como `true` na
configuração do espaço de trabalho ativo, a confirmação final dos requisitos dá
início à especificação. Cada etapa de geração avança após `PASS` ou
`PASS_WITH_WARNINGS`. `NEEDS_REVISION` ou `BLOCKED` interrompe a sequência, que
termina em `implement-tasks`.

A correção automática de artefatos se limita a defeitos verificados cuja solução
decorre de evidências dos artefatos anteriores. São permitidas no máximo duas
rodadas de correção e revisão. As recomendações são tratadas separadamente.
O ciclo de revisão e correção da implementação tem regras próprias de conclusão,
descritas abaixo.

Consulte o [guia do fluxo de trabalho](../user-guide/workflow.md) para ver as regras detalhadas.

<a id="project-structure"></a>

## Estrutura do projeto

A inicialização instala os recursos comuns e a integração do assistente selecionado:

```text
my-project/
├── .codexspec/
│   ├── config.yml
│   ├── memory/
│   │   └── constitution.md
│   ├── profile/
│   │   ├── constraints/
│   │   ├── conventions/
│   │   ├── pitfalls/
│   │   ├── decisions/
│   │   ├── strategies/
│   │   └── runbooks/
│   ├── review-code/              # Shared review standards
│   ├── specs/
│   │   └── <feature-id>-<name>/   # Added by feature workflows
│   │       ├── requirements.md
│   │       ├── spec.md
│   │       ├── design.md
│   │       ├── plan.md
│   │       ├── tasks.md
│   │       ├── review-*.md
│   │       └── checklists/       # When requested
│   ├── templates/docs/
│   └── scripts/                 # Platform helpers and commit runtime
├── .claude/commands/codexspec/   # --ai claude or both
├── .agents/skills/              # --ai codex or both
├── CLAUDE.md                    # Claude project context
└── AGENTS.md                    # Codex project context
```

O blueprint compartilhado fica no worktree dedicado de auto-dev. Não há uma cópia
editável separada em cada checkout do fluxo comum. Os rascunhos de revisão manual
do conhecimento são excluídos do Git.

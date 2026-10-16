# CodexSpec

![CodexSpec](assets/images/codexspec-logo-light.svg#only-light){ width="420" }

![CodexSpec](assets/images/codexspec-logo-dark.svg#only-dark){ width="420" }

**Um conjunto de ferramentas para Requirements-First SDD com Claude Code e OpenAI Codex**

O CodexSpec transforma requisitos confirmados em especificações, projetos técnicos,
planos, tarefas e implementações com rastreabilidade até suas fontes. Você decide
**o que** construir e **por quê**. O agente define **como** fazer isso dentro dos
requisitos confirmados, com etapas de revisão e conhecimento do projeto mantido
entre sessões.

Use o CodexSpec por meio dos comandos de barra do Claude Code, das skills do Codex
ou de ambos. Por padrão, cada funcionalidade do fluxo comum usa um worktree Git
separado. Um blueprint compartilhado opcional permite que o agente desenvolva
uma fila de requisitos confirmados de forma autônoma.

<a id="why-choose-codexspec"></a>

## Por que escolher o CodexSpec?

| Necessidade | O que o CodexSpec oferece |
|------|-------------------------|
| Clareza sobre a intenção do produto | Confirmação explícita e requisitos salvos em `requirements.md` antes da especificação |
| Desenvolvimento rastreável | Referências às fontes ao longo da sequência requisitos → especificação → projeto técnico → plano → tarefas |
| Decisões que podem ser revisadas | Quatro comandos de revisão de artefatos, análise entre artefatos e uma verificação separada de defeitos no código como critério de aprovação |
| Continuidade entre sessões e no trabalho em equipe | Registros das funcionalidades, princípios do projeto, conhecimento reutilizável e decisões anteriores relevantes |
| Várias funcionalidades em andamento | Um worktree Git por funcionalidade do fluxo comum, com reutilização consistente do espaço de trabalho |
| Mais automação | Avanço opcional entre etapas e desenvolvimento autônomo dos requisitos confirmados do blueprint |
| Preferências de idioma da equipe | Idiomas independentes para interação, documentos e commits |

<a id="what-is-requirements-first-sdd"></a>

### O que é Requirements-First SDD?

No desenvolvimento orientado a especificações que prioriza os requisitos
(Requirements-First Spec-Driven Development), os **requisitos confirmados são a
referência de maior prioridade para a funcionalidade**. Antes de derivar os
artefatos de implementação, o agente registra objetivos, restrições, decisões,
exclusões, perguntas em aberto e evidências de confirmação.

```text
Idea → Confirmed Requirements →     Spec    →     Design    →     Plan    →    Tasks     →     Code
                 ↓                   ↓              ↓              ↓             ↓              ↓
         User confirmation      review-spec   review-design   review-plan   review-tasks   review-code
```

Você confirma os requisitos; cada artefato derivado passa por uma revisão própria,
da especificação ao código.

A colaboração com as pessoas define e altera a intenção do produto. As revisões
automáticas verificam se os artefatos derivados correspondem a essa intenção.
Quando ativada, a automação faz o trabalho avançar pelas etapas aprovadas. Ela
não permite que o agente substitua silenciosamente os requisitos confirmados.

[![CodexSpec: desenvolvimento orientado por requisitos, revisões por etapa e reaproveitamento da experiência](../../assets/workflow/workflow-pt-BR-light.png#only-light)](../../assets/workflow/workflow-pt-BR-light.png#only-light)

[![CodexSpec: desenvolvimento orientado por requisitos, revisões por etapa e reaproveitamento da experiência](../../assets/workflow/workflow-pt-BR-dark.png#only-dark)](../../assets/workflow/workflow-pt-BR-dark.png#only-dark)

Abrir o diagrama em tamanho original: [☀️](../../assets/workflow/workflow-pt-BR-light.png) · [🌙](../../assets/workflow/workflow-pt-BR-dark.png)

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
e no espaço de trabalho retornados. Consulte o [Fluxo de trabalho principal](user-guide/workflow.md#core-workflow)
para conhecer os comandos seguintes.

Se você usa o aplicativo desktop do Codex, pode [pedir ao Codex para instalar e inicializar seu projeto](getting-started/installation.md#install-with-the-codex-desktop-app).

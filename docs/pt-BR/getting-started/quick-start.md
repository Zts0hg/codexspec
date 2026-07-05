# Início rápido

Esta página percorre o fluxo completo de **Requirements-First SDD** em oito passos.
Os requisitos confirmados são a autoridade de maior prioridade, e nada se torna vinculante até você confirmar explicitamente — cada etapa termina em um **Confirmation Gate** que você controla.

Para alterações pequenas e bem delimitadas, você pode pular o passo a passo completo e executar o `/codexspec:quick`.

## 1. Inicializar um projeto

Após a instalação, crie ou inicialize o seu projeto:

```bash
# Criar um novo projeto
codexspec init my-awesome-project

# Ou inicializar no diretório atual
codexspec init . --ai claude

# Com saída em chinês (define a base de output)
codexspec init my-project --lang zh-CN

# Totalmente não interativo (CI/scripts): base em zh-CN, mensagens de commit em inglês
codexspec init my-project --lang zh-CN --commit-lang en

# Definir cada dimensão de idioma explicitamente (scriptável, sem prompts)
codexspec init my-project \
  --interaction-lang zh-CN --document-lang en --commit-lang en
```

Depois entre no projeto e inicie o Claude Code:

```bash
cd my-awesome-project
claude
```

## 2. Estabelecer os princípios do projeto

Use o comando constitution para definir os padrões com os quais todos os artefatos posteriores serão verificados:

```
/codexspec:constitution Create principles focused on code quality and testing
```

## 3. Esclarecer os requisitos

Use `/codexspec:specify` para explorar os requisitos:

```
/codexspec:specify I want to build a task management application
```

Esse comando faz perguntas de esclarecimento, revela casos de borda e pede que você confirme um resumo final de requisitos, que é persistido em `requirements.md`.

> **Confirmation Gate**: o `/codexspec:specify` grava apenas as entradas que você confirma explicitamente. O resumo de requisitos que ele apresenta **não** é vinculante até você aceitá-lo — recuse, altere ou reabra qualquer item antes de dizer sim. Nada downstream pode se sobrepor ao que você confirmar aqui.

## 4. Gerar a especificação

Depois que o resumo de requisitos for confirmado, gere o documento de spec:

```
/codexspec:generate-spec
```

O `generate-spec` compila as entradas confirmadas em um `spec.md` estruturado, com referências à fonte para rastreabilidade, e em seguida executa uma revisão automática (defeitos exigem evidências concretas; sugestões consultivas nunca disparam alterações automáticas; defeitos verificados podem ser corrigidos e reavaliados por no máximo duas rodadas).

## 5. Revisar e validar

**Recomendado:** valide a spec antes de prosseguir:

```
/codexspec:review-spec
```

Esta é uma **revisão baseada em evidências**: todo defeito relatado cita evidência concreta, e os avisos de design ficam separados da aceitação.

## 6. Criar o plano técnico

```
/codexspec:spec-to-plan Use Python FastAPI for backend
```

O plano registra links `Covers` de volta aos requisitos da especificação e verifica os princípios aplicáveis da constituição.

## 7. Gerar tarefas

```
/codexspec:plan-to-tasks
```

As tarefas são organizadas em torno de resultados verificáveis, com links de rastreabilidade para o plano e os requisitos. A ordenação test-first é aplicada **condicionalmente** — apenas onde o plano, a constituição ou o risco da tarefa exigem. Tarefas não testáveis (docs, config) são implementadas diretamente.

## 8. Implementar

```
/codexspec:implement-tasks
```

A implementação segue **conditional TDD**: tarefas de código usam o ciclo Red → Green → Verify → Refactor quando exigido; tarefas de documentação e configuração são implementadas diretamente.

## Alterações pequenas: `/codexspec:quick`

Para uma alteração pequena e bem delimitada, você não precisa do passo a passo completo de oito etapas. O `/codexspec:quick` executa um fluxo compacto de Requirements-First SDD em um único comando:

```
/codexspec:quick Add a "remember me" checkbox to the login form
```

O Quick ainda respeita as mesmas salvaguardas do fluxo completo:

- Cria um workspace de funcionalidade e um `requirements.md` usando a mesma convenção de timestamp do `/codexspec:specify`.
- Apresenta um resumo conciso dos requisitos confirmados (`NEED-*`, os `CON-*`/`DEC-*` relevantes, `OUT-*`, `OPEN-*` não resolvidos) e aguarda a sua confirmação explícita — o **Confirmation Gate** continua valendo.
- Em seguida encadeia `/codexspec:generate-spec` → `/codexspec:spec-to-plan` → `/codexspec:plan-to-tasks` → `/codexspec:implement-tasks` nesse diretório de funcionalidade, com cada comando de geração responsável pelo seu próprio loop de revisão automática.

Se a alteração acabar se mostrando ampla ou tiver vários resultados independentes, o Quick pausa e recomenda o fluxo padrão.

## Estrutura do projeto

Após a inicialização:

```
my-project/
├── .codexspec/
│   ├── memory/
│   │   └── constitution.md    # Constituição do projeto
│   ├── specs/
│   │   └── {feature-id}/
│   │       ├── spec.md        # Especificação da funcionalidade
│   │       ├── plan.md        # Plano técnico
│   │       ├── tasks.md       # Decomposição de tarefas
│   │       └── checklists/    # Checklists de qualidade
│   ├── templates/             # Templates personalizados
│   ├── scripts/               # Scripts auxiliares
│   └── extensions/            # Extensões personalizadas
├── .claude/
│   └── commands/              # Slash commands do Claude Code
├── .agents/
│   └── skills/                # Skills do Codex (quando inicializado com --ai codex ou both)
├── CLAUDE.md                  # Contexto do Claude Code
└── AGENTS.md                  # Contexto do Codex
```

## Próximos passos

[Guia completo do fluxo de trabalho](../user-guide/workflow.md)

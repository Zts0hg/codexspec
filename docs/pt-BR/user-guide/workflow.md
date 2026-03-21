# Fluxo de Trabalho

O CodexSpec estrutura o desenvolvimento em **pontos de verificação revisáveis** com validação humana em cada etapa.

## Visão Geral do Fluxo de Trabalho

```
┌──────────────────────────────────────────────────────────────────────────┐
│              Fluxo de Trabalho de Colaboração Humano-AI do CodexSpec     │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. Constitution  ──►  Definir princípios do projeto                     │
│         │                                                                │
│         ▼                                                                │
│  2. Specify  ───────►  Perguntas e respostas interativas para esclarecer │
│         │               requisitos                                       │
│         ▼                                                                │
│  3. Generate Spec  ─►  Criar documento spec.md                           │
│         │               ✓ Revisão automática: gera review-spec.md        │
│         ▼                                                                │
│  4. Spec to Plan  ──►  Criar plano técnico                               │
│         │               ✓ Revisão automática: gera review-plan.md        │
│         ▼                                                                │
│  5. Plan to Tasks  ─►  Gerar tarefas atômicas                            │
│         │               ✓ Revisão automática: gera review-tasks.md       │
│         ▼                                                                │
│  6. Implement  ─────►  Executar com fluxo de trabalho TDD condicional    │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## Por Que a Revisão Importa

| Sem Revisão | Com Revisão |
|-------------|-------------|
| AI faz suposições incorretas | Humano detecta interpretações erradas cedo |
| Requisitos incompletos se propagam | Lacunas identificadas antes da implementação |
| Arquitetura se desvia da intenção | Alinhamento verificado em cada etapa |
| **Resultado: Retrabalho** | **Resultado: Correto na primeira vez** |

## Revisão Automática

Cada comando de geração agora **executa automaticamente uma revisão**:

- `/codexspec:generate-spec` → invoca automaticamente `review-spec`
- `/codexspec:spec-to-plan` → invoca automaticamente `review-plan`
- `/codexspec:plan-to-tasks` → invoca automaticamente `review-tasks`

Os relatórios de revisão são gerados junto com os artefatos, permitindo ver problemas imediatamente.

## Loop de Qualidade Iterativo

Quando problemas são encontrados nos relatórios de revisão, descreva as correções em linguagem natural e o sistema atualizará tanto o artefato quanto o relatório:

```
┌──────────────────────────────────────────────────────────────────────┐
│                    Loop de Qualidade Iterativo                        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Artefato (spec/plan/tasks.md)                                        │
│         │                                                             │
│         ▼                                                             │
│  Revisão automática  ───►  Relatório de revisão (review-*.md)         │
│         │                       │                                     │
│         │                       ▼                                     │
│         │                Problemas encontrados?                        │
│         │                       │                                     │
│         │                 ┌─────┴─────┐                               │
│         │                 │           │                               │
│         │                Sim        Não                               │
│         │                 │           │                               │
│         │                 ▼           ▼                               │
│         │       Descrever        Continuar para                       │
│         │       correção         próxima etapa                        │
│         │       na conversação                                           │
│         │                 │                                           │
│         │                 ▼                                           │
│         │       Atualizar simultaneamente:                             │
│         │         • Artefato (spec/plan/tasks.md)                      │
│         │         • Relatório de revisão (review-*.md)                 │
│         │                 │                                           │
│         └─────────────────┘                                           │
│           (Repetir até ficar satisfeito)                              │
│                                                                       │
│  Revisão manual: Execute /codexspec:review-* a qualquer momento       │
│  para obter uma nova análise                                          │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

**Como funciona**:

1. **Revisão automática**: Cada comando de geração executa automaticamente a revisão correspondente
2. **Relatório de revisão**: Gera arquivos `review-*.md` contendo os problemas encontrados
3. **Correção iterativa**: Descreva o que precisa ser corrigido na conversação, o artefato e o relatório são atualizados juntos
4. **Revisão manual**: Execute `/codexspec:review-spec|plan|tasks` a qualquer momento para uma nova análise

## Comandos Principais

| Etapa | Comando | Propósito |
|-------|---------|-----------|
| 1 | `/codexspec:constitution` | Definir princípios do projeto |
| 2 | `/codexspec:specify` | Perguntas e respostas interativas para requisitos |
| 3 | `/codexspec:generate-spec` | Criar documento de especificação (★ Revisão automática) |
| - | `/codexspec:review-spec` | Invocado automaticamente, ou revalidar manualmente |
| 4 | `/codexspec:spec-to-plan` | Criar plano técnico (★ Revisão automática) |
| - | `/codexspec:review-plan` | Invocado automaticamente, ou revalidar manualmente |
| 5 | `/codexspec:plan-to-tasks` | Dividir em tarefas (★ Revisão automática) |
| - | `/codexspec:review-tasks` | Invocado automaticamente, ou revalidar manualmente |
| 6 | `/codexspec:implement-tasks` | Executar implementação |

## Especificação em Duas Fases

### specify vs clarify

| Aspecto | `/codexspec:specify` | `/codexspec:clarify` |
|---------|----------------------|----------------------|
| **Propósito** | Exploração inicial | Refinamento iterativo |
| **Quando** | Nenhum spec.md existe | spec.md existe, precisa preencher lacunas |
| **Entrada** | Sua ideia inicial | spec.md existente |
| **Saída** | Nenhuma (apenas diálogo) | Atualiza spec.md |

## TDD Condicional

A implementação segue TDD condicional:

- **Tarefas de código**: Test-first (Vermelho → Verde → Verificar → Refatorar)
- **Tarefas não testáveis** (docs, config): Implementação direta

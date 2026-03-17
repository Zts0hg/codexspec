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
│         │                                                                │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ PORTÃO DE REVISÃO 1: /codexspec:review-spec ★                  ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  4. Spec to Plan  ──►  Criar plano técnico                               │
│         │                                                                │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ PORTÃO DE REVISÃO 2: /codexspec:review-plan ★                  ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  5. Plan to Tasks  ─►  Gerar tarefas atômicas                            │
│         │                                                                │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ PORTÃO DE REVISÃO 3: /codexspec:review-tasks ★                 ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  6. Implement  ─────►  Executar com fluxo de trabalho TDD condicional    │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## Por que a Revisão Importa

| Sem Revisão | Com Revisão |
|-------------|-------------|
| AI faz suposições incorretas | Humano detecta interpretações erradas cedo |
| Requisitos incompletos se propagam | Lacunas identificadas antes da implementação |
| Arquitetura se desvia da intenção | Alinhamento verificado em cada etapa |
| **Resultado: Retrabalho** | **Resultado: Correto na primeira vez** |

## Comandos Principais

| Etapa | Comando | Propósito |
|-------|---------|-----------|
| 1 | `/codexspec:constitution` | Definir princípios do projeto |
| 2 | `/codexspec:specify` | Perguntas e respostas interativas para requisitos |
| 3 | `/codexspec:generate-spec` | Criar documento de especificação |
| - | `/codexspec:review-spec` | ★ Validar especificação |
| 4 | `/codexspec:spec-to-plan` | Criar plano técnico |
| - | `/codexspec:review-plan` | ★ Validar plano |
| 5 | `/codexspec:plan-to-tasks` | Dividir em tarefas |
| - | `/codexspec:review-tasks` | ★ Validar tarefas |
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

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/images/codexspec-logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/images/codexspec-logo-light.svg">
  <img alt="CodexSpec Logo" src="assets/images/codexspec-logo-light.svg" width="420">
</picture>

# Bem-vindo ao CodexSpec

[![PyPI version](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Um toolkit de SDD Requirements-First para o Claude Code**

O CodexSpec ajuda você a construir software de alta qualidade por meio de **Requirements-First Spec-Driven Development (SDD)** — os requisitos confirmados são a autoridade de maior prioridade, e nada se torna vinculante até você confirmar explicitamente. Em vez de pular direto para o código, você confirma **o quê** construir e **por quê** antes de decidir **como** construir.

## Por que o CodexSpec?

Por que usar o CodexSpec sobre o Claude Code? Veja a comparação:

| Aspecto | Apenas Claude Code | CodexSpec + Claude Code |
|--------|------------------|-------------------------|
| **Suporte a múltiplos idiomas** | Interação em inglês por padrão | Configure o idioma da equipe para colaboração e revisões mais fluidas |
| **Rastreabilidade** | Difícil rastrear decisões após o fim da sessão | Todas as specs, planos e tarefas salvos em `.codexspec/specs/` |
| **Recuperação de sessão** | Interrupções do modo plan são difíceis de recuperar | Divisão em vários comandos + documentos persistidos = recuperação fácil |
| **Governança da equipe** | Sem princípios unificados, estilos inconsistentes | `constitution.md` impõe padrões e qualidade da equipe |

### O que é Requirements-First SDD?

**Requirements-First SDD** é a metodologia de Spec-Driven Development (SDD) com uma evolução: **os requisitos confirmados são a autoridade de maior prioridade**. Você define e confirma *o quê* construir e *por quê* antes de decidir *como* — e nada se torna vinculante até você confirmar explicitamente.

```
Tradicional:  Ideia → Código → Debug → Reescrever
SDD:          Ideia → Requisitos Confirmados → Spec → Plano → Tarefas → Código
```

### Principais recursos

- **Desenvolvimento baseado em Constituição** - Estabeleça princípios de projeto que orientam todas as decisões
- **Captura persistente de requisitos** - O `/specify` registra a discussão confirmada em `requirements.md` antes da geração de documentos
- **Revisões automáticas** - Todo artefato de spec, plano e tarefa gerado inclui verificações de qualidade embutidas
- **Esclarecimento interativo** - Refinamento de requisitos baseado em perguntas e respostas
- **Análise entre artefatos** - Detecte inconsistências antes da implementação
- **Tarefas rastreáveis** - As decomposições de tarefas preservam a cobertura de requisitos e do plano, aplicando **Conditional TDD** (ordenação test-first apenas onde o plano, a constituição ou o risco exigem; tarefas não testáveis, como docs/config, são implementadas diretamente)
- **Integração nativa com Claude Code** - Os slash commands funcionam de forma transparente
- **Suporte a múltiplos idiomas** - Mais de 13 idiomas via tradução dinâmica por LLM
- **Multiplataforma** - Scripts Bash e PowerShell incluídos
- **Extensível** - Arquitetura de plugins para comandos personalizados

## Início rápido

```bash
# Instalar
uv tool install codexspec

# Criar um novo projeto
codexspec init my-project

# Ou inicializar em um projeto existente
codexspec init . --ai claude
```

[Guia de instalação completo](getting-started/installation.md)

## Visão geral do fluxo de trabalho

O CodexSpec estrutura o desenvolvimento em **pontos de verificação revisáveis**. Os requisitos confirmados fluem por specs, planos e tarefas até chegarem ao código, com uma revisão em cada etapa.

```
Ideia → Requisitos Confirmados → Spec → Plano → Tarefas → Código
```

Cada artefato é produzido por um comando dedicado e validado antes do início da próxima etapa:

```
Ideia → /specify → requirements.md → /generate-spec → spec.md → /spec-to-plan → plan.md → /plan-to-tasks → tasks.md → /implement
                                                   │                         │                            │
                                              Revisar spec              Revisar plano                Revisar tarefas
```

### O Confirmation Gate

O diferencial definidor é o **Confirmation Gate**: requisitos, specs, planos e tarefas tornam-se vinculantes somente após a sua confirmação humana explícita. Os requisitos confirmados são a autoridade de maior prioridade sobre funcionalidades, então a IA não pode fixar decisões silenciosamente — artefatos derivados carregam links explícitos para a fonte, e conflitos são rastreados de volta em vez de propagados.

### Loop iterativo de qualidade

Cada comando de geração inclui uma **revisão automática baseada em evidências**: defeitos exigem evidências concretas, sugestões consultivas nunca disparam alterações automáticas, e defeitos verificados podem ser corrigidos e reavaliados por no máximo duas rodadas. Esse loop faz a qualidade subir sem que você precise vigiar cada detalhe.

[Aprenda o fluxo de trabalho](user-guide/workflow.md)

## Licença

Licença MIT - veja [LICENSE](https://github.com/Zts0hg/codexspec/blob/main/LICENSE) para detalhes.

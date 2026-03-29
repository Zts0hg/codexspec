<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/images/codexspec-logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/images/codexspec-logo-light.svg">
  <img alt="CodexSpec Logo" src="assets/images/codexspec-logo-light.svg" width="420">
</picture>

# Bem-vindo ao CodexSpec

[![Versão no PyPI](https://img.shields.io/pypi/v/codexspec:svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec:svg)](https://pypi.org/project/codexspec/)
[![Licença: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Um kit de ferramentas Spec-Driven Development (SDD) para Claude Code**

O CodexSpec é um kit de ferramentas que ajuda você a construir software de alta qualidade usando uma abordagem estruturada e orientada a especificações. Ele muda o paradigma do desenvolvimento tradicional ao tornar as especificações artefatos executáveis que guiam diretamente a implementação.

## Por que CodexSpec?

Por que usar CodexSpec alem do Claude Code? Aqui esta a comparacao:

| Aspecto | Apenas Claude Code | CodexSpec + Claude Code |
|---------|-------------------|-------------------------|
| **Suporte multilingue** | Interacao padrao em ingles | Configure o idioma da equipe para melhor colaboracao |
| **Rastreabilidade** | Dificil rastrear decisoes apos a sessao | Todos os specs, planos e tarefas salvos em `.codexspec/specs/` |
| **Recuperacao de sessao** | Dificil recuperar de interrupcoes no modo plan | Divisao em multiplos comandos + docs persistentes = recuperacao facil |
| **Governanca de equipe** | Sem principios unificados, estilos inconsistentes | `constitution.md` aplica padroes e qualidade da equipe |

### Colaboracao Humano-AI

O CodexSpec e construido sobre a crenca de que **o desenvolvimento eficaz auxiliado por IA requer participacao humana ativa em cada etapa**.

| Problema | Solucao |
|----------|---------|
| Requisitos pouco claros | Perguntas e respostas interativas para esclarecer antes de construir |
| Especificacoes incompletas | Comandos de revisao dedicados com pontuacao |
| Planos tecnicos desalinhados | Validacao baseada na constituicao |
| Divisoes de tarefas vagas | Geracao de tarefas com TDD obrigatorio |

### Recursos Principais

- **Baseado em Constituição** - Estabeleça princípios do projeto que guiam todas as decisões
- **Esclarecimento Interativo** - Refinamento de requisitos através de perguntas e respostas
- **Comandos de Revisão** - Valide artefatos em cada etapa
- **Pronto para TDD** - Metodologia test-first incorporada nas tarefas
- **Suporte i18n** - Mais de 13 idiomas via tradução LLM

## Início Rápido

```bash
# Instalar
uv tool install codexspec

# Criar um novo projeto
codexspec init meu-projeto

# Ou inicializar em um projeto existente
codexspec init . --ai claude
```

[Guia de Instalação Completo](getting-started/installation.md)

## Visão Geral do Fluxo de Trabalho

```
Ideia -> Esclarecer -> Revisar -> Planejar -> Revisar -> Tarefas -> Revisar -> Implementar
              ^                 ^                 ^
           Verificação         Verificação       Verificação
           humana              humana            humana
```

Cada artefato possui um comando de revisão correspondente para validar a saída da AI antes de prosseguir.

[Aprenda o Fluxo de Trabalho](user-guide/workflow.md)

## Licença

Licença MIT - consulte [LICENSE](https://github.com/Zts0hg/codexspec/blob/main/LICENSE) para detalhes.

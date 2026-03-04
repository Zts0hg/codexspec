# Bem-vindo ao CodexSpec

[![Versão no PyPI](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Licença: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Um kit de ferramentas Spec-Driven Development (SDD) para Claude Code**

O CodexSpec é um kit de ferramentas que ajuda você a construir software de alta qualidade usando uma abordagem estruturada e orientada a especificações. Ele muda o paradigma do desenvolvimento tradicional ao tornar as especificações artefatos executáveis que guiam diretamente a implementação.

## Por que CodexSpec?

### Colaboração Humano-AI

O CodexSpec é construído sobre a crença de que **o desenvolvimento eficaz auxiliado por IA requer participação humana ativa em cada etapa**.

| Problema | Solução |
|----------|---------|
| Requisitos pouco claros | Perguntas e respostas interativas para esclarecer antes de construir |
| Especificações incompletas | Comandos de revisão dedicados com pontuação |
| Planos técnicos desalinhados | Validação baseada na constituição |
| Divisões de tarefas vagas | Geração de tarefas com TDD obrigatório |

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

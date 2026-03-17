# Início Rápido

## 1. Inicializar um Projeto

Após a instalação, crie ou inicialize seu projeto:

```bash
# Criar novo projeto
codexspec init meu-projeto-incrivel

# Ou inicializar no diretório atual
codexspec init . --ai claude

# Com saída em português brasileiro
codexspec init meu-projeto --lang pt-BR
```

## 2. Estabelecer Princípios do Projeto

Inicie o Claude Code no diretório do projeto:

```bash
cd meu-projeto-incrivel
claude
```

Use o comando constitution:

```
/codexspec:constitution Criar princípios focados em qualidade de código e testes
```

## 3. Esclarecer Requisitos

Use `/codexspec:specify` para explorar os requisitos:

```
/codexspec:specify Eu quero construir uma aplicação de gerenciamento de tarefas
```

## 4. Gerar Especificação

Uma vez esclarecido, gere o documento de especificação:

```
/codexspec:generate-spec
```

## 5. Revisar e Validar

**Recomendado:** Valide antes de prosseguir:

```
/codexspec:review-spec
```

## 6. Criar Plano Técnico

```
/codexspec:spec-to-plan Usar Python FastAPI para o backend
```

## 7. Gerar Tarefas

```
/codexspec:plan-to-tasks
```

## 8. Implementar

```
/codexspec:implement-tasks
```

## Estrutura do Projeto

Após a inicialização:

```
meu-projeto/
+-- .codexspec/
|   +-- memory/
|   |   +-- constitution.md
|   +-- specs/
|   |   +-- {feature-id}/
|   |       +-- spec.md
|   |       +-- plan.md
|   |       +-- tasks.md
|   +-- scripts/
+-- .claude/
|   +-- commands/
+-- CLAUDE.md
```

## Próximos Passos

[Guia Completo de Fluxo de Trabalho](../user-guide/workflow.md)

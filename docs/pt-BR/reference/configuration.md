# Configuração

## Localização do arquivo de configuração

`.codexspec/config.yml`

## Schema de configuração

```yaml
version: "1.0"

language:
  output: "zh-CN"        # Idioma base; os três abaixo recaem sobre ele, depois sobre "en"
  interaction: "zh-CN"   # Diálogo com o LLM + saída do CLI codexspec (opcional → padrão: output)
  document: "en"         # Requisitos/spec/plan/tasks gerados (opcional → padrão: output)
  commit: "en"           # Mensagens de commit do git (opcional → padrão: output)
  templates: "en"        # Mantenha como "en"

project:
  ai: "claude"
  created: "2025-02-15"

workflow:
  auto_next: false       # Avanço automático entre etapas do fluxo (opt-in)

review:
  decided_by: reviewer   # Quem decide achados fora do contexto real de uso: reviewer (padrão) ou ask
```

## Configurações de idioma

O CodexSpec divide o idioma em quatro dimensões configuráveis de forma independente. `output` é a base; `interaction`, `document` e `commit` a sobrescrevem e recaem sobre ela (e depois sobre `en`) quando não definidas. Isso permite, por exemplo, conversar com o Claude em um idioma enquanto mantém os artefatos gerados ou as mensagens de commit em outro.

| Dimensão | Chave | Definir no init | Definir depois | Controla | Recai sobre |
|-----------|-------|-----------------|----------------|----------|-------------|
| Saída (base) | `output` | `--lang` | `config --set-lang` | base para as outras três | `en` |
| Interação | `interaction` | `--interaction-lang` | `config --set-interaction-lang` | diálogo com o LLM + saída da CLI | output → `en` |
| Documento | `document` | `--document-lang` | `config --set-document-lang` | spec/plan/tasks gerados | output → `en` |
| Commit | `commit` | `--commit-lang` | `config --set-commit-lang` | mensagens de commit do git | output → `en` |
| Templates | `templates` | — | — | origem dos templates de comando (sempre `en`) | — |

**Valores suportados:** veja [Internacionalização](../user-guide/i18n.md#supported-languages)

### `language.output`

O idioma base de saída. As demais dimensões recaem sobre ele quando não definidas explicitamente.

### `language.interaction`

Idioma da conversa entre você e o LLM, além da saída no terminal da CLI `codexspec`. Opcional — o padrão é `output`.

### `language.document`

Idioma dos arquivos de artefatos gerados (requisitos/spec/plan/tasks). Opcional — o padrão é `output`.

### `language.commit`

Idioma das mensagens de commit do git. Opcional — o padrão é `output`.

### `language.templates`

Idioma dos templates. Deve permanecer como `"en"` para compatibilidade.

## Configurações do projeto

### `project.ai`

O assistente de IA em uso. Controla quais arquivos de contexto de agente o `codexspec init` cria:

- `claude` (padrão) — cria `CLAUDE.md` (e `.claude/commands/`).
- `codex` — cria `AGENTS.md` e `.agents/skills/` em vez disso.
- `both` — cria todos os anteriores, deixando o projeto pronto tanto para Claude Code quanto para Codex CLI.

O `CLAUDE.md` é sempre criado (para que o projeto continue utilizável pelo Claude Code); `AGENTS.md` e `.agents/skills/` são criados apenas quando `project.ai` é `codex` ou `both`.

### `project.created`

Data em que o projeto foi inicializado.

## Configurações de fluxo de trabalho

### `workflow.auto_next`

Controla se o pipeline de Requirements-First SDD **avança automaticamente** para a próxima etapa do fluxo assim que a etapa atual é aprovada, em vez de exigir que você dispare o próximo comando manualmente.

- **Padrão:** `false` (opt-in). Apenas o valor literal `true` habilita o avanço automático.
- **Alternar / definir com:** `codexspec config --auto-next` (a flag isolada alterna o valor atual; passe `on`/`off` para defini-lo explicitamente).

**Cadeia:**

```
specify → generate-spec → spec-to-plan → plan-to-tasks → implement-tasks
```

**Critério de aprovação:**

- `generate-spec`, `spec-to-plan`, `plan-to-tasks`: o loop de revisão embutido no comando precisa informar um Overall Status de `PASS` ou `PASS_WITH_WARNINGS`.
- `specify`: não há loop de revisão, então o critério é a sua confirmação explícita de que a descoberta de requisitos terminou (o resumo **final** da etapa, e não cada resumo intermediário).
- `implement-tasks`: etapa terminal — nada dispara automaticamente depois dela.

Quando o loop de revisão informa `NEEDS_REVISION` ou `BLOCKED`, a cadeia para e o controle volta a você. Antes de cada avanço, o agente emite uma linha de aviso (por exemplo: `auto_next: review passed → invoking /codexspec:spec-to-plan`).

## Configurações de revisão

### `review.decided_by`

Define quem decide sobre um achado do `/codexspec:review-code` cujo gatilho depende de entradas ou ambientes fora do contexto real de uso do projeto.

- **Padrão:** `reviewer`, inclusive quando a chave ou a seção está ausente. O revisor decide cada achado, exatamente como antes.
- **`ask`:** a revisão relata esse item como uma decisão de cenário pendente em vez de falhar por ele. O `implement-tasks` pergunta a você uma única vez se deve corrigi-lo ou aceitar que o cenário está fora do escopo, e registra sua resposta em `requirements.md` como uma entrada `CON` ou `OUT` confirmada. As rodadas de revisão seguintes respeitam essa entrada.
- **Defina com:** `codexspec config --decided-by reviewer|ask` ou `/codexspec:config`. Uma única execução de `review-code` pode substituí-lo com `--decided-by`.
- Qualquer outro valor é inválido: o `codexspec config` o informa e o `review-code` para com um erro de argumento até que seja corrigido.

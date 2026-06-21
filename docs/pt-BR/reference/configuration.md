# Configuração

## Localização do Arquivo de Configuração

`.codexspec/config.yml`

## Schema de Configuração

```yaml
version: "1.0"

language:
  output: "zh-CN"        # Idioma base; os três abaixo recaem sobre ele e depois sobre "en"
  interaction: "zh-CN"   # Diálogo com o LLM + saída do CLI codexspec (opcional → padrão: output)
  document: "en"         # Requisitos/spec/plan/tasks gerados (opcional → padrão: output)
  commit: "en"           # Mensagens de commit do git (opcional → padrão: output)
  templates: "en"        # Idioma dos templates (mantenha como "en")

project:
  ai: "claude"      # Assistente de IA
  created: "2025-02-15"
```

## Configurações de Idioma

O CodexSpec divide o idioma em quatro dimensões configuráveis de forma independente. `output` é a base; `interaction`, `document` e `commit` a sobrescrevem e recaem sobre ela (e depois sobre `en`) quando não definidas. Isso permite, por exemplo, conversar com o Claude em um idioma enquanto mantém os artefatos gerados ou as mensagens de commit em outro.

| Dimensão | Chave | Definir no init | Definir depois | Controla | Recai sobre |
|-----------|-------|-----------------|----------------|----------|-------------|
| Saída (base) | `output` | `--lang` | `config --set-lang` | base para as outras três | `en` |
| Interação | `interaction` | `--interaction-lang` | `config --set-interaction-lang` | diálogo com o LLM + saída do CLI | output → `en` |
| Documento | `document` | `--document-lang` | `config --set-document-lang` | spec/plan/tasks gerados | output → `en` |
| Commit | `commit` | `--commit-lang` | `config --set-commit-lang` | mensagens de commit do git | output → `en` |
| Templates | `templates` | — | — | origem dos templates de comando (sempre `en`) | — |

**Valores suportados:** Consulte [Internacionalização](../user-guide/i18n.md#supported-languages)

### `language.output`

O idioma base de saída. As demais dimensões recaem sobre ele quando não são definidas explicitamente.

### `language.interaction`

Idioma da conversa entre você e o LLM, além da saída no terminal do CLI `codexspec`. Opcional — o padrão é `output`.

### `language.document`

Idioma dos arquivos de artefatos gerados (requisitos/spec/plan/tasks). Opcional — o padrão é `output`.

### `language.commit`

Idioma das mensagens de commit do git. Opcional — o padrão é `output`.

### `language.templates`

Idioma dos templates. Deve permanecer como `"en"` para compatibilidade.

## Configurações do Projeto

### `project.ai`

O assistente AI sendo usado. Atualmente suporta:

- `claude` (padrão)

### `project.created`

Data em que o projeto foi inicializado.

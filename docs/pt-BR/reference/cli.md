# Referência CLI

## Comandos

### `codexspec init`

Inicializar um novo projeto CodexSpec.

```bash
codexspec init [NOME_PROJETO] [OPÇÕES]
```

**Argumentos:**

| Argumento | Descrição |
|-----------|-----------|
| `NOME_PROJETO` | Nome para o seu novo diretório de projeto (use `.` ou `--here` para o diretório atual) |

**Opções:**

| Opção | Abrev. | Descrição |
|-------|--------|-----------|
| `--here` | `-h` | Inicializar no diretório atual |
| `--ai` | `-a` | Assistente de IA a usar (padrão: claude) |
| `--lang` | `-l` | Idioma (base) de saída; interaction/document/commit recaem sobre ele (ex: en, zh-CN, ja) |
| `--interaction-lang` | | Idioma de interação (diálogo com o LLM + saída do CLI `codexspec`); sobrescreve `--lang` |
| `--document-lang` | | Idioma dos documentos (requisitos/spec/plan/tasks gerados); sobrescreve `--lang` |
| `--commit-lang` | | Idioma das mensagens de commit; sobrescreve `--lang` |
| `--force` | `-f` | Sobrescrever arquivos existentes e confirmar prompts automaticamente; nunca regenera `config.yml` |
| `--no-git` | | Pular inicialização do git |
| `--debug` | `-d` | Habilitar saída de debug |

`--lang` define o idioma base de `output`; `--interaction-lang`, `--document-lang` e `--commit-lang` o sobrescrevem para a sua dimensão (cada um recai sobre `output` e depois sobre `en`). Veja [Internacionalização](../user-guide/i18n.md) para o modelo completo.

A primeira execução de `init` em um TTY sem `--lang` (e sem as três flags de dimensão) solicita um idioma base; em um ambiente não-TTY (CI/scripts) o padrão é `en` — **totalmente não interativo**. Executar `init` novamente preserva qualquer chave de idioma que você não tenha especificado; `--force` nunca regenera `config.yml`.

**Exemplos:**

```bash
# Criar novo projeto
codexspec init meu-projeto

# Inicializar no diretório atual
codexspec init . --ai claude

# Totalmente não interativo: base em zh-CN, mensagens de commit em inglês
codexspec init meu-projeto --lang zh-CN --commit-lang en

# Definir cada dimensão explicitamente (scriptável, sem prompts)
codexspec init meu-projeto \
  --interaction-lang zh-CN --document-lang en --commit-lang en
```

---

### `codexspec check`

Verificar ferramentas instaladas.

```bash
codexspec check
```

---

### `codexspec version`

Exibir informações de versão.

```bash
codexspec version
```

---

### `codexspec config`

Visualizar ou modificar a configuração do projeto.

```bash
codexspec config [OPÇÕES]
```

**Opções:**

| Opção | Abrev. | Descrição |
|-------|--------|-----------|
| `--set-lang` | `-l` | Definir o idioma (base) de saída |
| `--set-interaction-lang` | | Definir o idioma de interação (diálogo com o LLM + saída do CLI) |
| `--set-document-lang` | | Definir o idioma dos documentos (spec/plan/tasks gerados) |
| `--set-commit-lang` | `-c` | Definir o idioma das mensagens de commit |
| `--list-langs` | | Listar todos os idiomas suportados |

Cada `--set-*-lang` atualiza uma [dimensão de idioma](../user-guide/i18n.md); qualquer dimensão que você não definir recai sobre `output` e depois sobre `en`.

# Referência da CLI

## Comandos

### `codexspec show-blueprint`

Imprime o `.codexspec/blueprint.md` completo da branch fixa `codexspec/auto-dev` e de
`worktree-for-codexspec-auto-dev` como conteúdo bruto na saída padrão. Pré-requisitos ausentes são
informados no erro padrão com status diferente de zero. O comando é somente leitura e não executa
fetch, merge, escrita ou bloqueio.

```bash
codexspec show-blueprint
```

---

### `codexspec init`

Inicializa um novo projeto CodexSpec.

```bash
codexspec init [PROJECT_NAME] [OPTIONS]
```

**Argumentos:**

| Argumento | Descrição |
|----------|-----------|
| `PROJECT_NAME` | Nome do novo diretório do projeto (use `.` ou `--here` para o diretório atual) |

**Opções:**

| Opção | Abrev. | Descrição |
|-------|--------|-----------|
| `--here` | `-h` | Inicializa no diretório atual |
| `--ai` | `-a` | Assistente de IA a usar: `claude`, `codex` ou `both` (padrão: claude) |
| `--lang` | `-l` | Idioma (base) de saída; interaction/document/commit recaem sobre ele (ex.: en, zh-CN, ja) |
| `--interaction-lang` | | Idioma de interação (diálogo com o LLM + saída da CLI `codexspec`); sobrescreve `--lang` |
| `--document-lang` | | Idioma dos documentos (requisitos/spec/plan/tasks gerados); sobrescreve `--lang` |
| `--commit-lang` | | Idioma das mensagens de commit; sobrescreve `--lang` |
| `--force` | `-f` | Sobrescreve arquivos existentes e confirma prompts automaticamente; nunca regenera o `config.yml` |
| `--no-git` | | Pula a inicialização do repositório git |
| `--debug` | `-d` | Habilita a saída de debug |

`--lang` define o idioma base de `output`; `--interaction-lang`, `--document-lang` e `--commit-lang` o sobrescrevem para a sua dimensão (cada um recai sobre `output` e depois sobre `en`). Veja [Internacionalização](../user-guide/i18n.md) para o modelo completo.

A primeira execução do `init` em um TTY sem `--lang` (e sem as três flags de dimensão) solicita um idioma base; em um ambiente não-TTY (CI/scripts) o padrão é `en` — **totalmente não interativo**. Executar o `init` novamente preserva qualquer chave de idioma que você não tenha especificado; `--force` nunca regenera o `config.yml`.

**Exemplos:**

```bash
# Criar novo projeto
codexspec init my-project

# Inicializar no diretório atual
codexspec init . --ai claude

# Uso único (sem instalação) — inicializar para Codex CLI ou both
uvx codexspec init . --ai codex
uvx codexspec init . --ai both

# Totalmente não interativo: base em zh-CN, mensagens de commit em inglês
codexspec init my-project --lang zh-CN --commit-lang en

# Definir cada dimensão explicitamente (scriptável, sem prompts)
codexspec init my-project \
  --interaction-lang zh-CN --document-lang en --commit-lang en
```

`codexspec init` instala os recursos de revisão compartilhados pelo Claude Code e Codex em `.codexspec/review-code/`. `--force` atualiza recursos distribuídos e preserva arquivos de extensão com outros caminhos. Instalar apenas a CLI não cria arquivos de projeto. Com apenas o plugin, se o projeto não tiver a árvore instalada, a revisão usa os mesmos recursos da raiz resolvida pelo host.

---

### `codexspec check`

Verifica as ferramentas instaladas.

```bash
codexspec check
```

---

### `codexspec version`

Exibe informações de versão.

```bash
codexspec version
```

---

### `codexspec config`

Exibe ou modifica a configuração do projeto.

```bash
codexspec config [OPTIONS]
```

**Opções:**

| Opção | Abrev. | Descrição |
|-------|--------|-----------|
| `--set-lang` | `-l` | Define o idioma (base) de saída |
| `--set-interaction-lang` | | Define o idioma de interação (diálogo com o LLM + saída da CLI) |
| `--set-document-lang` | | Define o idioma dos documentos (spec/plan/tasks gerados) |
| `--set-commit-lang` | `-c` | Define o idioma das mensagens de commit |
| `--list-langs` | | Lista todos os idiomas suportados |
| `--auto-next` | | Alterna/define `workflow.auto_next` (a flag isolada alterna; ou on/off) |
| `--auto-maintenance` |  | Alterna/define `workflow.auto_maintenance` (on por padrão; sem valor alterna; ou on/off) |
| `--decided-by` | | Define `review.decided_by` como `reviewer` (padrão) ou `ask` |

Cada `--set-*-lang` atualiza uma [dimensão de idioma](../user-guide/i18n.md); qualquer dimensão que você não definir recai sobre `output` e depois sobre `en`.

`codexspec config --auto-maintenance on|off` salva `workflow.auto_maintenance` como booleano YAML em `.codexspec/config.yml`; se a chave não existir, vale `true`. As duas opções aceitam `on/true/1/yes` e `off/false/0/no` sem diferenciar maiúsculas. `implement-tasks` lê essa configuração ao corrigir automaticamente: `on` inclui melhorias incrementais de manutenção fundamentadas; `off` continua relatando as sugestões. Defeitos reais e verificações necessárias continuam obrigatórios. A configuração é independente de `auto-next` e não é um parâmetro de chamada de `implement-tasks`.

```bash
codexspec config --auto-maintenance on
codexspec config --auto-maintenance off
```

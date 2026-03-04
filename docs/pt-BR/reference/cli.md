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
| `NOME_PROJETO` | Nome para seu novo diretório de projeto |

**Opções:**

| Opção | Abrev. | Descrição |
|-------|--------|-----------|
| `--here` | `-h` | Inicializar no diretório atual |
| `--ai` | `-a` | Assistente AI a usar (padrão: claude) |
| `--lang` | `-l` | Idioma de saída (ex: en, pt-BR, ja) |
| `--force` | `-f` | Forçar sobrescrita de arquivos existentes |
| `--no-git` | | Pular inicialização do git |
| `--debug` | `-d` | Habilitar saída de debug |

**Exemplos:**

```bash
# Criar novo projeto
codexspec init meu-projeto

# Inicializar no diretório atual
codexspec init . --ai claude

# Com saída em português brasileiro
codexspec init meu-projeto --lang pt-BR
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
| `--set-lang` | `-l` | Definir o idioma de saída |
| `--list-langs` | | Listar todos os idiomas suportados |

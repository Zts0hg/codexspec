# Referência da CLI

<a id="cli-commands"></a>

## Comandos da CLI

| Comando | Finalidade |
|---------|---------|
| `codexspec init` | Inicializar ou atualizar um projeto para Claude, Codex ou ambos |
| `codexspec check` | Verificar ferramentas e dependências instaladas |
| `codexspec version` | Exibir informações de versão e sistema |
| `codexspec config` | Consultar ou alterar a configuração do projeto |
| `codexspec list-commands` | Listar os comandos de agentes disponíveis por categoria |
| `codexspec show-blueprint` | Exibir o blueprint do worktree compartilhado sem alterá-lo |

<a id="cli-installation"></a>

## Instalação da CLI

```bash
uv tool install codexspec

# Or use pip
pip install codexspec

# Verify the CLI and inspect available commands
codexspec version
codexspec --help
codexspec list-commands
```

Inicialize um novo projeto com `codexspec init my-project --ai claude` ou o
diretório atual com `codexspec init . --ai codex`. Use `--ai both` para as duas
integrações. O assistente padrão é `claude`; para usar Codex ou ambos, informe
essa escolha explicitamente.

<details>
<summary>Métodos alternativos de instalação</summary>

<a id="one-time-initialization"></a>

### Inicialização em uma única execução

```bash
uvx codexspec init my-project --ai claude
uvx codexspec init . --ai codex
```

A inicialização em uma única execução instala os comandos do projeto e o ambiente
independente de execução de commits. O roteamento de worktrees, blueprint/auto-dev
e a revisão manual do perfil continuam usando a CLI do CodexSpec. Deixe essa CLI
disponível para esses fluxos de trabalho.

<a id="development-versions"></a>

### Versões de desenvolvimento

```bash
uv tool install git+https://github.com/Zts0hg/codexspec.git
uv tool install git+https://github.com/Zts0hg/codexspec.git@main

# Replace <tag> with the version you want
uv tool install git+https://github.com/Zts0hg/codexspec.git@<tag>
```

</details>

<details>
<summary>Instalação no Windows</summary>

Use o PowerShell:

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
# Restart PowerShell, then:
uv tool install codexspec
codexspec version
```

Consulte o [Guia de solução de problemas no Windows](../WINDOWS-TROUBLESHOOTING.md)
para resolver problemas com PATH e instalação.

</details>

<a id="upgrade-and-refresh-a-project"></a>

## Atualizar a CLI e os comandos de um projeto

Atualizar a CLI e atualizar os comandos instalados em um projeto são duas etapas distintas:

```bash
uv tool install codexspec --upgrade
# Or: pip install --upgrade codexspec

# In the project you want to refresh; select its desired integration(s)
codexspec init . --force --ai both
```

Use `--ai claude` ou `--ai codex` se quiser apenas essa integração. `--force`
regenera os comandos e scripts distribuídos e atualiza os recursos de revisão.
Também confirma automaticamente as solicitações de migração, atualização de
comandos e conformidade com a Constituição do Projeto. Os requisitos e princípios
existentes são mantidos. Nos arquivos de contexto existentes, as orientações
gerenciadas são atualizadas e o restante do conteúdo é preservado. As chaves de
configuração que você não definir explicitamente também são mantidas.

O comando de planejamento é `design-to-plan`. As atualizações da instalação
removem a entrada antiga `spec-to-plan`, sem manter um alias.

<details>
<summary>Opções de inicialização da CLI</summary>

| Opção | Significado |
|--------|---------|
| `PROJECT_NAME` | Nome do novo diretório; use `.` para o diretório atual |
| `--here`, `-h` | Inicializar o diretório atual |
| `--ai`, `-a` | `claude`, `codex` ou `both`; o padrão é `claude` |
| `--lang`, `-l` | Definir o idioma base da saída |
| `--interaction-lang` | Definir o idioma de interação |
| `--document-lang` | Definir o idioma dos documentos |
| `--commit-lang` | Definir o idioma das mensagens de commit |
| `--force`, `-f` | Regenerar os artefatos instalados e confirmar automaticamente solicitações de migração, atualização e conformidade; preservar o contexto escrito para o projeto e as configurações não relacionadas |
| `--no-git` | Pular a inicialização do repositório Git |
| `--debug`, `-d` | Exibir informações detalhadas de depuração |

</details>

<details>
<summary>Opções de configuração da CLI</summary>

| Opção | Significado |
|--------|---------|
| `--set-lang`, `-l` | Definir o idioma base da saída |
| `--set-interaction-lang` | Definir o idioma de interação |
| `--set-document-lang` | Definir o idioma dos documentos |
| `--set-commit-lang`, `-c` | Definir o idioma das mensagens de commit |
| `--list-langs` | Listar os códigos de idioma aceitos |
| `--auto-next` | Alternar ou definir o avanço automático entre etapas |
| `--auto-distill` | Alternar ou definir a captura automática de conhecimento |
| `--auto-maintenance` | Alternar ou definir a manutenção incremental automática |
| `--worktrees` | Alternar ou definir o isolamento por worktree local a cada checkout |
| `--decided-by` | Definir o modo de decisão da revisão como `reviewer` ou `ask` |

</details>

## `codexspec show-blueprint`

Imprime o `.codexspec/blueprint.md` completo da branch fixa `codexspec/auto-dev` e de
`worktree-for-codexspec-auto-dev` como conteúdo bruto na saída padrão. Se o repositório, a branch, o worktree ou o arquivo estiver ausente, a saída de erro padrão
recebe um diagnóstico e o comando termina com um código diferente de zero. O comando é somente leitura e não executa
fetch, merge, escrita ou bloqueio.

```bash
codexspec show-blueprint
```

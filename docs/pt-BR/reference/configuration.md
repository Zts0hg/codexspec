<a id="configuration-and-internationalization"></a>

# Configuração e internacionalização

A configuração fica em `.codexspec/config.yml`. Os modelos continuam em inglês;
os agentes escrevem as interações e os artefatos gerados nos idiomas configurados.
Os 13 códigos de idioma padrão são `en`, `zh-CN`, `zh-TW`, `ja`, `ko`, `es`,
`fr`, `de`, `pt`, `ru`, `it`, `ar` e `hi`.
O código da CLI para português é `pt`; a documentação localizada e os catálogos
de tradução usam `pt-BR`.

<a id="language-dimensions"></a>

## Dimensões de idioma

| Dimensão | Chave de configuração | Na inicialização | Definir depois | Controla |
|-----------|------------|-------------------|-----------|----------|
| Saída/base | `language.output` | `--lang` | `config --set-lang` | Idioma usado quando as demais dimensões não têm configuração própria |
| Interação | `language.interaction` | `--interaction-lang` | `config --set-interaction-lang` | Conversas e saída da CLI |
| Documento | `language.document` | `--document-lang` | `config --set-document-lang` | Requisitos, especificações, projetos técnicos, planos e tarefas |
| Commit | `language.commit` | `--commit-lang` | `config --set-commit-lang` | Mensagens de commit e textos gerados nos fluxos de trabalho com Git |

Quando uma dimensão não tem um idioma próprio configurado, ela usa
`language.output`, independentemente das outras dimensões. Se esse valor também
não estiver definido, usa `en`. `language.templates` continua sendo `en`.

```bash
codexspec init my-project --ai both \
  --interaction-lang zh-CN --document-lang en --commit-lang en

codexspec config
codexspec config --set-document-lang en
codexspec config --list-langs
```

Na primeira inicialização com TTY, o idioma base é solicitado, a menos que você
informe `--lang` ou as três opções específicas de idioma. `--force` confirma
automaticamente as outras solicitações de inicialização, mas não elimina essa
escolha de idioma. Sem TTY, o padrão é inglês. Ao inicializar novamente, as chaves
de idioma que você não definir explicitamente são preservadas.

<a id="workflow-and-review-settings"></a>

## Configurações de fluxo de trabalho e revisão

| Configuração | Padrão | Efeito | Controle pela CLI |
|---------|---------|--------|-------------|
| `workflow.auto_next` | `false` | Avançar pelas etapas aprovadas do fluxo comum de SDD | `config --auto-next on\|off` |
| `workflow.auto_distill` | `true` | Capturar conhecimento sem interação após um encerramento bem-sucedido | `config --auto-distill on\|off` |
| `workflow.auto_maintenance` | `true` | Aplicar manutenção incremental verificada durante correções automáticas | `config --auto-maintenance on\|off` |
| `workflow.worktrees` | `true` | Isolar as funcionalidades do fluxo comum e a manutenção independente | `config --worktrees on\|off` |
| `review.decided_by` | `reviewer` | Definir quem decide sobre achados com condições de ocorrência fora do contexto operacional do projeto | `config --decided-by reviewer\|ask` |

As opções booleanas da CLI aceitam `on/true/1/yes` e `off/false/0/no`, sem distinguir
maiúsculas de minúsculas e permitindo espaços em branco ao redor. Uma opção
booleana sem valor alterna o valor atual do checkout de destino. Os valores
armazenados em YAML são booleanos.

Com `review.decided_by: reviewer`, o revisor decide quais achados são admitidos
como defeitos. Com `ask`, uma condição de ocorrência fora do contexto gera uma
decisão de cenário pendente. O usuário decide uma vez se o defeito deve ser
corrigido ou se o cenário deve ser excluído; a decisão confirmada é mantida para
as rodadas seguintes. Decisões pendentes bloqueiam a conclusão. Uma execução
individual de `review-code` pode substituir o modo configurado com `--decided-by`.

As alterações de configuração seguem o roteamento de worktrees. Uma alteração
independente iniciada no checkout principal é feita no worktree de manutenção
e não muda imediatamente a configuração efetiva do checkout principal.
Alterações em um worktree de funcionalidade entram em vigor ali.

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

<details>
<summary>Exemplo de configuração</summary>

```yaml
version: "1.0"

language:
  output: "en"
  interaction: "zh-CN"
  document: "en"
  commit: "en"
  templates: "en"

project:
  ai: "both"

workflow:
  auto_next: false
  auto_distill: true
  auto_maintenance: true
  worktrees: true

review:
  decided_by: reviewer
```

</details>

Veja os detalhes sobre idiomas e configurações em
[Configuração](configuration.md) e
[Internacionalização](../user-guide/i18n.md).

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="codexspec-logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="codexspec-logo-light.svg">
    <img alt="CodexSpec Logo" src="codexspec-logo-light.svg" width="420">
  </picture>
</div>

<h1 align="center">CodexSpec</h1>

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh-CN.md">中文</a> | <a href="README.ja.md">日本語</a> | <a href="README.es.md">Español</a> | <b>Português</b> | <a href="README.ko.md">한국어</a> | <a href="README.de.md">Deutsch</a> | <a href="README.fr.md">Français</a>
</p>

<p align="center">
  <a href="https://pypi.org/project/codexspec/"><img src="https://img.shields.io/pypi/v/codexspec.svg?style=for-the-badge" alt="PyPI version"></a>
  <a href="https://pypi.org/project/codexspec/"><img src="https://img.shields.io/pypi/pyversions/codexspec.svg?style=for-the-badge" alt="Python versions"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License: MIT"></a>
</p>

<p align="center">
  <strong>Um conjunto de ferramentas de SDD com requisitos em primeiro lugar para Claude Code e OpenAI Codex</strong>
</p>

O CodexSpec transforma requisitos confirmados em especificações, projetos técnicos,
planos, tarefas e implementações rastreáveis. Você decide **o que** construir e
**por quê**; o agente desenvolve **como** dentro desses requisitos confirmados,
com pontos de revisão e conhecimento persistente do projeto.

Use-o por meio de comandos de barra do Claude Code, skills do Codex ou ambos.
Por padrão, funcionalidades comuns usam worktrees Git separados, e um blueprint
compartilhado opcional permite que o agente desenvolva uma fila de requisitos
confirmados de forma autônoma.

[📖 Documentação](https://zts0hg.github.io/codexspec/) | [中文文档](https://zts0hg.github.io/codexspec/zh/) | [日本語ドキュメント](https://zts0hg.github.io/codexspec/ja/) | [한국어 문서](https://zts0hg.github.io/codexspec/ko/) | [Documentación](https://zts0hg.github.io/codexspec/es/) | [Documentation](https://zts0hg.github.io/codexspec/fr/) | [Dokumentation](https://zts0hg.github.io/codexspec/de/) | [Documentação](https://zts0hg.github.io/codexspec/pt-BR/)

## Índice

- [Por que escolher o CodexSpec?](#por-que-escolher-o-codexspec)
- [Início rápido em 30 segundos](#início-rápido-em-30-segundos)
- [Instalação](#instalação)
- [Fluxo de trabalho principal](#fluxo-de-trabalho-principal)
- [Blueprint compartilhado e desenvolvimento autônomo](#blueprint-compartilhado-e-desenvolvimento-autônomo)
- [Desenvolvimento com worktrees](#desenvolvimento-com-worktrees)
- [Trabalhar com código existente](#trabalhar-com-código-existente)
- [Revisão e depuração](#revisão-e-depuração)
- [Conhecimento do projeto](#conhecimento-do-projeto)
- [Fluxo de trabalho Git](#fluxo-de-trabalho-git)
- [Comandos disponíveis](#comandos-disponíveis)
- [Configuração e internacionalização](#configuração-e-internacionalização)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Materiais para extensões](#materiais-para-extensões)
- [Desenvolvimento](#desenvolvimento)
- [Contribuir](#contribuir)
- [Licença](#licença)

## Por que escolher o CodexSpec?

| Necessidade | O que o CodexSpec oferece |
|------|-------------------------|
| Intenção clara do produto | Confirmação explícita e um `requirements.md` persistente antes da especificação |
| Desenvolvimento rastreável | Referências às fontes ao longo de requisitos → especificação → projeto técnico → plano → tarefas |
| Decisões que podem ser revisadas | Quatro comandos de revisão de artefatos, análise entre artefatos e uma verificação separada de defeitos no código como critério de aprovação |
| Continuidade entre sessões e no trabalho em equipe | Registros de funcionalidades, princípios do projeto, conhecimento reutilizável e decisões históricas relevantes |
| Várias funcionalidades em andamento | Um worktree Git por funcionalidade comum, com reutilização estável do espaço de trabalho |
| Mais automação | Avanço opcional entre etapas e desenvolvimento autônomo de requisitos confirmados do blueprint |
| Preferências de idioma da equipe | Idiomas independentes para interação, documentos e commits |

### O que é SDD com requisitos em primeiro lugar?

O desenvolvimento orientado a especificações com requisitos em primeiro lugar
torna os **requisitos confirmados a autoridade máxima da funcionalidade**. O agente
registra objetivos, restrições, decisões, exclusões, perguntas em aberto e evidências
de confirmação antes de derivar os artefatos de implementação.

```text
Idea → Confirmed Requirements → Spec → Design → Plan → Tasks → Code
```

A colaboração humana estabelece e altera a intenção do produto. Revisões
automáticas verificam os artefatos derivados em relação a essa intenção. Ativar a
automação faz o trabalho avançar pelas etapas aprovadas; isso não permite que o
agente substitua requisitos confirmados silenciosamente.

## Início rápido em 30 segundos

Instale o CodexSpec e inicialize o projeto para o assistente que você usa:

```bash
uv tool install codexspec

# Create a new project for Claude Code
codexspec init my-project --ai claude

# Or initialize an existing project for Codex
cd your-existing-project
codexspec init . --ai codex

# Use --ai both when you want both integrations
```

Inicie seu assistente instalado no projeto inicializado. O mesmo fluxo de trabalho
usa estas duas formas de invocação:

| Assistente | Iniciar a descoberta de requisitos |
|-----------|------------------------------|
| Claude Code (`claude`) | `/codexspec:specify I want to build a todo application` |
| Codex (`codex`) | `$codexspec:specify I want to build a todo application` |

Personalize os princípios do projeto com `constitution` quando necessário.
Confirme o resumo final dos requisitos e continue usando o diretório da
funcionalidade e o espaço de trabalho retornados. Consulte o
[Fluxo de trabalho principal](#fluxo-de-trabalho-principal) para conhecer os demais comandos.

Está usando o aplicativo desktop do Codex? [Peça ao Codex para instalar e inicializar seu projeto](#instalar-com-o-aplicativo-desktop-do-codex).

## Instalação

### Instalar com o aplicativo desktop do Codex

Você pode pedir ao Codex para instalar o CodexSpec e configurar seu projeto diretamente pelo aplicativo desktop.

1. Adicione um projeto local no aplicativo desktop do Codex e selecione a pasta em que deseja trabalhar.
2. Inicie uma conversa nesse projeto e cole a solicitação abaixo.
3. Se o aplicativo pedir permissão para baixar ou instalar dependências, aprove a ação solicitada para continuar.

```text
Please install and initialize CodexSpec in the current project.
Project: https://github.com/Zts0hg/codexspec

Complete the setup directly instead of asking me to run terminal commands.

Check the environment. If uv or Python 3.11+ is missing, install the required
tools in my user directory using their official installation instructions.
Install the latest stable release of CodexSpec.

For a new setup, initialize the current project for Codex in English:
codexspec init . --ai codex --lang en

If CodexSpec is already configured, check its version and configuration before
updating. Preserve existing requirements, project principles, user files,
and configuration settings.

Verify that the CLI works and that AGENTS.md and the CodexSpec skill files
under .agents/skills/ are installed. Explain the result and how to start
describing my requirements in plain English. If the skills are not yet
available in this chat, tell me whether to start a new chat or restart the app.
```

Para respostas e documentos em chinês, substitua `--lang en` por `--lang zh-CN` e peça ao Codex para explicar o resultado em chinês.

O Codex instala a mesma CLI e as mesmas skills de projeto usadas na configuração manual abaixo. Você pode começar a usá-las com uma solicitação como `$codexspec:specify I want to build a todo application`. Consulte o [guia de skills da OpenAI](https://learn.chatgpt.com/docs/build-skills) para entender como as skills locais são descobertas e atualizadas.

### Pré-requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recomendado) ou pip
- O assistente que você pretende usar: Claude Code ou Codex
- Git para desenvolvimento com worktrees e fluxos de trabalho Git

### Instalação da CLI

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
diretório atual com `codexspec init . --ai codex`. Use `--ai both` para ambas as
integrações. A seleção padrão do assistente é `claude`; escolha o valor
explicitamente para Codex ou ambos.

<details>
<summary>Métodos alternativos de instalação</summary>

#### Inicialização de uso único

```bash
uvx codexspec init my-project --ai claude
uvx codexspec init . --ai codex
```

A inicialização de uso único instala os comandos do projeto e o ambiente de
execução independente de commits. O roteamento de worktrees, blueprint/auto-dev
e a revisão manual do perfil ainda invocam a CLI do CodexSpec; disponibilize-a
para esses fluxos de trabalho.

#### Versões de desenvolvimento

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

Consulte o [Guia de solução de problemas no Windows](docs/en/WINDOWS-TROUBLESHOOTING.md)
para resolver problemas de PATH e instalação.

</details>

### Atualizar o CodexSpec e renovar a instalação de um projeto

Atualizar a CLI e renovar os comandos instalados de um projeto são etapas distintas:

```bash
uv tool install codexspec --upgrade
# Or: pip install --upgrade codexspec

# In the project you want to refresh; select its desired integration(s)
codexspec init . --force --ai both
```

Use `--ai claude` ou `--ai codex` quando quiser apenas essa integração.
`--force` regenera os comandos/scripts distribuídos e atualiza os recursos de
revisão; também confirma automaticamente as solicitações de migração, atualização
de comandos e conformidade com a Constituição do Projeto. Os requisitos e
princípios existentes do projeto são mantidos, os corpos dos arquivos de contexto
existentes são preservados enquanto as orientações gerenciadas são atualizadas,
e as chaves de configuração que você não definiu explicitamente são mantidas.

O comando de planejamento é `design-to-plan`; atualizações da instalação retiram
a entrada antiga `spec-to-plan` sem criar um alias.

### Instalação pelo marketplace de plugins

Para Claude Code, instale o plugin pelo marketplace:

```text
/plugin marketplace add Zts0hg/codexspec
/plugin install codexspec@codexspec-market
/codexspec:config
```

O plugin fornece comandos e orientações no início da sessão para análise de
commits preparados e consulta a requisitos históricos, inclusive em sessões
retomadas. A instalação do plugin não inicializa um projeto. Use
`/codexspec:config` para criar ou modificar configurações de idioma, fluxo de
trabalho e revisão; use a inicialização pela CLI quando precisar da estrutura
completa do projeto.

A prévia direta de commits e os commits autorizados no diretório de trabalho
atual podem usar o ambiente de execução incluído com Python 3.11+ e Git, sem uma
CLI do CodexSpec instalada de forma persistente. O roteamento de worktrees,
blueprint/auto-dev e a revisão manual do perfil mantêm seus requisitos de CLI.
O hook de inicialização do plugin requer Git no PATH e uma versão do Claude Code
que aceite `args` em hooks de comando (forma exec). Suas orientações são para o
agente; ele não intercepta comandos Git manuais.

Consulte [Instalação](docs/en/getting-started/installation.md) para os detalhes da configuração.

## Fluxo de trabalho principal

O fluxo de trabalho padrão de uma funcionalidade preserva uma cadeia vinculada às fontes:

```text
/specify          → requirements.md
/generate-spec    → spec.md       → review-spec
/spec-to-design   → design.md     → review-design
/design-to-plan   → plan.md       → review-plan
/plan-to-tasks    → tasks.md      → review-tasks → analyze
/implement-tasks  → implementation and complete-feature code review
```

Os exemplos abaixo usam o prefixo `/codexspec:` do Claude. No Codex, use
`$codexspec:` com o mesmo nome de comando e os mesmos argumentos.

| Etapa | Comando | Finalidade e saída |
|------|---------|--------------------|
| Princípios do projeto | `/codexspec:constitution` | Criar/atualizar `constitution.md` e validar os artefatos afetados |
| Requisitos | `/codexspec:specify <idea>` | Discutir a intenção, confirmar um resumo final e persistir `requirements.md` |
| Especificação | `/codexspec:generate-spec <feature-dir>` | Compilar requisitos confirmados em `spec.md` com referências às fontes |
| Projeto técnico do sistema | `/codexspec:spec-to-design <feature-dir>` | Produzir `design.md`: componentes, interfaces e decisões centrais do projeto técnico |
| Plano de implementação | `/codexspec:design-to-plan <feature-dir>` | Produzir `plan.md`: fases, ordem e verificação |
| Tarefas | `/codexspec:plan-to-tasks <feature-dir>` | Produzir `tasks.md` rastreável e verificável; executar a análise entre artefatos |
| Implementação | `/codexspec:implement-tasks <feature-dir>` | Executar tarefas, verificar resultados e corrigir os achados da revisão verificados de forma independente |

Substitua `<feature-dir>` pelo diretório da funcionalidade retornado durante a
descoberta. Continue no worktree dela ou passe seu caminho explícito; isso mantém
a mesma identidade da funcionalidade entre comandos e sessões.

### specify, clarify e analyze

- **specify** inicia ou retoma a descoberta de requisitos. Somente a confirmação
  explícita torna o resumo dos requisitos vinculante.
- **clarify** resolve ambiguidades nos requisitos/especificação existentes:
  até cinco perguntas por execução, distribuídas em quatro categorias. Ele
  atualiza `requirements.md` primeiro e depois sincroniza `spec.md`.
- **analyze** verifica a cadeia completa de requisitos → especificação → projeto
  técnico → plano → tarefas. Ele aplica automaticamente correções determinísticas
  aos artefatos posteriores quando a correção decorre da autoridade dos artefatos
  anteriores; nunca edita `requirements.md`. Os achados não resolvidos são
  relatados. Ele é executado automaticamente após uma revisão de tarefas aprovada
  e é informativo, em vez de ser um critério de aprovação da implementação.

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

### Pequenas alterações com Quick

Use `quick` para uma alteração pequena e bem delimitada, como uma correção pontual:

```text
/codexspec:quick Fix the empty-state message on the task list
```

O Quick confirma e persiste um resumo compacto dos requisitos e depois coordena
especificação, planejamento, tarefas e implementação com as revisões dos comandos
de geração. Alterações amplas ou escolhas de produto/projeto técnico ainda não
resolvidas exigem o fluxo de trabalho padrão; o Quick pausa quando precisa de uma
nova decisão.

### Automação do fluxo de trabalho

O padrão de `workflow.auto_next` é **false**. Quando ele é `true` na configuração
do espaço de trabalho ativo, a confirmação final dos requisitos avança para a
especificação. Cada etapa de geração avança após `PASS` ou `PASS_WITH_WARNINGS`;
`NEEDS_REVISION` ou `BLOCKED` interrompe a cadeia. `implement-tasks` é a etapa final.

A correção automática de artefatos se limita a defeitos verificados cuja correção
decorre de evidências anteriores, com no máximo duas rodadas de correção e revisão.
As recomendações ficam separadas. O ciclo de revisão/correção da implementação tem
suas próprias regras de conclusão, descritas abaixo.

Consulte o [guia do fluxo de trabalho](docs/en/user-guide/workflow.md) para os contratos detalhados.

## Blueprint compartilhado e desenvolvimento autônomo

Use `blueprint` quando quiser preparar vários requisitos confirmados antes do
desenvolvimento, e `auto-dev` para desenvolver essa fila:

```text
/codexspec:blueprint Add a confirmed requirement for task reminders
/codexspec:auto-dev
```

A descoberta do blueprint resolve a direção, as escolhas e as restrições que
cabem ao usuário antes que um requisito entre na fila. O arquivo compartilhado
`.codexspec/blueprint.md` usa os estados `pending`, `in_progress` e `completed`.
Você pode acrescentar, substituir, excluir ou reordenar requisitos pendentes;
entradas ativas e concluídas são somente leitura para a manutenção do blueprint.

O Auto-dev segue a ordem do documento, retoma uma funcionalidade em andamento
antes de iniciar outra e relê a fila após cada conclusão, para que novos itens
pendentes acrescentados possam entrar na execução. Ele realiza as etapas de SDD,
implementação, verificação, revisão e correção dentro dos requisitos confirmados.
Invocar `auto-dev` ativa sua automação independentemente de `workflow.auto_next`
e não altera essa configuração.

Ambos os comandos compartilham `worktree-for-codexspec-auto-dev` no branch
`codexspec/auto-dev`. Eles podem operar simultaneamente sob as proteções
compartilhadas de titularidade e escrita; os requisitos são desenvolvidos
sequencialmente nesse espaço de trabalho. Decisões de produto que não podem ser
resolvidas a partir dos requisitos confirmados interrompem a execução com
evidências, em vez de gerar perguntas durante a execução autônoma normal.

Inspecione o blueprint compartilhado atual sem alterá-lo:

```bash
codexspec show-blueprint
```

## Desenvolvimento com worktrees

Um worktree Git é outro diretório de trabalho do mesmo repositório, com seu próprio
branch em checkout. Por padrão, o CodexSpec usa um por funcionalidade comum,
criando-o antes da primeira gravação de requisitos e mantendo juntos os
documentos, a implementação, os testes e as correções dessa funcionalidade.

```text
projects/
├── my-project/
└── my-project-codexspec-worktrees/
    ├── <feature-id>-task-reminders/
    ├── <feature-id>-search/
    ├── worktree-for-codexspec-maintenance/
    └── worktree-for-codexspec-auto-dev/
```

Continuar uma funcionalidade reutiliza seu espaço de trabalho. Alterações
independentes de configuração, Constituição do Projeto e perfil usam o worktree
de manutenção; alterações feitas em uma funcionalidade ativa permanecem ali.
A configuração é **local a cada checkout**: uma configuração alterada em um
worktree selecionado pelo roteamento entra em vigor ali primeiro e chega aos
demais checkouts por meio da integração Git. Execute comandos da CLI e
verificações no espaço de trabalho retornado.

As bases de novas funcionalidades comparam o histórico local com commits e o
histórico remoto obtido do branch principal pela ancestralidade Git. Históricos
divergentes são mesclados dentro do novo worktree e exigem verificação. Uma falha
no fetch gera um aviso e permite referências disponíveis localmente; falhas na
criação não levam à gravação no checkout principal como alternativa.

O padrão de `workflow.worktrees` é **true**; somente o valor YAML literal `false`
desativa o isolamento de funcionalidades comuns e da manutenção.
Blueprint/auto-dev mantêm seu worktree compartilhado fixo em ambos os casos.
A inicialização e as atualizações de instalação operam no checkout que você
seleciona explicitamente. Worktrees concluídos são mantidos; a conclusão não
os mescla nem os exclui automaticamente.

Consulte [Desenvolvimento com worktrees](docs/en/user-guide/workflow.md#worktree-development)
e [configuração](docs/en/reference/configuration.md#workflowworktrees).

## Trabalhar com código existente

Dois pontos de entrada atendem a objetivos diferentes:

| Comando | Use para | Saída/limite |
|---------|-----------|-----------------|
| `onboard [path]` | Iniciar o conhecimento reutilizável do projeto a partir de uma base de código existente | Convenções candidatas e restrições com evidências específicas no perfil; o código permanece somente leitura |
| `reverse-spec [path]` | Entender a arquitetura existente ou comparar o código com a intenção confirmada | Artefatos em rascunho ou um relatório de divergências; o código permanece somente leitura |

```text
/codexspec:onboard src/
/codexspec:reverse-spec
/codexspec:reverse-spec src/auth
```

O Onboard infere convenções a partir do código observável e propõe restrições
somente a partir de proibições explícitas. Convenções candidatas têm efeito local
imediato; restrições candidatas exigem uma decisão na sessão para persistir,
editar ou descartar. Ele preserva o conhecimento existente e não inventa
justificativas de decisões passadas nem armadilhas vivenciadas a partir de uma
análise inicial do código.

O Reverse-spec tem três modos:

- **Visão geral**: sem caminho, ou com a raiz do repositório, produz um
  `design.md` conciso de arquitetura e `slices.md` para escolher módulos a inspecionar.
- **Geração**: um caminho de módulo sem uma base confirmada produz rascunhos
  de `spec.md`, `design.md` e requisitos em aberto/inferidos.
- **Reconciliação**: um módulo com uma base confirmada produz `reconcile.md`,
  relatando comportamento não documentado, especificações não implementadas e
  diferenças semânticas em relação à especificação/projeto técnico confirmados,
  com os requisitos determinando a intenção.

Rascunhos inferidos exigem confirmação humana antes de se tornarem uma base.
A reconciliação informa a direção proposta — corrigir o código, atualizar
documentos ou decidir a intenção — e não a aplica automaticamente.

## Revisão e depuração

Quatro revisores de artefatos verificam fidelidade, cobertura, viabilidade e
qualidade interna: `review-spec`, `review-design`, `review-plan` e `review-tasks`.
Eles são executados automaticamente após a geração e também podem ser invocados
manualmente. Os relatórios distinguem defeitos verificados de recomendações de
risco que não bloqueiam a aprovação e oportunidades de projeto técnico, com
uma pontuação de compatibilidade.

O `review-code` oferece uma verificação separada de defeitos limitada às alterações
como critério de aprovação (gate de defeitos) e uma avaliação explícita da qualidade do código completo:

```text
/codexspec:review-code --feature <feature-dir>
/codexspec:review-code --uncommitted
/codexspec:review-code --audit src/
```

A revisão padrão cobre todas as diferenças do branch da funcionalidade, incluindo
alterações com commit, preparadas, não preparadas e não rastreadas que não estejam
ignoradas. Você pode selecionar explicitamente evidências com commit, sem commit
ou de um único commit. `--feature` acrescenta o contexto dos requisitos sem reduzir
o escopo Git. `--audit` avalia os caminhos indicados e produz uma avaliação consultiva
em vez de um veredito de conclusão.

As revisões carregam padrões compartilhados de `.codexspec/review-code/`,
selecionando dimensões de comportamento relevantes e verificações de linguagem/
framework. Os achados exigem evidências concretas, gatilhos alcançáveis,
atribuição à alteração selecionada e impacto. O revisor relata defeitos e
sugestões de manutenção fundamentadas sem editar arquivos; quem invoca a
correção as verifica de forma independente.

A implementação usa testes primeiro para tarefas de código e implementação
direta com verificações adequadas para documentação/configuração. Após as
correções, uma revisão incremental pode reutilizar a cobertura não afetada;
a aceitação final exige um novo `PASS` para a funcionalidade completa, cobertura
e verificação concluídas e nenhum defeito P0–P3 admitido. Sugestões de manutenção
fundamentadas são relatadas separadamente.

O padrão de `workflow.auto_maintenance` é **true** e controla se quem invoca as
correções também aplica melhorias de manutenção verificadas e compatíveis.
Desativá-lo mantém o relato dessas sugestões e não dispensa defeitos nem
verificações obrigatórias. Ele é independente do avanço entre etapas e não é
um argumento de `implement-tasks`.

Para depuração com investigação da causa raiz primeiro:

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

O Debug segue investigação → análise de padrões → verificação de uma única
hipótese → correção precedida por um teste que falha. A implementação escala
a investigação quando as correções ficam travadas, um defeito não trivial que
afeta a correção do comportamento precisa ser rastreado ou a mesma classe de causa raiz reaparece entre
rodadas de revisão. Três correções malsucedidas acionam uma reavaliação da arquitetura.

Use `checklist` para avaliar clareza, completude e consistência dos requisitos:

```text
/codexspec:checklist Check the authentication requirements for completeness
```

Consulte a [referência de comandos](docs/en/user-guide/commands.md) para seletores
de revisão, argumentos e procedimentos detalhados.

## Conhecimento do projeto

O perfil do projeto armazena conhecimento reutilizável em `.codexspec/profile/`:

| Categoria | Conteúdo |
|----------|----------|
| `constraints/` | Proibições explícitas e limites rígidos, lidos primeiro |
| `conventions/` | Padrões, nomenclatura e orientações entre funcionalidades |
| `pitfalls/` | Armadilhas vivenciadas, causas, soluções alternativas e lições |
| `decisions/` | Decisões reutilizáveis de arquitetura e entre funcionalidades |
| `strategies/` | Sinais que exigem uma abordagem de trabalho diferente |
| `runbooks/` | Procedimentos ordenados e recuperação de falhas |

O `distill` captura conhecimento reutilizável do trabalho; a intenção específica
de uma funcionalidade permanece nos requisitos/projeto técnico/plano dela.
O Init instala orientações em CLAUDE.md e/ou AGENTS.md para ler todas as
restrições e o conhecimento relevante antes de trabalhos substanciais.
Conhecimento acrescentado depois pode ter efeito sem reinicialização.
Registros candidatos são usados com cautela; registros validados exigem
verificação dos resultados e aprovação humana.

```text
/codexspec:distill Capture the reusable lessons from this work
/codexspec:distill review
/codexspec:evolve
```

Um `distill review` manual, ou um `distill` direto sem novo material para capturar,
abre um espaço de trabalho local e offline no navegador. Você pode revisar,
validar, descartar, adiar e consolidar registros, visualizar o Markdown final e
selecionar **Aplicar tudo**. As decisões permanecem em um rascunho recuperável
até a aplicação; verificações de conflito impedem a aplicação parcial ou a
sobrescrita silenciosa. Uma alternativa explícita em texto está disponível para
ambientes sem navegador.

O padrão de `workflow.auto_distill` é **true** e controla três hooks de encerramento:
`implement-tasks` bem-sucedido, commits executados por `commit-staged` e geração
por `pr`. A prévia de commit não aciona a captura.

As orientações instaladas no projeto também pedem que os agentes capturem
conhecimento reutilizável conforme ele surge em conversas comuns, correções
fora de SDD e durante execuções longas de `implement-tasks`. Essas orientações
se aplicam independentemente da configuração de encerramento; a captura ao
final da tarefa fornece uma última salvaguarda.

Dentro de uma sessão, gatilhos repetidos processam somente material novo.
Entre sessões, `distill` lê o perfil e ignora conhecimento já coberto. A captura
encerra sem gravar quando não resta nada reutilizável. A captura automática
nunca abre a revisão manual, espera por uma pessoa ou bloqueia o fluxo de
trabalho que a invocou.

O `evolve` seleciona somente conhecimento validado que seja útil além do projeto,
compila um rascunho de comando/skill e obtém aprovação explícita antes de fazer
push ou abrir um PR de contribuição para revisão humana.

Consulte [Conhecimento do projeto](docs/en/user-guide/commands.md#codexspecdistill)
para orientações detalhadas.

### Reutilizar decisões históricas

O histórico relevante em `.codexspec/specs/` também é consultado antes de
julgamentos substanciais sobre requisitos, projeto técnico, implementação,
depuração ou revisão — tanto em conversas comuns quanto em fluxos de trabalho
SDD. Os agentes reconstroem decisões inalteradas, acréscimos posteriores e
substituições explícitas antes de perguntar ao usuário.

Requisitos antigos inalterados continuam aplicáveis. A decisão explícita mais
recente do usuário sempre prevalece; propostas em aberto não são tratadas como
intenção confirmada. A consulta é limitada à tarefa e o contexto já suficiente
é reutilizado. Renove instalações existentes do projeto para receber essas orientações.

## Fluxo de trabalho Git

```text
/codexspec:commit-staged -p
/codexspec:pr --spec <feature-dir>/spec.md
/codexspec:release-notes --from <ref> --to HEAD
/codexspec:tasks-to-issues <feature-dir>
```

- **commit-staged** analisa a área de preparação exata e gera uma mensagem
  Conventional Commits; `-p` exibe uma prévia sem criar um commit. O fluxo de
  trabalho que o invoca escolhe e prepara os arquivos. A execução autorizada
  usa o ambiente de execução protegido, verificando novamente se o conteúdo
  incluído no commit corresponde à análise. As orientações de commit para
  agentes se aplicam a conversas comuns e fluxos de trabalho SDD, blueprint e
  auto-dev; a disponibilidade do comando por si só não o invoca nem autoriza um commit.
- **pr** gera uma descrição estruturada de PR do GitHub ou MR do GitLab a
  partir das diferenças. `--spec` acrescenta opcionalmente contexto da
  funcionalidade a partir do caminho de um arquivo `spec.md`, ou de um nome
  ou prefixo de diretório de funcionalidade resolvido para esse arquivo.
  A saída padrão é texto para uso na plataforma de hospedagem.
- **release-notes** deriva uma entrada Keep a Changelog e um texto de
  lançamento a partir do histórico Git. A seção padrão é `[Unreleased]`;
  `--version` usa um rótulo fornecido. Ele não prepara arquivos, cria commits,
  incrementa versões, cria tags, publica nem cria um lançamento.
- **tasks-to-issues** cria issues do GitHub a partir de tarefas existentes,
  incluindo dependências e critérios de aceitação. Requer uma CLI do GitHub
  autenticada e verifica se o repositório das issues corresponde ao remoto configurado.

A prévia direta de commits e os commits autorizados no diretório de trabalho
atual requerem Python 3.11+ e Git; o ambiente de execução é instalado com
projetos CLI e incluído no plugin do Claude. Mesclagens criadas pelo agente com
alterações de conteúdo também usam a análise da área de preparação. Mesclagens
apenas de histórico mantêm a mensagem padrão do Git enquanto validam a árvore
e os commits pais; fast-forwards não criam commit.

## Comandos disponíveis

A CLI tem seis comandos públicos. As integrações de agentes distribuem 28
comandos: Claude usa `/codexspec:<name>`, e Codex usa `$codexspec:<name>`.
As tabelas abaixo usam a forma do Claude para facilitar a leitura.

### Comandos da CLI

| Comando | Finalidade |
|---------|---------|
| `codexspec init` | Inicializar ou renovar um projeto para Claude, Codex ou ambos |
| `codexspec check` | Verificar ferramentas e dependências instaladas |
| `codexspec version` | Exibir informações de versão e sistema |
| `codexspec config` | Visualizar ou modificar a configuração do projeto |
| `codexspec list-commands` | Listar comandos de agentes disponíveis por categoria |
| `codexspec show-blueprint` | Exibir o blueprint do worktree compartilhado sem alterá-lo |

### Comandos do fluxo de trabalho principal

| Comando | Finalidade |
|---------|---------|
| `/codexspec:constitution` | Criar/atualizar princípios do projeto com validação entre artefatos |
| `/codexspec:specify` | Discutir, confirmar e persistir requisitos da funcionalidade |
| `/codexspec:blueprint` | Preparar ou manter requisitos pendentes confirmados do blueprint |
| `/codexspec:generate-spec` | Compilar requisitos confirmados em uma especificação rastreável; revisão automática |
| `/codexspec:spec-to-design` | Definir arquitetura, componentes, interfaces e decisões; revisão automática |
| `/codexspec:design-to-plan` | Planejar fases, ordem e verificação da implementação; revisão automática |
| `/codexspec:plan-to-tasks` | Produzir tarefas verificáveis com cobertura dos artefatos anteriores; revisão automática e analyze |
| `/codexspec:implement-tasks` | Executar tarefas, verificar resultados, revisar e corrigir |
| `/codexspec:auto-dev` | Desenvolver requisitos confirmados do blueprint de forma autônoma na ordem do documento |

### Comandos de revisão de artefatos

| Comando | Finalidade |
|---------|---------|
| `/codexspec:review-spec` | Verificar fidelidade e qualidade interna da especificação |
| `/codexspec:review-design` | Verificar fidelidade, viabilidade e prontidão do projeto técnico para planejamento |
| `/codexspec:review-plan` | Verificar fidelidade, viabilidade e prontidão do plano para implementação |
| `/codexspec:review-tasks` | Verificar fidelidade, dependências, executabilidade e verificação das tarefas |

### Requisitos, código existente e depuração

| Comando | Finalidade |
|---------|---------|
| `/codexspec:clarify` | Resolver ambiguidades de requisitos, atualizando os requisitos antes da especificação |
| `/codexspec:analyze` | Verificar rastreabilidade de ponta a ponta e adequar artefatos posteriores à autoridade |
| `/codexspec:checklist` | Gerar uma lista de verificação da qualidade dos requisitos |
| `/codexspec:tasks-to-issues` | Converter tarefas existentes em issues do GitHub prontas para execução |
| `/codexspec:debug` | Investigar causas raiz antes de aplicar uma correção |
| `/codexspec:reverse-spec` | Examinar a arquitetura existente, criar rascunhos de artefatos de módulos ou relatar divergências em relação à base |

### Comandos de conhecimento do projeto

| Comando | Finalidade |
|---------|---------|
| `/codexspec:distill` | Capturar conhecimento reutilizável ou revisar candidatos no espaço de trabalho local |
| `/codexspec:evolve` | Compilar conhecimento validado em um rascunho de contribuição upstream |
| `/codexspec:onboard` | Iniciar convenções candidatas e restrições fundamentadas a partir do código existente |

### Comandos de Git e revisão de código

| Comando | Finalidade |
|---------|---------|
| `/codexspec:commit-staged` | Gerar mensagens a partir de alterações preparadas; exibir prévia ou executar um commit autorizado |
| `/codexspec:pr` | Gerar uma descrição estruturada de PR/MR |
| `/codexspec:release-notes` | Manter uma entrada no changelog e gerar um texto de lançamento a partir do histórico Git |
| `/codexspec:review-code` | Revisar alterações selecionadas como gate de defeitos, detectando defeitos que impedem a aprovação; usar `--audit` para a qualidade dos caminhos |

### Comandos utilitários

| Comando | Finalidade |
|---------|---------|
| `/codexspec:config` | Criar/visualizar/modificar/redefinir a configuração do projeto de forma interativa |
| `/codexspec:quick` | Executar um fluxo de trabalho SDD compacto com requisitos em primeiro lugar para pequenas alterações |

## Configuração e internacionalização

A configuração fica em `.codexspec/config.yml`. Os modelos permanecem em inglês;
os agentes escrevem o texto de interação e os artefatos gerados nos idiomas
configurados. Os 13 códigos de idioma padrão são `en`, `zh-CN`, `zh-TW`, `ja`,
`ko`, `es`, `fr`, `de`, `pt`, `ru`, `it`, `ar` e `hi`.
O código da CLI para português é `pt`; a documentação localizada e os catálogos
de tradução usam `pt-BR`.

### Dimensões de idioma

| Dimensão | Chave de configuração | Na inicialização | Definir depois | Controla |
|-----------|------------|-------------------|-----------|----------|
| Saída/base | `language.output` | `--lang` | `config --set-lang` | Idioma de fallback das demais dimensões de idioma |
| Interação | `language.interaction` | `--interaction-lang` | `config --set-interaction-lang` | Conversa e saída da CLI |
| Documento | `language.document` | `--document-lang` | `config --set-document-lang` | Requisitos, especificações, projetos técnicos, planos e tarefas |
| Commit | `language.commit` | `--commit-lang` | `config --set-commit-lang` | Mensagens de commit e conteúdo de entrega via Git |

Cada idioma específico usa como fallback, de forma independente,
`language.output` e depois `en`. `language.templates` permanece `en`.

```bash
codexspec init my-project --ai both \
  --interaction-lang zh-CN --document-lang en --commit-lang en

codexspec config
codexspec config --set-document-lang en
codexspec config --list-langs
```

A inicialização TTY pela primeira vez solicita o idioma base, a menos que você
forneça `--lang` ou todas as três opções específicas de idioma. `--force` confirma
automaticamente outras solicitações de inicialização; ele não suprime essa seleção
de idioma. A inicialização sem TTY usa inglês por padrão. A reinicialização
preserva as chaves de idioma que você não definiu explicitamente.

### Configurações de fluxo de trabalho e revisão

| Configuração | Padrão | Efeito | Controle pela CLI |
|---------|---------|--------|-------------|
| `workflow.auto_next` | `false` | Avançar etapas comuns de SDD aprovadas | `config --auto-next on\|off` |
| `workflow.auto_distill` | `true` | Capturar conhecimento sem interação após um encerramento bem-sucedido | `config --auto-distill on\|off` |
| `workflow.auto_maintenance` | `true` | Aplicar manutenção incremental verificada durante correções automáticas | `config --auto-maintenance on\|off` |
| `workflow.worktrees` | `true` | Isolar funcionalidades comuns e manutenção independente | `config --worktrees on\|off` |
| `review.decided_by` | `reviewer` | Quem decide sobre achados acionados fora do contexto operacional do projeto | `config --decided-by reviewer\|ask` |

Opções booleanas da CLI aceitam `on/true/1/yes` e `off/false/0/no` sem distinguir
maiúsculas de minúsculas, incluindo espaços em branco ao redor. Uma opção
booleana sem valor alterna o valor atual do checkout de destino; os valores
armazenados em YAML são booleanos.

Com `review.decided_by: reviewer`, o revisor decide a admissão de defeitos.
Com `ask`, um gatilho fora de contexto se torna uma decisão de cenário pendente:
o usuário decide uma vez se deve corrigir o defeito ou excluir esse cenário,
e a decisão confirmada é mantida para rodadas posteriores. Decisões pendentes
bloqueiam a conclusão. Uma execução individual de `review-code` pode substituir
o modo configurado com `--decided-by`.

As gravações de configuração seguem o roteamento de worktrees. Uma alteração
independente a partir do checkout principal é feita no worktree de manutenção
e não altera imediatamente a configuração efetiva do principal; alterações
em um worktree de funcionalidade entram em vigor ali.

<details>
<summary>Opções de inicialização da CLI</summary>

| Opção | Significado |
|--------|---------|
| `PROJECT_NAME` | Nome do novo diretório; use `.` para o diretório atual |
| `--here`, `-h` | Inicializar o diretório atual |
| `--ai`, `-a` | `claude`, `codex` ou `both`; padrão `claude` |
| `--lang`, `-l` | Definir o idioma base da saída |
| `--interaction-lang` | Definir o idioma de interação |
| `--document-lang` | Definir o idioma dos documentos |
| `--commit-lang` | Definir o idioma das mensagens de commit |
| `--force`, `-f` | Regenerar artefatos instalados e confirmar automaticamente solicitações de migração/atualização/conformidade; preservar o contexto escrito para o projeto e as configurações não relacionadas |
| `--no-git` | Pular a inicialização do repositório Git |
| `--debug`, `-d` | Exibir saída detalhada de depuração |

</details>

<details>
<summary>Opções de configuração da CLI</summary>

| Opção | Significado |
|--------|---------|
| `--set-lang`, `-l` | Definir o idioma base da saída |
| `--set-interaction-lang` | Definir o idioma de interação |
| `--set-document-lang` | Definir o idioma dos documentos |
| `--set-commit-lang`, `-c` | Definir o idioma das mensagens de commit |
| `--list-langs` | Listar códigos de idioma aceitos |
| `--auto-next` | Alternar/definir o avanço automático entre etapas |
| `--auto-distill` | Alternar/definir a captura automática de conhecimento |
| `--auto-maintenance` | Alternar/definir a manutenção incremental automática |
| `--worktrees` | Alternar/definir o isolamento por worktree local a cada checkout |
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

Consulte [Configuração](docs/en/reference/configuration.md) e
[Internacionalização](docs/en/user-guide/i18n.md) para detalhes do comportamento
de idiomas e configurações.

## Estrutura do projeto

A inicialização instala recursos comuns e a integração do assistente selecionado:

```text
my-project/
├── .codexspec/
│   ├── config.yml
│   ├── memory/
│   │   └── constitution.md
│   ├── profile/
│   │   ├── constraints/
│   │   ├── conventions/
│   │   ├── pitfalls/
│   │   ├── decisions/
│   │   ├── strategies/
│   │   └── runbooks/
│   ├── review-code/              # Shared review standards
│   ├── specs/
│   │   └── <feature-id>-<name>/   # Added by feature workflows
│   │       ├── requirements.md
│   │       ├── spec.md
│   │       ├── design.md
│   │       ├── plan.md
│   │       ├── tasks.md
│   │       ├── review-*.md
│   │       └── checklists/       # When requested
│   ├── templates/docs/
│   └── scripts/                 # Platform helpers and commit runtime
├── .claude/commands/codexspec/   # --ai claude or both
├── .agents/skills/              # --ai codex or both
├── CLAUDE.md                    # Claude project context
└── AGENTS.md                    # Codex project context
```

O blueprint compartilhado fica no worktree dedicado de auto-dev, em vez de ser
uma cópia editável separada em cada checkout comum. Rascunhos de revisão manual
do conhecimento são excluídos do Git.

## Materiais para extensões

O repositório inclui um modelo de manifesto de extensão, um comando de exemplo
e o [Guia de desenvolvimento de extensões](extensions/EXTENSION-DEVELOPMENT-GUIDE.md).
São materiais de autoria. A CLI atual não tem comandos para instalar/listar/remover
extensões e não carrega automaticamente comandos ou hooks de `extension.yml`.
Os recursos compartilhados de revisão aceitam acréscimos específicos do projeto
em `.codexspec/review-code/`; a inicialização preserva edições existentes dos
recursos e arquivos adicionais, a menos que a substituição seja solicitada.

## Desenvolvimento

```bash
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Development tools are an optional dependency extra
uv sync --extra dev
# For documentation builds too: uv sync --extra dev --extra docs

uv run codexspec --help
uv run pytest
uv run ruff check src/
uv build
```

Leia [CLAUDE.md](CLAUDE.md), [AGENTS.md](AGENTS.md) e a
[Estrutura do repositório](docs/internal/repository-layout.md) antes de alterar
modelos, empacotamento ou inicialização. Cópias de comandos e skills distribuídos
são artefatos de instalação gerados; edite suas fontes oficiais e regenere-os.

## Contribuir

Consulte o [guia de contribuição](docs/en/development/contributing.md) para
orientações de configuração local e contribuição. As contribuições devem
preservar os requisitos confirmados, a rastreabilidade das fontes e o limite de
empacotamento entre usuários e mantenedores.

## Licença

MIT — consulte [LICENSE](LICENSE).

## Agradecimentos

Inspirado no [GitHub spec-kit](https://github.com/github/spec-kit).
Integra-se com Claude Code e OpenAI Codex.

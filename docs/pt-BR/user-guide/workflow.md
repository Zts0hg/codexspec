# Fluxo de trabalho

<a id="core-workflow"></a>

## Fluxo de trabalho principal

O fluxo de trabalho padrão de uma funcionalidade mantém uma sequência de
artefatos ligados por referências às fontes:

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

| Etapa | Comando | Finalidade e resultado |
|------|---------|--------------------|
| Princípios do projeto | `/codexspec:constitution` | Criar ou atualizar `constitution.md` e validar os artefatos afetados |
| Requisitos | `/codexspec:specify <idea>` | Discutir a intenção, confirmar o resumo final e salvar `requirements.md` |
| Especificação | `/codexspec:generate-spec <feature-dir>` | Transformar os requisitos confirmados em `spec.md`, com referências às fontes |
| Projeto técnico do sistema | `/codexspec:spec-to-design <feature-dir>` | Produzir `design.md` com componentes, interfaces e decisões importantes de projeto técnico |
| Plano de implementação | `/codexspec:design-to-plan <feature-dir>` | Produzir `plan.md` com fases, ordem e verificação |
| Tarefas | `/codexspec:plan-to-tasks <feature-dir>` | Produzir tarefas rastreáveis e verificáveis em `tasks.md` e executar a análise entre artefatos |
| Implementação | `/codexspec:implement-tasks <feature-dir>` | Executar as tarefas, verificar os resultados e corrigir os achados da revisão confirmados de forma independente |

Substitua `<feature-dir>` pelo diretório da funcionalidade retornado durante a
descoberta de requisitos. Continue no worktree correspondente ou informe seu
caminho explícito. Assim, os comandos e as sessões continuam trabalhando com a
mesma funcionalidade.

<a id="specify-clarify-and-analyze"></a>

### specify, clarify e analyze

- **specify** inicia ou retoma a descoberta de requisitos. O resumo dos requisitos
  só se torna vinculante após confirmação explícita.
- **clarify** resolve ambiguidades nos requisitos e na especificação existentes,
  com até cinco perguntas por execução, distribuídas em quatro categorias.
  Primeiro atualiza `requirements.md` e depois sincroniza `spec.md`.
- **analyze** verifica toda a sequência requisitos → especificação → projeto
  técnico → plano → tarefas. Aplica automaticamente correções determinísticas aos
  artefatos posteriores quando a correção decorre das fontes anteriores que os
  regem. Nunca edita `requirements.md`. Os achados não resolvidos são relatados.
  A análise é executada automaticamente após uma revisão de tarefas aprovada e
  tem caráter informativo; ela não é um critério de aprovação da implementação.

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

<a id="small-changes-with-quick"></a>

### Pequenas alterações com Quick

Use `quick` para uma alteração pequena e bem delimitada, como uma correção pontual:

```text
/codexspec:quick Fix the empty-state message on the task list
```

O Quick confirma e salva um resumo compacto dos requisitos. Em seguida, coordena
a especificação, o planejamento, as tarefas e a implementação, incluindo as
revisões dos comandos de geração. Alterações amplas ou decisões de produto e
projeto técnico ainda em aberto exigem o fluxo de trabalho padrão. O Quick pausa
quando precisa de uma nova decisão.

<a id="workflow-automation"></a>

### Automação do fluxo de trabalho

O padrão de `workflow.auto_next` é **false**. Se estiver definido como `true` na
configuração do espaço de trabalho ativo, a confirmação final dos requisitos dá
início à especificação. Cada etapa de geração avança após `PASS` ou
`PASS_WITH_WARNINGS`. `NEEDS_REVISION` ou `BLOCKED` interrompe a sequência, que
termina em `implement-tasks`.

A correção automática de artefatos se limita a defeitos verificados cuja solução
decorre de evidências dos artefatos anteriores. São permitidas no máximo duas
rodadas de correção e revisão. As recomendações são tratadas separadamente.
O ciclo de revisão e correção da implementação tem regras próprias de conclusão,
descritas abaixo.

<a id="shared-blueprint-and-autonomous-development"></a>

## Blueprint compartilhado e desenvolvimento autônomo

Use `blueprint` para preparar vários requisitos confirmados antes do
desenvolvimento e `auto-dev` para desenvolver essa fila:

```text
/codexspec:blueprint Add a confirmed requirement for task reminders
/codexspec:auto-dev
```

Na descoberta de requisitos para o blueprint, são definidas a direção, as escolhas
e as restrições que cabem ao usuário, antes que um requisito entre na fila.
O arquivo compartilhado `.codexspec/blueprint.md` usa os estados `pending`,
`in_progress` e `completed`. Você pode acrescentar, substituir, excluir ou
reordenar requisitos pendentes. Entradas ativas e concluídas não podem ser
alteradas pela manutenção do blueprint.

O Auto-dev segue a ordem do documento. Retoma a funcionalidade em andamento antes
de iniciar outra e relê a fila após cada conclusão. Assim, novos requisitos
pendentes acrescentados à fila podem ser incluídos na execução. Ele realiza as
etapas de SDD, implementação, verificação, revisão e correção dentro dos requisitos
confirmados. Chamar `auto-dev` ativa essa automação independentemente de
`workflow.auto_next`, sem alterar essa configuração.

Os dois comandos usam `worktree-for-codexspec-auto-dev` no branch
`codexspec/auto-dev`. Eles podem operar simultaneamente, respeitando as proteções
compartilhadas de controle do espaço de trabalho e de escrita. Nesse espaço, os
requisitos são desenvolvidos em sequência. Quando uma decisão de produto não pode
ser resolvida com base nos requisitos confirmados, a execução é interrompida e
as evidências são apresentadas. Durante a execução autônoma normal, não são
feitas perguntas para resolver essas decisões.

Veja o blueprint compartilhado atual sem alterá-lo:

```bash
codexspec show-blueprint
```

<a id="worktree-development"></a>

## Desenvolvimento com worktrees

Um worktree Git é outro diretório de trabalho do mesmo repositório, com seu próprio
branch selecionado. Por padrão, o CodexSpec usa um worktree por funcionalidade do
fluxo comum. Ele é criado antes de salvar os primeiros requisitos e reúne os
documentos, a implementação, os testes e as correções da funcionalidade.

```text
projects/
├── my-project/
└── my-project-codexspec-worktrees/
    ├── <feature-id>-task-reminders/
    ├── <feature-id>-search/
    ├── worktree-for-codexspec-maintenance/
    └── worktree-for-codexspec-auto-dev/
```

Ao retomar uma funcionalidade, seu espaço de trabalho é reutilizado. Alterações
independentes de configuração, Constituição do Projeto e perfil usam o worktree
de manutenção. Alterações feitas durante uma funcionalidade ativa permanecem no
worktree dela. A configuração é **local a cada checkout**: uma configuração
alterada em um worktree escolhido pelo roteamento entra em vigor primeiro ali
e chega aos outros checkouts pela integração Git. Execute os comandos da CLI e
as verificações no espaço de trabalho retornado.

Para definir a base de uma nova funcionalidade, o histórico já registrado em
commits do branch principal local é comparado ao histórico do branch principal
remoto obtido por fetch, usando a ancestralidade Git. Históricos divergentes são
mesclados no novo worktree e exigem verificação. Se o fetch falhar, um aviso é
emitido e as referências disponíveis localmente podem ser usadas. Se a criação
falhar, o sistema não passa a gravar no checkout principal como alternativa.

O padrão de `workflow.worktrees` é **true**. Somente o valor YAML literal `false`
desativa o isolamento das funcionalidades do fluxo comum e da manutenção.
Blueprint/auto-dev mantêm seu worktree compartilhado fixo em ambos os casos.
A inicialização e as atualizações da instalação ocorrem no checkout selecionado
explicitamente. Worktrees concluídos são mantidos; a conclusão não os mescla
nem os exclui automaticamente.

Consulte [Desenvolvimento com worktrees](workflow.md#worktree-development)
e [configuração](../reference/configuration.md#workflow-and-review-settings).

<a id="work-with-existing-code"></a>

## Trabalhar com código existente

Há dois pontos de entrada para objetivos diferentes:

| Comando | Use para | Resultado e limites |
|---------|-----------|-----------------|
| `onboard [path]` | Formar o conhecimento reutilizável do projeto a partir de uma base de código existente | Convenções candidatas e restrições de escopo delimitado e fundamentadas em evidências no perfil; o código permanece somente leitura |
| `reverse-spec [path]` | Entender a arquitetura existente ou comparar o código com a intenção confirmada | Artefatos em rascunho ou relatório de divergências; o código permanece somente leitura |

```text
/codexspec:onboard src/
/codexspec:reverse-spec
/codexspec:reverse-spec src/auth
```

O Onboard infere convenções a partir do código observável e só propõe restrições
com base em proibições explícitas. Convenções candidatas têm efeito local imediato.
Restrições candidatas exigem uma decisão na sessão: salvar, editar ou descartar.
O conhecimento existente é preservado. Uma análise inicial não serve para inventar
justificativas de decisões anteriores nem relatos de armadilhas vivenciadas.

O Reverse-spec tem três modos:

- **Visão geral**: sem um caminho, ou com a raiz do repositório, produz um projeto
  de arquitetura conciso em `design.md`, além de `slices.md` para escolher os
  módulos que serão examinados.
- **Geração**: um caminho de módulo sem uma base confirmada produz rascunhos de
  `spec.md`, `design.md` e requisitos em aberto ou inferidos.
- **Reconciliação**: um módulo com uma base confirmada produz `reconcile.md`,
  que relata comportamentos não documentados, especificações não implementadas
  e diferenças semânticas em relação à especificação e ao projeto técnico
  confirmados. Os requisitos determinam a intenção.

Rascunhos inferidos precisam de confirmação humana antes de servirem como base.
A reconciliação indica a direção proposta: corrigir o código, atualizar os
documentos ou decidir a intenção. Ela não aplica essa proposta automaticamente.

<a id="review-and-debugging"></a>

## Revisão e depuração

Quatro revisores de artefatos verificam fidelidade, cobertura, viabilidade e
qualidade interna: `review-spec`, `review-design`, `review-plan` e `review-tasks`.
Eles são executados automaticamente após a geração e também podem ser chamados
manualmente. Os relatórios distinguem defeitos verificados de recomendações de
risco que não bloqueiam a aprovação e de oportunidades de melhoria no projeto
técnico. Também incluem uma pontuação de compatibilidade.

O `review-code` oferece uma verificação separada de defeitos nas alterações
selecionadas como critério de aprovação (gate de defeitos), além de uma avaliação
explícita da qualidade de todo o código:

```text
/codexspec:review-code --feature <feature-dir>
/codexspec:review-code --uncommitted
/codexspec:review-code --audit src/
```

Por padrão, a revisão abrange todas as diferenças do branch da funcionalidade:
alterações com commit, na área de preparação, fora da área de preparação e não
rastreadas que não estejam ignoradas. Você pode selecionar explicitamente
alterações com commit, sem commit ou de um único commit como evidência.
`--feature` acrescenta o contexto dos requisitos sem reduzir o escopo Git.
`--audit` avalia os caminhos indicados e produz uma avaliação consultiva, em vez
de um veredito de conclusão.

As revisões carregam padrões compartilhados de `.codexspec/review-code/` e
selecionam as dimensões de comportamento relevantes, além das verificações de
linguagem e framework. Os achados precisam de evidências concretas, condições que
possam ocorrer, atribuição à alteração selecionada e impacto demonstrado.
O revisor relata defeitos e sugestões de manutenção fundamentadas sem editar
arquivos. Quem conduz a correção verifica esses achados de forma independente.

Nas tarefas de código, os testes são escritos primeiro. Tarefas de documentação
e configuração são implementadas diretamente, com as verificações adequadas.
Após as correções, a revisão incremental pode reutilizar a cobertura de revisão
das partes não afetadas. A aceitação final exige um novo `PASS` para a
funcionalidade completa, cobertura e verificação concluídas e nenhum defeito
P0–P3 admitido. As sugestões de manutenção fundamentadas são relatadas separadamente.

O padrão de `workflow.auto_maintenance` é **true**. Essa configuração controla se
quem conduz as correções também aplica melhorias de manutenção verificadas e
compatíveis. Quando ela é desativada, as sugestões continuam sendo relatadas;
os defeitos ainda precisam ser corrigidos e as verificações obrigatórias
continuam sendo exigidas. A configuração é independente do avanço entre etapas
e não é um argumento de `implement-tasks`.

Para uma depuração que começa pela investigação da causa raiz:

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

O Debug segue a sequência investigação → análise de padrões → verificação de
uma única hipótese → correção precedida de um teste que falha. Durante a
implementação, essa investigação é acionada quando as correções não avançam,
um defeito não trivial no comportamento do código precisa ser rastreado
ou a mesma classe de causa raiz reaparece em várias rodadas de revisão.
Após três correções malsucedidas, a arquitetura é reavaliada.

Use `checklist` para avaliar a clareza, a completude e a consistência dos requisitos:

```text
/codexspec:checklist Check the authentication requirements for completeness
```

A [referência de comandos](commands.md) detalha as opções de
seleção da revisão, os argumentos e os procedimentos.

<a id="project-knowledge"></a>

## Conhecimento do projeto

O perfil do projeto armazena conhecimento reutilizável em `.codexspec/profile/`:

| Categoria | Conteúdo |
|----------|----------|
| `constraints/` | Proibições explícitas e limites rígidos; devem ser lidos primeiro |
| `conventions/` | Padrões, nomenclatura e orientações que se aplicam a várias funcionalidades |
| `pitfalls/` | Armadilhas vivenciadas, causas, soluções alternativas e lições |
| `decisions/` | Decisões reutilizáveis de arquitetura e de assuntos comuns a várias funcionalidades |
| `strategies/` | Sinais de que é preciso mudar a abordagem de trabalho |
| `runbooks/` | Procedimentos ordenados e recuperação de falhas |

O `distill` captura conhecimento reutilizável do trabalho. A intenção específica
de cada funcionalidade permanece nos requisitos, no projeto técnico e no plano
dela. O Init instala orientações em CLAUDE.md e/ou AGENTS.md para ler todas as
restrições e o conhecimento relevante antes de realizar trabalho substancial. Conhecimento acrescentado depois pode ter efeito sem uma nova
inicialização. Registros candidatos são usados com cautela. Registros validados
exigem a verificação dos resultados e a aprovação de uma pessoa.

```text
/codexspec:distill Capture the reusable lessons from this work
/codexspec:distill review
/codexspec:evolve
```

Um `distill review` manual, ou um `distill` direto sem novo material para capturar,
abre um espaço de trabalho local e offline no navegador. Nele, você pode revisar,
validar, descartar, adiar e consolidar registros, conferir uma prévia do Markdown
final e selecionar **Aplicar tudo**. Até a aplicação, as decisões ficam em um
rascunho recuperável. As verificações de conflito impedem a aplicação parcial e
a sobrescrita silenciosa. Há uma alternativa explícita em texto para ambientes
sem navegador.

O padrão de `workflow.auto_distill` é **true** e controla três hooks de encerramento:
`implement-tasks` concluído com sucesso, commits executados por `commit-staged`
e geração por `pr`. A prévia de um commit não aciona a captura.

As orientações instaladas no projeto também pedem aos agentes que capturem
conhecimento reutilizável assim que ele surgir: em conversas comuns, em correções
fora de SDD e durante execuções longas de `implement-tasks`. Essas orientações
valem independentemente da configuração de encerramento. A captura ao final da
tarefa funciona como uma última salvaguarda.

Na mesma sessão, acionamentos repetidos processam apenas material novo. Entre
sessões, o `distill` lê o perfil e ignora conhecimento já registrado. Se não
restar nada reutilizável, a captura termina sem gravar. A captura automática nunca abre a revisão manual, não espera por uma pessoa
nem bloqueia o fluxo de trabalho que a chamou.

O `evolve` seleciona apenas conhecimento validado que seja útil além do projeto
e o transforma em um rascunho de comando ou skill. Antes de fazer push ou abrir
um PR de contribuição para revisão humana, obtém aprovação explícita.

Veja mais orientações em [Conhecimento do projeto](commands.md#codexspecdistill).

<a id="reusing-historical-decisions"></a>

### Reutilizar decisões anteriores

Antes de fazer perguntas sobre uma mudança, o agente consulta o histórico das
funcionalidades relacionadas em `.codexspec/specs/`. Ele lê as decisões confirmadas
em `requirements.md`, acompanha os acréscimos posteriores e as substituições
explícitas e, quando necessário, consulta as justificativas do projeto técnico
ou as evidências da implementação. Essa preparação também deve preceder análises
e decisões relevantes sobre projeto técnico, implementação, depuração ou revisão,
tanto em conversas comuns quanto nos fluxos de trabalho SDD.

Os registros de data e hora dos diretórios de funcionalidades ajudam a reconstruir
a ordem das iterações; um documento mais recente não invalida automaticamente uma
decisão anterior. Requisitos anteriores que não foram alterados continuam válidos,
e propostas em aberto não são tratadas como intenção confirmada. A consulta se
concentra na tarefa atual e termina quando há contexto suficiente, que será
reaproveitado nas etapas seguintes.

Por exemplo, ao alterar uma interface, um agente que não consultou o histórico
poderia perguntar:

> “Como esta funcionalidade deve lidar com a compatibilidade com versões anteriores?”

Depois de verificar as decisões relevantes e a implementação atual, ele pode
fazer uma pergunta mais específica:

> “Você havia confirmado que a interface antiga deveria ser mantida, e a
> implementação atual ainda oferece suporte a ela. Sugiro mantê-la nesta mudança.
> Podemos seguir assim?”

Informações já estabelecidas que claramente continuam válidas podem ser
reutilizadas sem repetir a pergunta. Se você já disse “Remova a interface antiga
nesta mudança”, o agente segue essa decisão e explica os impactos da migração.
**Sua decisão explícita mais recente sempre prevalece**; o histórico ajuda a
preparar perguntas mais precisas e evitar repetições.

Atualize as instalações existentes dos projetos para receber essas orientações.

<a id="git-workflow"></a>

## Fluxo de trabalho Git

```text
/codexspec:commit-staged -p
/codexspec:pr --spec <feature-dir>/spec.md
/codexspec:release-notes --from <ref> --to HEAD
/codexspec:tasks-to-issues <feature-dir>
```

- **commit-staged** analisa exatamente a área de preparação e gera uma mensagem
  no padrão Conventional Commits. `-p` mostra uma prévia sem criar um commit.
  O fluxo de trabalho que chama o comando escolhe os arquivos e os adiciona à
  área de preparação. A execução autorizada usa o ambiente de execução protegido
  e confere novamente se o conteúdo incluído no commit corresponde à análise.
  As orientações de commit para agentes se aplicam a conversas comuns e aos
  fluxos SDD, blueprint e auto-dev. A simples disponibilidade do comando não
  significa que ele foi chamado nem autoriza um commit.
- **pr** gera uma descrição estruturada de PR do GitHub ou MR do GitLab a partir
  das diferenças. `--spec` pode acrescentar o contexto da funcionalidade: aceita
  o caminho de um arquivo `spec.md`, ou o nome ou prefixo de um diretório de
  funcionalidade que seja resolvido para esse arquivo. Por padrão, a saída é
  texto para uso na plataforma de hospedagem.
- **release-notes** gera, a partir do histórico Git, uma entrada no formato Keep
  a Changelog e um texto de lançamento. A seção padrão é `[Unreleased]`;
  `--version` usa o rótulo informado. O comando não adiciona arquivos à área de preparação, não cria commits,
  não incrementa versões, não cria tags, não publica e não cria lançamentos.
- **tasks-to-issues** cria issues do GitHub a partir de tarefas existentes,
  incluindo dependências e critérios de aceitação. Requer uma CLI do GitHub
  autenticada e verifica se o repositório das issues corresponde ao remoto configurado.

A prévia direta de commits e os commits autorizados no diretório de trabalho
atual exigem Python 3.11+ e Git. O ambiente de execução é instalado nos projetos
inicializados pela CLI e incluído no plugin do Claude. Mesclagens com alterações
de conteúdo criadas pelo agente também usam a análise da área de preparação.
Mesclagens que apenas unem históricos mantêm a mensagem padrão do Git, mas
validam a árvore e os commits pais. Fast-forwards não criam commit.

## Rastreabilidade e continuação

O arquivo `requirements.md` confirmado rege a intenção da funcionalidade; a cadeia seguinte é `spec.md` → `design.md` → `plan.md` → `tasks.md`, interpretada junto com os princípios aplicáveis do projeto e os fatos verificados do repositório. Requisitos usam IDs estáveis, itens da especificação citam `Sources` e o trabalho posterior cita `Covers`. Um artefato posterior não pode redefinir silenciosamente uma decisão anterior. Conflitos entre fontes de autoridade ou novas decisões de produto precisam ser resolvidos pelo usuário. Funcionalidades antigas sem requisitos informam a ausência da confirmação original; se não houver projeto técnico, usam a alternativa documentada.

Passe um caminho explícito da funcionalidade quando a seleção for ambígua; os comandos não escolhem silenciosamente o diretório mais recente. O diretório pai dos worktrees é definido a partir do repositório principal, mesmo quando o comando é chamado de um subdiretório ou de outro worktree vinculado. Para repositórios bare, ele é um diretório irmão chamado `<bare-repository-name>-codexspec-worktrees`. A manutenção independente usa a branch `codexspec/maintenance`.

Uma preparação de worktree que falha mantém sua identidade para permitir a continuação. Merges de bases divergentes precisam passar pelas verificações do projeto antes de gravar requisitos ou iniciar o desenvolvimento. A inspeção somente leitura mantém sua fonte; os relatórios usam o checkout de saída resolvido. A execução de commits mantém o índice selecionado e nunca transfere as alterações preparadas de main para outro worktree. Se faltarem recursos instalados necessários em um novo worktree, inicialize esse destino antes de continuar.

## Modelo de revisão

As revisões separam três tipos de saída:

- **Defeitos de fidelidade**: conflito com uma fonte autoritativa ou omissão de cobertura exigida.
- **Defeitos intrínsecos**: o artefato é internamente contraditório, inverificável ou inviável.
- **Avisos de risco / oportunidades de design**: melhorias opcionais, sem evidência de um defeito atual.

Todo defeito deve identificar sua evidência, local, divergência, impacto e remediação mínima. Achados com a mesma causa raiz são mesclados. Avisos não afetam status, pontuação nem correções automáticas.

O status da revisão é:

- `PASS`: nenhum defeito crítico, de aviso ou menor.
- `PASS_WITH_WARNINGS`: restam apenas defeitos menores.
- `NEEDS_REVISION`: restam um ou mais avisos.
- `BLOCKED`: um conflito crítico impede a continuação confiável.

A pontuação de compatibilidade é derivada dos mesmos achados classificados, em vez de deduções fixas por seção de template. O status é autoritativo; a pontuação existe para integrações que ainda esperam um número.

## Auto Review limitado

Os comandos de geração executam a revisão correspondente automaticamente. Esta é a disciplina de **revisão baseada em evidências** em ação: eles só podem reparar defeitos com evidência e reavaliar por no máximo duas rodadas. Eles param antes em `PASS` e param para entrada do usuário quando:

- uma fonte autoritativa conflita com outra fonte;
- uma correção mudaria uma intenção confirmada;
- o item restante é consultivo, e não um defeito;
- duas rodadas de reparo já foram usadas.

Comandos manuais `/codexspec:review-*` podem ser executados a qualquer momento para um relatório atualizado.

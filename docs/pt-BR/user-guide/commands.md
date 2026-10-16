<a id="available-commands"></a>

# Comandos disponíveis

A CLI tem seis comandos públicos. As integrações de agentes distribuem 28
comandos: Claude usa `/codexspec:<name>` e Codex usa `$codexspec:<name>`.
As tabelas abaixo usam a forma do Claude para facilitar a leitura.

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

<a id="core-workflow-commands"></a>

## Comandos do fluxo de trabalho principal

| Comando | Finalidade |
|---------|---------|
| `/codexspec:constitution` | Criar ou atualizar os princípios do projeto com validação entre artefatos |
| `/codexspec:specify` | Discutir, confirmar e salvar os requisitos da funcionalidade |
| `/codexspec:blueprint` | Preparar ou manter requisitos confirmados e pendentes do blueprint |
| `/codexspec:generate-spec` | Transformar requisitos confirmados em uma especificação rastreável; revisão automática |
| `/codexspec:spec-to-design` | Definir arquitetura, componentes, interfaces e decisões; revisão automática |
| `/codexspec:design-to-plan` | Planejar as fases, a ordem e a verificação da implementação; revisão automática |
| `/codexspec:plan-to-tasks` | Produzir tarefas verificáveis que cubram os artefatos anteriores; revisão automática e analyze |
| `/codexspec:implement-tasks` | Executar tarefas, verificar resultados, revisar e corrigir |
| `/codexspec:auto-dev` | Desenvolver autonomamente os requisitos confirmados do blueprint, na ordem do documento |

<a id="artifact-review-commands"></a>

## Comandos de revisão de artefatos

| Comando | Finalidade |
|---------|---------|
| `/codexspec:review-spec` | Verificar a fidelidade e a qualidade interna da especificação |
| `/codexspec:review-design` | Verificar a fidelidade, a viabilidade e se o projeto técnico está pronto para o planejamento |
| `/codexspec:review-plan` | Verificar a fidelidade, a viabilidade e se o plano está pronto para a implementação |
| `/codexspec:review-tasks` | Verificar a fidelidade, as dependências, a possibilidade de execução e a verificação das tarefas |

<a id="requirements-existing-code-and-debugging"></a>

## Requisitos, código existente e depuração

| Comando | Finalidade |
|---------|---------|
| `/codexspec:clarify` | Resolver ambiguidades nos requisitos; atualizá-los antes da especificação |
| `/codexspec:analyze` | Verificar a rastreabilidade de ponta a ponta e adequar os artefatos posteriores às fontes que os regem |
| `/codexspec:checklist` | Gerar uma lista de verificação da qualidade dos requisitos |
| `/codexspec:tasks-to-issues` | Converter tarefas existentes em issues do GitHub que orientem sua execução |
| `/codexspec:debug` | Investigar as causas raiz antes de aplicar uma correção |
| `/codexspec:reverse-spec` | Examinar a arquitetura existente, criar rascunhos de artefatos de módulos ou relatar divergências em relação à base |

<a id="project-knowledge-commands"></a>

## Comandos de conhecimento do projeto

| Comando | Finalidade |
|---------|---------|
| `/codexspec:distill` | Capturar conhecimento reutilizável ou revisar registros candidatos no espaço de trabalho local |
| `/codexspec:evolve` | Transformar conhecimento validado em um rascunho de contribuição upstream |
| `/codexspec:onboard` | Extrair do código existente convenções candidatas e restrições fundamentadas |

<a id="git-and-code-review-commands"></a>

## Comandos de Git e revisão de código

| Comando | Finalidade |
|---------|---------|
| `/codexspec:commit-staged` | Gerar mensagens a partir das alterações na área de preparação; mostrar uma prévia ou executar um commit autorizado |
| `/codexspec:pr` | Gerar uma descrição estruturada de PR/MR |
| `/codexspec:release-notes` | Manter uma entrada no changelog e gerar um texto de lançamento a partir do histórico Git |
| `/codexspec:review-code` | Revisar as alterações selecionadas como gate de defeitos; usar `--audit` para avaliar a qualidade do código nos caminhos indicados |

<a id="utility-commands"></a>

## Comandos utilitários

| Comando | Finalidade |
|---------|---------|
| `/codexspec:config` | Criar, consultar, alterar ou redefinir a configuração do projeto de forma interativa |
| `/codexspec:quick` | Executar um fluxo compacto de Requirements-First SDD para pequenas alterações |

As antigas entradas de revisão de Python/React são mantidas por compatibilidade do plugin e não fazem parte do catálogo de 28 comandos instalados. Use `review-code`, que carrega os critérios pertinentes à linguagem ou ao framework, e `--audit` para avaliar caminhos.

## Referência de comandos

### `/codexspec:constitution`

Crie ou atualize a constituição do projeto. A constituição define princípios de arquitetura, pilha de tecnologia, padrões de código e regras de governança que orientam todas as decisões de desenvolvimento subsequentes.

**Sintaxe:**

```
/codexspec:constitution [principles description]
```

**Argumentos:**

| Argumento | Obrigatório | Descrição |
|----------|----------|-------------|
| `principles description` | Não | Descrição de princípios a incluir (será solicitada se não fornecida) |

**O que faz:**

- Cria `.codexspec/memory/constitution.md` se não existir
- Atualiza a constituição existente com novos princípios
- Valida a consistência entre artefatos com os modelos
- Gera um Relatório de Impacto de Sincronização mostrando alterações e arquivos afetados
- Inclui revisão de constitucionalidade dos modelos dependentes

**O que cria:**

```
.codexspec/
└── memory/
    └── constitution.md    # Project governance document
```

**Exemplo:**

```text
You: /codexspec:constitution Focus on code quality, testing standards, and clean architecture

AI:  Creating constitution...

     ✓ Created .codexspec/memory/constitution.md
     Version: 1.0.0

     Sync Impact Report:
     - plan-template-*.md: ✅ aligned
     - spec-template-*.md: ✅ aligned
     - tasks-template-*.md: ✅ aligned

     Core Principles:
     1. Code Quality First
     2. Test-Driven Development
     3. Clean Architecture

     Suggested commit: docs: create constitution v1.0.0
```

**Dicas:**

- Defina os princípios no início do projeto para uma tomada de decisão consistente
- Inclua tanto princípios técnicos quanto de processo
- Revise a constituição antes de desenvolvimentos importantes de funcionalidades
- Alterações na constituição acionam validação entre artefatos

---

### `/codexspec:specify`

Esclareça requisitos por meio de perguntas e respostas interativas, confirme o resumo resultante e guarde-o para sessões futuras.

**Sintaxe:**

```
/codexspec:specify [your idea or requirement]
```

**Argumentos:**

| Argumento | Obrigatório | Descrição |
|----------|----------|-------------|
| `your idea or requirement` | Não | Descrição inicial do que você deseja construir (será solicitada se não fornecida) |

**O que faz:**

- Faz perguntas esclarecedoras para compreender sua ideia
- Explora casos extremos que você pode não ter considerado
- Cocria requisitos de alta qualidade por meio do diálogo
- Concentra-se no "o quê" e "por quê", não na implementação técnica
- Atribui IDs estáveis a necessidades, restrições, decisões, exclusões e perguntas em aberto confirmadas
- Registra evidências do usuário e um log de confirmação
- Cria o workspace da funcionalidade e o `requirements.md`

**O que cria:**

```text
.codexspec/specs/{feature-id}-{feature-name}/requirements.md
```

Somente itens confirmados se tornam requisitos autoritativos. Perguntas em aberto permanecem explicitamente em aberto. Este é o Portão de Confirmação dos requisitos: nada é vinculante até que você confirme explicitamente o resumo final.

**Exemplo:**

```text
You: /codexspec:specify I want to build a task management app

AI:  Great! Let me help you clarify the requirements.

     First, who are the target users for this app?
     - Individual professionals
     - Small teams
     - Enterprise organizations
     - All of the above

You: Small teams, mainly software development teams

AI:  Got it. For small dev teams:
     - Do you need real-time collaboration features?
     - Should tasks support sub-tasks or just flat lists?
     - Any integration requirements (GitHub, Slack, etc.)?

You: Real-time is important. Sub-tasks yes. GitHub integration would be nice.

AI:  [Continues exploring requirements...]

     Summary of clarified requirements:
     - Target: Small dev teams (5-20 people)
     - Core: Tasks with sub-tasks, real-time updates
     - Integration: GitHub (optional)
     - Priority: Real-time collaboration > Sub-tasks > GitHub

     Ready to generate the spec document?
     Use /codexspec:generate-spec to create spec.md
```

**Dicas:**

- Use para exploração inicial de requisitos
- Não se preocupe em ser completo — o refinamento é iterativo
- Faça perguntas se a IA fizer suposições
- Revise o resumo antes de gerar a spec

---

### `/codexspec:blueprint`

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

---

### `/codexspec:generate-spec`

Transformar requisitos confirmados em uma especificação rastreável; revisão automática.

**Sintaxe:**

```
/codexspec:generate-spec
```

**Argumentos:**

| Argumento | Obrigatório | Descrição |
|----------|----------|-------------|
| Caminho da funcionalidade | Não | Diretório explícito da funcionalidade, `requirements.md` ou `spec.md` de destino; obrigatório quando a resolução é ambígua |

**O que faz:**

- Lê os requisitos confirmados do workspace da funcionalidade selecionada
- Suporta workspaces legados que contêm apenas `spec.md`, com um aviso explícito de rastreabilidade
- Gera um `spec.md` abrangente com:
  - Visão geral e objetivos da funcionalidade
  - Histórias de usuário com critérios de aceitação
  - Requisitos funcionais (formato REQ-XXX)
  - Requisitos não funcionais (formato NFR-XXX)
  - Casos extremos e abordagens de tratamento
  - Itens fora do escopo
- Adiciona referências de `Sources` de volta aos IDs de requisitos
- Interrompe para confirmação do usuário em vez de resolver conflitos de autoridade por suposição
- Revisa automaticamente e pode reparar defeitos embasados por evidências por no máximo duas rodadas

**O que cria:**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── spec.md
```

**Exemplo:**

```text
You: /codexspec:generate-spec

AI:  Generating specification...

     ✓ Created .codexspec/specs/2026-0613-1200ab-task-management/spec.md

     Sections included:
     - Overview: Task management for small dev teams
     - 4 User Stories with acceptance criteria
     - 12 Functional Requirements (REQ-001 to REQ-012)
     - 3 Non-Functional Requirements (NFR-001 to NFR-003)
     - 5 Edge Cases documented
     - Out of Scope: Mobile apps, Enterprise SSO

     Next steps:
     - Review the spec with /codexspec:review-spec
     - Or proceed to /codexspec:spec-to-design
```

---

### `/codexspec:spec-to-design`

Lê os arquivos confirmados `requirements.md` e `spec.md`, os princípios do projeto e os fatos relevantes do repositório. Produz `design.md` com componentes, interfaces, fluxo de dados, alternativas e decisões vinculados aos requisitos de origem. Executa `review-design` automaticamente. O fluxo para se uma escolha alterar a intenção confirmada ou exigir uma nova decisão do usuário.

```text
/codexspec:spec-to-design <feature-dir>
```

---

### `/codexspec:design-to-plan`

Converte o design confirmado em um plano de implementação. Execute primeiro `spec-to-design` para definir arquitetura, componentes, interfaces e escolhas tecnológicas.

```text
/codexspec:design-to-plan [design.md | spec.md | feature-directory]
```

Lê `requirements.md`, `spec.md`, `design.md` e a constituição. Planeja fases, ordem e verificação, referenciando o design sem redesenhar o sistema. Cada componente do plano inclui `Covers: REQ-xxx; Design: <design component>`.

Gera `plan.md` e executa `review-plan`. Com `auto_next` ativado, uma revisão aprovada avança para `plan-to-tasks`. Decisões que alterem a intenção confirmada exigem confirmação. Um caminho explícito tem prioridade sobre a branch atual; ambiguidades exigem uma seleção. Funcionalidades antigas sem `design.md` mantêm a possibilidade de planejamento a partir de `spec.md`.

---

### `/codexspec:plan-to-tasks`

Decomponha o plano técnico em tarefas acionáveis, com cobertura explícita e resultados verificáveis.

**Sintaxe:**

```
/codexspec:plan-to-tasks [path_to_spec.md path_to_plan.md]
```

**Argumentos:**

| Argumento | Obrigatório | Descrição |
|----------|----------|-------------|
| `paths` | Não | Caminhos para spec e plano (detectados automaticamente se não fornecidos) |

**O que faz:**

- Cria tarefas com um resultado verificável; uma tarefa pode tocar em vários arquivos relacionados
- Usa ordenação test-first apenas quando exigido pelo plano, constituição, necessidades confirmadas ou risco
- Marca tarefas como `[P]` somente quando são genuinamente independentes
- Especifica caminhos exatos de arquivos para cada tarefa
- Adiciona links `Covers` para o plano e IDs de requisitos

**O que cria:**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── tasks.md    # Task breakdown
```

**Estrutura da tarefa:**

```markdown
### Task 2.1: Write Tests for Entity A [P]
- **Type**: Testing
- **Files**: `tests/test_entity_a.py`
- **Description**: Write unit tests for Entity A
- **Dependencies**: Task 1.3
- **Est. Complexity**: Low
```

**Exemplo:**

```text
You: /codexspec:plan-to-tasks

AI:  Breaking down plan into tasks...

     ✓ Created tasks.md
     Total: 24 tasks
     Parallelizable: 8 tasks (33%)

     Phase 1: Foundation (4 tasks)
     Phase 2: Core Implementation - TDD (10 tasks)
     Phase 3: Integration (4 tasks)
     Phase 4: Interface Layer (3 tasks)
     Phase 5: Testing & Documentation (3 tasks)

     Execution Order:
     Phase 1 → [Phase 2 tasks in parallel groups] → Phase 3 → Phase 4 → Phase 5

     Checkpoints defined at each phase boundary.
```

**Dicas:**

- Cada tarefa deve produzir um resultado verificável e pode tocar em arquivos intimamente relacionados
- Tarefas de teste precedem implementação apenas quando test-first é exigido
- `[P]` marca tarefas paralelizáveis verdadeiramente independentes
- Revise as dependências antes da implementação

Depois de escrever as tarefas, executa-se `review-tasks`. Um resultado `PASS` ou `PASS_WITH_WARNINGS` aciona `analyze` uma vez; a análise não acrescenta uma condição bloqueante à conclusão. As tarefas cobrem os requisitos confirmados, a especificação, o projeto técnico e o plano.

---

### `/codexspec:implement-tasks`

Executar tarefas, verificar resultados, revisar e corrigir.

```text
/codexspec:implement-tasks <feature-dir>
```

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

---

### `/codexspec:auto-dev`

Desenvolver autonomamente os requisitos confirmados do blueprint, na ordem do documento.

Consulte [`blueprint`](#codexspecblueprint).

```text
/codexspec:auto-dev
```

---

### `/codexspec:review-spec`

Valide a especificação em relação aos requisitos confirmados e à sua própria qualidade interna.

**Sintaxe:**

```
/codexspec:review-spec [path_to_spec.md]
```

**Argumentos:**

| Argumento | Obrigatório | Descrição |
|----------|----------|-------------|
| `path_to_spec.md` | Não | Caminho para o arquivo de spec (detectado automaticamente se não fornecido) |

**O que faz:**

- Verifica a fidelidade às entradas confirmadas em `requirements.md`
- Verifica consistência interna, clareza e verificabilidade
- Trata uma seção ausente do modelo como defeito apenas quando o conteúdo autoritativo a exige
- Exige que cada defeito inclua `Evidence`, `Location`, `Mismatch`, `Impact` e `Remediation`
- Separa `Risk Advisories / Design Opportunities` dos defeitos
- Gera um status e uma pontuação de compatibilidade derivada das constatações classificadas

**Contrato compartilhado de revisão:**

| Categoria | Significado |
|----------|---------|
| Defeito de fidelidade | Conflita com ou omite uma fonte autoritativa |
| Defeito intrínseco | Internamente contraditório, inviável ou não verificável |
| Consultivo | Melhoria opcional sem evidência de um defeito atual |

O status é `PASS`, `PASS_WITH_WARNINGS`, `NEEDS_REVISION` ou `BLOCKED`. Achados consultivos nunca alteram status ou pontuação.

**Exemplo:**

```text
You: /codexspec:review-spec

AI:  Overall Status: NEEDS_REVISION
     Compatibility Score: 79/100

     Warning SPEC-001
     Evidence: CON-002 requires a measurable response-time limit.
     Location: spec.md, REQ-006
     Mismatch: "Respond quickly" has no measurable threshold.
     Impact: Acceptance cannot be verified.
     Remediation: Ask the user to confirm a threshold, update requirements.md,
                  then synchronize REQ-006.

     Risk Advisories / Design Opportunities:
     - None
```

**Dicas:**

- Execute antes de `/codexspec:spec-to-design`
- Trate `BLOCKED` e `NEEDS_REVISION` como não prontos para prosseguir
- Não promova achados consultivos a requisitos
- Execute novamente após fazer correções

---

### `/codexspec:review-design`

Revisa a fidelidade e a viabilidade de `design.md`, além de verificar se ele está pronto para orientar o planejamento, com base nos requisitos confirmados e na especificação. Separa defeitos comprovados de melhorias opcionais de projeto e aplica os mesmos estados e limites de correção usados nas demais revisões de artefatos.

```text
/codexspec:review-design <feature-dir>
```

---

### `/codexspec:review-plan`

Revise o plano técnico de implementação quanto a fidelidade, viabilidade e decisões técnicas justificadas.

**Sintaxe:**

```
/codexspec:review-plan [path_to_plan.md]
```

**Argumentos:**

| Argumento | Obrigatório | Descrição |
|----------|----------|-------------|
| `path_to_plan.md` | Não | Caminho para o arquivo de plano (detectado automaticamente se não fornecido) |

**O que faz:**

- Verifica links `Covers` e cobertura exigida da spec
- Verifica regras aplicáveis da constituição e fatos do repositório
- Sinaliza complexidade injustificada apenas quando cria um custo ou conflito concreto
- Exige campos de evidência para todo defeito e mescla constatações com a mesma causa raiz
- Relata melhorias opcionais de arquitetura como achados consultivos
- Usa o contrato compartilhado de status e pontuação de compatibilidade

**Exemplo:**

```text
You: /codexspec:review-plan

AI:  Overall Status: PASS
     Compatibility Score: 100/100
     Verified defects: none

     Risk Advisories / Design Opportunities:
     - A caching layer may become useful if production measurements exceed
       the confirmed latency target. It is not required by the current plan.
```

**Dicas:**

- Execute antes de `/codexspec:plan-to-tasks`
- Resolva defeitos embasados por evidência antes da geração de tarefas
- Mantenha ideias arquiteturais especulativas na seção consultiva
- Verifique se a pilha tecnológica está alinhada com as habilidades da equipe

O plano implementa o `design.md` confirmado, sem reabrir decisões de arquitetura. A revisão verifica as referências do plano ao projeto técnico, além da cobertura dos requisitos.

---

### `/codexspec:review-tasks`

Valide a decomposição de tarefas quanto a cobertura, resultados verificáveis, ordenação correta e dependências viáveis.

**Sintaxe:**

```
/codexspec:review-tasks [path_to_tasks.md]
```

**Argumentos:**

| Argumento | Obrigatório | Descrição |
|----------|----------|-------------|
| `path_to_tasks.md` | Não | Caminho para o arquivo de tarefas (detectado automaticamente se não fornecido) |

**O que faz:**

- Verifica se todos os itens exigidos do plano e os requisitos têm cobertura de tarefas
- Valida a ordenação test-first apenas onde uma fonte autoritativa a exige
- Verifica se cada tarefa tem um resultado que pode ser conferido
- Valida dependências (sem ciclos, ordenação correta)
- Revisa marcadores de paralelização
- Valida caminhos de arquivo
- Exige campos de evidência para todo defeito
- Relata refinamentos opcionais de processo como achados consultivos
- Usa o contrato compartilhado de status e pontuação de compatibilidade

**Exemplo:**

```text
You: /codexspec:review-tasks

AI:  Overall Status: NEEDS_REVISION
     Compatibility Score: 79/100

     Warning TASK-001
     Evidence: Task 2.5 declares a dependency on Task 2.4.
     Location: tasks.md, Task 2.5
     Mismatch: Task 2.5 is also marked [P].
     Impact: Parallel execution can start before its prerequisite completes.
     Remediation: Remove [P] or remove the dependency if the plan proves independence.
```

**Dicas:**

- Execute antes de `/codexspec:implement-tasks`
- Achados de ordenação de testes são defeitos apenas quando testes são exigidos por uma fonte autoritativa
- Verifique se os marcadores de paralelização estão corretos
- Confirme se os caminhos de arquivo correspondem à estrutura do projeto

---

### `/codexspec:clarify`

Examine uma especificação existente em busca de ambiguidades e lacunas. Use para refinamento iterativo após a criação inicial da spec.

**Sintaxe:**

```
/codexspec:clarify [path_to_spec.md]
```

**Argumentos:**

| Argumento | Obrigatório | Descrição |
|----------|----------|-------------|
| `path_to_spec.md` | Não | Caminho para o arquivo de spec (detectado automaticamente se não fornecido) |

**O que faz:**

- Examina requisitos e spec usando categorias focadas de ambiguidade
- Faz perguntas direcionadas de esclarecimento (no máximo 5)
- Atualiza `requirements.md` primeiro após confirmação do usuário, depois sincroniza `spec.md`
- Integra-se às constatações do review-spec quando disponíveis

**Categorias de ambiguidade:**

| Categoria | O que detecta |
|----------|-----------------|
| **Lacunas de completude** | Seções ausentes, conteúdo vazio, critérios de aceitação inexistentes |
| **Problemas de especificidade** | Termos vagos ("rápido", "escalável"), restrições indefinidas |
| **Clareza comportamental** | Lacunas no tratamento de erros, transições de estado indefinidas |
| **Problemas de mensurabilidade** | Requisitos não funcionais sem métricas |

**Exemplo:**

```text
You: /codexspec:clarify

AI:  Scanning spec.md for ambiguities...

     Found issues in 3 categories.

     ## Question 1/5: Specificity

     **Context**: NFR-001 states "System should respond quickly"

     **Question**: What is the target response time?

     | Option | Description | Impact |
     |--------|-------------|--------|
     | A | < 100ms for all operations | High performance requirement |
     | B | < 500ms for reads, < 1s for writes | Balanced approach |
     | Custom | Provide a different answer | - |

     **Recommendation**: Option B - balanced for typical web app

You: B

AI:  ✓ Updated NFR-001: Response time < 500ms reads, < 1s writes
     Added to Clarifications section in spec.md
```

**Dicas:**

- Use quando spec.md existe, mas precisa de refinamento
- Integra-se às constatações de `/codexspec:review-spec`
- No máximo 5 perguntas por execução
- Execute várias vezes para especificações complexas

---

### `/codexspec:analyze`

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

Se uma funcionalidade antiga não tiver `requirements.md`, a análise começa em `spec.md`, informa a ausência de evidências da discussão original e apenas relata os resultados, sem modificar artefatos. A falta de um `design.md` antigo também não impede a análise.

---

### `/codexspec:checklist`

Gere checklists de qualidade para validar completude, clareza e consistência dos requisitos. São "testes de unidade para a escrita de requisitos".

**Sintaxe:**

```
/codexspec:checklist [focus_area]
```

**Argumentos:**

| Argumento | Obrigatório | Descrição |
|----------|----------|-------------|
| `focus_area` | Não | Foco de domínio (ex.: "ux", "api", "security", "performance") |

**O que faz:**

- Gera checklists organizadas por dimensões de qualidade
- Cria checklists no diretório `FEATURE_DIR/checklists/`
- Itens focam em qualidade de requisitos, não em testes de implementação

**Dimensões de qualidade:**

- **Completude dos requisitos**: Todos os requisitos necessários estão presentes?
- **Clareza dos requisitos**: Os requisitos são específicos e inequívocos?
- **Consistência dos requisitos**: Os requisitos estão alinhados sem conflitos?
- **Qualidade dos critérios de aceitação**: Os critérios de sucesso são mensuráveis?
- **Cobertura de cenários**: Todos os fluxos/casos foram tratados?
- **Cobertura de casos extremos**: As condições de contorno estão definidas?
- **Requisitos não funcionais**: Desempenho, segurança, acessibilidade especificados?
- **Dependências e premissas**: Estão documentadas?

**Exemplos de tipos de checklist:**

- `ux.md` - Hierarquia visual, estados de interação, acessibilidade
- `api.md` - Formatos de erro, limitação de taxa, autenticação
- `security.md` - Proteção de dados, modelo de ameaças, resposta a vazamentos
- `performance.md` - Métricas, condições de carga, degradação

**Exemplo:**

```text
You: /codexspec:checklist security

AI:  Generating security checklist...

     ✓ Created .codexspec/specs/2026-0613-1200ab-task-management/checklists/security.md

     ## Security Requirements Quality Checklist

     ### Authentication Requirements
     - [ ] CHK001 - Are authentication requirements defined for all protected endpoints? [Completeness]
     - [ ] CHK002 - Is password complexity explicitly specified? [Clarity]
     - [ ] CHK003 - Are session timeout requirements quantified? [Measurability]

     ### Data Protection
     - [ ] CHK004 - Are data encryption requirements specified at rest? [Completeness]
     - [ ] CHK005 - Are data encryption requirements specified in transit? [Completeness]
     - [ ] CHK006 - Is PII handling explicitly documented? [Clarity]

     Total: 15 items across 4 categories
```

**Dicas:**

- Checklists validam qualidade dos requisitos, não corretude da implementação
- Use para revisão e melhoria de requisitos
- Crie checklists específicas de domínio para validação focada
- Execute antes de prosseguir para o planejamento técnico

---

### `/codexspec:tasks-to-issues`

Converta tarefas de `tasks.md` em Issues do GitHub para acompanhamento e colaboração no projeto.

**Sintaxe:**

```
/codexspec:tasks-to-issues
```

**Argumentos:**

| Argumento | Obrigatório | Descrição |
|----------|----------|-------------|
| Nenhum | - | Converte todas as tarefas da funcionalidade atual |

**O que faz:**

- Analisa IDs de tarefas, descrições, dependências e caminhos de arquivo
- Cria Issues do GitHub com corpo estruturado
- Adiciona rótulos com base no tipo de tarefa (setup, implementation, testing, documentation)
- Vincula dependências entre issues
- Relata as issues criadas com URLs

**Pré-requisitos:**

- Repositório Git com remote no GitHub
- GitHub CLI (`gh`) instalado e autenticado
- Arquivo `tasks.md` existente

**Exemplo:**

```text
You: /codexspec:tasks-to-issues

AI:  Converting tasks to GitHub issues...

     Repository: github.com/example/taskman

     Creating issues:
     ✓ #42: Task 1.1 - Setup Project Structure (setup)
     ✓ #43: Task 2.1 - Write Tests for Task Entity (testing)
     ✓ #44: Task 2.2 - Implement Task Entity (implementation)
     ...

     Summary:
     - Issues created: 24
     - Labels applied: setup(4), implementation(12), testing(5), documentation(3)
     - Dependencies linked: 18

     View issues: https://github.com/example/taskman/issues
```

**Dicas:**

- Requer autenticação no GitHub CLI (`gh auth login`)
- Funciona apenas com repositórios do GitHub
- Cria issues na configuração padrão do repositório
- Verifique duplicatas antes de executar

Antes de criar issues, confira o repositório de destino com seu remoto e obtenha autorização explícita. Gerar uma lista de tarefas, por si só, não autoriza a publicação.

---

### `/codexspec:debug`

Investigar as causas raiz antes de aplicar uma correção.

Consulte [Fluxo de trabalho](workflow.md#review-and-debugging).

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

---

### `/codexspec:reverse-spec`

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

---

### `/codexspec:distill`

Captura conhecimento reutilizável entre funcionalidades em `.codexspec/profile/` e revisa candidatos pendentes sem editar à mão seus arquivos Markdown.

**Sintaxe:**

```text
/codexspec:distill [interaction segment]
/codexspec:distill review
```

**Revisão manual:**

- `/codexspec:distill review`, ou uma invocação direta sem novo segmento a extrair, abre uma página HTML offline servida apenas de `127.0.0.1`. Seu cabeçalho identifica o diretório do projeto em que a sessão vai gravar, para que duas revisões abertas ao mesmo tempo não possam ser confundidas.
- A página oferece revisão estruturada, aprovação, descarte, adiamento, consolidação, um resumo completo do que está preparado e um **Aplicar tudo** explícito. Uma revisão ou fusão precisa exibir sua pré-visualização final exata em Markdown antes que a mesma ação possa ser preparada; a página informa em qual dos três estados de pré-visualização cada registro está — sem pré-visualização, correspondendo às edições atuais, ou alterado após a pré-visualização — antes de você usar um controle de decisão.
- Toda ação que remove arquivos de registro pede uma segunda confirmação declarando sua consequência: o descarte informa o arquivo que será excluído ao aplicar, a fusão informa quantos registros membros serão excluídos, e o descarte do rascunho informa quantas decisões preparadas serão perdidas.
- Um registro só se torna `vetted` com aprovação humana **e** evidência de verificação baseada em resultado. A página mostra, antes de você escolher aprovar, se as evidências salvas já atendem a esse requisito.
- A fila agrupa os registros de acordo com as decisões já tomadas e mostra quantos dos pendentes já estão resolvidos. Preparar uma decisão avança para o próximo registro sem decisão; uma opção no cabeçalho desativa esse avanço automático.
- A página é operável pelo teclado — pressione `?` para ver as teclas. Nenhuma tecla isolada aplica o lote, cancela a sessão ou descarta o rascunho.
- As decisões preparadas usam um rascunho de projeto recuperável e excluído do Git. Apenas uma revisão com permissão de gravação fica ativa por projeto.
- Um rascunho estruturalmente danificado é preservado com um diagnóstico acionável e só é removido por uma ação de descarte explícita.
- Ao aplicar, os hashes de origem são verificados novamente e todo o lote é rejeitado se algum registro mudou; nunca sobrescreve uma edição concorrente nem relata sucesso parcial.
- Todos os recursos da página são distribuídos com o CodexSpec. A página não usa CDN, chamada a modelo remoto nem telemetria.
- Se nenhum navegador puder ser aberto, o comando imprime a URL local protegida por token. Solicite o modo de texto explícito quando um navegador não for adequado; ele usa a mesma validação e o mesmo caminho de gravação.

A destilação automática permanece não interativa e não bloqueante: nunca abre a página, nunca inicia a revisão em texto e nunca espera por um rascunho salvo.

---

### `/codexspec:evolve`

O `evolve` seleciona apenas conhecimento validado que seja útil além do projeto
e o transforma em um rascunho de comando ou skill. Antes de fazer push ou abrir
um PR de contribuição para revisão humana, obtém aprovação explícita.

```text
/codexspec:evolve
```

---

### `/codexspec:onboard`

Extrair do código existente convenções candidatas e restrições fundamentadas.

Consulte [`reverse-spec`](#codexspecreverse-spec).

```text
/codexspec:onboard src/
```

---

### `/codexspec:commit-staged`

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

O helper compartilhado `.codexspec/scripts/commit-staged-helper.py` (ou a cópia incluída no plugin) exige Python 3.11+ e Git, não chama nenhum LLM, preserva os Git hooks e rejeita conteúdo preparado que tenha mudado após a análise. A inicialização de uso único fornece esse runtime; o roteamento de espaços de trabalho, blueprint e auto-dev continuam exigindo a CLI.

---

### `/codexspec:pr`

Gere uma descrição estruturada de Pull Request do GitHub / Merge Request do GitLab a partir do git diff. Integra opcionalmente o `spec.md` para contexto rastreável por SDD.

**Sintaxe:**

```
/codexspec:pr [--target-branch <branch>] [--sections <list>] [--spec <id-or-path>] [--output <file>]
```

**Argumentos:**

| Argumento | Obrigatório | Descrição |
|----------|----------|-------------|
| `--target-branch <branch>` | Não | Branch para comparar (padrão: `origin/main`) |
| `--sections <list>` | Não | Subconjunto separado por vírgulas de `summary, changes, testing, verify, checklist, notes` (padrão: `all`) |
| `--spec <id-or-path>` | Não | Integração opt-in de spec: um ID de funcionalidade (ex.: `2025-0321-1430k7-auth`) resolvido em `.codexspec/specs/`, ou um `path/to/spec.md` explícito. Omita para gerar apenas a partir do git |
| `--output <file>` | Não | Salvar a descrição em um arquivo em vez do terminal |

**O que faz:**

- Coleta contexto do git (branch atual, URL do remote, commits à frente, alterações de arquivos, diff completo, mensagens de commit) em relação ao branch de destino
- Detecta automaticamente a plataforma pela URL do remote: GitHub → "Pull Request", GitLab → "Merge Request", outro/nenhum → usa a terminologia do GitHub e apresenta um aviso
- Carrega `.codexspec/memory/constitution.md` quando presente e alinha a descrição com padrões de documentação/revisão de código
- Usa `language.commit` (depois `language.output`, depois inglês) para o idioma da descrição; termos técnicos (API, JWT, PR, MR) permanecem em inglês quando apropriado
- Quando `--spec` é fornecido, adiciona uma seção Contexto com histórias de usuário e requisitos extraídos de spec.md; caso contrário, gera puramente a partir do diff
- Emite seções conforme `--sections` (Resumo, Alterações, Testes, Passos de Verificação, Checklist pré-merge, Notas / Breaking Changes)

**Exemplo:**

```text
You: /codexspec:pr --spec 2026-0613-1200ab-task-management

AI:  Generating Pull Request description...

     Platform: GitHub (github.com/example/taskman)
     Branch:   feature/task-management  →  origin/main
     Commits:  8 ahead

     ## Pull Request: Task management for small dev teams

     ### Context
     - User stories and REQ-* pulled from spec.md

     ### Summary
     - Adds task CRUD, sub-tasks, and real-time updates

     ### Changes
     - src/taskman/models/task.py (new)
     - src/taskman/api/tasks.py (new)
     - ...

     ### Verification Steps
     1. `uv run pytest`
     2. `uv run codexspec check`
```

**Dicas:**

- Omita `--spec` para pequenas correções de bug ou mudanças sem especificação formal
- Combine com `/codexspec:commit-staged` para produzir tanto uma mensagem de commit quanto uma descrição de PR a partir do mesmo trabalho
- Veja o [estudo de caso do gerador de descrição de PR](../case-studies/case-study-pr-description-generator.md) para um exemplo completo de ponta a ponta desse comando (incluindo como o contexto de spec.md é conectado)

---

### `/codexspec:release-notes`

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

#### Opções das notas de versão

| Comandos | Referência |
|---|---|
| `--version <X.Y.Z>` | Rótulo de versão informado; se omitido, `[Unreleased]` |
| `--from <ref>` | Referência inicial; por padrão, última tag alcançável, depois uma versão localizável do changelog e, por fim, todo o histórico |
| `--to <ref>` | Referência final; padrão `HEAD` |
| `--output <file>` | Arquivo para o texto da versão; por padrão, saída no terminal |
| `--spec <feature>` | Contexto opcional da funcionalidade; se ela não for localizada, o problema é informado e a geração continua com Git |

---

### `/codexspec:review-code`

Revisa a alteração Git selecionada como um gate de defeitos rigoroso antes do merge. O alvo padrão inclui a diferença completa da funcionalidade; seletores explícitos escolhem mudanças commitadas, não commitadas ou um único commit, sem aceitar filtros de caminho.

<!-- REVIEW-CODE-BREAKING: DEFAULT-GATE -->
<!-- REVIEW-CODE-BREAKING: PATH-AUDIT -->

**Modo de revisão padrão:**

- O comando padrão agora é um gate de defeitos limitado à alteração, não uma pontuação geral de qualidade.
- Caminhos posicionais não são mais válidos. Use `--audit` explicitamente para a pontuação consultiva de qualidade por caminho.

**Sintaxe do gate de defeitos:**

```text
/codexspec:review-code
/codexspec:review-code --committed [--base <branch>] [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code --uncommitted [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code --commit <sha> [--parent <n>] [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code [--committed] --incremental-from <fingerprint> [--feature <feature-dir>]
```

Toda forma do gate de defeitos também aceita `--decided-by reviewer|ask`, que substitui `review.decided_by` naquela execução.

<!-- REVIEW-CODE-SYSTEM-CONTRACT -->
<!-- REVIEW-CODE-VARIANT-SEARCH -->
<!-- REVIEW-CODE-NEUTRAL-HANDOFF -->

O gate inventaria todos os artefatos selecionados, avalia requisitos aplicáveis e executa cinco fases nesta ordem: Scope, System Contract, Behavior, Risk e Verification. Ele registra contratos entre módulos sustentados por evidências e partições semânticas de revisão; cada causa raiz repetível e validada aciona, antes do fim da rodada, uma busca delimitada por ocorrências relacionadas. As seis seções do relatório são seguidas por um único envelope `<review-code-result>` legível por máquina com `schema_version: "3"`. O envelope transporta a identidade do alvo, a cobertura e obrigações objetivas a serem verificadas novamente após o reparo. O chamador preserva essas obrigações neutras para uma nova revisão completa, sem transmitir o raciocínio do reparo nem conclusões anteriores de correção. O veredito é `PASS`, `FAIL` ou `INCONCLUSIVE`: todo defeito P0-P3 produz `FAIL`; evidência obrigatória ausente ou cobertura incompleta produz `INCONCLUSIVE`.

**Rodadas incrementais.** Depois de um reparo, `--incremental-from <fingerprint>` revisa novamente apenas o que mudou desde aquele resultado anterior: os arquivos alterados, as partições de revisão e os contratos que eles tocam, e as obrigações pendentes. A cobertura dos arquivos inalterados e não afetados é reaproveitada, e o revisor ainda relata qualquer defeito que encontrar em outro lugar. Um `PASS` incremental nunca conclui uma funcionalidade: o `implement-tasks` executa primeiro uma revisão completa, revisões incrementais após cada reparo e, como aceite final, uma nova revisão completa. Os registros da revisão são gravados fora do repositório, no seu diretório de cache de usuário (`~/.cache/codexspec/review/` ou `%LOCALAPPDATA%\codexspec\review\`); na conversa aparecem apenas o relatório e o envelope.

**Modo de decisão.** `review.decided_by` em `.codexspec/config.yml` define quem decide sobre um achado cujo gatilho está fora do contexto real de uso do projeto, como uma entrada que o projeto nunca recebe. Com o padrão `reviewer`, a revisão se comporta exatamente como antes. Com `ask`, a revisão relata esse item como uma decisão de cenário pendente em vez de falhar por ele, e o `implement-tasks` pergunta a você uma única vez: corrigir ou aceitar que o cenário está fora do escopo. Sua resposta é registrada em `requirements.md` como uma entrada `CON` ou `OUT` confirmada, para que rodadas posteriores não a levantem novamente.

```text
You: /codexspec:review-code --feature .codexspec/specs/2026-0714-example

AI:  ## Verdict
     **PASS** — all required review and verification completed with no findings.
```

**Critérios aplicáveis e manutenção.** Cada revisão lê as regras comuns e o modo escolhido, avalia as sete dimensões e carrega detalhes apenas quando o comportamento, contrato ou dependência os torna relevantes. Dependências sem alterações constatações no rastreamento também podem ativar listas de linguagem ou framework. Sugestões de manutenção exigem evidência de um problema atual e uma melhoria local compatível com o comportamento existente. Complexidade futura hipotética e limites de estilo isolados não justificam correções. O resultado de defeitos mantém a versão 3; um `<review-code-maintenance>` separado, de versão 1, relata sugestões ligadas à mesma impressão digital do alvo. A revisão isolada apenas relata. `implement-tasks` verifica e aplica conforme `workflow.auto_maintenance` (padrão `true`). As correções continuam enquanto houver progresso substancial e respeitam os critérios de parada existentes. Não há um limite fixo de rodadas; a aceitação final exige uma nova revisão completa.

As opções booleanas da CLI aceitam `on/true/1/yes` e `off/false/0/no`, sem distinguir
maiúsculas de minúsculas e permitindo espaços em branco ao redor. Uma opção
booleana sem valor alterna o valor atual do checkout de destino. Os valores
armazenados em YAML são booleanos.

`codexspec init` instala os recursos de revisão compartilhados pelo Claude Code e Codex em `.codexspec/review-code/`. `--force` atualiza recursos distribuídos e preserva arquivos de extensão com outros caminhos. Instalar apenas a CLI não cria arquivos de projeto. Com apenas o plugin, se o projeto não tiver a árvore instalada, a revisão usa os mesmos recursos da raiz resolvida pelo host.

<!-- REVIEW-CODE-AUDIT -->

#### Auditoria de qualidade por caminho

O ramo audit explícito revisa o conteúdo atual completo dos arquivos quanto a clareza idiomática, corretude, robustez, arquitetura e alinhamento constitucional. A pontuação é consultiva e não pode concluir `implement-tasks`.

**Sintaxe:**

```
/codexspec:review-code --audit [paths...]
```

**Argumentos:**

| Argumento | Obrigatório | Descrição |
|----------|----------|-------------|
| `path...` | Não | Um ou mais arquivos ou diretórios-fonte para revisar (separados por espaços). O padrão é `src/` se omitido |

**O que faz:**

- Detecta a(s) linguagem(ns) principal(is) pelas extensões de arquivo e executa uma análise por linguagem para alvos com linguagens mistas
- Executa ferramentas de análise estática quando sua configuração está presente (`ruff`/`mypy`, `eslint`/`tsc`, `go vet`/`gofmt`, `cargo check`/`cargo clippy`, `shellcheck`); pula essas verificações e relata cobertura degradada caso contrário
- Pontua quatro dimensões: Clareza Idiomática e Simplicidade, Corretude e Contratos Explícitos, Robustez de Tempo de Execução e Disciplina de Recursos, e Integridade de Arquitetura e Design
- Injeta subseções obrigatórias para frameworks detectados (ex.: Conformidade com Hooks para React, Ownership e Borrowing para Rust, Disciplina de Goroutine e Context para Go, Segurança de Memória e Tempo de Vida para C/C++, Segurança de Execução para Shell)
- Referencia as constatações contra `.codexspec/memory/constitution.md` quando presente; se ausente, o eixo da constituição é descartado e seu peso é redistribuído
- Classifica as constatações por severidade: CRITICAL, HIGH, MEDIUM, LOW (sugestões LOW têm dedução total limitada a 5 pontos)

**Exemplo:**

```text
You: /codexspec:review-code --audit src/

AI:  # Code Review Report

     ## Summary
     - Overall Status: Needs Work
     - Quality Score: 78/100
     - Detected Language: Python

     ## Static Analysis Results
     | Tool   | Status | Issues | Details                |
     |--------|--------|--------|------------------------|
     | ruff   | Warn   | 3      | Unused imports, line length |
     | mypy   | Pass   | 0      | No type errors         |

     ## Detailed Findings
     ### Critical Issues (CRITICAL)
     - [ ] [CODE-001] src/auth/service.py:42 - bare `except Exception:` swallows the original cause
       Impact: Original error context is lost during debugging.
       Suggestion: narrow the exception and re-raise with `raise ... from err`.

     ### Suggestions (LOW)
     - [ ] [CODE-004] src/auth/service.py:120 - manual loop where a comprehension suffices

     ## Recommendations
     1. Priority 1: Fix CODE-001 before merge.
     2. Priority 2: Apply LOW suggestions opportunistically.
```

**Dicas:**

- Passe múltiplos caminhos para revisar uma parte específica, ex.: `src/ tests/`
- A pontuação é consultiva; as constatações CRITICAL/HIGH são o base para decidir o que corrigir

---

### `/codexspec:config`

Gerencie a configuração do projeto de forma interativa (criar/visualizar/modificar/redefinir). Este é o slash command equivalente ao CLI `codexspec config`, ideal para instalações via Plugin Marketplace.

**Sintaxe:**

```
/codexspec:config [--view]
```

**Argumentos:**

| Argumento | Obrigatório | Descrição |
|----------|----------|-------------|
| `--view` | Não | Exibe a configuração atual sem modificá-la. Sem argumentos, abre o menu de gerenciamento interativo |

**O que faz:**

- Tem como alvo exclusivamente `.codexspec/config.yml`
- `--view` (ou a opção de menu "View current config") imprime o arquivo em formato legível; relata "Configuration Not Found" se ausente
- O modo interativo, quando há configuração, oferece: Visualizar, Modificar, Redefinir para padrões, Cancelar
- Se não houver configuração, executa o fluxo de criação que grava uma configuração mínima apenas com `output` (interação/documento/commit resolvem para `output`, depois `en`, então um arquivo apenas com `output` é totalmente funcional)
- Permite definir cada dimensão de linguagem independentemente (output, interaction, document, commit) e alternar opções de fluxo de trabalho como `auto_next`

**O que cria/edita:**

```
.codexspec/config.yml
```

**Exemplo:**

```text
You: /codexspec:config

AI:  ## Configuration Manager

     Configuration file found at .codexspec/config.yml.
     What would you like to do?
     - View current config
     - Modify config
     - Reset to defaults
     - Cancel

You: Modify config

AI:  Select a dimension to change:
     - Output language (base)
     - Interaction language
     - Document language
     - Commit-message language
     - workflow.auto_next
     - workflow.auto_distill
     - workflow.auto_maintenance
     - workflow.worktrees (default on; checkout-local)
     - review.decided_by

You: Output language (base) → zh-CN

AI:  ✓ Updated language.output: "zh-CN"
     (interaction and document fall back to output, then en.)
```

**Dicas:**

- Use `/codexspec:config --view` para inspecionar o estado atual antes de alterar qualquer coisa
- Uma configuração nova ou redefinida grava apenas `output`; defina `interaction`/`document` apenas quando elas devam diferir de `output`
- Para mudanças via script em um terminal, prefira o CLI `codexspec config` (`--set-lang`, `--set-interaction-lang`, `--set-document-lang`, `--set-commit-lang`, `--auto-next`)

O menu interativo também gerencia `workflow.auto_distill`, `workflow.auto_maintenance`, `workflow.worktrees` e `review.decided_by`. As alterações de configuração seguem o roteamento de worktrees e entram em vigor separadamente em cada checkout.

---

### `/codexspec:quick`

Execute um fluxo Requirements-First SDD simplificado para pequenas mudanças.

**Sintaxe:**

```
/codexspec:quick [describe a small requirement]
```

**Argumentos:**

| Argumento | Obrigatório | Descrição |
|----------|----------|-------------|
| `describe a small requirement` | Não | Descrição curta de uma mudança pequena e bem delimitada (será solicitada se não fornecida) |

**O que faz:**

- Avalia o escopo (arquivos afetados, abrangência de módulos, novas dependências, decisões de produto não resolvidas) e, se a mudança for ampla ou tiver múltiplos resultados independentes, recomenda o fluxo padrão
- Cria um workspace da funcionalidade e `requirements.md` usando a mesma convenção de timestamp que `/codexspec:specify`
- Resolve apenas ambiguidades que afetem de forma relevante a implementação; apresenta um resumo confirmado conciso (`NEED-*`, `CON-*`/`DEC-*` relevantes, `OUT-*`, `OPEN-*` não resolvidos)
- Mantém-se no Portão de Confirmação: nada é gerado até você confirmar o resumo
- Encadeia os comandos de geração no novo diretório da funcionalidade: `/codexspec:generate-spec`, `/codexspec:design-to-plan`, `/codexspec:plan-to-tasks`, `/codexspec:implement-tasks`
- Delega ao próprio loop de revisão automática de cada comando de geração; pausa e pergunta ao usuário se uma revisão precisar de uma nova decisão de produto ou arquitetura
- Relata o diretório da funcionalidade, os caminhos dos artefatos, os resultados das revisões, a verificação da implementação e os achados consultivos não resolvidos separadamente

**O que cria:**

```text
.codexspec/specs/{timestamp}-{feature-name}/
├── requirements.md
├── spec.md
├── plan.md
└── tasks.md
```

**Exemplo:**

```text
You: /codexspec:quick Add a "remember me" checkbox to the login form

AI:  Scope check: 1 component, 1 form field, no new dependencies. Quick is appropriate.

     Confirmed requirements:
     - NEED-1: "Remember me" checkbox on the login form (default unchecked)
     - DEC-1: Persist a long-lived refresh token only when checked
     OUT-1: SSO / social login (unchanged)

     Confirm this summary to start the automated flow. [y/N]

You: y

AI:  Running generate-spec → design-to-plan → plan-to-tasks → implement-tasks ...

     ✓ Feature dir: .codexspec/specs/2026-0713-0915ab-remember-me/
     ✓ All reviews PASS_WITH_WARNINGS or higher
     ✓ Implementation verified
     Open advisories: none
```

**Dicas:**

- Reserve Quick para mudanças genuinamente pequenas e de resultado único; caso contrário, execute `/codexspec:specify` e o fluxo padrão
- A confirmação ainda é necessária — Quick nunca infere uma decisão de produto para manter a automação em movimento
- Se qualquer revisão de geração retornar `NEEDS_REVISION`/`BLOCKED`, Quick para e devolve o controle a você

---

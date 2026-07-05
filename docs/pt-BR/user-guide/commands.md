# Comandos

Esta é a referência dos slash commands do CodexSpec. Esses comandos são invocados na interface de chat do Claude Code.

Para padrões de fluxo de trabalho e quando usar cada comando, consulte [Fluxo de trabalho](workflow.md). Para comandos do CLI, consulte [CLI](../reference/cli.md).

## Referência rápida

Agrupados por categoria, espelhando o catálogo do README. Dentro de cada grupo, os comandos aparecem na ordem do fluxo de trabalho.

### Comandos do fluxo de trabalho principal

| Comando | Finalidade |
|---------|---------|
| `/codexspec:constitution` | Criar ou atualizar a constituição do projeto com validação entre artefatos |
| `/codexspec:specify` | Esclarecer, confirmar e persistir requisitos em `requirements.md` |
| `/codexspec:generate-spec` | Gerar o documento `spec.md` a partir dos requisitos esclarecidos (★ Revisão automática) |
| `/codexspec:spec-to-plan` | Converter a especificação em plano técnico de implementação (★ Revisão automática) |
| `/codexspec:plan-to-tasks` | Decompor o plano em tarefas rastreáveis e verificáveis (★ Revisão automática) |
| `/codexspec:implement-tasks` | Executar tarefas com fluxo de trabalho TDD condicional |

### Comandos de revisão (portões de qualidade)

| Comando | Finalidade |
|---------|---------|
| `/codexspec:review-spec` | Validar a especificação quanto a completude e qualidade |
| `/codexspec:review-plan` | Revisar o plano técnico quanto a viabilidade e aderência |
| `/codexspec:review-tasks` | Validar cobertura, ordenação e viabilidade das tarefas |

### Comandos de aprimoramento

| Comando | Finalidade |
|---------|---------|
| `/codexspec:config` | Gerenciar a configuração do projeto de forma interativa (criar/visualizar/modificar/redefinir) |
| `/codexspec:clarify` | Examinar uma spec existente em busca de ambiguidades (4 categorias, no máximo 5 perguntas) |
| `/codexspec:analyze` | Análise de consistência entre artefatos (somente leitura, baseada em severidade) |
| `/codexspec:checklist` | Gerar checklists de qualidade de requisitos |
| `/codexspec:tasks-to-issues` | Converter tarefas em Issues do GitHub |

### Comandos de fluxo de trabalho Git

| Comando | Finalidade |
|---------|---------|
| `/codexspec:commit-staged` | Gerar mensagem de commit a partir das alterações em stage (com consciência do contexto da sessão) |
| `/codexspec:pr` | Gerar descrição de PR/MR a partir do git diff (detecta a plataforma automaticamente) |

### Comandos de revisão de código

| Comando | Finalidade |
|---------|---------|
| `/codexspec:review-code` | Revisar código em qualquer linguagem (clareza idiomática, corretude, robustez, arquitetura) |
| `/codexspec:review-python-code` | Revisar código Python (PEP 8, segurança de tipos, robustez, consistência com a constituição) |
| `/codexspec:review-react-code` | Revisar código React/TypeScript (arquitetura de componentes, regras de Hooks, estado, desempenho) |

### Fast Track

| Comando | Finalidade |
|---------|---------|
| `/codexspec:quick` | Executar um fluxo Requirements-First SDD simplificado para pequenas mudanças |

---

## Categorias de comandos

### Comandos do fluxo de trabalho principal

Comandos para o fluxo de trabalho principal de Requirements-First SDD: Constituição → Requisitos Confirmados → Especificação → Plano → Tarefas → Implementação. Os Requisitos Confirmados são a autoridade de maior prioridade aqui — nada no encadeamento se torna vinculante até que você o confirme explicitamente no Portão de Confirmação.

### Comandos de revisão (portões de qualidade)

Comandos que validam os artefatos em cada estágio do fluxo de trabalho sob um contrato de **revisão baseada em evidências**: todo defeito deve incluir `Evidence`, `Location`, `Mismatch`, `Impact` e `Remediation` concretos. Sugestões consultivas de design são relatadas separadamente e nunca alteram o status nem acionam mudanças automáticas. Defeitos verificados podem ser corrigidos e revisados novamente por no máximo duas rodadas; sugestões consultivas permanecem opcionais do início ao fim.

### Comandos de aprimoramento

Comandos para refinamento iterativo, validação entre artefatos, configuração e integração com gerenciamento de projetos.

### Comandos de fluxo de trabalho Git

Comandos que transformam trabalho concluído em artefatos compartilháveis: mensagens de commit a partir do diff em stage e descrições estruturadas de PR/MR a partir do diff do branch.

### Comandos de revisão de código

Comandos que revisam código-fonte (qualquer linguagem, específico para Python, específico para React/TypeScript) quanto a clareza idiomática, corretude, robustez, arquitetura e aderência à constituição. As descobertas usam a mesma disciplina de severidade das revisões de artefatos: problemas CRITICAL/HIGH devem citar evidência concreta; sugestões LOW são apenas consultivas.

### Fast Track

Um comando simplificado que executa o fluxo Requirements-First SDD de ponta a ponta para mudanças pequenas e bem delimitadas.

---

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
    └── constitution.md    # Documento de governança do projeto
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

Esclareça requisitos por meio de perguntas e respostas interativas, confirme o resumo resultante e persista-o para sessões posteriores.

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

### `/codexspec:generate-spec`

Gere o documento `spec.md` a partir dos requisitos esclarecidos. Este comando atua como um "compilador de requisitos" que transforma seus requisitos esclarecidos em uma especificação estruturada.

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
     - Or proceed to /codexspec:spec-to-plan
```

**Dicas:**

- Execute após `/codexspec:specify` ter esclarecido os requisitos
- Revise a spec gerada antes de prosseguir
- Use `/codexspec:review-spec` para validação de qualidade
- Edite spec.md diretamente se forem necessários pequenos ajustes

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
- Integra-se às descobertas do review-spec quando disponíveis

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
- Integra-se às descobertas de `/codexspec:review-spec`
- No máximo 5 perguntas por sessão
- Execute várias vezes para especificações complexas

---

### `/codexspec:spec-to-plan`

Converta a especificação da funcionalidade em um plano técnico de implementação. É aqui que você define **como** a funcionalidade será construída.

**Sintaxe:**

```
/codexspec:spec-to-plan [path_to_spec.md]
```

**Argumentos:**

| Argumento | Obrigatório | Descrição |
|----------|----------|-------------|
| `path_to_spec.md` | Não | Caminho para o arquivo de spec (detectado automaticamente em `.codexspec/specs/` se não fornecido) |

**O que faz:**

- Lê a especificação e a constituição
- Inclui apenas o detalhamento técnico exigido pelos requisitos confirmados e pelas restrições do repositório
- Verifica as regras aplicáveis da constituição sem tratar convenções opcionais como requisitos da funcionalidade
- Adiciona links `Covers` aos requisitos da especificação
- Documenta decisões técnicas com justificativa
- Interrompe quando uma decisão alteraria a intenção confirmada

**O que cria:**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── plan.md    # Plano técnico de implementação
```

**Exemplo:**

```text
You: /codexspec:spec-to-plan Use Python FastAPI for backend, React for frontend, PostgreSQL for database

AI:  Generating technical plan...

     Constitutionality Review:
     ✓ Clean Architecture: Modular design with clear boundaries
     ✓ TDD: Test-first approach enforced in phases
     ✓ Code Quality: Linting and type hints required

     Architecture:
     - Backend: FastAPI with layered architecture
     - Frontend: React with component structure
     - Database: PostgreSQL with migration strategy

     Module Dependency Graph:
     ┌─────────────┐
     │    API      │
     └──────┬──────┘
            │
     ┌──────▼──────┐
     │  Services   │
     └──────┬──────┘
            │
     ┌──────▼──────┐
     │    Data     │
     └─────────────┘

     ✓ Created plan.md
     5 Implementation Phases defined
```

**Dicas:**

- Execute após a spec ser revisada e estável
- Regras aplicáveis da constituição são obrigatórias; convenções irrelevantes do modelo, não
- Inclua seções relevantes com base no tipo de projeto
- Revise o plano antes de prosseguir para tarefas

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
        └── tasks.md    # Decomposição em tarefas
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

---

### `/codexspec:implement-tasks`

Execute as tarefas de implementação com fluxo de trabalho TDD condicional. Percorre a lista de tarefas de forma sistemática.

**Sintaxe:**

```
/codexspec:implement-tasks [tasks_path]
/codexspec:implement-tasks [spec_path plan_path tasks_path]
```

**Argumentos:**

| Argumento | Obrigatório | Descrição |
|----------|----------|-------------|
| `tasks_path` | Não | Caminho para tasks.md (detectado automaticamente se não fornecido) |
| `spec_path plan_path tasks_path` | Não | Caminhos explícitos para os três documentos |

**Resolução de arquivos:**

- **Sem argumentos**: Detecta automaticamente em `.codexspec/specs/`
- **Um argumento**: Tratado como caminho de `tasks.md`, derivando os outros do mesmo diretório
- **Três argumentos**: Caminhos explícitos para spec.md, plan.md e tasks.md

**O que faz:**

- Lê tasks.md e identifica tarefas incompletas
- Aplica o fluxo TDD para tarefas de código:
  - **Red**: Escrever testes falhos primeiro
  - **Green**: Implementar para passar nos testes
  - **Verify**: Executar todos os testes
  - **Refactor**: Melhorar mantendo os testes no verde
- Implementação direta para tarefas não testáveis (documentos, configuração)
- Atualiza caixas de seleção das tarefas conforme o trabalho avança
- Registra bloqueios em issues.md, se encontrados

**Fluxo TDD para tarefas de código:**

```
Red → Green → Verify → Refactor → Mark Complete
```

**Implementação direta para tarefas não testáveis:**

- Arquivos de documentação
- Arquivos de configuração
- Ativos estáticos
- Arquivos de infraestrutura

**Exemplo:**

```text
You: /codexspec:implement-tasks

AI:  Starting implementation...

     Loading context:
     - spec.md ✓
     - plan.md ✓
     - tasks.md ✓
     - constitution.md ✓

     Tech Stack: Python 3.11+ / FastAPI / PostgreSQL / pytest

     Working on Task 1.1: Setup Project Structure
     ✓ Created src/taskman/__init__.py
     ✓ Created pyproject.toml
     [x] Task 1.1 Complete

     Working on Task 2.1: Write Tests for Task Entity [P]
     ✓ Created tests/test_task.py
     Running tests... 5 passed (all expected failures)
     [x] Task 2.1 Complete

     Working on Task 2.2: Implement Task Entity
     ✓ Created src/taskman/models/task.py
     Running tests... 5 passed
     [x] Task 2.2 Complete

     ...
```

**Dicas:**

- Pode retomar de onde parou, se interrompido
- Bloqueios são registrados em issues.md
- Commits são feitos após tarefas/fases significativas
- Execute `/codexspec:review-tasks` primeiro para validação

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
- Gera um status e uma pontuação de compatibilidade derivada das descobertas classificadas

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

- Execute antes de `/codexspec:spec-to-plan`
- Trate `BLOCKED` e `NEEDS_REVISION` como não prontos para prosseguir
- Não promova achados consultivos a requisitos
- Execute novamente após fazer correções

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
- Exige campos de evidência para todo defeito e mescla descobertas com a mesma causa raiz
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

### `/codexspec:analyze`

Realize uma análise de consistência não destrutiva entre requirements.md, spec.md, plan.md e tasks.md. Identifica conflitos de autoridade, lacunas de rastreabilidade, duplicação e cobertura ausente.

**Sintaxe:**

```
/codexspec:analyze
```

**Argumentos:**

| Argumento | Obrigatório | Descrição |
|----------|----------|-------------|
| Nenhum | - | Analisa os artefatos da funcionalidade atual |

**O que faz:**

- Detecta duplicações entre artefatos
- Identifica ambiguidades sem critérios mensuráveis
- Localiza itens subespecificados
- Verifica alinhamento com a constituição
- Mapeia a cobertura de requisitos para tarefas
- Relata inconsistências em terminologia e ordenação

**Níveis de severidade:**

| Nível | Definição |
|-------|------------|
| **CRITICAL** | Violação da constituição, artefato central ausente, cobertura zero |
| **HIGH** | Requisito duplicado/conflitante, atributo de segurança ambíguo |
| **MEDIUM** | Deriva de terminologia, cobertura não funcional ausente |
| **LOW** | Melhorias de estilo/redação |

**Exemplo:**

```text
You: /codexspec:analyze

AI:  Analyzing artifacts...

     # Specification Analysis Report

     ## Coverage Summary
     | Requirement Key | Has Task? | Task IDs |
     |-----------------|-----------|----------|
     | REQ-001 | ✅ | 2.1, 2.2 |
     | REQ-002 | ✅ | 2.3, 2.4 |
     | REQ-003 | ❌ | None |

     ## Issues Found

     | ID | Category | Severity | Summary |
     |----|----------|----------|---------|
     | A1 | Coverage | CRITICAL | REQ-003 has no task coverage |
     | A2 | Duplication | HIGH | REQ-005 and REQ-008 overlap |
     | A3 | Ambiguity | MEDIUM | NFR-002 "secure" not defined |

     ## Metrics
     - Total Requirements: 12
     - Total Tasks: 24
     - Coverage: 92% (11/12 requirements)
     - Critical Issues: 1

     ## Next Actions
     1. Add tasks for REQ-003 (CRITICAL)
     2. Consider merging REQ-005 and REQ-008
     3. Define "secure" in NFR-002

     Resolve CRITICAL issues before /codexspec:implement-tasks
```

**Dicas:**

- Execute após `/codexspec:plan-to-tasks`, antes da implementação
- Problemas CRITICAL devem bloquear a implementação
- Análise somente leitura — nenhum arquivo é modificado
- Use as descobertas para melhorar a qualidade dos artefatos

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

---

### `/codexspec:commit-staged`

Gere uma mensagem de commit em conformidade com Conventional Commits com base nas alterações em stage do git, com consciência do contexto da sessão. Este comando compreende sua sessão de desenvolvimento para gerar mensagens de commit significativas.

**Sintaxe:**

```
/codexspec:commit-staged [-p]
```

**Argumentos:**

| Argumento | Obrigatório | Descrição |
|----------|----------|-------------|
| `-p` | Não | Modo de pré-visualização — exibe a mensagem sem commitar |

**O que faz:**

- Executa `git diff --staged` para obter as alterações em stage
- Analisa alterações e contexto da sessão para compreensão da intenção
- Segue a especificação Conventional Commits
- No modo de execução (padrão): commita diretamente após gerar a mensagem
- No modo de pré-visualização (`-p`): exibe a mensagem sem commitar
- Relata erro se não houver alterações em stage

**Exemplo:**

```text
You: /codexspec:commit-staged

AI:  Analyzing staged changes...

     Files staged:
     - src/auth/service.py
     - tests/test_auth.py

     Generated commit message:
     feat(auth): implement token refresh logic

     - Add refresh token generation
     - Include token expiration handling
     - Add tests for refresh flow

     Executing commit...

     ✓ Committed: def5678
```

**Exemplo do modo de pré-visualização:**

```text
You: /codexspec:commit-staged -p

AI:  Preview mode - no commit will be executed

     Suggested commit message:
     feat(auth): implement token refresh logic

     - Add refresh token generation
     - Include token expiration handling
     - Add tests for refresh flow
```

**Dicas:**

- Faça stage das alterações primeiro com `git add`
- Analisa apenas o conteúdo em stage — respeita o fluxo de commit em dois estágios do Git
- Considera o contexto da sessão para mensagens de commit significativas
- Use a flag `-p` para pré-visualizar antes de commitar
- Por padrão, segue a especificação Conventional Commits

---

### `/codexspec:review-code`

Revise código em qualquer linguagem quanto a clareza idiomática, corretude, robustez, arquitetura e aderência à constituição.

**Sintaxe:**

```
/codexspec:review-code [path...]
```

**Argumentos:**

| Argumento | Obrigatório | Descrição |
|----------|----------|-------------|
| `path...` | Não | Um ou mais arquivos ou diretórios-fonte para revisar (separados por espaços). O padrão é `src/` se omitido |

**O que faz:**

- Detecta a(s) linguagem(ns) principal(is) pelas extensões de arquivo e executa uma análise por linguagem para alvos com linguagens mistas
- Executa ferramentas de análise estática quando sua configuração está presente (`ruff`/`mypy`, `eslint`/`tsc`, `go vet`/`gofmt`, `cargo check`/`cargo clippy`, `shellcheck`); ignora graciosamente e relata cobertura degradada caso contrário
- Pontua quatro dimensões: Clareza Idiomática e Simplicidade, Corretude e Contratos Explícitos, Robustez de Tempo de Execução e Disciplina de Recursos, e Integridade de Arquitetura e Design
- Injeta subseções obrigatórias para frameworks detectados (ex.: Conformidade com Hooks para React, Ownership e Borrowing para Rust, Disciplina de Goroutine e Context para Go, Segurança de Memória e Tempo de Vida para C/C++, Segurança de Execução para Shell)
- Referencia as descobertas contra `.codexspec/memory/constitution.md` quando presente; se ausente, o eixo da constituição é descartado e seu peso é redistribuído
- Classifica as descobertas por severidade: CRITICAL, HIGH, MEDIUM, LOW (sugestões LOW têm dedução total limitada a 5 pontos)

**Exemplo:**

```text
You: /codexspec:review-code src/

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

- Passe múltiplos caminhos para revisar uma fatia focada, ex.: `src/ tests/`
- A pontuação é consultiva; as descobertas CRITICAL/HIGH são o sinal acionável
- Para projetos apenas Python ou apenas React, prefira `/codexspec:review-python-code` ou `/codexspec:review-react-code` para verificações mais profundas e específicas da linguagem
- Execute novamente após correções para confirmar a recuperação da pontuação (esperado ≥ 95 após resolver problemas CRITICAL/HIGH)

---

### `/codexspec:review-python-code`

Revise código Python quanto a conformidade com PEP 8, segurança de tipos, robustez de engenharia e consistência com a constituição.

**Sintaxe:**

```
/codexspec:review-python-code [path...]
```

**Argumentos:**

| Argumento | Obrigatório | Descrição |
|----------|----------|-------------|
| `path...` | Não | Um ou mais arquivos ou diretórios Python para revisar (separados por espaços). O padrão é `src/` se omitido |

**O que faz:**

- Executa `ruff check` para resultados de PEP 8 / linting e `mypy` para resultados de verificação de tipos
- Revisa quatro dimensões específicas de Python: Princípio Pythonic e KISS, Segurança e Explicitude de Tipos, Robustez de Engenharia e Alinhamento com a Constituição
- Verifica completude de anotações de tipo, tratamento de exceções amplas e preservação de contexto com `raise ... from err`
- Valida gestão de recursos (gerenciadores de contexto `with`), corretude de async/await e disciplina de `logging` estruturado
- Referencia as descobertas contra os princípios MUST/SHOULD de `.codexspec/memory/constitution.md` quando presente
- Classifica as descobertas por severidade: CRITICAL (violações MUST da constituição, bugs de lógica, vulnerabilidades de segurança), HIGH (lacunas de segurança de tipos, erros de ruff/mypy, vazamentos de recursos), MEDIUM (oportunidades de design/refatoração, anotações ausentes), LOW (legibilidade, açúcar sintático Pythonic)

**Exemplo:**

```text
You: /codexspec:review-python-code src/codexspec/

AI:  # Python Code Review Report

     ## Static Analysis
     | Tool  | Status | Issues |
     |-------|--------|--------|
     | ruff  | Pass   | 0      |
     | mypy  | Pass   | 0      |

     ## Findings
     ### Warnings (HIGH)
     - [ ] [CODE-002] src/codexspec/__init__.py:218 - public function missing return type annotation
       Suggestion: add the return type and verify with mypy.

     ### Suggestions (LOW)
     - [ ] [CODE-004] src/codexspec/cli.py:140 - use `pathlib.Path` instead of `os.path` string concatenation
```

**Dicas:**

- Use em vez de `/codexspec:review-code` quando o alvo for apenas Python e você quiser a profundidade de PEP 8 / segurança de tipos
- Tanto `ruff` quanto `mypy` devem estar instalados e configurados no projeto de destino para cobertura completa; o comando relata cobertura degradada quando estiverem ausentes
- Princípios MUST da constituição são pontuados; metaprincípios independentes de linguagem (testabilidade, simplicidade) aplicam-se quando não há constituição

---

### `/codexspec:review-react-code`

Revise código React/TypeScript quanto a arquitetura de componentes, regras de Hooks, gestão de estado, desempenho e consistência com a constituição.

**Sintaxe:**

```
/codexspec:review-react-code [path...]
```

**Argumentos:**

| Argumento | Obrigatório | Descrição |
|----------|----------|-------------|
| `path...` | Não | Um ou mais arquivos ou diretórios React/TypeScript para revisar (separados por espaços; espera-se `.tsx`, `.ts`, `.jsx`, `.js`). O padrão é `src/` se omitido |

**O que faz:**

- Executa `npx eslint` (quando há configuração ESLint) e `npx tsc --noEmit` (quando há `tsconfig.json`)
- Revisa quatro dimensões específicas de React: Atomicidade e Responsabilidade Única do Componente, Conformidade com Hooks e Gestão de Efeitos Colaterais, Gestão de Estado e Fluxo de Dados, e Desempenho e Robustez
- Verifica se os arrays de dependências do `useEffect` são exaustivos, detecta uso indevido de estado-derivado-como-estado e sinaliza efeitos desnecessários
- Procura por riscos de closure obsoleta, limpeza de efeito ausente, prop drilling, renders custosos sem memoização e estados de carregamento/erro ausentes
- Referencia as descobertas contra `.codexspec/memory/constitution.md` quando presente
- Classifica as descobertas por severidade: CRITICAL (violações de regras de Hooks, condições de corrida), HIGH (limpeza ausente, rejeições de promise não tratadas), MEDIUM (candidatos a refatoração), LOW (legibilidade)

**Exemplo:**

```text
You: /codexspec:review-react-code src/components/

AI:  # React Code Review Report

     ## Static Analysis
     | Tool  | Status | Issues |
     |-------|--------|--------|
     | eslint| Warn   | 2      |
     | tsc   | Pass   | 0      |

     ## Findings
     ### Critical Issues (CRITICAL)
     - [ ] [CODE-001] src/components/UserProfile.tsx:38 - `useEffect` missing `userId` in dependency array
       Impact: stale closure fetches the wrong user after navigation.
       Suggestion: add `userId` to the dependency array or extract to a custom hook.

     ### Suggestions (LOW)
     - [ ] [CODE-004] src/components/Button.tsx:12 - extract derived value instead of `useState`
```

**Dicas:**

- Use em vez de `/codexspec:review-code` quando o alvo for apenas React/TypeScript e você quiser profundidade em Hooks/arquitetura de componentes
- Tanto ESLint quanto um `tsconfig.json` devem estar presentes para cobertura completa; o comando relata cobertura degradada quando estiverem ausentes
- As descobertas do React se somam às verificações base de TypeScript, então problemas de segurança de tipos ainda aparecem

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
- Resolve apenas ambiguidades que alterem materialmente a implementação; apresenta um resumo confirmado conciso (`NEED-*`, `CON-*`/`DEC-*` relevantes, `OUT-*`, `OPEN-*` não resolvidos)
- Mantém-se no Portão de Confirmação: nada é gerado até você confirmar o resumo
- Encadeia os comandos de geração contra o novo diretório da funcionalidade: `/codexspec:generate-spec`, `/codexspec:spec-to-plan`, `/codexspec:plan-to-tasks`, `/codexspec:implement-tasks`
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

AI:  Running generate-spec → spec-to-plan → plan-to-tasks → implement-tasks ...

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
- Detecta automaticamente a plataforma pela URL do remote: GitHub → "Pull Request", GitLab → "Merge Request", outro/nenhum → padrão para terminologia do GitHub com aviso
- Carrega `.codexspec/memory/constitution.md` quando presente e alinha a descrição com padrões de documentação/revisão de código
- Honra `language.commit` (depois `language.output`, depois inglês) para o idioma da descrição; termos técnicos (API, JWT, PR, MR) permanecem em inglês quando apropriado
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

You: Output language (base) → zh-CN

AI:  ✓ Updated language.output: "zh-CN"
     (interaction and document fall back to output, then en.)
```

**Dicas:**

- Use `/codexspec:config --view` para inspecionar o estado atual antes de alterar qualquer coisa
- Uma configuração nova ou redefinida grava apenas `output`; defina `interaction`/`document` apenas quando elas devam diferir de `output`
- Para mudanças via script em um terminal, prefira o CLI `codexspec config` (`--set-lang`, `--set-interaction-lang`, `--set-document-lang`, `--set-commit-lang`, `--auto-next`)

---

## Visão geral do fluxo de trabalho

```text
Idea → /specify → requirements.md → /generate-spec → spec.md → /spec-to-plan → plan.md → /plan-to-tasks → tasks.md → /implement
                                                   │                         │                            │
                                              Review spec               Review plan                  Review tasks
```

Cada revisão é um ponto de verificação humano. Valida fidelidade e qualidade intrínseca por meio de descobertas embasadas por evidência. Sugestões consultivas de design permanecem separadas e nunca bloqueiam a progressão. Defeitos verificados podem ser corrigidos e revisados novamente por no máximo duas rodadas.

---

## Solução de problemas

### "Feature directory not found"

O comando não conseguiu localizar o diretório da funcionalidade.

**Soluções:**

- Execute `codexspec init` primeiro para inicializar o projeto
- Verifique se o diretório `.codexspec/specs/` existe
- Confirme se você está no diretório correto do projeto
- Passe um diretório de funcionalidade explícito ou caminho de artefato quando houver múltiplos candidatos

### "No spec.md found"

O arquivo de especificação ainda não existe.

**Soluções:**

- Execute `/codexspec:specify` para esclarecer os requisitos primeiro
- Em seguida execute `/codexspec:generate-spec` para criar spec.md

### "Constitution not found"

Não existe constituição do projeto.

**Soluções:**

- Execute `/codexspec:constitution` para criar uma
- A constituição é opcional, mas recomendada para decisões consistentes

### "Tasks file not found"

A decomposição de tarefas não existe.

**Soluções:**

- Certifique-se de ter executado `/codexspec:spec-to-plan` primeiro
- Em seguida execute `/codexspec:plan-to-tasks` para criar tasks.md

### "GitHub CLI not authenticated"

O comando `/codexspec:tasks-to-issues` requer autenticação no GitHub.

**Soluções:**

- Instale o GitHub CLI: `brew install gh` (macOS) ou equivalente
- Autentique-se: `gh auth login`
- Verifique: `gh auth status`

---

## Próximos passos

- [Fluxo de trabalho](workflow.md) - Padrões comuns e quando usar cada comando
- [CLI](../reference/cli.md) - Comandos de terminal para inicialização do projeto

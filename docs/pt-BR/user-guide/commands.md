# Comandos

Esta é a referência dos comandos slash do CodexSpec. Esses comandos são invocados na interface de chat do Claude Code.

Para padrões de fluxo de trabalho e quando usar cada comando, consulte [Fluxo de Trabalho](workflow.md). Para comandos CLI, consulte [CLI](../reference/cli.md).

## Referência Rápida

| Comando | Propósito |
|---------|-----------|
| `/codexspec.constitution` | Criar ou atualizar a constituição do projeto com validação cruzada de artefatos |
| `/codexspec.specify` | Esclarecer requisitos através de perguntas e respostas interativas |
| `/codexspec.generate-spec` | Gerar documento spec.md a partir dos requisitos esclarecidos |
| `/codexspec.clarify` | Escanear spec existente por ambiguidades (refinamento iterativo) |
| `/codexspec.spec-to-plan` | Converter especificação em plano de implementação técnica |
| `/codexspec.plan-to-tasks` | Dividir o plano em tarefas atômicas com TDD obrigatório |
| `/codexspec.implement-tasks` | Executar tarefas com fluxo de trabalho TDD condicional |
| `/codexspec.review-spec` | Validar especificação para completude e qualidade |
| `/codexspec.review-plan` | Revisar plano técnico para viabilidade e alinhamento |
| `/codexspec.review-tasks` | Validar divisão de tarefas para conformidade com TDD |
| `/codexspec.analyze` | Análise de consistência cruzada de artefatos (somente leitura) |
| `/codexspec.checklist` | Gerar checklists de qualidade de requisitos |
| `/codexspec.tasks-to-issues` | Converter tarefas em issues do GitHub |
| `/codexspec.commit` | Gerar mensagens Conventional Commits com contexto de sessão |
| `/codexspec.commit-staged` | Gerar mensagem de commit a partir de alterações staged |

---

## Categorias de Comandos

### Comandos Principais do Fluxo de Trabalho

Comandos para o fluxo principal SDD: Constituição → Especificação → Plano → Tarefas → Implementação.

### Comandos de Revisão (Portões de Qualidade)

Comandos que validam artefatos em cada etapa do fluxo de trabalho. **Recomendados antes de prosseguir para a próxima etapa.**

### Comandos Avançados

Comandos para refinamento iterativo, validação cruzada de artefatos e integração com gerenciamento de projetos.

---

## Referência de Comandos

### `/codexspec.constitution`

Criar ou atualizar a constituição do projeto. A constituição define princípios arquiteturais, pilha tecnológica, padrões de código e regras de governança que guiam todas as decisões de desenvolvimento subsequentes.

**Sintaxe:**
```
/codexspec.constitution [descrição dos princípios]
```

**Argumentos:**
| Argumento | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `descrição dos princípios` | Não | Descrição dos princípios a incluir (será solicitado se não fornecido) |

**O que faz:**
- Cria `.codexspec/memory/constitution.md` se não existir
- Atualiza a constituição existente com novos princípios
- Valida consistência cruzada de artefatos com templates
- Gera Relatório de Impacto de Sincronização mostrando alterações e arquivos afetados
- Inclui revisão de constitucionalidade para templates dependentes

**O que cria:**
```
.codexspec/
└── memory/
    └── constitution.md    # Documento de governança do projeto
```

**Exemplo:**
```text
Você: /codexspec.constitution Focar em qualidade de código, padrões de teste e arquitetura limpa

AI:  Criando constituição...

     ✓ Criado .codexspec/memory/constitution.md
     Versão: 1.0.0

     Relatório de Impacto de Sincronização:
     - plan-template-*.md: ✅ alinhado
     - spec-template-*.md: ✅ alinhado
     - tasks-template-*.md: ✅ alinhado

     Princípios Principais:
     1. Qualidade de Código em Primeiro Lugar
     2. Desenvolvimento Orientado a Testes
     3. Arquitetura Limpa

     Commit sugerido: docs: criar constituição v1.0.0
```

**Dicas:**
- Defina princípios no início do projeto para decisões consistentes
- Inclua princípios técnicos e de processo
- Revise a constituição antes de grandes desenvolvimentos de funcionalidades
- Mudanças na constituição disparam validação cruzada de artefatos

---

### `/codexspec.specify`

Esclarecer requisitos através de perguntas e respostas interativas. Este comando explora sua ideia inicial sem criar nenhum arquivo — você mantém controle total.

**Sintaxe:**
```
/codexspec.specify [sua ideia ou requisito]
```

**Argumentos:**
| Argumento | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `sua ideia ou requisito` | Não | Descrição inicial do que você quer construir (será solicitado se não fornecido) |

**O que faz:**
- Faz perguntas esclarecedoras para entender sua ideia
- Explora casos de borda que você pode não ter considerado
- Co-cria requisitos de alta qualidade através de diálogo
- Foca em "o quê" e "por quê", não na implementação técnica
- **NÃO gera arquivos** - você decide quando criar documentação

**O que NÃO cria:**
- Nenhum arquivo é criado durante este comando
- Requisitos permanecem na conversa até você aprovar

**Exemplo:**
```text
Você: /codexspec.specify Eu quero construir um app de gerenciamento de tarefas

AI:  Ótimo! Deixe-me ajudar a esclarecer os requisitos.

     Primeiro, quem são os usuários alvo deste app?
     - Profissionais individuais
     - Equipes pequenas
     - Organizações empresariais
     - Todos os acima

Você: Equipes pequenas, principalmente equipes de desenvolvimento de software

AI:  Entendi. Para pequenas equipes de dev:
     - Você precisa de funcionalidades de colaboração em tempo real?
     - As tarefas devem suportar subtarefas ou apenas listas planas?
     - Algum requisito de integração (GitHub, Slack, etc.)?

Você: Tempo real é importante. Subtarefas sim. Integração com GitHub seria legal.

AI:  [Continua explorando requisitos...]

     Resumo dos requisitos esclarecidos:
     - Alvo: Pequenas equipes de dev (5-20 pessoas)
     - Principal: Tarefas com subtarefas, atualizações em tempo real
     - Integração: GitHub (opcional)
     - Prioridade: Colaboração em tempo real > Subtarefas > GitHub

     Pronto para gerar o documento de especificação?
     Use /codexspec.generate-spec para criar spec.md
```

**Dicas:**
- Use para exploração inicial de requisitos
- Não se preocupe em estar completo — o refinamento é iterativo
- Faça perguntas se a AI fizer suposições
- Revise o resumo antes de gerar a spec

---

### `/codexspec.generate-spec`

Gerar o documento `spec.md` a partir dos requisitos esclarecidos. Este comando atua como um "compilador de requisitos" que transforma seus requisitos esclarecidos em uma especificação estruturada.

**Sintaxe:**
```
/codexspec.generate-spec
```

**Argumentos:**
| Argumento | Obrigatório | Descrição |
|-----------|-------------|-----------|
| Nenhum | - | Usa contexto da sessão `/codexspec.specify` anterior |

**O que faz:**
- Cria diretório `.codexspec/specs/{NNN}-{nome-funcionalidade}/`
- Gera `spec.md` abrangente com:
  - Visão geral e objetivos da funcionalidade
  - Histórias de usuário com critérios de aceitação
  - Requisitos funcionais (formato REQ-XXX)
  - Requisitos não-funcionais (formato NFR-XXX)
  - Casos de borda e abordagens de tratamento
  - Itens fora do escopo

**O que cria:**
```
.codexspec/
└── specs/
    └── 001-gerenciamento-tarefas/
        └── spec.md
```

**Exemplo:**
```text
Você: /codexspec.generate-spec

AI:  Gerando especificação...

     ✓ Criado .codexspec/specs/001-gerenciamento-tarefas/spec.md

     Seções incluídas:
     - Visão Geral: Gerenciamento de tarefas para pequenas equipes de dev
     - 4 Histórias de Usuário com critérios de aceitação
     - 12 Requisitos Funcionais (REQ-001 a REQ-012)
     - 3 Requisitos Não-Funcionais (NFR-001 a NFR-003)
     - 5 Casos de Borda documentados
     - Fora do Escopo: Apps móveis, SSO empresarial

     Próximos passos:
     - Revise a spec com /codexspec.review-spec
     - Ou prossiga para /codexspec.spec-to-plan
```

**Dicas:**
- Execute após `/codexspec.specify` ter esclarecido os requisitos
- Revise a spec gerada antes de prosseguir
- Use `/codexspec.review-spec` para validação de qualidade
- Edite spec.md diretamente se ajustes menores forem necessários

---

### `/codexspec.clarify`

Escanear uma especificação existente por ambiguidades e lacunas. Use isto para refinamento iterativo após a criação inicial da spec.

**Sintaxe:**
```
/codexspec.clarify [caminho_para_spec.md]
```

**Argumentos:**
| Argumento | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `caminho_para_spec.md` | Não | Caminho para o arquivo spec (detectado automaticamente se não fornecido) |

**O que faz:**
- Escaneia spec usando 4 categorias focadas de ambiguidade
- Faz perguntas direcionadas de esclarecimento (máximo 5)
- Atualiza spec.md com respostas do esclarecimento
- Integra com descobertas do review-spec se disponível

**Categorias de Ambiguidade:**

| Categoria | O que Detecta |
|-----------|---------------|
| **Lacunas de Completude** | Seções ausentes, conteúdo vazio, critérios de aceitação ausentes |
| **Problemas de Especificidade** | Termos vagos ("rápido", "escalável"), restrições indefinidas |
| **Clareza Comportamental** | Lacunas no tratamento de erros, transições de estado indefinidas |
| **Problemas de Mensurabilidade** | Requisitos não-funcionais sem métricas |

**Exemplo:**
```text
Você: /codexspec.clarify

AI:  Escaneando spec.md por ambiguidades...

     Problemas encontrados em 3 categorias.

     ## Pergunta 1/5: Especificidade

     **Contexto**: NFR-001 afirma "O sistema deve responder rapidamente"

     **Pergunta**: Qual é o tempo de resposta alvo?

     | Opção | Descrição | Impacto |
     |-------|-----------|---------|
     | A | < 100ms para todas as operações | Alto requisito de performance |
     | B | < 500ms para leituras, < 1s para escritas | Abordagem equilibrada |
     | Personalizado | Forneça uma resposta diferente | - |

     **Recomendação**: Opção B - equilibrada para app web típico

Você: B

AI:  ✓ Atualizado NFR-001: Tempo de resposta < 500ms leituras, < 1s escritas
     Adicionado à seção Clarifications em spec.md
```

**Dicas:**
- Use quando spec.md existe mas precisa de refinamento
- Integra com descobertas de `/codexspec.review-spec`
- Máximo de 5 perguntas por sessão
- Execute múltiplas vezes para especificações complexas

---

### `/codexspec.spec-to-plan`

Converter a especificação da funcionalidade em um plano de implementação técnica. É aqui que você define **como** a funcionalidade será construída.

**Sintaxe:**
```
/codexspec.spec-to-plan [caminho_para_spec.md]
```

**Argumentos:**
| Argumento | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `caminho_para_spec.md` | Não | Caminho para o arquivo spec (detectado automaticamente de `.codexspec/specs/` se não fornecido) |

**O que faz:**
- Lê especificação e constituição
- Define pilha tecnológica com restrições de versão
- Realiza revisão de constitucionalidade (obrigatória se constituição existe)
- Cria arquitetura com grafo de dependência de módulos
- Documenta decisões técnicas com racional
- Planeja fases de implementação

**O que cria:**
```
.codexspec/
└── specs/
    └── 001-gerenciamento-tarefas/
        └── plan.md    # Plano de implementação técnica
```

**Exemplo:**
```text
Você: /codexspec.spec-to-plan Usar Python FastAPI para backend, React para frontend, PostgreSQL para banco de dados

AI:  Gerando plano técnico...

     Revisão de Constitucionalidade:
     ✓ Arquitetura Limpa: Design modular com limites claros
     ✓ TDD: Abordagem test-first obrigatória nas fases
     ✓ Qualidade de Código: Linting e type hints obrigatórios

     Arquitetura:
     - Backend: FastAPI com arquitetura em camadas
     - Frontend: React com estrutura de componentes
     - Banco de dados: PostgreSQL com estratégia de migração

     Grafo de Dependência de Módulos:
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

     ✓ Criado plan.md
     5 Fases de Implementação definidas
```

**Dicas:**
- Execute após a spec ser revisada e estável
- Revisão de constitucionalidade é obrigatória se constituição existe
- Inclua seções relevantes com base no tipo de projeto
- Revise o plano antes de prosseguir para tarefas

---

### `/codexspec.plan-to-tasks`

Dividir o plano técnico em tarefas atômicas e acionáveis com TDD obrigatório.

**Sintaxe:**
```
/codexspec.plan-to-tasks [caminho_para_spec.md caminho_para_plan.md]
```

**Argumentos:**
| Argumento | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `caminhos` | Não | Caminhos para spec e plan (detectados automaticamente se não fornecidos) |

**O que faz:**
- Cria tarefas atômicas (um arquivo principal por tarefa)
- Obriga TDD: tarefas de teste precedem tarefas de implementação
- Marca tarefas paralelizáveis com `[P]`
- Especifica caminhos exatos de arquivos para cada tarefa
- Define pontos de verificação de fase

**O que cria:**
```
.codexspec/
└── specs/
    └── 001-gerenciamento-tarefas/
        └── tasks.md    # Divisão de tarefas
```

**Estrutura da Tarefa:**
```markdown
### Task 2.1: Escrever Testes para Entidade A [P]
- **Tipo**: Testing
- **Arquivos**: `tests/test_entity_a.py`
- **Descrição**: Escrever testes unitários para Entidade A
- **Dependências**: Task 1.3
- **Complexidade Est.**: Baixa
```

**Exemplo:**
```text
Você: /codexspec.plan-to-tasks

AI:  Dividindo plano em tarefas...

     ✓ Criado tasks.md
     Total: 24 tarefas
     Paralelizáveis: 8 tarefas (33%)

     Fase 1: Fundação (4 tarefas)
     Fase 2: Implementação Principal - TDD (10 tarefas)
     Fase 3: Integração (4 tarefas)
     Fase 4: Camada de Interface (3 tarefas)
     Fase 5: Testes e Documentação (3 tarefas)

     Ordem de Execução:
     Fase 1 → [Fase 2 tarefas em grupos paralelos] → Fase 3 → Fase 4 → Fase 5

     Pontos de verificação definidos em cada limite de fase.
```

**Dicas:**
- Cada tarefa deve envolver apenas UM arquivo principal
- Tarefas de teste sempre precedem tarefas de implementação
- `[P]` marca tarefas verdadeiramente independentes paralelizáveis
- Revise dependências antes da implementação

---

### `/codexspec.implement-tasks`

Executar tarefas de implementação com fluxo de trabalho TDD condicional. Trabalha através da lista de tarefas sistematicamente.

**Sintaxe:**
```
/codexspec.implement-tasks [caminho_tasks]
/codexspec.implement-tasks [caminho_spec caminho_plan caminho_tasks]
```

**Argumentos:**
| Argumento | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `caminho_tasks` | Não | Caminho para tasks.md (detectado automaticamente se não fornecido) |
| `caminho_spec caminho_plan caminho_tasks` | Não | Caminhos explícitos para todos os três documentos |

**Resolução de Arquivos:**
- **Sem argumentos**: Detecção automática de `.codexspec/specs/`
- **Um argumento**: Trata como caminho `tasks.md`, deriva outros do mesmo diretório
- **Três argumentos**: Caminhos explícitos para spec.md, plan.md e tasks.md

**O que faz:**
- Lê tasks.md e identifica tarefas incompletas
- Aplica fluxo de trabalho TDD para tarefas de código:
  - **Red**: Escrever testes falhando primeiro
  - **Green**: Implementar para passar nos testes
  - **Verify**: Executar todos os testes
  - **Refactor**: Melhorar mantendo testes verde
- Implementação direta para tarefas não testáveis (docs, config)
- Atualiza checkboxes de tarefas conforme o progresso
- Registra bloqueadores em issues.md se encontrados

**Fluxo de Trabalho TDD para Tarefas de Código:**
```
Red → Green → Verify → Refactor → Marcar Completa
```

**Implementação Direta para Não-Testáveis:**
- Arquivos de documentação
- Arquivos de configuração
- Assets estáticos
- Arquivos de infraestrutura

**Exemplo:**
```text
Você: /codexspec.implement-tasks

AI:  Iniciando implementação...

     Carregando contexto:
     - spec.md ✓
     - plan.md ✓
     - tasks.md ✓
     - constitution.md ✓

     Pilha Tecnológica: Python 3.11+ / FastAPI / PostgreSQL / pytest

     Trabalhando na Task 1.1: Setup da Estrutura do Projeto
     ✓ Criado src/taskman/__init__.py
     ✓ Criado pyproject.toml
     [x] Task 1.1 Completa

     Trabalhando na Task 2.1: Escrever Testes para Entidade Task [P]
     ✓ Criado tests/test_task.py
     Executando testes... 5 passaram (todas falhas esperadas)
     [x] Task 2.1 Completa

     Trabalhando na Task 2.2: Implementar Entidade Task
     ✓ Criado src/taskman/models/task.py
     Executando testes... 5 passaram
     [x] Task 2.2 Completa

     ...
```

**Dicas:**
- Pode retomar de onde parou se interrompido
- Bloqueadores são registrados em issues.md
- Commits são feitos após tarefas/fases significativas
- Execute `/codexspec.review-tasks` primeiro para validação

---

### `/codexspec.review-spec`

Validar a especificação para completude, clareza, consistência e prontidão para planejamento técnico.

**Sintaxe:**
```
/codexspec.review-spec [caminho_para_spec.md]
```

**Argumentos:**
| Argumento | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `caminho_para_spec.md` | Não | Caminho para o arquivo spec (detectado automaticamente se não fornecido) |

**O que faz:**
- Verifica completude de todas as seções obrigatórias
- Avalia clareza e especificidade
- Verifica consistência interna
- Avalia testabilidade dos requisitos
- Verifica alinhamento com a constituição
- Gera relatório de revisão pontuado

**Dimensões de Revisão:**

| Dimensão | Peso | O que Valida |
|----------|------|--------------|
| Completude | 25% | Todas seções presentes e substantivas |
| Clareza | 25% | Sem linguagem vaga, interpretação única |
| Consistência | 20% | Sem contradições internas |
| Testabilidade | 20% | Requisitos podem ser verificados |
| Alinhamento com Constituição | 10% | Alinha com princípios do projeto |

**Exemplo:**
```text
Você: /codexspec.review-spec

AI:  Revisando especificação...

     # Relatório de Revisão de Especificação

     ## Resumo
     - **Status Geral**: ⚠️ Precisa de Trabalho
     - **Pontuação de Qualidade**: 72/100
     - **Prontidão**: Precisa de Revisão

     ## Análise de Seções
     | Seção | Status | Completude | Qualidade |
     |-------|--------|------------|-----------|
     | Visão Geral | ✅ | 100% | Alta |
     | Objetivos | ✅ | 100% | Alta |
     | Histórias de Usuário | ⚠️ | 80% | Média |
     | Requisitos Funcionais | ✅ | 100% | Alta |
     | Requisitos Não-Funcionais | ⚠️ | 50% | Média |
     | Casos de Borda | ❌ | 0% | N/A |

     ## Problemas Críticos (Deve Corrigir)
     - [SPEC-001]: Seção de Casos de Borda está vazia
       - Impacto: Pode perder cenários de falha importantes
       - Sugestão: Documente pelo menos 3-5 casos de borda

     ## Avisos (Deveria Corrigir)
     - [SPEC-002]: NFR-001 usa termo vago "rápido"
       - Impacto: Não pode verificar sem métricas
       - Sugestão: Especifique tempo de resposta concreto

     ## Recomendações
     1. Adicionar seção de Casos de Borda com abordagens de tratamento
     2. Quantificar requisitos não-funcionais
     3. Adicionar critérios de aceitação à História de Usuário 3

     Acompanhamento disponível:
     - /codexspec.clarify - para abordar ambiguidades
     - /codexspec.spec-to-plan - se problemas resolvidos
```

**Dicas:**
- Execute antes de `/codexspec.spec-to-plan`
- Resolva problemas Críticos antes de prosseguir
- Avisos não bloqueiam mas indicam risco
- Execute novamente após fazer correções

---

### `/codexspec.review-plan`

Revisar o plano de implementação técnica para viabilidade, qualidade de arquitetura e alinhamento com a especificação.

**Sintaxe:**
```
/codexspec.review-plan [caminho_para_plan.md]
```

**Argumentos:**
| Argumento | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `caminho_para_plan.md` | Não | Caminho para o arquivo plan (detectado automaticamente se não fornecido) |

**O que faz:**
- Verifica se requisitos da spec têm cobertura no plano
- Avalia escolhas de pilha tecnológica
- Avalia decisões de arquitetura
- Valida fases de implementação
- Verifica alinhamento com a constituição
- Gera relatório de revisão pontuado

**Dimensões de Revisão:**

| Dimensão | Peso | O que Valida |
|----------|------|--------------|
| Alinhamento com Spec | 30% | Todos requisitos têm implementação |
| Pilha Tecnológica | 15% | Escolhas de tecnologia apropriadas |
| Qualidade de Arquitetura | 25% | Design e padrões sólidos |
| Planejamento de Fases | 15% | Fases lógicas e realistas |
| Alinhamento com Constituição | 15% | Segue princípios do projeto |

**Exemplo:**
```text
Você: /codexspec.review-plan

AI:  Revisando plano técnico...

     # Relatório de Revisão de Plano

     ## Resumo
     - **Status Geral**: ✅ Passou
     - **Pontuação de Qualidade**: 85/100
     - **Prontidão**: Pronto para Divisão de Tarefas

     ## Alinhamento com Spec
     | Requisito | Cobertura | Status |
     |-----------|-----------|--------|
     | REQ-001 a REQ-012 | ✅ Completa | Todos cobertos |
     | US-001 a US-004 | ✅ Completa | Todos cobertos |
     | NFR-001 a NFR-003 | ⚠️ Parcial | Caching não detalhado |

     ## Revisão de Arquitetura
     Pontos Fortes:
     - Separação limpa de responsabilidades
     - Limites de módulos bem definidos
     - Padrões de design apropriados

     Preocupações:
     - Documentação de estratégia de tratamento de erros ausente

     ## Alinhamento com Constituição
     | Princípio | Conformidade |
     |-----------|--------------|
     | Arquitetura Limpa | ✅ |
     | TDD | ✅ |
     | Qualidade de Código | ✅ |

     Pronto para /codexspec.plan-to-tasks
```

**Dicas:**
- Execute antes de `/codexspec.plan-to-tasks`
- Problemas críticos devem ser resolvidos
- Use para detectar problemas de arquitetura cedo
- Verifique se a pilha tecnológica alinha com habilidades da equipe

---

### `/codexspec.review-tasks`

Validar a divisão de tarefas para completude, conformidade com TDD, ordenação correta e dependências adequadas.

**Sintaxe:**
```
/codexspec.review-tasks [caminho_para_tasks.md]
```

**Argumentos:**
| Argumento | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `caminho_para_tasks.md` | Não | Caminho para o arquivo tasks (detectado automaticamente se não fornecido) |

**O que faz:**
- Verifica se todos os itens do plano têm cobertura de tarefas
- Valida conformidade com TDD (testes antes de implementação)
- Verifica granularidade das tarefas (atômicas, foco em arquivo único)
- Valida dependências (sem ciclos, ordenação correta)
- Revisa marcadores de paralelização
- Valida caminhos de arquivos

**Dimensões de Revisão:**

| Dimensão | Peso | O que Valida |
|----------|------|--------------|
| Cobertura do Plano | 30% | Todos itens do plano têm tarefas |
| Conformidade com TDD | 25% | Fluxo test-first obrigatório |
| Dependência e Ordenação | 20% | Dependências corretas, sem ciclos |
| Granularidade de Tarefas | 15% | Atômicas, escopo apropriado |
| Paralelização e Arquivos | 10% | Marcadores e caminhos corretos |

**Exemplo:**
```text
Você: /codexspec.review-tasks

AI:  Revisando divisão de tarefas...

     # Relatório de Revisão de Tarefas

     ## Resumo
     - **Status Geral**: ⚠️ Precisa de Trabalho
     - **Pontuação de Qualidade**: 78/100
     - **Total de Tarefas**: 24
     - **Paralelizáveis**: 8 (33%)

     ## Conformidade com TDD
     | Componente | Tarefa de Teste | Teste Antes de Impl | Status |
     |------------|-----------------|---------------------|--------|
     | Entidade Task | ✅ | ✅ | ✅ |
     | Entidade User | ✅ | ✅ | ✅ |
     | TaskService | ❌ Ausente | N/A | ❌ |

     ## Violações de TDD
     - [TDD-001]: TaskService sem tarefa de teste

     ## Problemas de Dependência
     - [DEP-001]: Task 2.5 marcada [P] mas depende de 2.4

     ## Recomendações
     1. Adicionar tarefa de teste para TaskService antes da implementação
     2. Corrigir marcador de paralelização na Task 2.5

     Corrija problemas antes de /codexspec.implement-tasks
```

**Dicas:**
- Execute antes de `/codexspec.implement-tasks`
- Violações de TDD são críticas para qualidade de código
- Verifique se marcadores de paralelização são precisos
- Verifique se caminhos de arquivos correspondem à estrutura do projeto

---

### `/codexspec.analyze`

Realizar uma análise de consistência cruzada de artefatos não destrutiva entre spec.md, plan.md e tasks.md. Identifica inconsistências, duplicações e lacunas de cobertura.

**Sintaxe:**
```
/codexspec.analyze
```

**Argumentos:**
| Argumento | Obrigatório | Descrição |
|-----------|-------------|-----------|
| Nenhum | - | Analisa os artefatos da funcionalidade atual |

**O que faz:**
- Detecta duplicações entre artefatos
- Identifica ambiguidades sem critérios mensuráveis
- Encontra itens subespecificados
- Verifica alinhamento com a constituição
- Mapeia cobertura de requisitos para tarefas
- Relata inconsistências em terminologia e ordenação

**Níveis de Severidade:**

| Nível | Definição |
|-------|-----------|
| **CRITICAL** | Violação de constituição, artefato principal ausente, cobertura zero |
| **HIGH** | Requisito duplicado/conflitante, atributo de segurança ambíguo |
| **MEDIUM** | Deriva de terminologia, cobertura não-funcional ausente |
| **LOW** | Melhorias de estilo/wording |

**Exemplo:**
```text
Você: /codexspec.analyze

AI:  Analisando artefatos...

     # Relatório de Análise de Especificação

     ## Resumo de Cobertura
     | Chave de Requisito | Tem Tarefa? | IDs das Tarefas |
     |--------------------|-------------|-----------------|
     | REQ-001 | ✅ | 2.1, 2.2 |
     | REQ-002 | ✅ | 2.3, 2.4 |
     | REQ-003 | ❌ | Nenhum |

     ## Problemas Encontrados

     | ID | Categoria | Severidade | Resumo |
     |----|-----------|------------|--------|
     | A1 | Cobertura | CRITICAL | REQ-003 sem cobertura de tarefa |
     | A2 | Duplicação | HIGH | REQ-005 e REQ-008 sobrepõem |
     | A3 | Ambiguidade | MEDIUM | NFR-002 "seguro" não definido |

     ## Métricas
     - Total de Requisitos: 12
     - Total de Tarefas: 24
     - Cobertura: 92% (11/12 requisitos)
     - Problemas Críticos: 1

     ## Próximas Ações
     1. Adicionar tarefas para REQ-003 (CRITICAL)
     2. Considerar mesclar REQ-005 e REQ-008
     3. Definir "seguro" em NFR-002

     Resolva problemas CRITICAL antes de /codexspec.implement-tasks
```

**Dicas:**
- Execute após `/codexspec.plan-to-tasks`, antes da implementação
- Problemas CRITICAL devem bloquear implementação
- Análise somente leitura — nenhum arquivo é modificado
- Use descobertas para melhorar qualidade dos artefatos

---

### `/codexspec.checklist`

Gerar checklists de qualidade para validar completude, clareza e consistência dos requisitos. Estes são "testes unitários para escrita de requisitos".

**Sintaxe:**
```
/codexspec.checklist [area_foco]
```

**Argumentos:**
| Argumento | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `area_foco` | Não | Foco de domínio (ex: "ux", "api", "security", "performance") |

**O que faz:**
- Gera checklists organizadas por dimensões de qualidade
- Cria checklists no diretório `FEATURE_DIR/checklists/`
- Itens focam em qualidade de requisitos, não testes de implementação

**Dimensões de Qualidade:**
- **Completude de Requisitos**: Todos os requisitos necessários estão presentes?
- **Clareza de Requisitos**: Os requisitos são específicos e sem ambiguidades?
- **Consistência de Requisitos**: Os requisitos estão alinhados sem conflitos?
- **Qualidade dos Critérios de Aceitação**: Os critérios de sucesso são mensuráveis?
- **Cobertura de Cenários**: Todos os fluxos/casos são abordados?
- **Cobertura de Casos de Borda**: Condições de limite estão definidas?
- **Requisitos Não-Funcionais**: Performance, Segurança, Acessibilidade especificados?
- **Dependências e Suposições**: Estão documentadas?

**Exemplos de Tipos de Checklist:**
- `ux.md` - Hierarquia visual, estados de interação, acessibilidade
- `api.md` - Formatos de erro, rate limiting, autenticação
- `security.md` - Proteção de dados, modelo de ameaças, resposta a brechas
- `performance.md` - Métricas, condições de carga, degradação

**Exemplo:**
```text
Você: /codexspec.checklist security

AI:  Gerando checklist de segurança...

     ✓ Criado .codexspec/specs/001-gerenciamento-tarefas/checklists/security.md

     ## Checklist de Qualidade de Requisitos de Segurança

     ### Requisitos de Autenticação
     - [ ] CHK001 - Requisitos de autenticação estão definidos para todos endpoints protegidos? [Completude]
     - [ ] CHK002 - Complexidade de senha está explicitamente especificada? [Clareza]
     - [ ] CHK003 - Requisitos de timeout de sessão estão quantificados? [Mensurabilidade]

     ### Proteção de Dados
     - [ ] CHK004 - Requisitos de criptografia de dados estão especificados em repouso? [Completude]
     - [ ] CHK005 - Requisitos de criptografia de dados estão especificados em trânsito? [Completude]
     - [ ] CHK006 - Tratamento de PII está explicitamente documentado? [Clareza]

     Total: 15 itens em 4 categorias
```

**Dicas:**
- Checklists validam qualidade de requisitos, não correção de implementação
- Use para revisão e melhoria de requisitos
- Crie checklists específicas de domínio para validação focada
- Execute antes de prosseguir para planejamento técnico

---

### `/codexspec.tasks-to-issues`

Converter tarefas de `tasks.md` em issues do GitHub para rastreamento e colaboração de projeto.

**Sintaxe:**
```
/codexspec.tasks-to-issues
```

**Argumentos:**
| Argumento | Obrigatório | Descrição |
|-----------|-------------|-----------|
| Nenhum | - | Converte todas as tarefas da funcionalidade atual |

**O que faz:**
- Analisa IDs de tarefas, descrições, dependências e caminhos de arquivos
- Cria issues do GitHub com corpo estruturado
- Adiciona labels baseadas no tipo de tarefa (setup, implementation, testing, documentation)
- Vincula dependências entre issues
- Relata issues criados com URLs

**Pré-requisitos:**
- Repositório Git com remote GitHub
- GitHub CLI (`gh`) instalado e autenticado
- Arquivo `tasks.md` existe

**Exemplo:**
```text
Você: /codexspec.tasks-to-issues

AI:  Convertendo tarefas para issues do GitHub...

     Repositório: github.com/example/taskman

     Criando issues:
     ✓ #42: Task 1.1 - Setup da Estrutura do Projeto (setup)
     ✓ #43: Task 2.1 - Escrever Testes para Entidade Task (testing)
     ✓ #44: Task 2.2 - Implementar Entidade Task (implementation)
     ...

     Resumo:
     - Issues criados: 24
     - Labels aplicadas: setup(4), implementation(12), testing(5), documentation(3)
     - Dependências vinculadas: 18

     Ver issues: https://github.com/example/taskman/issues
```

**Dicas:**
- Requer autenticação do GitHub CLI (`gh auth login`)
- Funciona apenas com repositórios GitHub
- Cria issues na configuração padrão do repositório
- Verifique duplicatas antes de executar

---

### `/codexspec.commit`

Gerar uma mensagem de commit compatível com Conventional Commits baseada no status do git e contexto de sessão. Este comando é context-aware e lida com diferentes estados do git.

**Sintaxe:**
```
/codexspec.commit
```

**Argumentos:**
| Argumento | Obrigatório | Descrição |
|-----------|-------------|-----------|
| Nenhum | - | Analisa estado atual do git e contexto de sessão |

**O que faz:**
- Coleta contexto git (branch, status, alterações staged/unstaged)
- Analisa histórico de conversação da sessão para entendimento de intenção
- Segue lógica de prioridade baseada no estado do git:
  - **Alterações staged existem**: Gera mensagem de commit apenas das alterações staged
  - **Sem staged, mas alterações unstaged**: Sugere mensagem de commit com lembrete de staging
  - **Sem alterações**: Relata diretório de trabalho limpo
- Gera mensagens compatíveis com Conventional Commits
- Confirma com usuário antes de executar commit

**Tratamento de Estado do Git:**

| Estado | Comportamento |
|--------|---------------|
| Alterações staged | Gerar mensagem, confirmar, commitar |
| Apenas unstaged | Sugerir mensagem, lembrar de staging, perguntar se deve stage all |
| Limpo | Relatar "Nenhuma alteração detectada" |

**Exemplo:**
```text
Você: /codexspec.commit

AI:  Analisando contexto git...

     Branch: feature/add-auth
     Staged: 2 arquivos
     Unstaged: 3 arquivos

     Mensagem de commit sugerida:
     feat(auth): adicionar módulo de autenticação JWT

     - Implementar geração e validação de tokens
     - Adicionar middleware para rotas protegidas
     - Incluir testes unitários para serviço de auth

     Confirmar commit? (y/n)

Você: y

AI:  ✓ Commitado: abc1234
```

**Dicas:**
- Mais flexível que `/codexspec.commit-staged` - lida com vários estados do git
- Considera contexto de sessão para mensagens de commit significativas
- Sempre confirma antes de commitar
- Para alterações unstaged, fornece lembrete claro para stage primeiro

---

### `/codexspec.commit-staged`

Gerar uma mensagem de commit compatível com Conventional Commits baseada apenas nas alterações git staged. Este é um comando mais simples e focado para quando você já staged suas alterações.

**Sintaxe:**
```
/codexspec.commit-staged
```

**Argumentos:**
| Argumento | Obrigatório | Descrição |
|-----------|-------------|-----------|
| Nenhum | - | Analisa apenas alterações staged |

**O que faz:**
- Executa `git diff --staged` para recuperar alterações staged
- Analisa alterações e gera mensagem de commit
- Segue especificação Conventional Commits
- Confirma com usuário antes de commitar
- Relata erro se não existirem alterações staged

**Exemplo:**
```text
Você: /codexspec.commit-staged

AI:  Analisando alterações staged...

     Arquivos staged:
     - src/auth/service.py
     - tests/test_auth.py

     Mensagem de commit sugerida:
     feat(auth): implementar lógica de refresh token

     - Adicionar geração de refresh token
     - Incluir tratamento de expiração de token
     - Adicionar testes para fluxo de refresh

     Confirmar commit? (y/n)

Você: y

AI:  ✓ Commitado: def5678
```

**Dicas:**
- Stage alterações primeiro com `git add`
- Apenas analisa conteúdo staged - ignora unstaged
- Mais simples que `/codexspec.commit` quando você sabe o que quer commitar
- Use `/codexspec.commit` para mensagens mais context-aware

---

## Visão Geral do Fluxo de Trabalho

```
┌──────────────────────────────────────────────────────────────────────────┐
│              Fluxo de Trabalho de Colaboração Humano-AI do CodexSpec      │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. Constitution  ──►  Definir princípios do projeto                     │
│         │                         com validação cruzada de artefatos      │
│         ▼                                                                │
│  2. Specify  ───────►  Perguntas e respostas interativas para esclarecer │
│         │               requisitos (nenhum arquivo criado - controle      │
│         │               humano)                                          │
│         ▼                                                                │
│  3. Generate Spec  ─►  Criar documento spec.md                           │
│         │                                                                │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ PORTÃO DE REVISÃO 1: /codexspec.review-spec ★                  ║   │
│  ║  Validar: Completude, Clareza, Testabilidade, Constituição         ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  4. Clarify  ───────►  Resolver ambiguidades (iterativo)                 │
│         │               4 categorias direcionadas, máx 5 perguntas       │
│         ▼                                                                │
│  5. Spec to Plan  ──►  Criar plano técnico com:                          │
│         │               • Revisão de constitucionalidade (OBRIGATÓRIO)    │
│         │               • Grafo de dependência de módulos                 │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ PORTÃO DE REVISÃO 2: /codexspec.review-plan ★                  ║   │
│  ║  Validar: Alinhamento com Spec, Arquitetura, Tech Stack, Fases     ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  6. Plan to Tasks  ─►  Gerar tarefas atômicas com:                       │
│         │               • TDD obrigatório (testes antes de impl)         │
│         │               • Marcadores paralelos [P]                       │
│         │               • Especificações de caminho de arquivo           │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ PORTÃO DE REVISÃO 3: /codexspec.review-tasks ★                 ║   │
│  ║  Validar: Cobertura, Conformidade TDD, Dependências, Granularidade ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  7. Analyze  ───────►  Verificação de consistência cruzada de artefatos   │
│         │               Detectar lacunas, duplicações, problemas de       │
│         │               constituição                                      │
│         ▼                                                                │
│  8. Implement  ─────►  Executar com fluxo de trabalho TDD condicional     │
│                          Código: Test-first | Docs/Config: Direto         │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

**Ponto Principal**: Cada portão de revisão (★) é um **ponto de verificação humano** onde você valida a saída da AI antes de investir mais tempo. Pular esses portões frequentemente leva a retrabalho custoso.

---

## Solução de Problemas

### "Diretório de funcionalidade não encontrado"

O comando não conseguiu localizar o diretório da funcionalidade.

**Soluções:**
- Execute `codexspec init` primeiro para inicializar o projeto
- Verifique se o diretório `.codexspec/specs/` existe
- Verifique se você está no diretório correto do projeto

### "Nenhum spec.md encontrado"

O arquivo de especificação ainda não existe.

**Soluções:**
- Execute `/codexspec.specify` para esclarecer requisitos primeiro
- Depois execute `/codexspec.generate-spec` para criar spec.md

### "Constituição não encontrada"

Nenhuma constituição de projeto existe.

**Soluções:**
- Execute `/codexspec.constitution` para criar uma
- Constituição é opcional mas recomendada para decisões consistentes

### "Arquivo de tarefas não encontrado"

A divisão de tarefas não existe.

**Soluções:**
- Certifique-se de ter executado `/codexspec.spec-to-plan` primeiro
- Depois execute `/codexspec.plan-to-tasks` para criar tasks.md

### "GitHub CLI não autenticado"

O comando `/codexspec.tasks-to-issues` requer autenticação do GitHub.

**Soluções:**
- Instale GitHub CLI: `brew install gh` (macOS) ou equivalente
- Autentique: `gh auth login`
- Verifique: `gh auth status`

---

## Próximos Passos

- [Fluxo de Trabalho](workflow.md) - Padrões comuns e quando usar cada comando
- [CLI](../reference/cli.md) - Comandos de terminal para inicialização de projeto

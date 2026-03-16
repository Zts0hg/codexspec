# Estudo de Caso CodexSpec: Adicionando Funcionalidade de Geração de Descrição de PR

> Este documento registra o processo completo de usar o kit de ferramentas CodexSpec para adicionar uma nova funcionalidade ao próprio CodexSpec, demonstrando a aplicação prática do Spec-Driven Development (SDD).

## Visão Geral

**Funcionalidade Objetivo**: Adicionar comando `/codexspec.pr` para gerar descrições estruturadas de PR do GitHub / MR do GitLab.

**Fluxo de Desenvolvimento**: `specify → generate-spec → review-spec → clarify → spec-to-plan`

**Característica Principal**: Durante o desenvolvimento, problemas de requisitos foram descobertos e ajustados através do comando `clarify`, demonstrando a flexibilidade do SDD.

---

## Fase 1: Esclarecimento de Requisitos Iniciais (`/codexspec.specify`)

### Entrada Inicial do Usuário

```
Eu gostaria de adicionar uma funcionalidade ao projeto: fornecer um novo comando relacionado ao Git para gerar informações de PR do GitHub precisas, detalhadas e em conformidade (ou informações de MR, para GitLab). Aqui estão dois conteúdos de comando PR que usei em outros projetos, fornecidos para sua referência.

[Exemplo de Referência 1 - Descrição Estruturada]
Agora, por favor, atue como mantenedor do projeto, com base em todo o nosso trabalho até agora, escreva uma descrição clara de Pull Request para este commit.
A descrição do PR precisa ser voltada para outros revisores da equipe, incluindo as seguintes partes:
1. Contexto (Context)
2. Plano de Implementação (Implementation)
3. Testes (Testing)
4. Como Verificar Manualmente (How to Verify)

[Exemplo de Referência 2 - Descrição Simples]
Por favor, com base na diferença de código entre a branch atual e a branch origin/main, organize um título e descrição de Merge Request em conformidade com as especificações Git usando formato Markdown. (Use descrição em chinês)
```

### Processo de Esclarecimento

**Q1: Idioma de Saída**

- Opções: Seguir configuração do projeto / Chinês / Detecção automática
- **Escolha do Usuário**: Seguir configuração do projeto (atual: en)

**Q2: Suporte de Plataforma**

- Opções: Suportar GitHub e GitLab simultaneamente / Apenas GitHub / Detectar plataforma automaticamente
- **Escolha do Usuário**: Detectar plataforma automaticamente

**Q3: Conteúdo da Descrição do PR**

- Opções: Descrição estruturada detalhada / Descrição concisa / Template personalizável
- **Escolha do Usuário**: Descrição estruturada detalhada (recomendado)

**Q4: Condição de Disparo**

- Opções: Branch atual vs origin/main / Commits não enviados / Possibilidade de especificar branch alvo
- **Escolha do Usuário**: Possibilidade de especificar branch alvo

**Q5: Fonte do Spec**

- Opções: Priorizar uso de spec.md / Apenas informações git / Combinar todas as fontes
- **Escolha do Usuário**: Combinar todas as fontes (recomendado)

**Q6: Nomenclatura**

- Opções: codexspec.pr / codexspec.create-pr / codexspec.create-mr
- **Escolha do Usuário**: codexspec.pr (recomendado)

**Q7: Tratamento Sem Spec**

- Opções: Continuar gerando, pular contexto / Avisar usuário para criar spec primeiro / Alertar e continuar
- **Escolha do Usuário**: Continuar gerando, pular contexto

**Q8: Modo de Saída**

- Opções: Saída no terminal / Salvar em arquivo / Terminal + arquivo opcional
- **Escolha do Usuário**: Terminal + arquivo opcional (recomendado)

**Q9: Seções Padrão**

- Opções: Contexto, Plano de Implementação, Testes, Como Verificar (selecionar todos)
- **Escolha do Usuário**: Todas as quatro seções

**Q10: Parâmetros do Comando**

- **Escolha do Usuário**: Todos os parâmetros são opcionais
  - `--target-branch`: Padrão origin/main
  - `--output`: Quando não especificado, padrão apenas saída no terminal
  - `--sections`: Quando não especificado, seguir padrão
  - `--no-spec`: Pular busca do arquivo spec.md

### Correção da Configuração de Idioma

**Feedback do Usuário**: O idioma deve seguir a mesma prioridade que o comando `/commit`, primeiro conforme parâmetro `language.commit` em `config.yml`, se não houver configuração `language.commit`, então conforme `language.output`.

**Resumo de Requisitos Atualizado**:

```
Prioridade de Idioma: language.commit > language.output > English (padrão)
```

---

## Fase 2: Gerar Documento de Especificação (`/codexspec.generate-spec`)

### Estrutura do Documento Gerado

O `spec.md` gerado contém as seguintes partes:

- **Visão Geral**: Resumo da funcionalidade
- **Objetivos**: 4 objetivos
- **Histórias de Usuário**: 4 histórias de usuário com critérios de aceitação
- **Requisitos Funcionais**: 8 requisitos (REQ-001 a REQ-008)
- **Parâmetros do Comando**: 4 definições de parâmetros
- **Requisitos Não-Funcionais**: 3 requisitos (performance, compatibilidade, tratamento de erros)
- **Critérios de Aceitação (Casos de Teste)**: 10 casos de teste
- **Casos de Borda**: 6 casos de borda
- **Exemplo de Formato de Saída**: Exemplos de PR GitHub e MR GitLab
- **Fora do Escopo**: Funcionalidades explicitamente excluídas
- **Dependências**: Itens dependentes
- **Comandos Relacionados**: Comandos relacionados

### Resumo de Requisitos Principais

```markdown
### REQ-003: Language Configuration
The command shall determine output language in the following priority order:
1. `language.commit` in `.codexspec/config.yml` (highest priority)
2. `language.output` in `.codexspec/config.yml` (fallback)
3. English (default if no configuration)
```

---

## Fase 3: Revisão de Especificação (`/codexspec.review-spec`)

### Resultado da Revisão

- **Status Geral**: ✅ Passou
- **Pontuação de Qualidade**: 92/100
- **Status de Prontidão**: Ready for Planning

### Problemas Encontrados

**Avisos (Should Fix)**:

1. **SPEC-001**: Lógica de descoberta de arquivos de teste não especificada
2. **SPEC-002**: Seleção de "modificação mais recente" quando múltiplos spec.md pode ser impreciso

**Sugestões (Nice to Have)**:

1. Considerar adicionar parâmetro `--title`
2. Adicionar requisito de validação de formato de saída
3. Considerar suporte a padrão de URL GitHub Enterprise

### Local de Salvamento do Relatório de Revisão

`.codexspec/specs/001-pr-description-generator/review-spec.md`

---

## Fase 4: Esclarecimento e Ajuste de Requisitos (`/codexspec.clarify`) ⚠️ Ponto de Virada Crítico

### Problemas Descobertos

**Feedback do Usuário**:
> Eu percebi que há um problema com o uso do spec.md. Por exemplo, o usuário está na verdade fazendo uma alteração muito pequena, então não usou o fluxo de trabalho padronizado do codexspec specify->plan->tasks->implement, mas sim modificação direta via diálogo ou plan mode embutido do claude code, e depois de completar as modificações quer chamar individualmente o comando do codexspec para gerar informações de pr padronizadas. Nesta situação, usar diretamente o spec.md modificado mais recentemente pode usar conteúdo de spec.md anterior não relacionado a esta modificação.

### Processo de Perguntas e Respostas de Esclarecimento

**Q1: Estratégia de Seleção de Spec**

**Contexto**: EC-004 atual determina "múltiplos spec.md → usar o modificado mais recentemente". Mas quando o usuário faz pequenas alterações pode não ter usado o fluxo SDD, o spec.md mais recente pode não estar relacionado à modificação atual.

| Opção | Descrição |
|-------|-----------|
| A | Não usar spec.md por padrão, a menos que o usuário especifique explicitamente o parâmetro `--spec` |
| B | Matching baseado no nome da branch |
| C | Solicitar seleção ao usuário |
| D | Matching baseado em alterações de arquivo |

**Escolha do Usuário**: Opção A
**Razão**: Evitar referência incorreta, parâmetro `--spec` permite usuários que precisam de integração SDD especificar explicitamente.

---

**Q2: Estratégia de Extração de Conteúdo do Spec**

**Contexto**: Quando o usuário usa `--spec`, se a estrutura do spec.md estiver incompleta, o que fazer?

| Opção | Descrição |
|-------|-----------|
| A | Melhor esforço de extração, pular partes ausentes |
| B | Alertar e pular Context |
| C | Exigir estrutura completa, senão erro |

**Escolha do Usuário**: Opção A
**Razão**: Evitar bloqueio do fluxo de trabalho devido a problemas de formato spec.

---

**Q3: Descoberta de Arquivos de Teste**

**Contexto**: Como descobrir arquivos de teste para a seção Testing?

| Opção | Descrição |
|-------|-----------|
| A | Padrões de diretório comuns (tests/, test/) |
| B | Heurística agnóstica de linguagem (diretório + padrão de nome de arquivo) |
| C | Não descobrir ativamente, apenas inferir de mensagens de commit |

**Escolha do Usuário**: Opção B
**Razão**: Cobrir múltiplas estruturas de projeto de diferentes linguagens.

---

**Q4: Geração de Título do PR**

**Contexto**: Como o título do PR deve ser gerado?

| Opção | Descrição |
|-------|-----------|
| A | Prioridade de análise do nome da branch |
| B | Prioridade da primeira mensagem de commit |
| C | Geração combinada (git diff + nome da branch + mensagem de commit) |

**Escolha do Usuário**: Opção C
**Razão do Usuário**: O primeiro commit pode ser apenas uma pequena parte das alterações; nome da branch requer altos padrões de nomenclatura. Como há muita informação git e code changes para referenciar, análise combinada é mais precisa.

---

**Q5: Geração de Comandos de Verificação**

**Contexto**: Como gerar comandos de verificação para a seção "How to Verify"?

| Opção | Descrição |
|-------|-----------|
| A | Template genérico |
| B | Detecção de projeto (pyproject.toml → pytest, package.json → npm test) |
| C | Inferir de mensagens de commit |

**Escolha do Usuário**: Opção B
**Razão**: Detecção de projeto pode gerar comandos de verificação mais práticos.

---

### Resumo da Sessão de Esclarecimento

| Questão | Decisão | Impacto |
|---------|---------|---------|
| Estratégia de Seleção de Spec | Opt-in via `--spec` | REQ-007, EC-004, Tabela de Parâmetros |
| Extração de Conteúdo de Spec | Melhor esforço de extração | REQ-005b, EC-004c |
| Descoberta de Arquivos de Teste | Heurística agnóstica de linguagem | REQ-006b |
| Geração de Título de PR | Análise combinada | REQ-008a |
| Geração de Comandos de Verificação | Detecção de arquivos do projeto | REQ-010 |

### Mudança Principal: Inversão de Lógica de Parâmetros

```
Design Original: --no-spec (pular spec)
Novo Design: --spec (habilitar spec, opt-in)
```

---

## Fase 5: Plano de Implementação Técnica (`/codexspec.spec-to-plan`)

### Resumo do Plano

**Método de Implementação**: Arquivo template Markdown (consistente com `/codexspec.commit`)

**Sem Novas Dependências** - Funcionalidade implementada via template de slash command, não requer código Python.

### Resumo de Decisões Técnicas

| Decisão | Escolha | Razão |
|---------|---------|-------|
| Método de Implementação | Template Markdown | Consistente com comandos existentes, fácil de manter |
| Prioridade de Idioma | commit > output > en | Consistente com comando `/commit` |
| Detecção de Plataforma | Parsing de Remote URL | Simples e confiável |
| Integração com Spec | Opt-in (`--spec`) | Evitar referência incorreta |
| Extração de Conteúdo | Melhor esforço | Não bloquear fluxo de trabalho |
| Descoberta de Testes | Padrão de diretório + nome de arquivo | Agnóstico de linguagem |
| Geração de Título | Análise combinada | Mais preciso |
| Detecção de Comando | Detecção de arquivos do projeto | Mais prático |
| Modo de Saída | Terminal primeiro, arquivo opcional | Flexível |

### Fases de Implementação

1. **Fase 1**: Criação de template (YAML frontmatter, configuração de idioma, contexto Git)
2. **Fase 2**: Funcionalidade principal (integração Spec, descoberta de testes, detecção de comando, geração de título)
3. **Fase 3**: Tratamento de casos de borda
4. **Fase 4**: Testes
5. **Fase 5**: Atualização de documentação

### Lista de Arquivos

**Criar**:

- `templates/commands/pr.md`

**Modificar**:

- `CLAUDE.md` - Adicionar descrição do comando
- `README.md` - Adicionar comando à lista

**Testar**:

- `tests/test_pr_template.py`

---

## Diagrama de Fluxo Completo

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Fluxo de Desenvolvimento SDD CodexSpec           │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec.specify                                                      │
│  ├─ Esclarecer requisitos via perguntas e respostas                      │
│  ├─ Usuário forneceu exemplos de referência                              │
│  └─ 10 questões, cobrindo idioma, plataforma, conteúdo, parâmetros etc   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec.generate-spec                                                │
│  ├─ Gerar spec.md completo                                               │
│  ├─ 4 histórias de usuário, 8 requisitos funcionais, 10 casos de teste   │
│  └─ Salvar em .codexspec/specs/001-pr-description-generator/spec.md      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec.review-spec                                                  │
│  ├─ Pontuação de qualidade: 92/100                                       │
│  ├─ Encontrados 2 avisos (descoberta de arquivos teste, múltiplos spec)  │
│  └─ Status: Passou, pode entrar na fase de planejamento                  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec.clarify  ⚠️ Ajuste Crítico                                   │
│  ├─ Usuário descobriu problema de cenário de uso real                    │
│  ├─ 5 questões de esclarecimento, todas respondidas                      │
│  ├─ Mudança principal: --no-spec → --spec (opt-in)                       │
│  └─ Novos 5 requisitos (REQ-005b, 006b, 008a, 010, atualização 007)      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec.spec-to-plan                                                 │
│  ├─ Atualizar plano de implementação técnica                             │
│  ├─ 9 decisões técnicas, incluindo 5 novas decisões                      │
│  ├─ 5 fases de implementação                                             │
│  └─ Salvar em .codexspec/specs/001-pr-description-generator/plan.md      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Próximos Passos (não completados nesta sessão)                          │
│  ├─ /codexspec.review-plan - Validar qualidade do plano                  │
│  ├─ /codexspec.plan-to-tasks - Decompor em tarefas executáveis           │
│  └─ /codexspec.implement-tasks - Executar implementação                  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Principais Pontos de Aprendizado

### 1. Valor da Fase de Esclarecimento

Este caso demonstra o papel crítico do comando `clarify`:

- **Usuário descobriu problemas reais durante o uso** - Risco de uso indevido de spec.md em cenários de pequenas alterações
- **Resolveu falhas de design através de perguntas e respostas de esclarecimento** - Mudança de detecção automática para modo opt-in
- **Mudanças de requisitos registradas sistematicamente** - Todas as mudanças salvas na seção Clarifications do spec.md

### 2. Flexibilidade do Fluxo SDD

- Não é um fluxo linear, pode retornar e ajustar em qualquer fase
- `clarify` pode ser inserido após `review-spec`, antes de `spec-to-plan`
- Documentos de especificação e plano técnico são atualizados para refletir mudanças

### 3. Evolução do Design de Parâmetros

```
Design Inicial:
  --no-spec: Pular spec.md (usar por padrão)

Design Final:
  --spec: Habilitar spec.md (não usar por padrão)
```

Esta mudança reflete a transição de design de "fluxo de trabalho SDD padrão" para "suporte a fluxo de trabalho não-SDD", tornando a ferramenta mais versátil.

### 4. Produção de Documentos

| Fase | Arquivo Produzido | Conteúdo |
|------|-------------------|----------|
| generate-spec | spec.md | Documento de especificação completo |
| review-spec | review-spec.md | Relatório de revisão de qualidade |
| clarify | (atualiza spec.md) | Registro de esclarecimento + atualização de requisitos |
| spec-to-plan | plan.md | Plano de implementação técnica |

---

## Apêndice: Referência Rápida de Uso de Comandos

```bash
# 1. Esclarecimento de requisitos iniciais
/codexspec.specify

# 2. Gerar documento de especificação
/codexspec.generate-spec

# 3. Revisar qualidade da especificação
/codexspec.review-spec

# 4. Esclarecer/ajustar requisitos (opcional, usar após descobrir problemas)
/codexspec.clarify [descrição do problema]

# 5. Gerar plano técnico
/codexspec.spec-to-plan

# 6. Revisar qualidade do plano (opcional)
/codexspec.review-plan

# 7. Decompor em tarefas
/codexspec.plan-to-tasks

# 8. Executar implementação
/codexspec.implement-tasks
```

---

*Este documento foi gerado automaticamente pelo fluxo de trabalho SDD CodexSpec, registrando o processo real de diálogo de desenvolvimento.*

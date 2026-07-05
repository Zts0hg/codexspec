# Estudo de caso do CodexSpec: adicionar um gerador de descrições de PR ao projeto

> Este documento registra o processo completo de usar o conjunto de ferramentas do CodexSpec para adicionar uma nova funcionalidade ao próprio CodexSpec, demonstrando o Spec-Driven Development (SDD) na prática.

## Visão geral

**Funcionalidade-alvo**: adicionar o comando `/codexspec:pr`, que gera descrições estruturadas de PR do GitHub / MR do GitLab. (Veja a [entrada `/codexspec:pr` no README](https://github.com/Zts0hg/codexspec/blob/main/README.md) para o resumo voltado ao usuário do comando entregue.)

**Fluxo de desenvolvimento**: `specify → generate-spec → review-spec → clarify → spec-to-plan`

**Característica-chave**: um problema de requisito surgiu no meio do fluxo e foi corrigido pelo comando `clarify`, ilustrando a flexibilidade do SDD. Este é um exemplo concreto do **Confirmation Gate** do CodexSpec — nada se torna vinculante até você confirmar explicitamente, e uma decisão anteriormente aceita pode ser reaberta e revertida no ponto de verificação do clarify.

---

## Etapa 1: esclarecimento inicial dos requisitos (`/codexspec:specify`)

### Entrada inicial do usuário

```
I want to add a feature to the project: a new Git-related command that generates accurate, detailed, and standards-compliant GitHub PR descriptions (or MR descriptions, for GitLab). Below are two PR commands I have used in other projects, provided for reference.

[Reference Example 1 - Structured Description]
Now, acting as a project maintainer, based on all the work we have done so far, write a clear Pull Request description for this submission.
The PR description should be aimed at the other reviewers on the team and include the following sections:
1. Context
2. Implementation
3. Testing
4. How to Verify

[Reference Example 2 - Simple Description]
Based on the code diff between the current branch and origin/main, use Markdown to produce a Merge Request title and description that comply with Git conventions. (Describe in Chinese.)
```

### Processo de esclarecimento

**Q1: Idioma de saída**

- Opções: Seguir a configuração do projeto / Chinês / Detecção automática
- **Escolha do usuário**: Seguir a configuração do projeto (atual: en)

**Q2: Suporte a plataformas**

- Opções: Suportar GitHub e GitLab / Apenas GitHub / Detectar plataforma automaticamente
- **Escolha do usuário**: Detectar plataforma automaticamente

**Q3: Conteúdo da descrição do PR**

- Opções: Descrição estruturada detalhada / Descrição concisa / Template personalizável
- **Escolha do usuário**: Descrição estruturada detalhada (recomendado)

**Q4: Condição de disparo**

- Opções: Branch atual vs. origin/main / Commits ainda não enviados / Branch alvo configurável
- **Escolha do usuário**: Branch alvo configurável

**Q5: Fonte da spec**

- Opções: Privilegiar spec.md / Apenas informações do git / Combinar todas as fontes
- **Escolha do usuário**: Combinar todas as fontes (recomendado)

**Q6: Nomenclatura**

- Opções: codexspec.pr / codexspec.create-pr / codexspec.create-mr
- **Escolha do usuário**: codexspec.pr (recomendado)

**Q7: Tratamento quando não há spec**

- Opções: Continuar gerando, pular Context / Pedir ao usuário para criar a spec antes / Avisar e continuar
- **Escolha do usuário**: Continuar gerando, pular Context

**Q8: Método de saída**

- Opções: Saída no terminal / Salvar em arquivo / Terminal + arquivo opcional
- **Escolha do usuário**: Terminal + arquivo opcional (recomendado)

**Q9: Seções padrão**

- Opções: Context, Implementation, Testing, How to Verify (todas selecionadas)
- **Escolha do usuário**: As quatro seções

**Q10: Parâmetros do comando**

- **Escolha do usuário**: Todos os parâmetros são opcionais
  - `--target-branch`: padrão origin/main
  - `--output`: quando omitido, o padrão é apenas saída no terminal
  - `--sections`: quando omitido, segue os padrões
  - `--no-spec`: pula a busca por spec.md

### Correção da configuração de idioma

**Feedback do usuário**: o comportamento de idioma deveria corresponder ao do comando `/commit-staged` — honrar primeiro `language.commit` do `config.yml` e só recair para `language.output` quando `language.commit` não estiver definido.

**Resumo de requisitos atualizado**:

```
Language priority: language.commit > language.output > English (default)
```

---

## Etapa 2: gerar o documento de especificação (`/codexspec:generate-spec`)

### Estrutura do documento gerado

O `spec.md` gerado contém as seguintes seções:

- **Visão geral**: visão geral da funcionalidade
- **Objetivos**: 4 objetivos
- **Histórias de usuário**: 4 histórias de usuário com critérios de aceitação
- **Requisitos funcionais**: 8 requisitos (REQ-001 a REQ-008)
- **Parâmetros do comando**: 4 definições de parâmetros
- **Requisitos não funcionais**: 3 requisitos (desempenho, compatibilidade, tratamento de erros)
- **Critérios de aceitação (casos de teste)**: 10 casos de teste
- **Casos de borda**: 6 casos de borda
- **Exemplo de formato de saída**: exemplos de PR do GitHub e MR do GitLab
- **Fora de escopo**: funcionalidades explicitamente excluídas
- **Dependências**: dependências
- **Comandos relacionados**: comandos relacionados

### Trecho de requisito-chave

```markdown
### REQ-003: Language Configuration
The command shall determine output language in the following priority order:
1. `language.commit` in `.codexspec/config.yml` (highest priority)
2. `language.output` in `.codexspec/config.yml` (fallback)
3. English (default if no configuration)
```

---

## Etapa 3: revisão da especificação (`/codexspec:review-spec`)

### Resultado da revisão

- **Status geral**: ✅ Pass
- **Pontuação de qualidade**: 92/100
- **Prontidão**: Ready for Planning

### Problemas encontrados

**Avisos (Should Fix)**:

1. **SPEC-001**: a lógica de descoberta de arquivos de teste não está especificada explicitamente
2. **SPEC-002**: quando há vários spec.md, escolher "modificado mais recentemente" pode ser impreciso

**Sugestões (Nice to Have)**:

1. Considere adicionar um parâmetro `--title`
2. Adicione um requisito de validação do formato de saída
3. Considere suportar padrões de URL do GitHub Enterprise

### Local do relatório de revisão

`.codexspec/specs/2026-0613-1200ab-pr-description-generator/review-spec.md`

Esta é uma **revisão baseada em evidências**: cada aviso e sugestão acima está vinculado a uma lacuna concreta e identificável na spec, e os itens consultivos (Nice to Have) não afetam a aceitação nem disparam alterações automáticas.

---

## Etapa 4: esclarecimento e ajuste de requisitos (`/codexspec:clarify`) — ponto de virada crítico

### Problema descoberto

**Feedback do usuário**:
> Percebi que há um problema com o uso do spec.md. Por exemplo, o usuário pode, na verdade, estar fazendo uma alteração muito pequena, então não seguiu o fluxo padronizado do CodexSpec de specify → plan → tasks → implement. Em vez disso, fez alterações diretamente por conversação ou pelo modo plan embutido do Claude Code e, ao terminar, quer invocar um comando do CodexSpec separadamente para gerar uma descrição de PR em conformidade com os padrões. Nesse caso, usar por padrão o spec.md modificado mais recentemente pode puxar conteúdo de um spec.md anterior que nada tem a ver com essa alteração.

É o **Confirmation Gate** em ação: a decisão anterior ("usar por padrão o spec.md modificado mais recentemente") havia sido registrada, mas ainda não era vinculante no sentido de irreversível — o usuário a reabriu no ponto de verificação do clarify com novas informações sobre um padrão de uso real, e o padrão antes aceito foi revertido.

### Processo de perguntas e respostas do esclarecimento

**Q1: Estratégia de seleção da spec**

**Contexto**: o atual EC-004 diz "vários spec.md → usar o modificado mais recentemente". Mas quando o usuário faz uma pequena alteração sem seguir o fluxo de SDD, o spec.md mais recente pode não ter relação com a alteração atual.

| Opção | Descrição |
|--------|-------------|
| A | Não usar spec.md por padrão, a menos que o usuário passe `--spec` explicitamente |
| B | Casar pelo nome da branch |
| C | Pedir ao usuário para escolher |
| D | Casar pelas alterações de arquivos |

**Escolha do usuário**: Opção A
**Motivo**: evita referências incorretas; o parâmetro `--spec` permite que usuários que querem integração com SDD optem explicitamente.

---

**Q2: Estratégia de extração de conteúdo da spec**

**Contexto**: quando o usuário passa `--spec`, o que acontece se a estrutura do spec.md estiver incompleta?

| Opção | Descrição |
|--------|-------------|
| A | Extração por melhor esforço, pulando seções ausentes |
| B | Avisar e pular Context |
| C | Exigir estrutura completa; caso contrário, erro |

**Escolha do usuário**: Opção A
**Motivo**: evita que um problema de formato da spec bloqueie o fluxo de trabalho.

---

**Q3: Descoberta de arquivos de teste**

**Contexto**: como a seção Testing deveria descobrir arquivos de teste?

| Opção | Descrição |
|--------|-------------|
| A | Padrões comuns de diretório (tests/, test/) |
| B | Heurísticas independentes de linguagem (diretório + padrões de nome de arquivo) |
| C | Sem descoberta ativa; inferir apenas das mensagens de commit |

**Escolha do usuário**: Opção B
**Motivo**: cobre diversas estruturas de projeto em diferentes linguagens.

---

**Q4: Geração do título do PR**

**Contexto**: como o título do PR deveria ser gerado?

| Opção | Descrição |
|--------|-------------|
| A | Primeiro, parsing do nome da branch |
| B | Primeiro, a mensagem de commit inicial |
| C | Síntese (git diff + nome da branch + mensagens de commit) |

**Escolha do usuário**: Opção C
**Motivo do usuário**: o primeiro commit pode representar apenas uma fatia pequena da alteração, e nomes de branch pressupõem disciplina forte de nomenclatura. Tendo informação substantiva do git e alterações de código disponíveis para referência, uma análise sintetizada é mais precisa.

---

**Q5: Geração do comando de verificação**

**Contexto**: como a seção "How to Verify" deveria gerar comandos de verificação?

| Opção | Descrição |
|--------|-------------|
| A | Templates genéricos |
| B | Detecção de projeto (pyproject.toml → pytest, package.json → npm test) |
| C | Inferir das mensagens de commit |

**Escolha do usuário**: Opção B
**Motivo**: a detecção de projeto produz comandos de verificação mais práticos.

---

### Resumo da sessão de esclarecimento

| Pergunta | Decisão | Impacto |
|----------|----------|--------|
| Estratégia de seleção da spec | Opt-in via `--spec` | REQ-007, EC-004, tabela de parâmetros |
| Extração de conteúdo da spec | Extração por melhor esforço | REQ-005b, EC-004c |
| Descoberta de arquivos de teste | Heurísticas independentes de linguagem | REQ-006b |
| Geração do título do PR | Análise sintetizada | REQ-008a |
| Geração do comando de verificação | Detecção de arquivos do projeto | REQ-010 |

### Mudança-chave: inversão da lógica de parâmetros

```
Original design: --no-spec (skip spec)
New design:      --spec (enable spec, opt-in)
```

Essa inversão é a ilustração mais clara do Confirmation Gate neste estudo de caso: um padrão originalmente "vinculante" (`--no-spec`, ou seja, spec ligada por padrão) foi reaberto, revertido e reconfirmado como opt-in assim que o usuário trouxe um fluxo de trabalho real que ele teria quebrado.

---

## Etapa 5: plano técnico de implementação (`/codexspec:spec-to-plan`)

### Visão geral do plano

**Abordagem de implementação**: arquivo de template Markdown (consistente com `/codexspec:commit-staged`)

**Sem novas dependências** — a funcionalidade é entregue por meio de um template de slash command e não exige código Python.

### Resumo das decisões técnicas

| Decisão | Escolha | Motivo |
|----------|--------|--------|
| Abordagem de implementação | Template Markdown | Consistente com comandos existentes, fácil de manter |
| Prioridade de idioma | commit > output > en | Consistente com `/commit-staged` |
| Detecção de plataforma | Parsing da remote URL | Simples e confiável |
| Integração com spec | Opt-in (`--spec`) | Evita referências incorretas |
| Extração de conteúdo | Melhor esforço | Não bloqueia o fluxo de trabalho |
| Descoberta de testes | Padrões de diretório + nome de arquivo | Independente de linguagem |
| Geração do título | Análise sintetizada | Mais precisa |
| Detecção de comandos | Detecção de arquivos do projeto | Mais prática |
| Modo de saída | Terminal primeiro, arquivo opcional | Flexível |

### Fases de implementação

1. **Fase 1**: criação do template (YAML frontmatter, configuração de idioma, contexto Git)
2. **Fase 2**: funcionalidade central (integração com spec, descoberta de testes, detecção de comandos, geração de título)
3. **Fase 3**: tratamento de casos de borda
4. **Fase 4**: testes
5. **Fase 5**: atualizações de documentação

### Lista de arquivos

**Criados**:

- `templates/commands/pr.md`

**Modificados**:

- `CLAUDE.md` - Adicionar a descrição do comando
- `README.md` - Adicionar o comando à lista

**Testes**:

- `tests/test_pr_template.py`

---

## Diagrama completo do fluxo

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   Fluxo de desenvolvimento SDD do CodexSpec              │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:specify                                                      │
│  ├─ Esclarecer requisitos via perguntas e respostas                      │
│  ├─ Usuário fornece exemplos de referência                               │
│  └─ 10 perguntas cobrindo idioma, plataforma, conteúdo, parâmetros etc. │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:generate-spec                                                │
│  ├─ Gera um spec.md completo                                             │
│  ├─ 4 histórias de usuário, 8 requisitos funcionais, 10 casos de teste   │
│  └─ Salvo em .codexspec/specs/2026-0613-1200ab-pr-description-generator/spec.md │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:review-spec                                                  │
│  ├─ Pontuação de qualidade: 92/100                                       │
│  ├─ 2 avisos encontrados (descoberta de testes, múltiplas specs)         │
│  └─ Status: Pass, pode prosseguir para o planejamento                    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:clarify  (Ajuste crítico)                                    │
│  ├─ Usuário traz um problema de uso real                                 │
│  ├─ 5 perguntas de esclarecimento, todas respondidas                     │
│  ├─ Mudança-chave: --no-spec → --spec (opt-in)                           │
│  └─ 5 requisitos adicionados (REQ-005b, 006b, 008a, 010, atualização do 007) │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:spec-to-plan                                                 │
│  ├─ Atualiza o plano técnico de implementação                            │
│  ├─ 9 decisões técnicas, incluindo 5 novas                               │
│  ├─ 5 fases de implementação                                             │
│  └─ Salvo em .codexspec/specs/2026-0613-1200ab-pr-description-generator/plan.md │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Etapas seguintes (não concluídas nesta sessão)                          │
│  ├─ /codexspec:review-plan - Validar a qualidade do plano                │
│  ├─ /codexspec:plan-to-tasks - Decompor em tarefas executáveis           │
│  └─ /codexspec:implement-tasks - Executar a implementação                │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Principais aprendizados

### 1. O valor da etapa clarify

Este caso mostra o papel central do comando `clarify`:

- **O usuário descobre um problema real durante o uso** — o risco de usar spec.md indevidamente em cenários de alteração pequena
- **Uma falha de design é resolvida por perguntas e respostas de esclarecimento** — passagem de detecção automática para opt-in
- **Mudanças de requisito são registradas sistematicamente** — todas as mudanças ficam salvas na seção Clarifications do spec.md

### 2. Flexibilidade do fluxo SDD

- Não é um fluxo linear; é possível retornar e ajustar em qualquer etapa
- `clarify` pode ser inserido após `review-spec` e antes de `spec-to-plan`
- Tanto o documento de especificação quanto o plano técnico são atualizados para refletir a mudança

### 3. Evolução do design de parâmetros

```
Initial design:
  --no-spec: skip spec.md (used by default)

Final design:
  --spec: enable spec.md (not used by default)
```

Essa mudança reflete uma transição de design de "fluxo SDD por padrão" para "também suportar fluxos não-SDD", tornando a ferramenta mais versátil.

### 4. Documentos produzidos

| Etapa | Arquivo de saída | Conteúdo |
|-------|-------------|---------|
| generate-spec | spec.md | Documento de especificação completo |
| review-spec | review-spec.md | Relatório de revisão de qualidade |
| clarify | (atualiza spec.md) | Registros de esclarecimento + atualizações de requisitos |
| spec-to-plan | plan.md | Plano técnico de implementação |

---

## Apêndice: referência rápida de comandos

```bash
# 1. Esclarecimento inicial dos requisitos
/codexspec:specify

# 2. Gerar o documento de especificação
/codexspec:generate-spec

# 3. Revisar a qualidade da especificação
/codexspec:review-spec

# 4. Esclarecer/ajustar requisitos (opcional; use quando um problema for encontrado)
/codexspec:clarify [issue description]

# 5. Gerar o plano técnico
/codexspec:spec-to-plan

# 6. Revisar a qualidade do plano (opcional)
/codexspec:review-plan

# 7. Decompor em tarefas
/codexspec:plan-to-tasks

# 8. Executar a implementação
/codexspec:implement-tasks
```

---

*Este documento foi gerado pelo fluxo de trabalho SDD do CodexSpec e registra uma conversa real de desenvolvimento.*

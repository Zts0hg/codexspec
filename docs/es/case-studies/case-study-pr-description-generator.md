# Caso de estudio de CodexSpec: añadir un generador de descripciones de PR al proyecto

> Caso histórico: la conversación, las decisiones intermedias, la secuencia de comandos y las puntuaciones siguientes reflejan el flujo de aquella época, no el contrato actual. El flujo estándar actual incluye una etapa de diseño independiente y `review-design`; `clarify` actualiza los requisitos confirmados antes que la especificación. Consulta el [flujo actual](../user-guide/workflow.md) y la [referencia del comando PR](../user-guide/commands.md#codexspecpr).

> Este documento recoge el proceso completo de usar la cadena de herramientas de CodexSpec para añadir una nueva funcionalidad al propio CodexSpec, mostrando Spec-Driven Development (SDD) en la práctica.

## Resumen

**Funcionalidad objetivo**: añadir el comando `/codexspec:pr`, que genera descripciones estructuradas de PR de GitHub / MR de GitLab. (Consulta la [entrada `/codexspec:pr` en el README](https://github.com/Zts0hg/codexspec/blob/main/README.md) para el resumen orientado al usuario del comando publicado.)

**Flujo de desarrollo**: `specify → generate-spec → review-spec → clarify → design-to-plan`

**Característica clave**: un problema de requisitos afloró a mitad de proceso y se corrigió mediante el comando `clarify`, ilustrando la flexibilidad de SDD. Es un ejemplo concreto del **Confirmation Gate** de CodexSpec: nada es vinculante hasta que lo confirmas explícitamente, y una decisión previamente aceptada puede reabrirse y revertirse en el punto de control de clarify.

---

## Etapa 1: Clarificación inicial de requisitos (`/codexspec:specify`)

### Entrada inicial del usuario

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

### Proceso de clarificación

**P1: Idioma de salida**

- Opciones: Seguir la configuración del proyecto / Chino / Detectar automáticamente
- **Elección del usuario**: Seguir la configuración del proyecto (actual: en)

**P2: Soporte de plataformas**

- Opciones: Soportar tanto GitHub como GitLab / Solo GitHub / Detectar plataforma automáticamente
- **Elección del usuario**: Detectar plataforma automáticamente

**P3: Contenido de la descripción del PR**

- Opciones: Descripción estructurada detallada / Descripción concisa / Plantilla personalizable
- **Elección del usuario**: Descripción estructurada detallada (recomendado)

**P4: Condición de disparo**

- Opciones: Rama actual frente a origin/main / Commits aún no enviados al remoto / Rama objetivo configurable
- **Elección del usuario**: Rama objetivo configurable

**P5: Fuente de la especificación**

- Opciones: Preferir spec.md / Solo información de git / Combinar todas las fuentes
- **Elección del usuario**: Combinar todas las fuentes (recomendado)

**P6: Nombre del comando**

- Opciones: codexspec.pr / codexspec.create-pr / codexspec.create-mr
- **Elección del usuario**: codexspec.pr (recomendado)

**P7: Cómo actuar cuando falta spec**

- Opciones: Continuar generando, omitir Context / Pedir al usuario que cree el spec primero / Avisar y continuar
- **Elección del usuario**: Continuar generando, omitir Context

**P8: Método de salida**

- Opciones: Salida por terminal / Guardar a archivo / Terminal + archivo opcional
- **Elección del usuario**: Terminal + archivo opcional (recomendado)

**P9: Secciones por defecto**

- Opciones: Context, Implementation, Testing, How to Verify (todas seleccionadas)
- **Elección del usuario**: Las cuatro secciones

**P10: Parámetros del comando**

- **Elección del usuario**: Todos los parámetros son opcionales
  - `--target-branch`: por defecto origin/main
  - `--output`: si no se indica, por defecto solo salida por terminal
  - `--sections`: si no se indica, sigue los valores por defecto
  - `--no-spec`: omite la búsqueda en spec.md

### Corrección de la configuración de idioma

**Comentario del usuario**: el comportamiento de idioma debería coincidir con el del comando `/commit-staged`: aplicar primero `language.commit` de `config.yml` y solo caer a `language.output` cuando `language.commit` no esté establecido.

**Resumen de requisitos actualizado**:

```
Language priority: language.commit > language.output > English (default)
```

---

## Etapa 2: Generación del documento de especificación (`/codexspec:generate-spec`)

### Estructura del documento generado

El `spec.md` generado contiene las siguientes secciones:

- **Visión general (Overview)**: descripción de la funcionalidad
- **Objetivos (Goals)**: 4 objetivos
- **Historias de usuario (User Stories)**: 4 historias con criterios de aceptación
- **Requisitos funcionales**: 8 requisitos (REQ-001 a REQ-008)
- **Parámetros del comando**: 4 definiciones de parámetros
- **Requisitos no funcionales**: 3 requisitos (rendimiento, compatibilidad, gestión de errores)
- **Criterios de aceptación (casos de prueba)**: 10 casos
- **Casos límite (Edge Cases)**: 6 casos
- **Ejemplo de formato de salida**: ejemplos de PR de GitHub y MR de GitLab
- **Fuera de alcance (Out of Scope)**: funcionalidades explícitamente excluidas
- **Dependencias**: dependencias
- **Comandos relacionados**: comandos relacionados

### Extracto de un requisito clave

```markdown
### REQ-003: Language Configuration
The command shall determine output language in the following priority order:
1. `language.commit` in `.codexspec/config.yml` (highest priority)
2. `language.output` in `.codexspec/config.yml` (fallback)
3. English (default if no configuration)
```

---

## Etapa 3: Revisión de la especificación (`/codexspec:review-spec`)

### Resultado de la revisión

- **Estado global**: PASS
- **Puntuación de calidad**: 92/100
- **Preparación**: lista para planificación

### Problemas encontrados

**Advertencias (deberían corregirse)**:

1. **SPEC-001**: la lógica de descubrimiento de archivos de prueba no está especificada explícitamente
2. **SPEC-002**: cuando existen varios spec.md, elegir "el modificado más recientemente" puede ser inexacto

**Sugerencias (deseables)**:

1. Considerar añadir un parámetro `--title`
2. Añadir un requisito de validación del formato de salida
3. Considerar soportar patrones de URL de GitHub Enterprise

### Ubicación del informe de revisión

`.codexspec/specs/2026-0613-1200ab-pr-description-generator/review-spec.md`

Se trata de una **revisión basada en evidencia**: cada advertencia y sugerencia anterior está vinculada a un hueco concreto e identificable del spec, y los ítems consultivos (deseables) no afectan a la aceptación ni disparan cambios automáticos.

---

## Etapa 4: Clarificación y ajuste de requisitos (`/codexspec:clarify`) — punto de inflexión crítico

### Problema descubierto

**Comentario del usuario**:
> Me he dado cuenta de que hay un problema con el uso de spec.md. Por ejemplo, el usuario puede estar haciendo un cambio muy pequeño, así que no ha seguido el flujo estandarizado de CodexSpec de specify → plan → tasks → implement. En su lugar, ha hecho cambios directamente mediante conversación o el modo plan integrado de Claude Code y, tras terminarlos, quiere invocar un comando de CodexSpec por separado para generar una descripción de PR conforme a los estándares. En este caso, usar por defecto el spec.md modificado más recientemente puede arrastrar contenido de un spec.md anterior que nada tiene que ver con este cambio.

Aquí opera el **Confirmation Gate**: la decisión anterior ("usar por defecto el spec.md modificado más recientemente") había quedado registrada, pero no era vinculante en el sentido de irreversible: el usuario la reabrió en el punto de control de clarify con nueva información sobre un patrón de uso real, y el valor por defecto aceptado antes se revirtió.

### Proceso de preguntas y respuestas de clarificación

**P1: Estrategia de selección del spec**

**Contexto**: el actual EC-004 dice "varios spec.md → usar el modificado más recientemente". Pero cuando un usuario hace un cambio pequeño sin seguir el flujo SDD, el spec.md más reciente puede no estar relacionado con el cambio actual.

| Opción | Descripción |
|--------|-------------|
| A | No usar spec.md por defecto, salvo que el usuario pase `--spec` explícitamente |
| B | Emparejar por nombre de rama |
| C | Pedir al usuario que elija |
| D | Emparejar por cambios de archivos |

**Elección del usuario**: opción A
**Motivo**: evita referencias incorrectas; el parámetro `--spec` permite que los usuarios que quieran integración con SDD opten por ella de forma explícita.

---

**P2: Estrategia de extracción del contenido del spec**

**Contexto**: cuando el usuario pasa `--spec`, ¿qué ocurre si la estructura del spec.md es incompleta?

| Opción | Descripción |
|--------|-------------|
| A | Extracción con mejor esfuerzo, omitir secciones ausentes |
| B | Avisar y omitir Context |
| C | Exigir una estructura completa; en caso contrario, error |

**Elección del usuario**: opción A
**Motivo**: evitar que un problema de formato del spec bloquee el flujo de trabajo.

---

**P3: Descubrimiento de archivos de prueba**

**Contexto**: ¿cómo debería la sección Testing descubrir los archivos de prueba?

| Opción | Descripción |
|--------|-------------|
| A | Patrones de directorios habituales (tests/, test/) |
| B | Heurísticas independientes del lenguaje (patrones de directorio + nombre de archivo) |
| C | Sin descubrimiento activo; inferir solo a partir de los mensajes de commit |

**Elección del usuario**: opción B
**Motivo**: cubre una variedad de estructuras de proyecto en distintos lenguajes.

---

**P4: Generación del título del PR**

**Contexto**: ¿cómo debería generarse el título del PR?

| Opción | Descripción |
|--------|-------------|
| A | Primero analizar el nombre de rama |
| B | Primero el primer mensaje de commit |
| C | Sintetizar (git diff + nombre de rama + mensajes de commit) |

**Elección del usuario**: opción C
**Motivo del usuario**: el primer commit puede representar solo una porción pequeña del cambio, y los nombres de rama asumen una normas de nomenclatura estrictas. Con información sustancial de git y cambios de código disponibles como referencia, un análisis sintetizado es más preciso.

---

**P5: Generación del comando de verificación**

**Contexto**: ¿cómo debería la sección "How to Verify" generar los comandos de verificación?

| Opción | Descripción |
|--------|-------------|
| A | Plantillas genéricas |
| B | Detección de proyecto (pyproject.toml → pytest, package.json → npm test) |
| C | Inferir a partir de los mensajes de commit |

**Elección del usuario**: opción B
**Motivo**: la detección de proyecto produce comandos de verificación más prácticos.

---

### Resumen de la sesión de clarificación

| Pregunta | Decisión | Impacto |
|----------|----------|--------|
| Estrategia de selección del spec | Opt-in vía `--spec` | REQ-007, EC-004, tabla de parámetros |
| Extracción del contenido del spec | Extracción con mejor esfuerzo | REQ-005b, EC-004c |
| Descubrimiento de archivos de prueba | Heurísticas independientes del lenguaje | REQ-006b |
| Generación del título del PR | Análisis sintetizado | REQ-008a |
| Generación del comando de verificación | Detección por archivos del proyecto | REQ-010 |

### Cambio clave: inversión de la lógica del parámetro

```
Original design: --no-spec (skip spec)
New design:      --spec (enable spec, opt-in)
```

Esta inversión es la ilustración más nítida del Confirmation Gate en este caso de estudio: un valor por defecto originalmente "vinculante" (`--no-spec`, es decir, spec activado por defecto) se reabrió, invirtió y se reconfirmó como opt-in en cuanto el usuario sacó a la luz un flujo de trabajo real que ese valor por defecto habría perjudicado.

---

## Etapa 5: Plan técnico de implementación (`/codexspec:design-to-plan`)

### Visión general del plan

**Enfoque de implementación**: archivo de plantilla Markdown (coherente con `/codexspec:commit-staged`)

**Sin dependencias nuevas**: la funcionalidad se entrega mediante una plantilla de slash command y no requiere código Python.

### Resumen de decisiones técnicas

| Decisión | Elección | Motivo |
|----------|--------|--------|
| Enfoque de implementación | Plantilla Markdown | Coherente con los comandos existentes, fácil de mantener |
| Prioridad de idioma | commit > output > en | Coherente con `/commit-staged` |
| Detección de plataforma | Parseo de la URL remota | Simple y fiable |
| Integración con spec | Opt-in (`--spec`) | Evita referencias incorrectas |
| Extracción de contenido | Mejor esfuerzo | No bloquea el flujo de trabajo |
| Descubrimiento de pruebas | Patrones de directorio + nombre de archivo | Independiente del lenguaje |
| Generación del título | Análisis sintetizado | Lo más preciso |
| Detección de comandos | Detección por archivos del proyecto | Más práctico |
| Modo de salida | Primero terminal, archivo opcional | Flexible |

### Fases de implementación

1. **Fase 1**: creación de la plantilla (frontmatter YAML, configuración de idioma, contexto Git)
2. **Fase 2**: funcionalidad central (integración con Spec, descubrimiento de pruebas, detección de comandos, generación de título)
3. **Fase 3**: gestión de casos límite
4. **Fase 4**: pruebas
5. **Fase 5**: actualización de documentación

### Manifiesto de archivos

**Creados**:

- `templates/commands/pr.md`

**Modificados**:

- `CLAUDE.md`: añadir la descripción del comando
- `README.md`: añadir el comando a la lista

**Pruebas**:

- `tests/test_pr_template.py`

---

## Diagrama completo del flujo

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   CodexSpec SDD Development Flow                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:specify                                                     │
│  ├─ Clarify requirements through Q&A                                    │
│  ├─ User provides reference examples                                    │
│  └─ 10 questions covering language, platform, content, parameters, etc. │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:generate-spec                                               │
│  ├─ Generate a complete spec.md                                         │
│  ├─ 4 user stories, 8 functional requirements, 10 test cases            │
│  └─ Saved to .codexspec/specs/2026-0613-1200ab-pr-description-generator/spec.md │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:review-spec                                                 │
│  ├─ Quality score: 92/100                                               │
│  ├─ Found 2 warnings (test-file discovery, multi-spec handling)         │
│  └─ Status: Pass, can proceed to planning                               │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:clarify  (Critical adjustment)                              │
│  ├─ User surfaces a real-world usage issue                              │
│  ├─ 5 clarification questions, all answered                             │
│  ├─ Key change: --no-spec → --spec (opt-in)                             │
│  └─ Added 5 requirements (REQ-005b, 006b, 008a, 010, updated 007)       │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:design-to-plan                                                │
│  ├─ Update the technical implementation plan                            │
│  ├─ 9 technical decisions, including 5 new ones                         │
│  ├─ 5 implementation phases                                             │
│  └─ Saved to .codexspec/specs/2026-0613-1200ab-pr-description-generator/plan.md │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Subsequent steps (not completed in this session)                       │
│  ├─ /codexspec:review-plan - Validate plan quality                      │
│  ├─ /codexspec:plan-to-tasks - Break down into executable tasks         │
│  └─ /codexspec:implement-tasks - Execute the implementation             │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Aprendizajes clave

### 1. El valor de la etapa clarify

Este caso muestra el papel decisivo del comando `clarify`:

- **El usuario descubre un problema real durante el uso**: el riesgo de usar mal spec.md en escenarios de cambios pequeños
- **Un defecto de diseño se resuelve mediante Q&A clarificador**: pasar de la autodetección a opt-in
- **Los cambios de requisitos se registran de forma sistemática**: todos los cambios quedan en la sección Clarifications de spec.md

### 2. Flexibilidad del flujo SDD

- No es un flujo lineal; puedes retroceder y ajustar en cualquier etapa
- `clarify` puede intercalarse después de `review-spec` y antes de `design-to-plan`
- Tanto el documento de especificación como el plan técnico se actualizan para reflejar el cambio

### 3. Evolución del diseño del parámetro

```
Initial design:
  --no-spec: skip spec.md (used by default)

Final design:
  --spec: enable spec.md (not used by default)
```

Este cambio refleja un giro de "flujo SDD por defecto" a "soportar también flujos no SDD", haciendo la herramienta más general.

### 4. Salidas documentadas

| Etapa | Archivo de salida | Contenido |
|-------|-------------|---------|
| generate-spec | spec.md | Documento de especificación completo |
| review-spec | review-spec.md | Informe de revisión de calidad |
| clarify | (actualiza spec.md) | Registros de clarificación + actualizaciones de requisitos |
| design-to-plan | plan.md | Plan técnico de implementación |

---

## Apéndice: referencia rápida de comandos

```bash
# 1. Initial requirement clarification
/codexspec:specify

# 2. Generate the specification document
/codexspec:generate-spec

# 3. Review the specification quality
/codexspec:review-spec

# 4. Clarify/adjust requirements (optional; use when an issue is found)
/codexspec:clarify [issue description]

# 5. Generate the technical plan
/codexspec:design-to-plan

# 6. Review the plan quality (optional)
/codexspec:review-plan

# 7. Break down into tasks
/codexspec:plan-to-tasks

# 8. Execute the implementation
/codexspec:implement-tasks
```

---

*Este documento fue generado por el flujo de trabajo SDD de CodexSpec y recoge una conversación real de desarrollo.*

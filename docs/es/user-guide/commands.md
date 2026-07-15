# Comandos

Esta es la referencia de los slash commands de CodexSpec. Estos comandos se invocan en la interfaz de chat de Claude Code.

Para ver los patrones de flujo de trabajo y cuándo usar cada comando, consulta [Flujo de trabajo](workflow.md). Para los comandos de la CLI, consulta [CLI](../reference/cli.md).

## Referencia rápida

Agrupados por categoría, reflejando el catálogo del README. Dentro de cada grupo, los comandos aparecen en el orden del flujo de trabajo.

### Comandos del flujo de trabajo principal

| Comando | Propósito |
|---------|---------|
| `/codexspec:constitution` | Crear o actualizar la constitución del proyecto con validación entre artefactos |
| `/codexspec:specify` | Aclarar, confirmar y persistir requisitos en `requirements.md` |
| `/codexspec:generate-spec` | Generar el documento `spec.md` a partir de los requisitos aclarados (★ Auto-revisión) |
| `/codexspec:spec-to-plan` | Convertir la especificación en un plan de implementación técnica (★ Auto-revisión) |
| `/codexspec:plan-to-tasks` | Desglosar el plan en tareas trazables y verificables (★ Auto-revisión) |
| `/codexspec:implement-tasks` | Ejecutar tareas con flujo de trabajo TDD condicional |

### Comandos de revisión (puertas de calidad)

| Comando | Propósito |
|---------|---------|
| `/codexspec:review-spec` | Validar la completitud y calidad de la especificación |
| `/codexspec:review-plan` | Revisar la viabilidad y alineación del plan técnico |
| `/codexspec:review-tasks` | Validar la cobertura, el orden y la viabilidad de las tareas |

### Comandos de mejora

| Comando | Propósito |
|---------|---------|
| `/codexspec:config` | Gestionar la configuración del proyecto de forma interactiva (crear/ver/modificar/restablecer) |
| `/codexspec:clarify` | Escanear una especificación existente en busca de ambigüedades (4 categorías, máximo 5 preguntas) |
| `/codexspec:analyze` | Análisis de consistencia entre artefactos (solo lectura, basado en severidad) |
| `/codexspec:checklist` | Generar checklists de calidad de requisitos |
| `/codexspec:tasks-to-issues` | Convertir tareas en GitHub Issues |

### Comandos del flujo de trabajo con Git

| Comando | Propósito |
|---------|---------|
| `/codexspec:commit-staged` | Generar un mensaje de commit a partir de los cambios en staging (consciente del contexto de sesión) |
| `/codexspec:pr` | Generar una descripción de PR/MR a partir del git diff (detecta la plataforma automáticamente) |

### Comandos de revisión de código

| Comando | Propósito |
|---------|---------|
| `/codexspec:review-code` | Puerta de defectos para cambios; puntuación por ruta con `--audit` |
| `/codexspec:review-python-code` | Revisar código Python (PEP 8, seguridad de tipos, robustez, consistencia con la constitución) |
| `/codexspec:review-react-code` | Revisar código React/TypeScript (arquitectura de componentes, reglas de Hooks, estado, rendimiento) |

### Vía rápida

| Comando | Propósito |
|---------|---------|
| `/codexspec:quick` | Ejecutar un flujo Requirements-First SDD simplificado para cambios pequeños |

---

## Categorías de comandos

### Comandos del flujo de trabajo principal

Comandos para el flujo de trabajo principal de Requirements-First SDD: Constitución → Requisitos Confirmados → Especificación → Plan → Tareas → Implementación. Aquí los requisitos confirmados son la autoridad de máxima prioridad: nada en la cadena es vinculante hasta que lo confirmes explícitamente en la Confirmation Gate.

### Comandos de revisión (puertas de calidad)

Comandos que validan los artefactos en cada etapa del flujo de trabajo bajo un contrato de **revisión basada en evidencia**: cada defecto debe incluir `Evidence`, `Location`, `Mismatch`, `Impact` y `Remediation` concretos. Las sugerencias de diseño consultivas se reportan por separado y nunca cambian el estado ni disparan cambios automáticos. Los defectos verificados pueden corregirse y volver a revisarse durante un máximo de dos rondas; los avisos siguen siendo opcionales en todo momento.

### Comandos de mejora

Comandos para el refinamiento iterativo, la validación entre artefactos, la configuración y la integración con la gestión de proyectos.

### Comandos del flujo de trabajo con Git

Comandos que convierten el trabajo terminado en artefactos compartibles: mensajes de commit a partir del diff en staging y descripciones estructuradas de PR/MR a partir del diff de la rama.

### Comandos de revisión de código

Comandos que revisan código fuente (cualquier lenguaje, específicos para Python, específicos para React/TypeScript) en busca de claridez idiomática, corrección, robustez, arquitectura y alineación con la constitución. Los hallazgos aplican la misma disciplina de severidad que las revisiones de artefactos: los problemas CRITICAL/HIGH deben citar evidencia concreta; las sugerencias LOW son únicamente consultivas.

### Vía rápida

Un comando simplificado que ejecuta el flujo Requirements-First SDD de extremo a extremo para cambios pequeños y bien delimitados.

---

## Referencia de comandos

### `/codexspec:constitution`

Crea o actualiza la constitución del proyecto. La constitución define los principios arquitectónicos, el stack tecnológico, los estándares de código y las reglas de gobernanza que guían todas las decisiones de desarrollo posteriores.

**Sintaxis:**

```
/codexspec:constitution [descripción de principios]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `descripción de principios` | No | Descripción de los principios a incluir (se solicitará si no se proporciona) |

**Lo que hace:**

- Crea `.codexspec/memory/constitution.md` si no existe
- Actualiza la constitución existente con nuevos principios
- Valida la consistencia entre artefactos con las plantillas
- Genera un Informe de Impacto de Sincronización que muestra los cambios y los archivos afectados
- Incluye una revisión de constitucionalidad para las plantillas dependientes

**Lo que crea:**

```
.codexspec/
└── memory/
    └── constitution.md    # Documento de gobernanza del proyecto
```

**Ejemplo:**

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

**Consejos:**

- Define los principios al inicio del proyecto para una toma de decisiones consistente
- Incluye tanto principios técnicos como de proceso
- Revisa la constitución antes de desarrollar funcionalidades importantes
- Los cambios en la constitución disparan validación entre artefactos

---

### `/codexspec:specify`

Aclara los requisitos mediante preguntas y respuestas interactivas, confirma el resumen resultante y lo persiste para sesiones posteriores.

**Sintaxis:**

```
/codexspec:specify [tu idea o requisito]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `tu idea o requisito` | No | Descripción inicial de lo que quieres construir (se solicitará si no se proporciona) |

**Lo que hace:**

- Hace preguntas aclaratorias para entender tu idea
- Explora casos extremos que quizás no habías considerado
- Cocrea requisitos de alta calidad mediante el diálogo
- Se centra en el "qué" y el "porqué", no en la implementación técnica
- Asigna IDs estables a necesidades, restricciones, decisiones, exclusiones y preguntas abiertas confirmadas
- Registra evidencia del usuario y un registro de confirmación
- Crea el espacio de trabajo de la funcionalidad y `requirements.md`

**Lo que crea:**

```text
.codexspec/specs/{feature-id}-{feature-name}/requirements.md
```

Solo los elementos confirmados se convierten en requisitos autoritativos. Las preguntas abiertas permanecen explícitamente abiertas. Esta es la Confirmation Gate para los requisitos: nada es vinculante hasta que confirmes explícitamente el resumen final.

**Ejemplo:**

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

**Consejos:**

- Úsalo para la exploración inicial de requisitos
- No te preocupes por ser completo: el refinamiento es iterativo
- Pregunta si la IA hace suposiciones
- Revisa el resumen antes de generar la especificación

---

### `/codexspec:generate-spec`

Genera el documento `spec.md` a partir de los requisitos aclarados. Este comando actúa como un "compilador de requisitos" que transforma tus requisitos aclarados en una especificación estructurada.

**Sintaxis:**

```
/codexspec:generate-spec
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| Ruta de la funcionalidad | No | Directorio de funcionalidad explícito, `requirements.md` o `spec.md` destino; obligatorio cuando la resolución es ambigua |

**Lo que hace:**

- Lee los requisitos confirmados del espacio de trabajo de la funcionalidad seleccionado
- Admite espacios de trabajo heredados que solo contienen `spec.md`, con una advertencia explícita de trazabilidad
- Genera un `spec.md` completo con:
  - Resumen y objetivos de la funcionalidad
  - Historias de usuario con criterios de aceptación
  - Requisitos funcionales (formato REQ-XXX)
  - Requisitos no funcionales (formato NFR-XXX)
  - Casos extremos y enfoques de manejo
  - Elementos fuera de alcance
- Añade referencias `Sources` hacia los IDs de requisitos
- Se detiene para confirmación del usuario en lugar de resolver conflictos de autoridad por suposición
- Revisa automáticamente y puede reparar defectos con evidencia durante un máximo de dos rondas

**Lo que crea:**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── spec.md
```

**Ejemplo:**

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

**Consejos:**

- Ejecútalo después de que `/codexspec:specify` haya aclarado los requisitos
- Revisa la especificación generada antes de continuar
- Usa `/codexspec:review-spec` para validación de calidad
- Edita spec.md directamente si necesitas ajustes menores

---

### `/codexspec:clarify`

Escanea una especificación existente en busca de ambigüedades y vacíos. Úsalo para refinamiento iterativo tras la creación inicial de la especificación.

**Sintaxis:**

```
/codexspec:clarify [ruta_a_spec.md]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `ruta_a_spec.md` | No | Ruta al archivo de especificación (se detecta automáticamente si no se proporciona) |

**Lo que hace:**

- Escanea requisitos y especificación usando categorías de ambigüedad enfocadas
- Hace preguntas de aclaración dirigidas (máximo 5)
- Actualiza primero `requirements.md` tras la confirmación del usuario, luego sincroniza `spec.md`
- Se integra con los hallazgos de review-spec si están disponibles

**Categorías de ambigüedad:**

| Categoría | Lo que detecta |
|----------|-----------------|
| **Vacíos de completitud** | Secciones faltantes, contenido vacío, criterios de aceptación ausentes |
| **Problemas de especificidad** | Términos vagos ("rápido", "escalable"), restricciones indefinidas |
| **Claridad de comportamiento** | Vacíos en manejo de errores, transiciones de estado indefinidas |
| **Problemas de medibilidad** | Requisitos no funcionales sin métricas |

**Ejemplo:**

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

**Consejos:**

- Úsalo cuando spec.md existe pero necesita refinamiento
- Se integra con los hallazgos de `/codexspec:review-spec`
- Máximo 5 preguntas por sesión
- Ejecútalo varias veces para especificaciones complejas

---

### `/codexspec:spec-to-plan`

Convierte la especificación de la funcionalidad en un plan de implementación técnica. Aquí es donde defines **cómo** se construirá la funcionalidad.

**Sintaxis:**

```
/codexspec:spec-to-plan [ruta_a_spec.md]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `ruta_a_spec.md` | No | Ruta al archivo de especificación (se detecta automáticamente desde `.codexspec/specs/` si no se proporciona) |

**Lo que hace:**

- Lee la especificación y la constitución
- Incluye solo el detalle técnico que requieren los requisitos confirmados y las restricciones del repositorio
- Comprueba las reglas aplicables de la constitución sin tratar convenciones opcionales como requisitos de la funcionalidad
- Añade enlaces `Covers` a los requisitos de la especificación
- Documenta las decisiones técnicas con su justificación
- Se detiene cuando una decisión cambiaría la intención confirmada

**Lo que crea:**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── plan.md    # Plan de implementación técnica
```

**Ejemplo:**

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

**Consejos:**

- Ejecútalo después de que la especificación esté revisada y estable
- Las reglas aplicables de la constitución son obligatorias; las convenciones de plantilla irrelevantes no lo son
- Incluye las secciones relevantes según el tipo de proyecto
- Revisa el plan antes de continuar con las tareas

---

### `/codexspec:plan-to-tasks`

Desglosa el plan técnico en tareas accionables con cobertura explícita y resultados verificables.

**Sintaxis:**

```
/codexspec:plan-to-tasks [ruta_a_spec.md ruta_a_plan.md]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `rutas` | No | Rutas a la especificación y al plan (se detectan automáticamente si no se proporcionan) |

**Lo que hace:**

- Crea tareas con un resultado verificable; una tarea puede tocar varios archivos relacionados
- Usa orden test-first solo cuando lo requiere el plan, la constitución, las necesidades confirmadas o el riesgo
- Marca las tareas `[P]` solo cuando son genuinamente independientes
- Especifica las rutas de archivo exactas para cada tarea
- Añade enlaces `Covers` a los IDs del plan y de los requisitos

**Lo que crea:**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── tasks.md    # Desglose de tareas
```

**Estructura de tareas:**

```markdown
### Task 2.1: Write Tests for Entity A [P]
- **Type**: Testing
- **Files**: `tests/test_entity_a.py`
- **Description**: Write unit tests for Entity A
- **Dependencies**: Task 1.3
- **Est. Complexity**: Low
```

**Ejemplo:**

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

**Consejos:**

- Cada tarea debe producir un resultado verificable y puede tocar archivos estrechamente relacionados
- Las tareas de prueba preceden a la implementación solo cuando se requiere test-first
- `[P]` marca tareas paralelizables verdaderamente independientes
- Revisa las dependencias antes de la implementación

---

### `/codexspec:implement-tasks`

Ejecuta las tareas de implementación con un flujo de trabajo TDD condicional. Recorre la lista de tareas de forma sistemática.

**Sintaxis:**

```
/codexspec:implement-tasks [ruta_tareas]
/codexspec:implement-tasks [ruta_spec ruta_plan ruta_tareas]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `ruta_tareas` | No | Ruta a tasks.md (se detecta automáticamente si no se proporciona) |
| `ruta_spec ruta_plan ruta_tareas` | No | Rutas explícitas a los tres documentos |

**Resolución de archivos:**

- **Sin argumentos**: Se detecta automáticamente desde `.codexspec/specs/`
- **Un argumento**: Se trata como ruta de `tasks.md`, las demás se deducen del mismo directorio
- **Tres argumentos**: Rutas explícitas a spec.md, plan.md y tasks.md

**Lo que hace:**

- Lee tasks.md e identifica las tareas incompletas
- Aplica el flujo TDD para tareas de código:
  - **Red**: Escribe primero las pruebas que fallan
  - **Green**: Implementa para que pasen las pruebas
  - **Verifica**: Ejecuta todas las pruebas
  - **Refactoriza**: Mejora manteniendo las pruebas en verde
- Implementación directa para tareas no testeables (documentación, configuración)
- Actualiza las casillas de verificación de las tareas a medida que avanza el trabajo
- Registra bloqueos en issues.md si los encuentra

**Flujo TDD para tareas de código:**

```
Red → Green → Verify → Refactor → Mark Complete
```

**Implementación directa para lo no testeable:**

- Archivos de documentación
- Archivos de configuración
- Recursos estáticos
- Archivos de infraestructura

**Ejemplo:**

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

**Consejos:**

- Puede reanudarse donde se dejó si se interrumpe
- Los bloqueos se registran en issues.md
- Los commits se hacen después de tareas/fases significativas
- Ejecuta primero `/codexspec:review-tasks` para validación

---

### `/codexspec:review-spec`

Valida la especificación frente a los requisitos confirmados y su propia calidad interna.

**Sintaxis:**

```
/codexspec:review-spec [ruta_a_spec.md]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `ruta_a_spec.md` | No | Ruta al archivo de especificación (se detecta automáticamente si no se proporciona) |

**Lo que hace:**

- Comprueba la fidelidad a las entradas confirmadas de `requirements.md`
- Comprueba la consistencia interna, la claridad y la verificabilidad
- Trata una sección de plantilla faltante como defecto solo cuando el contenido autoritativo la requiere
- Exige que cada defecto incluya `Evidence`, `Location`, `Mismatch`, `Impact` y `Remediation`
- Separa los `Risk Advisories / Design Opportunities` de los defectos
- Genera un estado más una puntuación de compatibilidad derivada de los hallazgos clasificados

**Contrato de revisión compartido:**

| Categoría | Significado |
|----------|---------|
| Defecto de fidelidad | Conflicta con una fuente autoritativa o la omite |
| Defecto intrínseco | Internamente contradictorio, inviable o no verificable |
| Aviso | Mejora opcional sin evidencia de un defecto actual |

El estado es `PASS`, `PASS_WITH_WARNINGS`, `NEEDS_REVISION` o `BLOCKED`. Los avisos nunca cambian el estado ni la puntuación.

**Ejemplo:**

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

**Consejos:**

- Ejecútalo antes de `/codexspec:spec-to-plan`
- Trata `BLOCKED` y `NEEDS_REVISION` como no listos para continuar
- No promuevas avisos a requisitos
- Vuelve a ejecutarlo tras aplicar correcciones

---

### `/codexspec:review-plan`

Revisa el plan de implementación técnica en busca de fidelidad, viabilidad y decisiones técnicas justificadas.

**Sintaxis:**

```
/codexspec:review-plan [ruta_a_plan.md]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `ruta_a_plan.md` | No | Ruta al archivo del plan (se detecta automáticamente si no se proporciona) |

**Lo que hace:**

- Verifica los enlaces `Covers` y la cobertura requerida de la especificación
- Comprueba las reglas aplicables de la constitución y los hechos del repositorio
- Marca complejidad injustificada solo cuando crea un coste o conflicto concreto
- Exige los campos de evidencia para cada defecto y fusiona hallazgos con la misma causa raíz
- Reporta mejoras de arquitectura opcionales como avisos
- Usa el contrato compartido de estado y puntuación de compatibilidad

**Ejemplo:**

```text
You: /codexspec:review-plan

AI:  Overall Status: PASS
     Compatibility Score: 100/100
     Verified defects: none

     Risk Advisories / Design Opportunities:
     - A caching layer may become useful if production measurements exceed
       the confirmed latency target. It is not required by the current plan.
```

**Consejos:**

- Ejecútalo antes de `/codexspec:plan-to-tasks`
- Resuelve los defectos con evidencia antes de la generación de tareas
- Mantén las ideas especulativas de arquitectura en la sección de avisos
- Verifica que el stack tecnológico se alinea con las habilidades del equipo

---

### `/codexspec:review-tasks`

Valida el desglose de tareas en cuanto a cobertura, resultados verificables, orden correcto y dependencias viables.

**Sintaxis:**

```
/codexspec:review-tasks [ruta_a_tasks.md]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `ruta_a_tasks.md` | No | Ruta al archivo de tareas (se detecta automáticamente si no se proporciona) |

**Lo que hace:**

- Comprueba que todos los elementos requeridos del plan y los requisitos tengan cobertura de tareas
- Valida el orden test-first solo donde una fuente autoritativa lo requiere
- Verifica que cada tarea tenga un resultado verificable
- Valida las dependencias (sin ciclos, orden correcto)
- Revisa los marcadores de paralelización
- Valida las rutas de archivo
- Exige los campos de evidencia para cada defecto
- Reporta refinamientos de proceso opcionales como avisos
- Usa el contrato compartido de estado y puntuación de compatibilidad

**Ejemplo:**

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

**Consejos:**

- Ejecútalo antes de `/codexspec:implement-tasks`
- Los hallazgos de orden de pruebas son defectos solo cuando una fuente autoritativa requiere testing
- Comprueba que los marcadores de paralelización sean precisos
- Verifica que las rutas de archivo coincidan con la estructura del proyecto

---

### `/codexspec:analyze`

Realiza un análisis de consistencia no destructivo entre requirements.md, spec.md, plan.md y tasks.md. Identifica conflictos de autoridad, vacíos de trazabilidad, duplicación y cobertura faltante.

**Sintaxis:**

```
/codexspec:analyze
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| Ninguno | - | Analiza los artefactos de la funcionalidad actual |

**Lo que hace:**

- Detecta duplicaciones entre artefactos
- Identifica ambigüedades que carecen de criterios medibles
- Encuentra elementos poco especificados
- Comprueba la alineación con la constitución
- Mapea la cobertura de requisitos a tareas
- Reporta inconsistencias en terminología y orden

**Niveles de severidad:**

| Nivel | Definición |
|-------|------------|
| **CRITICAL** | Violación de la constitución, artefacto central faltante, cobertura cero |
| **HIGH** | Requisito duplicado/en conflicto, atributo de seguridad ambiguo |
| **MEDIUM** | Deriva terminológica, cobertura no funcional faltante |
| **LOW** | Mejoras de estilo/redacción |

**Ejemplo:**

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

**Consejos:**

- Ejecútalo después de `/codexspec:plan-to-tasks`, antes de la implementación
- Los problemas CRITICAL deberían bloquear la implementación
- Análisis de solo lectura: no se modifican archivos
- Usa los hallazgos para mejorar la calidad de los artefactos

---

### `/codexspec:checklist`

Genera checklists de calidad para validar la completitud, claridad y consistencia de los requisitos. Son "pruebas unitarias para la redacción de requisitos".

**Sintaxis:**

```
/codexspec:checklist [área_de_enfoque]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `área_de_enfoque` | No | Enfoque de dominio (p. ej., "ux", "api", "security", "performance") |

**Lo que hace:**

- Genera checklists organizadas por dimensiones de calidad
- Crea checklists en el directorio `FEATURE_DIR/checklists/`
- Los elementos se centran en la calidad de los requisitos, no en las pruebas de implementación

**Dimensiones de calidad:**

- **Completitud de requisitos**: ¿Están presentes todos los requisitos necesarios?
- **Claridad de requisitos**: ¿Los requisitos son específicos y sin ambigüedades?
- **Consistencia de requisitos**: ¿Los requisitos se alinean sin conflictos?
- **Calidad de los criterios de aceptación**: ¿Los criterios de éxito son medibles?
- **Cobertura de escenarios**: ¿Se abordan todos los flujos/casos?
- **Cobertura de casos extremos**: ¿Están definidas las condiciones de frontera?
- **Requisitos no funcionales**: ¿Se especifican rendimiento, seguridad, accesibilidad?
- **Dependencias y supuestos**: ¿Están documentados?

**Ejemplos de tipos de checklist:**

- `ux.md` - Jerarquía visual, estados de interacción, accesibilidad
- `api.md` - Formatos de error, limitación de tasa, autenticación
- `security.md` - Protección de datos, modelo de amenazas, respuesta a brechas
- `performance.md` - Métricas, condiciones de carga, degradación

**Ejemplo:**

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

**Consejos:**

- Las checklists validan la calidad de los requisitos, no la corrección de la implementación
- Úsalas para la revisión y mejora de requisitos
- Crea checklists específicas de dominio para validación enfocada
- Ejecútalo antes de pasar a la planificación técnica

---

### `/codexspec:tasks-to-issues`

Convierte tareas de `tasks.md` en GitHub issues para el seguimiento y la colaboración del proyecto.

**Sintaxis:**

```
/codexspec:tasks-to-issues
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| Ninguno | - | Convierte todas las tareas de la funcionalidad actual |

**Lo que hace:**

- Analiza IDs de tareas, descripciones, dependencias y rutas de archivo
- Crea GitHub issues con un cuerpo estructurado
- Añade etiquetas según el tipo de tarea (setup, implementation, testing, documentation)
- Vincula dependencias entre issues
- Reporta las issues creadas con sus URLs

**Requisitos previos:**

- Repositorio Git con remoto en GitHub
- GitHub CLI (`gh`) instalada y autenticada
- El archivo `tasks.md` existe

**Ejemplo:**

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

**Consejos:**

- Requiere autenticación con GitHub CLI (`gh auth login`)
- Solo funciona con repositorios de GitHub
- Crea issues en la configuración predeterminada del repositorio
- Comprueba si hay duplicados antes de ejecutarlo

---

### `/codexspec:commit-staged`

Genera un mensaje de commit conforme a Conventional Commits basado en los cambios en staging de git, con conciencia del contexto de sesión. Este comando entiende tu sesión de desarrollo para generar mensajes de commit significativos.

**Sintaxis:**

```
/codexspec:commit-staged [-p]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `-p` | No | Modo vista previa: muestra el mensaje sin hacer commit |

**Lo que hace:**

- Ejecuta `git diff --staged` para recuperar los cambios en staging
- Analiza los cambios y el contexto de la sesión para entender la intención
- Sigue la especificación Conventional Commits
- En modo ejecución (predeterminado): hace commit directamente tras generar el mensaje
- En modo vista previa (`-p`): muestra el mensaje sin hacer commit
- Reporta un error si no hay cambios en staging

**Ejemplo:**

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

**Ejemplo de modo vista previa:**

```text
You: /codexspec:commit-staged -p

AI:  Preview mode - no commit will be executed

     Suggested commit message:
     feat(auth): implement token refresh logic

     - Add refresh token generation
     - Include token expiration handling
     - Add tests for refresh flow
```

**Consejos:**

- Haz staging de los cambios primero con `git add`
- Solo analiza el contenido en staging: respetal flujo de commit en dos etapas de Git
- Considera el contexto de la sesión para mensajes de commit significativos
- Usa el flag `-p` para vista previa antes de hacer commit
- Sigue la especificación Conventional Commits por defecto

---

### `/codexspec:review-code`

Revisa el cambio Git seleccionado como una puerta de defectos estricta antes de fusionarlo. El objetivo predeterminado incluye la diferencia completa de la funcionalidad; los selectores explícitos eligen cambios confirmados, no confirmados o un solo commit, pero no aceptan filtros de ruta.

<!-- REVIEW-CODE-BREAKING: DEFAULT-GATE -->
<!-- REVIEW-CODE-BREAKING: PATH-AUDIT -->

**Cambio incompatible en la próxima versión:**

- El comando predeterminado ahora es una puerta de defectos centrada en cambios, no una puntuación general de calidad.
- Las rutas posicionales ya no son válidas. Usa `--audit` explícitamente para la puntuación consultiva de calidad por ruta.

**Sintaxis de la puerta de defectos:**

```text
/codexspec:review-code
/codexspec:review-code --committed [--base <branch>] [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code --uncommitted [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code --commit <sha> [--parent <n>] [--feature <feature-dir>] [--focus <instructions>]
```

La puerta inventaría todos los artefactos seleccionados, evalúa los requisitos aplicables y ejecuta las fases Scope, Behavior, Risk y Verification. El resultado es `PASS`, `FAIL` o `INCONCLUSIVE`. Tras seis secciones del informe aparece un único envelope `<review-code-result>` legible por máquinas. Cualquier hallazgo P0-P3 produce `FAIL`; la falta de evidencia obligatoria produce `INCONCLUSIVE`.

```text
You: /codexspec:review-code --feature .codexspec/specs/2026-0714-example

AI:  ## Verdict
     **PASS** — la revisión y verificación obligatorias terminaron sin hallazgos.
```

<!-- REVIEW-CODE-AUDIT -->

#### Auditoría de calidad por ruta

La rama audit explícita revisa el contenido actual completo de los archivos para evaluar claridad idiomática, corrección, robustez, arquitectura y alineación constitucional. La puntuación es consultiva y no puede completar `implement-tasks`.

**Sintaxis:**

```
/codexspec:review-code --audit [paths...]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `ruta...` | No | Uno o más archivos o directorios fuente a revisar (separados por espacios). Por defecto `src/` si se omite |

**Lo que hace:**

- Detecta el lenguaje o lenguajes principales a partir de las extensiones de archivo y ejecuta una pasada por idioma para objetivos multilenguaje
- Ejecuta herramientas de análisis estático cuando su configuración está presente (`ruff`/`mypy`, `eslint`/`tsc`, `go vet`/`gofmt`, `cargo check`/`cargo clippy`, `shellcheck`); si no, las omite elegantemente y reporta cobertura degradada
- Puntúa cuatro dimensiones: Claridad y simplicidad idiomática, Corrección y contratos explícitos, Robustez en tiempo de ejecución y disciplina de recursos, e Integridad arquitectónica y de diseño
- Inyecta subsecciones obligatorias para los frameworks detectados (p. ej., Cumplimiento de Hooks para React, Ownership y Borrowing para Rust, Disciplina de Goroutine y Context para Go, Seguridad de Memoria y Lifetime para C/C++, Seguridad de Ejecución para Shell)
- Referencia cruzada los hallazgos contra `.codexspec/memory/constitution.md` cuando está presente; si está ausente, el eje de constitución se descarta y su peso se redistribuye
- Clasifica los hallazgos por severidad: CRITICAL, HIGH, MEDIUM, LOW (las sugerencias LOW se limitan a una deducción total de 5 puntos)

**Ejemplo:**

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

**Consejos:**

- Pasa varias rutas para revisar una porción enfocada, p. ej., `src/ tests/`
- La puntuación es consultiva; los hallazgos CRITICAL/HIGH son la señal accionable
- Para proyectos solo Python o solo React, prefiere los dedicados `/codexspec:review-python-code` o `/codexspec:review-react-code` para comprobaciones más profundas y específicas del lenguaje
- Vuelve a ejecutarlo tras las correcciones para confirmar que la puntuación se recupera (se espera ≥ 95 una vez resueltos los problemas CRITICAL/HIGH)

---

### `/codexspec:review-python-code`

Revisa código Python en busca de cumplimiento de PEP 8, seguridad de tipos, robustez de ingeniería y consistencia con la constitución.

**Sintaxis:**

```
/codexspec:review-python-code [ruta...]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `ruta...` | No | Uno o más archivos o directorios Python a revisar (separados por espacios). Por defecto `src/` si se omite |

**Lo que hace:**

- Ejecuta `ruff check` para resultados de PEP 8 / linting y `mypy` para resultados de comprobación de tipos
- Revisa cuatro dimensiones específicas de Python: Principio Pythonic y KISS, Seguridad y explicitud de tipos, Robustez de ingeniería y Alineación con la constitución
- Comprueba la completitud de anotaciones de tipo, el manejo de excepciones amplias y la preservación del contexto `raise ... from err`
- Valida la gestión de recursos (gestores de contexto `with`), la corrección de async/await y la disciplina de `logging` estructurado
- Referencia cruzada los hallazgos contra los principios MUST/SHOULD de `.codexspec/memory/constitution.md` cuando está presente
- Clasifica los hallazgos por severidad: CRITICAL (violaciones MUST de la constitución, errores lógicos, vulnerabilidades de seguridad), HIGH (vacíos de seguridad de tipos, errores de ruff/mypy, fugas de recursos), MEDIUM (oportunidades de diseño/refactor, anotaciones faltantes), LOW (legibilidad, azúcar Pythonic)

**Ejemplo:**

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

**Consejos:**

- Úsalo en lugar de `/codexspec:review-code` cuando el objetivo sea solo Python y quieras la profundidad de PEP 8 / seguridad de tipos
- Tanto `ruff` como `mypy` deben estar instalados y configurados en el proyecto destino para cobertura completa; el comando reporta cobertura degradada cuando están ausentes
- Los principios MUST de la constitución se puntúan; los metaprincipios generales del lenguaje (testeabilidad, simplicidad) aplican cuando no existe constitución

---

### `/codexspec:review-react-code`

Revisa código React/TypeScript en busca de arquitectura de componentes, reglas de Hooks, gestión de estado, rendimiento y consistencia con la constitución.

**Sintaxis:**

```
/codexspec:review-react-code [ruta...]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `ruta...` | No | Uno o más archivos o directorios React/TypeScript a revisar (separados por espacios; espera `.tsx`, `.ts`, `.jsx`, `.js`). Por defecto `src/` si se omite |

**Lo que hace:**

- Ejecuta `npx eslint` (cuando existe configuración de ESLint) y `npx tsc --noEmit` (cuando existe un `tsconfig.json`)
- Revisa cuatro dimensiones específicas de React: Atomicidad y responsabilidad única del componente, Cumplimiento de Hooks y gestión de efectos secundarios, Gestión de estado y flujo de datos, y Rendimiento y robustez
- Verifica que los arrays de dependencias de `useEffect` sean exhaustivos, detecta el uso indebido de estado derivado como estado y marca efectos innecesarios
- Comprueba riesgos de closures obsoletos, falta de limpieza de efectos, prop drilling, renders costosos sin memoización y ausencia de estados de carga/error
- Referencia cruzada los hallazgos contra `.codexspec/memory/constitution.md` cuando está presente
- Clasifica los hallazgos por severidad: CRITICAL (violaciones de reglas de Hooks, condiciones de carrera), HIGH (falta de limpieza, rechazos de promesas no manejados), MEDIUM (candidatos a refactor), LOW (legibilidad)

**Ejemplo:**

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

**Consejos:**

- Úsalo en lugar de `/codexspec:review-code` cuando el objetivo sea solo React/TypeScript y quieras profundidad en Hooks y arquitectura de componentes
- Deben estar presentes tanto ESLint como un `tsconfig.json` para cobertura completa; el comando reporta cobertura degradada cuando están ausentes
- Los hallazgos de React se superponen a las comprobaciones base de TypeScript, por lo que los problemas de seguridad de tipos siguen apareciendo

---

### `/codexspec:quick`

Ejecuta un flujo Requirements-First SDD simplificado para cambios pequeños.

**Sintaxis:**

```
/codexspec:quick [describe un requisito pequeño]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `describe un requisito pequeño` | No | Descripción breve del cambio pequeño y bien delimitado (se solicitará si no se proporciona) |

**Lo que hace:**

- Evalúa el alcance (archivos afectados, extensión del módulo, nuevas dependencias, decisiones de producto sin resolver) y, si el cambio es amplio o tiene varios resultados independientes, recomienda el flujo estándar
- Crea un espacio de trabajo de funcionalidad y `requirements.md` usando la misma convención de marca de tiempo que `/codexspec:specify`
- Resuelve solo ambigüedades que cambien materialmente la implementación; presenta un resumen conciso confirmado (`NEED-*`, `CON-*`/`DEC-*` relevantes, `OUT-*`, `OPEN-*` sin resolver)
- Se detiene en la Confirmation Gate: no se genera nada hasta que confirmes el resumen
- Encadena los comandos de generación contra el nuevo directorio de la funcionalidad: `/codexspec:generate-spec`, `/codexspec:spec-to-plan`, `/codexspec:plan-to-tasks`, `/codexspec:implement-tasks`
- Difiere al propio bucle de auto-revisión de cada comando de generación; hace una pausa y pregunta al usuario si una revisión necesita una decisión nueva de producto o arquitectura
- Reporta el directorio de la funcionalidad, las rutas de los artefactos, los resultados de las revisiones, la verificación de la implementación y los avisos sin resolver por separado

**Lo que crea:**

```text
.codexspec/specs/{timestamp}-{feature-name}/
├── requirements.md
├── spec.md
├── plan.md
└── tasks.md
```

**Ejemplo:**

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

**Consejos:**

- Reserva Quick para cambios genuinamente pequeños y de un único resultado; en caso contrario ejecuta `/codexspec:specify` y el flujo estándar
- La confirmación sigue siendo obligatoria: Quick nunca infiere una decisión de producto para mantener la automatización en marcha
- Si alguna revisión de generación devuelve `NEEDS_REVISION`/`BLOCKED`, Quick se detiene y te devuelve el control

---

### `/codexspec:pr`

Genera una descripción estructurada de GitHub Pull Request / GitLab Merge Request a partir del git diff. Opcionalmente integra `spec.md` para contexto trazado por SDD.

**Sintaxis:**

```
/codexspec:pr [--target-branch <rama>] [--sections <lista>] [--spec <id-o-ruta>] [--output <archivo>]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `--target-branch <rama>` | No | Rama contra la que comparar (predeterminada: `origin/main`) |
| `--sections <lista>` | No | Subconjunto separado por comas de `summary, changes, testing, verify, checklist, notes` (predeterminado: `all`) |
| `--spec <id-o-ruta>` | No | Integración opt-in de spec: un id de funcionalidad (p. ej., `2025-0321-1430k7-auth`) resuelto bajo `.codexspec/specs/`, o una ruta `path/to/spec.md` explícita. Omitir para generar solo desde git |
| `--output <archivo>` | No | Guardar la descripción en un archivo en lugar de la terminal |

**Lo que hace:**

- Recopila el contexto de git (rama actual, URL del remoto, commits por delante, cambios de archivo, diff completo, mensajes de commit) contra la rama objetivo
- Detecta automáticamente la plataforma desde la URL del remoto: GitHub → "Pull Request", GitLab → "Merge Request", otro/ninguno → por defecto terminología de GitHub con una advertencia
- Carga `.codexspec/memory/constitution.md` cuando está presente y alinea la descripción con los estándares de documentación/revisión de código
- Respeta `language.commit` (luego `language.output`, luego inglés) para el idioma de la descripción; los términos técnicos (API, JWT, PR, MR) permanecen en inglés cuando procede
- Cuando se proporciona `--spec`, añade una sección de Contexto con historias de usuario y requisitos extraídos de spec.md; en caso contrario genera puramente desde el diff
- Emite secciones según `--sections` (Resumen, Cambios, Pruebas, Pasos de verificación, Checklist pre-fusión, Notas / Cambios disruptivos)

**Ejemplo:**

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

**Consejos:**

- Omite `--spec` para correcciones de errores pequeñas o cambios sin especificación formal
- Combínalo con `/codexspec:commit-staged` para producir tanto un mensaje de commit como una descripción de PR a partir del mismo trabajo
- Consulta el [caso de estudio del generador de descripciones de PR](../case-studies/case-study-pr-description-generator.md) para un ejemplo completo de extremo a extremo de este comando (incluyendo cómo se conecta el contexto de spec.md)

---

### `/codexspec:config`

Gestiona la configuración del proyecto de forma interactiva (crear/ver/modificar/restablecer). Es la contrapartida en slash command de la CLI `codexspec config`, ideal para instalaciones del Plugin Marketplace.

**Sintaxis:**

```
/codexspec:config [--view]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `--view` | No | Muestra la configuración actual sin modificarla. Sin argumentos, abre el menú interactivo de gestión |

**Lo que hace:**

- Afecta exclusivamente a `.codexspec/config.yml`
- `--view` (o la opción de menú "View current config") imprime el archivo en un formato legible; reporta "Configuration Not Found" si está ausente
- El modo interactivo, cuando existe una configuración, ofrece: Ver, Modificar, Restablecer a valores predeterminados, Cancelar
- Si no existe configuración, ejecuta el flujo de creación que escribe una configuración mínima solo con `output` (interaction/document/commit se resuelven a `output`, luego `en`, así que un archivo solo con `output` es totalmente funcional)
- Permite ajustar cada dimensión de idioma de forma independiente (output, interaction, document, commit) y activar opciones del flujo de trabajo como `auto_next`

**Lo que crea/edita:**

```
.codexspec/config.yml
```

**Ejemplo:**

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

**Consejos:**

- Usa `/codexspec:config --view` para inspeccionar el estado actual antes de cambiar nada
- Una configuración nueva o restablecida escribe solo `output`; ajusta `interaction`/`document` solo cuando deban diferir de `output`
- Para cambios programados en una terminal, prefiere la CLI `codexspec config` (`--set-lang`, `--set-interaction-lang`, `--set-document-lang`, `--set-commit-lang`, `--auto-next`)

---

## Visión general del flujo de trabajo

```text
Idea → /specify → requirements.md → /generate-spec → spec.md → /spec-to-plan → plan.md → /plan-to-tasks → tasks.md → /implement
                                                   │                         │                            │
                                              Review spec               Review plan                  Review tasks
```

Cada revisión es un punto de control humano. Valida la fidelidad y la calidad intrínseca mediante hallazgos respaldados por evidencia. Las sugerencias de diseño consultivas permanecen separadas y nunca bloquean la progresión. Los defectos verificados pueden corregirse y volver a revisarse durante un máximo de dos rondas.

---

## Resolución de problemas

### "Feature directory not found"

El comando no pudo localizar el directorio de la funcionalidad.

**Soluciones:**

- Ejecuta primero `codexspec init` para inicializar el proyecto
- Comprueba que el directorio `.codexspec/specs/` exista
- Verifica que estás en el directorio de proyecto correcto
- Pasa una ruta explícita del directorio de funcionalidad o del artefacto cuando existan múltiples candidatos

### "No spec.md found"

El archivo de especificación todavía no existe.

**Soluciones:**

- Ejecuta `/codexspec:specify` para aclarar primero los requisitos
- Luego ejecuta `/codexspec:generate-spec` para crear spec.md

### "Constitution not found"

No existe constitución del proyecto.

**Soluciones:**

- Ejecuta `/codexspec:constitution` para crear una
- La constitución es opcional pero recomendable para decisiones consistentes

### "Tasks file not found"

El desglose de tareas no existe.

**Soluciones:**

- Asegúrate de haber ejecutado primero `/codexspec:spec-to-plan`
- Luego ejecuta `/codexspec:plan-to-tasks` para crear tasks.md

### "GitHub CLI not authenticated"

El comando `/codexspec:tasks-to-issues` requiere autenticación en GitHub.

**Soluciones:**

- Instala la GitHub CLI: `brew install gh` (macOS) o equivalente
- Autentícate: `gh auth login`
- Verifica: `gh auth status`

---

## Próximos pasos

- [Flujo de trabajo](workflow.md) - Patrones comunes y cuándo usar cada comando
- [CLI](../reference/cli.md) - Comandos de terminal para la inicialización del proyecto

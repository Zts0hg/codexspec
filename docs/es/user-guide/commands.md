<a id="available-commands"></a>

# Comandos disponibles

La CLI tiene seis comandos públicos. Las integraciones de agentes distribuyen
28 comandos: Claude utiliza `/codexspec:<name>` y Codex, `$codexspec:<name>`.
Las tablas siguientes muestran la sintaxis de Claude para facilitar la lectura.

<a id="cli-commands"></a>

## Comandos CLI

| Comando | Propósito |
|---------|---------|
| `codexspec init` | Inicializar o actualizar un proyecto para Claude, Codex o ambos |
| `codexspec check` | Comprobar las herramientas y dependencias instaladas |
| `codexspec version` | Mostrar la versión e información del sistema |
| `codexspec config` | Consultar o modificar la configuración del proyecto |
| `codexspec list-commands` | Mostrar los comandos de agente disponibles por categoría |
| `codexspec show-blueprint` | Mostrar el blueprint del worktree compartido sin modificarlo |

<a id="core-workflow-commands"></a>

## Comandos del flujo de trabajo principal

| Comando | Propósito |
|---------|---------|
| `/codexspec:constitution` | Crear o actualizar los principios del proyecto y validarlos entre artefactos |
| `/codexspec:specify` | Hablar sobre los requisitos de una funcionalidad, confirmarlos y guardarlos |
| `/codexspec:blueprint` | Preparar o mantener los requisitos confirmados pendientes del blueprint |
| `/codexspec:generate-spec` | Elaborar una especificación trazable a partir de los requisitos confirmados, con revisión automática |
| `/codexspec:spec-to-design` | Definir la arquitectura, los componentes, las interfaces y las decisiones, con revisión automática |
| `/codexspec:design-to-plan` | Planificar las fases de implementación, su orden y su verificación, con revisión automática |
| `/codexspec:plan-to-tasks` | Elaborar tareas verificables que cubran los artefactos anteriores, con revisión automática y analyze |
| `/codexspec:implement-tasks` | Ejecutar las tareas, verificar los resultados, revisar y corregir |
| `/codexspec:auto-dev` | Desarrollar de forma autónoma los requisitos confirmados del blueprint en el orden del documento |

<a id="artifact-review-commands"></a>

## Comandos de revisión de artefactos

| Comando | Propósito |
|---------|---------|
| `/codexspec:review-spec` | Revisar la fidelidad y la calidad interna de la especificación |
| `/codexspec:review-design` | Revisar la fidelidad y la viabilidad del diseño, y comprobar si está listo para planificar |
| `/codexspec:review-plan` | Revisar la fidelidad y la viabilidad del plan, y comprobar si está listo para implementar |
| `/codexspec:review-tasks` | Revisar la fidelidad, las dependencias, la ejecutabilidad y la verificación de las tareas |

<a id="requirements-existing-code-and-debugging"></a>

## Requisitos, código existente y depuración

| Comando | Propósito |
|---------|---------|
| `/codexspec:clarify` | Resolver ambigüedades en los requisitos, actualizándolos antes que la especificación |
| `/codexspec:analyze` | Comprobar la trazabilidad de principio a fin y ajustar los artefactos derivados a las fuentes que los rigen |
| `/codexspec:checklist` | Generar una lista de comprobación de la calidad de los requisitos |
| `/codexspec:tasks-to-issues` | Convertir las tareas existentes en issues de GitHub con acciones concretas |
| `/codexspec:debug` | Investigar la causa raíz antes de aplicar una corrección |
| `/codexspec:reverse-spec` | Examinar la arquitectura existente, elaborar borradores de artefactos de módulos o informar de desviaciones respecto a la base confirmada |

<a id="project-knowledge-commands"></a>

## Comandos de conocimiento del proyecto

| Comando | Propósito |
|---------|---------|
| `/codexspec:distill` | Recoger conocimiento reutilizable o revisar candidatos en el espacio de trabajo local |
| `/codexspec:evolve` | Elaborar un borrador de contribución al proyecto de origen a partir de conocimiento validado |
| `/codexspec:onboard` | Obtener convenciones candidatas y restricciones respaldadas por evidencia a partir del código existente |

<a id="git-and-code-review-commands"></a>

## Comandos de Git y revisión de código

| Comando | Propósito |
|---------|---------|
| `/codexspec:commit-staged` | Generar mensajes a partir de los cambios preparados; previsualizar o ejecutar un commit autorizado |
| `/codexspec:pr` | Generar una descripción estructurada de PR/MR |
| `/codexspec:release-notes` | Mantener una entrada del registro de cambios y obtener el texto de una publicación del historial de Git |
| `/codexspec:review-code` | Revisar los cambios seleccionados como puerta de defectos; utilizar `--audit` para evaluar la calidad en las rutas indicadas |

<a id="utility-commands"></a>

## Comandos de utilidad

| Comando | Propósito |
|---------|---------|
| `/codexspec:config` | Crear, consultar, modificar o restablecer la configuración del proyecto de forma interactiva |
| `/codexspec:quick` | Ejecutar un flujo SDD breve con prioridad en los requisitos para cambios pequeños |

Las antiguas entradas de revisión de Python/React se conservan por compatibilidad del plugin y no forman parte del catálogo de 28 comandos instalados. Usa `review-code`, que carga los criterios pertinentes del lenguaje o framework, y `--audit` para evaluar rutas.

## Referencia de comandos

### `/codexspec:constitution`

Crea o actualiza la constitución del proyecto. La constitución define los principios arquitectónicos, el stack tecnológico, los estándares de código y las reglas de gobernanza que guían todas las decisiones de desarrollo posteriores.

**Sintaxis:**

```
/codexspec:constitution [principles description]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `principles description` | No | Descripción de los principios a incluir (se solicitará si no se proporciona) |

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
    └── constitution.md    # Project governance document
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

Aclara los requisitos mediante preguntas y respuestas interactivas, confirma el resumen resultante y lo guarda para futuras sesiones.

**Sintaxis:**

```
/codexspec:specify [your idea or requirement]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `your idea or requirement` | No | Descripción inicial de lo que quieres construir (se solicitará si no se proporciona) |

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
- No hace falta definirlo todo al principio: el refinamiento es iterativo
- Pregunta si la IA hace suposiciones
- Revisa el resumen antes de generar la especificación

---

### `/codexspec:blueprint`

Utiliza `blueprint` para preparar varios requisitos confirmados antes de empezar
el desarrollo, y `auto-dev` para desarrollar esa cola:

```text
/codexspec:blueprint Add a confirmed requirement for task reminders
/codexspec:auto-dev
```

Antes de añadir un requisito a la cola del blueprint, se resuelven la dirección,
las decisiones y las restricciones que corresponden al usuario. El archivo
compartido `.codexspec/blueprint.md` utiliza los estados `pending`, `in_progress`
y `completed`. Puedes añadir, sustituir, eliminar o reordenar los requisitos
pendientes; durante el mantenimiento del blueprint, las entradas en curso y
las completadas son de solo lectura.

Auto-dev desarrolla los requisitos en el orden del documento. Retoma la
funcionalidad en curso antes de comenzar otra y vuelve a leer la cola después
de cada finalización, por lo que los nuevos requisitos pendientes pueden
incorporarse a la ejecución. Realiza las etapas SDD, la implementación, la
verificación, la revisión y las correcciones dentro de los requisitos
confirmados. Invocar `auto-dev` activa su automatización independientemente de
`workflow.auto_next`, sin modificar ese ajuste.

Ambos comandos comparten `worktree-for-codexspec-auto-dev`, en la rama
`codexspec/auto-dev`. Pueden ejecutarse a la vez gracias a los mecanismos
compartidos que controlan quién ocupa el espacio de trabajo y protegen las
escrituras; los requisitos se desarrollan de uno en uno en ese espacio. Si una decisión de producto no puede resolverse a
partir de los requisitos confirmados, la ejecución se detiene y aporta la
evidencia, en vez de preguntar durante el funcionamiento autónomo habitual.

Para consultar el blueprint compartido sin modificarlo:

```bash
codexspec show-blueprint
```

---

### `/codexspec:generate-spec`

Elaborar una especificación trazable a partir de los requisitos confirmados, con revisión automática.

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
     - Or proceed to /codexspec:spec-to-design
```

---

### `/codexspec:spec-to-design`

Lee `requirements.md` y `spec.md` confirmados, los principios del proyecto y los hechos pertinentes del repositorio. Genera `design.md` con componentes, interfaces, flujo de datos, alternativas y decisiones vinculados a los requisitos de origen. Ejecuta `review-design` automáticamente. Se detiene si una elección cambia la intención confirmada o requiere una nueva decisión del usuario.

```text
/codexspec:spec-to-design <feature-dir>
```

---

### `/codexspec:design-to-plan`

Convierte el diseño confirmado en un plan de implementación. Ejecute primero `spec-to-design` para definir la arquitectura, los componentes, las interfaces y las decisiones tecnológicas.

```text
/codexspec:design-to-plan [design.md | spec.md | feature-directory]
```

Lee `requirements.md`, `spec.md`, `design.md` y la constitución. Planifica las fases, su orden y la verificación; hace referencia al diseño sin volver a diseñar el sistema. Cada componente del plan incluye `Covers: REQ-xxx; Design: <design component>`.

Genera `plan.md` y ejecuta `review-plan`. Con `auto_next` activado, una revisión satisfactoria da paso a `plan-to-tasks`. Las decisiones que cambien la intención confirmada requieren confirmación. Una ruta explícita tiene prioridad sobre la rama actual; si hay ambigüedad, se solicita una selección. Las funcionalidades antiguas sin `design.md` conservan la planificación a partir de `spec.md`.

---

### `/codexspec:plan-to-tasks`

Desglosa el plan técnico en tareas accionables con cobertura explícita y resultados verificables.

**Sintaxis:**

```
/codexspec:plan-to-tasks [path_to_spec.md path_to_plan.md]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `paths` | No | Rutas a la especificación y al plan (se detectan automáticamente si no se proporcionan) |

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
        └── tasks.md    # Task breakdown
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

Tras escribir las tareas, se ejecuta `review-tasks`. Un resultado `PASS` o `PASS_WITH_WARNINGS` activa `analyze` una sola vez; el análisis no añade una condición de bloqueo para completar el trabajo. Las tareas cubren los requisitos confirmados, la especificación, el diseño y el plan.

---

### `/codexspec:implement-tasks`

Ejecutar las tareas, verificar los resultados, revisar y corregir.

```text
/codexspec:implement-tasks <feature-dir>
```

Los cuatro revisores de artefactos —`review-spec`, `review-design`, `review-plan`
y `review-tasks`— comprueban la fidelidad, la cobertura, la viabilidad y la calidad
interna. Se ejecutan automáticamente después de generar los artefactos y también
pueden invocarse manualmente. Los informes distinguen los defectos verificados
de las advertencias sobre riesgos que no bloquean el avance y de las
oportunidades de diseño, e incluyen una puntuación de compatibilidad.

`review-code` ofrece una puerta de defectos independiente cuyo alcance son los
cambios, así como una evaluación explícita de la calidad del código en su conjunto:

```text
/codexspec:review-code --feature <feature-dir>
/codexspec:review-code --uncommitted
/codexspec:review-code --audit src/
```

La revisión predeterminada abarca todos los cambios de la rama de la
funcionalidad: los registrados en commits, los preparados, los no preparados
y los archivos sin seguimiento que no estén ignorados. Puedes seleccionar
explícitamente los cambios registrados en commits, los no confirmados o los
de un único commit. `--feature` añade el contexto de requisitos sin reducir
el alcance de Git. `--audit` evalúa las rutas indicadas y genera una ficha
orientativa de calidad en lugar de un veredicto de finalización.

Las revisiones cargan los estándares compartidos de `.codexspec/review-code/`
y seleccionan las dimensiones de comportamiento y las comprobaciones de lenguaje
o framework pertinentes. Cada hallazgo debe contar con evidencia concreta,
una condición que pueda darse, una relación demostrada con los cambios
seleccionados y un impacto. El revisor informa de los defectos y las sugerencias
de mantenimiento fundamentadas sin editar archivos; quien aplica las
correcciones los verifica de forma independiente.

En las tareas de código, la implementación empieza por las pruebas. Para la
documentación y la configuración se implementa directamente y se realizan las
comprobaciones adecuadas. Tras una corrección, la revisión incremental puede
reutilizar la cobertura que no se haya visto afectada. La aceptación final
requiere una revisión nueva de toda la funcionalidad con resultado `PASS`,
cobertura y verificación completas, y ningún defecto P0–P3 admitido. Las
sugerencias de mantenimiento fundamentadas se presentan por separado.

El valor predeterminado de `workflow.auto_maintenance` es **true**. Este ajuste
controla si, además de corregir defectos, se aplican mejoras de mantenimiento
verificadas y compatibles. Si lo desactivas, se sigue informando de esas
sugerencias y siguen siendo obligatorias las correcciones de defectos y las
comprobaciones exigidas. El ajuste es independiente del avance entre etapas
y no es un argumento de `implement-tasks`.

Para empezar la depuración por la causa raíz:

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

Debug sigue esta secuencia: investigación → análisis de patrones → verificación
de una sola hipótesis → corrección precedida de una prueba que falla. Durante
la implementación se recurre a este proceso cuando las correcciones se atascan,
cuando hace falta rastrear un defecto de funcionamiento no trivial o cuando
la misma clase de causa raíz reaparece en varias rondas de revisión. Tres
intentos fallidos de corrección obligan a reevaluar la arquitectura.

Utiliza `checklist` para evaluar la claridad, la integridad y la coherencia de los requisitos:

```text
/codexspec:checklist Check the authentication requirements for completeness
```

La [referencia de comandos](commands.md) detalla los
selectores de revisión, los argumentos y los procedimientos.

---

### `/codexspec:auto-dev`

Desarrollar de forma autónoma los requisitos confirmados del blueprint en el orden del documento.

Consulta [`blueprint`](#codexspecblueprint).

```text
/codexspec:auto-dev
```

---

### `/codexspec:review-spec`

Valida la especificación frente a los requisitos confirmados y su propia calidad interna.

**Sintaxis:**

```
/codexspec:review-spec [path_to_spec.md]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `path_to_spec.md` | No | Ruta al archivo de especificación (se detecta automáticamente si no se proporciona) |

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
| Defecto de fidelidad | Contradice una fuente de referencia u omite contenido obligatorio de ella |
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

- Ejecútalo antes de `/codexspec:spec-to-design`
- Trata `BLOCKED` y `NEEDS_REVISION` como no listos para continuar
- No promuevas avisos a requisitos
- Vuelve a ejecutarlo tras aplicar correcciones

---

### `/codexspec:review-design`

Revisa la fidelidad, viabilidad y preparación de `design.md` para la planificación frente a los requisitos confirmados y la especificación. Distingue los defectos respaldados por evidencia de las mejoras de diseño opcionales; aplica los mismos estados y límites de reparación que los demás revisores de artefactos.

```text
/codexspec:review-design <feature-dir>
```

---

### `/codexspec:review-plan`

Revisa el plan de implementación técnica en busca de fidelidad, viabilidad y decisiones técnicas justificadas.

**Sintaxis:**

```
/codexspec:review-plan [path_to_plan.md]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `path_to_plan.md` | No | Ruta al archivo del plan (se detecta automáticamente si no se proporciona) |

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

El plan lleva a la práctica el `design.md` confirmado; no reabre las decisiones de arquitectura. La revisión comprueba sus referencias al diseño, además de la cobertura de requisitos.

---

### `/codexspec:review-tasks`

Valida el desglose de tareas en cuanto a cobertura, resultados verificables, orden correcto y dependencias viables.

**Sintaxis:**

```
/codexspec:review-tasks [path_to_tasks.md]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `path_to_tasks.md` | No | Ruta al archivo de tareas (se detecta automáticamente si no se proporciona) |

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

### `/codexspec:clarify`

Escanea una especificación existente en busca de ambigüedades y vacíos. Úsalo para refinamiento iterativo tras la creación inicial de la especificación.

**Sintaxis:**

```
/codexspec:clarify [path_to_spec.md]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `path_to_spec.md` | No | Ruta al archivo de especificación (se detecta automáticamente si no se proporciona) |

**Lo que hace:**

- Escanea requisitos y especificación usando categorías de ambigüedad enfocadas
- Hace preguntas de aclaración dirigidas (máximo 5)
- Actualiza primero `requirements.md` tras la confirmación del usuario, luego sincroniza `spec.md`
- Se integra con los hallazgos de review-spec si están disponibles

**Categorías de ambigüedad:**

| Categoría | Lo que detecta |
|----------|-----------------|
| **Información que falta** | Secciones faltantes, contenido vacío, criterios de aceptación ausentes |
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
- Máximo 5 preguntas por ejecución
- Ejecútalo varias veces para especificaciones complejas

---

### `/codexspec:analyze`

- **specify** inicia o retoma la definición de requisitos. El resumen solo adquiere carácter vinculante cuando se confirma explícitamente.
- **clarify** resuelve las ambigüedades de los requisitos o de la especificación existentes: plantea hasta cinco preguntas por ejecución, repartidas entre cuatro categorías. Primero actualiza `requirements.md` y después sincroniza `spec.md`.
- **analyze** revisa la cadena completa: requisitos → especificación → diseño → plan → tareas. Aplica automáticamente correcciones deterministas a los artefactos derivados cuando se deducen de las fuentes que los rigen; nunca modifica `requirements.md`. Informa de los hallazgos pendientes. Se ejecuta automáticamente después de que la revisión de tareas se apruebe y tiene carácter informativo, sin bloquear la implementación.

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

Si una funcionalidad antigua no tiene `requirements.md`, el análisis parte de `spec.md`, indica que falta la evidencia de la conversación original y solo informa de los hallazgos, sin modificar artefactos. La ausencia de un `design.md` antiguo tampoco impide el análisis.

---

### `/codexspec:checklist`

Genera checklists de calidad para validar la completitud, claridad y consistencia de los requisitos. Son "pruebas unitarias para la redacción de requisitos".

**Sintaxis:**

```
/codexspec:checklist [focus_area]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `focus_area` | No | Enfoque de dominio (p. ej., "ux", "api", "security", "performance") |

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

Antes de crear issues, verifica el repositorio de destino con su remoto y obtén autorización explícita. Generar una lista de tareas no autoriza por sí solo su publicación.

---

### `/codexspec:debug`

Investigar la causa raíz antes de aplicar una corrección.

Consulta [Flujo de trabajo](workflow.md#review-and-debugging).

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

---

### `/codexspec:reverse-spec`

Estos dos comandos responden a necesidades distintas:

| Comando | Úsalo para | Resultado y límites |
|---------|-----------|-----------------|
| `onboard [path]` | Obtener conocimiento reutilizable del proyecto a partir de una base de código existente | Convenciones candidatas y restricciones respaldadas por evidencia concreta en el perfil; el código permanece en modo de solo lectura |
| `reverse-spec [path]` | Entender la arquitectura existente o comparar el código con la intención confirmada | Borradores de artefactos o informe de desviaciones; el código permanece en modo de solo lectura |

```text
/codexspec:onboard src/
/codexspec:reverse-spec
/codexspec:reverse-spec src/auth
```

Onboard deduce convenciones a partir del código observable y solo propone
restricciones cuando existen prohibiciones explícitas. Las convenciones
candidatas se aplican de inmediato en el proyecto; las restricciones candidatas
requieren decidir en la sesión si se guardan, se editan o se descartan. Se
conserva el conocimiento existente. Un primer examen del código no se utiliza
para inventar las razones de decisiones pasadas ni problemas que supuestamente
se hayan experimentado.

Reverse-spec ofrece tres modos:

- **Panorama general**: si no se indica una ruta o se indica la raíz del repositorio, genera un `design.md` con una descripción breve de la arquitectura y un `slices.md` para elegir los módulos que se van a inspeccionar.
- **Generación**: si se indica la ruta de un módulo sin una base confirmada, genera borradores de `spec.md` y `design.md`, además de requisitos pendientes o inferidos.
- **Conciliación**: si el módulo tiene una base confirmada, genera `reconcile.md`. El informe identifica comportamientos no documentados, especificaciones no implementadas y discrepancias semánticas con la especificación y el diseño confirmados; los requisitos rigen la intención del producto.

Los borradores inferidos requieren confirmación humana antes de convertirse
en una base de referencia. La conciliación propone un curso de acción —corregir
el código, actualizar los documentos o decidir la intención—, pero no lo aplica
automáticamente.

---

### `/codexspec:distill`

Captura conocimiento reutilizable entre funcionalidades en `.codexspec/profile/` y revisa los candidatos pendientes sin editar a mano sus archivos Markdown.

**Sintaxis:**

```text
/codexspec:distill [interaction segment]
/codexspec:distill review
```

**Revisión manual:**

- `/codexspec:distill review`, o una invocación directa sin un segmento nuevo que extraer, abre una página HTML sin conexión servida únicamente desde `127.0.0.1`. Su encabezado nombra el directorio del proyecto en el que escribirá la sesión, de modo que dos revisiones abiertas a la vez no puedan confundirse.
- La página admite revisión estructurada, aprobación, descarte, aplazamiento, consolidación, un resumen completo de lo preparado y un **Aplicar todo** explícito. Una revisión o una fusión debe mostrar su vista previa final exacta en Markdown antes de poder preparar la misma acción; la página indica en cuál de los tres estados de vista previa está cada registro —sin vista previa, coincidente con los cambios actuales, o modificado tras la vista previa— antes de que uses un control de decisión.
- Toda acción que elimina archivos de registro pide una segunda confirmación que declara su consecuencia: descartar nombra el archivo que se eliminará al aplicar, fusionar nombra cuántos registros miembro se eliminarán, y descartar el borrador nombra cuántas decisiones preparadas se perderán.
- Un registro no pasa a `vetted` sin aprobación humana **y** prueba de verificación basada en resultados. La página muestra, antes de que elijas aprobar, si las pruebas guardadas ya cumplen ese requisito.
- La cola agrupa los registros según lo decidido y muestra cuántos de los pendientes ya están resueltos. Al preparar una decisión pasa al siguiente registro sin decidir; un interruptor en el encabezado lo desactiva.
- La página se maneja con el teclado: pulsa `?` para ver las teclas. Ninguna tecla por sí sola aplica el lote, cancela la sesión ni descarta el borrador.
- Las decisiones preparadas usan un borrador de proyecto recuperable y excluido de Git. Solo hay una revisión con permiso de escritura activa por proyecto.
- Un borrador dañado estructuralmente se conserva con un diagnóstico accionable y solo se elimina mediante una acción de descarte explícita.
- Al aplicar se vuelven a comprobar los hash de origen y se rechaza todo el lote si algún registro cambió; nunca sobrescribe una edición concurrente ni informa de un éxito parcial.
- Todos los recursos de la página se distribuyen con CodexSpec. La página no usa CDN, llamada a modelo remoto ni telemetría.
- Si no se puede abrir ningún navegador, el comando imprime la URL local protegida por token. Pide el modo de texto explícito cuando un navegador no sea adecuado; usa la misma validación y la misma ruta de escritura.

La destilación automática sigue siendo no interactiva y no bloqueante: nunca abre la página, nunca inicia la revisión de texto y nunca espera un borrador guardado.

---

### `/codexspec:evolve`

`evolve` selecciona únicamente conocimiento validado que sea útil fuera del
proyecto, elabora un borrador de comando o habilidad y obtiene aprobación
explícita antes de hacer push o abrir una PR de contribución para revisión humana.

```text
/codexspec:evolve
```

---

### `/codexspec:onboard`

Obtener convenciones candidatas y restricciones respaldadas por evidencia a partir del código existente.

Consulta [`reverse-spec`](#codexspecreverse-spec).

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

- **commit-staged** analiza exactamente el área de preparación y genera un mensaje de Conventional Commits; `-p` muestra una vista previa sin crear un commit. El flujo que lo invoca elige y prepara los archivos. La ejecución autorizada utiliza un entorno protegido que vuelve a comprobar que el contenido del commit coincide con el análisis. Las instrucciones de commits para agentes se aplican en conversaciones habituales y en los flujos SDD, blueprint y auto-dev; disponer del comando no equivale a invocarlo ni autoriza un commit.
- **pr** genera una descripción estructurada de una PR de GitHub o una MR de GitLab a partir del diff. `--spec` puede añadir contexto de la funcionalidad a partir de la ruta de un archivo `spec.md`, o del nombre o prefijo de un directorio de funcionalidad que se resuelva a ese archivo. La salida predeterminada es texto para utilizar en la plataforma de alojamiento.
- **release-notes** obtiene del historial de Git una entrada de Keep a Changelog y el texto de una publicación. La sección predeterminada es `[Unreleased]`; `--version` utiliza la etiqueta proporcionada. No prepara archivos, ni crea commits, ni incrementa versiones, ni crea tags, ni publica, ni crea una release.
- **tasks-to-issues** crea issues de GitHub a partir de las tareas existentes, con sus dependencias y criterios de aceptación. Requiere una CLI de GitHub autenticada y comprueba que el repositorio de los issues coincida con el remoto configurado.

La vista previa directa de commits y los commits autorizados en el directorio
actual requieren Python 3.11+ y Git. El entorno de ejecución se instala en los
proyectos inicializados mediante la CLI y viene incluido en el plugin de Claude.
Las fusiones creadas por el agente que modifican contenido también pasan por
el análisis de los cambios preparados. Las fusiones que solo unen historiales
conservan el mensaje predeterminado de Git y validan el árbol y los padres;
los avances rápidos no crean commits.

El helper compartido `.codexspec/scripts/commit-staged-helper.py` (o la copia incluida en el plugin) requiere Python 3.11+ y Git, no invoca ningún LLM, conserva los Git hooks y rechaza el contenido preparado que haya cambiado tras el análisis. La inicialización de un solo uso instala este runtime; el enrutamiento de espacios de trabajo, blueprint y auto-dev siguen necesitando la CLI.

---

### `/codexspec:pr`

Genera una descripción estructurada de GitHub Pull Request / GitLab Merge Request a partir del git diff. Opcionalmente integra `spec.md` para contexto trazado por SDD.

**Sintaxis:**

```
/codexspec:pr [--target-branch <branch>] [--sections <list>] [--spec <id-or-path>] [--output <file>]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `--target-branch <branch>` | No | Rama contra la que comparar (predeterminada: `origin/main`) |
| `--sections <list>` | No | Subconjunto separado por comas de `summary, changes, testing, verify, checklist, notes` (predeterminado: `all`) |
| `--spec <id-or-path>` | No | Integración opt-in de spec: un id de funcionalidad (p. ej., `2025-0321-1430k7-auth`) resuelto bajo `.codexspec/specs/`, o una ruta `path/to/spec.md` explícita. Omitir para generar solo desde git |
| `--output <file>` | No | Guardar la descripción en un archivo en lugar de la terminal |

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

### `/codexspec:release-notes`

```text
/codexspec:commit-staged -p
/codexspec:pr --spec <feature-dir>/spec.md
/codexspec:release-notes --from <ref> --to HEAD
/codexspec:tasks-to-issues <feature-dir>
```

- **commit-staged** analiza exactamente el área de preparación y genera un mensaje de Conventional Commits; `-p` muestra una vista previa sin crear un commit. El flujo que lo invoca elige y prepara los archivos. La ejecución autorizada utiliza un entorno protegido que vuelve a comprobar que el contenido del commit coincide con el análisis. Las instrucciones de commits para agentes se aplican en conversaciones habituales y en los flujos SDD, blueprint y auto-dev; disponer del comando no equivale a invocarlo ni autoriza un commit.
- **pr** genera una descripción estructurada de una PR de GitHub o una MR de GitLab a partir del diff. `--spec` puede añadir contexto de la funcionalidad a partir de la ruta de un archivo `spec.md`, o del nombre o prefijo de un directorio de funcionalidad que se resuelva a ese archivo. La salida predeterminada es texto para utilizar en la plataforma de alojamiento.
- **release-notes** obtiene del historial de Git una entrada de Keep a Changelog y el texto de una publicación. La sección predeterminada es `[Unreleased]`; `--version` utiliza la etiqueta proporcionada. No prepara archivos, ni crea commits, ni incrementa versiones, ni crea tags, ni publica, ni crea una release.
- **tasks-to-issues** crea issues de GitHub a partir de las tareas existentes, con sus dependencias y criterios de aceptación. Requiere una CLI de GitHub autenticada y comprueba que el repositorio de los issues coincida con el remoto configurado.

La vista previa directa de commits y los commits autorizados en el directorio
actual requieren Python 3.11+ y Git. El entorno de ejecución se instala en los
proyectos inicializados mediante la CLI y viene incluido en el plugin de Claude.
Las fusiones creadas por el agente que modifican contenido también pasan por
el análisis de los cambios preparados. Las fusiones que solo unen historiales
conservan el mensaje predeterminado de Git y validan el árbol y los padres;
los avances rápidos no crean commits.

#### Opciones de notas de versión

| Comandos | Referencia |
|---|---|
| `--version <X.Y.Z>` | Etiqueta de versión indicada; si se omite, `[Unreleased]` |
| `--from <ref>` | Referencia inicial; por defecto, última etiqueta alcanzable, luego una versión del changelog localizable y, finalmente, todo el historial |
| `--to <ref>` | Referencia final; por defecto, `HEAD` |
| `--output <file>` | Archivo para el texto de la versión; por defecto, salida en el terminal |
| `--spec <feature>` | Contexto opcional de la funcionalidad; si no se resuelve, se informa y se continúa con Git |

---

### `/codexspec:review-code`

Revisa el cambio Git seleccionado como una puerta de defectos estricta antes de fusionarlo. El objetivo predeterminado incluye la diferencia completa de la funcionalidad; los selectores explícitos eligen cambios registrados en commits, cambios sin commit o un único commit, pero no aceptan filtros de ruta.

<!-- REVIEW-CODE-BREAKING: DEFAULT-GATE -->
<!-- REVIEW-CODE-BREAKING: PATH-AUDIT -->

**Modo de revisión predeterminado:**

- El comando predeterminado ahora es una puerta de defectos centrada en cambios, no una puntuación general de calidad.
- Las rutas posicionales ya no son válidas. Usa `--audit` explícitamente para la puntuación consultiva de calidad por ruta.

**Sintaxis de la puerta de defectos:**

```text
/codexspec:review-code
/codexspec:review-code --committed [--base <branch>] [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code --uncommitted [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code --commit <sha> [--parent <n>] [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code [--committed] --incremental-from <fingerprint> [--feature <feature-dir>]
```

Todas las formas de la puerta de defectos aceptan además `--decided-by reviewer|ask`, que anula `review.decided_by` para esa ejecución.

<!-- REVIEW-CODE-SYSTEM-CONTRACT -->
<!-- REVIEW-CODE-VARIANT-SEARCH -->
<!-- REVIEW-CODE-NEUTRAL-HANDOFF -->

La revisión inventaría todos los artefactos seleccionados, evalúa los requisitos aplicables y ejecuta cinco fases en este orden: Scope, System Contract, Behavior, Risk y Verification. Registra contratos entre módulos respaldados por evidencia y particiones de revisión semánticas; cada causa raíz repetible y validada activa, antes de terminar la ronda, una búsqueda acotada de casos relacionados. Tras seis secciones del informe aparece un único bloque de resultados `<review-code-result>` legible por máquinas con `schema_version: "3"`. El bloque de resultados contiene la identidad del objetivo, la cobertura y obligaciones objetivas que deben volver a verificarse tras la reparación. El llamador conserva esas obligaciones neutrales para una revisión completa nueva, sin transmitir el razonamiento de la reparación ni conclusiones previas de corrección. El resultado es `PASS`, `FAIL` o `INCONCLUSIVE`: cualquier hallazgo P0-P3 produce `FAIL`; la falta de evidencia obligatoria o la cobertura incompleta producen `INCONCLUSIVE`.

**Rondas incrementales.** Tras una reparación, `--incremental-from <fingerprint>` vuelve a revisar solo lo que cambió desde ese resultado anterior: los archivos modificados, las particiones de revisión y los contratos que tocan, y las obligaciones pendientes. Se reutiliza la cobertura de los archivos sin cambios y no afectados, y el revisor sigue informando cualquier defecto que encuentre en otro lugar. Un `PASS` incremental nunca completa una funcionalidad: `implement-tasks` ejecuta primero una revisión completa, revisiones incrementales después de cada reparación y, como aceptación final, una nueva revisión completa. Los registros de revisión se guardan fuera del repositorio, en tu directorio de caché de usuario (`~/.cache/codexspec/review/` o `%LOCALAPPDATA%\codexspec\review\`); en la conversación solo aparecen el informe y el bloque de resultados.

**Modo de decisión.** `review.decided_by` en `.codexspec/config.yml` determina quién decide sobre un hallazgo cuyo desencadenante está fuera del contexto real de uso del proyecto, como una entrada que el proyecto nunca recibe. Con el valor predeterminado `reviewer`, la revisión se comporta exactamente igual que antes. Con `ask`, la revisión informa ese elemento como una decisión de escenario pendiente en lugar de fallar por él, e `implement-tasks` te pregunta una vez: corregirlo o aceptar que el escenario queda fuera del alcance. Tu respuesta se registra en `requirements.md` como una entrada `CON` u `OUT` confirmada, de modo que las rondas posteriores no vuelvan a plantearlo.

```text
You: /codexspec:review-code --feature .codexspec/specs/2026-0714-example

AI:  ## Verdict
     **PASS** — all required review and verification completed with no findings.
```

**Criterios aplicables y mantenimiento.** Cada revisión lee las reglas comunes y el modo elegido, evalúa las siete dimensiones y carga detalles solo cuando el comportamiento, contrato o dependencia los hace pertinentes. Las dependencias sin cambios descubiertas durante el seguimiento también pueden activar listas de lenguaje o framework. Las propuestas de mantenimiento necesitan pruebas de un problema actual y una mejora local compatible con el comportamiento existente. La complejidad futura hipotética y los umbrales de estilo por sí solos no justifican reparaciones. El resultado de defectos mantiene la versión 3; un `<review-code-maintenance>` separado, de versión 1, informa propuestas vinculadas a la misma huella del objetivo. La revisión independiente solo informa. `implement-tasks` verifica y aplica según `workflow.auto_maintenance` (por defecto `true`). Las reparaciones continúan mientras haya avances sustanciales y respetan las condiciones de parada existentes. No hay un máximo fijo de rondas; la aceptación final requiere una nueva revisión completa.

Las opciones booleanas de la CLI aceptan `on/true/1/yes` y `off/false/0/no`,
sin distinguir mayúsculas y minúsculas y admitiendo espacios alrededor del
valor. Una opción booleana sin valor invierte el valor actual del checkout de
destino; en YAML, los valores se guardan como booleanos.

`codexspec init` instala recursos de revisión compartidos por Claude Code y Codex en `.codexspec/review-code/`. `--force` actualiza los recursos distribuidos y conserva archivos de extensión con otras rutas. Instalar solo la CLI no crea archivos de proyecto. Si se usa únicamente el plugin y el proyecto no tiene recursos instalados, la revisión carga los mismos recursos desde la raíz resuelta por el anfitrión.

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
| `path...` | No | Uno o más archivos o directorios fuente a revisar (separados por espacios). Por defecto `src/` si se omite |

**Lo que hace:**

- Detecta el lenguaje o lenguajes principales a partir de las extensiones de archivo y ejecuta una pasada por idioma para objetivos multilenguaje
- Ejecuta herramientas de análisis estático cuando su configuración está presente (`ruff`/`mypy`, `eslint`/`tsc`, `go vet`/`gofmt`, `cargo check`/`cargo clippy`, `shellcheck`); si no, omite esas comprobaciones y reporta cobertura degradada
- Puntúa cuatro dimensiones: Claridad y simplicidad idiomática, Corrección y contratos explícitos, Robustez en tiempo de ejecución y disciplina de recursos, e Integridad arquitectónica y de diseño
- Inyecta subsecciones obligatorias para los frameworks detectados (p. ej., Cumplimiento de Hooks para React, Ownership y Borrowing para Rust, Disciplina de Goroutine y Context para Go, Seguridad de Memoria y Lifetime para C/C++, Seguridad de Ejecución para Shell)
- Contrasta los hallazgos con `.codexspec/memory/constitution.md` cuando está presente; si está ausente, el eje de constitución se descarta y su peso se redistribuye
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
- La puntuación es consultiva; los hallazgos CRITICAL/HIGH son la base para decidir qué corregir

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
     - workflow.auto_distill
     - workflow.auto_maintenance
     - workflow.worktrees (default on; checkout-local)
     - review.decided_by

You: Output language (base) → zh-CN

AI:  ✓ Updated language.output: "zh-CN"
     (interaction and document fall back to output, then en.)
```

**Consejos:**

- Usa `/codexspec:config --view` para inspeccionar el estado actual antes de cambiar nada
- Una configuración nueva o restablecida escribe solo `output`; ajusta `interaction`/`document` solo cuando deban diferir de `output`
- Para cambios programados en una terminal, prefiere la CLI `codexspec config` (`--set-lang`, `--set-interaction-lang`, `--set-document-lang`, `--set-commit-lang`, `--auto-next`)

El menú interactivo también permite gestionar `workflow.auto_distill`, `workflow.auto_maintenance`, `workflow.worktrees` y `review.decided_by`. Los cambios de configuración siguen las reglas de enrutamiento de worktrees y se aplican a cada checkout por separado.

---

### `/codexspec:quick`

Ejecuta un flujo Requirements-First SDD simplificado para cambios pequeños.

**Sintaxis:**

```
/codexspec:quick [describe a small requirement]
```

**Argumentos:**

| Argumento | Requerido | Descripción |
|----------|----------|-------------|
| `describe a small requirement` | No | Descripción breve del cambio pequeño y bien delimitado (se solicitará si no se proporciona) |

**Lo que hace:**

- Evalúa el alcance (archivos afectados, extensión del módulo, nuevas dependencias, decisiones de producto sin resolver) y, si el cambio es amplio o tiene varios resultados independientes, recomienda el flujo estándar
- Crea un espacio de trabajo de funcionalidad y `requirements.md` usando la misma convención de marca de tiempo que `/codexspec:specify`
- Resuelve solo ambigüedades que cambien de forma sustancial la implementación; presenta un resumen conciso confirmado (`NEED-*`, `CON-*`/`DEC-*` relevantes, `OUT-*`, `OPEN-*` sin resolver)
- Se detiene en la Confirmation Gate: no se genera nada hasta que confirmes el resumen
- Encadena los comandos de generación sobre el nuevo directorio de la funcionalidad: `/codexspec:generate-spec`, `/codexspec:design-to-plan`, `/codexspec:plan-to-tasks`, `/codexspec:implement-tasks`
- Delega la revisión en el bucle automático de cada comando de generación; hace una pausa y pregunta al usuario si una revisión necesita una decisión nueva de producto o arquitectura
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

AI:  Running generate-spec → design-to-plan → plan-to-tasks → implement-tasks ...

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

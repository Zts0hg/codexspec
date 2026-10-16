# Inicio rápido

<a id="30-second-quick-start"></a>

## Inicio rápido en 30 segundos

Instala CodexSpec e inicializa el proyecto para el asistente que utilices:

```bash
uv tool install codexspec

# Create a new project for Claude Code
codexspec init my-project --ai claude

# Or initialize an existing project for Codex
cd your-existing-project
codexspec init . --ai codex

# Use --ai both when you want both integrations
```

Inicia el asistente instalado en el proyecto que acabas de inicializar. El
flujo de trabajo es el mismo; cambia la forma de invocar los comandos:

| Asistente | Empezar a definir los requisitos |
|-----------|------------------------------|
| Claude Code (`claude`) | `/codexspec:specify I want to build a todo application` |
| Codex (`codex`) | `$codexspec:specify I want to build a todo application` |

Si hace falta, adapta los principios del proyecto con `constitution`. Confirma
el resumen final de requisitos y continúa en el directorio de la funcionalidad
y el espacio de trabajo que indique el comando. Los siguientes pasos se explican
en [Flujo de trabajo principal](../user-guide/workflow.md#core-workflow).

¿Usas la aplicación de escritorio de Codex? [Pide a Codex que instale e inicialice tu proyecto](installation.md#install-with-the-codex-desktop-app).

<a id="core-workflow"></a>

## Flujo de trabajo principal

En el flujo estándar, los artefactos de cada funcionalidad mantienen referencias a sus fuentes:

```text
/specify          → requirements.md
/generate-spec    → spec.md       → review-spec
/spec-to-design   → design.md     → review-design
/design-to-plan   → plan.md       → review-plan
/plan-to-tasks    → tasks.md      → review-tasks → analyze
/implement-tasks  → implementation and complete-feature code review
```

Los ejemplos siguientes utilizan el prefijo `/codexspec:` de Claude. En Codex,
utiliza `$codexspec:` con el mismo nombre de comando y los mismos argumentos.

| Paso | Comando | Propósito y resultado |
|------|---------|--------------------|
| Principios del proyecto | `/codexspec:constitution` | Crear o actualizar `constitution.md` y validar los artefactos afectados |
| Requisitos | `/codexspec:specify <idea>` | Hablar sobre la intención, confirmar el resumen final y guardar `requirements.md` |
| Especificación | `/codexspec:generate-spec <feature-dir>` | Elaborar `spec.md` a partir de los requisitos confirmados, con referencias a las fuentes |
| Diseño del sistema | `/codexspec:spec-to-design <feature-dir>` | Elaborar `design.md` con los componentes, las interfaces y las decisiones de diseño clave |
| Plan de implementación | `/codexspec:design-to-plan <feature-dir>` | Elaborar `plan.md` con las fases, el orden y la verificación |
| Tareas | `/codexspec:plan-to-tasks <feature-dir>` | Elaborar un `tasks.md` trazable y verificable, y analizar la coherencia entre artefactos |
| Implementación | `/codexspec:implement-tasks <feature-dir>` | Ejecutar las tareas, verificar los resultados y corregir los hallazgos de revisión que se hayan verificado de forma independiente |

Sustituye `<feature-dir>` por el directorio de la funcionalidad que indique el
comando al definir los requisitos. Continúa en su worktree o indica su ruta
explícita para conservar la identidad de la funcionalidad entre comandos y sesiones.

<a id="specify-clarify-and-analyze"></a>

### specify, clarify y analyze

- **specify** inicia o retoma la definición de requisitos. El resumen solo adquiere carácter vinculante cuando se confirma explícitamente.
- **clarify** resuelve las ambigüedades de los requisitos o de la especificación existentes: plantea hasta cinco preguntas por ejecución, repartidas entre cuatro categorías. Primero actualiza `requirements.md` y después sincroniza `spec.md`.
- **analyze** revisa la cadena completa: requisitos → especificación → diseño → plan → tareas. Aplica automáticamente correcciones deterministas a los artefactos derivados cuando se deducen de las fuentes que los rigen; nunca modifica `requirements.md`. Informa de los hallazgos pendientes. Se ejecuta automáticamente después de que la revisión de tareas se apruebe y tiene carácter informativo, sin bloquear la implementación.

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

<a id="small-changes-with-quick"></a>

### Cambios pequeños con Quick

Utiliza `quick` para un cambio pequeño y bien delimitado, como una corrección localizada:

```text
/codexspec:quick Fix the empty-state message on the task list
```

Quick confirma y guarda un resumen breve de requisitos y, a continuación,
coordina la especificación, la planificación, las tareas y la implementación,
con las revisiones de los comandos de generación. Los cambios amplios y las
decisiones pendientes sobre el producto o el diseño requieren el flujo estándar.
Quick se detiene cuando hace falta tomar una nueva decisión.

<a id="workflow-automation"></a>

### Automatización del flujo de trabajo

El valor predeterminado de `workflow.auto_next` es **false**. Si es `true` en
la configuración del espacio de trabajo activo, la confirmación final de los
requisitos da paso a la especificación. Cada etapa de generación avanza tras
un resultado `PASS` o `PASS_WITH_WARNINGS`; un resultado `NEEDS_REVISION` o
`BLOCKED` detiene la cadena. `implement-tasks` es la última etapa.

La corrección automática de artefactos solo abarca defectos verificados cuya
solución se deduce de la evidencia de los artefactos anteriores, con un máximo
de dos rondas de corrección y revisión. Las recomendaciones se tratan por
separado. La revisión y corrección de la implementación tienen sus propias
reglas de finalización, descritas más adelante.

La [guía del flujo de trabajo](../user-guide/workflow.md) detalla las reglas de cada etapa.

<a id="project-structure"></a>

## Estructura del proyecto

La inicialización instala los recursos comunes y la integración del asistente seleccionado:

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

El blueprint compartido se guarda en el worktree dedicado a auto-dev. No hay
una copia editable independiente en cada checkout del flujo estándar. Los
borradores de revisión manual del conocimiento se excluyen de Git.

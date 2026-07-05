# Inicio rápido

Esta página recorre el flujo completo de **Requirements-First SDD** en ocho pasos.
Los requisitos confirmados son la autoridad de máxima prioridad, y nada es vinculante hasta que tú lo confirmes de forma explícita: cada etapa termina en un **Confirmation Gate** que tú controlas.

Para cambios pequeños y bien delimitados puedes omitir el recorrido completo y ejecutar `/codexspec:quick` en su lugar.

## 1. Inicializar un proyecto

Tras la instalación, crea o inicializa tu proyecto:

```bash
# Crear un proyecto nuevo
codexspec init my-awesome-project

# O inicializar en el directorio actual
codexspec init . --ai claude

# Con salida en chino (establece la base de salida)
codexspec init my-project --lang zh-CN

# Totalmente no interactivo (CI/scripts): base de salida zh-CN, mensajes de commit en inglés
codexspec init my-project --lang zh-CN --commit-lang en

# Establecer cada dimensión de idioma explícitamente (scriptable, sin prompts)
codexspec init my-project \
  --interaction-lang zh-CN --document-lang en --commit-lang en
```

A continuación, entra en el proyecto y lanza Claude Code:

```bash
cd my-awesome-project
claude
```

## 2. Establecer los principios del proyecto

Usa el comando constitution para fijar los estándares contra los que se verificarán todos los artefactos posteriores:

```
/codexspec:constitution Crear principios centrados en calidad de código y pruebas
```

## 3. Clarificar requisitos

Usa `/codexspec:specify` para explorar los requisitos:

```
/codexspec:specify Quiero construir una aplicación de gestión de tareas
```

Este comando formula preguntas aclaratorias, saca a la luz casos límite y te pide confirmar un resumen final de requisitos que se persiste en `requirements.md`.

> **Confirmation Gate**: `/codexspec:specify` solo escribe las entradas que confirmas explícitamente. El resumen de requisitos que presenta **no** es vinculante hasta que lo aceptas: recházalo, modifícalo o reabre cualquier punto antes de decir que sí. Nada en fases posteriores puede sobrescribir lo que aquí confirmas.

## 4. Generar la especificación

Una vez confirmado el resumen de requisitos, genera el documento de especificación:

```
/codexspec:generate-spec
```

`generate-spec` compila las entradas confirmadas en un `spec.md` estructurado con referencias de origen para trazabilidad, y luego ejecuta una revisión automática (los defectos requieren evidencia concreta; las sugerencias consultivas nunca disparan cambios automáticos; los defectos verificados pueden corregirse y volverse a revisar como máximo dos rondas).

## 5. Revisar y validar

**Recomendado:** valida la especificación antes de continuar:

```
/codexspec:review-spec
```

Se trata de una **revisión basada en evidencia**: todo defecto reportado cita evidencia concreta, y las recomendaciones de diseño se mantienen separadas de la aceptación.

## 6. Crear el plan técnico

```
/codexspec:spec-to-plan Usar Python FastAPI para el backend
```

El plan registra enlaces `Covers` hacia los requisitos de la especificación y verifica los principios de constitución aplicables.

## 7. Generar tareas

```
/codexspec:plan-to-tasks
```

Las tareas se organizan en torno a resultados verificables, con enlaces de trazabilidad hacia el plan y los requisitos. El orden test-first se aplica de forma **condicional**: únicamente donde el plan, la constitución o el riesgo de la tarea lo exigen. Las tareas no testeables (docs, configuración) se implementan directamente.

## 8. Implementar

```
/codexspec:implement-tasks
```

La implementación sigue **conditional TDD**: las tareas de código usan el ciclo Red → Green → Verify → Refactor cuando es necesario; las tareas de documentación y configuración se implementan directamente.

## Cambios pequeños: `/codexspec:quick`

Para un cambio pequeño y bien delimitado no necesitas el recorrido completo de ocho pasos. `/codexspec:quick` ejecuta un flujo compacto de Requirements-First SDD en un único comando:

```
/codexspec:quick Añadir una casilla "recuérdame" al formulario de inicio de sesión
```

Quick respeta las mismas salvaguardas que el flujo completo:

- Crea un espacio de trabajo de funcionalidad y un `requirements.md` usando la misma convención de marca de tiempo que `/codexspec:specify`.
- Presenta un resumen conciso de requisitos confirmados (`NEED-*`, `CON-*`/`DEC-*` relevantes, `OUT-*`, `OPEN-*` sin resolver) y espera tu confirmación explícita: el **Confirmation Gate** sigue vigente.
- Luego encadena `/codexspec:generate-spec` → `/codexspec:spec-to-plan` → `/codexspec:plan-to-tasks` → `/codexspec:implement-tasks` sobre ese directorio de funcionalidad, donde cada comando de generación gestiona su propio bucle automático de revisión.

Si el cambio resulta amplio o tiene múltiples resultados independientes, Quick se detiene y recomienda el flujo estándar.

## Estructura del proyecto

Tras la inicialización:

```
my-project/
├── .codexspec/
│   ├── memory/
│   │   └── constitution.md    # Constitución del proyecto
│   ├── specs/
│   │   └── {feature-id}/
│   │       ├── spec.md        # Especificación de la funcionalidad
│   │       ├── plan.md        # Plan técnico
│   │       ├── tasks.md       # Desglose de tareas
│   │       └── checklists/    # Listas de verificación de calidad
│   ├── templates/             # Plantillas personalizadas
│   ├── scripts/               # Scripts auxiliares
│   └── extensions/            # Extensiones personalizadas
├── .claude/
│   └── commands/              # Slash commands de Claude Code
├── .agents/
│   └── skills/                # Skills de Codex (cuando se inicializa con --ai codex o both)
├── CLAUDE.md                  # Contexto de Claude Code
└── AGENTS.md                  # Contexto de Codex
```

## Próximos pasos

[Guía completa del flujo de trabajo](../user-guide/workflow.md)

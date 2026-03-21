# Flujo de Trabajo

CodexSpec estructura el desarrollo en **puntos de control revisables** con validación humana en cada etapa.

## Resumen del Flujo de Trabajo

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    Flujo de Trabajo de Colaboración Humano-AI CodexSpec  │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. Constitution  ──►  Definir principios del proyecto                   │
│         │                                                                │
│         ▼                                                                │
│  2. Specify  ───────►  Q&A interactivo para clarificar requisitos        │
│         │                                                                │
│         ▼                                                                │
│  3. Generate Spec  ─►  Crear documento spec.md                           │
│         │               ✓ Revisión automática: genera review-spec.md     │
│         ▼                                                                │
│  4. Spec to Plan  ──►  Crear plan técnico                                │
│         │               ✓ Revisión automática: genera review-plan.md     │
│         ▼                                                                │
│  5. Plan to Tasks  ─►  Generar tareas atómicas                           │
│         │               ✓ Revisión automática: genera review-tasks.md    │
│         ▼                                                                │
│  6. Implement  ─────►  Ejecutar con flujo de trabajo TDD condicional     │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## Por Qué Importa la Revisión

| Sin Revisión | Con Revisión |
|---------------|-------------|
| AI hace suposiciones incorrectas | El humano detecta malas interpretaciones temprano |
| Requisitos incompletos se propagan | Brechas identificadas antes de la implementación |
| La arquitectura se desvía de la intención | Alineación verificada en cada etapa |
| **Resultado: Retrabajo** | **Resultado: Correcto a la primera** |

## Revisión Automática

Cada comando de generación ahora **ejecuta automáticamente una revisión**:

- `/codexspec:generate-spec` → invoca automáticamente `review-spec`
- `/codexspec:spec-to-plan` → invoca automáticamente `review-plan`
- `/codexspec:plan-to-tasks` → invoca automáticamente `review-tasks`

Los informes de revisión se generan junto con los artefactos, permitiendo ver problemas inmediatamente.

## Bucle de Calidad Iterativo

Cuando se encuentran problemas en los informes de revisión, describe las correcciones en lenguaje natural y el sistema actualizará tanto el artefacto como el informe:

```
┌──────────────────────────────────────────────────────────────────────┐
│                    Bucle de Calidad Iterativo                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Artefacto (spec/plan/tasks.md)                                       │
│         │                                                             │
│         ▼                                                             │
│  Revisión automática  ───►  Informe de revisión (review-*.md)         │
│         │                       │                                     │
│         │                       ▼                                     │
│         │                ¿Problemas encontrados?                       │
│         │                       │                                     │
│         │                 ┌─────┴─────┐                               │
│         │                 │           │                               │
│         │                Sí          No                               │
│         │                 │           │                               │
│         │                 ▼           ▼                               │
│         │       Describir        Continuar al                         │
│         │       corrección       siguiente paso                       │
│         │       en conversación                                           │
│         │                 │                                           │
│         │                 ▼                                           │
│         │       Actualizar simultáneamente:                            │
│         │         • Artefacto (spec/plan/tasks.md)                     │
│         │         • Informe de revisión (review-*.md)                  │
│         │                 │                                           │
│         └─────────────────┘                                           │
│           (Repetir hasta estar satisfecho)                            │
│                                                                       │
│  Revisión manual: Ejecuta /codexspec:review-* en cualquier momento    │
│  para obtener un análisis nuevo                                       │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

**Cómo funciona**:

1. **Revisión automática**: Cada comando de generación ejecuta automáticamente la revisión correspondiente
2. **Informe de revisión**: Genera archivos `review-*.md` que contienen los problemas encontrados
3. **Corrección iterativa**: Describe qué necesita corrección en la conversación, el artefacto y el informe se actualizan juntos
4. **Revisión manual**: Ejecuta `/codexspec:review-spec|plan|tasks` en cualquier momento para un análisis nuevo

## Comandos Principales

| Etapa | Comando | Propósito |
|-------|---------|---------|
| 1 | `/codexspec:constitution` | Definir principios del proyecto |
| 2 | `/codexspec:specify` | Q&A interactivo para requisitos |
| 3 | `/codexspec:generate-spec` | Crear documento de especificación (★ Revisión automática) |
| - | `/codexspec:review-spec` | Invocado automáticamente, o revalidar manualmente |
| 4 | `/codexspec:spec-to-plan` | Crear plan técnico (★ Revisión automática) |
| - | `/codexspec:review-plan` | Invocado automáticamente, o revalidar manualmente |
| 5 | `/codexspec:plan-to-tasks` | Desglosar en tareas (★ Revisión automática) |
| - | `/codexspec:review-tasks` | Invocado automáticamente, o revalidar manualmente |
| 6 | `/codexspec:implement-tasks` | Ejecutar implementación |

## Especificación en Dos Fases

### specify vs clarify

| Aspecto | `/codexspec:specify` | `/codexspec:clarify` |
|--------|----------------------|----------------------|
| **Propósito** | Exploración inicial | Refinamiento iterativo |
| **Cuándo** | No existe spec.md | spec.md existe, necesita llenar brechas |
| **Entrada** | Tu idea inicial | spec.md existente |
| **Salida** | Ninguna (solo diálogo) | Actualiza spec.md |

## TDD Condicional

La implementación sigue TDD condicional:

- **Tareas de código**: Test-first (Red → Green → Verify → Refactor)
- **Tareas no testeables** (docs, config): Implementación directa

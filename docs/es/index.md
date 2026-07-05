<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/images/codexspec-logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/images/codexspec-logo-light.svg">
  <img alt="CodexSpec Logo" src="assets/images/codexspec-logo-light.svg" width="420">
</picture>

# Bienvenido a CodexSpec

[![PyPI version](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Un toolkit de SDD Requirements-First para Claude Code**

CodexSpec te ayuda a construir software de alta calidad mediante **Spec-Driven Development (SDD) Requirements-First**: los requisitos confirmados son la autoridad de máxima prioridad, y nada es vinculante hasta que tú lo confirmes de forma explícita. En lugar de saltar directamente al código, confirmas **qué** construir y **por qué** antes de decidir **cómo** construirlo.

## ¿Por qué CodexSpec?

¿Por qué usar CodexSpec sobre Claude Code? Aquí la comparativa:

| Aspecto | Solo Claude Code | CodexSpec + Claude Code |
|--------|------------------|-------------------------|
| **Soporte multilingüe** | Interacción por defecto en inglés | Configura el idioma del equipo para una colaboración y revisión más fluidas |
| **Trazabilidad** | Difícil rastrear decisiones tras cerrar la sesión | Todas las especificaciones, planes y tareas se guardan en `.codexspec/specs/` |
| **Recuperación de sesión** | Las interrupciones del modo plan son difíciles de recuperar | División entre comandos + documentación persistente = recuperación sencilla |
| **Gobernanza del equipo** | Sin principios unificados, estilos inconsistentes | `constitution.md` impone estándares y calidad al equipo |

### ¿Qué es Requirements-First SDD?

**Requirements-First SDD** es la metodología Spec-Driven Development (SDD) con una mejora: **los requisitos confirmados son la autoridad de máxima prioridad**. Defines y confirmas *qué* construir y *por qué* antes de decidir *cómo*, y nada se vuelve vinculante hasta que lo confirmas explícitamente.

```
Tradicional:   Idea → Código → Depurar → Reescribir
SDD:           Idea → Requisitos Confirmados → Especificación → Plan → Tareas → Código
```

### Características principales

- **Desarrollo basado en Constitución**: establece principios de proyecto que guían todas las decisiones
- **Captura persistente de requisitos**: `/specify` registra la discusión confirmada en `requirements.md` antes de generar documentación
- **Revisiones automáticas**: toda especificación, plan y tarea generados incluyen comprobaciones de calidad integradas
- **Clarificación interactiva**: refinamiento de requisitos mediante preguntas y respuestas
- **Análisis entre artefactos**: detecta inconsistencias antes de la implementación
- **Tareas trazables**: el desglose de tareas conserva la cobertura de requisitos y plan, aplicando **Conditional TDD** (orden test-first únicamente donde el plan, la constitución o el riesgo lo exigen; las tareas no testeables como docs/config se implementan directamente)
- **Integración nativa con Claude Code**: los slash commands funcionan de forma transparente
- **Soporte multilingüe**: más de 13 idiomas mediante traducción dinámica con LLM
- **Multiplataforma**: incluye scripts en Bash y PowerShell
- **Extensible**: arquitectura de plugins para comandos personalizados

## Inicio rápido

```bash
# Instalar
uv tool install codexspec

# Crear un nuevo proyecto
codexspec init my-project

# O inicializar en un proyecto existente
codexspec init . --ai claude
```

[Guía completa de instalación](getting-started/installation.md)

## Visión general del flujo de trabajo

CodexSpec estructura el desarrollo en **puntos de control revisables**. Los requisitos confirmados fluyen a través de especificaciones, planes y tareas hasta llegar al código, con una revisión en cada etapa.

```
Idea → Requisitos Confirmados → Especificación → Plan → Tareas → Código
```

Cada artefacto se produce mediante un comando dedicado y se valida antes de iniciar la etapa siguiente:

```
Idea → /specify → requirements.md → /generate-spec → spec.md → /spec-to-plan → plan.md → /plan-to-tasks → tasks.md → /implement
                                                   │                         │                            │
                                         Revisar especificación        Revisar plan                Revisar tareas
```

### El Confirmation Gate

El diferenciador definitorio es el **Confirmation Gate**: los requisitos, especificaciones, planes y tareas se vuelven vinculantes solo tras tu confirmación humana explícita. Los requisitos confirmados son la autoridad de máxima prioridad sobre las funcionalidades, de modo que la IA no puede bloquear decisiones en silencio: los artefactos derivados incluyen enlaces explícitos a su origen, y los conflictos se rastrean hacia atrás en lugar de propagarse.

### Bucle iterativo de calidad

Cada comando de generación incluye una **revisión automática basada en evidencia**: los defectos requieren evidencia concreta, las sugerencias consultivas nunca disparan cambios automáticos, y los defectos verificados pueden corregirse y volverse a revisar como máximo dos rondas. Este bucle mantiene la calidad en ascenso sin que tengas que vigilar cada detalle.

[Conoce el flujo de trabajo](user-guide/workflow.md)

## Licencia

Licencia MIT: consulta [LICENSE](https://github.com/Zts0hg/codexspec/blob/main/LICENSE) para más detalles.

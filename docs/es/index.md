<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/images/codexspec-logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/images/codexspec-logo-light.svg">
  <img alt="CodexSpec Logo" src="assets/images/codexspec-logo-light.svg" width="420">
</picture>

# Bienvenido a CodexSpec

[![PyPI version](https://img.shields.io/pypi/v/codexspec:svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec:svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Un kit de herramientas de Spec-Driven Development (SDD) para Claude Code**

CodexSpec es un kit de herramientas que te ayuda a construir software de alta calidad utilizando un enfoque estructurado basado en especificaciones. Invierte el script del desarrollo tradicional haciendo que las especificaciones sean artefactos ejecutables que guían directamente la implementación.

## Por que CodexSpec?

### Colaboracion Humano-AI

CodexSpec se basa en la creencia de que **el desarrollo asistido por AI efectivo requiere participacion humana activa en cada etapa**.

| Problema | Solucion |
|---------|----------|
| Requisitos poco claros | Q&A interactivo para aclarar antes de construir |
| Especificaciones incompletas | Comandos de revision dedicados con puntuacion |
| Planes tecnicos desalineados | Validacion basada en la constitucion |
| Desgloses de tareas vagos | Generacion de tareas con TDD aplicado |

### Caracteristicas Clave

- **Basado en Constitucion** - Establece principios de proyecto que guian todas las decisiones
- **Clarificacion Interactiva** - Refinamiento de requisitos basado en Q&A
- **Comandos de Revision** - Valida artefactos en cada etapa
- **Preparado para TDD** - Metodologia test-first integrada en las tareas
- **Soporte i18n** - Mas de 13 idiomas mediante traduccion LLM

## Inicio Rapido

```bash
# Instalar
uv tool install codexspec

# Crear un nuevo proyecto
codexspec init my-project

# O inicializar en un proyecto existente
codexspec init . --ai claude
```

[Guia de Instalacion Completa](getting-started/installation.md)

## Resumen del Flujo de Trabajo

```
Idea -> Clarificar -> Revisar -> Planificar -> Revisar -> Tareas -> Revisar -> Implementar
            ^              ^              ^
         Chequeos humanos  Chequeos humanos  Chequeos humanos
```

Cada artefacto tiene un comando de revision correspondiente para validar la salida de AI antes de continuar.

[Aprender el Flujo de Trabajo](user-guide/workflow.md)

## Licencia

Licencia MIT - ver [LICENSE](https://github.com/Zts0hg/codexspec/blob/main/LICENSE) para mas detalles.

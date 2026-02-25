# CodexSpec

[English](README.md) | [中文](README.zh-CN.md) | [日本語](README.ja.md) | **Español** | [Português](README.pt-BR.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md)

[![PyPI version](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**[📖 Documentación](https://zts0hg.github.io/codexspec/)**

**Un toolkit de Desarrollo Guiado por Especificaciones (SDD) para Claude Code**

CodexSpec es un toolkit que te ayuda a construir software de alta calidad utilizando un enfoque estructurado y guiado por especificaciones. Invierte el script del desarrollo tradicional convirtiendo las especificaciones en artefactos ejecutables que guían directamente la implementación.

## Filosofía de Diseño: Colaboración Humano-AI

CodexSpec está construido sobre la creencia de que **el desarrollo efectivo asistido por IA requiere participación humana activa en cada etapa**. El toolkit está diseñado alrededor de un principio fundamental:

> **Revisar y validar cada artefacto antes de avanzar.**

### Por Qué Importa la Supervisión Humana

En el desarrollo asistido por IA, saltarse las etapas de revisión lleva a:

| Problema | Consecuencia |
|----------|--------------|
| Requisitos poco claros | La IA hace suposiciones que divergen de tu intención |
| Especificaciones incompletas | Se construyen características sin casos límite críticos |
| Planes técnicos desalineados | La arquitectura no coincide con las necesidades del negocio |
| Desgloses de tareas vagos | La implementación se desvía, requiriendo retrabajo costoso |

### El Enfoque de CodexSpec

CodexSpec estructura el desarrollo en **puntos de control revisables**:

```
Idea → Clarificar → Revisar → Planificar → Revisar → Tareas → Revisar → Analizar → Implementar
               ↑                  ↑                  ↑
            Chequeo humano     Chequeo humano     Chequeo humano
```

**Cada artefacto tiene un comando de revisión correspondiente:**
- `spec.md` → `/codexspec.review-spec`
- `plan.md` → `/codexspec.review-plan`
- `tasks.md` → `/codexspec.review-tasks`
- Todos los artefactos → `/codexspec.analyze`

Este proceso sistemático de revisión asegura:
- **Detección temprana de errores**: Capturar malentendidos antes de escribir código
- **Verificación de alineación**: Confirmar que la interpretación de la IA coincide con tu intención
- **Puertas de calidad**: Validar completitud, claridad y viabilidad en cada etapa
- **Reducción de retrabajo**: Invertir minutos en revisión para ahorrar horas de reimplementación

## Características

### Flujo de Trabajo SDD Central
- **Basado en Constitución**: Establecer principios del proyecto que guían todas las decisiones posteriores
- **Especificación en Dos Fases**: Clarificación interactiva (`/specify`) seguida de generación de documento (`/generate-spec`)
- **Desarrollo Guiado por Planes**: Las decisiones técnicas vienen después de validar los requisitos
- **Tareas Preparadas para TDD**: Los desgloses de tareas aplican metodología test-first

### Colaboración Humano-AI
- **Comandos de Revisión**: Comandos de revisión dedicados para spec, plan y tareas para validar salida de IA
- **Clarificación Interactiva**: Refinamiento de requisitos basado en Q&A con retroalimentación inmediata
- **Análisis Entre Artefactos**: Detectar inconsistencias entre spec, plan y tareas antes de la implementación
- **Checklists de Calidad**: Evaluación automatizada de calidad para requisitos

### Experiencia del Desarrollador
- **Integración con Claude Code**: Comandos slash nativos para Claude Code
- **Internacionalización (i18n)**: Soporte multilingüe mediante traducción dinámica LLM
- **Multiplataforma**: Soporte para scripts Bash y PowerShell
- **Extensible**: Arquitectura de plugins para comandos personalizados

## Instalación

### Requisitos previos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recomendado) o pip

### Opción 1: Instalar con uv (Recomendado)

La forma más fácil de instalar CodexSpec es usando uv:

```bash
uv tool install codexspec
```

### Opción 2: Instalar con pip

Alternativamente, puedes usar pip:

```bash
pip install codexspec
```

### Opción 3: Uso único

Ejecutar directamente sin instalar:

```bash
# Crear un nuevo proyecto
uvx codexspec init my-project

# Inicializar en un proyecto existente
cd your-existing-project
uvx codexspec init . --ai claude
```

### Opción 4: Instalar desde GitHub (Versión de Desarrollo)

Para obtener la última versión de desarrollo o una rama específica:

```bash
# Usando uv
uv tool install git+https://github.com/Zts0hg/codexspec.git

# Usando pip
pip install git+https://github.com/Zts0hg/codexspec.git

# Rama o etiqueta específica
uv tool install git+https://github.com/Zts0hg/codexspec.git@main
uv tool install git+https://github.com/Zts0hg/codexspec.git@v0.2.0
```

## Para Usuarios de Windows

### Recomendado: Usar PowerShell

**Los usuarios de Windows deben usar PowerShell para instalar y ejecutar CodexSpec**:

```powershell
# 1. Instalar uv (si aún no está instalado)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. Reiniciar PowerShell, luego instalar codexspec
uv tool install codexspec

# 3. Verificar la instalación
codexspec --version
```

### Solución de Problemas para Usuarios de CMD

Si encuentras errores de "Acceso denegado" o "spawn codexspec acceso denegado (OSError 5)" en CMD:

**Solución 1: Actualizar variables de entorno**
```cmd
# Cerrar todas las ventanas de CMD y abrir una nueva
# O actualizar manualmente PATH
set PATH=%PATH%;%USERPROFILE%\.local\bin
codexspec --version
```

**Solución 2: Usar ruta completa**
```cmd
%USERPROFILE%\.local\bin\codexspec.exe --version
```

**Solución 3: Usar pipx en lugar de uv tool**
```cmd
pip install pipx
pipx ensurepath
# Reiniciar CMD
pipx install codexspec
```

### Preguntas Frecuentes

**P: ¿Por qué funciona en PowerShell pero no en CMD?**
R: PowerShell y CMD manejan las variables de entorno de usuario de manera diferente. Cuando uv agrega rutas al PATH de usuario, PowerShell típicamente las reconoce inmediatamente, mientras que CMD puede requerir un reinicio o actualización manual.

Para más detalles, consulta la [Guía de Solución de Problemas de Windows](docs/WINDOWS-TROUBLESHOOTING.md) (en inglés).

## Inicio Rápido

Después de la instalación, puedes usar el CLI:

```bash
# Crear nuevo proyecto
codexspec init my-project

# Crear proyecto con salida en español
codexspec init my-project --lang es

# Inicializar en proyecto existente
codexspec init . --ai claude
# o
codexspec init --here --ai claude

# Verificar herramientas instaladas
codexspec check

# Ver versión
codexspec version
```

Para actualizar a la última versión:

```bash
# Usando uv
uv tool install codexspec --upgrade

# Usando pip
pip install --upgrade codexspec
```

## Uso

### 1. Inicializar un Proyecto

Después de la [instalación](#instalación), crea o inicializa tu proyecto:

```bash
codexspec init my-awesome-project
# o en el directorio actual
codexspec init . --ai claude
```

### 2. Establecer Principios del Proyecto

Inicia Claude Code en el directorio del proyecto:

```bash
cd my-awesome-project
claude
```

Usa el comando `/codexspec.constitution` para crear los principios de gobernanza del proyecto:

```
/codexspec.constitution Crear principios enfocados en calidad de código, estándares de testing y arquitectura limpia
```

### 3. Clarificar Requisitos

Usa `/codexspec.specify` para **explorar y clarificar** tus requisitos mediante Q&A interactivo:

```
/codexspec.specify Quiero construir una aplicación de gestión de tareas
```

Este comando:
- Hará preguntas de clarificación para entender tu idea
- Explorará casos límite que quizás no hayas considerado
- Co-creará requisitos de alta calidad mediante diálogo
- **NO** generará archivos automáticamente - tú mantienes el control

### 4. Generar Documento de Especificación

Una vez clarificados los requisitos, usa `/codexspec.generate-spec` para crear el documento `spec.md`:

```
/codexspec.generate-spec
```

Este comando actúa como un "compilador de requisitos" que transforma tus requisitos clarificados en un documento de especificación estructurado.

### 5. Revisar Especificación (Recomendado)

**Antes de proceder a la planificación, valida tu especificación:**

```
/codexspec.review-spec
```

Este comando genera un informe de revisión detallado con:
- Análisis de completitud de secciones
- Evaluación de claridad y testeabilidad
- Verificación de alineación con la constitución
- Recomendaciones priorizadas

### 6. Crear un Plan Técnico

Usa `/codexspec.spec-to-plan` para definir cómo implementarlo:

```
/codexspec.spec-to-plan Usar Python con FastAPI para el backend, PostgreSQL para la base de datos y React para el frontend
```

El comando incluye **revisión de constitucionalidad** - verificando que tu plan se alinea con los principios del proyecto.

### 7. Revisar Plan (Recomendado)

**Antes de desglosar en tareas, valida tu plan técnico:**

```
/codexspec.review-plan
```

Esto verifica:
- Alineación con la especificación
- Solidez de arquitectura
- Adecuación del stack tecnológico
- Cumplimiento de la constitución

### 8. Generar Tareas

Usa `/codexspec.plan-to-tasks` para desglosar el plan:

```
/codexspec.plan-to-tasks
```

Las tareas se organizan en fases estándar con:
- **Aplicación de TDD**: Las tareas de test preceden a las de implementación
- **Marcadores de paralelismo `[P]`**: Identifican tareas independientes
- **Especificaciones de rutas de archivo**: Entregables claros por tarea

### 9. Revisar Tareas (Recomendado)

**Antes de la implementación, valida el desglose de tareas:**

```
/codexspec.review-tasks
```

Esto verifica:
- Cobertura del plan
- Cumplimiento de TDD
- Corrección de dependencias
- Granularidad de tareas

### 10. Analizar (Opcional pero Recomendado)

Usa `/codexspec.analyze` para verificación de consistencia entre artefactos:

```
/codexspec.analyze
```

Esto detecta problemas entre spec, plan y tareas:
- Brechas de cobertura (requisitos sin tareas)
- Duplicaciones e inconsistencias
- Violaciones de constitución
- Elementos subespecificados

### 11. Implementar

Usa `/codexspec.implement-tasks` para ejecutar la implementación:

```
/codexspec.implement-tasks
```

La implementación sigue **flujo de trabajo TDD condicional**:
- Tareas de código: Test-first (Rojo → Verde → Verificar → Refactorizar)
- Tareas no testeables (docs, config): Implementación directa

## Comandos Disponibles

### Comandos CLI

| Comando | Descripción |
|---------|-------------|
| `codexspec init` | Inicializar un nuevo proyecto CodexSpec |
| `codexspec check` | Verificar herramientas instaladas |
| `codexspec version` | Mostrar información de versión |
| `codexspec config` | Ver o modificar configuración del proyecto |

### Opciones de `codexspec init`

| Opción | Descripción |
|--------|-------------|
| `PROJECT_NAME` | Nombre del nuevo directorio del proyecto |
| `--here`, `-h` | Inicializar en el directorio actual |
| `--ai`, `-a` | Asistente de IA a usar (por defecto: claude) |
| `--lang`, `-l` | Idioma de salida (ej: en, zh-CN, ja) |
| `--force`, `-f` | Forzar sobrescritura de archivos existentes |
| `--no-git` | Saltar inicialización de git |
| `--debug`, `-d` | Habilitar salida de depuración |

### Opciones de `codexspec config`

| Opción | Descripción |
|--------|-------------|
| `--set-lang`, `-l` | Establecer el idioma de salida |
| `--set-commit-lang`, `-c` | Establecer el idioma de los mensajes de commit (por defecto: idioma de salida) |
| `--list-langs` | Listar todos los idiomas soportados |

### Comandos Slash

Después de la inicialización, estos comandos slash están disponibles en Claude Code:

#### Comandos de Flujo de Trabajo Central

| Comando | Descripción |
|---------|-------------|
| `/codexspec.constitution` | Crear o actualizar constitución del proyecto con validación entre artefactos e informe de impacto de sincronización |
| `/codexspec.specify` | **Clarificar** requisitos mediante Q&A interactivo (sin generación de archivos) |
| `/codexspec.generate-spec` | **Generar** documento `spec.md` después de clarificar requisitos |
| `/codexspec.spec-to-plan` | Convertir especificación a plan técnico con revisión de constitucionalidad y grafo de dependencia de módulos |
| `/codexspec.plan-to-tasks` | Desglosar plan en tareas atómicas con aplicación de TDD y marcadores de paralelismo `[P]` |
| `/codexspec.implement-tasks` | Ejecutar tareas con flujo de trabajo TDD condicional (TDD para código, directo para docs/config) |

#### Comandos de Revisión (Puertas de Calidad)

| Comando | Descripción |
|---------|-------------|
| `/codexspec.review-spec` | Validar especificación por completitud, claridad, consistencia y testeabilidad con puntuación |
| `/codexspec.review-plan` | Revisar plan técnico por viabilidad, calidad de arquitectura y alineación con constitución |
| `/codexspec.review-tasks` | Validar desglose de tareas por cobertura del plan, cumplimiento TDD, dependencias y granularidad |

#### Comandos de Mejora

| Comando | Descripción |
|---------|-------------|
| `/codexspec.clarify` | Escanear spec.md existente buscando ambigüedades usando 4 categorías enfocadas, integrar con hallazgos de revisión |
| `/codexspec.analyze` | Análisis no destructivo entre artefactos (spec, plan, tareas) con detección de problemas basada en severidad |
| `/codexspec.checklist` | Generar checklists de calidad para validación de requisitos |
| `/codexspec.tasks-to-issues` | Convertir tareas a GitHub issues para integración con gestión de proyectos |

#### Comandos de Flujo de Trabajo Git

| Comando | Descripción |
|---------|-------------|
| `/codexspec.commit` | Generar mensajes de Conventional Commits basados en el estado de git y el contexto de la sesión |
| `/codexspec.commit-staged` | Generar mensaje de commit solo desde los cambios preparados |

## Resumen del Flujo de Trabajo

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    Flujo de Trabajo de Colaboración Humano-AI CodexSpec  │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. Constitución  ──►  Definir principios del proyecto                   │
│         │                         con validación entre artefactos         │
│         ▼                                                                │
│  2. Especificar  ───────►  Q&A interactivo para clarificar requisitos    │
│         │                   (sin crear archivo - control humano)          │
│         ▼                                                                │
│  3. Generar Spec  ─►  Crear documento spec.md                            │
│         │                                                                │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ PUERTA DE REVISIÓN 1: /codexspec.review-spec ★                 ║   │
│  ║  Validar: Completitud, Claridad, Testeabilidad, Constitución       ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  4. Clarificar  ───────►  Resolver ambigüedades (iterativo)              │
│         │                   4 categorías enfocadas, máx 5 preguntas       │
│         ▼                                                                │
│  5. Spec a Plan  ──────►  Crear plan técnico con:                        │
│         │                   • Revisión de constitucionalidad (OBLIGATORIO)│
│         │                   • Grafo de dependencia de módulos             │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ PUERTA DE REVISIÓN 2: /codexspec.review-plan ★                 ║   │
│  ║  Validar: Alineación Spec, Arquitectura, Stack Tech, Fases         ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  6. Plan a Tareas  ──►  Generar tareas atómicas con:                     │
│         │                   • Aplicación TDD (tests antes de impl)       │
│         │                   • Marcadores de paralelismo [P]              │
│         │                   • Especificaciones de rutas de archivo       │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ PUERTA DE REVISIÓN 3: /codexspec.review-tasks ★                ║   │
│  ║  Validar: Cobertura, Cumplimiento TDD, Dependencias, Granularidad  ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  7. Analizar  ───────►  Verificación de consistencia entre artefactos    │
│         │               Detectar brechas, duplicaciones, problemas const. │
│         ▼                                                                │
│  8. Implementar  ─────►  Ejecutar con flujo de trabajo TDD condicional   │
│                          Código: Test-first | Docs/Config: Directo        │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

**Insight Clave**: Cada puerta de revisión (★) es un **punto de control humano** donde validas la salida de la IA antes de invertir más tiempo. Saltarse estas puertas a menudo lleva a retrabajo costoso.

### Concepto Clave: Flujo de Trabajo de Clarificación de Requisitos

CodexSpec proporciona **dos comandos de clarificación distintos** para diferentes etapas del flujo de trabajo:

#### specify vs clarify: ¿Cuál usar cuándo?

| Aspecto | `/codexspec.specify` | `/codexspec.clarify` |
|---------|----------------------|----------------------|
| **Propósito** | Exploración inicial de requisitos | Refinamiento iterativo de spec existente |
| **Cuándo usar** | Empezar con idea nueva, no existe spec.md | spec.md existe, necesita llenar brechas |
| **Entrada** | Tu idea o requisito inicial | Archivo spec.md existente |
| **Salida** | Ninguna (solo diálogo) | Actualiza spec.md con clarificaciones |
| **Método** | Q&A abierto | Escaneo de ambigüedad estructurado (4 categorías) |
| **Límite de preguntas** | Sin límite | Máximo 5 preguntas |
| **Uso típico** | "Quiero construir una app de tareas" | "La spec carece de detalles de manejo de errores" |

#### Especificación en Dos Fases

Antes de generar cualquier documentación:

| Fase | Comando | Propósito | Salida |
|------|---------|-----------|--------|
| **Exploración** | `/codexspec.specify` | Q&A interactivo para explorar y refinar requisitos | Ninguna (solo diálogo) |
| **Generación** | `/codexspec.generate-spec` | Compilar requisitos clarificados en documento estructurado | `spec.md` |

#### Clarificación Iterativa

Después de crear spec.md:

```
spec.md ──► /codexspec.clarify ──► spec.md actualizado (con sección Clarifications)
                │
                └── Escanea ambigüedades en 4 categorías enfocadas:
                    • Brechas de Completitud - Secciones faltantes, contenido vacío
                    • Problemas de Especificidad - Términos vagos, restricciones no definidas
                    • Claridad de Comportamiento - Manejo de errores, transiciones de estado
                    • Problemas de Medibilidad - Requisitos no funcionales sin métricas
```

#### Beneficios de este Diseño

- **Colaboración humano-AI**: Participas activamente en el descubrimiento de requisitos
- **Control explícito**: Los archivos solo se crean cuando tú decides
- **Enfoque en calidad**: Los requisitos se exploran completamente antes de documentar
- **Refinamiento iterativo**: Las specs pueden mejorarse incrementalmente a medida que se profundiza el entendimiento

## Estructura del Proyecto

Después de la inicialización, tu proyecto tendrá esta estructura:

```
my-project/
├── .codexspec/
│   ├── memory/
│   │   └── constitution.md    # Principios de gobernanza del proyecto
│   ├── specs/
│   │   └── {feature-id}/
│   │       ├── spec.md        # Especificación de característica
│   │       ├── plan.md        # Plan técnico
│   │       ├── tasks.md       # Desglose de tareas
│   │       └── checklists/    # Checklists de calidad
│   ├── templates/             # Plantillas personalizadas
│   ├── scripts/               # Scripts de ayuda
│   │   ├── bash/              # Scripts Bash
│   │   └── powershell/        # Scripts PowerShell
│   └── extensions/            # Extensiones personalizadas
├── .claude/
│   └── commands/              # Comandos slash para Claude Code
└── CLAUDE.md                  # Contexto para Claude Code
```

## Internacionalización (i18n)

CodexSpec soporta múltiples idiomas a través de **traducción dinámica LLM**. En lugar de mantener plantillas traducidas, dejamos que Claude traduzca el contenido en tiempo real basándose en tu configuración de idioma.

### Establecer Idioma

**Durante la inicialización:**
```bash
# Crear un proyecto con salida en chino
codexspec init my-project --lang zh-CN

# Crear un proyecto con salida en japonés
codexspec init my-project --lang ja
```

**Después de la inicialización:**
```bash
# Ver configuración actual
codexspec config

# Cambiar configuración de idioma
codexspec config --set-lang zh-CN

# Listar idiomas soportados
codexspec config --list-langs
```

### Idioma de los Mensajes de Commit

Puedes configurar un idioma diferente para los mensajes de commit que el idioma de salida:

```bash
# Usar español para interacciones pero inglés para mensajes de commit
codexspec config --set-lang es
codexspec config --set-commit-lang en
```

**Prioridad de idioma para mensajes de commit:**
1. Configuración `language.commit` (si se especifica)
2. `language.output` (alternativa)
3. `"en"` (por defecto)

**Nota:** El tipo de commit (feat, fix, docs, etc.) y el ámbito siempre permanecen en inglés. Solo la parte de la descripción usa el idioma configurado.

### Archivo de Configuración

El archivo `.codexspec/config.yml` almacena la configuración de idioma:

```yaml
version: "1.0"

language:
  # Idioma de salida para interacciones con Claude y documentos generados
  output: "zh-CN"

  # Idioma de los mensajes de commit (por defecto: idioma de salida)
  # Establecer como "en" para mensajes de commit en inglés independientemente del idioma de salida
  commit: "zh-CN"

  # Idioma de plantillas - mantener como "en" para compatibilidad
  templates: "en"

project:
  ai: "claude"
  created: "2026-02-15"
```

### Idiomas Soportados

| Código | Idioma |
|--------|--------|
| `en` | English (por defecto) |
| `zh-CN` | Chinese (Simplified) |
| `zh-TW` | Chinese (Traditional) |
| `ja` | Japanese |
| `ko` | Korean |
| `es` | Spanish |
| `fr` | French |
| `de` | German |
| `pt` | Portuguese |
| `ru` | Russian |
| `it` | Italian |
| `ar` | Arabic |
| `hi` | Hindi |

### Cómo Funciona

1. **Plantillas en Inglés Únicamente**: Todas las plantillas de comandos permanecen en inglés
2. **Configuración de Idioma**: El proyecto especifica el idioma de salida preferido
3. **Traducción Dinámica**: Claude lee instrucciones en inglés, genera salida en idioma objetivo
4. **Consciente del Contexto**: Los términos técnicos (JWT, OAuth, etc.) permanecen en inglés cuando es apropiado

### Beneficios

- **Cero Mantenimiento de Traducción**: No es necesario mantener múltiples versiones de plantillas
- **Siempre Actualizado**: Las actualizaciones de plantillas benefician automáticamente a todos los idiomas
- **Traducción Consciente del Contexto**: Claude proporciona traducciones naturales y apropiadas para el contexto
- **Idiomas Ilimitados**: Cualquier idioma soportado por Claude funciona inmediatamente

### Constitution y Documentos Generados

Cuando usas `/codexspec.constitution` para crear la constitución de tu proyecto, se generará en el idioma especificado en tu configuración:

- **Enfoque de Archivo Único**: La constitución se genera en un solo idioma
- **Claude Entiende Todos los Idiomas**: Claude puede trabajar con archivos de constitución en cualquier idioma soportado
- **Colaboración en Equipo**: Los equipos deben usar un idioma de trabajo consistente

Este diseño evita problemas de sincronización entre múltiples versiones de idiomas y reduce la sobrecarga de mantenimiento.

## Sistema de Extensiones

CodexSpec soporta una arquitectura de plugins para agregar comandos personalizados:

### Estructura de Extensión

```
mi-extension/
├── extension.yml          # Manifiesto de extensión
├── commands/              # Comandos slash personalizados
│   └── comando.md
└── README.md
```

### Crear Extensiones

1. Copia la plantilla desde `extensions/template/`
2. Modifica `extension.yml` con los detalles de tu extensión
3. Agrega tus comandos personalizados en `commands/`
4. Prueba localmente y publica

Consulta `extensions/EXTENSION-DEVELOPMENT-GUIDE.md` para más detalles.

## Desarrollo

### Requisitos Previos

- Python 3.11+
- Gestor de paquetes uv
- Git

### Desarrollo Local

```bash
# Clonar el repositorio
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Instalar dependencias de desarrollo
uv sync --dev

# Ejecutar localmente
uv run codexspec --help

# Ejecutar pruebas
uv run pytest

# Revisar código con linter
uv run ruff check src/
```

### Compilación

```bash
# Compilar el paquete
uv build
```

## Comparación con spec-kit

CodexSpec está inspirado en spec-kit de GitHub pero con algunas diferencias clave:

| Característica | spec-kit | CodexSpec |
|----------------|----------|-----------|
| Filosofía Central | Desarrollo guiado por especificaciones | Desarrollo guiado por especificaciones + colaboración humano-AI |
| Nombre del CLI | `specify` | `codexspec` |
| IA Principal | Soporte multi-agente | Enfocado en Claude Code |
| Prefijo de Comandos | `/speckit.*` | `/codexspec.*` |
| Sistema de Constitución | Básico | Constitución completa con validación entre artefactos |
| Spec en Dos Fases | No | Sí (clarificar + generar) |
| Comandos de Revisión | Opcional | 3 comandos de revisión dedicados con puntuación |
| Comando Clarify | Sí | 4 categorías enfocadas, integración con revisión |
| Comando Analyze | Sí | Solo lectura, basado en severidad, consciente de constitución |
| TDD en Tareas | Opcional | Aplicado (tests preceden implementación) |
| Implementación | Estándar | TDD condicional (código vs docs/config) |
| Sistema de Extensiones | Sí | Sí |
| Scripts PowerShell | Sí | Sí |
| Soporte i18n | No | Sí (13+ idiomas vía traducción LLM) |

### Diferenciadores Clave

1. **Cultura de Revisión Primero**: Cada artefacto principal tiene un comando de revisión dedicado
2. **Gobernanza por Constitución**: Los principios se validan, no solo se documentan
3. **TDD por Defecto**: Metodología test-first aplicada en generación de tareas
4. **Puntos de Control Humanos**: Flujo de trabajo diseñado alrededor de puertas de validación

## Filosofía

CodexSpec sigue estos principios fundamentales:

### Fundamentos SDD

1. **Desarrollo guiado por intenciones**: Las especificaciones definen el "qué" antes del "cómo"
2. **Creación rica de especificaciones**: Usar barreras y principios organizacionales
3. **Refinamiento en múltiples pasos**: En lugar de generación de código de un solo shot
4. **Gobernanza por constitución**: Los principios del proyecto guían todas las decisiones

### Colaboración Humano-AI

5. **Humano en el ciclo**: La IA genera artefactos, los humanos los validan
6. **Orientado a revisión**: Validar cada artefacto antes de avanzar
7. **Revelación progresiva**: Información compleja revelada incrementalmente
8. **Explícito sobre implícito**: Los requisitos deben ser claros, no asumidos

### Aseguramiento de Calidad

9. **Test-driven por defecto**: Flujo de trabajo TDD integrado en generación de tareas
10. **Consistencia entre artefactos**: Analizar spec, plan y tareas juntos
11. **Alineación con constitución**: Todos los artefactos respetan los principios del proyecto

### Por Qué Importa la Revisión

| Sin Revisión | Con Revisión |
|--------------|--------------|
| La IA hace suposiciones incorrectas | El humano captura malas interpretaciones temprano |
| Requisitos incompletos se propagan | Brechas identificadas antes de implementación |
| La arquitectura se desvía de la intención | Alineación verificada en cada etapa |
| Las tareas pierden funcionalidad crítica | Cobertura validada sistemáticamente |
| **Resultado: Retrabajo, esfuerzo desperdiciado** | **Resultado: Correcto a la primera** |

## Contribuir

¡Las contribuciones son bienvenidas! Por favor lee nuestras guías de contribución antes de enviar un pull request.

## Licencia

Licencia MIT - ver [LICENSE](LICENSE) para detalles.

## Agradecimientos

- Inspirado por [GitHub spec-kit](https://github.com/github/spec-kit)
- Construido para [Claude Code](https://claude.ai/code)

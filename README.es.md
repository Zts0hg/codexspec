# CodexSpec

[English](README.md) | [中文](README.zh-CN.md) | [日本語](README.ja.md) | **Español** | [Português](README.pt-BR.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md)

[![PyPI version](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Un toolkit de Desarrollo Guiado por Especificaciones (SDD) para Claude Code**

CodexSpec es un toolkit que te ayuda a construir software de alta calidad utilizando un enfoque estructurado y guiado por especificaciones. Invierte el script del desarrollo tradicional convirtiendo las especificaciones en artefactos ejecutables que guían directamente la implementación.

## Características

- **Flujo de trabajo estructurado**: Comandos claros para cada fase del desarrollo
- **Integración con Claude Code**: Comandos slash nativos para Claude Code
- **Basado en constitución**: Los principios del proyecto guían todas las decisiones
- **Especificaciones primero**: Define qué y por qué antes del cómo
- **Guiado por planes**: Las decisiones técnicas vienen después de los requisitos
- **Orientado a tareas**: Divide la implementación en tareas accionables
- **Aseguramiento de calidad**: Comandos integrados de revisión, análisis y checklists
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

## Inicio Rápido

Después de la instalación, puedes usar el CLI:

```bash
# Crear nuevo proyecto (salida en español)
codexspec init my-project --lang es

# Inicializar en proyecto existente
codexspec init . --ai claude

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
codexspec init my-awesome-project --lang es
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

### 5. Crear un Plan Técnico

Usa `/codexspec.spec-to-plan` para definir cómo implementarlo:

```
/codexspec.spec-to-plan Usar Python con FastAPI para el backend, PostgreSQL para la base de datos y React para el frontend
```

### 6. Generar Tareas

Usa `/codexspec.plan-to-tasks` para desglosar el plan:

```
/codexspec.plan-to-tasks
```

### 7. Analizar (Opcional pero Recomendado)

Usa `/codexspec.analyze` para verificación de consistencia entre artefactos:

```
/codexspec.analyze
```

### 8. Implementar

Usa `/codexspec.implement-tasks` para ejecutar la implementación:

```
/codexspec.implement-tasks
```

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
| `--lang`, `-l` | Idioma de salida (ej: en, es, zh-CN, ja) |
| `--force`, `-f` | Forzar sobrescritura de archivos existentes |
| `--no-git` | Saltar inicialización de git |
| `--debug`, `-d` | Habilitar salida de depuración |

### Opciones de `codexspec config`

| Opción | Descripción |
|--------|-------------|
| `--set-lang`, `-l` | Establecer el idioma de salida |
| `--list-langs` | Listar todos los idiomas soportados |

### Comandos Slash

Después de la inicialización, estos comandos slash están disponibles en Claude Code:

#### Comandos Principales

| Comando | Descripción |
|---------|-------------|
| `/codexspec.constitution` | Crear o actualizar principios de gobernanza del proyecto |
| `/codexspec.specify` | **Clarificar** requisitos mediante Q&A interactivo (sin generación de archivos) |
| `/codexspec.generate-spec` | **Generar** documento `spec.md` después de clarificar requisitos |
| `/codexspec.spec-to-plan` | Convertir especificación a plan técnico |
| `/codexspec.plan-to-tasks` | Desglosar plan en tareas accionables |
| `/codexspec.implement-tasks` | Ejecutar tareas según el desglose |

#### Comandos de Revisión

| Comando | Descripción |
|---------|-------------|
| `/codexspec.review-spec` | Revisar completitud de la especificación |
| `/codexspec.review-plan` | Revisar viabilidad del plan técnico |
| `/codexspec.review-tasks` | Revisar completitud del desglose de tareas |

#### Comandos Mejorados

| Comando | Descripción |
|---------|-------------|
| `/codexspec.clarify` | Escanear spec.md existente para ambigüedades y actualizar con clarificaciones |
| `/codexspec.analyze` | Análisis de consistencia entre artefactos |
| `/codexspec.checklist` | Generar checklists de calidad para requisitos |
| `/codexspec.tasks-to-issues` | Convertir tareas a GitHub issues |

## Resumen del Flujo de Trabajo

```
┌──────────────────────────────────────────────────────────────┐
│                    Flujo de Trabajo CodexSpec                 │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Constitución  ──►  Definir principios del proyecto       │
│         │                                                    │
│         ▼                                                    │
│  2. Especificar  ────►  Q&A interactivo para clarificar      │
│         │             requisitos (sin crear archivo)         │
│         │                                                    │
│         ▼                                                    │
│  3. Generar Spec  ───►  Crear documento spec.md              │
│         │             (usuario llama explícitamente)         │
│         │                                                    │
│         ▼                                                    │
│  4. Revisar Spec  ───►  Validar especificación               │
│         │                                                    │
│         ▼                                                    │
│  5. Clarificar  ─────►  Resolver ambigüedades (opcional)     │
│         │                                                    │
│         ▼                                                    │
│  6. Spec a Plan  ────►  Crear plan técnico                   │
│         │                                                    │
│         ▼                                                    │
│  7. Revisar Plan  ───►  Validar plan técnico                 │
│         │                                                    │
│         ▼                                                    │
│  8. Plan a Tareas  ──►  Generar desglose de tareas           │
│         │                                                    │
│         ▼                                                    │
│  9. Analizar  ───────►  Consistencia entre artefactos (opcional)│
│         │                                                    │
│         ▼                                                    │
│  10. Revisar Tareas ─►  Validar desglose de tareas           │
│         │                                                    │
│         ▼                                                    │
│  11. Implementar  ────►  Ejecutar implementación             │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Concepto Clave: Flujo de Trabajo de Clarificación de Requisitos

CodexSpec proporciona **dos comandos de clarificación distintos** para diferentes etapas del flujo de trabajo:

#### specify vs clarify: ¿Cuál usar cuándo?

| Aspecto | `/codexspec.specify` | `/codexspec.clarify` |
|---------|----------------------|----------------------|
| **Propósito** | Exploración inicial de requisitos | Refinamiento iterativo de specs existentes |
| **Cuándo usar** | Empezar con idea nueva, sin spec.md | spec.md existe, necesita llenar brechas |
| **Entrada** | Tu idea o requisito inicial | Archivo spec.md existente |
| **Salida** | Ninguna (solo diálogo) | Actualiza spec.md con clarificaciones |
| **Método** | Q&A abierto | Escaneo de ambigüedad estructurado (6 categorías) |
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
                └── Escanea ambigüedades en 6 categorías:
                    • Alcance funcional y comportamiento
                    • Dominio y modelo de datos
                    • Interacción y flujo UX
                    • Atributos de calidad no funcionales
                    • Casos límite y manejo de fallos
                    • Resolución de conflictos
```

#### Beneficios de este Diseño

- **Colaboración humano-AI**: Participas activamente en el descubrimiento de requisitos
- **Control explícito**: Los archivos solo se crean cuando tú decides
- **Enfoque en calidad**: Los requisitos se exploran completamente antes de documentar
- **Refinamiento iterativo**: Las specs pueden mejorarse incrementalmente

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

CodexSpec soporta múltiples idiomas a través de **traducción dinámica LLM**. En lugar de mantener plantillas traducidas, dejamos que Claude traduzca el contenido en tiempo real basándose en tu preferencia de idioma.

### Establecer Idioma

**Durante la inicialización:**
```bash
# Crear un proyecto con salida en español
codexspec init my-project --lang es

# Crear un proyecto con salida en chino
codexspec init my-project --lang zh-CN
```

**Después de la inicialización:**
```bash
# Ver configuración actual
codexspec config

# Cambiar configuración de idioma
codexspec config --set-lang es

# Listar idiomas soportados
codexspec config --list-langs
```

### Idiomas Soportados

| Código | Idioma |
|--------|--------|
| `en` | English (por defecto) |
| `zh-CN` | 中文（简体） |
| `zh-TW` | 中文（繁體） |
| `ja` | 日本語 |
| `ko` | 한국어 |
| `es` | Español |
| `fr` | Français |
| `de` | Deutsch |
| `pt` | Português |
| `ru` | Русский |
| `it` | Italiano |
| `ar` | العربية |
| `hi` | हिन्दी |

### Archivo de Configuración

El archivo `.codexspec/config.yml` almacena la configuración de idioma:

```yaml
version: "1.0"

language:
  # Idioma de salida para interacciones con Claude y documentos generados
  output: "es"

  # Idioma de plantillas - mantener como "en" para compatibilidad
  templates: "en"

project:
  ai: "claude"
  created: "2026-02-15"
```

### Cómo Funciona

1. **Plantillas en Inglés Únicamente**: Todas las plantillas de comandos permanecen en inglés
2. **Configuración de Idioma**: El proyecto especifica el idioma de salida preferido
3. **Traducción Dinámica**: Claude lee las instrucciones en inglés y genera salida en el idioma objetivo
4. **Consciente del Contexto**: Los términos técnicos (JWT, OAuth, etc.) permanecen en inglés cuando es apropiado

### Beneficios

- **Cero Mantenimiento de Traducción**: No es necesario mantener múltiples versiones de plantillas
- **Siempre Actualizado**: Las actualizaciones de plantillas benefician automáticamente a todos los idiomas
- **Traducción Consciente del Contexto**: Claude proporciona traducciones naturales y apropiadas para el contexto
- **Idiomas Ilimitados**: Cualquier idioma soportado por Claude funciona inmediatamente

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
| Filosofía Central | Desarrollo guiado por especificaciones | Desarrollo guiado por especificaciones |
| Nombre del CLI | `specify` | `codexspec` |
| IA Principal | Soporte multi-agente | Enfocado en Claude Code |
| Prefijo de Comandos | `/speckit.*` | `/codexspec.*` |
| Flujo de Trabajo | especificar → planificar → tareas → implementar | constitución → especificar → generar-spec → planificar → tareas → analizar → implementar |
| Especificación en Dos Fases | No | Sí (clarificación + generación) |
| Pasos de Revisión | Opcional | Comandos de revisión integrados |
| Comando Clarify | Sí | Sí |
| Comando Analyze | Sí | Sí |
| Comando Checklist | Sí | Sí |
| Sistema de Extensiones | Sí | Sí |
| Scripts PowerShell | Sí | Sí |
| Soporte i18n | No | Sí (13+ idiomas vía traducción LLM) |

## Filosofía

CodexSpec sigue estos principios fundamentales:

1. **Desarrollo guiado por intenciones**: Las especificaciones definen el "qué" antes del "cómo"
2. **Creación rica de especificaciones**: Usar barreras y principios organizacionales
3. **Refinamiento en múltiples pasos**: En lugar de generación de código de un solo shot
4. **Alta dependencia de IA**: Aprovechar IA para interpretación de especificaciones
5. **Orientado a revisión**: Validar cada artefacto antes de avanzar
6. **Calidad primero**: Checklists y análisis integrados para calidad de requisitos

## Contribuir

¡Las contribuciones son bienvenidas! Por favor lee nuestras guías de contribución antes de enviar un pull request.

## Licencia

Licencia MIT - ver [LICENSE](LICENSE) para detalles.

## Agradecimientos

- Inspirado por [GitHub spec-kit](https://github.com/github/spec-kit)
- Construido para [Claude Code](https://claude.ai/code)

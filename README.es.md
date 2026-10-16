<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="codexspec-logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="codexspec-logo-light.svg">
    <img alt="CodexSpec Logo" src="codexspec-logo-light.svg" width="420">
  </picture>
</div>

<h1 align="center">CodexSpec</h1>

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh-CN.md">中文</a> | <a href="README.ja.md">日本語</a> | <b>Español</b> | <a href="README.pt-BR.md">Português</a> | <a href="README.ko.md">한국어</a> | <a href="README.de.md">Deutsch</a> | <a href="README.fr.md">Français</a>
</p>

<p align="center">
  <a href="https://pypi.org/project/codexspec/"><img src="https://img.shields.io/pypi/v/codexspec.svg?style=for-the-badge" alt="PyPI version"></a>
  <a href="https://pypi.org/project/codexspec/"><img src="https://img.shields.io/pypi/pyversions/codexspec.svg?style=for-the-badge" alt="Python versions"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License: MIT"></a>
</p>

<p align="center">
  <strong>Herramientas SDD con prioridad en los requisitos para Claude Code y OpenAI Codex</strong>
</p>

CodexSpec transforma los requisitos confirmados en especificaciones, diseños,
planes, tareas e implementaciones con trazabilidad. Tú decides **qué** construir
y **por qué**; el agente se encarga de definir **cómo** hacerlo, siempre dentro
de los requisitos que hayas confirmado y con el apoyo de revisiones y del
conocimiento que el proyecto conserva entre sesiones.

Puedes usar los comandos con barra de Claude Code, las habilidades de Codex o
ambas integraciones. De forma predeterminada, las funcionalidades del flujo
estándar se desarrollan en worktrees de Git separados. También puedes utilizar
un blueprint compartido para que el agente desarrolle de forma autónoma una
cola de requisitos confirmados.

[📖 Documentación](https://zts0hg.github.io/codexspec/) | [中文文档](https://zts0hg.github.io/codexspec/zh/) | [日本語ドキュメント](https://zts0hg.github.io/codexspec/ja/) | [한국어 문서](https://zts0hg.github.io/codexspec/ko/) | [Documentación](https://zts0hg.github.io/codexspec/es/) | [Documentation](https://zts0hg.github.io/codexspec/fr/) | [Dokumentation](https://zts0hg.github.io/codexspec/de/) | [Documentação](https://zts0hg.github.io/codexspec/pt-BR/)

## Índice

- [¿Por qué elegir CodexSpec?](#por-qué-elegir-codexspec)
- [Inicio rápido en 30 segundos](#inicio-rápido-en-30-segundos)
- [Instalación](#instalación)
- [Flujo de trabajo principal](#flujo-de-trabajo-principal)
- [Blueprint compartido y desarrollo autónomo](#blueprint-compartido-y-desarrollo-autónomo)
- [Desarrollo con worktrees](#desarrollo-con-worktrees)
- [Trabajar con código existente](#trabajar-con-código-existente)
- [Revisión y depuración](#revisión-y-depuración)
- [Conocimiento del proyecto](#conocimiento-del-proyecto)
- [Flujo de trabajo con Git](#flujo-de-trabajo-con-git)
- [Comandos disponibles](#comandos-disponibles)
- [Configuración e internacionalización](#configuración-e-internacionalización)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Materiales para extensiones](#materiales-para-extensiones)
- [Desarrollo](#desarrollo)
- [Contribuir](#contribuir)
- [Licencia](#licencia)

## ¿Por qué elegir CodexSpec?

| Necesidad | Qué ofrece CodexSpec |
|------|-------------------------|
| Definir con claridad la intención del producto | Confirmación explícita y registro persistente en `requirements.md` antes de elaborar la especificación |
| Mantener la trazabilidad del desarrollo | Referencias a las fuentes en toda la cadena: requisitos → especificación → diseño → plan → tareas |
| Poder revisar las decisiones | Cuatro comandos de revisión de artefactos, análisis entre artefactos y una puerta de defectos independiente para el código |
| Dar continuidad al trabajo entre sesiones y equipos | Registros de funcionalidades, principios del proyecto, conocimiento reutilizable y decisiones históricas pertinentes |
| Trabajar en varias funcionalidades a la vez | Un worktree de Git por funcionalidad del flujo estándar, reutilizando siempre el mismo espacio de trabajo |
| Automatizar más tareas | Avance opcional entre etapas y desarrollo autónomo de los requisitos confirmados del blueprint |
| Respetar los idiomas de trabajo del equipo | Idiomas independientes para la interacción, los documentos y los commits |

### ¿En qué consiste SDD con prioridad en los requisitos?

En el desarrollo guiado por especificaciones con prioridad en los requisitos,
**los requisitos confirmados tienen la máxima autoridad sobre la funcionalidad**.
Antes de elaborar los artefactos de implementación, el agente registra los
objetivos, las restricciones, las decisiones, las exclusiones, las preguntas
pendientes y las pruebas de que los requisitos se han confirmado.

```text
Idea → Confirmed Requirements →     Spec    →     Design    →     Plan    →    Tasks     →     Code
                 ↓                   ↓              ↓              ↓             ↓              ↓
         User confirmation      review-spec   review-design   review-plan   review-tasks   review-code
```

Tú confirmas los requisitos; cada artefacto derivado tiene su propia revisión,
desde la especificación hasta el código.

La intención del producto se define y se modifica mediante la colaboración
humana. Las revisiones automáticas comprueban que los artefactos derivados
respeten esa intención. Al activar la automatización, el trabajo avanza por las
etapas que superan la revisión; el agente no puede sustituir los requisitos
confirmados sin avisar.

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
en [Flujo de trabajo principal](#flujo-de-trabajo-principal).

¿Usas la aplicación de escritorio de Codex? [Pide a Codex que instale e inicialice tu proyecto](#instalar-desde-la-aplicación-de-escritorio-de-codex).

## Instalación

### Instalar desde la aplicación de escritorio de Codex

Desde la aplicación de escritorio puedes pedir a Codex que instale CodexSpec y configure tu proyecto directamente.

1. Añade un proyecto local en la aplicación de escritorio de Codex y selecciona la carpeta en la que quieras trabajar.
2. Abre un chat en ese proyecto y pega la instrucción que aparece a continuación.
3. Si la aplicación te pide permiso para descargar o instalar dependencias, aprueba la acción solicitada para continuar.

```text
Please install and initialize CodexSpec in the current project.
Project: https://github.com/Zts0hg/codexspec

Complete the setup directly instead of asking me to run terminal commands.

Check the environment. If uv or Python 3.11+ is missing, install the required
tools in my user directory using their official installation instructions.
Install the latest stable release of CodexSpec.

For a new setup, initialize the current project for Codex in English:
codexspec init . --ai codex --lang en

If CodexSpec is already configured, check its version and configuration before
updating. Preserve existing requirements, project principles, user files,
and configuration settings.

Verify that the CLI works and that AGENTS.md and the CodexSpec skill files
under .agents/skills/ are installed. Explain the result and how to start
describing my requirements in plain English. If the skills are not yet
available in this chat, tell me whether to start a new chat or restart the app.
```

Para recibir respuestas y documentos en chino, cambia `--lang en` por `--lang zh-CN` y pide a Codex que explique el resultado en chino.

Codex instala la misma CLI y las mismas habilidades del proyecto que se obtienen con la configuración manual descrita a continuación. Puedes empezar con una instrucción como `$codexspec:specify I want to build a todo application`. La [guía de habilidades de OpenAI](https://learn.chatgpt.com/docs/build-skills) explica cómo se detectan y actualizan las habilidades locales.

### Requisitos previos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recomendado) o pip
- El asistente que vayas a utilizar: Claude Code o Codex
- Git para desarrollar con worktrees y trabajar con Git

### Instalación de la CLI

```bash
uv tool install codexspec

# Or use pip
pip install codexspec

# Verify the CLI and inspect available commands
codexspec version
codexspec --help
codexspec list-commands
```

Para crear un proyecto, ejecuta `codexspec init my-project --ai claude`; para
inicializar el directorio actual, ejecuta `codexspec init . --ai codex`. Con
`--ai both` se instalan ambas integraciones. El asistente predeterminado es
`claude`: si quieres Codex o ambos, debes indicarlo explícitamente.

<details>
<summary>Otros métodos de instalación</summary>

#### Inicialización puntual

```bash
uvx codexspec init my-project --ai claude
uvx codexspec init . --ai codex
```

La inicialización puntual instala los comandos del proyecto y el entorno de
ejecución independiente para commits. El enrutamiento de worktrees, los flujos
blueprint/auto-dev y la revisión manual del perfil siguen utilizando la CLI de
CodexSpec; asegúrate de que esté disponible si vas a utilizar esos flujos.

#### Versiones de desarrollo

```bash
uv tool install git+https://github.com/Zts0hg/codexspec.git
uv tool install git+https://github.com/Zts0hg/codexspec.git@main

# Replace <tag> with the version you want
uv tool install git+https://github.com/Zts0hg/codexspec.git@<tag>
```

</details>

<details>
<summary>Instalación en Windows</summary>

Utiliza PowerShell:

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
# Restart PowerShell, then:
uv tool install codexspec
codexspec version
```

La [Guía de resolución de problemas en Windows](docs/en/WINDOWS-TROUBLESHOOTING.md)
explica cómo resolver problemas de PATH y de instalación.

</details>

### Actualizar CodexSpec y los archivos del proyecto

La actualización de la CLI y la de los comandos instalados en un proyecto se hacen por separado:

```bash
uv tool install codexspec --upgrade
# Or: pip install --upgrade codexspec

# In the project you want to refresh; select its desired integration(s)
codexspec init . --force --ai both
```

Utiliza `--ai claude` o `--ai codex` si solo necesitas una de las integraciones.
`--force` regenera los comandos y scripts distribuidos y actualiza los recursos
de revisión. También confirma automáticamente las solicitudes de migración,
actualización de comandos y cumplimiento de la constitución. Se conservan los
requisitos y los principios del proyecto. En los archivos de contexto se
actualizan las instrucciones gestionadas, pero se mantiene el cuerpo existente;
también se conservan las claves de configuración que no hayas establecido
explícitamente.

El comando de planificación es `design-to-plan`. Al actualizar la instalación
se elimina la antigua entrada `spec-to-plan`, sin conservarla como alias.

### Instalación desde el marketplace de plugins

En Claude Code, instala el plugin desde su marketplace:

```text
/plugin marketplace add Zts0hg/codexspec
/plugin install codexspec@codexspec-market
/codexspec:config
```

El plugin incluye comandos e instrucciones que se cargan al inicio de la
sesión, también al reanudarla, para analizar los cambios preparados para commit
y consultar los requisitos históricos. Instalar el plugin no inicializa el
proyecto. Utiliza `/codexspec:config` para crear o modificar los ajustes de
idioma, flujo de trabajo y revisión; si necesitas la estructura completa del
proyecto, inicialízalo mediante la CLI.

El entorno de ejecución incluido permite previsualizar commits directamente
y realizar commits autorizados en el directorio actual con Python 3.11+ y Git,
sin mantener instalada la CLI de CodexSpec. El enrutamiento de worktrees, los
flujos blueprint/auto-dev y la revisión manual del perfil siguen requiriendo
la CLI. El hook de inicio del plugin necesita Git en PATH y una versión de
Claude Code que admita `args` en los hooks de comandos (forma exec). Sus
instrucciones están dirigidas al agente; no intercepta los comandos Git que
se ejecutan manualmente.

Consulta [Instalación](docs/en/getting-started/installation.md) para conocer el procedimiento completo.

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

### specify, clarify y analyze

- **specify** inicia o retoma la definición de requisitos. El resumen solo adquiere carácter vinculante cuando se confirma explícitamente.
- **clarify** resuelve las ambigüedades de los requisitos o de la especificación existentes: plantea hasta cinco preguntas por ejecución, repartidas entre cuatro categorías. Primero actualiza `requirements.md` y después sincroniza `spec.md`.
- **analyze** revisa la cadena completa: requisitos → especificación → diseño → plan → tareas. Aplica automáticamente correcciones deterministas a los artefactos derivados cuando se deducen de las fuentes que los rigen; nunca modifica `requirements.md`. Informa de los hallazgos pendientes. Se ejecuta automáticamente después de que la revisión de tareas se apruebe y tiene carácter informativo, sin bloquear la implementación.

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

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

La [guía del flujo de trabajo](docs/en/user-guide/workflow.md) detalla las reglas de cada etapa.

## Blueprint compartido y desarrollo autónomo

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

## Desarrollo con worktrees

Un worktree de Git es otro directorio de trabajo del mismo repositorio, con su
propia rama activa. CodexSpec utiliza uno por funcionalidad del flujo estándar
de forma predeterminada. Lo crea antes de escribir el primer requisito y
mantiene juntos los documentos, la implementación, las pruebas y las
correcciones de esa funcionalidad.

```text
projects/
├── my-project/
└── my-project-codexspec-worktrees/
    ├── <feature-id>-task-reminders/
    ├── <feature-id>-search/
    ├── worktree-for-codexspec-maintenance/
    └── worktree-for-codexspec-auto-dev/
```

Al retomar una funcionalidad se reutiliza su espacio de trabajo. Los cambios
independientes de configuración, constitución o perfil se realizan en el
worktree de mantenimiento; los cambios de una funcionalidad activa permanecen
en su worktree. La configuración es **local a cada checkout**: un ajuste
modificado en el worktree al que se dirige la operación surte efecto primero
allí y llega a los demás checkouts mediante la integración de Git. Ejecuta
los comandos de la CLI y las comprobaciones en el espacio de trabajo indicado.

Para establecer la base de una nueva funcionalidad, se comparan los historiales
de commits de la rama principal local y de la rama principal remota obtenida
mediante fetch, según su relación de ascendencia en Git. Si los historiales han
divergido, se fusionan en el nuevo worktree y la fusión debe verificarse. Si
falla fetch, se emite una advertencia y se permite utilizar las referencias
disponibles localmente. Un fallo de creación no permite pasar a escribir en
el checkout principal.

El valor predeterminado de `workflow.worktrees` es **true**. Solo el valor YAML
literal `false` desactiva el aislamiento de las funcionalidades del flujo
estándar y del mantenimiento. Blueprint/auto-dev conservan siempre su worktree
compartido fijo. La inicialización y las actualizaciones de instalación operan
en el checkout que selecciones explícitamente. Los worktrees de funcionalidades
completadas se conservan; la finalización no los fusiona ni los elimina
automáticamente.

Consulta [Desarrollo con worktrees](docs/en/user-guide/workflow.md#worktree-development)
y [configuración](docs/en/reference/configuration.md#workflowworktrees).

## Trabajar con código existente

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

## Revisión y depuración

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

La [referencia de comandos](docs/en/user-guide/commands.md) detalla los
selectores de revisión, los argumentos y los procedimientos.

## Conocimiento del proyecto

El perfil del proyecto guarda conocimiento reutilizable en `.codexspec/profile/`:

| Categoría | Contenido |
|----------|----------|
| `constraints/` | Prohibiciones explícitas y límites estrictos; deben leerse primero |
| `conventions/` | Patrones, nombres y orientaciones aplicables a varias funcionalidades |
| `pitfalls/` | Problemas experimentados, sus causas, soluciones alternativas y lecciones |
| `decisions/` | Decisiones de arquitectura y otras decisiones reutilizables entre funcionalidades |
| `strategies/` | Señales que indican la necesidad de cambiar el enfoque de trabajo |
| `runbooks/` | Procedimientos ordenados y recuperación ante fallos |

`distill` recoge conocimiento reutilizable del trabajo realizado. La intención
específica de cada funcionalidad permanece en sus requisitos, diseño y plan.
La inicialización instala instrucciones en CLAUDE.md y/o AGENTS.md para leer
todas las restricciones y el conocimiento pertinente antes de realizar trabajo
sustantivo. El conocimiento que se añada después puede aplicarse sin volver
a inicializar el proyecto. Los registros candidatos se utilizan con cautela;
los registros validados requieren resultados verificados y respaldo humano.

```text
/codexspec:distill Capture the reusable lessons from this work
/codexspec:distill review
/codexspec:evolve
```

Al ejecutar manualmente `distill review`, o invocar directamente `distill` sin
material nuevo que recoger, se abre un espacio de trabajo local en el navegador
que funciona sin conexión. Puedes revisar, validar, descartar, aplazar y
consolidar registros, previsualizar el Markdown final y seleccionar **Aplicar todo**. Las decisiones se guardan en un borrador recuperable hasta que se aplican.
Las comprobaciones de conflictos evitan que se apliquen parcialmente o que se
sobrescriba contenido sin avisar. También hay una alternativa explícita en modo
texto para entornos sin navegador.

El valor predeterminado de `workflow.auto_distill` es **true**. Controla tres
hooks de cierre: la finalización correcta de `implement-tasks`, los commits
ejecutados mediante `commit-staged` y la generación de `pr`. La vista previa
de un commit no activa la captura.

Las instrucciones instaladas en el proyecto también piden al agente que recoja
el conocimiento reutilizable cuando surja en conversaciones habituales, en
correcciones fuera de SDD y en ejecuciones largas de `implement-tasks`. Estas
instrucciones se aplican independientemente del ajuste de cierre; la captura
al final de la tarea ofrece una última oportunidad de conservar ese conocimiento.

Dentro de una sesión, las activaciones repetidas solo procesan material nuevo.
Entre sesiones, `distill` lee el perfil y omite el conocimiento que ya contiene.
Si no queda nada reutilizable, termina sin escribir. La captura automática nunca abre la revisión manual, no espera a una persona
ni bloquea el flujo de trabajo que la invoca.

`evolve` selecciona únicamente conocimiento validado que sea útil fuera del
proyecto, elabora un borrador de comando o habilidad y obtiene aprobación
explícita antes de hacer push o abrir una PR de contribución para revisión humana.

Consulta [Conocimiento del proyecto](docs/en/user-guide/commands.md#codexspecdistill)
para obtener instrucciones detalladas.

### Reutilizar decisiones históricas

Antes de preguntarte por un cambio, el agente consulta el historial de las
funcionalidades relacionadas en `.codexspec/specs/`. Lee las decisiones
confirmadas en `requirements.md`, sigue las incorporaciones posteriores y las
sustituciones explícitas y, cuando hace falta, consulta las razones del diseño
o las pruebas de lo que está implementado. Esta preparación también precede
a los juicios sustantivos sobre diseño, implementación, depuración o revisión,
tanto en conversaciones habituales como en flujos SDD.

Las marcas de tiempo de los directorios de funcionalidades ayudan a reconstruir
el orden de las iteraciones; un documento más reciente no invalida por sí solo
una decisión anterior. Los requisitos anteriores que no se hayan modificado
siguen siendo aplicables, y las propuestas pendientes no cuentan como intención
confirmada. La búsqueda se centra en la tarea actual y termina cuando hay
suficiente contexto, que se reutiliza en las etapas posteriores.

Por ejemplo, al modificar una interfaz, un agente que no haya consultado el
historial podría preguntar:

> «¿Cómo debería gestionar esta funcionalidad la compatibilidad con versiones anteriores?»

Tras comprobar las decisiones pertinentes y la implementación actual, puede
plantear una pregunta más concreta:

> «Antes confirmaste que debía conservarse la interfaz antigua, y la implementación
> actual sigue admitiéndola. Propongo mantener ese comportamiento en este cambio.
> ¿Lo mantenemos?»

La información ya establecida que siga siendo claramente aplicable puede
reutilizarse sin volver a preguntar. Si ya has dicho «Elimina la interfaz antigua
en este cambio», el agente sigue esa decisión y explica las repercusiones de
la migración. **Tu última decisión explícita siempre tiene prioridad**; el
historial sirve para preparar preguntas más precisas y evitar las repetidas.

Actualiza las instalaciones de los proyectos existentes para recibir estas
instrucciones.

## Flujo de trabajo con Git

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

## Comandos disponibles

La CLI tiene seis comandos públicos. Las integraciones de agentes distribuyen
28 comandos: Claude utiliza `/codexspec:<name>` y Codex, `$codexspec:<name>`.
Las tablas siguientes muestran la sintaxis de Claude para facilitar la lectura.

### Comandos CLI

| Comando | Propósito |
|---------|---------|
| `codexspec init` | Inicializar o actualizar un proyecto para Claude, Codex o ambos |
| `codexspec check` | Comprobar las herramientas y dependencias instaladas |
| `codexspec version` | Mostrar la versión e información del sistema |
| `codexspec config` | Consultar o modificar la configuración del proyecto |
| `codexspec list-commands` | Mostrar los comandos de agente disponibles por categoría |
| `codexspec show-blueprint` | Mostrar el blueprint del worktree compartido sin modificarlo |

### Comandos del flujo de trabajo principal

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

### Comandos de revisión de artefactos

| Comando | Propósito |
|---------|---------|
| `/codexspec:review-spec` | Revisar la fidelidad y la calidad interna de la especificación |
| `/codexspec:review-design` | Revisar la fidelidad y la viabilidad del diseño, y comprobar si está listo para planificar |
| `/codexspec:review-plan` | Revisar la fidelidad y la viabilidad del plan, y comprobar si está listo para implementar |
| `/codexspec:review-tasks` | Revisar la fidelidad, las dependencias, la ejecutabilidad y la verificación de las tareas |

### Requisitos, código existente y depuración

| Comando | Propósito |
|---------|---------|
| `/codexspec:clarify` | Resolver ambigüedades en los requisitos, actualizándolos antes que la especificación |
| `/codexspec:analyze` | Comprobar la trazabilidad de principio a fin y ajustar los artefactos derivados a las fuentes que los rigen |
| `/codexspec:checklist` | Generar una lista de comprobación de la calidad de los requisitos |
| `/codexspec:tasks-to-issues` | Convertir las tareas existentes en issues de GitHub con acciones concretas |
| `/codexspec:debug` | Investigar la causa raíz antes de aplicar una corrección |
| `/codexspec:reverse-spec` | Examinar la arquitectura existente, elaborar borradores de artefactos de módulos o informar de desviaciones respecto a la base confirmada |

### Comandos de conocimiento del proyecto

| Comando | Propósito |
|---------|---------|
| `/codexspec:distill` | Recoger conocimiento reutilizable o revisar candidatos en el espacio de trabajo local |
| `/codexspec:evolve` | Elaborar un borrador de contribución al proyecto de origen a partir de conocimiento validado |
| `/codexspec:onboard` | Obtener convenciones candidatas y restricciones respaldadas por evidencia a partir del código existente |

### Comandos de Git y revisión de código

| Comando | Propósito |
|---------|---------|
| `/codexspec:commit-staged` | Generar mensajes a partir de los cambios preparados; previsualizar o ejecutar un commit autorizado |
| `/codexspec:pr` | Generar una descripción estructurada de PR/MR |
| `/codexspec:release-notes` | Mantener una entrada del registro de cambios y obtener el texto de una publicación del historial de Git |
| `/codexspec:review-code` | Revisar los cambios seleccionados como puerta de defectos; utilizar `--audit` para evaluar la calidad en las rutas indicadas |

### Comandos de utilidad

| Comando | Propósito |
|---------|---------|
| `/codexspec:config` | Crear, consultar, modificar o restablecer la configuración del proyecto de forma interactiva |
| `/codexspec:quick` | Ejecutar un flujo SDD breve con prioridad en los requisitos para cambios pequeños |

## Configuración e internacionalización

La configuración se guarda en `.codexspec/config.yml`. Las plantillas permanecen
en inglés; el agente redacta las conversaciones y los artefactos generados en
los idiomas configurados. Los 13 códigos de idioma estándar son `en`, `zh-CN`,
`zh-TW`, `ja`, `ko`, `es`, `fr`, `de`, `pt`, `ru`, `it`, `ar` y `hi`.
Para portugués, la CLI utiliza `pt`; la documentación localizada y los catálogos
de traducción utilizan `pt-BR`.

### Idiomas de interacción, documentos y commits

| Dimensión | Clave de configuración | Al inicializar | Cambiar después | Qué controla |
|-----------|------------|-------------------|-----------|----------|
| Salida/base | `language.output` | `--lang` | `config --set-lang` | Idioma de respaldo para las demás dimensiones |
| Interacción | `language.interaction` | `--interaction-lang` | `config --set-interaction-lang` | Conversación y salida de la CLI |
| Documentos | `language.document` | `--document-lang` | `config --set-document-lang` | Requisitos, especificaciones, diseños, planes y tareas |
| Commits | `language.commit` | `--commit-lang` | `config --set-commit-lang` | Mensajes de commit y textos generados en los flujos de trabajo con Git |

Si no se define el idioma de una dimensión, se utiliza `language.output` y,
en su defecto, `en`. Esta regla se aplica de forma independiente a cada
dimensión. `language.templates` permanece en `en`.

```bash
codexspec init my-project --ai both \
  --interaction-lang zh-CN --document-lang en --commit-lang en

codexspec config
codexspec config --set-document-lang en
codexspec config --list-langs
```

En la primera inicialización desde una terminal TTY se pide el idioma base,
a menos que indiques `--lang` o las tres opciones de idioma específicas.
`--force` confirma automáticamente las demás solicitudes de inicialización,
pero no omite esta selección. Sin TTY, se utiliza el inglés de forma
predeterminada. Al volver a inicializar, se conservan las claves de idioma
que no hayas establecido explícitamente.

### Ajustes del flujo de trabajo y la revisión

| Ajuste | Valor predeterminado | Efecto | Control CLI |
|---------|---------|--------|-------------|
| `workflow.auto_next` | `false` | Avanzar por las etapas aprobadas del flujo SDD estándar | `config --auto-next on\|off` |
| `workflow.auto_distill` | `true` | Recoger conocimiento sin interacción al terminar correctamente el trabajo | `config --auto-distill on\|off` |
| `workflow.auto_maintenance` | `true` | Aplicar mantenimiento incremental verificado durante las correcciones automáticas | `config --auto-maintenance on\|off` |
| `workflow.worktrees` | `true` | Aislar las funcionalidades del flujo estándar y el mantenimiento independiente | `config --worktrees on\|off` |
| `review.decided_by` | `reviewer` | Decidir quién resuelve los hallazgos cuya condición se da fuera del contexto operativo del proyecto | `config --decided-by reviewer\|ask` |

Las opciones booleanas de la CLI aceptan `on/true/1/yes` y `off/false/0/no`,
sin distinguir mayúsculas y minúsculas y admitiendo espacios alrededor del
valor. Una opción booleana sin valor invierte el valor actual del checkout de
destino; en YAML, los valores se guardan como booleanos.

Con `review.decided_by: reviewer`, el revisor decide qué hallazgos se admiten
como defectos. Con `ask`, si la condición que origina un hallazgo se da fuera
del contexto del proyecto, queda pendiente una decisión sobre ese escenario.
El usuario decide una vez si se corrige el problema o se excluye el escenario,
y su decisión confirmada se conserva para las rondas posteriores. Las decisiones
pendientes bloquean la finalización. En una ejecución concreta de `review-code`
puedes cambiar el modo configurado con `--decided-by`.

Las modificaciones de configuración siguen el enrutamiento de worktrees. Un
cambio independiente solicitado desde el checkout principal se realiza en el
worktree de mantenimiento y no altera de inmediato el ajuste efectivo del
principal. Los cambios realizados en el worktree de una funcionalidad surten
efecto allí.

<details>
<summary>Opciones de inicialización de la CLI</summary>

| Opción | Significado |
|--------|---------|
| `PROJECT_NAME` | Nombre del nuevo directorio; utiliza `.` para el directorio actual |
| `--here`, `-h` | Inicializar el directorio actual |
| `--ai`, `-a` | `claude`, `codex` o `both`; valor predeterminado: `claude` |
| `--lang`, `-l` | Establecer el idioma base de salida |
| `--interaction-lang` | Establecer el idioma de interacción |
| `--document-lang` | Establecer el idioma de los documentos |
| `--commit-lang` | Establecer el idioma de los mensajes de commit |
| `--force`, `-f` | Regenerar los artefactos instalados y confirmar automáticamente las solicitudes de migración, actualización y cumplimiento; conservar el contexto creado para el proyecto y la configuración no relacionada |
| `--no-git` | Omitir la inicialización del repositorio de Git |
| `--debug`, `-d` | Mostrar información detallada de depuración |

</details>

<details>
<summary>Opciones de configuración de la CLI</summary>

| Opción | Significado |
|--------|---------|
| `--set-lang`, `-l` | Establecer el idioma base de salida |
| `--set-interaction-lang` | Establecer el idioma de interacción |
| `--set-document-lang` | Establecer el idioma de los documentos |
| `--set-commit-lang`, `-c` | Establecer el idioma de los mensajes de commit |
| `--list-langs` | Mostrar los códigos de idioma admitidos |
| `--auto-next` | Alternar o establecer el avance automático entre etapas |
| `--auto-distill` | Alternar o establecer la captura automática de conocimiento |
| `--auto-maintenance` | Alternar o establecer el mantenimiento incremental automático |
| `--worktrees` | Alternar o establecer el aislamiento por worktrees local a cada checkout |
| `--decided-by` | Establecer el modo de decisión de revisión en `reviewer` o `ask` |

</details>

<details>
<summary>Ejemplo de configuración</summary>

```yaml
version: "1.0"

language:
  output: "en"
  interaction: "zh-CN"
  document: "en"
  commit: "en"
  templates: "en"

project:
  ai: "both"

workflow:
  auto_next: false
  auto_distill: true
  auto_maintenance: true
  worktrees: true

review:
  decided_by: reviewer
```

</details>

Consulta [Configuración](docs/en/reference/configuration.md) e
[Internacionalización](docs/en/user-guide/i18n.md) para conocer en detalle
el funcionamiento de los idiomas y los ajustes.

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

## Materiales para extensiones

El repositorio incluye una plantilla de manifiesto de extensión, un comando de
ejemplo y una [Guía de desarrollo de extensiones](extensions/EXTENSION-DEVELOPMENT-GUIDE.md).
Estos materiales sirven para crear extensiones. La CLI actual no ofrece
comandos para instalar, listar o eliminar extensiones, ni carga automáticamente
los comandos o hooks de `extension.yml`. Los recursos de revisión compartidos
admiten adiciones propias del proyecto en `.codexspec/review-code/`. La
inicialización conserva los recursos modificados y los archivos adicionales,
a menos que se solicite su sustitución.

## Desarrollo

```bash
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Development tools are an optional dependency extra
uv sync --extra dev
# For documentation builds too: uv sync --extra dev --extra docs

uv run codexspec --help
uv run pytest
uv run ruff check src/
uv build
```

Antes de modificar las plantillas, el empaquetado o la inicialización, lee
[CLAUDE.md](CLAUDE.md), [AGENTS.md](AGENTS.md) y
[Distribución del repositorio](docs/internal/repository-layout.md). Las copias
distribuidas de los comandos y las habilidades son artefactos de instalación
generados; modifica sus fuentes autorizadas y vuelve a generarlas.

## Contribuir

La [guía para contribuir](docs/en/development/contributing.md) explica cómo
preparar el entorno local y aportar cambios. Las contribuciones deben respetar
los requisitos confirmados, la trazabilidad de las fuentes y el límite de
empaquetado entre usuarios y mantenedores.

## Licencia

MIT — consulta [LICENSE](LICENSE).

## Agradecimientos

Inspirado en [GitHub spec-kit](https://github.com/github/spec-kit).
Se integra con Claude Code y OpenAI Codex.

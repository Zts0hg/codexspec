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
  <strong>Un conjunto de herramientas SDD que prioriza los requisitos para Claude Code y OpenAI Codex</strong>
</p>

CodexSpec convierte los requisitos confirmados en especificaciones, diseños,
planes, tareas e implementaciones trazables. Tú decides **qué** construir y **por qué**;
el agente desarrolla **cómo** hacerlo dentro de esos requisitos confirmados,
con puntos de revisión y conocimiento persistente del proyecto.

Úsalo mediante los comandos con barra de Claude Code, las habilidades de Codex o
ambos. De forma predeterminada, cada funcionalidad ordinaria usa un worktree de Git
independiente; un blueprint compartido opcional permite al agente desarrollar
una cola de requisitos confirmados de forma autónoma.

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
| Intención clara del producto | Confirmación explícita y un `requirements.md` persistente antes de la especificación |
| Desarrollo trazable | Referencias a las fuentes a través de requisitos → especificación → diseño → plan → tareas |
| Decisiones revisables | Cuatro comandos de revisión de artefactos, análisis entre artefactos y una puerta de defectos independiente para el código |
| Continuidad entre sesiones y equipos | Registros de funcionalidades, principios del proyecto, conocimiento reutilizable y decisiones históricas pertinentes |
| Varias funcionalidades en curso | Un worktree de Git por funcionalidad ordinaria, con reutilización estable del espacio de trabajo |
| Más automatización | Avance opcional entre etapas y desarrollo autónomo de requisitos confirmados del blueprint |
| Preferencias lingüísticas del equipo | Idiomas independientes para la interacción, los documentos y los commits |

### ¿Qué es SDD que prioriza los requisitos?

El desarrollo guiado por especificaciones que prioriza los requisitos establece
**los requisitos confirmados como la autoridad de mayor prioridad para una funcionalidad**.
El agente registra objetivos, restricciones, decisiones, exclusiones, preguntas
abiertas y evidencia de confirmación antes de derivar los artefactos de implementación.

```text
Idea → Confirmed Requirements → Spec → Design → Plan → Tasks → Code
```

La colaboración humana establece y modifica la intención del producto. Las
revisiones automáticas comprueban los artefactos derivados frente a ella.
Activar la automatización hace avanzar el trabajo por las etapas aprobadas;
no permite al agente sustituir silenciosamente los requisitos confirmados.

## Inicio rápido en 30 segundos

Instala CodexSpec e inicializa el proyecto para el asistente que uses:

```bash
uv tool install codexspec

# Create a new project for Claude Code
codexspec init my-project --ai claude

# Or initialize an existing project for Codex
cd your-existing-project
codexspec init . --ai codex

# Use --ai both when you want both integrations
```

Inicia tu asistente instalado en el proyecto inicializado. El mismo flujo de
trabajo usa estas dos formas de invocación:

| Asistente | Iniciar el descubrimiento de requisitos |
|-----------|------------------------------|
| Claude Code (`claude`) | `/codexspec:specify I want to build a todo application` |
| Codex (`codex`) | `$codexspec:specify I want to build a todo application` |

Personaliza los principios del proyecto con `constitution` cuando sea necesario.
Confirma el resumen final de requisitos y continúa usando el directorio de la
funcionalidad y el espacio de trabajo devueltos. Consulta [Flujo de trabajo principal](#flujo-de-trabajo-principal)
para los comandos restantes.

¿Usas la aplicación de escritorio de Codex? [Pide a Codex que instale e inicialice tu proyecto](#instalar-con-la-aplicación-de-escritorio-de-codex).

## Instalación

### Instalar con la aplicación de escritorio de Codex

Puedes pedir a Codex que instale CodexSpec y configure tu proyecto directamente desde la aplicación de escritorio.

1. Añade un proyecto local en la aplicación de escritorio de Codex y selecciona la carpeta donde quieras trabajar.
2. Inicia un chat en ese proyecto y pega la instrucción siguiente.
3. Si la aplicación solicita permiso para descargar o instalar dependencias, aprueba la acción solicitada para continuar.

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

Para obtener respuestas y documentos en chino, sustituye `--lang en` por `--lang zh-CN` y pide a Codex que explique el resultado en chino.

Codex instala la misma CLI y las mismas habilidades del proyecto que utiliza la configuración manual siguiente. Puedes empezar a usarlas con una instrucción como `$codexspec:specify I want to build a todo application`. Consulta la [guía de habilidades de OpenAI](https://learn.chatgpt.com/docs/build-skills) para conocer cómo se descubren y actualizan las habilidades locales.

### Requisitos previos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recomendado) o pip
- El asistente que quieras usar: Claude Code o Codex
- Git para el desarrollo con worktrees y los flujos de trabajo con Git

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

Inicializa un proyecto nuevo con `codexspec init my-project --ai claude`,
o el directorio actual con `codexspec init . --ai codex`. Usa `--ai both`
para ambas integraciones. La selección del asistente es `claude` de forma
predeterminada; elige el valor explícitamente para Codex o ambos.

<details>
<summary>Métodos alternativos de instalación</summary>

#### Inicialización de una sola ejecución

```bash
uvx codexspec init my-project --ai claude
uvx codexspec init . --ai codex
```

La inicialización de una sola ejecución instala los comandos del proyecto y el
entorno de ejecución autónomo para commits. El enrutamiento de worktrees,
blueprint/auto-dev y la revisión manual del perfil siguen invocando la CLI de
CodexSpec; asegúrate de que esté disponible para esos flujos de trabajo.

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

Usa PowerShell:

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
# Restart PowerShell, then:
uv tool install codexspec
codexspec version
```

Consulta la [Guía de resolución de problemas en Windows](docs/en/WINDOWS-TROUBLESHOOTING.md)
para resolver problemas de PATH y de instalación.

</details>

### Actualizar y regenerar los archivos de un proyecto

Actualizar la CLI y regenerar los comandos instalados de un proyecto son pasos independientes:

```bash
uv tool install codexspec --upgrade
# Or: pip install --upgrade codexspec

# In the project you want to refresh; select its desired integration(s)
codexspec init . --force --ai both
```

Usa `--ai claude` o `--ai codex` cuando solo quieras esa integración.
`--force` regenera los comandos y scripts distribuidos y actualiza los recursos
de revisión; también confirma automáticamente las solicitudes de migración,
actualización de comandos y cumplimiento de la constitución. Se conservan los
requisitos y principios existentes del proyecto, el cuerpo de los archivos de
contexto existentes se mantiene mientras se actualizan las instrucciones
gestionadas, y se conservan las claves de configuración que no hayas establecido explícitamente.

El comando de planificación es `design-to-plan`; las actualizaciones de
instalación retiran la antigua entrada `spec-to-plan` sin dejar un alias.

### Instalación desde el marketplace de plugins

Para Claude Code, instala el plugin desde su marketplace:

```text
/plugin marketplace add Zts0hg/codexspec
/plugin install codexspec@codexspec-market
/codexspec:config
```

El plugin proporciona comandos e instrucciones al inicio de la sesión para el
análisis de commits preparados y la consulta de requisitos históricos, también
en sesiones reanudadas. La instalación del plugin no inicializa un proyecto.
Usa `/codexspec:config` para crear o modificar los ajustes de idioma, flujo de
trabajo y revisión; usa la inicialización mediante CLI cuando necesites la
estructura completa del proyecto.

La vista previa directa de commits y los commits autorizados en el directorio
actual pueden usar el entorno de ejecución incluido con Python 3.11+ y Git,
sin una CLI de CodexSpec instalada de forma persistente. El enrutamiento de
worktrees, blueprint/auto-dev y la revisión manual del perfil mantienen sus
requisitos de CLI. El hook de inicio del plugin requiere Git en PATH y una
versión de Claude Code compatible con `args` en los hooks de comandos (forma exec).
Sus instrucciones se dirigen al agente; no intercepta comandos Git manuales.

Consulta [Instalación](docs/en/getting-started/installation.md) para la configuración detallada.

## Flujo de trabajo principal

El flujo de trabajo estándar de una funcionalidad conserva una cadena de referencias a las fuentes:

```text
/specify          → requirements.md
/generate-spec    → spec.md       → review-spec
/spec-to-design   → design.md     → review-design
/design-to-plan   → plan.md       → review-plan
/plan-to-tasks    → tasks.md      → review-tasks → analyze
/implement-tasks  → implementation and complete-feature code review
```

Los ejemplos siguientes usan el prefijo `/codexspec:` de Claude. En Codex,
usa `$codexspec:` con el mismo nombre de comando y los mismos argumentos.

| Paso | Comando | Propósito y resultado |
|------|---------|--------------------|
| Principios del proyecto | `/codexspec:constitution` | Crear/actualizar `constitution.md` y validar los artefactos afectados |
| Requisitos | `/codexspec:specify <idea>` | Discutir la intención, confirmar un resumen final y guardar `requirements.md` |
| Especificación | `/codexspec:generate-spec <feature-dir>` | Compilar los requisitos confirmados en `spec.md` con referencias a las fuentes |
| Diseño del sistema | `/codexspec:spec-to-design <feature-dir>` | Producir `design.md`: componentes, interfaces y decisiones de diseño clave |
| Plan de implementación | `/codexspec:design-to-plan <feature-dir>` | Producir `plan.md`: fases, orden y verificación |
| Tareas | `/codexspec:plan-to-tasks <feature-dir>` | Producir un `tasks.md` trazable y verificable; ejecutar el análisis entre artefactos |
| Implementación | `/codexspec:implement-tasks <feature-dir>` | Ejecutar tareas, verificar resultados y corregir los hallazgos de revisión verificados de forma independiente |

Sustituye `<feature-dir>` por el directorio de la funcionalidad devuelto durante
el descubrimiento. Continúa en su worktree o pasa su ruta explícita; así se
conserva la identidad de la funcionalidad entre comandos y sesiones.

### specify, clarify y analyze

- **specify** inicia o retoma el descubrimiento de requisitos. Solo la confirmación
  explícita hace vinculante el resumen de requisitos.
- **clarify** resuelve ambigüedades en los requisitos o la especificación existentes:
  hasta cinco preguntas por ejecución, repartidas entre cuatro categorías.
  Actualiza primero `requirements.md` y después sincroniza `spec.md`.
- **analyze** comprueba la cadena completa requisitos → especificación → diseño →
  plan → tareas. Aplica automáticamente correcciones deterministas a los artefactos
  posteriores cuando su corrección se deduce de la autoridad de los anteriores;
  nunca edita `requirements.md`. Informa de los hallazgos sin resolver. Se ejecuta
  automáticamente tras una revisión de tareas aprobada y es informativo, no un
  control que bloquee la implementación.

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

### Cambios pequeños con Quick

Usa `quick` para un cambio pequeño y bien delimitado, como una corrección localizada:

```text
/codexspec:quick Fix the empty-state message on the task list
```

Quick confirma y guarda un resumen compacto de requisitos y después coordina
la especificación, la planificación, las tareas y la implementación con las
revisiones de los comandos de generación. Los cambios amplios o las decisiones
de producto o diseño sin resolver requieren el flujo de trabajo estándar;
Quick se detiene cuando necesita una nueva decisión.

### Automatización del flujo de trabajo

`workflow.auto_next` es **false** de forma predeterminada. Cuando es `true` en
la configuración del espacio de trabajo activo, la confirmación final de los
requisitos da paso a la especificación. Cada etapa de generación avanza tras
`PASS` o `PASS_WITH_WARNINGS`; `NEEDS_REVISION` o `BLOCKED` detiene la cadena.
`implement-tasks` es la etapa final.

La corrección automática de artefactos se limita a defectos verificados cuya
corrección se deduce de la evidencia de los artefactos anteriores, con un máximo
de dos rondas de corrección y revisión. Las recomendaciones se mantienen aparte.
El bucle de revisión y corrección de la implementación tiene sus propias reglas
de finalización, descritas más adelante.

Consulta la [guía del flujo de trabajo](docs/en/user-guide/workflow.md) para los contratos detallados.

## Blueprint compartido y desarrollo autónomo

Usa `blueprint` cuando quieras preparar varios requisitos confirmados antes del
desarrollo, y `auto-dev` para desarrollar esa cola:

```text
/codexspec:blueprint Add a confirmed requirement for task reminders
/codexspec:auto-dev
```

El descubrimiento del blueprint resuelve la dirección, las elecciones y las
restricciones que corresponden al usuario antes de que un requisito entre en la
cola. El archivo compartido `.codexspec/blueprint.md` usa los estados `pending`,
`in_progress` y `completed`. Puedes añadir, sustituir, eliminar o reordenar
requisitos pendientes; las entradas activas y completadas son de solo lectura
para el mantenimiento del blueprint.

Auto-dev sigue el orden del documento, retoma una funcionalidad en curso antes
de empezar otra y vuelve a leer la cola tras cada finalización, de modo que el
trabajo pendiente recién añadido pueda incorporarse a la ejecución. Realiza las
etapas SDD, la implementación, la verificación, la revisión y la corrección dentro
de los requisitos confirmados. Invocar `auto-dev` activa su automatización de
forma independiente de `workflow.auto_next` y no modifica ese ajuste.

Ambos comandos comparten `worktree-for-codexspec-auto-dev` en la rama
`codexspec/auto-dev`. Pueden operar simultáneamente con las protecciones de
propiedad y escritura compartidas; los requisitos se desarrollan secuencialmente
en ese espacio de trabajo. Las decisiones de producto que no puedan resolverse
con los requisitos confirmados detienen la ejecución con evidencia, en lugar de
solicitar respuestas durante la ejecución autónoma normal.

Inspecciona el blueprint compartido actual sin modificarlo:

```bash
codexspec show-blueprint
```

## Desarrollo con worktrees

Un worktree de Git es otro directorio de trabajo para el mismo repositorio, con
su propia rama extraída. CodexSpec usa uno por funcionalidad ordinaria de forma
predeterminada, lo crea antes de escribir el primer requisito y mantiene juntos
los documentos, la implementación, las pruebas y las correcciones de esa funcionalidad.

```text
projects/
├── my-project/
└── my-project-codexspec-worktrees/
    ├── <feature-id>-task-reminders/
    ├── <feature-id>-search/
    ├── worktree-for-codexspec-maintenance/
    └── worktree-for-codexspec-auto-dev/
```

Al continuar una funcionalidad, se reutiliza su espacio de trabajo. Los cambios
independientes de configuración, constitución y perfil usan el worktree de
mantenimiento; los cambios hechos en una funcionalidad activa permanecen allí.
La configuración es **local a cada checkout**: un ajuste modificado en un
worktree al que se ha enrutado la operación surte efecto primero allí y llega a
los demás checkouts mediante la integración de Git. Ejecuta los comandos CLI y
las comprobaciones en el espacio de trabajo devuelto.

Las bases de nuevas funcionalidades comparan, mediante la ascendencia de Git,
el historial registrado en commits de la rama principal local con el de la rama principal
remota obtenido mediante fetch. Los historiales divergentes se fusionan dentro
del nuevo worktree y requieren verificación. Un fetch fallido genera una
advertencia y permite usar las referencias disponibles localmente; los fallos de
creación no hacen que se escriba en el checkout principal como alternativa.

`workflow.worktrees` es **true** de forma predeterminada; solo el valor YAML
literal `false` desactiva el aislamiento de funcionalidades ordinarias y
mantenimiento. Blueprint/auto-dev conservan su worktree compartido fijo en ambos
casos. La inicialización y las actualizaciones de instalación operan en el
checkout que selecciones explícitamente. Los worktrees completados se conservan;
la finalización no los fusiona ni elimina automáticamente.

Consulta [Desarrollo con worktrees](docs/en/user-guide/workflow.md#worktree-development)
y [configuración](docs/en/reference/configuration.md#workflowworktrees).

## Trabajar con código existente

Dos puntos de entrada sirven a objetivos distintos:

| Comando | Úsalo para | Resultado/límite |
|---------|-----------|-----------------|
| `onboard [path]` | Crear conocimiento reutilizable del proyecto a partir de una base de código existente | Convenciones candidatas y restricciones con evidencia precisa en el perfil; el código sigue siendo de solo lectura |
| `reverse-spec [path]` | Comprender la arquitectura existente o comparar el código con la intención confirmada | Borradores de artefactos o un informe de desviaciones; el código sigue siendo de solo lectura |

```text
/codexspec:onboard src/
/codexspec:reverse-spec
/codexspec:reverse-spec src/auth
```

Onboard infiere convenciones a partir del código observable y solo propone
restricciones a partir de prohibiciones explícitas. Las convenciones candidatas
surten efecto localmente de inmediato; las restricciones candidatas requieren
una decisión en la sesión para guardarlas, editarlas o descartarlas. Conserva el
conocimiento existente y no inventa justificaciones de decisiones pasadas ni
problemas conocidos por experiencia a partir de un primer examen del código.

Reverse-spec tiene tres modos:

- **Panorama general**: sin ruta, o con la raíz del repositorio, produce un
  `design.md` de arquitectura conciso y un `slices.md` para elegir módulos que inspeccionar.
- **Generación**: una ruta de módulo sin una base confirmada produce borradores de
  `spec.md`, `design.md` y requisitos abiertos o inferidos.
- **Conciliación**: un módulo con una base confirmada produce `reconcile.md`,
  que informa de comportamientos no documentados, especificaciones no implementadas
  y discrepancias semánticas frente a la especificación y el diseño confirmados,
  con los requisitos como autoridad sobre la intención.

Los borradores inferidos requieren confirmación humana antes de convertirse en
una base. La conciliación informa de la dirección propuesta —corregir el código,
actualizar los documentos o decidir la intención— y no la aplica automáticamente.

## Revisión y depuración

Cuatro revisores de artefactos comprueban la fidelidad, la cobertura, la
viabilidad y la calidad interna: `review-spec`, `review-design`, `review-plan`
y `review-tasks`. Se ejecutan automáticamente tras la generación y también
pueden invocarse manualmente. Los informes distinguen los defectos verificados
de las recomendaciones sobre riesgos que no bloquean el avance y de las
oportunidades de diseño, e incluyen una puntuación de compatibilidad.

`review-code` proporciona una puerta de defectos independiente limitada a los
cambios y una evaluación explícita de la calidad de todo el código:

```text
/codexspec:review-code --feature <feature-dir>
/codexspec:review-code --uncommitted
/codexspec:review-code --audit src/
```

La revisión predeterminada cubre todos los cambios de la rama de la funcionalidad,
incluidos los registrados en commits, preparados, no preparados y no rastreados que no estén
ignorados. Puedes seleccionar explícitamente evidencia de cambios registrados en commits,
sin confirmar o de un solo commit. `--feature` adjunta el contexto de requisitos
sin reducir el alcance de Git. `--audit` evalúa las rutas indicadas y produce una
ficha de evaluación orientativa en lugar de un veredicto de finalización.

Las revisiones cargan estándares compartidos de `.codexspec/review-code/`,
seleccionando las dimensiones de comportamiento y las comprobaciones de lenguaje
o framework pertinentes. Los hallazgos requieren evidencia concreta,
desencadenantes alcanzables, atribución a los cambios seleccionados e impacto.
El revisor informa de defectos y sugerencias de mantenimiento fundamentadas sin
editar archivos; el proceso que aplica las correcciones los verifica de forma independiente.

La implementación usa pruebas primero para las tareas de código e implementación
directa con comprobaciones apropiadas para documentación y configuración. Tras
las correcciones, una revisión incremental puede reutilizar la cobertura no
afectada; la aceptación final requiere un `PASS` nuevo de la funcionalidad
completa, cobertura y verificación terminadas, y ningún defecto P0–P3 admitido.
Las sugerencias de mantenimiento fundamentadas se informan por separado.

`workflow.auto_maintenance` es **true** de forma predeterminada y controla si
los procesos de corrección también aplican mejoras de mantenimiento verificadas
y compatibles. Desactivarlo sigue permitiendo informar de esas sugerencias y
no exime de corregir defectos ni de realizar las comprobaciones obligatorias.
Es independiente del avance entre etapas y no es un argumento de `implement-tasks`.

Para depurar empezando por la causa raíz:

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

Debug sigue investigación → análisis de patrones → verificación de una sola
hipótesis → corrección precedida de una prueba que falla. La implementación
recurre a esta disciplina cuando las correcciones se atascan, un defecto de
funcionamiento no trivial requiere rastreo o la misma clase de causa raíz reaparece
entre rondas de revisión. Tres correcciones fallidas provocan una reevaluación arquitectónica.

Usa `checklist` para evaluar la claridad, integridad y consistencia de los requisitos:

```text
/codexspec:checklist Check the authentication requirements for completeness
```

Consulta la [referencia de comandos](docs/en/user-guide/commands.md) para los
selectores de revisión, argumentos y procedimientos detallados.

## Conocimiento del proyecto

El perfil del proyecto almacena conocimiento reutilizable en `.codexspec/profile/`:

| Categoría | Contenido |
|----------|----------|
| `constraints/` | Prohibiciones explícitas y límites estrictos, que se leen primero |
| `conventions/` | Patrones, nombres e instrucciones aplicables a varias funcionalidades |
| `pitfalls/` | Problemas conocidos por experiencia, causas, soluciones alternativas y lecciones |
| `decisions/` | Decisiones arquitectónicas y entre funcionalidades reutilizables |
| `strategies/` | Señales que requieren un enfoque de trabajo distinto |
| `runbooks/` | Procedimientos ordenados y recuperación ante fallos |

`distill` captura conocimiento reutilizable del trabajo; la intención específica
de una funcionalidad permanece en sus requisitos, diseño y plan. Init instala
instrucciones en CLAUDE.md y/o AGENTS.md para leer todas las restricciones y el
conocimiento pertinente antes de realizar trabajo sustantivo. El conocimiento
añadido posteriormente puede surtir efecto sin reinicialización. Los registros
candidatos se usan con cautela; los validados requieren verificación de los
resultados y respaldo humano.

```text
/codexspec:distill Capture the reusable lessons from this work
/codexspec:distill review
/codexspec:evolve
```

Una ejecución manual de `distill review`, o una invocación directa de `distill`
sin material nuevo que capturar, abre un espacio de trabajo local y sin conexión
en el navegador. Puedes revisar, validar, descartar, aplazar y consolidar
registros, previsualizar el Markdown final y seleccionar **Aplicar todo**.
Las decisiones permanecen en un borrador recuperable hasta su aplicación; las
comprobaciones de conflictos evitan la aplicación parcial o la sobrescritura
silenciosa. Hay una alternativa explícita en modo texto para entornos sin navegador.

`workflow.auto_distill` es **true** de forma predeterminada y controla tres hooks
de cierre: `implement-tasks` finalizado con éxito, commits ejecutados mediante
`commit-staged` y generación de `pr`. La vista previa de commits no activa la captura.

Las instrucciones instaladas del proyecto también piden a los agentes que
capturen el conocimiento reutilizable a medida que surge en conversaciones
ordinarias, correcciones fuera de SDD y ejecuciones largas de `implement-tasks`.
Esas instrucciones se aplican de forma independiente del ajuste de cierre;
la captura al terminar la tarea proporciona una última salvaguarda.

Dentro de una sesión, los desencadenantes repetidos procesan solo material nuevo.
Entre sesiones, `distill` lee el perfil y omite el conocimiento ya cubierto.
La captura termina sin escribir cuando no queda nada reutilizable. La captura
automática nunca abre la revisión manual, ni espera a una persona ni bloquea el
flujo de trabajo que la invoca.

`evolve` selecciona únicamente conocimiento validado útil más allá del proyecto,
compila un borrador de comando o habilidad y obtiene aprobación explícita antes
de hacer push o abrir una PR de contribución para revisión humana.

Consulta [Conocimiento del proyecto](docs/en/user-guide/commands.md#codexspecdistill)
para las instrucciones detalladas.

### Reutilizar decisiones históricas

También se consulta la historia pertinente de `.codexspec/specs/` antes de
emitir juicios sustantivos sobre requisitos, diseño, implementación, depuración
o revisión, tanto en conversaciones ordinarias como en flujos SDD. Los agentes
reconstruyen las decisiones sin cambios, las adiciones posteriores y las
sustituciones explícitas antes de preguntar al usuario.

Los requisitos antiguos que no hayan cambiado siguen siendo aplicables.
La última decisión explícita del usuario siempre tiene prioridad; las propuestas
abiertas no se consideran intención confirmada. La consulta se limita a la tarea
y se reutiliza el contexto suficiente. Actualiza las instalaciones de los
proyectos existentes para recibir estas instrucciones.

## Flujo de trabajo con Git

```text
/codexspec:commit-staged -p
/codexspec:pr --spec <feature-dir>/spec.md
/codexspec:release-notes --from <ref> --to HEAD
/codexspec:tasks-to-issues <feature-dir>
```

- **commit-staged** analiza el área de preparación exacta y genera un mensaje
  de Conventional Commits; `-p` muestra una vista previa sin hacer commit.
  El flujo de trabajo que lo invoca elige y prepara los archivos. La ejecución
  autorizada usa el entorno de ejecución protegido y vuelve a comprobar que el
  contenido del commit coincide con el análisis. Las instrucciones de commits
  para agentes se aplican en conversaciones ordinarias y en flujos SDD, blueprint
  y auto-dev; que el comando esté disponible no lo invoca ni autoriza un commit.
- **pr** genera una descripción estructurada de una PR de GitHub o una MR de
  GitLab a partir del diff. `--spec` añade opcionalmente contexto de la
  funcionalidad desde la ruta de un archivo `spec.md`, o desde un nombre o
  prefijo de directorio de funcionalidad que se resuelve a ese archivo.
  La salida predeterminada es texto para usar en la plataforma de alojamiento.
- **release-notes** deriva una entrada de Keep a Changelog y el cuerpo de una
  publicación a partir del historial de Git. La sección predeterminada es
  `[Unreleased]`; `--version` usa una etiqueta proporcionada. No prepara archivos,
  ni hace commits, ni incrementa versiones, ni crea tags, ni publica ni crea una release.
- **tasks-to-issues** crea issues de GitHub a partir de tareas existentes,
  incluidas las dependencias y los criterios de aceptación. Requiere una CLI
  de GitHub autenticada y verifica que el repositorio de los issues coincida
  con el remoto configurado.

La vista previa directa de commits y los commits autorizados en el directorio
actual requieren Python 3.11+ y Git; el entorno de ejecución se instala con los
proyectos CLI y se incluye en el plugin de Claude. Las fusiones creadas por el
agente que modifican contenido también usan el análisis de cambios preparados.
Las fusiones que solo conectan historiales conservan el mensaje predeterminado
de Git mientras validan el árbol y los padres; los avances rápidos no crean commits.

## Comandos disponibles

La CLI tiene seis comandos públicos. Las integraciones de agentes distribuyen
28 comandos: Claude usa `/codexspec:<name>` y Codex usa `$codexspec:<name>`.
Las tablas siguientes usan la forma de Claude para facilitar la lectura.

### Comandos CLI

| Comando | Propósito |
|---------|---------|
| `codexspec init` | Inicializar o actualizar un proyecto para Claude, Codex o ambos |
| `codexspec check` | Comprobar las herramientas y dependencias instaladas |
| `codexspec version` | Mostrar la versión e información del sistema |
| `codexspec config` | Ver o modificar la configuración del proyecto |
| `codexspec list-commands` | Enumerar los comandos de agente disponibles por categoría |
| `codexspec show-blueprint` | Imprimir el blueprint del worktree compartido sin modificarlo |

### Comandos del flujo de trabajo principal

| Comando | Propósito |
|---------|---------|
| `/codexspec:constitution` | Crear/actualizar los principios del proyecto con validación entre artefactos |
| `/codexspec:specify` | Discutir, confirmar y guardar los requisitos de una funcionalidad |
| `/codexspec:blueprint` | Preparar o mantener requisitos confirmados pendientes del blueprint |
| `/codexspec:generate-spec` | Compilar los requisitos confirmados en una especificación trazable; revisión automática |
| `/codexspec:spec-to-design` | Definir arquitectura, componentes, interfaces y decisiones; revisión automática |
| `/codexspec:design-to-plan` | Planificar las fases de implementación, su orden y verificación; revisión automática |
| `/codexspec:plan-to-tasks` | Producir tareas verificables que cubran los artefactos anteriores; revisión automática y analyze |
| `/codexspec:implement-tasks` | Ejecutar tareas, verificar resultados, revisar y corregir |
| `/codexspec:auto-dev` | Desarrollar de forma autónoma los requisitos confirmados del blueprint en el orden del documento |

### Comandos de revisión de artefactos

| Comando | Propósito |
|---------|---------|
| `/codexspec:review-spec` | Comprobar la fidelidad y la calidad interna de la especificación |
| `/codexspec:review-design` | Comprobar la fidelidad y viabilidad del diseño y su preparación para la planificación |
| `/codexspec:review-plan` | Comprobar la fidelidad y viabilidad del plan y su preparación para la implementación |
| `/codexspec:review-tasks` | Comprobar la fidelidad, dependencias, ejecutabilidad y verificación de las tareas |

### Requisitos, código existente y depuración

| Comando | Propósito |
|---------|---------|
| `/codexspec:clarify` | Resolver ambigüedades en los requisitos, actualizándolos antes de la especificación |
| `/codexspec:analyze` | Comprobar la trazabilidad de extremo a extremo y ajustar los artefactos posteriores a la autoridad |
| `/codexspec:checklist` | Generar una lista de comprobación de la calidad de los requisitos |
| `/codexspec:tasks-to-issues` | Convertir tareas existentes en issues de GitHub accionables |
| `/codexspec:debug` | Investigar las causas raíz antes de aplicar una corrección |
| `/codexspec:reverse-spec` | Examinar la arquitectura existente, redactar artefactos de módulos o informar de desviaciones respecto a la base |

### Comandos de conocimiento del proyecto

| Comando | Propósito |
|---------|---------|
| `/codexspec:distill` | Capturar conocimiento reutilizable o revisar candidatos en el espacio de trabajo local |
| `/codexspec:evolve` | Compilar conocimiento validado en un borrador de contribución al proyecto de origen |
| `/codexspec:onboard` | Crear convenciones candidatas y restricciones respaldadas por evidencia a partir del código existente |

### Comandos de Git y revisión de código

| Comando | Propósito |
|---------|---------|
| `/codexspec:commit-staged` | Generar mensajes a partir de cambios preparados; previsualizar o ejecutar un commit autorizado |
| `/codexspec:pr` | Generar una descripción estructurada de PR/MR |
| `/codexspec:release-notes` | Mantener una entrada del registro de cambios y generar el cuerpo de una publicación a partir del historial de Git |
| `/codexspec:review-code` | Revisar los cambios seleccionados como puerta de defectos; usar `--audit` para evaluar la calidad del código en las rutas indicadas |

### Comandos de utilidad

| Comando | Propósito |
|---------|---------|
| `/codexspec:config` | Crear/ver/modificar/restablecer interactivamente la configuración del proyecto |
| `/codexspec:quick` | Ejecutar un flujo SDD compacto que prioriza los requisitos para cambios pequeños |

## Configuración e internacionalización

La configuración se encuentra en `.codexspec/config.yml`. Las plantillas
permanecen en inglés; los agentes escriben el texto de interacción y los
artefactos generados en los idiomas configurados. Los 13 códigos de idioma
estándar son `en`, `zh-CN`, `zh-TW`, `ja`, `ko`, `es`, `fr`, `de`, `pt`, `ru`,
`it`, `ar` y `hi`. El código de portugués de la CLI es `pt`; la documentación
localizada y los catálogos de traducción usan `pt-BR`.

### Dimensiones de idioma

| Dimensión | Clave de configuración | En la inicialización | Establecer después | Controla |
|-----------|------------|-------------------|-----------|----------|
| Salida/base | `language.output` | `--lang` | `config --set-lang` | Idioma de respaldo para las otras dimensiones |
| Interacción | `language.interaction` | `--interaction-lang` | `config --set-interaction-lang` | Conversación y salida de la CLI |
| Documento | `language.document` | `--document-lang` | `config --set-document-lang` | Requisitos, especificaciones, diseños, planes y tareas |
| Commit | `language.commit` | `--commit-lang` | `config --set-commit-lang` | Mensajes de commit y contenido de entrega mediante Git |

Cada idioma específico recurre de forma independiente a `language.output` y,
después, a `en`. `language.templates` permanece en `en`.

```bash
codexspec init my-project --ai both \
  --interaction-lang zh-CN --document-lang en --commit-lang en

codexspec config
codexspec config --set-document-lang en
codexspec config --list-langs
```

La primera inicialización en TTY solicita el idioma base, salvo que proporciones
`--lang` o las tres opciones de idioma específicas. `--force` confirma
automáticamente las demás solicitudes de inicialización; no omite esta selección
de idioma. La inicialización sin TTY usa inglés de forma predeterminada.
La reinicialización conserva las claves de idioma que no hayas establecido explícitamente.

### Ajustes del flujo de trabajo y la revisión

| Ajuste | Valor predeterminado | Efecto | Control CLI |
|---------|---------|--------|-------------|
| `workflow.auto_next` | `false` | Avanzar por las etapas SDD ordinarias aprobadas | `config --auto-next on\|off` |
| `workflow.auto_distill` | `true` | Captura no interactiva de conocimiento tras un cierre exitoso | `config --auto-distill on\|off` |
| `workflow.auto_maintenance` | `true` | Aplicar mantenimiento incremental verificado durante las correcciones automáticas | `config --auto-maintenance on\|off` |
| `workflow.worktrees` | `true` | Aislar funcionalidades ordinarias y mantenimiento independiente | `config --worktrees on\|off` |
| `review.decided_by` | `reviewer` | Quién decide sobre hallazgos desencadenados fuera del contexto operativo del proyecto | `config --decided-by reviewer\|ask` |

Los interruptores booleanos de la CLI aceptan `on/true/1/yes` y `off/false/0/no`
sin distinguir mayúsculas y minúsculas, incluidos los espacios circundantes.
Un interruptor booleano sin valor invierte el valor actual del checkout de
destino; los valores almacenados en YAML son booleanos.

Con `review.decided_by: reviewer`, el revisor decide si se admite un defecto.
Con `ask`, un desencadenante fuera de contexto se convierte en una decisión de
escenario pendiente: el usuario decide una vez si debe corregirse o excluirse
ese escenario, y la decisión confirmada se conserva para rondas posteriores.
Las decisiones pendientes bloquean la finalización. Una ejecución individual de
`review-code` puede sustituir el modo configurado con `--decided-by`.

Las escrituras de configuración siguen el enrutamiento de worktrees. Un cambio
independiente desde el checkout principal se hace en el worktree de mantenimiento
y no cambia inmediatamente el ajuste efectivo del principal; los cambios en un
worktree de funcionalidad surten efecto allí.

<details>
<summary>Opciones de inicialización de la CLI</summary>

| Opción | Significado |
|--------|---------|
| `PROJECT_NAME` | Nombre del directorio nuevo; usa `.` para el directorio actual |
| `--here`, `-h` | Inicializar el directorio actual |
| `--ai`, `-a` | `claude`, `codex` o `both`; predeterminado: `claude` |
| `--lang`, `-l` | Establecer el idioma base de salida |
| `--interaction-lang` | Establecer el idioma de interacción |
| `--document-lang` | Establecer el idioma de los documentos |
| `--commit-lang` | Establecer el idioma de los mensajes de commit |
| `--force`, `-f` | Regenerar los artefactos instalados y confirmar automáticamente solicitudes de migración/actualización/cumplimiento; conservar el contexto creado por el proyecto y la configuración no relacionada |
| `--no-git` | Omitir la inicialización del repositorio Git |
| `--debug`, `-d` | Mostrar la salida de depuración detallada |

</details>

<details>
<summary>Opciones de configuración de la CLI</summary>

| Opción | Significado |
|--------|---------|
| `--set-lang`, `-l` | Establecer el idioma base de salida |
| `--set-interaction-lang` | Establecer el idioma de interacción |
| `--set-document-lang` | Establecer el idioma de los documentos |
| `--set-commit-lang`, `-c` | Establecer el idioma de los mensajes de commit |
| `--list-langs` | Enumerar los códigos de idioma compatibles |
| `--auto-next` | Alternar/establecer el avance automático entre etapas |
| `--auto-distill` | Alternar/establecer la captura automática de conocimiento |
| `--auto-maintenance` | Alternar/establecer el mantenimiento incremental automático |
| `--worktrees` | Alternar/establecer el aislamiento mediante worktrees local a cada checkout |
| `--decided-by` | Establecer el modo de decisión de revisión `reviewer` o `ask` |

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
[Internacionalización](docs/en/user-guide/i18n.md) para el comportamiento detallado
de los idiomas y los ajustes.

## Estructura del proyecto

La inicialización instala recursos comunes y la integración del asistente seleccionado:

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

El blueprint compartido se encuentra en el worktree dedicado a auto-dev, en
lugar de existir como una copia editable independiente en cada checkout
ordinario. Los borradores de revisión manual del conocimiento se excluyen de Git.

## Materiales para extensiones

El repositorio incluye una plantilla de manifiesto de extensión, un comando de
ejemplo y una [Guía de desarrollo de extensiones](extensions/EXTENSION-DEVELOPMENT-GUIDE.md).
Son materiales de creación. La CLI actual no tiene comandos para instalar,
enumerar o eliminar extensiones y no carga automáticamente los comandos o hooks
de `extension.yml`. Los recursos de revisión compartidos admiten adiciones
específicas del proyecto en `.codexspec/review-code/`; la inicialización conserva
las modificaciones de recursos existentes y los archivos adicionales, salvo
que se solicite su sustitución.

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

Lee [CLAUDE.md](CLAUDE.md), [AGENTS.md](AGENTS.md) y
[Distribución del repositorio](docs/internal/repository-layout.md) antes de
modificar las plantillas, el empaquetado o la inicialización. Las copias de
comandos y habilidades distribuidos son artefactos de instalación generados;
edita sus fuentes autorizadas y vuelve a generarlos.

## Contribuir

Consulta la [guía para contribuir](docs/en/development/contributing.md) para la
configuración local y las instrucciones de contribución. Las contribuciones
deben conservar los requisitos confirmados, la trazabilidad de las fuentes y
el límite de empaquetado entre usuarios y mantenedores.

## Licencia

MIT — consulta [LICENSE](LICENSE).

## Agradecimientos

Inspirado en [GitHub spec-kit](https://github.com/github/spec-kit).
Se integra con Claude Code y OpenAI Codex.

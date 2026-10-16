# CodexSpec

![CodexSpec](assets/images/codexspec-logo-light.svg#only-light){ width="420" }

![CodexSpec](assets/images/codexspec-logo-dark.svg#only-dark){ width="420" }

**Herramientas SDD con prioridad en los requisitos para Claude Code y OpenAI Codex**

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

<a id="why-choose-codexspec"></a>

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

<a id="what-is-requirements-first-sdd"></a>

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

[![CodexSpec: desarrollo guiado por requisitos, revisiones por etapa y reutilización de la experiencia](../../assets/workflow/workflow-es-light.png#only-light)](../../assets/workflow/workflow-es-light.png#only-light)

[![CodexSpec: desarrollo guiado por requisitos, revisiones por etapa y reutilización de la experiencia](../../assets/workflow/workflow-es-dark.png#only-dark)](../../assets/workflow/workflow-es-dark.png#only-dark)

Abrir el diagrama a tamaño completo: [☀️](../../assets/workflow/workflow-es-light.png) · [🌙](../../assets/workflow/workflow-es-dark.png)

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
en [Flujo de trabajo principal](user-guide/workflow.md#core-workflow).

¿Usas la aplicación de escritorio de Codex? [Pide a Codex que instale e inicialice tu proyecto](getting-started/installation.md#install-with-the-codex-desktop-app).

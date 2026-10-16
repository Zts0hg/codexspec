# Flujo de trabajo

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

<a id="shared-blueprint-and-autonomous-development"></a>

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

<a id="worktree-development"></a>

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

Consulta [Desarrollo con worktrees](workflow.md#worktree-development)
y [configuración](../reference/configuration.md#workflow-and-review-settings).

<a id="work-with-existing-code"></a>

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

<a id="review-and-debugging"></a>

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

La [referencia de comandos](commands.md) detalla los
selectores de revisión, los argumentos y los procedimientos.

<a id="project-knowledge"></a>

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

Consulta [Conocimiento del proyecto](commands.md#codexspecdistill)
para obtener instrucciones detalladas.

<a id="reusing-historical-decisions"></a>

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

<a id="git-workflow"></a>

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

## Trazabilidad y continuación

El archivo `requirements.md` confirmado rige la intención de la funcionalidad; la cadena posterior es `spec.md` → `design.md` → `plan.md` → `tasks.md`, interpretada junto con los principios aplicables del proyecto y los hechos verificados del repositorio. Los requisitos usan ID estables, las entradas de especificación citan `Sources` y el trabajo posterior cita `Covers`. Un artefacto posterior no puede redefinir silenciosamente una decisión anterior. Los conflictos entre fuentes de autoridad o las nuevas decisiones de producto requieren resolución del usuario. Las funcionalidades antiguas sin requisitos indican que falta la confirmación original; si carecen de diseño, usan la alternativa documentada.

Pasa una ruta de funcionalidad explícita si la selección es ambigua; los comandos no eligen silenciosamente el directorio más reciente. El directorio padre de los worktrees se deriva del repositorio principal, incluso al invocar desde un subdirectorio u otro worktree vinculado. En repositorios bare es un directorio hermano llamado `<bare-repository-name>-codexspec-worktrees`. El mantenimiento independiente usa la rama `codexspec/maintenance`.

Si la preparación de un worktree falla, conserva su identidad para poder continuar. Las fusiones de bases divergentes deben superar las comprobaciones del proyecto antes de escribir los requisitos o iniciar el desarrollo. La inspección de solo lectura conserva su fuente; los informes se escriben en el checkout de salida resuelto. La ejecución de commits mantiene el índice seleccionado y nunca traslada los cambios preparados de main a otro worktree. Si faltan recursos instalados necesarios en un worktree nuevo, inicializa ese destino antes de continuar.

## Modelo de revisión

Las revisiones separan tres tipos de salida:

- **Defectos de fidelidad**: conflicto con una fuente autoritativa u omisión de cobertura requerida.
- **Defectos intrínsecos**: el artefacto es internamente contradictorio, no verificable o inviable.
- **Advertencias de riesgo / oportunidades de diseño**: mejoras opcionales sin evidencia de un defecto actual.

Cada defecto debe identificar su evidencia, ubicación, desajuste, impacto y remediación mínima. Los hallazgos con la misma causa raíz se fusionan. Las advertencias no afectan al estado, a la puntuación ni a las correcciones automáticas.

El estado de revisión es:

- `PASS`: no hay defectos críticos, advertencias ni menores.
- `PASS_WITH_WARNINGS`: solo quedan defectos menores.
- `NEEDS_REVISION`: queda una o más advertencias.
- `BLOCKED`: un conflicto crítico impide continuar de forma fiable.

La puntuación de compatibilidad se deriva de los mismos hallazgos clasificados, en lugar de deducciones fijas por sección de plantilla. El estado es autoritativo; la puntuación existe para integraciones que aún esperan un número.

## Revisión automática acotada

Los comandos de generación ejecutan automáticamente la revisión correspondiente. Esta es la disciplina de **revisión basada en evidencia** en acción: solo pueden reparar defectos respaldados por evidencia y volverse a revisar como máximo dos rondas. Se detienen antes si llega `PASS`, y se detienen para pedir entrada del usuario cuando:

- una fuente autoritativa entra en conflicto con otra fuente;
- una corrección cambiaría la intención confirmada;
- el ítem restante es consultivo y no un defecto;
- ya se han consumido dos rondas de reparación.

Los comandos manuales `/codexspec:review-*` pueden ejecutarse en cualquier momento para obtener un informe nuevo.

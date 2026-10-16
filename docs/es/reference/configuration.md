<a id="configuration-and-internationalization"></a>

# Configuración e internacionalización

La configuración se guarda en `.codexspec/config.yml`. Las plantillas permanecen
en inglés; el agente redacta las conversaciones y los artefactos generados en
los idiomas configurados. Los 13 códigos de idioma estándar son `en`, `zh-CN`,
`zh-TW`, `ja`, `ko`, `es`, `fr`, `de`, `pt`, `ru`, `it`, `ar` y `hi`.
Para portugués, la CLI utiliza `pt`; la documentación localizada y los catálogos
de traducción utilizan `pt-BR`.

<a id="language-dimensions"></a>

## Idiomas de interacción, documentos y commits

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

<a id="workflow-and-review-settings"></a>

## Ajustes del flujo de trabajo y la revisión

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

Consulta [Configuración](configuration.md) e
[Internacionalización](../user-guide/i18n.md) para conocer en detalle
el funcionamiento de los idiomas y los ajustes.

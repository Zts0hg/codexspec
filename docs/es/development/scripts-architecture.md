# Arquitectura de scripts e instalación

## Capas de ejecución y autoría

La CLI de Python en `src/codexspec/` instala las plantillas completas de comandos de `templates/commands/`, las plantillas de documentos y los criterios de revisión compartidos. Claude Code recibe comandos de barra; Codex, skills nativas generadas a partir de las mismas fuentes. Los 28 comandos públicos mantienen las mismas reglas de flujo de trabajo en ambos entornos.

## Instalación y contexto del proyecto

`codexspec init` selecciona los scripts auxiliares de la plataforma y la integración solicitada. Los recursos compartidos se guardan en `.codexspec/`, los comandos de Claude en `.claude/commands/codexspec/` y las skills de Codex en `.agents/skills/`. La CLI instalada también ofrece el enrutamiento de espacios de trabajo y las operaciones auxiliares con comprobaciones de protección que utilizan los flujos.

La inicialización actualiza los bloques administrados por CodexSpec en los archivos `AGENTS.md` y `CLAUDE.md` existentes y conserva el contenido propio del proyecto fuera de ellos. `--force` actualiza los artefactos instalados y confirma las solicitudes de actualización; no sustituye todo el archivo de contexto ni descarta configuraciones ajenas. Instalar la CLI no inicializa por sí solo un proyecto.

## Scripts auxiliares por plataforma

Los proyectos Unix reciben los scripts Bash de `scripts/bash/`; los de Windows, los scripts PowerShell de `scripts/powershell/`. La creación de funcionalidades y las comprobaciones de requisitos previos resuelven la funcionalidad seleccionada y devuelven contexto legible por máquinas. `common.sh` y `common.ps1` contienen utilidades compartidas de cada plataforma; `review-context` ayuda a recopilar el contexto del objetivo de revisión. En ambas plataformas, el runtime independiente de commits se copia de `src/codexspec/commit_runtime.py` a `.codexspec/scripts/commit-staged-helper.py`.

## Identidad de funcionalidades y compatibilidad de artefactos

Los nombres siguen el formato `YYYY-MMDD-HHMMss-name`: una marca temporal con precisión de minutos, un sufijo de dos caracteres alfanuméricos en minúscula y un nombre ASCII. El nombre completo identifica un espacio de trabajo; continúa usando su ruta explícita o su rama. No se admiten identificadores secuenciales `NNN-name`. La compatibilidad con versiones anteriores se aplica a los artefactos: las funcionalidades antiguas pueden carecer de `requirements.md` o `design.md`, y los comandos indican las limitaciones de trazabilidad en lugar de inventar una confirmación original.

## Mantenimiento para colaboradores

Edita las fuentes oficiales, regenera las copias derivadas y verifica la distribución. Los comandos que usan fragmentos se editan en `internal/command_templates/sources/`; sus archivos completos en `templates/commands/` se generan. Las demás plantillas de comandos se editan directamente. No modifiques a mano las copias instaladas de Claude o Codex.

El paquete incluye las plantillas públicas y los dos directorios de scripts por plataforma. Las herramientas de mantenimiento de `internal/`, las fuentes del sitio de `docs/`, las pruebas y las fuentes e imágenes de los diagramas quedan fuera del paquete instalado. No amplíes el ámbito de inclusión a todo `scripts/`.

<a id="extension-materials"></a>

## Materiales para extensiones

El repositorio incluye una plantilla de manifiesto de extensión, un comando de
ejemplo y una [Guía de desarrollo de extensiones](https://github.com/Zts0hg/codexspec/blob/main/extensions/EXTENSION-DEVELOPMENT-GUIDE.md).
Estos materiales sirven para crear extensiones. La CLI actual no ofrece
comandos para instalar, listar o eliminar extensiones, ni carga automáticamente
los comandos o hooks de `extension.yml`. Los recursos de revisión compartidos
admiten adiciones propias del proyecto en `.codexspec/review-code/`. La
inicialización conserva los recursos modificados y los archivos adicionales,
a menos que se solicite su sustitución.

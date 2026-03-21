# Caso de Uso de CodexSpec: Agregar Funcionalidad de Generacion de Descripciones PR al Proyecto

> Este documento registra el proceso completo de usar la cadena de herramientas CodexSpec para agregar nueva funcionalidad al propio proyecto CodexSpec, mostrando la aplicacion practica de Spec-Driven Development (SDD).

## Resumen

**Funcionalidad Objetivo**: Agregar comando `/codexspec:pr` para generar descripciones estructuradas de GitHub PR / GitLab MR.

**Flujo de Desarrollo**: `specify -> generate-spec -> review-spec -> clarify -> spec-to-plan`

**Caracteristicas Clave**: Se descubrieron problemas de requisitos durante el desarrollo y se ajustaron mediante el comando `clarify`, mostrando la flexibilidad de SDD.

---

## Fase 1: Clarificacion de Requisitos Originales (`/codexspec:specify`)

### Entrada Inicial del Usuario

```
Me gustaria agregar una funcionalidad al proyecto: proporcionar un nuevo comando relacionado con Git para generar informacion de PR de GitHub precisa, detallada y conforme a estandares (o informacion de MR, para GitLab). Estos son los contenidos de dos comandos de PR que he usado en otros proyectos, proporcionados para tu referencia.

[Ejemplo de Referencia 1 - Descripcion Estructurada]
Ahora, por favor actua como mantenedor del proyecto, basandote en todo el trabajo realizado hasta ahora, escribe una descripcion clara de Pull Request para este commit.
La descripcion del PR debe estar orientada a otros revisores del equipo e incluir las siguientes secciones:
1. Contexto (Context)
2. Implementacion (Implementation)
3. Pruebas (Testing)
4. Como Verificar Manualmente (How to Verify)

[Ejemplo de Referencia 2 - Descripcion Simple]
Por favor, basandote en la diferencia de codigo entre la rama actual y la rama origin/main, organiza un titulo y descripcion de Merge Request conforme a los estandares de Git en formato Markdown. (Usar descripcion en chino)
```

### Proceso de Clarificacion

**Q1: Idioma de Salida**

- Opciones: Seguir configuracion del proyecto / Chino / Deteccion automatica
- **Seleccion del Usuario**: Seguir configuracion del proyecto (actual: en)

**Q2: Soporte de Plataforma**

- Opciones: Soportar GitHub y GitLab simultaneamente / Solo GitHub / Deteccion automatica de plataforma
- **Seleccion del Usuario**: Deteccion automatica de plataforma

**Q3: Contenido de Descripcion PR**

- Opciones: Descripcion estructurada detallada / Descripcion concisa / Plantilla personalizable
- **Seleccion del Usuario**: Descripcion estructurada detallada (recomendado)

**Q4: Condicion de Disparo**

- Opciones: Rama actual vs origin/main / Commits no enviados / Poder especificar rama objetivo
- **Seleccion del Usuario**: Poder especificar rama objetivo

**Q5: Fuente de Spec**

- Opciones: Priorizar spec.md / Solo usar info git / Combinar todas las fuentes
- **Seleccion del Usuario**: Combinar todas las fuentes (recomendado)

**Q6: Nomenclatura**

- Opciones: codexspec.pr / codexspec.create-pr / codexspec.create-mr
- **Seleccion del Usuario**: codexspec.pr (recomendado)

**Q7: Manejo sin Spec**

- Opciones: Continuar generando, saltar contexto / Solicitar crear spec primero / Advertir y continuar
- **Seleccion del Usuario**: Continuar generando, saltar contexto

**Q8: Metodo de Salida**

- Opciones: Salida a terminal / Guardar a archivo / Terminal + archivo opcional
- **Seleccion del Usuario**: Terminal + archivo opcional (recomendado)

**Q9: Secciones por Defecto**

- Opciones: Contexto, Implementacion, Pruebas, Como Verificar (todas)
- **Seleccion del Usuario**: Las cuatro secciones completas

**Q10: Parametros del Comando**

- **Seleccion del Usuario**: Todos los parametros son opcionales
  - `--target-branch`: Por defecto origin/main
  - `--output`: Si no se especifica, por defecto solo salida a terminal
  - `--sections`: Si no se especifica, seguir valores por defecto
  - `--no-spec`: Saltar busqueda de archivo spec.md

### Correccion de Configuracion de Idioma

**Retroalimentacion del Usuario**: El idioma deberia seguir la misma logica que el comando `/commit-staged`, priorizando el parametro `language.commit` en `config.yml`, y si no hay parametro `language.commit` configurado, entonces segun `language.output`.

**Resumen de Requisitos Actualizado**:

```
Prioridad de idioma: language.commit > language.output > English (por defecto)
```

---

## Fase 2: Generar Documento de Especificacion (`/codexspec:generate-spec`)

### Estructura del Documento Generado

El `spec.md` generado incluye las siguientes secciones:

- **Overview**: Resumen de funcionalidad
- **Goals**: 4 objetivos
- **User Stories**: 4 historias de usuario con criterios de aceptacion
- **Functional Requirements**: 8 requisitos (REQ-001 a REQ-008)
- **Command Parameters**: 4 definiciones de parametros
- **Non-Functional Requirements**: 3 requisitos (rendimiento, compatibilidad, manejo de errores)
- **Acceptance Criteria (Test Cases)**: 10 casos de prueba
- **Edge Cases**: 6 casos limite
- **Output Format Example**: Ejemplos de GitHub PR y GitLab MR
- **Out of Scope**: Funcionalidades explicitamente excluidas
- **Dependencies**: Dependencias
- **Related Commands**: Comandos relacionados

### Extracto de Requisitos Clave

```markdown
### REQ-003: Language Configuration
The command shall determine output language in the following priority order:
1. `language.commit` in `.codexspec/config.yml` (highest priority)
2. `language.output` in `.codexspec/config.yml` (fallback)
3. English (default if no configuration)
```

---

## Fase 3: Revision de Especificacion (`/codexspec:review-spec`)

### Resultados de Revision

- **Estado General**: OK Pasar
- **Puntuacion de Calidad**: 92/100
- **Estado de Preparacion**: Ready for Planning

### Problemas Encontrados

**Advertencias (Should Fix)**:

1. **SPEC-001**: Logica de descubrimiento de archivos de prueba no especificada
2. **SPEC-002**: Cuando hay multiples spec.md, seleccionar "modificado mas recientemente" puede ser inexacto

**Sugerencias (Nice to Have)**:

1. Considerar agregar parametro `--title`
2. Agregar requisito de validacion de formato de salida
3. Considerar soporte de patrones URL de GitHub Enterprise

### Ubizacion de Guardado del Reporte de Revision

`.codexspec/specs/001-pr-description-generator/review-spec.md`

---

## Fase 4: Clarificacion y Ajuste de Requisitos (`/codexspec:clarify`) - Punto de Inflexion Critico

### Problemas Descubiertos

**Retroalimentacion del Usuario**:
> Me di cuenta de que hay un problema con el uso de spec.md. Por ejemplo, el usuario esta haciendo un cambio muy pequeno, por lo que no uso el flujo estandarizado specify->plan->tasks->implement de codexspec, sino que hizo cambios directamente a traves de对话 o el plan mode integrado de claude code, y luego de completar los cambios desea llamar individualmente al comando de codexspec para generar informacion de PR conforme a estandares. En este caso, usar por defecto el spec.md modificado mas recientemente podria usar contenido de spec.md previo no relacionado con este cambio.

### Proceso de Preguntas de Clarificacion

**Q1: Estrategia de Seleccion de Spec**

**Contexto**: Actualmente EC-004 establece "multiples spec.md -> usar el modificado mas recientemente". Pero cuando el usuario hace cambios pequenos puede no haber usado el flujo SDD, y el spec.md mas reciente puede no estar relacionado con los cambios actuales.

| Opcion | Descripcion |
|--------|-------------|
| A | Por defecto no usar spec.md, a menos que el usuario especifique explicitamente el parametro `--spec` |
| B | Matching basado en nombre de rama |
| C | Solicitar al usuario que seleccione |
| D | Matching basado en cambios de archivos |

**Seleccion del Usuario**: Opcion A
**Razon**: Evitar referencias erroneas, el parametro `--spec` permite a usuarios que necesitan integracion SDD especificar explicitamente.

---

**Q2: Estrategia de Extraccion de Contenido de Spec**

**Contexto**: Cuando el usuario usa `--spec`, si la estructura de spec.md esta incompleta que hacer?

| Opcion | Descripcion |
|--------|-------------|
| A | Mejor esfuerzo de extraccion, saltar partes faltantes |
| B | Advertir y saltar Context |
| C | Requerir estructura completa, sino error |

**Seleccion del Usuario**: Opcion A
**Razon**: Evitar bloquear flujo de trabajo por problemas de formato de spec.

---

**Q3: Descubrimiento de Archivos de Prueba**

**Contexto**: Como descubrir archivos de prueba para la seccion Testing?

| Opcion | Descripcion |
|--------|-------------|
| A | Patrones de directorios comunes (tests/, test/) |
| B | Heuristica independiente del lenguaje (directorio + patron de nombre de archivo) |
| C | No descubrir activamente, solo inferir de mensajes de commit |

**Seleccion del Usuario**: Opcion B
**Razon**: Cubrir multiples estructuras de proyecto en diferentes lenguajes.

---

**Q4: Generacion de Titulo PR**

**Contexto**: Como deberia generarse el titulo del PR?

| Opcion | Descripcion |
|--------|-------------|
| A | Priorizar parsing de nombre de rama |
| B | Priorizar primer mensaje de commit |
| C | Generacion integral (git diff + nombre de rama + mensaje de commit) |

**Seleccion del Usuario**: Opcion C
**Razon del Usuario**: El primer commit puede ser solo una pequena parte de los cambios; el nombre de rama requiere alta disciplina de nomenclatura. Teniendo mucha informacion de git y code changes para referencia, el analisis integral es mas preciso.

---

**Q5: Generacion de Comandos de Verificacion**

**Contexto**: Como generar comandos de verificacion para la seccion "How to Verify"?

| Opcion | Descripcion |
|--------|-------------|
| A | Plantilla generica |
| B | Deteccion de proyecto (pyproject.toml -> pytest, package.json -> npm test) |
| C | Inferir de mensajes de commit |

**Seleccion del Usuario**: Opcion B
**Razon**: La deteccion de proyecto puede generar comandos de verificacion mas utiles.

---

### Resumen de Sesion de Clarificacion

| Problema | Decision | Impacto |
|------|------|------|
| Estrategia de seleccion de Spec | Opt-in via `--spec` | REQ-007, EC-004, tabla de parametros |
| Extraccion de contenido de Spec | Extraccion de mejor esfuerzo | REQ-005b, EC-004c |
| Descubrimiento de archivos de prueba | Heuristica independiente del lenguaje | REQ-006b |
| Generacion de titulo PR | Analisis integral | REQ-008a |
| Generacion de comandos de verificacion | Deteccion de archivos de proyecto | REQ-010 |

### Cambio Clave: Inversion de Logica de Parametros

```
Diseno original: --no-spec (saltar spec)
Nuevo diseno: --spec (habilitar spec, opt-in)
```

---

## Fase 5: Plan de Implementacion Tecnica (`/codexspec:spec-to-plan`)

### Resumen del Plan

**Metodo de Implementacion**: Archivo de plantilla Markdown (consistente con `/codexspec:commit-staged`)

**Sin Nuevas Dependencias** - La funcionalidad se implementa mediante plantillas de slash command, no requiere codigo Python.

### Resumen de Decisiones Tecnicas

| Decision | Seleccion | Razon |
|------|------|------|
| Metodo de implementacion | Plantilla Markdown | Consistente con comandos existentes, facil de mantener |
| Prioridad de idioma | commit > output > en | Consistente con comando `/commit-staged` |
| Deteccion de plataforma | Parsing de URL remota | Simple y confiable |
| Integracion de Spec | Opt-in (`--spec`) | Evitar referencias erroneas |
| Extraccion de contenido | Mejor esfuerzo | No bloquear flujo de trabajo |
| Descubrimiento de pruebas | Patron de directorio+nombre de archivo | Independiente del lenguaje |
| Generacion de titulo | Analisis integral | Mas preciso |
| Deteccion de comandos | Deteccion de archivos de proyecto | Mas util |
| Modo de salida | Terminal primero, archivo opcional | Flexible |

### Fases de Implementacion

1. **Fase 1**: Creacion de plantilla (YAML frontmatter, configuracion de idioma, contexto Git)
2. **Fase 2**: Funcionalidad principal (integracion Spec, descubrimiento de pruebas, deteccion de comandos, generacion de titulo)
3. **Fase 3**: Manejo de casos limite
4. **Fase 4**: Pruebas
5. **Fase 5**: Actualizacion de documentacion

### Lista de Archivos

**Crear**:

- `templates/commands/pr.md`

**Modificar**:

- `CLAUDE.md` - Agregar descripcion del comando
- `README.md` - Agregar comando a la lista

**Pruebas**:

- `tests/test_pr_template.py`

---

## Diagrama de Flujo Completo

```
+-------------------------------------------------------------------------+
|                         Flujo de Desarrollo SDD CodexSpec                |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|  /codexspec:specify                                                      |
|  |-- Clarificar requisitos mediante Q&A                                 |
|  |-- Usuario proporciono ejemplos de referencia                         |
|  |-- 10 preguntas, cubriendo idioma, plataforma, contenido, params      |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|  /codexspec:generate-spec                                                |
|  |-- Generar spec.md completo                                           |
|  |-- 4 historias de usuario, 8 requisitos funcionales, 10 casos prueba  |
|  |-- Guardar en .codexspec/specs/001-pr-description-generator/spec.md   |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|  /codexspec:review-spec                                                  |
|  |-- Puntuacion de calidad: 92/100                                      |
|  |-- Encontradas 2 advertencias (descubrimiento archivos prueba,        |
|  |   manejo multiple specs)                                             |
|  |-- Estado: Pasar, puede entrar en fase de planificacion               |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|  /codexspec:clarify  - Ajuste Critico                                   |
|  |-- Usuario descubrio problema de escenario de uso real                |
|  |-- 5 preguntas de clarificacion, todas respondidas                    |
|  |-- Cambio clave: --no-spec -> --spec (opt-in)                         |
|  |-- Nuevos 5 requisitos (REQ-005b, 006b, 008a, 010, actualizar 007)    |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|  /codexspec:spec-to-plan                                                 |
|  |-- Actualizar plan de implementacion tecnica                          |
|  |-- 9 decisiones tecnicas, incluyendo 5 nuevas                         |
|  |-- 5 fases de implementacion                                          |
|  |-- Guardar en .codexspec/specs/001-pr-description-generator/plan.md   |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|  Proximos Pasos (no completados en esta sesion)                         |
|  |-- /codexspec:review-plan - Validar calidad del plan                  |
|  |-- /codexspec:plan-to-tasks - Descomponer en tareas ejecutables       |
|  |-- /codexspec:implement-tasks - Ejecutar implementacion               |
+-------------------------------------------------------------------------+
```

---

## Puntos Clave de Aprendizaje

### 1. Valor de la Fase de Clarificacion

Este caso de uso demuestra el rol critico del comando `clarify`:

- **Usuario descubrio problemas reales durante el uso** - Riesgo de uso erroneo de spec.md en escenarios de cambios pequenos
- **Resuelto defectos de diseno mediante Q&A de clarificacion** - Cambio de deteccion automatica a modo opt-in
- **Cambios de requisitos registrados sistematicamente** - Todos los cambios guardados en seccion Clarifications de spec.md

### 2. Flexibilidad del Flujo SDD

- No es un flujo lineal, puede volver a ajustar en cualquier etapa
- `clarify` puede insertarse despues de `review-spec`, antes de `spec-to-plan`
- Documento de especificacion y plan tecnico se actualizan para reflejar cambios

### 3. Evolucion del Diseno de Parametros

```
Diseno inicial:
  --no-spec: Saltar spec.md (usar por defecto)

Diseno final:
  --spec: Habilitar spec.md (no usar por defecto)
```

Este cambio refleja la transicion de diseno de "flujo de trabajo SDD por defecto" a "soportar flujo de trabajo no SDD", haciendo la herramienta mas versatil.

### 4. Entregables de Documentacion

| Fase | Archivo Producido | Contenido |
|------|----------|------|
| generate-spec | spec.md | Documento de especificacion completo |
| review-spec | review-spec.md | Reporte de revision de calidad |
| clarify | (actualiza spec.md) | Registro de clarificacion + actualizacion de requisitos |
| spec-to-plan | plan.md | Plan de implementacion tecnica |

---

## Apéndice: Referencia Rapida de Uso de Comandos

```bash
# 1. Clarificacion de requisitos inicial
/codexspec:specify

# 2. Generar documento de especificacion
/codexspec:generate-spec

# 3. Revisar calidad de especificacion
/codexspec:review-spec

# 4. Clarificar/ajustar requisitos (opcional, usar despues de descubrir problemas)
/codexspec:clarify [descripcion del problema]

# 5. Generar plan tecnico
/codexspec:spec-to-plan

# 6. Revisar calidad del plan (opcional)
/codexspec:review-plan

# 7. Descomponer en tareas
/codexspec:plan-to-tasks

# 8. Ejecutar implementacion
/codexspec:implement-tasks
```

---

*Este documento fue generado automaticamente por el flujo de trabajo SDD de CodexSpec, registrando el proceso de conversacion de desarrollo real.*

# Comandos

Esta es la referencia de los comandos slash de CodexSpec. Estos comandos se invocan en la interfaz de chat de Claude Code.

Para patrones de flujo de trabajo y cuando usar cada comando, ver [Flujo de Trabajo](workflow.md). Para comandos CLI, ver [CLI](../reference/cli.md).

## Referencia Rapida

| Comando | Proposito |
|---------|---------|
| `/codexspec.constitution` | Crear o actualizar la constitucion del proyecto con validacion cruzada de artefactos |
| `/codexspec.specify` | Clarificar requisitos a traves de Q&A interactivo |
| `/codexspec.generate-spec` | Generar documento spec.md desde requisitos clarificados |
| `/codexspec.clarify` | Escanear spec existente en busca de ambiguedades (refinamiento iterativo) |
| `/codexspec.spec-to-plan` | Convertir especificacion en plan de implementacion tecnica |
| `/codexspec.plan-to-tasks` | Desglosar plan en tareas atomicas con TDD aplicado |
| `/codexspec.implement-tasks` | Ejecutar tareas con flujo de trabajo TDD condicional |
| `/codexspec.review-spec` | Validar especificacion por completitud y calidad |
| `/codexspec.review-plan` | Revisar plan tecnico por viabilidad y alineacion |
| `/codexspec.review-tasks` | Validar desglose de tareas por cumplimiento TDD |
| `/codexspec.analyze` | Analisis de consistencia cruzada entre artefactos (solo lectura) |
| `/codexspec.checklist` | Generar listas de verificacion de calidad de requisitos |
| `/codexspec.tasks-to-issues` | Convertir tareas en issues de GitHub |
| `/codexspec.commit` | Generar mensajes Conventional Commits con contexto de sesion |
| `/codexspec.commit-staged` | Generar mensaje de commit desde cambios en staging |

---

## Categorias de Comandos

### Comandos de Flujo de Trabajo Principal

Comandos para el flujo SDD principal: Constitution -> Specification -> Plan -> Tasks -> Implementation.

### Comandos de Revision (Puertas de Calidad)

Comandos que validan artefactos en cada etapa del flujo de trabajo. **Recomendados antes de continuar a la siguiente etapa.**

### Comandos Avanzados

Comandos para refinamiento iterativo, validacion cruzada de artefactos e integracion con gestion de proyectos.

---

## Referencia de Comandos

### `/codexspec.constitution`

Crear o actualizar la constitucion del proyecto. La constitucion define principios arquitectonicos, stack tecnologico, estandares de codigo y reglas de gobierno que guian todas las decisiones de desarrollo posteriores.

**Sintaxis:**
```
/codexspec.constitution [descripcion de principios]
```

**Argumentos:**
| Argumento | Requerido | Descripcion |
|----------|----------|-------------|
| `descripcion de principios` | No | Descripcion de principios a incluir (se solicitara si no se proporciona) |

**Que hace:**
- Crea `.codexspec/memory/constitution.md` si no existe
- Actualiza constitucion existente con nuevos principios
- Valida consistencia cruzada con plantillas
- Genera Informe de Impacto de Sincronizacion mostrando cambios y archivos afectados
- Incluye revision de constitucionalidad para plantillas dependientes

**Que crea:**
```
.codexspec/
+-- memory/
    +-- constitution.md    # Documento de gobierno del proyecto
```

**Ejemplo:**
```text
Tu: /codexspec.constitution Enfocarse en calidad de codigo, estandares de pruebas y clean architecture

AI:  Creando constitucion...

     + Creado .codexspec/memory/constitution.md
     Version: 1.0.0

     Informe de Impacto de Sincronizacion:
     - plan-template-*.md: OK alineado
     - spec-template-*.md: OK alineado
     - tasks-template-*.md: OK alineado

     Principios Principales:
     1. Calidad de Codigo Primero
     2. Test-Driven Development
     3. Clean Architecture

     Commit sugerido: docs: create constitution v1.0.0
```

**Consejos:**
- Define principios temprano en el proyecto para toma de decisiones consistente
- Incluye tanto principios tecnicos como de proceso
- Revisa la constitucion antes del desarrollo de funcionalidades importantes
- Los cambios en la constitucion activan validacion cruzada de artefactos

---

### `/codexspec.specify`

Clarificar requisitos a traves de Q&A interactivo. Este comando explora tu idea inicial sin crear ningun archivo: mantienes control total.

**Sintaxis:**
```
/codexspec.specify [tu idea o requisito]
```

**Argumentos:**
| Argumento | Requerido | Descripcion |
|----------|----------|-------------|
| `tu idea o requisito` | No | Descripcion inicial de lo que quieres construir (se solicitara si no se proporciona) |

**Que hace:**
- Hace preguntas clarificadoras para entender tu idea
- Explora casos limite que podrias no haber considerado
- Co-crea requisitos de alta calidad a traves del dialogo
- Se enfoca en "que" y "por que", no en implementacion tecnica
- **NO genera archivos** - tu decides cuando crear documentacion

**Que NO crea:**
- No se crean archivos durante este comando
- Los requisitos permanecen en la conversacion hasta que apruebes

**Ejemplo:**
```text
Tu: /codexspec.specify Quiero construir una app de gestion de tareas

AI:  Excelente! Te ayudo a clarificar los requisitos.

     Primero, quienes son los usuarios objetivo de esta app?
     - Profesionales individuales
     - Equipos pequenos
     - Organizaciones empresariales
     - Todos los anteriores

Tu: Equipos pequenos, principalmente equipos de desarrollo de software

AI:  Entendido. Para equipos de desarrollo pequenos:
     - Necesitas funciones de colaboracion en tiempo real?
     - Las tareas deben soportar subtareas o solo listas planas?
     - AlgUn requisito de integracion (GitHub, Slack, etc.)?

Tu: Tiempo real es importante. Subtareas si. Integracion con GitHub seria bueno.

AI:  [Continua explorando requisitos...]

     Resumen de requisitos clarificados:
     - Objetivo: Equipos de desarrollo pequenos (5-20 personas)
     - Principal: Tareas con subtareas, actualizaciones en tiempo real
     - Integracion: GitHub (opcional)
     - Prioridad: Colaboracion en tiempo real > Subtareas > GitHub

     Listo para generar el documento de especificacion?
     Usa /codexspec.generate-spec para crear spec.md
```

**Consejos:**
- Usar para exploracion inicial de requisitos
- No te preocupes por estar completo - el refinamiento es iterativo
- Pregunta si AI hace suposiciones
- Revisa el resumen antes de generar spec

---

### `/codexspec.generate-spec`

Generar el documento `spec.md` desde requisitos clarificados. Este comando actua como un "compilador de requisitos" que transforma tus requisitos clarificados en una especificacion estructurada.

**Sintaxis:**
```
/codexspec.generate-spec
```

**Argumentos:**
| Argumento | Requerido | Descripcion |
|----------|----------|-------------|
| Ninguno | - | Usa contexto de sesion `/codexspec.specify` previa |

**Que hace:**
- Crea directorio `.codexspec/specs/{NNN}-{feature-name}/`
- Genera `spec.md` completo con:
  - Resumen de funcionalidad y objetivos
  - Historias de usuario con criterios de aceptacion
  - Requisitos funcionales (formato REQ-XXX)
  - Requisitos no funcionales (formato NFR-XXX)
  - Casos limite y enfoques de manejo
  - Elementos fuera del alcance

**Que crea:**
```
.codexspec/
+-- specs/
    +-- 001-task-management/
        +-- spec.md
```

**Ejemplo:**
```text
Tu: /codexspec.generate-spec

AI:  Generando especificacion...

     + Creado .codexspec/specs/001-task-management/spec.md

     Secciones incluidas:
     - Resumen: Gestion de tareas para equipos de desarrollo pequenos
     - 4 Historias de Usuario con criterios de aceptacion
     - 12 Requisitos Funcionales (REQ-001 a REQ-012)
     - 3 Requisitos No Funcionales (NFR-001 a NFR-003)
     - 5 Casos Limite documentados
     - Fuera del Alcance: Apps moviles, SSO empresarial

     Proximos pasos:
     - Revisar el spec con /codexspec.review-spec
     - O continuar con /codexspec.spec-to-plan
```

**Consejos:**
- Ejecutar despues de que `/codexspec.specify` ha clarificado requisitos
- Revisar el spec generado antes de continuar
- Usar `/codexspec.review-spec` para validacion de calidad
- Editar spec.md directamente si se necesitan ajustes menores

---

### `/codexspec.clarify`

Escanear una especificacion existente en busca de ambiguedades y brechas. Usar esto para refinamiento iterativo despues de la creacion inicial del spec.

**Sintaxis:**
```
/codexspec.clarify [ruta_a_spec.md]
```

**Argumentos:**
| Argumento | Requerido | Descripcion |
|----------|----------|-------------|
| `ruta_a_spec.md` | No | Ruta al archivo spec (auto-detectado si no se proporciona) |

**Que hace:**
- Escanea spec usando 4 categorias de ambiguedad enfocadas
- Hace preguntas de clarificacion dirigidas (maximo 5)
- Actualiza spec.md con respuestas de clarificacion
- Se integra con hallazgos de review-spec si estan disponibles

**Categorias de Ambiguedad:**

| Categoria | Que Detecta |
|----------|-----------------|
| **Brechas de Completitud** | Secciones faltantes, contenido vacio, criterios de aceptacion ausentes |
| **Problemas de Especificidad** | Terminos vagos ("rapido", "escalable"), restricciones no definidas |
| **Claridad Conductual** | Brechas en manejo de errores, transiciones de estado no definidas |
| **Problemas de Medibilidad** | Requisitos no funcionales sin metricas |

**Ejemplo:**
```text
Tu: /codexspec.clarify

AI:  Escaneando spec.md en busca de ambiguedades...

     Problemas encontrados en 3 categorias.

     ## Pregunta 1/5: Especificidad

     **Contexto**: NFR-001 establece "El sistema debe responder rapidamente"

     **Pregunta**: Cual es el tiempo de respuesta objetivo?

     | Opcion | Descripcion | Impacto |
     |--------|-------------|--------|
     | A | < 100ms para todas las operaciones | Requisito de alto rendimiento |
     | B | < 500ms para lecturas, < 1s para escrituras | Enfoque equilibrado |
     | Custom | Proporcionar una respuesta diferente | - |

     **Recomendacion**: Opcion B - equilibrado para app web tipica

Tu: B

AI:  + Actualizado NFR-001: Tiempo de respuesta < 500ms lecturas, < 1s escrituras
     Agregado a seccion Clarifications en spec.md
```

**Consejos:**
- Usar cuando spec.md existe pero necesita refinamiento
- Se integra con hallazgos de `/codexspec.review-spec`
- Maximo 5 preguntas por sesion
- Ejecutar multiples veces para especificaciones complejas

---

### `/codexspec.spec-to-plan`

Convertir la especificacion de funcionalidad en un plan de implementacion tecnica. Aqui es donde defines **como** se construira la funcionalidad.

**Sintaxis:**
```
/codexspec.spec-to-plan [ruta_a_spec.md]
```

**Argumentos:**
| Argumento | Requerido | Descripcion |
|----------|----------|-------------|
| `ruta_a_spec.md` | No | Ruta al archivo spec (auto-detectado desde `.codexspec/specs/` si no se proporciona) |

**Que hace:**
- Lee especificacion y constitucion
- Define stack tecnologico con restricciones de version
- Realiza revision de constitucionalidad (obligatoria si existe constitucion)
- Crea arquitectura con grafo de dependencia de modulos
- Documenta decisiones tecnicas con justificacion
- Planifica fases de implementacion

**Que crea:**
```
.codexspec/
+-- specs/
    +-- 001-task-management/
        +-- plan.md    # Plan de implementacion tecnica
```

**Ejemplo:**
```text
Tu: /codexspec.spec-to-plan Usar Python FastAPI para backend, React para frontend, PostgreSQL para base de datos

AI:  Generando plan tecnico...

     Revision de Constitucionalidad:
     + Clean Architecture: Diseno modular con limites claros
     + TDD: Enfoque test-first aplicado en fases
     + Calidad de Codigo: Linting y type hints requeridos

     Arquitectura:
     - Backend: FastAPI con arquitectura en capas
     - Frontend: React con estructura de componentes
     - Base de datos: PostgreSQL con estrategia de migracion

     Grafo de Dependencia de Modulos:
     +-------------+
     |    API      |
     +------+------+
            |
     +------v------+
     |  Services   |
     +------+------+
            |
     +------v------+
     |    Data     |
     +-------------+

     + Creado plan.md
     5 Fases de Implementacion definidas
```

**Consejos:**
- Ejecutar despues de que el spec esta revisado y estable
- La revision de constitucionalidad es obligatoria si existe constitucion
- Incluir secciones relevantes segun el tipo de proyecto
- Revisar plan antes de continuar con tareas

---

### `/codexspec.plan-to-tasks`

Desglosar el plan tecnico en tareas atomicas y accionables con aplicacion de TDD.

**Sintaxis:**
```
/codexspec.plan-to-tasks [ruta_a_spec.md ruta_a_plan.md]
```

**Argumentos:**
| Argumento | Requerido | Descripcion |
|----------|----------|-------------|
| `rutas` | No | Rutas a spec y plan (auto-detectadas si no se proporcionan) |

**Que hace:**
- Crea tareas atomicas (un archivo principal por tarea)
- Aplica TDD: tareas de prueba preceden tareas de implementacion
- Marca tareas paralelizables con `[P]`
- Especifica rutas de archivo exactas para cada tarea
- Define puntos de control de fase

**Que crea:**
```
.codexspec/
+-- specs/
    +-- 001-task-management/
        +-- tasks.md    # Desglose de tareas
```

**Estructura de Tarea:**
```markdown
### Task 2.1: Write Tests for Entity A [P]
- **Type**: Testing
- **Files**: `tests/test_entity_a.py`
- **Description**: Write unit tests for Entity A
- **Dependencies**: Task 1.3
- **Est. Complexity**: Low
```

**Ejemplo:**
```text
Tu: /codexspec.plan-to-tasks

AI:  Desglosando plan en tareas...

     + Creado tasks.md
     Total: 24 tareas
     Paralelizables: 8 tareas (33%)

     Fase 1: Fundacion (4 tareas)
     Fase 2: Implementacion Principal - TDD (10 tareas)
     Fase 3: Integracion (4 tareas)
     Fase 4: Capa de Interfaz (3 tareas)
     Fase 5: Pruebas y Documentacion (3 tareas)

     Orden de Ejecucion:
     Fase 1 -> [Fase 2 tareas en grupos paralelos] -> Fase 3 -> Fase 4 -> Fase 5

     Puntos de control definidos en cada limite de fase.
```

**Consejos:**
- Cada tarea debe involucrar solo UN archivo principal
- Las tareas de prueba siempre preceden tareas de implementacion
- `[P]` marca tareas verdaderamente independientes paralelizables
- Revisar dependencias antes de implementacion

---

### `/codexspec.implement-tasks`

Ejecutar tareas de implementacion con flujo de trabajo TDD condicional. Trabaja a traves de la lista de tareas sistematicamente.

**Sintaxis:**
```
/codexspec.implement-tasks [ruta_tasks]
/codexspec.implement-tasks [ruta_spec ruta_plan ruta_tasks]
```

**Argumentos:**
| Argumento | Requerido | Descripcion |
|----------|----------|-------------|
| `ruta_tasks` | No | Ruta a tasks.md (auto-detectado si no se proporciona) |
| `ruta_spec ruta_plan ruta_tasks` | No | Rutas explicitas a los tres documentos |

**Resolucion de Archivos:**
- **Sin argumentos**: Auto-detectar desde `.codexspec/specs/`
- **Un argumento**: Tratar como ruta `tasks.md`, derivar otros del mismo directorio
- **Tres argumentos**: Rutas explicitas a spec.md, plan.md y tasks.md

**Que hace:**
- Lee tasks.md e identifica tareas incompletas
- Aplica flujo de trabajo TDD para tareas de codigo:
  - **Red**: Escribir pruebas que fallan primero
  - **Green**: Implementar para pasar pruebas
  - **Verify**: Ejecutar todas las pruebas
  - **Refactor**: Mejorar manteniendo pruebas en verde
- Implementacion directa para tareas no testeables (docs, config)
- Actualiza checkboxes de tareas a medida que progresa el trabajo
- Registra bloqueos en issues.md si se encuentran

**Flujo de Trabajo TDD para Tareas de Codigo:**
```
Red -> Green -> Verify -> Refactor -> Marcar Completo
```

**Implementacion Directa para No Testeables:**
- Archivos de documentacion
- Archivos de configuracion
- Recursos estaticos
- Archivos de infraestructura

**Ejemplo:**
```text
Tu: /codexspec.implement-tasks

AI:  Iniciando implementacion...

     Cargando contexto:
     - spec.md OK
     - plan.md OK
     - tasks.md OK
     - constitution.md OK

     Stack Tecnologico: Python 3.11+ / FastAPI / PostgreSQL / pytest

     Trabajando en Task 1.1: Setup Project Structure
     + Creado src/taskman/__init__.py
     + Creado pyproject.toml
     [x] Task 1.1 Completo

     Trabajando en Task 2.1: Write Tests for Task Entity [P]
     + Creado tests/test_task.py
     Ejecutando pruebas... 5 pasadas (todas fallas esperadas)
     [x] Task 2.1 Completo

     Trabajando en Task 2.2: Implement Task Entity
     + Creado src/taskman/models/task.py
     Ejecutando pruebas... 5 pasadas
     [x] Task 2.2 Completo

     ...
```

**Consejos:**
- Puede continuar donde se quedo si se interrumpe
- Los bloqueos se registran en issues.md
- Los commits se hacen despues de tareas/fases significativas
- Ejecutar `/codexspec.review-tasks` primero para validacion

---

### `/codexspec.review-spec`

Validar la especificacion por completitud, claridad, consistencia y preparacion para planificacion tecnica.

**Sintaxis:**
```
/codexspec.review-spec [ruta_a_spec.md]
```

**Argumentos:**
| Argumento | Requerido | Descripcion |
|----------|----------|-------------|
| `ruta_a_spec.md` | No | Ruta al archivo spec (auto-detectado si no se proporciona) |

**Que hace:**
- Verifica completitud de todas las secciones requeridas
- Evalua claridad y especificidad
- Verifica consistencia interna
- Evalua testeabilidad de requisitos
- Verifica alineacion con constitucion
- Genera informe de revision con puntuacion

**Dimensiones de Revision:**

| Dimension | Peso | Que Valida |
|-----------|--------|-------------------|
| Completitud | 25% | Todas las secciones presentes y sustanciales |
| Claridad | 25% | Sin lenguaje vago, interpretaciones unicas |
| Consistencia | 20% | Sin contradicciones internas |
| Testeabilidad | 20% | Los requisitos pueden verificarse |
| Alineacion con Constitucion | 10% | Se alinea con principios del proyecto |

**Ejemplo:**
```text
Tu: /codexspec.review-spec

AI:  Revisando especificacion...

     # Informe de Revision de Especificacion

     ## Resumen
     - **Estado General**: ! Necesita Trabajo
     - **Puntuacion de Calidad**: 72/100
     - **Preparacion**: Necesita Revision

     ## Analisis de Secciones
     | Seccion | Estado | Completitud | Calidad |
     |---------|--------|--------------|---------|
     | Resumen | OK | 100% | Alta |
     | Objetivos | OK | 100% | Alta |
     | Historias de Usuario | ! | 80% | Media |
     | Requisitos Funcionales | OK | 100% | Alta |
     | Requisitos No Funcionales | ! | 50% | Media |
     | Casos Limite | X | 0% | N/A |

     ## Problemas Criticos (Debe Corregir)
     - [SPEC-001]: La seccion Casos Limite esta vacia
       - Impacto: Puede perder escenarios de fallo importantes
       - Sugerencia: Documentar al menos 3-5 casos limite

     ## Advertencias (Deberia Corregir)
     - [SPEC-002]: NFR-001 usa termino vago "rapido"
       - Impacto: No se puede verificar sin metricas
       - Sugerencia: Especificar tiempo de respuesta concreto

     ## Recomendaciones
     1. Agregar seccion de Casos Limite con enfoques de manejo
     2. Cuantificar requisitos no funcionales
     3. Agregar criterios de aceptacion a Historia de Usuario 3

     Seguimiento disponible:
     - /codexspec.clarify - para abordar ambiguedades
     - /codexspec.spec-to-plan - si problemas resueltos
```

**Consejos:**
- Ejecutar antes de `/codexspec.spec-to-plan`
- Abordar problemas Criticos antes de continuar
- Las Advertencias no bloquean pero indican riesgo
- Re-ejecutar despues de hacer correcciones

---

### `/codexspec.review-plan`

Revisar el plan de implementacion tecnica por viabilidad, calidad de arquitectura y alineacion con la especificacion.

**Sintaxis:**
```
/codexspec.review-plan [ruta_a_plan.md]
```

**Argumentos:**
| Argumento | Requerido | Descripcion |
|----------|----------|-------------|
| `ruta_a_plan.md` | No | Ruta al archivo plan (auto-detectado si no se proporciona) |

**Que hace:**
- Verifica que los requisitos del spec tengan cobertura en el plan
- Evalua elecciones de stack tecnologico
- Evalua decisiones de arquitectura
- Valida fases de implementacion
- Verifica alineacion con constitucion
- Genera informe de revision con puntuacion

**Dimensiones de Revision:**

| Dimension | Peso | Que Valida |
|-----------|--------|-------------------|
| Alineacion con Spec | 30% | Todos los requisitos tienen implementacion |
| Stack Tecnologico | 15% | Elecciones de tecnologia apropiadas |
| Calidad de Arquitectura | 25% | Diseno y patrones solidos |
| Planificacion de Fases | 15% | Fases logicas y realistas |
| Alineacion con Constitucion | 15% | Sigue principios del proyecto |

**Ejemplo:**
```text
Tu: /codexspec.review-plan

AI:  Revisando plan tecnico...

     # Informe de Revision de Plan

     ## Resumen
     - **Estado General**: OK Pasar
     - **Puntuacion de Calidad**: 85/100
     - **Preparacion**: Listo para Desglose de Tareas

     ## Alineacion con Spec
     | Requisito | Cobertura | Estado |
     |-------------|----------|--------|
     | REQ-001 a REQ-012 | OK Completo | Todos cubiertos |
     | US-001 a US-004 | OK Completo | Todos cubiertos |
     | NFR-001 a NFR-003 | ! Parcial | Caching no detallado |

     ## Revision de Arquitectura
     Fortalezas:
     - Separacion clara de responsabilidades
     - Limites de modulo bien definidos
     - Patrones de diseno apropiados

     Preocupaciones:
     - Falta documentacion de estrategia de manejo de errores

     ## Alineacion con Constitucion
     | Principio | Cumplimiento |
     |-----------|------------|
     | Clean Architecture | OK |
     | TDD | OK |
     | Calidad de Codigo | OK |

     Listo para /codexspec.plan-to-tasks
```

**Consejos:**
- Ejecutar antes de `/codexspec.plan-to-tasks`
- Los problemas criticos deben resolverse
- Usar para detectar problemas de arquitectura temprano
- Verificar que el stack tecnologico se alinea con las habilidades del equipo

---

### `/codexspec.review-tasks`

Validar el desglose de tareas por completitud, cumplimiento TDD, ordenamiento correcto y dependencias apropiadas.

**Sintaxis:**
```
/codexspec.review-tasks [ruta_a_tasks.md]
```

**Argumentos:**
| Argumento | Requerido | Descripcion |
|----------|----------|-------------|
| `ruta_a_tasks.md` | No | Ruta al archivo tasks (auto-detectado si no se proporciona) |

**Que hace:**
- Verifica que todos los items del plan tengan cobertura de tareas
- Valida cumplimiento TDD (pruebas antes de implementacion)
- Verifica granularidad de tareas (atomicas, enfoque de archivo unico)
- Valida dependencias (sin ciclos, ordenamiento correcto)
- Revisa marcadores de paralelizacion
- Valida rutas de archivos

**Dimensiones de Revision:**

| Dimension | Peso | Que Valida |
|-----------|--------|-------------------|
| Cobertura del Plan | 30% | Todos los items del plan tienen tareas |
| Cumplimiento TDD | 25% | Flujo test-first aplicado |
| Dependencias y Ordenamiento | 20% | Dependencias correctas, sin ciclos |
| Granularidad de Tareas | 15% | Atomicas, alcance apropiado |
| Paralelizacion y Archivos | 10% | Marcadores y rutas correctos |

**Ejemplo:**
```text
Tu: /codexspec.review-tasks

AI:  Revisando desglose de tareas...

     # Informe de Revision de Tareas

     ## Resumen
     - **Estado General**: ! Necesita Trabajo
     - **Puntuacion de Calidad**: 78/100
     - **Total Tareas**: 24
     - **Paralelizables**: 8 (33%)

     ## Cumplimiento TDD
     | Componente | Tarea Prueba | Prueba Antes de Impl | Estado |
     |-----------|-----------|------------------|--------|
     | Task Entity | OK | OK | OK |
     | User Entity | OK | OK | OK |
     | TaskService | X Falta | N/A | X |

     ## Violaciones TDD
     - [TDD-001]: TaskService falta tarea de prueba

     ## Problemas de Dependencias
     - [DEP-001]: Task 2.5 marcada [P] pero depende de 2.4

     ## Recomendaciones
     1. Agregar tarea de prueba para TaskService antes de implementacion
     2. Corregir marcador de paralelizacion en Task 2.5

     Corregir problemas antes de /codexspec.implement-tasks
```

**Consejos:**
- Ejecutar antes de `/codexspec.implement-tasks`
- Las violaciones TDD son criticas para calidad de codigo
- Verificar que los marcadores de paralelizacion son precisos
- Verificar que las rutas de archivos coinciden con estructura del proyecto

---

### `/codexspec.analyze`

Realizar un analisis de consistencia cruzada entre artefactos no destructivo a traves de spec.md, plan.md y tasks.md. Identifica inconsistencias, duplicaciones y brechas de cobertura.

**Sintaxis:**
```
/codexspec.analyze
```

**Argumentos:**
| Argumento | Requerido | Descripcion |
|----------|----------|-------------|
| Ninguno | - | Analiza los artefactos de la funcionalidad actual |

**Que hace:**
- Detecta duplicaciones entre artefactos
- Identifica ambiguedades que carecen de criterios medibles
- Encuentra items sub-especificados
- Verifica alineacion con constitucion
- Mapea cobertura de requisitos a tareas
- Reporta inconsistencias en terminologia y ordenamiento

**Niveles de Severidad:**

| Nivel | Definicion |
|-------|------------|
| **CRITICAL** | Violacion de constitucion, artefacto principal faltante, cobertura cero |
| **HIGH** | Requisito duplicado/contradictorio, atributo de seguridad ambiguo |
| **MEDIUM** | Deriva de terminologia, falta cobertura no funcional |
| **LOW** | Mejoras de estilo/redaccion |

**Ejemplo:**
```text
Tu: /codexspec.analyze

AI:  Analizando artefactos...

     # Informe de Analisis de Especificacion

     ## Resumen de Cobertura
     | Clave de Requisito | Tiene Tarea? | IDs de Tarea |
     |-----------------|-----------|----------|
     | REQ-001 | OK | 2.1, 2.2 |
     | REQ-002 | OK | 2.3, 2.4 |
     | REQ-003 | X | Ninguno |

     ## Problemas Encontrados

     | ID | Categoria | Severidad | Resumen |
     |----|----------|----------|---------|
     | A1 | Cobertura | CRITICAL | REQ-003 no tiene cobertura de tarea |
     | A2 | Duplicacion | HIGH | REQ-005 y REQ-008 se superponen |
     | A3 | Ambiguedad | MEDIUM | NFR-002 "seguro" no definido |

     ## Metricas
     - Total Requisitos: 12
     - Total Tareas: 24
     - Cobertura: 92% (11/12 requisitos)
     - Problemas Criticos: 1

     ## Proximas Acciones
     1. Agregar tareas para REQ-003 (CRITICAL)
     2. Considerar fusionar REQ-005 y REQ-008
     3. Definir "seguro" en NFR-002

     Resolver problemas CRITICAL antes de /codexspec.implement-tasks
```

**Consejos:**
- Ejecutar despues de `/codexspec.plan-to-tasks`, antes de implementacion
- Los problemas CRITICAL deben bloquear implementacion
- Analisis de solo lectura - no se modifican archivos
- Usar hallazgos para mejorar calidad de artefactos

---

### `/codexspec.checklist`

Generar listas de verificacion de calidad para validar completitud, claridad y consistencia de requisitos. Estas son "pruebas unitarias para escritura de requisitos".

**Sintaxis:**
```
/codexspec.checklist [area_enfoque]
```

**Argumentos:**
| Argumento | Requerido | Descripcion |
|----------|----------|-------------|
| `area_enfoque` | No | Enfoque de dominio (ej., "ux", "api", "seguridad", "rendimiento") |

**Que hace:**
- Genera listas de verificacion organizadas por dimensiones de calidad
- Crea listas de verificacion en directorio `FEATURE_DIR/checklists/`
- Los items se enfocan en calidad de requisitos, no pruebas de implementacion

**Dimensiones de Calidad:**
- **Completitud de Requisitos**: Estan todos los requisitos necesarios presentes?
- **Claridad de Requisitos**: Son los requisitos especificos y sin ambiguedades?
- **Consistencia de Requisitos**: Los requisitos se alinean sin conflictos?
- **Calidad de Criterios de Aceptacion**: Son los criterios de exito medibles?
- **Cobertura de Escenarios**: Estan todos los flujos/casos abordados?
- **Cobertura de Casos Limite**: Estan las condiciones limite definidas?
- **Requisitos No Funcionales**: Rendimiento, Seguridad, Accesibilidad especificados?
- **Dependencias y Suposiciones**: Estan documentadas?

**Ejemplos de Tipos de Lista de Verificacion:**
- `ux.md` - Jerarquia visual, estados de interaccion, accesibilidad
- `api.md` - Formatos de error, rate limiting, autenticacion
- `security.md` - Proteccion de datos, modelo de amenazas, respuesta a brechas
- `performance.md` - Metricas, condiciones de carga, degradacion

**Ejemplo:**
```text
Tu: /codexspec.checklist seguridad

AI:  Generando lista de verificacion de seguridad...

     + Creado .codexspec/specs/001-task-management/checklists/security.md

     ## Lista de Verificacion de Calidad de Requisitos de Seguridad

     ### Requisitos de Autenticacion
     - [ ] CHK001 - Estan definidos los requisitos de autenticacion para todos los endpoints protegidos? [Completitud]
     - [ ] CHK002 - Esta la complejidad de contrasena explicitamente especificada? [Claridad]
     - [ ] CHK003 - Estan cuantificados los requisitos de timeout de sesion? [Medibilidad]

     ### Proteccion de Datos
     - [ ] CHK004 - Estan especificados los requisitos de encriptacion de datos en reposo? [Completitud]
     - [ ] CHK005 - Estan especificados los requisitos de encriptacion de datos en transito? [Completitud]
     - [ ] CHK006 - Esta el manejo de PII explicitamente documentado? [Claridad]

     Total: 15 items a traves de 4 categorias
```

**Consejos:**
- Las listas de verificacion validan calidad de requisitos, no correccion de implementacion
- Usar para revision y mejora de requisitos
- Crear listas de verificacion especificas de dominio para validacion enfocada
- Ejecutar antes de continuar con planificacion tecnica

---

### `/codexspec.tasks-to-issues`

Convertir tareas de `tasks.md` en issues de GitHub para seguimiento de proyecto y colaboracion.

**Sintaxis:**
```
/codexspec.tasks-to-issues
```

**Argumentos:**
| Argumento | Requerido | Descripcion |
|----------|----------|-------------|
| Ninguno | - | Convierte todas las tareas de la funcionalidad actual |

**Que hace:**
- Parsea IDs de tarea, descripciones, dependencias y rutas de archivo
- Crea issues de GitHub con cuerpo estructurado
- Agrega etiquetas basadas en tipo de tarea (setup, implementation, testing, documentation)
- Vincula dependencias entre issues
- Reporta issues creados con URLs

**Requisitos Previos:**
- Repositorio Git con remote de GitHub
- GitHub CLI (`gh`) instalado y autenticado
- Archivo `tasks.md` existe

**Ejemplo:**
```text
Tu: /codexspec.tasks-to-issues

AI:  Convirtiendo tareas a issues de GitHub...

     Repositorio: github.com/example/taskman

     Creando issues:
     + #42: Task 1.1 - Setup Project Structure (setup)
     + #43: Task 2.1 - Write Tests for Task Entity (testing)
     + #44: Task 2.2 - Implement Task Entity (implementation)
     ...

     Resumen:
     - Issues creados: 24
     - Etiquetas aplicadas: setup(4), implementation(12), testing(5), documentation(3)
     - Dependencias vinculadas: 18

     Ver issues: https://github.com/example/taskman/issues
```

**Consejos:**
- Requiere autenticacion de GitHub CLI (`gh auth login`)
- Solo funciona con repositorios de GitHub
- Crea issues en la configuracion predeterminada del repositorio
- Verificar duplicados antes de ejecutar

---

### `/codexspec.commit`

Generar un mensaje de commit conforme a Conventional Commits basado en el estado de git y contexto de sesion. Este comando es consciente del contexto y maneja diferentes estados de git.

**Sintaxis:**
```
/codexspec.commit
```

**Argumentos:**
| Argumento | Requerido | Descripcion |
|----------|----------|-------------|
| Ninguno | - | Analiza estado actual de git y contexto de sesion |

**Que hace:**
- Recopila contexto git (rama, estado, cambios staged/unstaged)
- Analiza historial de conversacion de sesion para entender intencion
- Sigue logica de prioridad basada en estado de git:
  - **Existen cambios en staging**: Generar mensaje de commit solo desde cambios en staging
  - **Sin staged, pero unstaged changes**: Sugerir mensaje de commit con recordatorio de staging
  - **Sin cambios**: Reportar directorio de trabajo limpio
- Genera mensajes conformes a Conventional Commits
- Confirma con usuario antes de ejecutar commit

**Manejo de Estado de Git:**

| Estado | Comportamiento |
|-------|----------|
| Cambios en staging | Generar mensaje, confirmar, commit |
| Solo unstaged | Sugerir mensaje, recordar hacer stage, preguntar si debe hacer stage all |
| Limpio | Reportar "No se detectaron cambios" |

**Ejemplo:**
```text
Tu: /codexspec.commit

AI:  Analizando contexto git...

     Rama: feature/add-auth
     Staged: 2 archivos
     Unstaged: 3 archivos

     Mensaje de commit sugerido:
     feat(auth): add JWT authentication module

     - Implement token generation and validation
     - Add middleware for protected routes
     - Include unit tests for auth service

     Confirmar commit? (y/n)

Tu: y

AI:  + Committed: abc1234
```

**Consejos:**
- Mas flexible que `/codexspec.commit-staged` - maneja varios estados de git
- Considera contexto de sesion para mensajes de commit significativos
- Siempre confirma antes de hacer commit
- Para cambios unstaged, proporciona recordatorio claro de hacer stage primero

---

### `/codexspec.commit-staged`

Generar un mensaje de commit conforme a Conventional Commits basado unicamente en cambios de git en staging. Este es un comando mas simple y enfocado para cuando ya has hecho stage de tus cambios.

**Sintaxis:**
```
/codexspec.commit-staged
```

**Argumentos:**
| Argumento | Requerido | Descripcion |
|----------|----------|-------------|
| Ninguno | - | Analiza solo cambios en staging |

**Que hace:**
- Ejecuta `git diff --staged` para obtener cambios en staging
- Analiza cambios y genera mensaje de commit
- Sigue especificacion Conventional Commits
- Confirma con usuario antes de hacer commit
- Reporta error si no existen cambios en staging

**Ejemplo:**
```text
Tu: /codexspec.commit-staged

AI:  Analizando cambios en staging...

     Archivos en staging:
     - src/auth/service.py
     - tests/test_auth.py

     Mensaje de commit sugerido:
     feat(auth): implement token refresh logic

     - Add refresh token generation
     - Include token expiration handling
     - Add tests for refresh flow

     Confirmar commit? (y/n)

Tu: y

AI:  + Committed: def5678
```

**Consejos:**
- Haz stage de cambios primero con `git add`
- Solo analiza contenido en staging - ignora unstaged
- Mas simple que `/codexspec.commit` cuando sabes lo que quieres commit
- Usar `/codexspec.commit` para mensajes mas conscientes del contexto

---

## Resumen del Flujo de Trabajo

```
+--------------------------------------------------------------------------+
|                    Flujo de Trabajo de Colaboracion Humano-AI CodexSpec  |
+--------------------------------------------------------------------------+
|                                                                          |
|  1. Constitution  -->  Definir principios del proyecto                   |
|         |                         con validacion cruzada de artefactos   |
|         v                                                                |
|  2. Specify  --------->  Q&A interactivo para clarificar requisitos      |
|         |               (ningun archivo creado - control humano)         |
|         v                                                                |
|  3. Generate Spec  -->  Crear documento spec.md                          |
|         |                                                                |
|         v                                                                |
|  +==================================================================+   |
|  |  ★ PUERTA DE REVISION 1: /codexspec.review-spec ★                 |   |
|  |  Validar: Completitud, Claridad, Testeabilidad, Constitucion      |   |
|  +==================================================================+   |
|         |                                                                |
|         v                                                                |
|  4. Clarify  --------->  Resolver ambiguedades (iterativo)               |
|         |               4 categorias dirigidas, maximo 5 preguntas       |
|         v                                                                |
|  5. Spec to Plan  -->  Crear plan tecnico con:                           |
|         |               * Revision de constitucionalidad (OBLIGATORIO)   |
|         |               * Grafo de dependencia de modulos                |
|         v                                                                |
|  +==================================================================+   |
|  |  ★ PUERTA DE REVISION 2: /codexspec.review-plan ★                 |   |
|  |  Validar: Alineacion Spec, Arquitectura, Stack Tech, Fases         |   |
|  +==================================================================+   |
|         |                                                                |
|         v                                                                |
|  6. Plan to Tasks  ->  Generar tareas atomicas con:                      |
|         |               * Aplicacion TDD (pruebas antes de impl)         |
|         |               * Marcadores Paralelos [P]                       |
|         |               * Especificaciones de rutas de archivo          |
|         v                                                                |
|  +==================================================================+   |
|  |  ★ PUERTA DE REVISION 3: /codexspec.review-tasks ★                |   |
|  |  Validar: Cobertura, Cumplimiento TDD, Dependencias, Granularidad  |   |
|  +==================================================================+   |
|         |                                                                |
|         v                                                                |
|  7. Analyze  --------->  Verificacion de consistencia cruzada            |
|         |               Detectar brechas, duplicaciones, problemas const |
|         v                                                                |
|  8. Implement  -------->  Ejecutar con flujo de trabajo TDD condicional  |
|                          Codigo: Test-first | Docs/Config: Directo       |
|                                                                          |
+--------------------------------------------------------------------------+
```

**Punto Clave**: Cada puerta de revision (★) es un **punto de control humano** donde validas la salida de AI antes de invertir mas tiempo. Saltar estas puertas a menudo conduce a costoso retrabajo.

---

## Solucion de Problemas

### "Feature directory not found"

El comando no pudo localizar el directorio de funcionalidad.

**Soluciones:**
- Ejecutar `codexspec init` primero para inicializar el proyecto
- Verificar que el directorio `.codexspec/specs/` existe
- Verificar que estas en el directorio de proyecto correcto

### "No spec.md found"

El archivo de especificacion aun no existe.

**Soluciones:**
- Ejecutar `/codexspec.specify` para clarificar requisitos primero
- Luego ejecutar `/codexspec.generate-spec` para crear spec.md

### "Constitution not found"

No existe constitucion del proyecto.

**Soluciones:**
- Ejecutar `/codexspec.constitution` para crear una
- La constitucion es opcional pero recomendada para decisiones consistentes

### "Tasks file not found"

El desglose de tareas no existe.

**Soluciones:**
- Asegurarse de haber ejecutado `/codexspec.spec-to-plan` primero
- Luego ejecutar `/codexspec.plan-to-tasks` para crear tasks.md

### "GitHub CLI not authenticated"

El comando `/codexspec.tasks-to-issues` requiere autenticacion de GitHub.

**Soluciones:**
- Instalar GitHub CLI: `brew install gh` (macOS) o equivalente
- Autenticarse: `gh auth login`
- Verificar: `gh auth status`

---

## Proximos Pasos

- [Flujo de Trabajo](workflow.md) - Patrones comunes y cuando usar cada comando
- [CLI](../reference/cli.md) - Comandos de terminal para inicializacion de proyecto

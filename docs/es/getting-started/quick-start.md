# Inicio Rapido

## 1. Inicializar un Proyecto

Despues de la instalacion, crea o inicializa tu proyecto:

```bash
# Crear nuevo proyecto
codexspec init my-awesome-project

# O inicializar en el directorio actual
codexspec init . --ai claude

# Con salida en espanol
codexspec init my-project --lang es
```

## 2. Establecer Principios del Proyecto

Inicia Claude Code en el directorio del proyecto:

```bash
cd my-awesome-project
claude
```

Usa el comando constitution:

```
/codexspec:constitution Crear principios enfocados en calidad de codigo y pruebas
```

## 3. Clarificar Requisitos

Usa `/codexspec:specify` para explorar los requisitos:

```
/codexspec:specify Quiero construir una aplicacion de gestion de tareas
```

## 4. Generar Especificacion

Una vez clarificados, genera el documento de especificacion:

```
/codexspec:generate-spec
```

## 5. Revisar y Validar

**Recomendado:** Valida antes de continuar:

```
/codexspec:review-spec
```

## 6. Crear Plan Tecnico

```
/codexspec:spec-to-plan Usar Python FastAPI para el backend
```

## 7. Generar Tareas

```
/codexspec:plan-to-tasks
```

## 8. Implementar

```
/codexspec:implement-tasks
```

## Estructura del Proyecto

Despues de la inicializacion:

```
my-project/
+-- .codexspec/
|   +-- memory/
|   |   +-- constitution.md
|   +-- specs/
|   |   +-- {feature-id}/
|   |       +-- spec.md
|   |       +-- plan.md
|   |       +-- tasks.md
|   +-- scripts/
+-- .claude/
|   +-- commands/
+-- CLAUDE.md
```

## Proximos Pasos

[Guia Completa de Flujo de Trabajo](../user-guide/workflow.md)

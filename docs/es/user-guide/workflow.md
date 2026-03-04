# Flujo de Trabajo

CodexSpec estructura el desarrollo en **puntos de control revisables** con validacion humana en cada etapa.

## Resumen del Flujo de Trabajo

```
+--------------------------------------------------------------------------+
|                    Flujo de Trabajo de Colaboracion Humano-AI CodexSpec  |
+--------------------------------------------------------------------------+
|                                                                          |
|  1. Constitution  -->  Definir principios del proyecto                   |
|         |                                                                |
|         v                                                                |
|  2. Specify  --------->  Q&A interactivo para clarificar requisitos      |
|         |                                                                |
|         v                                                                |
|  3. Generate Spec  -->  Crear documento spec.md                          |
|         |                                                                |
|         v                                                                |
|  +==================================================================+   |
|  |  ★ PUERTA DE REVISION 1: /codexspec.review-spec ★                 |   |
|  +==================================================================+   |
|         |                                                                |
|         v                                                                |
|  4. Spec to Plan  -->  Crear plan tecnico                                |
|         |                                                                |
|         v                                                                |
|  +==================================================================+   |
|  |  ★ PUERTA DE REVISION 2: /codexspec.review-plan ★                 |   |
|  +==================================================================+   |
|         |                                                                |
|         v                                                                |
|  5. Plan to Tasks  ->  Generar tareas atomicas                           |
|         |                                                                |
|         v                                                                |
|  +==================================================================+   |
|  |  ★ PUERTA DE REVISION 3: /codexspec.review-tasks ★                |   |
|  +==================================================================+   |
|         |                                                                |
|         v                                                                |
|  6. Implement  ------->  Ejecutar con flujo de trabajo TDD condicional   |
|                                                                          |
+--------------------------------------------------------------------------+
```

## Por Que Importa la Revision

| Sin Revision | Con Revision |
|---------------|-------------|
| AI hace suposiciones incorrectas | El humano detecta malas interpretaciones temprano |
| Requisitos incompletos se propagan | Brechas identificadas antes de la implementacion |
| La arquitectura se desvia de la intencion | Alineacion verificada en cada etapa |
| **Resultado: Retrabajo** | **Resultado: Correcto a la primera** |

## Comandos Principales

| Etapa | Comando | Proposito |
|-------|---------|---------|
| 1 | `/codexspec.constitution` | Definir principios del proyecto |
| 2 | `/codexspec.specify` | Q&A interactivo para requisitos |
| 3 | `/codexspec.generate-spec` | Crear documento de especificacion |
| - | `/codexspec.review-spec` | ★ Validar especificacion |
| 4 | `/codexspec.spec-to-plan` | Crear plan tecnico |
| - | `/codexspec.review-plan` | ★ Validar plan |
| 5 | `/codexspec.plan-to-tasks` | Desglosar en tareas |
| - | `/codexspec.review-tasks` | ★ Validar tareas |
| 6 | `/codexspec.implement-tasks` | Ejecutar implementacion |

## Especificacion en Dos Fases

### specify vs clarify

| Aspecto | `/codexspec.specify` | `/codexspec.clarify` |
|--------|----------------------|----------------------|
| **Proposito** | Exploracion inicial | Refinamiento iterativo |
| **Cuando** | No existe spec.md | spec.md existe, necesita llenar brechas |
| **Entrada** | Tu idea inicial | spec.md existente |
| **Salida** | Ninguna (solo dialogo) | Actualiza spec.md |

## TDD Condicional

La implementacion sigue TDD condicional:

- **Tareas de codigo**: Test-first (Red -> Green -> Verify -> Refactor)
- **Tareas no testeables** (docs, config): Implementacion directa

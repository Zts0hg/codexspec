# Solución de problemas en Windows

## Comprobar la instalación

Usa PowerShell para comprobar qué ejecutable se está utilizando y si la CLI arranca. El comando de versión es `codexspec version`.

```powershell
Get-Command codexspec -All
codexspec version
codexspec check
```

## Comando no encontrado

Si falta uv, sigue su guía de instalación. Si instalaste CodexSpec con uv pero no está en `PATH`, consulta el directorio de ejecutables, actualiza la configuración del shell y abre un terminal nuevo. Reinicia también el asistente si heredó el entorno anterior. El directorio puede diferir del predeterminado; usa la ruta que indique uv.

```powershell
uv tool list
uv tool dir --bin
uv tool update-shell
```

[uv](https://docs.astral.sh/uv/getting-started/installation/) · [uv tool update-shell](https://docs.astral.sh/uv/reference/cli/#uv-tool-update-shell)

## Acceso denegado o fallo al iniciar

Un mensaje de acceso denegado no identifica por sí solo la causa. Registra el comando exacto, la ruta del ejecutable, el error y las versiones. Comprueba que el ejecutable exista, que no se esté seleccionando otra instalación y que los permisos o el software de seguridad no hayan bloqueado la ejecución. En un dispositivo administrado, sigue el procedimiento de soporte aprobado. Compara PowerShell y CMD solo para acotar las diferencias de entorno; no des por hecho que cambiar de shell resuelve la causa.

Una vez que funcione la CLI, inicializa el proyecto seleccionado con la integración deseada. Consulta la guía de instalación para conocer los requisitos previos y cómo actualizar un proyecto.

[CodexSpec](getting-started/installation.md)

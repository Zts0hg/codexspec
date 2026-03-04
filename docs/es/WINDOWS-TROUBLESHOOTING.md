# Guia de Solucion de Problemas para Windows

Esta guia ayuda a los usuarios de Windows a resolver problemas comunes al instalar y ejecutar CodexSpec.

## Problema: "spawn codexspec access denied" (OSError 5) en CMD

### Sintomas

- Ejecutar `codexspec --version` o `codexspec init` en CMD falla con "Access denied" o "spawn codexspec access denied (OSError 5)"
- Los mismos comandos funcionan correctamente en PowerShell

### Causa Raiz

Esto es causado por diferencias en como Windows CMD y PowerShell manejan las variables de entorno de usuario:

1. **Actualizacion de variable de entorno PATH**: Cuando uv instala codexspec, agrega `%USERPROFILE%\.local\bin` al PATH de usuario. PowerShell tipicamente reconoce esto inmediatamente, mientras que CMD puede no actualizar las variables de entorno hasta que se reinicie la terminal.

2. **Diferencias de creacion de procesos**: CMD usa la API CreateProcess de Windows, mientras que PowerShell usa un mecanismo diferente que puede ser mas tolerante a problemas de resolucion de rutas.

### Soluciones

#### Solucion 1: Usar PowerShell (Recomendado)

La solucion mas simple es usar PowerShell en lugar de CMD:

```powershell
# Instalar y ejecutar codexspec en PowerShell
uv tool install codexspec
codexspec --version
```

#### Solucion 2: Reiniciar CMD

Cierra todas las ventanas de CMD y abre una nueva. Esto fuerza a CMD a recargar las variables de entorno.

#### Solucion 3: Actualizar PATH Manualmente en CMD

```cmd
# Agregar el directorio bin de uv al PATH para la sesion actual
set PATH=%PATH%;%USERPROFILE%\.local\bin

# Verificar
codexspec --version
```

#### Solucion 4: Usar Ruta Completa

```cmd
# Ejecutar codexspec usando su ruta completa
%USERPROFILE%\.local\bin\codexspec.exe --version
```

#### Solucion 5: Agregar al PATH del Sistema Permanentemente

1. Abrir **Propiedades del Sistema** -> **Variables de Entorno**
2. Encontrar `Path` en **Variables de usuario** o **Variables del sistema**
3. Agregar: `%USERPROFILE%\.local\bin`
4. Hacer clic en OK y reiniciar todas las terminales

#### Solucion 6: Usar pipx en Lugar de uv tool

Si uv continua teniendo problemas, usa pipx como alternativa:

```cmd
# Instalar pipx
pip install pipx
pipx ensurepath

# Reiniciar CMD, luego instalar codexspec
pipx install codexspec

# Verificar
codexspec --version
```

## Pasos de Verificacion

Para diagnosticar el problema, ejecuta estos comandos en CMD:

```cmd
# Verificar si el directorio bin de uv esta en PATH
echo %PATH% | findstr ".local\bin"

# Verificar si el ejecutable codexspec existe
dir %USERPROFILE%\.local\bin\codexspec.*

# Intentar ejecutar con ruta completa
%USERPROFILE%\.local\bin\codexspec.exe --version
```

## Problemas Comunes

### Problema: "uv is not recognized"

**Causa**: uv no esta instalado o no esta en PATH.

**Solucion**:
```powershell
# Instalar uv usando PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Reiniciar terminal y verificar
uv --version
```

### Problema: "python is not recognized"

**Causa**: Python no esta instalado o no esta en PATH.

**Solucion**:
1. Instalar Python 3.11+ desde [python.org](https://www.python.org/downloads/)
2. Durante la instalacion, marcar "Add Python to PATH"
3. Reiniciar terminal

### Problema: Antivirus Bloqueando Ejecucion

**Sintomas**: Codexspec funciona brevemente y luego se detiene, o muestra errores intermitentes.

**Solucion**: Agregar codexspec a la lista blanca de tu antivirus:
- **Windows Defender**: Configuracion -> Actualizacion y seguridad -> Seguridad de Windows -> Proteccion contra virus y amenazas -> Administrar configuracion -> Exclusiones
- Agregar ruta: `%USERPROFILE%\.local\bin\codexspec.exe`

## Recursos Relacionados

- [uv GitHub Issue #16747](https://github.com/astral-sh/uv/issues/16747) - Problemas conocidos de permisos en Windows con uv
- [Guia de Instalacion de uv para Windows](https://docs.astral.sh/uv/getting-started/installation/)
- [Documentacion de pipx](https://pypa.github.io/pipx/) - Instalador alternativo de aplicaciones Python

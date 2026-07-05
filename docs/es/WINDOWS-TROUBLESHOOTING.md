# Guía de resolución de problemas en Windows

Esta guía ayuda a los usuarios de Windows a resolver los problemas más comunes al instalar y ejecutar CodexSpec.

## Problema: "spawn codexspec access denied" (OSError 5) en CMD

### Síntomas

- Ejecutar `codexspec --version` o `codexspec init` en CMD falla con "Access denied" o "spawn codexspec access denied (OSError 5)"
- Los mismos comandos funcionan correctamente en PowerShell

### Causa raíz

Se debe a diferencias en cómo Windows CMD y PowerShell gestionan las variables de entorno de usuario:

1. **Refresco de la variable de entorno PATH**: cuando uv instala codexspec, añade `%USERPROFILE%\.local\bin` al PATH de usuario. PowerShell normalmente lo reconoce de inmediato, mientras que CMD puede no refrescar las variables de entorno hasta que se reinicia el terminal.

2. **Diferencias en la creación de procesos**: CMD usa la API CreateProcess de Windows, mientras que PowerShell emplea un mecanismo distinto que puede tolerar mejor los problemas de resolución de rutas.

### Soluciones

#### Solución 1: usar PowerShell (recomendado)

La solución más sencilla es usar PowerShell en lugar de CMD:

```powershell
# Instalar y ejecutar codexspec en PowerShell
uv tool install codexspec
codexspec --version
```

#### Solución 2: reiniciar CMD

Cierra todas las ventanas de CMD y abre una nueva. Esto obliga a CMD a recargar las variables de entorno.

#### Solución 3: refrescar PATH manualmente en CMD

```cmd
# Añade el directorio bin de uv al PATH de la sesión actual
set PATH=%PATH%;%USERPROFILE%\.local\bin

# Verifica
codexspec --version
```

#### Solución 4: usar la ruta completa

```cmd
# Ejecuta codexspec usando su ruta completa
%USERPROFILE%\.local\bin\codexspec.exe --version
```

#### Solución 5: añadir al PATH del sistema de forma permanente

1. Abre **Propiedades del sistema** → **Variables de entorno**
2. Busca `Path` en **Variables de usuario** o **Variables del sistema**
3. Añade: `%USERPROFILE%\.local\bin`
4. Haz clic en Aceptar y reinicia todos los terminales

#### Solución 6: usar pipx en lugar de uv tool

Si uv sigue dando problemas, usa pipx como alternativa:

```cmd
# Instala pipx
pip install pipx
pipx ensurepath

# Reinicia CMD y luego instala codexspec
pipx install codexspec

# Verifica
codexspec --version
```

## Pasos de verificación

Para diagnosticar el problema, ejecuta estos comandos en CMD:

```cmd
# Comprueba si el directorio bin de uv está en PATH
echo %PATH% | findstr ".local\bin"

# Comprueba si existe el ejecutable de codexspec
dir %USERPROFILE%\.local\bin\codexspec.*

# Prueba a ejecutarlo con la ruta completa
%USERPROFILE%\.local\bin\codexspec.exe --version
```

## Problemas habituales

### Problema: "uv is not recognized"

**Causa**: uv no está instalado o no está en PATH.

**Solución**:

```powershell
# Instala uv con PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Reinicia el terminal y verifica
uv --version
```

### Problema: "python is not recognized"

**Causa**: Python no está instalado o no está en PATH.

**Solución**:

1. Instala Python 3.11+ desde [python.org](https://www.python.org/downloads/)
2. Durante la instalación, marca "Add Python to PATH"
3. Reinicia el terminal

### Problema: el antivirus bloquea la ejecución

**Síntomas**: codexspec funciona brevemente y luego se detiene, o muestra errores intermitentes.

**Solución**: añade codexspec a la lista de exclusiones de tu antivirus:

- **Windows Defender**: Configuración → Actualización y seguridad → Seguridad de Windows → Protección contra virus y amenazas → Administrar configuración → Exclusiones
- Añade la ruta: `%USERPROFILE%\.local\bin\codexspec.exe`

## Recursos relacionados

- [uv GitHub Issue #16747](https://github.com/astral-sh/uv/issues/16747): problemas conocidos de permisos de uv en Windows
- [Guía de instalación de uv en Windows](https://docs.astral.sh/uv/getting-started/installation/)
- [Documentación de pipx](https://pypa.github.io/pipx/): instalador alternativo de aplicaciones Python

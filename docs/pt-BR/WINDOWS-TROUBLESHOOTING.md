# Guia de solução de problemas no Windows

Este guia ajuda usuários Windows a resolver problemas comuns ao instalar e executar o CodexSpec.

## Problema: "spawn codexspec access denied" (OSError 5) no CMD

### Sintomas

- Executar `codexspec --version` ou `codexspec init` no CMD falha com "Access denied" ou "spawn codexspec access denied (OSError 5)"
- Os mesmos comandos funcionam corretamente no PowerShell

### Causa raiz

Isso é causado por diferenças em como o CMD e o PowerShell do Windows tratam as variáveis de ambiente do usuário:

1. **Atualização da variável de ambiente PATH**: quando o uv instala o codexspec, ele adiciona `%USERPROFILE%\.local\bin` ao PATH do usuário. O PowerShell tipicamente reconhece isso imediatamente, enquanto o CMD pode não atualizar as variáveis de ambiente até o terminal ser reiniciado.

2. **Diferenças na criação de processos**: o CMD usa a API Windows CreateProcess, enquanto o PowerShell usa um mecanismo diferente, que pode ser mais tolerante a problemas de resolução de caminho.

### Soluções

#### Solução 1: Usar o PowerShell (recomendado)

A solução mais simples é usar o PowerShell em vez do CMD:

```powershell
# Instalar e executar o codexspec no PowerShell
uv tool install codexspec
codexspec --version
```

#### Solução 2: Reiniciar o CMD

Feche todas as janelas do CMD e abra uma nova. Isso força o CMD a recarregar as variáveis de ambiente.

#### Solução 3: Atualizar o PATH manualmente no CMD

```cmd
# Adicionar o diretório bin do uv ao PATH para a sessão atual
set PATH=%PATH%;%USERPROFILE%\.local\bin

# Verificar
codexspec --version
```

#### Solução 4: Usar o caminho completo

```cmd
# Executar o codexspec usando seu caminho completo
%USERPROFILE%\.local\bin\codexspec.exe --version
```

#### Solução 5: Adicionar ao PATH do sistema de forma permanente

1. Abra **Propriedades do Sistema** → **Variáveis de Ambiente**
2. Encontre `Path` em **Variáveis de usuário** ou **Variáveis do sistema**
3. Adicione: `%USERPROFILE%\.local\bin`
4. Clique em OK e reinicie todos os terminais

#### Solução 6: Usar pipx em vez de uv tool

Se o uv continuar apresentando problemas, use o pipx como alternativa:

```cmd
# Instalar pipx
pip install pipx
pipx ensurepath

# Reinicie o CMD e então instale o codexspec
pipx install codexspec

# Verificar
codexspec --version
```

## Etapas de verificação

Para diagnosticar o problema, execute estes comandos no CMD:

```cmd
# Verificar se o diretório bin do uv está no PATH
echo %PATH% | findstr ".local\bin"

# Verificar se o executável codexspec existe
dir %USERPROFILE%\.local\bin\codexspec.*

# Tentar executar com o caminho completo
%USERPROFILE%\.local\bin\codexspec.exe --version
```

## Problemas comuns

### Problema: "uv is not recognized"

**Causa**: o uv não está instalado ou não está no PATH.

**Solução**:

```powershell
# Instalar o uv usando o PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Reiniciar o terminal e verificar
uv --version
```

### Problema: "python is not recognized"

**Causa**: o Python não está instalado ou não está no PATH.

**Solução**:

1. Instale o Python 3.11+ a partir de [python.org](https://www.python.org/downloads/)
2. Durante a instalação, marque "Add Python to PATH"
3. Reinicie o terminal

### Problema: antivírus bloqueando a execução

**Sintomas**: o codexspec funciona brevemente e depois para, ou mostra erros intermitentes.

**Solução**: adicione o codexspec à lista de permissões do seu antivírus:

- **Windows Defender**: Configurações → Atualização e Segurança → Segurança do Windows → Proteção contra vírus e ameaças → Gerenciar configurações → Exclusões
- Adicione o caminho: `%USERPROFILE%\.local\bin\codexspec.exe`

## Recursos relacionados

- [uv GitHub Issue #16747](https://github.com/astral-sh/uv/issues/16747) - Problemas conhecidos de permissão no Windows com o uv
- [Guia de instalação do uv no Windows](https://docs.astral.sh/uv/getting-started/installation/)
- [Documentação do pipx](https://pypa.github.io/pipx/) - Instalador alternativo de aplicações Python

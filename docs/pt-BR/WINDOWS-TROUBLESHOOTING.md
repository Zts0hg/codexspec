# Guia de Solução de Problemas para Windows

Este guia ajuda usuários Windows a resolver problemas comuns ao instalar e executar o CodexSpec.

## Problema: "spawn codexspec access denied" (OSError 5) no CMD

### Sintomas

- Executar `codexspec --version` ou `codexspec init` no CMD falha com "Access denied" ou "spawn codexspec access denied (OSError 5)"
- Os mesmos comandos funcionam corretamente no PowerShell

### Causa Raiz

Isso é causado por diferenças em como o Windows CMD e PowerShell lidam com variáveis de ambiente do usuário:

1. **Atualização da variável de ambiente PATH**: Quando uv instala o codexspec, ele adiciona `%USERPROFILE%\.local\bin` ao PATH do usuário. O PowerShell tipicamente reconhece isso imediatamente, enquanto o CMD pode não atualizar as variáveis de ambiente até que o terminal seja reiniciado.

2. **Diferenças na criação de processos**: O CMD usa a API Windows CreateProcess, enquanto o PowerShell usa um mecanismo diferente que pode ser mais tolerante a problemas de resolução de caminho.

### Soluções

#### Solução 1: Usar PowerShell (Recomendado)

A solução mais simples é usar PowerShell em vez de CMD:

```powershell
# Instalar e executar codexspec no PowerShell
uv tool install codexspec
codexspec --version
```

#### Solução 2: Reiniciar o CMD

Feche todas as janelas do CMD e abra uma nova. Isso força o CMD a recarregar as variáveis de ambiente.

#### Solução 3: Atualizar PATH Manualmente no CMD

```cmd
# Adicionar diretório bin do uv ao PATH para a sessão atual
set PATH=%PATH%;%USERPROFILE%\.local\bin

# Verificar
codexspec --version
```

#### Solução 4: Usar Caminho Completo

```cmd
# Executar codexspec usando seu caminho completo
%USERPROFILE%\.local\bin\codexspec.exe --version
```

#### Solução 5: Adicionar ao PATH do Sistema Permanentemente

1. Abra **Propriedades do Sistema** → **Variáveis de Ambiente**
2. Encontre `Path` nas **Variáveis de usuário** ou **Variáveis do sistema**
3. Adicione: `%USERPROFILE%\.local\bin`
4. Clique OK e reinicie todos os terminais

#### Solução 6: Usar pipx em Vez de uv tool

Se uv continuar com problemas, use pipx como alternativa:

```cmd
# Instalar pipx
pip install pipx
pipx ensurepath

# Reiniciar CMD, então instalar codexspec
pipx install codexspec

# Verificar
codexspec --version
```

## Passos de Verificação

Para diagnosticar o problema, execute estes comandos no CMD:

```cmd
# Verificar se o diretório bin do uv está no PATH
echo %PATH% | findstr ".local\bin"

# Verificar se o executável codexspec existe
dir %USERPROFILE%\.local\bin\codexspec.*

# Tentar executar com caminho completo
%USERPROFILE%\.local\bin\codexspec.exe --version
```

## Problemas Comuns

### Problema: "uv is not recognized"

**Causa**: uv não está instalado ou não está no PATH.

**Solução**:

```powershell
# Instalar uv usando PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Reiniciar terminal e verificar
uv --version
```

### Problema: "python is not recognized"

**Causa**: Python não está instalado ou não está no PATH.

**Solução**:

1. Instale Python 3.11+ de [python.org](https://www.python.org/downloads/)
2. Durante a instalação, marque "Add Python to PATH"
3. Reinicie o terminal

### Problema: Antivírus Bloqueando Execução

**Sintomas**: Codexspec funciona brevemente depois para, ou mostra erros intermitentes.

**Solução**: Adicione codexspec à lista de permissões do seu antivírus:

- **Windows Defender**: Configurações → Atualização e Segurança → Segurança do Windows → Proteção contra vírus e ameaças → Gerenciar configurações → Exclusões
- Adicione o caminho: `%USERPROFILE%\.local\bin\codexspec.exe`

## Recursos Relacionados

- [uv GitHub Issue #16747](https://github.com/astral-sh/uv/issues/16747) - Problemas conhecidos de permissão Windows com uv
- [Guia de Instalação do uv para Windows](https://docs.astral.sh/uv/getting-started/installation/)
- [Documentação do pipx](https://pypa.github.io/pipx/) - Instalador alternativo de aplicações Python

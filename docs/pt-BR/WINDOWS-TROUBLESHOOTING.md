# Solução de problemas no Windows

## Verificar a instalação

Use o PowerShell para conferir qual executável está sendo usado e se a CLI inicia. O comando de versão é `codexspec version`.

```powershell
Get-Command codexspec -All
codexspec version
codexspec check
```

## Comando não encontrado

Se o uv não estiver instalado, siga o guia de instalação dele. Se o CodexSpec foi instalado com uv, mas não está no `PATH`, confira o diretório dos executáveis, atualize a configuração do shell e abra um novo terminal. Reinicie também o assistente se ele herdou o ambiente anterior. O diretório pode ser diferente do padrão; use o caminho informado pelo uv.

```powershell
uv tool list
uv tool dir --bin
uv tool update-shell
```

[uv](https://docs.astral.sh/uv/getting-started/installation/) · [uv tool update-shell](https://docs.astral.sh/uv/reference/cli/#uv-tool-update-shell)

## Acesso negado ou falha ao iniciar

Uma mensagem de acesso negado, por si só, não identifica a causa. Registre o comando exato, o caminho do executável, o erro e as versões. Confira se o arquivo existe, se outra instalação está sendo selecionada no lugar dele e se permissões ou software de segurança bloquearam a execução. Em um dispositivo gerenciado, siga o processo de suporte administrativo aprovado. Compare PowerShell e CMD apenas para isolar diferenças de ambiente; não presuma que trocar de shell resolve a causa.

Quando a CLI funcionar, inicialize o projeto selecionado com a integração desejada. Consulte o guia de instalação para ver os pré-requisitos e o comportamento de atualização de projetos.

[CodexSpec](getting-started/installation.md)

# Arquitetura de scripts e instalação

## Camadas de execução e autoria

A CLI Python em `src/codexspec/` instala os modelos completos de comandos de `templates/commands/`, os modelos de documentos e os critérios de revisão compartilhados. O Claude Code recebe comandos de barra; o Codex recebe skills nativas geradas a partir das mesmas fontes. Os 28 comandos públicos seguem as mesmas regras de fluxo de trabalho nos dois ambientes.

## Instalação e contexto do projeto

`codexspec init` seleciona os scripts auxiliares da plataforma e a integração solicitada. Os recursos compartilhados ficam em `.codexspec/`, os comandos do Claude em `.claude/commands/codexspec/` e as skills do Codex em `.agents/skills/`. A CLI instalada também oferece o roteamento de espaços de trabalho e as operações auxiliares com verificações de proteção usadas pelos fluxos.

A inicialização atualiza os blocos gerenciados pelo CodexSpec nos arquivos `AGENTS.md` e `CLAUDE.md` existentes e preserva o conteúdo próprio do projeto fora desses blocos. `--force` atualiza os artefatos instalados e confirma as solicitações de atualização; ele não substitui o arquivo de contexto inteiro nem descarta configurações sem relação com a atualização. Instalar apenas a CLI não inicializa um projeto.

## Scripts auxiliares por plataforma

Projetos Unix recebem os scripts Bash de `scripts/bash/`; projetos Windows recebem os scripts PowerShell de `scripts/powershell/`. A criação de funcionalidades e as verificações de pré-requisitos identificam a funcionalidade selecionada e retornam contexto legível por máquina. `common.sh` e `common.ps1` reúnem utilitários comuns de cada plataforma; `review-context` auxilia na coleta de informações sobre o alvo da revisão. Nas duas plataformas, o runtime independente de commits é copiado de `src/codexspec/commit_runtime.py` para `.codexspec/scripts/commit-staged-helper.py`.

## Identidade das funcionalidades e compatibilidade dos artefatos

Os nomes seguem o formato `YYYY-MMDD-HHMMss-name`: um timestamp com precisão de minutos, um sufixo de dois caracteres alfanuméricos minúsculos e um nome ASCII. O nome completo identifica um espaço de trabalho; continue usando seu caminho explícito ou sua branch. Identificadores sequenciais `NNN-name` não são aceitos. A compatibilidade com funcionalidades antigas se aplica aos artefatos: se faltarem `requirements.md` ou `design.md`, os comandos informam as limitações de rastreabilidade, sem inventar uma confirmação original.

## Manutenção para colaboradores

Edite as fontes oficiais, regenere as cópias derivadas e verifique a distribuição. Comandos que usam fragmentos são escritos em `internal/command_templates/sources/`; seus arquivos completos em `templates/commands/` são gerados. Os demais modelos de comandos continuam sendo editados diretamente. Não altere manualmente as cópias instaladas do Claude ou do Codex.

O pacote inclui os modelos públicos e os dois diretórios de scripts por plataforma. As ferramentas de manutenção em `internal/`, as fontes do site em `docs/`, os testes e as fontes e imagens dos diagramas ficam fora do pacote instalado. Não amplie a inclusão de scripts para todo o diretório `scripts/`.

<a id="extension-materials"></a>

## Materiais para extensões

O repositório inclui um modelo de manifesto de extensão, um comando de exemplo
e o [Guia de desenvolvimento de extensões](https://github.com/Zts0hg/codexspec/blob/main/extensions/EXTENSION-DEVELOPMENT-GUIDE.md).
Esses materiais servem para criar extensões. A CLI atual não oferece comandos
para instalar, listar ou remover extensões e não carrega automaticamente comandos
ou hooks de `extension.yml`. Os recursos compartilhados de revisão permitem
acréscimos específicos do projeto em `.codexspec/review-code/`. A inicialização
preserva as alterações existentes nos recursos e os arquivos adicionais, a menos
que sua substituição seja solicitada.

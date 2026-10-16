<a id="installation"></a>

# Installation

<a id="install-with-the-codex-desktop-app"></a>

## Installation mit der Codex-Desktop-App

Sie können Codex direkt in der Desktop-App bitten, CodexSpec zu installieren und
Ihr Projekt einzurichten.

1. Fügen Sie in der Codex-Desktop-App ein lokales Projekt hinzu und wählen Sie den Ordner aus, in dem Sie arbeiten möchten.
2. Starten Sie in diesem Projekt einen Chat und fügen Sie die folgende Eingabe ein.
3. Falls die App um Erlaubnis zum Herunterladen oder Installieren von Abhängigkeiten bittet, genehmigen Sie die angeforderte Aktion, um fortzufahren.

```text
Please install and initialize CodexSpec in the current project.
Project: https://github.com/Zts0hg/codexspec

Complete the setup directly instead of asking me to run terminal commands.

Check the environment. If uv or Python 3.11+ is missing, install the required
tools in my user directory using their official installation instructions.
Install the latest stable release of CodexSpec.

For a new setup, initialize the current project for Codex in English:
codexspec init . --ai codex --lang en

If CodexSpec is already configured, check its version and configuration before
updating. Preserve existing requirements, project principles, user files,
and configuration settings.

Verify that the CLI works and that AGENTS.md and the CodexSpec skill files
under .agents/skills/ are installed. Explain the result and how to start
describing my requirements in plain English. If the skills are not yet
available in this chat, tell me whether to start a new chat or restart the app.
```

Für Antworten und Dokumente auf Chinesisch ersetzen Sie `--lang en` durch
`--lang zh-CN` und bitten Codex, das Ergebnis auf Chinesisch zu erklären.

Codex installiert dieselbe CLI und dieselben Projekt-Skills wie bei der unten
beschriebenen manuellen Einrichtung. Sie können anschließend beispielsweise
`$codexspec:specify I want to build a todo application` eingeben. Wie lokale Skills
erkannt und aktualisiert werden, erläutert [OpenAIs Skills-Anleitung](https://learn.chatgpt.com/docs/build-skills).

<a id="prerequisites"></a>

## Voraussetzungen

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (empfohlen) oder pip
- Der Assistent, den Sie nutzen möchten: Claude Code oder Codex
- Git für die Entwicklung mit Worktrees und für Git-Workflows

<a id="cli-installation"></a>

## CLI-Installation

```bash
uv tool install codexspec

# Or use pip
pip install codexspec

# Verify the CLI and inspect available commands
codexspec version
codexspec --help
codexspec list-commands
```

Initialisieren Sie ein neues Projekt mit `codexspec init my-project --ai claude`
oder das aktuelle Verzeichnis mit `codexspec init . --ai codex`. Mit `--ai both`
wählen Sie beide Integrationen. Standardmäßig ist `claude` ausgewählt; für Codex
oder beide Integrationen müssen Sie den Wert explizit angeben.

<details>
<summary>Alternative Installationsmethoden</summary>

<a id="one-time-initialization"></a>

### Einmalige Initialisierung

```bash
uvx codexspec init my-project --ai claude
uvx codexspec init . --ai codex
```

Die einmalige Initialisierung installiert die Projektbefehle und die eigenständige
Laufzeitumgebung für Commits. Die Auswahl des Arbeitsbereichs über Worktrees, blueprint/auto-dev
und die manuelle Profilprüfung rufen weiterhin die CodexSpec-CLI auf. Stellen Sie
sicher, dass diese CLI für die genannten Workflows verfügbar ist.

<a id="development-versions"></a>

### Entwicklungsversionen

```bash
uv tool install git+https://github.com/Zts0hg/codexspec.git
uv tool install git+https://github.com/Zts0hg/codexspec.git@main

# Replace <tag> with the version you want
uv tool install git+https://github.com/Zts0hg/codexspec.git@<tag>
```

</details>

<details>
<summary>Installation unter Windows</summary>

Verwenden Sie PowerShell:

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
# Restart PowerShell, then:
uv tool install codexspec
codexspec version
```

Hilfe bei Problemen mit PATH oder der Installation finden Sie in der
[Anleitung zur Fehlerbehebung unter Windows](../WINDOWS-TROUBLESHOOTING.md).

</details>

<a id="upgrade-and-refresh-a-project"></a>

## CLI aktualisieren und Projektinstallation erneuern

Die Aktualisierung der CLI und die Erneuerung der installierten Projektbefehle
sind zwei separate Schritte:

```bash
uv tool install codexspec --upgrade
# Or: pip install --upgrade codexspec

# In the project you want to refresh; select its desired integration(s)
codexspec init . --force --ai both
```

Verwenden Sie `--ai claude` oder `--ai codex`, wenn Sie nur diese Integration
benötigen. `--force` erzeugt die ausgelieferten Befehle und Skripte neu und
aktualisiert die Review-Ressourcen. Es bestätigt außerdem Rückfragen zu Migration,
Befehlsaktualisierung und Einhaltung der Projektverfassung automatisch. Bestehende
Anforderungen und Projektprinzipien bleiben erhalten. In vorhandenen Kontextdateien
werden nur die verwalteten Hinweise aktualisiert; der übrige Inhalt bleibt bestehen.
Konfigurationsschlüssel, die Sie nicht explizit setzen, werden beibehalten.

Der Planungsbefehl heißt `design-to-plan`. Bei Installationsaktualisierungen wird
der alte Eintrag `spec-to-plan` entfernt; ein Alias bleibt nicht erhalten.

<a id="plugin-marketplace-installation"></a>

## Installation über den Plugin-Marktplatz

Installieren Sie das Plugin für Claude Code über dessen Marktplatz:

```text
/plugin marketplace add Zts0hg/codexspec
/plugin install codexspec@codexspec-market
/codexspec:config
```

Das Plugin stellt Befehle bereit und gibt dem Agenten zu Beginn einer Sitzung
Hinweise zur Analyse von Änderungen im Staging-Bereich und zum Heranziehen früherer
Anforderungen. Das gilt auch für fortgesetzte Sitzungen. Durch die Installation
des Plugins wird kein Projekt initialisiert. Mit `/codexspec:config` erstellen
oder ändern Sie Sprach-, Workflow- und Review-Einstellungen. Wenn Sie das
vollständige Projektgerüst benötigen, verwenden Sie die CLI-Initialisierung.

Für die direkte Commit-Vorschau und autorisierte Commits im aktuellen
Arbeitsverzeichnis genügt die mitgelieferte Laufzeitumgebung mit Python 3.11+ und Git;
eine dauerhaft installierte CodexSpec-CLI ist dafür nicht erforderlich. Die
Auswahl des Arbeitsbereichs über Worktrees, blueprint/auto-dev und die manuelle
Profilprüfung benötigen weiterhin die CLI. Der Start-Hook des Plugins setzt Git
im PATH und eine Claude-Code-Version voraus, die `args` bei Befehls-Hooks
(exec-Form) unterstützt. Die Hinweise richten sich an den Agenten; manuelle
Git-Befehle werden nicht abgefangen.

Eine ausführliche Anleitung finden Sie unter [Installation](installation.md).

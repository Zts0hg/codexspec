# CLI-Referenz

<a id="cli-commands"></a>

## CLI-Befehle

| Befehl | Zweck |
|---------|---------|
| `codexspec init` | Ein Projekt für Claude, Codex oder beide initialisieren oder die Installation erneuern |
| `codexspec check` | Installierte Werkzeuge und Abhängigkeiten prüfen |
| `codexspec version` | Versions- und Systeminformationen anzeigen |
| `codexspec config` | Projektkonfiguration anzeigen oder ändern |
| `codexspec list-commands` | Verfügbare Agentenbefehle nach Kategorie auflisten |
| `codexspec show-blueprint` | Den Blueprint des gemeinsamen Worktrees ausgeben, ohne ihn zu ändern |

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

<details>
<summary>CLI-Initialisierungsoptionen</summary>

| Option | Bedeutung |
|--------|---------|
| `PROJECT_NAME` | Name des neuen Verzeichnisses; für das aktuelle Verzeichnis `.` verwenden |
| `--here`, `-h` | Das aktuelle Verzeichnis initialisieren |
| `--ai`, `-a` | `claude`, `codex` oder `both`; Standard ist `claude` |
| `--lang`, `-l` | Die Basissprache für die Ausgabe festlegen |
| `--interaction-lang` | Die Interaktionssprache festlegen |
| `--document-lang` | Die Dokumentsprache festlegen |
| `--commit-lang` | Die Sprache für Commit-Nachrichten festlegen |
| `--force`, `-f` | Installierte Artefakte neu erzeugen und Rückfragen zu Migration, Aktualisierung und Konformität automatisch bestätigen; projektspezifische Kontextinhalte und nicht betroffene Konfiguration erhalten |
| `--no-git` | Die Initialisierung des Git-Repositorys überspringen |
| `--debug`, `-d` | Detaillierte Debug-Ausgabe anzeigen |

</details>

<details>
<summary>CLI-Konfigurationsoptionen</summary>

| Option | Bedeutung |
|--------|---------|
| `--set-lang`, `-l` | Die Basissprache für die Ausgabe festlegen |
| `--set-interaction-lang` | Die Interaktionssprache festlegen |
| `--set-document-lang` | Die Dokumentsprache festlegen |
| `--set-commit-lang`, `-c` | Die Sprache für Commit-Nachrichten festlegen |
| `--list-langs` | Unterstützte Sprachcodes auflisten |
| `--auto-next` | Automatischen Phasenübergang umschalten oder festlegen |
| `--auto-distill` | Automatische Wissenserfassung umschalten oder festlegen |
| `--auto-maintenance` | Automatische inkrementelle Wartung umschalten oder festlegen |
| `--worktrees` | Die lokal pro Checkout geltende Worktree-Isolation umschalten oder festlegen |
| `--decided-by` | Den Review-Entscheidungsmodus auf `reviewer` oder `ask` setzen |

</details>

## `codexspec show-blueprint`

Gibt die vollständige `.codexspec/blueprint.md` aus dem festen Branch `codexspec/auto-dev` und
`worktree-for-codexspec-auto-dev` unverändert auf der Standardausgabe aus. Fehlen Repository, Branch, worktree oder Datei, wird dies auf der Standardfehlerausgabe
mit einem Exit-Status ungleich null gemeldet. Der Befehl ist
schreibgeschützt und führt weder Fetch, Merge, Schreibzugriffe noch Sperren aus.

```bash
codexspec show-blueprint
```

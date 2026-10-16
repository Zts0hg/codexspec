# Skript- und Installationsarchitektur

## Laufzeit und Befehlsquellen

Die Python-CLI in `src/codexspec/` installiert vollständige Befehlsvorlagen aus `templates/commands/`, Dokumentvorlagen und gemeinsame Prüfstandards. Claude Code erhält Slash-Befehle, Codex native Skills, die aus denselben Befehlsquellen erzeugt werden. Die 28 öffentlichen Befehle folgen auf beiden Plattformen denselben Workflow-Regeln.

## Installation und Projektkontext

`codexspec init` wählt die plattformspezifischen Hilfsskripte und die gewünschte Assistentenintegration aus. Gemeinsame Ressourcen liegen unter `.codexspec/`, Claude-Befehle unter `.claude/commands/codexspec/` und Codex-Skills unter `.agents/skills/`. Die installierte CLI unterstützt außerdem das Workspace-Routing und die durch Schutzprüfungen abgesicherten Hilfsoperationen der Workflows.

Die Initialisierung aktualisiert die von CodexSpec verwalteten Blöcke in vorhandenen `AGENTS.md`- und `CLAUDE.md`-Dateien und erhält projektseitige Inhalte außerhalb dieser Blöcke. `--force` aktualisiert installierte Artefakte und bestätigt Aktualisierungsabfragen; es ersetzt weder die gesamte Kontextdatei noch entfernt es andere Konfigurationseinstellungen. Die reine CLI-Installation initialisiert noch kein Projekt.

## Plattformspezifische Hilfsskripte

Unix-Projekte erhalten die Bash-Skripte aus `scripts/bash/`, Windows-Projekte die PowerShell-Skripte aus `scripts/powershell/`. Feature-Erstellung und Vorbedingungsprüfungen ermitteln das ausgewählte Feature und liefern maschinenlesbaren Kontext zurück. `common.sh` und `common.ps1` enthalten gemeinsame Hilfsfunktionen der jeweiligen Plattform; `review-context` unterstützt die Erfassung des Prüfkontexts. Die eigenständige Commit-Laufzeit wird auf beiden Plattformen von `src/codexspec/commit_runtime.py` nach `.codexspec/scripts/commit-staged-helper.py` kopiert.

## Feature-Identität und Artefaktkompatibilität

Feature-Namen folgen dem Format `YYYY-MMDD-HHMMss-name`: ein minutengenauer Zeitstempel, zwei Kleinbuchstaben oder Ziffern als Suffix und ein ASCII-Name. Der vollständige Feature-Name identifiziert einen Workspace; setzen Sie die Arbeit über dessen expliziten Pfad oder Branch fort. Fortlaufende `NNN-name`-Kennungen werden nicht unterstützt. Die Kompatibilität mit älteren Features betrifft die Artefakte: Fehlen `requirements.md` oder `design.md`, legen die Befehle die daraus entstehenden Grenzen der Rückverfolgbarkeit offen, statt eine ursprüngliche Bestätigung zu erfinden.

## Wartung für Mitwirkende

Bearbeiten Sie die maßgeblichen Quellen, erzeugen Sie die abgeleiteten Kopien neu und prüfen Sie die Distribution. Befehle mit Fragmenten werden unter `internal/command_templates/sources/` verfasst; die vollständigen Dateien unter `templates/commands/` werden daraus erzeugt. Andere Befehlsvorlagen werden weiterhin direkt bearbeitet. Ändern Sie installierte Claude- oder Codex-Kopien nicht von Hand.

Das Paket enthält öffentliche Vorlagen und die beiden plattformspezifischen Skriptverzeichnisse. Wartungswerkzeuge in `internal/`, Website-Quellen in `docs/`, Tests sowie Quellen und Bilder der Workflow-Diagramme bleiben außerhalb des installierten Pakets. Erweitern Sie die Skripteinbindung nicht auf das gesamte Verzeichnis `scripts/`.

<a id="extension-materials"></a>

## Materialien für Erweiterungen

Das Repository enthält eine Vorlage für ein Erweiterungsmanifest, einen
Beispielbefehl und eine [Entwicklungsanleitung für Erweiterungen](https://github.com/Zts0hg/codexspec/blob/main/extensions/EXTENSION-DEVELOPMENT-GUIDE.md).
Diese Materialien dienen der Erstellung von Erweiterungen. Die aktuelle CLI
bietet keine Befehle zum Installieren, Auflisten oder Entfernen von Erweiterungen
und lädt Befehle oder Hooks aus `extension.yml` nicht automatisch. Die gemeinsamen
Review-Ressourcen erlauben projektspezifische Ergänzungen unter
`.codexspec/review-code/`. Die Initialisierung bewahrt bestehende Änderungen an
Ressourcen und zusätzliche Dateien, sofern keine Ersetzung angefordert wird.

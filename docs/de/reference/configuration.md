<a id="configuration-and-internationalization"></a>

# Konfiguration und Internationalisierung

Die Konfiguration liegt in `.codexspec/config.yml`. Vorlagen bleiben auf Englisch;
Agenten verfassen Dialogtexte und erzeugte Artefakte in den konfigurierten
Sprachen. Die 13 Standard-Sprachcodes sind `en`, `zh-CN`, `zh-TW`, `ja`, `ko`,
`es`, `fr`, `de`, `pt`, `ru`, `it`, `ar` und `hi`.
Für Portugiesisch verwendet die CLI `pt`; lokalisierte Dokumentation und
Übersetzungskataloge verwenden `pt-BR`.

<a id="language-dimensions"></a>

## Sprachdimensionen

| Dimension | Konfigurationsschlüssel | Bei der Initialisierung | Später festlegen | Steuert |
|-----------|------------|-------------------|-----------|----------|
| Ausgabe/Basis | `language.output` | `--lang` | `config --set-lang` | Ersatzwert für die anderen Sprachdimensionen |
| Interaktion | `language.interaction` | `--interaction-lang` | `config --set-interaction-lang` | Gespräche und CLI-Ausgabe |
| Dokument | `language.document` | `--document-lang` | `config --set-document-lang` | Anforderungen, Spezifikationen, Entwürfe, Pläne und Aufgaben |
| Commit | `language.commit` | `--commit-lang` | `config --set-commit-lang` | Commit-Nachrichten und Texte aus den Git-Workflows |

Ist für eine Dimension keine spezifische Sprache gesetzt, wird unabhängig von
den anderen Dimensionen `language.output` verwendet. Ist auch dieser Wert nicht
gesetzt, gilt `en`. `language.templates` bleibt `en`.

```bash
codexspec init my-project --ai both \
  --interaction-lang zh-CN --document-lang en --commit-lang en

codexspec config
codexspec config --set-document-lang en
codexspec config --list-langs
```

Bei der erstmaligen Initialisierung mit TTY wird die Basissprache abgefragt,
sofern Sie weder `--lang` noch alle drei spezifischen Sprachoptionen angeben.
`--force` bestätigt andere Initialisierungsrückfragen automatisch, unterdrückt
aber diese Sprachauswahl nicht. Ohne TTY wird standardmäßig Englisch verwendet.
Bei erneuter Initialisierung bleiben Sprachschlüssel erhalten, die Sie nicht
explizit setzen.

<a id="workflow-and-review-settings"></a>

## Workflow- und Review-Einstellungen

| Einstellung | Standard | Wirkung | CLI-Steuerung |
|---------|---------|--------|-------------|
| `workflow.auto_next` | `false` | Nach bestandenen regulären SDD-Phasen zur nächsten Phase wechseln | `config --auto-next on\|off` |
| `workflow.auto_distill` | `true` | Wissen nach erfolgreichem Abschluss ohne Interaktion erfassen | `config --auto-distill on\|off` |
| `workflow.auto_maintenance` | `true` | Bei automatischen Korrekturen verifizierte inkrementelle Wartungsverbesserungen umsetzen | `config --auto-maintenance on\|off` |
| `workflow.worktrees` | `true` | Reguläre Features und eigenständige Wartungsarbeiten isolieren | `config --worktrees on\|off` |
| `review.decided_by` | `reviewer` | Festlegen, wer über Befunde mit Auslösern außerhalb des Einsatzkontexts des Projekts entscheidet | `config --decided-by reviewer\|ask` |

Boolesche CLI-Schalter akzeptieren `on/true/1/yes` und `off/false/0/no` unabhängig
von Groß- und Kleinschreibung und auch mit umgebenden Leerzeichen. Ein boolescher
Schalter ohne Wert kehrt den aktuellen Wert im Ziel-Checkout um. Gespeicherte
YAML-Werte sind boolesch.

Bei `review.decided_by: reviewer` entscheidet der Reviewer, welche Befunde als
Fehler anerkannt werden. Bei `ask` führt ein Auslöser außerhalb des Einsatzkontexts
zu einer ausstehenden Szenarioentscheidung. Der Benutzer entscheidet einmal, ob
der Fehler behoben oder das Szenario ausgeschlossen wird; diese bestätigte
Entscheidung bleibt für spätere Runden erhalten. Ausstehende Entscheidungen
blockieren den Abschluss. Ein einzelner `review-code`-Aufruf kann den konfigurierten
Modus mit `--decided-by` überschreiben.

Konfigurationsänderungen folgen der Auswahl des Arbeitsbereichs über Worktrees.
Eine eigenständige Änderung aus dem Haupt-Checkout erfolgt im Wartungs-Worktree
und ändert nicht sofort die wirksame Einstellung im Haupt-Checkout. Änderungen
in einem Feature-Worktree werden dort wirksam.

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

<details>
<summary>Konfigurationsbeispiel</summary>

```yaml
version: "1.0"

language:
  output: "en"
  interaction: "zh-CN"
  document: "en"
  commit: "en"
  templates: "en"

project:
  ai: "both"

workflow:
  auto_next: false
  auto_distill: true
  auto_maintenance: true
  worktrees: true

review:
  decided_by: reviewer
```

</details>

Details zum Verhalten der Sprachen und Einstellungen finden Sie unter
[Konfiguration](configuration.md) und
[Internationalisierung](../user-guide/i18n.md).

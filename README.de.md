<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="codexspec-logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="codexspec-logo-light.svg">
    <img alt="CodexSpec Logo" src="codexspec-logo-light.svg" width="420">
  </picture>
</div>

<h1 align="center">CodexSpec</h1>

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh-CN.md">中文</a> | <a href="README.ja.md">日本語</a> | <a href="README.es.md">Español</a> | <a href="README.pt-BR.md">Português</a> | <a href="README.ko.md">한국어</a> | <b>Deutsch</b> | <a href="README.fr.md">Français</a>
</p>

<p align="center">
  <a href="https://pypi.org/project/codexspec/"><img src="https://img.shields.io/pypi/v/codexspec.svg?style=for-the-badge" alt="PyPI version"></a>
  <a href="https://pypi.org/project/codexspec/"><img src="https://img.shields.io/pypi/pyversions/codexspec.svg?style=for-the-badge" alt="Python versions"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License: MIT"></a>
</p>

<p align="center">
  <strong>Ein Toolkit für Requirements-First SDD mit Claude Code und OpenAI Codex</strong>
</p>

CodexSpec erstellt aus bestätigten Anforderungen Spezifikationen, Entwürfe, Pläne,
Aufgaben und Implementierungen, die sich auf ihre Quellen zurückführen lassen.
Sie entscheiden, **was** entwickelt werden soll und **warum**. Der Agent erarbeitet
innerhalb dieser bestätigten Anforderungen das **Wie** und nutzt dabei
Review-Prüfpunkte und dauerhaft gespeichertes Projektwissen.

Nutzen Sie CodexSpec mit den Slash-Befehlen von Claude Code, mit Codex-Skills oder
mit beiden. Für reguläre Features werden standardmäßig separate Git-Worktrees
verwendet. Mit einem optionalen gemeinsamen Blueprint kann der Agent eine Liste
bestätigter Anforderungen autonom abarbeiten.

[📖 Dokumentation](https://zts0hg.github.io/codexspec/) | [中文文档](https://zts0hg.github.io/codexspec/zh/) | [日本語ドキュメント](https://zts0hg.github.io/codexspec/ja/) | [한국어 문서](https://zts0hg.github.io/codexspec/ko/) | [Documentación](https://zts0hg.github.io/codexspec/es/) | [Documentation](https://zts0hg.github.io/codexspec/fr/) | [Dokumentation](https://zts0hg.github.io/codexspec/de/) | [Documentação](https://zts0hg.github.io/codexspec/pt-BR/)

## Inhaltsverzeichnis

- [Warum CodexSpec?](#warum-codexspec)
- [Schnellstart in 30 Sekunden](#schnellstart-in-30-sekunden)
- [Installation](#installation)
- [Kern-Workflow](#kern-workflow)
- [Gemeinsamer Blueprint und autonome Entwicklung](#gemeinsamer-blueprint-und-autonome-entwicklung)
- [Entwicklung mit Worktrees](#entwicklung-mit-worktrees)
- [Mit bestehendem Code arbeiten](#mit-bestehendem-code-arbeiten)
- [Reviews und Debugging](#reviews-und-debugging)
- [Projektwissen](#projektwissen)
- [Git-Workflow](#git-workflow)
- [Verfügbare Befehle](#verfügbare-befehle)
- [Konfiguration und Internationalisierung](#konfiguration-und-internationalisierung)
- [Projektstruktur](#projektstruktur)
- [Materialien für Erweiterungen](#materialien-für-erweiterungen)
- [Entwicklung](#entwicklung)
- [Beiträge](#beiträge)
- [Lizenz](#lizenz)

## Warum CodexSpec?

| Bedarf | Was CodexSpec bietet |
|------|-------------------------|
| Klarer Zweck des Produkts | Explizite Bestätigung und dauerhaft gespeicherte Anforderungen in `requirements.md` vor der Spezifikation |
| Nachvollziehbare Entwicklung | Quellenverweise entlang der Kette Anforderungen → Spezifikation → Entwurf → Plan → Aufgaben |
| Überprüfbare Entscheidungen | Vier Befehle zur Prüfung von Artefakten, eine artefaktübergreifende Analyse und eine separate Codeprüfung, bei der Fehler die Freigabe verhindern |
| Kontinuität zwischen Sitzungen und im Team | Feature-Aufzeichnungen, Projektprinzipien, wiederverwendbares Wissen und relevante frühere Entscheidungen |
| Mehrere Features gleichzeitig | Ein Git-Worktree pro regulärem Feature; der zugehörige Arbeitsbereich wird zuverlässig wiederverwendet |
| Mehr Automatisierung | Optionaler automatischer Übergang zwischen Phasen und autonome Entwicklung bestätigter Blueprint-Anforderungen |
| Sprachpräferenzen im Team | Unabhängig wählbare Sprachen für Interaktion, Dokumente und Commits |

### Was ist Requirements-First SDD?

Bei Requirements-First Spec-Driven Development sind **bestätigte Anforderungen
für ein Feature die maßgebliche Grundlage mit der höchsten Priorität**. Bevor der
Agent daraus Implementierungsartefakte ableitet, hält er Ziele, Einschränkungen,
Entscheidungen, Ausschlüsse, offene Fragen und die Belege für die Bestätigung fest.

```text
Idea → Confirmed Requirements → Spec → Design → Plan → Tasks → Code
```

In der Zusammenarbeit mit Menschen wird festgelegt und geändert, was das Produkt
leisten soll. Automatische Reviews prüfen die abgeleiteten Artefakte anhand dieser
Vorgaben. Wird die Automatisierung aktiviert, setzt sie die Arbeit nach erfolgreich
geprüften Phasen fort. Sie berechtigt den Agenten nicht, bestätigte Anforderungen
stillschweigend zu ersetzen.

## Schnellstart in 30 Sekunden

Installieren Sie CodexSpec und initialisieren Sie das Projekt für den Assistenten,
den Sie verwenden:

```bash
uv tool install codexspec

# Create a new project for Claude Code
codexspec init my-project --ai claude

# Or initialize an existing project for Codex
cd your-existing-project
codexspec init . --ai codex

# Use --ai both when you want both integrations
```

Starten Sie den installierten Assistenten im initialisierten Projekt. Je nach
Assistent wird derselbe Workflow auf eine der folgenden Arten aufgerufen:

| Assistent | Anforderungsermittlung starten |
|-----------|------------------------------|
| Claude Code (`claude`) | `/codexspec:specify I want to build a todo application` |
| Codex (`codex`) | `$codexspec:specify I want to build a todo application` |

Passen Sie die Projektprinzipien bei Bedarf mit `constitution` an. Bestätigen Sie
die abschließende Zusammenfassung der Anforderungen. Arbeiten Sie anschließend
im zurückgegebenen Feature-Verzeichnis und Arbeitsbereich weiter. Die weiteren
Befehle finden Sie unter [Kern-Workflow](#kern-workflow).

Wenn Sie die Codex-Desktop-App verwenden, können Sie [Codex mit der Installation und Initialisierung Ihres Projekts beauftragen](#installation-mit-der-codex-desktop-app).

## Installation

### Installation mit der Codex-Desktop-App

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

### Voraussetzungen

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (empfohlen) oder pip
- Der Assistent, den Sie nutzen möchten: Claude Code oder Codex
- Git für die Entwicklung mit Worktrees und für Git-Workflows

### CLI-Installation

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

#### Einmalige Initialisierung

```bash
uvx codexspec init my-project --ai claude
uvx codexspec init . --ai codex
```

Die einmalige Initialisierung installiert die Projektbefehle und die eigenständige
Laufzeitumgebung für Commits. Die Auswahl des Arbeitsbereichs über Worktrees, blueprint/auto-dev
und die manuelle Profilprüfung rufen weiterhin die CodexSpec-CLI auf. Stellen Sie
sicher, dass diese CLI für die genannten Workflows verfügbar ist.

#### Entwicklungsversionen

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
[Anleitung zur Fehlerbehebung unter Windows](docs/en/WINDOWS-TROUBLESHOOTING.md).

</details>

### CLI aktualisieren und Projektinstallation erneuern

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

### Installation über den Plugin-Marktplatz

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

Eine ausführliche Anleitung finden Sie unter [Installation](docs/en/getting-started/installation.md).

## Kern-Workflow

Der Standard-Workflow für Features bewahrt eine durch Quellenverweise verknüpfte Kette:

```text
/specify          → requirements.md
/generate-spec    → spec.md       → review-spec
/spec-to-design   → design.md     → review-design
/design-to-plan   → plan.md       → review-plan
/plan-to-tasks    → tasks.md      → review-tasks → analyze
/implement-tasks  → implementation and complete-feature code review
```

Die folgenden Beispiele verwenden Claudes Präfix `/codexspec:`. Verwenden Sie in
Codex `$codexspec:` mit demselben Befehlsnamen und denselben Argumenten.

| Schritt | Befehl | Zweck und Ergebnis |
|------|---------|--------------------|
| Projektprinzipien | `/codexspec:constitution` | `constitution.md` erstellen oder aktualisieren und betroffene Artefakte validieren |
| Anforderungen | `/codexspec:specify <idea>` | Zielsetzung besprechen, die abschließende Zusammenfassung bestätigen und `requirements.md` dauerhaft speichern |
| Spezifikation | `/codexspec:generate-spec <feature-dir>` | Bestätigte Anforderungen mit Quellenverweisen in `spec.md` überführen |
| Systementwurf | `/codexspec:spec-to-design <feature-dir>` | `design.md` mit Komponenten, Schnittstellen und wesentlichen Entwurfsentscheidungen erstellen |
| Implementierungsplan | `/codexspec:design-to-plan <feature-dir>` | `plan.md` mit Phasen, Reihenfolge und Verifikation erstellen |
| Aufgaben | `/codexspec:plan-to-tasks <feature-dir>` | Nachvollziehbare, überprüfbare Aufgaben in `tasks.md` erstellen und die artefaktübergreifende Analyse ausführen |
| Implementierung | `/codexspec:implement-tasks <feature-dir>` | Aufgaben ausführen, Ergebnisse verifizieren und unabhängig bestätigte Review-Befunde beheben |

Ersetzen Sie `<feature-dir>` durch das Feature-Verzeichnis, das bei der
Anforderungsermittlung zurückgegeben wurde. Arbeiten Sie in dessen Worktree
weiter oder geben Sie seinen expliziten Pfad an. So beziehen sich alle Befehle
und Sitzungen weiterhin auf dasselbe Feature.

### specify, clarify und analyze

- **specify** beginnt die Anforderungsermittlung oder nimmt sie wieder auf. Erst
  die explizite Bestätigung macht die Zusammenfassung der Anforderungen verbindlich.
- **clarify** klärt Mehrdeutigkeiten in vorhandenen Anforderungen und der
  Spezifikation. Pro Aufruf werden bis zu fünf Fragen aus vier Kategorien gestellt.
  Zuerst wird `requirements.md` aktualisiert, anschließend `spec.md` synchronisiert.
- **analyze** prüft die gesamte Kette Anforderungen → Spezifikation → Entwurf →
  Plan → Aufgaben. Es korrigiert nachgelagerte Artefakte automatisch, wenn sich
  die Korrektur eindeutig aus den maßgeblichen vorgelagerten Quellen ergibt.
  `requirements.md` wird niemals bearbeitet. Ungelöste Befunde werden gemeldet.
  Die Analyse läuft automatisch nach einem bestandenen Aufgaben-Review und dient
  der Information; sie ist kein Freigabekriterium für die Implementierung.

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

### Kleine Änderungen mit Quick

Nutzen Sie `quick` für kleine, klar abgegrenzte Änderungen, etwa eine punktuelle Korrektur:

```text
/codexspec:quick Fix the empty-state message on the task list
```

Quick bestätigt und speichert eine kompakte Zusammenfassung der Anforderungen.
Danach koordiniert es Spezifikation, Planung, Aufgaben und Implementierung
mitsamt den Reviews der Generierungsbefehle. Umfangreiche Änderungen oder noch
offene Produkt- und Entwurfsentscheidungen erfordern den Standard-Workflow.
Quick pausiert, sobald eine neue Entscheidung benötigt wird.

### Workflow-Automatisierung

`workflow.auto_next` ist standardmäßig **false**. Steht es in der Konfiguration
des aktiven Arbeitsbereichs auf `true`, folgt auf die abschließende Bestätigung
der Anforderungen automatisch die Spezifikation. Jede Generierungsphase führt
nach `PASS` oder `PASS_WITH_WARNINGS` zur nächsten Phase. `NEEDS_REVISION` oder
`BLOCKED` hält die Kette an. Mit `implement-tasks` endet sie.

Artefakte werden automatisch nur bei verifizierten Fehlern korrigiert, deren
Behebung sich aus vorgelagerten Belegen ergibt. Dafür sind höchstens zwei
Korrektur- und Review-Runden vorgesehen. Empfehlungen werden separat behandelt.
Für die Review- und Korrekturschleife der Implementierung gelten eigene
Abschlussregeln, die weiter unten beschrieben sind.

Die genauen Regeln finden Sie in der [Workflow-Anleitung](docs/en/user-guide/workflow.md).

## Gemeinsamer Blueprint und autonome Entwicklung

Mit `blueprint` bereiten Sie mehrere bestätigte Anforderungen vor der Entwicklung
vor. Mit `auto-dev` lassen Sie diese Liste abarbeiten:

```text
/codexspec:blueprint Add a confirmed requirement for task reminders
/codexspec:auto-dev
```

Bei der Anforderungsermittlung für den Blueprint werden Richtung, Entscheidungen
und Einschränkungen, die der Benutzer festlegen muss, geklärt, bevor eine
Anforderung in die Liste aufgenommen wird. Die gemeinsame Datei
`.codexspec/blueprint.md` verwendet die Zustände `pending`, `in_progress` und
`completed`. Sie können ausstehende Anforderungen anhängen, ersetzen, löschen
oder neu anordnen. Aktive und abgeschlossene Einträge sind bei der
Blueprint-Pflege schreibgeschützt.

Auto-dev folgt der Reihenfolge im Dokument. Es setzt ein bereits begonnenes
Feature fort, bevor es ein weiteres beginnt, und liest die Liste nach jedem
Abschluss erneut. So können auch neu angehängte ausstehende Anforderungen in den
laufenden Durchgang aufgenommen werden. Es führt SDD-Phasen, Implementierung,
Verifikation, Reviews und Korrekturen innerhalb der bestätigten Anforderungen
aus. Ein Aufruf von `auto-dev` aktiviert diese Automatisierung unabhängig von
`workflow.auto_next`, ohne diese Einstellung zu ändern.

Beide Befehle nutzen `worktree-for-codexspec-auto-dev` auf dem Branch
`codexspec/auto-dev`. Unter den gemeinsamen Regeln zur Zuständigkeit und zum
Schreibschutz können sie gleichzeitig arbeiten. Die Anforderungen werden in
diesem Arbeitsbereich nacheinander entwickelt. Lässt sich eine Produktentscheidung
nicht aus den bestätigten Anforderungen ableiten, wird der Durchgang mit
entsprechenden Belegen angehalten. Während der normalen autonomen Ausführung
werden dazu keine Rückfragen gestellt.

Zeigen Sie den aktuellen gemeinsamen Blueprint an, ohne ihn zu ändern:

```bash
codexspec show-blueprint
```

## Entwicklung mit Worktrees

Ein Git-Worktree ist ein weiteres Arbeitsverzeichnis desselben Repositorys, in
dem ein eigener Branch ausgecheckt ist. CodexSpec nutzt standardmäßig einen
Worktree pro regulärem Feature. Er wird vor dem ersten Speichern von Anforderungen
angelegt und enthält sämtliche Dokumente, Implementierung, Tests und Korrekturen
des Features.

```text
projects/
├── my-project/
└── my-project-codexspec-worktrees/
    ├── <feature-id>-task-reminders/
    ├── <feature-id>-search/
    ├── worktree-for-codexspec-maintenance/
    └── worktree-for-codexspec-auto-dev/
```

Wenn Sie ein Feature fortsetzen, wird dessen Arbeitsbereich wiederverwendet.
Eigenständige Änderungen an Konfiguration, Projektverfassung und Profil erfolgen
im Wartungs-Worktree. Änderungen innerhalb eines aktiven Features bleiben in
dessen Worktree. Die Konfiguration gilt **lokal pro Checkout**: Eine Einstellung,
die in einem zugewiesenen Worktree geändert wird, wirkt zunächst dort und gelangt
über die Git-Integration in andere Checkouts. Führen Sie CLI-Befehle und Prüfungen
im zurückgegebenen Arbeitsbereich aus.

Für die Ausgangsbasis neuer Features wird der bereits in Commits gespeicherte
Verlauf des lokalen Hauptbranches mit dem abgerufenen Verlauf des entfernten
Hauptbranches anhand der Git-Abstammung verglichen. Bei auseinanderlaufenden
Verläufen erfolgt im neuen Worktree ein Merge, der verifiziert werden muss.
Schlägt der Abruf fehl, wird eine Warnung ausgegeben; lokal verfügbare Referenzen
dürfen dann verwendet werden. Schlägt die Erstellung fehl, wird nicht ersatzweise
in den Haupt-Checkout geschrieben.

`workflow.worktrees` ist standardmäßig **true**. Nur der wörtliche YAML-Wert
`false` deaktiviert die Isolation regulärer Features und Wartungsarbeiten.
Blueprint/auto-dev behalten unabhängig davon ihren festen gemeinsamen Worktree.
Initialisierung und Installationsaktualisierungen erfolgen in dem Checkout, den
Sie explizit auswählen. Abgeschlossene Worktrees bleiben erhalten; durch den
Abschluss werden sie weder automatisch zusammengeführt noch gelöscht.

Siehe [Entwicklung mit Worktrees](docs/en/user-guide/workflow.md#worktree-development)
und [Konfiguration](docs/en/reference/configuration.md#workflowworktrees).

## Mit bestehendem Code arbeiten

Für unterschiedliche Ziele gibt es zwei Einstiegspunkte:

| Befehl | Zweck | Ergebnis und Grenzen |
|---------|-----------|-----------------|
| `onboard [path]` | Wiederverwendbares Projektwissen aus einer bestehenden Codebasis aufbauen | Konventionseinträge mit Kandidatenstatus und nur eng gefasste und durch konkrete Belege gestützte Einschränkungen im Profil; der Code bleibt schreibgeschützt |
| `reverse-spec [path]` | Die vorhandene Architektur verstehen oder Code mit der bestätigten Zielsetzung vergleichen | Artefakte als Entwurf oder ein Abweichungsbericht; der Code bleibt schreibgeschützt |

```text
/codexspec:onboard src/
/codexspec:reverse-spec
/codexspec:reverse-spec src/auth
```

Onboard leitet Konventionen aus dem beobachtbaren Code ab und schlägt
Einschränkungen ausschließlich auf Grundlage expliziter Verbote vor.
Konventionseinträge mit Kandidatenstatus werden lokal sofort wirksam. Bei
Einschränkungen mit Kandidatenstatus ist in der Sitzung eine Entscheidung nötig:
speichern, bearbeiten oder verwerfen. Onboard bewahrt vorhandenes Wissen und
erfindet bei einer erstmaligen Untersuchung weder Begründungen früherer
Entscheidungen noch Erfahrungswissen über Fallstricke.

Reverse-spec bietet drei Modi:

- **Überblick**: Ohne Pfad oder bei Angabe des Repository-Stammverzeichnisses
  erstellt es einen knappen Architekturentwurf in `design.md` sowie `slices.md`
  zur Auswahl der zu untersuchenden Module.
- **Generieren**: Bei einem Modulpfad ohne bestätigte Ausgangsbasis entstehen
  Entwürfe von `spec.md`, `design.md` und offene oder abgeleitete Anforderungen.
- **Abgleichen**: Bei einem Modul mit bestätigter Ausgangsbasis entsteht
  `reconcile.md`. Es meldet undokumentiertes Verhalten, nicht implementierte
  Spezifikationen und semantische Abweichungen von der bestätigten Spezifikation
  und dem bestätigten Entwurf. Die Anforderungen bestimmen dabei die Zielsetzung.

Abgeleitete Entwürfe müssen von einem Menschen bestätigt werden, bevor sie als
Ausgangsbasis dienen können. Der Abgleich nennt die vorgeschlagene Vorgehensweise:
Code korrigieren, Dokumente aktualisieren oder die Zielsetzung klären. Er setzt
sie nicht automatisch um.

## Reviews und Debugging

Vier Artefakt-Reviewer prüfen Übereinstimmung mit den Vorgaben, Abdeckung,
Machbarkeit und interne Qualität: `review-spec`, `review-design`, `review-plan`
und `review-tasks`. Sie laufen nach der Generierung automatisch und lassen sich
auch manuell aufrufen. Ihre Berichte unterscheiden verifizierte Fehler von
nicht blockierenden Risikohinweisen und möglichen Verbesserungen des Entwurfs.
Sie enthalten außerdem eine Kompatibilitätsbewertung.

`review-code` bietet eine separate Fehlerprüfung für ausgewählte Änderungen als
Freigabekriterium (Defekt-Gate) sowie eine explizite Qualitätsbewertung des gesamten Codes:

```text
/codexspec:review-code --feature <feature-dir>
/codexspec:review-code --uncommitted
/codexspec:review-code --audit src/
```

Standardmäßig wird die vollständige Differenz des Feature-Branches geprüft:
Änderungen mit Commit, Änderungen im Staging-Bereich, Änderungen außerhalb des
Staging-Bereichs und nicht ignorierte unversionierte Änderungen. Sie können
explizit nur Änderungen mit Commit, Änderungen ohne Commit oder einen einzelnen
Commit als Prüfgrundlage auswählen. `--feature` ergänzt den Anforderungskontext,
ohne den Git-Prüfumfang einzuschränken. `--audit` bewertet die angegebenen Pfade
und erstellt eine beratende Bewertung statt eines Abschlussurteils.

Reviews laden gemeinsame Standards aus `.codexspec/review-code/` und wählen die
relevanten Verhaltensdimensionen sowie Prüfungen für Sprache und Framework aus.
Jeder Befund benötigt konkrete Belege, einen tatsächlich erreichbaren Auslöser,
eine Zuordnung zur ausgewählten Änderung und eine Beschreibung der Auswirkungen.
Der Reviewer meldet Fehler und belegte Wartungsempfehlungen, ohne Dateien zu
bearbeiten. Die Stelle, die die Korrektur ausführt, prüft diese Befunde unabhängig.

Bei Code-Aufgaben werden zuerst Tests geschrieben. Dokumentations- und
Konfigurationsaufgaben werden direkt umgesetzt und mit geeigneten Prüfungen
verifiziert. Nach Korrekturen kann ein inkrementelles Review die Prüfabdeckung
unveränderter Bereiche wiederverwenden. Für die endgültige Abnahme sind ein
frisches `PASS` für das vollständige Feature, vollständige Prüfabdeckung und
Verifikation sowie null anerkannte P0–P3-Fehler erforderlich. Belegte
Wartungsempfehlungen werden separat gemeldet.

`workflow.auto_maintenance` ist standardmäßig **true** und bestimmt, ob bei
Korrekturen auch verifizierte, kompatible Wartungsverbesserungen umgesetzt werden.
Wird es deaktiviert, werden diese Empfehlungen weiterhin gemeldet; Fehler müssen
weiterhin behoben und erforderliche Prüfungen weiterhin ausgeführt werden. Die
Einstellung ist unabhängig vom automatischen Phasenübergang und kein Argument
von `implement-tasks`.

Für Debugging, bei dem zuerst die Ursache untersucht wird:

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

Debug folgt der Reihenfolge Untersuchung → Musteranalyse → Prüfung einer
Einzelhypothese → Korrektur mit einem zuerst fehlschlagenden Test. Bei der
Implementierung wird diese Untersuchung hinzugezogen, wenn Korrekturen nicht
vorankommen, ein nicht trivialer Korrektheitsfehler nachvollzogen werden muss
oder Fehler derselben Ursachenklasse in mehreren Review-Runden wiederkehren.
Nach drei fehlgeschlagenen Korrekturen wird die Architektur neu bewertet.

Mit `checklist` prüfen Sie die Klarheit, Vollständigkeit und Konsistenz der Anforderungen:

```text
/codexspec:checklist Check the authentication requirements for completeness
```

Die [Befehlsreferenz](docs/en/user-guide/commands.md) erläutert die Auswahl des
Review-Umfangs, die Argumente und die Verfahren im Detail.

## Projektwissen

Das Projektprofil speichert wiederverwendbares Wissen unter `.codexspec/profile/`:

| Kategorie | Inhalt |
|----------|----------|
| `constraints/` | Explizite Verbote und feste Grenzen; zuerst lesen |
| `conventions/` | Muster, Namensgebung und featureübergreifende Hinweise |
| `pitfalls/` | Erlebte Fallstricke, Ursachen, Lösungswege und Lehren |
| `decisions/` | Wiederverwendbare Entscheidungen zur Architektur und zu featureübergreifenden Fragen |
| `strategies/` | Signale dafür, dass ein anderer Arbeitsansatz nötig ist |
| `runbooks/` | Geordnete Verfahren und Wiederherstellung nach Fehlern |

`distill` erfasst wiederverwendbares Wissen aus der Arbeit. Die Zielsetzung eines
bestimmten Features bleibt in dessen Anforderungen, Entwurf und Plan. Init
installiert in CLAUDE.md und/oder AGENTS.md Hinweise, vor inhaltlicher Arbeit alle
Einschränkungen und das relevante Wissen zu lesen. Später hinzugefügtes Wissen
kann ohne erneute Initialisierung wirksam werden. Einträge mit Kandidatenstatus
werden vorsichtig verwendet. Geprüfte Einträge setzen verifizierte Ergebnisse und
menschliche Zustimmung voraus.

```text
/codexspec:distill Capture the reusable lessons from this work
/codexspec:distill review
/codexspec:evolve
```

Ein manuelles `distill review` oder ein direktes `distill`, bei dem kein neues
Material zu erfassen ist, öffnet einen lokalen Offline-Arbeitsbereich im Browser.
Dort können Sie Einträge überarbeiten, prüfen und bestätigen, verwerfen,
zurückstellen oder zusammenführen. Anschließend können Sie das endgültige Markdown
in der Vorschau ansehen und **Alle anwenden** auswählen. Bis zur Anwendung bleiben
die Entscheidungen in einem wiederherstellbaren Entwurf gespeichert.
Konfliktprüfungen verhindern eine teilweise Anwendung oder stillschweigendes
Überschreiben. Für Umgebungen ohne Browser gibt es eine explizite textbasierte Alternative.

`workflow.auto_distill` ist standardmäßig **true** und steuert drei Abschluss-Hooks:
erfolgreiches `implement-tasks`, über `commit-staged` ausgeführte Commits und die
Generierung durch `pr`. Eine Commit-Vorschau löst keine Erfassung aus.

Die installierten Projekthinweise fordern Agenten außerdem auf, wiederverwendbares
Wissen zu erfassen, sobald es entsteht: in gewöhnlichen Gesprächen, bei Korrekturen
außerhalb von SDD und während langer `implement-tasks`-Durchgänge. Diese Hinweise
gelten unabhängig von der Einstellung für Abschluss-Hooks. Die Erfassung am
Aufgabenende dient als letzte Absicherung.

Innerhalb einer Sitzung verarbeiten wiederholte Auslöser nur neues Material.
Über Sitzungen hinweg liest `distill` das Profil und überspringt bereits erfasstes
Wissen. Gibt es nichts Wiederverwendbares mehr, endet die Erfassung ohne
Schreibvorgang. Die automatische Erfassung öffnet niemals die manuelle Prüfung,
wartet nicht auf Menschen und blockiert nicht den aufrufenden Workflow.

`evolve` wählt nur geprüftes Wissen aus, das auch außerhalb des Projekts nützlich
ist, und erstellt daraus einen Befehls- oder Skill-Entwurf. Vor einem Push oder
dem Öffnen eines Beitrags-PRs zur menschlichen Prüfung holt es explizite Zustimmung ein.

Weitere Hinweise finden Sie unter [Projektwissen](docs/en/user-guide/commands.md#codexspecdistill).

### Frühere Entscheidungen wiederverwenden

Vor inhaltlichen Urteilen zu Anforderungen, Entwurf, Implementierung, Debugging
oder Reviews wird auch die relevante Historie unter `.codexspec/specs/`
herangezogen. Das gilt für gewöhnliche Gespräche ebenso wie für SDD-Workflows.
Bevor Agenten dem Benutzer Fragen stellen, rekonstruieren sie unveränderte
Entscheidungen, spätere Ergänzungen und explizite Ersetzungen.

Ältere Anforderungen, die nicht geändert wurden, bleiben gültig. Die neueste
explizite Entscheidung des Benutzers hat immer Vorrang. Offene Vorschläge werden
nicht als bestätigte Zielsetzung behandelt. Die Recherche beschränkt sich auf die
Aufgabe; bereits ausreichender Hintergrund wird wiederverwendet. Erneuern Sie
bestehende Projektinstallationen, um diese Hinweise zu erhalten.

## Git-Workflow

```text
/codexspec:commit-staged -p
/codexspec:pr --spec <feature-dir>/spec.md
/codexspec:release-notes --from <ref> --to HEAD
/codexspec:tasks-to-issues <feature-dir>
```

- **commit-staged** analysiert den exakten Staging-Bereich und erstellt eine
  Nachricht gemäß Conventional Commits. Mit `-p` sehen Sie eine Vorschau, ohne
  einen Commit zu erstellen. Der aufrufende Workflow wählt die Dateien aus und
  übernimmt sie in den Staging-Bereich. Die autorisierte Ausführung nutzt die
  abgesicherte Laufzeitumgebung und prüft erneut, ob der tatsächlich im Commit
  gespeicherte Inhalt mit der Analyse übereinstimmt. Die Commit-Hinweise für
  Agenten gelten in gewöhnlichen Gesprächen sowie in SDD-, Blueprint- und
  auto-dev-Workflows. Die bloße Verfügbarkeit des Befehls ruft ihn weder auf noch
  autorisiert sie einen Commit.
- **pr** erstellt aus der Differenz eine strukturierte Beschreibung für einen
  GitHub-PR oder GitLab-MR. `--spec` ergänzt optional den Feature-Kontext. Dazu
  dient ein Dateipfad zu `spec.md` oder ein Name beziehungsweise Präfix eines
  Feature-Verzeichnisses, der zu dieser Datei aufgelöst wird. Standardmäßig wird
  Text zur Verwendung auf der Hosting-Plattform ausgegeben.
- **release-notes** erstellt aus dem Git-Verlauf einen Eintrag nach Keep a
  Changelog und einen Veröffentlichungstext. Der Standardabschnitt ist
  `[Unreleased]`; `--version` verwendet die angegebene Bezeichnung. Es übernimmt
  keine Dateien in den Staging-Bereich, erstellt keine Commits, erhöht keine
  Versionen, setzt keine Tags, veröffentlicht nichts und erstellt kein Release.
- **tasks-to-issues** erstellt GitHub-Issues aus bestehenden Aufgaben, einschließlich
  Abhängigkeiten und Abnahmekriterien. Es benötigt eine authentifizierte GitHub-CLI
  und prüft, ob das Issue-Repository dem konfigurierten Remote entspricht.

Für die direkte Commit-Vorschau und autorisierte Commits im aktuellen
Arbeitsverzeichnis sind Python 3.11+ und Git erforderlich. Die Laufzeitumgebung wird mit
CLI-Projekten installiert und mit dem Claude-Plugin ausgeliefert. Auch vom
Agenten erstellte Merges mit Inhaltsänderungen nutzen die Staging-Analyse.
Merges, die nur Historien verbinden, behalten die Standardnachricht von Git
bei; Baum und Eltern-Commits werden dennoch validiert. Fast-Forwards erstellen keinen Commit.

## Verfügbare Befehle

Die CLI bietet sechs öffentliche Befehle. Die Agentenintegrationen liefern
28 Befehle: Claude verwendet `/codexspec:<name>`, Codex `$codexspec:<name>`.
Der besseren Lesbarkeit halber verwenden die folgenden Tabellen Claudes Schreibweise.

### CLI-Befehle

| Befehl | Zweck |
|---------|---------|
| `codexspec init` | Ein Projekt für Claude, Codex oder beide initialisieren oder die Installation erneuern |
| `codexspec check` | Installierte Werkzeuge und Abhängigkeiten prüfen |
| `codexspec version` | Versions- und Systeminformationen anzeigen |
| `codexspec config` | Projektkonfiguration anzeigen oder ändern |
| `codexspec list-commands` | Verfügbare Agentenbefehle nach Kategorie auflisten |
| `codexspec show-blueprint` | Den Blueprint des gemeinsamen Worktrees ausgeben, ohne ihn zu ändern |

### Befehle des Kern-Workflows

| Befehl | Zweck |
|---------|---------|
| `/codexspec:constitution` | Projektprinzipien erstellen oder aktualisieren und artefaktübergreifend validieren |
| `/codexspec:specify` | Feature-Anforderungen besprechen, bestätigen und dauerhaft speichern |
| `/codexspec:blueprint` | Bestätigte, ausstehende Blueprint-Anforderungen vorbereiten oder pflegen |
| `/codexspec:generate-spec` | Bestätigte Anforderungen in eine nachvollziehbare Spezifikation überführen; automatisches Review |
| `/codexspec:spec-to-design` | Architektur, Komponenten, Schnittstellen und Entscheidungen festlegen; automatisches Review |
| `/codexspec:design-to-plan` | Implementierungsphasen, Reihenfolge und Verifikation planen; automatisches Review |
| `/codexspec:plan-to-tasks` | Überprüfbare Aufgaben erstellen, die vorgelagerte Vorgaben abdecken; automatisches Review und analyze |
| `/codexspec:implement-tasks` | Aufgaben ausführen, Ergebnisse verifizieren, prüfen und korrigieren |
| `/codexspec:auto-dev` | Bestätigte Blueprint-Anforderungen autonom in der Reihenfolge des Dokuments entwickeln |

### Befehle für Artefakt-Reviews

| Befehl | Zweck |
|---------|---------|
| `/codexspec:review-spec` | Übereinstimmung der Spezifikation mit den Vorgaben und ihre interne Qualität prüfen |
| `/codexspec:review-design` | Übereinstimmung des Entwurfs mit den Vorgaben, Machbarkeit und Eignung für die Planung prüfen |
| `/codexspec:review-plan` | Übereinstimmung des Plans mit den Vorgaben, Machbarkeit und Eignung für die Implementierung prüfen |
| `/codexspec:review-tasks` | Übereinstimmung der Aufgaben mit den Vorgaben, Abhängigkeiten, Ausführbarkeit und Verifikation prüfen |

### Anforderungen, bestehender Code und Debugging

| Befehl | Zweck |
|---------|---------|
| `/codexspec:clarify` | Mehrdeutige Anforderungen klären; zuerst die Anforderungen und dann die Spezifikation aktualisieren |
| `/codexspec:analyze` | Durchgängige Nachvollziehbarkeit prüfen und nachgelagerte Artefakte an die maßgeblichen Vorgaben anpassen |
| `/codexspec:checklist` | Eine Checkliste zur Anforderungsqualität erstellen |
| `/codexspec:tasks-to-issues` | Bestehende Aufgaben in umsetzbare GitHub-Issues überführen |
| `/codexspec:debug` | Die Ursachen untersuchen, bevor eine Korrektur vorgenommen wird |
| `/codexspec:reverse-spec` | Bestehende Architektur untersuchen, Modul-Artefakte entwerfen oder Abweichungen von der Ausgangsbasis melden |

### Befehle für Projektwissen

| Befehl | Zweck |
|---------|---------|
| `/codexspec:distill` | Wiederverwendbares Wissen erfassen oder Einträge mit Kandidatenstatus im lokalen Arbeitsbereich prüfen |
| `/codexspec:evolve` | Geprüftes Wissen in einen Entwurf für einen Upstream-Beitrag überführen |
| `/codexspec:onboard` | Aus bestehendem Code Konventionseinträge mit Kandidatenstatus und belegte Einschränkungen gewinnen |

### Git- und Code-Review-Befehle

| Befehl | Zweck |
|---------|---------|
| `/codexspec:commit-staged` | Nachrichten aus Änderungen im Staging-Bereich erstellen; Vorschau oder Ausführung eines autorisierten Commits |
| `/codexspec:pr` | Eine strukturierte PR/MR-Beschreibung erstellen |
| `/codexspec:release-notes` | Einen Changelog-Eintrag pflegen und einen Veröffentlichungstext aus dem Git-Verlauf erstellen |
| `/codexspec:review-code` | Ausgewählte Änderungen als Defekt-Gate prüfen; mit `--audit` die Codequalität in angegebenen Pfaden bewerten |

### Hilfsbefehle

| Befehl | Zweck |
|---------|---------|
| `/codexspec:config` | Projektkonfiguration interaktiv erstellen, anzeigen, ändern oder zurücksetzen |
| `/codexspec:quick` | Einen kompakten Requirements-First-SDD-Workflow für kleine Änderungen ausführen |

## Konfiguration und Internationalisierung

Die Konfiguration liegt in `.codexspec/config.yml`. Vorlagen bleiben auf Englisch;
Agenten verfassen Dialogtexte und erzeugte Artefakte in den konfigurierten
Sprachen. Die 13 Standard-Sprachcodes sind `en`, `zh-CN`, `zh-TW`, `ja`, `ko`,
`es`, `fr`, `de`, `pt`, `ru`, `it`, `ar` und `hi`.
Für Portugiesisch verwendet die CLI `pt`; lokalisierte Dokumentation und
Übersetzungskataloge verwenden `pt-BR`.

### Sprachdimensionen

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

### Workflow- und Review-Einstellungen

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
[Konfiguration](docs/en/reference/configuration.md) und
[Internationalisierung](docs/en/user-guide/i18n.md).

## Projektstruktur

Die Initialisierung installiert gemeinsame Ressourcen und die ausgewählte
Assistentenintegration:

```text
my-project/
├── .codexspec/
│   ├── config.yml
│   ├── memory/
│   │   └── constitution.md
│   ├── profile/
│   │   ├── constraints/
│   │   ├── conventions/
│   │   ├── pitfalls/
│   │   ├── decisions/
│   │   ├── strategies/
│   │   └── runbooks/
│   ├── review-code/              # Shared review standards
│   ├── specs/
│   │   └── <feature-id>-<name>/   # Added by feature workflows
│   │       ├── requirements.md
│   │       ├── spec.md
│   │       ├── design.md
│   │       ├── plan.md
│   │       ├── tasks.md
│   │       ├── review-*.md
│   │       └── checklists/       # When requested
│   ├── templates/docs/
│   └── scripts/                 # Platform helpers and commit runtime
├── .claude/commands/codexspec/   # --ai claude or both
├── .agents/skills/              # --ai codex or both
├── CLAUDE.md                    # Claude project context
└── AGENTS.md                    # Codex project context
```

Der gemeinsame Blueprint liegt im dedizierten auto-dev-Worktree. In den regulären
Checkouts gibt es keine separat bearbeitbare Kopie. Entwürfe für die manuelle
Wissensprüfung sind von Git ausgeschlossen.

## Materialien für Erweiterungen

Das Repository enthält eine Vorlage für ein Erweiterungsmanifest, einen
Beispielbefehl und eine [Entwicklungsanleitung für Erweiterungen](extensions/EXTENSION-DEVELOPMENT-GUIDE.md).
Diese Materialien dienen der Erstellung von Erweiterungen. Die aktuelle CLI
bietet keine Befehle zum Installieren, Auflisten oder Entfernen von Erweiterungen
und lädt Befehle oder Hooks aus `extension.yml` nicht automatisch. Die gemeinsamen
Review-Ressourcen erlauben projektspezifische Ergänzungen unter
`.codexspec/review-code/`. Die Initialisierung bewahrt bestehende Änderungen an
Ressourcen und zusätzliche Dateien, sofern keine Ersetzung angefordert wird.

## Entwicklung

```bash
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Development tools are an optional dependency extra
uv sync --extra dev
# For documentation builds too: uv sync --extra dev --extra docs

uv run codexspec --help
uv run pytest
uv run ruff check src/
uv build
```

Lesen Sie [CLAUDE.md](CLAUDE.md), [AGENTS.md](AGENTS.md) und
[Repository-Struktur](docs/internal/repository-layout.md), bevor Sie Vorlagen,
Paketierung oder Initialisierung ändern. Ausgelieferte Kopien von Befehlen und
Skills sind generierte Installationsartefakte. Bearbeiten Sie ihre maßgeblichen
Quellen und erzeugen Sie die Kopien erneut.

## Beiträge

Die [Beitragsanleitung](docs/en/development/contributing.md) erläutert die lokale
Einrichtung und das Vorgehen bei Beiträgen. Beiträge sollten bestätigte
Anforderungen, die Rückverfolgbarkeit zu den Quellen und die Paketierungsgrenze
zwischen Benutzer- und Maintainer-Inhalten bewahren.

## Lizenz

MIT — siehe [LICENSE](LICENSE).

## Danksagungen

Inspiriert von [GitHub spec-kit](https://github.com/github/spec-kit).
Bietet Integrationen für Claude Code und OpenAI Codex.

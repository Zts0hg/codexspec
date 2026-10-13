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
  <strong>Ein Requirements-First-SDD-Werkzeugkasten für Claude Code und OpenAI Codex</strong>
</p>

CodexSpec überführt bestätigte Anforderungen in nachvollziehbare Spezifikationen,
Entwürfe, Pläne, Aufgaben und Implementierungen. Sie entscheiden, **was** gebaut
werden soll und **warum**; der Agent entwickelt das **Wie** innerhalb dieser
bestätigten Anforderungen, mit Review-Prüfpunkten und dauerhaftem Projektwissen.

Nutzen Sie CodexSpec über Slash-Befehle in Claude Code, Codex-Skills oder beides.
Gewöhnliche Features verwenden standardmäßig separate Git-Worktrees. Ein optionaler
gemeinsamer Blueprint ermöglicht es dem Agenten, eine Warteschlange bestätigter
Anforderungen autonom abzuarbeiten.

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
- [Beitragen](#beitragen)
- [Lizenz](#lizenz)

## Warum CodexSpec?

| Bedarf | Was CodexSpec bietet |
|------|-------------------------|
| Klare Produktabsicht | Explizite Bestätigung und eine dauerhaft gespeicherte `requirements.md` vor der Spezifikation |
| Nachvollziehbare Entwicklung | Quellenverweise entlang Anforderungen → Spezifikation → Entwurf → Plan → Aufgaben |
| Überprüfbare Entscheidungen | Vier Befehle für Artefakt-Reviews, artefaktübergreifende Analyse und eine separate Fehlerprüfung für Code als Freigabekriterium |
| Kontinuität über Sitzungen und im Team | Feature-Aufzeichnungen, Projektprinzipien, wiederverwendbares Wissen und relevante frühere Entscheidungen |
| Mehrere Features in Bearbeitung | Ein Git-Worktree pro gewöhnlichem Feature mit verlässlicher Wiederverwendung des Arbeitsbereichs |
| Mehr Automatisierung | Optionales Fortschreiten zwischen Phasen und autonome Entwicklung bestätigter Blueprint-Anforderungen |
| Sprachpräferenzen im Team | Unabhängige Sprachen für Interaktion, Dokumente und Commits |

### Was ist Requirements-First SDD?

Requirements-First Spec-Driven Development macht **bestätigte Anforderungen zur
höchsten maßgeblichen Instanz für ein Feature**. Der Agent dokumentiert Ziele,
Einschränkungen, Entscheidungen, Ausschlüsse, offene Fragen und Bestätigungsbelege,
bevor er die Implementierungsartefakte daraus ableitet.

```text
Idea → Confirmed Requirements → Spec → Design → Plan → Tasks → Code
```

Die Zusammenarbeit mit Menschen legt die Produktabsicht fest und ändert sie.
Automatische Reviews prüfen abgeleitete Artefakte dagegen. Aktivierte Automatisierung
führt die Arbeit durch erfolgreich geprüfte Phasen weiter; sie erlaubt dem Agenten
nicht, bestätigte Anforderungen stillschweigend zu ersetzen.

## Schnellstart in 30 Sekunden

Installieren Sie CodexSpec und initialisieren Sie das Projekt für Ihren Assistenten:

```bash
uv tool install codexspec

# Create a new project for Claude Code
codexspec init my-project --ai claude

# Or initialize an existing project for Codex
cd your-existing-project
codexspec init . --ai codex

# Use --ai both when you want both integrations
```

Starten Sie Ihren installierten Assistenten im initialisierten Projekt.
Derselbe Workflow verwendet diese beiden Aufrufformen:

| Assistent | Anforderungsermittlung starten |
|-----------|------------------------------|
| Claude Code (`claude`) | `/codexspec:specify I want to build a todo application` |
| Codex (`codex`) | `$codexspec:specify I want to build a todo application` |

Passen Sie die Projektprinzipien bei Bedarf mit `constitution` an. Bestätigen Sie
die abschließende Anforderungszusammenfassung und arbeiten Sie dann mit dem
zurückgegebenen Feature-Verzeichnis und Arbeitsbereich weiter. Die übrigen Befehle
finden Sie unter [Kern-Workflow](#kern-workflow).

Verwenden Sie die Codex-Desktop-App? [Bitten Sie Codex, Ihr Projekt zu installieren und zu initialisieren](#mit-der-codex-desktop-app-installieren).

## Installation

### Mit der Codex-Desktop-App installieren

Sie können Codex direkt in der Desktop-App bitten, CodexSpec zu installieren und Ihr Projekt einzurichten.

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

Für Antworten und Dokumente auf Chinesisch ersetzen Sie `--lang en` durch `--lang zh-CN` und bitten Codex, das Ergebnis auf Chinesisch zu erklären.

Codex installiert dieselbe CLI und dieselben Projekt-Skills wie die unten beschriebene manuelle Einrichtung. Sie können sie beispielsweise mit `$codexspec:specify I want to build a todo application` nutzen. Informationen zur Erkennung und Aktualisierung lokaler Skills finden Sie in [OpenAIs Skills-Anleitung](https://learn.chatgpt.com/docs/build-skills).

### Voraussetzungen

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (empfohlen) oder pip
- Der gewünschte Assistent: Claude Code oder Codex
- Git für die Entwicklung mit Worktrees und Git-Workflows

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
oder das aktuelle Verzeichnis mit `codexspec init . --ai codex`. Verwenden Sie
`--ai both` für beide Integrationen. Die Assistentenauswahl ist standardmäßig
`claude`; wählen Sie den Wert für Codex oder beide Integrationen explizit.

<details>
<summary>Alternative Installationsmethoden</summary>

#### Einmalige Initialisierung

```bash
uvx codexspec init my-project --ai claude
uvx codexspec init . --ai codex
```

Die einmalige Initialisierung installiert Projektbefehle und die eigenständige
Commit-Laufzeit. Worktree-Routing, blueprint/auto-dev und die manuelle Prüfung des
Profils rufen weiterhin die CodexSpec-CLI auf; stellen Sie diese für die genannten
Workflows bereit.

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

Hilfe bei PATH- und Installationsproblemen finden Sie in der
[Anleitung zur Fehlerbehebung unter Windows](docs/en/WINDOWS-TROUBLESHOOTING.md).

</details>

### Ein Projekt aktualisieren und seine Installation erneuern

Die CLI zu aktualisieren und die installierten Befehle eines Projekts zu erneuern sind separate Schritte:

```bash
uv tool install codexspec --upgrade
# Or: pip install --upgrade codexspec

# In the project you want to refresh; select its desired integration(s)
codexspec init . --force --ai both
```

Verwenden Sie `--ai claude` oder `--ai codex`, wenn Sie nur diese Integration
benötigen. `--force` erzeugt die ausgelieferten Befehle/Skripte neu und aktualisiert
Review-Ressourcen; außerdem bestätigt es Rückfragen zu Migration, Befehlsaktualisierung
und Einhaltung der Projektverfassung automatisch. Bestehende Anforderungen und
Projektprinzipien bleiben erhalten. Die Inhalte vorhandener Kontextdateien bleiben
bestehen, während verwaltete Hinweise aktualisiert werden. Konfigurationsschlüssel,
die Sie nicht explizit gesetzt haben, bleiben erhalten.

Der Planungsbefehl heißt `design-to-plan`; Installationsaktualisierungen entfernen
den alten Eintrag `spec-to-plan` ohne Alias.

### Installation über den Plugin-Marktplatz

Installieren Sie für Claude Code das Plugin über dessen Marktplatz:

```text
/plugin marketplace add Zts0hg/codexspec
/plugin install codexspec@codexspec-market
/codexspec:config
```

Das Plugin stellt Befehle und Hinweise zum Sitzungsbeginn für die Analyse
bereitgestellter Commits und das Heranziehen früherer Anforderungen bereit,
auch bei fortgesetzten Sitzungen. Die Plugin-Installation initialisiert kein
Projekt. Verwenden Sie `/codexspec:config`, um Sprach-, Workflow- und
Review-Einstellungen anzulegen oder zu ändern; nutzen Sie die CLI-Initialisierung,
wenn Sie das vollständige Projektgerüst benötigen.

Die direkte Commit-Vorschau und autorisierte Commits im bestehenden Arbeitsverzeichnis
können mit Python 3.11+ und Git die gebündelte Laufzeit verwenden, ohne eine dauerhaft
installierte CodexSpec-CLI. Worktree-Routing, blueprint/auto-dev und die manuelle
Profilprüfung benötigen weiterhin die CLI. Der Start-Hook des Plugins benötigt
Git im PATH und eine Claude-Code-Version, die `args` für Befehls-Hooks
(exec-Form) unterstützt. Seine Hinweise richten sich an den Agenten;
manuelle Git-Befehle fängt er nicht ab.

Details zur Einrichtung finden Sie unter [Installation](docs/en/getting-started/installation.md).

## Kern-Workflow

Der standardmäßige Feature-Workflow erhält eine Kette mit Quellenverweisen:

```text
/specify          → requirements.md
/generate-spec    → spec.md       → review-spec
/spec-to-design   → design.md     → review-design
/design-to-plan   → plan.md       → review-plan
/plan-to-tasks    → tasks.md      → review-tasks → analyze
/implement-tasks  → implementation and complete-feature code review
```

Die folgenden Beispiele verwenden Claudes Präfix `/codexspec:`. In Codex
verwenden Sie `$codexspec:` mit demselben Befehlsnamen und denselben Argumenten.

| Schritt | Befehl | Zweck und Ausgabe |
|------|---------|--------------------|
| Projektprinzipien | `/codexspec:constitution` | `constitution.md` erstellen/aktualisieren und betroffene Artefakte validieren |
| Anforderungen | `/codexspec:specify <idea>` | Absicht besprechen, eine abschließende Zusammenfassung bestätigen und `requirements.md` dauerhaft speichern |
| Spezifikation | `/codexspec:generate-spec <feature-dir>` | Bestätigte Anforderungen mit Quellenverweisen in `spec.md` überführen |
| Systementwurf | `/codexspec:spec-to-design <feature-dir>` | `design.md` erstellen: Komponenten, Schnittstellen und zentrale Entwurfsentscheidungen |
| Implementierungsplan | `/codexspec:design-to-plan <feature-dir>` | `plan.md` erstellen: Phasen, Reihenfolge und Verifikation |
| Aufgaben | `/codexspec:plan-to-tasks <feature-dir>` | Nachvollziehbare, überprüfbare `tasks.md` erstellen; artefaktübergreifende Analyse ausführen |
| Implementierung | `/codexspec:implement-tasks <feature-dir>` | Aufgaben ausführen, Ergebnisse verifizieren und unabhängig geprüfte Review-Befunde beheben |

Ersetzen Sie `<feature-dir>` durch das bei der Ermittlung zurückgegebene
Feature-Verzeichnis. Arbeiten Sie in dessen Worktree weiter oder übergeben Sie
den expliziten Pfad; so bleibt die Feature-Identität über Befehle und Sitzungen hinweg erhalten.

### specify, clarify und analyze

- **specify** startet die Anforderungsermittlung oder nimmt sie wieder auf.
  Erst eine explizite Bestätigung macht die Anforderungszusammenfassung verbindlich.
- **clarify** klärt Mehrdeutigkeiten in bestehenden Anforderungen/Spezifikationen:
  bis zu fünf Fragen pro Aufruf aus vier Kategorien. Es aktualisiert zuerst
  `requirements.md` und synchronisiert danach `spec.md`.
- **analyze** prüft die vollständige Kette Anforderungen → Spezifikation → Entwurf
  → Plan → Aufgaben. Es wendet deterministische Korrekturen automatisch auf
  nachgelagerte Artefakte an, wenn sich die Korrektur aus der maßgeblichen
  vorgelagerten Grundlage ergibt; `requirements.md` bearbeitet es niemals.
  Ungelöste Befunde werden gemeldet. Es läuft nach einem bestandenen Aufgaben-Review
  automatisch und dient der Information, nicht als Freigabekriterium für die Implementierung.

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

### Kleine Änderungen mit Quick

Verwenden Sie `quick` für eine kleine, klar begrenzte Änderung, etwa eine punktuelle Korrektur:

```text
/codexspec:quick Fix the empty-state message on the task list
```

Quick bestätigt und speichert eine kompakte Anforderungszusammenfassung und
koordiniert anschließend Spezifikation, Planung, Aufgaben und Implementierung
einschließlich der Reviews der Generierungsbefehle. Umfangreiche Änderungen oder
offene Produkt-/Entwurfsentscheidungen benötigen den Standard-Workflow;
Quick pausiert, wenn eine neue Entscheidung erforderlich ist.

### Workflow-Automatisierung

`workflow.auto_next` ist standardmäßig **false**. Ist es in der Konfiguration des
aktiven Arbeitsbereichs `true`, führt die abschließende Anforderungsbestätigung
zur Spezifikation weiter. Jede Generierungsphase geht nach `PASS` oder
`PASS_WITH_WARNINGS` weiter; `NEEDS_REVISION` oder `BLOCKED` stoppt die Kette.
`implement-tasks` ist die letzte Phase.

Automatische Artefaktkorrekturen sind auf verifizierte Fehler beschränkt, deren
Korrektur aus vorgelagerten Belegen folgt, mit höchstens zwei Korrektur- und
Review-Runden. Empfehlungen bleiben separat. Die Review-/Korrekturschleife der
Implementierung hat eigene Abschlussregeln, die unten beschrieben werden.

Die detaillierten Regeln finden Sie in der [Workflow-Anleitung](docs/en/user-guide/workflow.md).

## Gemeinsamer Blueprint und autonome Entwicklung

Verwenden Sie `blueprint`, um vor der Entwicklung mehrere bestätigte Anforderungen
vorzubereiten, und `auto-dev`, um diese Warteschlange abzuarbeiten:

```text
/codexspec:blueprint Add a confirmed requirement for task reminders
/codexspec:auto-dev
```

Die Blueprint-Ermittlung klärt die vom Benutzer zu bestimmende Richtung,
Entscheidungen und Einschränkungen, bevor eine Anforderung in die Warteschlange
aufgenommen wird. Die gemeinsame `.codexspec/blueprint.md` verwendet die Zustände
`pending`, `in_progress` und `completed`. Ausstehende Anforderungen können Sie
anhängen, ersetzen, löschen oder umordnen; aktive und abgeschlossene Einträge
sind für die Blueprint-Pflege schreibgeschützt.

Auto-dev folgt der Dokumentreihenfolge, setzt ein laufendes Feature vor dem Start
eines weiteren fort und liest die Warteschlange nach jedem Abschluss erneut,
sodass neu angehängte ausstehende Arbeit in den Lauf aufgenommen werden kann.
Es führt SDD-Phasen, Implementierung, Verifikation, Reviews und Korrekturen
innerhalb der bestätigten Anforderungen aus. Der Aufruf von `auto-dev` aktiviert
seine Automatisierung unabhängig von `workflow.auto_next` und ändert diese Einstellung nicht.

Beide Befehle teilen sich `worktree-for-codexspec-auto-dev` auf dem Branch
`codexspec/auto-dev`. Sie können unter den gemeinsamen Besitz- und Schreibschutzregeln
gleichzeitig arbeiten; Anforderungen werden in diesem Arbeitsbereich nacheinander
entwickelt. Produktentscheidungen, die sich nicht aus bestätigten Anforderungen
auflösen lassen, stoppen den Lauf mit Belegen, statt während der normalen autonomen
Ausführung Rückfragen zu stellen.

Zeigen Sie den aktuellen gemeinsamen Blueprint an, ohne ihn zu ändern:

```bash
codexspec show-blueprint
```

## Entwicklung mit Worktrees

Ein Git-Worktree ist ein weiteres Arbeitsverzeichnis desselben Repositorys mit
einem eigenen ausgecheckten Branch. CodexSpec verwendet standardmäßig eines pro
gewöhnlichem Feature, legt es vor dem ersten Schreiben von Anforderungen an und
hält die Dokumente, Implementierung, Tests und Korrekturen dieses Features zusammen.

```text
projects/
├── my-project/
└── my-project-codexspec-worktrees/
    ├── <feature-id>-task-reminders/
    ├── <feature-id>-search/
    ├── worktree-for-codexspec-maintenance/
    └── worktree-for-codexspec-auto-dev/
```

Die Fortsetzung eines Features verwendet seinen Arbeitsbereich erneut. Eigenständige
Änderungen an Konfiguration, Projektverfassung und Profil verwenden den
Wartungs-Worktree; Änderungen innerhalb eines aktiven Features bleiben dort.
Die Konfiguration gilt **lokal pro Checkout**: Eine in einem zugewiesenen Worktree
geänderte Einstellung wirkt zunächst dort und erreicht andere Checkouts durch
Git-Integration. Führen Sie CLI-Befehle und Prüfungen im zurückgegebenen Arbeitsbereich aus.

Die Ausgangsbasis neuer Features vergleicht den lokalen Verlauf mit bereits
erstellten Commits und den abgerufenen Remote-Verlauf des Hauptbranches anhand
der Git-Abstammung.
Auseinanderlaufende Verläufe werden im neuen Worktree zusammengeführt und müssen
verifiziert werden. Ein fehlgeschlagener Abruf erzeugt eine Warnung und erlaubt
lokal verfügbare Referenzen; bei Erstellungsfehlern wird nicht ersatzweise in den
Haupt-Checkout geschrieben.

`workflow.worktrees` ist standardmäßig **true**; nur der wörtliche YAML-Wert
`false` deaktiviert die Isolation gewöhnlicher Features und Wartungsarbeiten.
Blueprint/auto-dev behalten in beiden Fällen ihren festen gemeinsamen Worktree.
Initialisierung und Installationsaktualisierung arbeiten in dem Checkout, den Sie
explizit auswählen. Abgeschlossene Worktrees bleiben erhalten; der Abschluss
führt sie nicht automatisch zusammen und löscht sie nicht.

Siehe [Entwicklung mit Worktrees](docs/en/user-guide/workflow.md#worktree-development)
und [Konfiguration](docs/en/reference/configuration.md#workflowworktrees).

## Mit bestehendem Code arbeiten

Zwei Einstiegspunkte dienen unterschiedlichen Zielen:

| Befehl | Einsatzzweck | Ausgabe/Grenze |
|---------|-----------|-----------------|
| `onboard [path]` | Wiederverwendbares Projektwissen aus einer bestehenden Codebasis aufbauen | Konventionskandidaten und eng belegte Einschränkungen im Profil; der Code bleibt schreibgeschützt |
| `reverse-spec [path]` | Bestehende Architektur verstehen oder Code mit bestätigter Absicht vergleichen | Artefaktentwürfe oder ein Abweichungsbericht; der Code bleibt schreibgeschützt |

```text
/codexspec:onboard src/
/codexspec:reverse-spec
/codexspec:reverse-spec src/auth
```

Onboard leitet Konventionen aus beobachtbarem Code ab und schlägt Einschränkungen
ausschließlich aus expliziten Verboten vor. Konventionskandidaten gelten lokal
sofort; Einschränkungskandidaten erfordern in der Sitzung eine Entscheidung:
speichern, bearbeiten oder verwerfen. Es bewahrt vorhandenes Wissen und erfindet
bei einer erstmaligen Untersuchung weder Begründungen früherer Entscheidungen
noch Erfahrungswissen über Fallstricke.

Reverse-spec hat drei Modi:

- **Überblick**: Ohne Pfad oder mit dem Repository-Stamm erstellt es eine knappe
  Architektur-`design.md` und `slices.md`, um zu untersuchende Module auszuwählen.
- **Generieren**: Ein Modulpfad ohne bestätigte Ausgangsbasis führt zu Entwürfen
  für `spec.md`, `design.md` und offenen/abgeleiteten Anforderungen.
- **Abgleichen**: Ein Modul mit bestätigter Ausgangsbasis führt zu `reconcile.md`,
  das undokumentiertes Verhalten, nicht implementierte Spezifikationen und
  semantische Abweichungen von bestätigter Spezifikation/Entwurf meldet, wobei
  die Anforderungen die Absicht bestimmen.

Abgeleitete Entwürfe benötigen eine menschliche Bestätigung, bevor sie zur
Ausgangsbasis werden. Der Abgleich berichtet die vorgeschlagene Richtung —
Code korrigieren, Dokumente aktualisieren oder Absicht entscheiden — und setzt
sie nicht automatisch um.

## Reviews und Debugging

Vier Artefakt-Reviewer prüfen Übereinstimmung, Abdeckung, Machbarkeit und interne
Qualität: `review-spec`, `review-design`, `review-plan` und `review-tasks`.
Sie laufen nach der Generierung automatisch und lassen sich auch manuell aufrufen.
Berichte unterscheiden verifizierte Fehler von nicht blockierenden Risikohinweisen
und Gestaltungsmöglichkeiten und enthalten eine Kompatibilitätsbewertung.

`review-code` bietet eine separate, auf ausgewählte Änderungen begrenzte
Fehlerprüfung als Freigabekriterium (Defekt-Gate) und eine explizite Qualitätsbewertung des gesamten Codes:

```text
/codexspec:review-code --feature <feature-dir>
/codexspec:review-code --uncommitted
/codexspec:review-code --audit src/
```

Das Standard-Review umfasst die vollständige Differenz des Feature-Branches,
einschließlich in Commits gespeicherter, bereitgestellter, nicht bereitgestellter
und unversionierter, nicht ignorierter Änderungen. Sie können explizit Änderungen
mit oder ohne Commit oder einen einzelnen Commit als Beleg auswählen. `--feature` fügt Anforderungskontext hinzu,
ohne den Git-Umfang einzuschränken. `--audit` bewertet die benannten Pfade und
erstellt eine beratende Bewertung statt eines Abschlussurteils.

Reviews laden gemeinsame Standards aus `.codexspec/review-code/` und wählen
relevante Verhaltensdimensionen sowie Sprach-/Framework-Prüfungen aus.
Befunde benötigen konkrete Belege, erreichbare Auslöser, eine Zuordnung zur
ausgewählten Änderung und Auswirkungen. Der Reviewer meldet Fehler und belegte
Wartungsempfehlungen, ohne Dateien zu bearbeiten; die aufrufende Korrekturinstanz
prüft sie unabhängig.

Bei Code-Aufgaben erfolgt die Implementierung mit Tests zuerst, bei Dokumentation/
Konfiguration direkt mit geeigneten Prüfungen. Nach Korrekturen kann ein
inkrementelles erneutes Review unberührte Abdeckung wiederverwenden; die abschließende
Abnahme erfordert ein frisches `PASS` für das vollständige Feature, abgeschlossene
Abdeckung und Verifikation sowie null anerkannte P0–P3-Fehler. Belegte
Wartungsempfehlungen werden separat gemeldet.

`workflow.auto_maintenance` ist standardmäßig **true** und steuert, ob aufrufende
Korrekturinstanzen auch verifizierte, kompatible Wartungsverbesserungen anwenden.
Wenn es deaktiviert ist, werden diese Empfehlungen weiterhin gemeldet; Fehler und
erforderliche Prüfungen entfallen dadurch nicht. Es ist unabhängig vom Fortschreiten
zwischen Phasen und kein Argument von `implement-tasks`.

Für Debugging mit Ursachenanalyse zuerst:

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

Debug folgt Untersuchung → Musteranalyse → Prüfung einer einzelnen Hypothese
→ Korrektur nach einem zunächst fehlschlagenden Test. Die Implementierung eskaliert,
wenn Korrekturen feststecken, ein nicht trivialer Korrektheitsfehler nachvollzogen
werden muss oder dieselbe Ursachenklasse über Review-Runden hinweg wiederkehrt.
Drei fehlgeschlagene Korrekturen lösen eine Neubewertung der Architektur aus.

Verwenden Sie `checklist`, um Klarheit, Vollständigkeit und Konsistenz der Anforderungen zu prüfen:

```text
/codexspec:checklist Check the authentication requirements for completeness
```

Review-Auswahl, Argumente und detaillierte Verfahren finden Sie in der
[Befehlsreferenz](docs/en/user-guide/commands.md).

## Projektwissen

Das Projektprofil speichert wiederverwendbares Wissen unter `.codexspec/profile/`:

| Kategorie | Inhalt |
|----------|----------|
| `constraints/` | Explizite Verbote und feste Grenzen; zuerst lesen |
| `conventions/` | Muster, Benennung und featureübergreifende Hinweise |
| `pitfalls/` | Erlebte Fallstricke, Ursachen, Umgehungen und Lehren |
| `decisions/` | Wiederverwendbare Architektur- und featureübergreifende Entscheidungen |
| `strategies/` | Signale, die einen anderen Arbeitsansatz erfordern |
| `runbooks/` | Geordnete Verfahren und Wiederherstellung bei Fehlern |

`distill` erfasst wiederverwendbares Wissen aus der Arbeit; featurespezifische
Absicht bleibt in den Anforderungen, dem Entwurf und dem Plan des jeweiligen Features.
Init installiert Hinweise in CLAUDE.md und/oder AGENTS.md, um vor inhaltlich relevanter
Arbeit alle Einschränkungen und das einschlägige Wissen zu lesen. Später hinzugefügtes
Wissen kann ohne erneute Initialisierung wirksam werden. Kandidateneinträge werden
vorsichtig verwendet; geprüfte Einträge erfordern verifizierte Ergebnisse und
menschliche Zustimmung.

```text
/codexspec:distill Capture the reusable lessons from this work
/codexspec:distill review
/codexspec:evolve
```

Ein manuelles `distill review` oder ein direktes `distill` ohne neues zu erfassendes
Material öffnet einen lokalen Offline-Arbeitsbereich im Browser. Dort können Sie
Einträge überarbeiten, prüfen und bestätigen, verwerfen, zurückstellen und
zusammenführen, eine Vorschau des finalen Markdown ansehen und anschließend
**Alle anwenden** auswählen. Entscheidungen bleiben bis zur Anwendung in einem
wiederherstellbaren Entwurf; Konfliktprüfungen verhindern eine teilweise Anwendung
oder stillschweigendes Überschreiben. Für Umgebungen ohne Browser steht eine
explizite textbasierte Alternative zur Verfügung.

`workflow.auto_distill` ist standardmäßig **true** und steuert drei Abschluss-Hooks:
erfolgreiches `implement-tasks`, ausgeführte Commits über `commit-staged` und die
Generierung durch `pr`. Eine Commit-Vorschau löst keine Erfassung aus.

Installierte Projekthinweise fordern Agenten außerdem auf, wiederverwendbares
Wissen sofort zu erfassen, wenn es in gewöhnlichen Gesprächen, Korrekturen außerhalb
von SDD und während langer `implement-tasks`-Läufe entsteht. Diese Hinweise gelten
unabhängig von der Abschlusseinstellung; die Erfassung am Aufgabenende bietet eine
abschließende Absicherung.

Innerhalb einer Sitzung verarbeiten wiederholte Auslöser nur neues Material.
Sitzungsübergreifend liest `distill` das Profil und überspringt bereits abgedecktes
Wissen. Die Erfassung endet ohne Schreibvorgang, wenn nichts Wiederverwendbares
übrig bleibt. Automatische Erfassung öffnet niemals die manuelle Prüfung, wartet
nicht auf einen Menschen und blockiert nicht den aufrufenden Workflow.

`evolve` wählt ausschließlich geprüftes Wissen aus, das über das Projekt hinaus
nützlich ist, erstellt einen Befehls-/Skill-Entwurf und holt explizite Zustimmung
ein, bevor es pusht oder einen Beitrags-PR zur menschlichen Prüfung öffnet.

Details finden Sie unter [Projektwissen](docs/en/user-guide/commands.md#codexspecdistill).

### Frühere Entscheidungen wiederverwenden

Relevante Historie unter `.codexspec/specs/` wird ebenfalls vor inhaltlichen
Urteilen zu Anforderungen, Entwurf, Implementierung, Debugging oder Reviews
herangezogen — in gewöhnlichen Gesprächen ebenso wie in SDD-Workflows. Agenten
rekonstruieren unveränderte Entscheidungen, spätere Ergänzungen und explizite
Ersetzungen, bevor sie den Benutzer fragen.

Ältere unveränderte Anforderungen bleiben gültig. Die neueste explizite Entscheidung
des Benutzers hat immer Vorrang; offene Vorschläge gelten nicht als bestätigte
Absicht. Die Recherche bleibt auf die Aufgabe beschränkt, und ausreichender
Hintergrund wird wiederverwendet. Erneuern Sie bestehende Projektinstallationen,
um diese Hinweise zu erhalten.

## Git-Workflow

```text
/codexspec:commit-staged -p
/codexspec:pr --spec <feature-dir>/spec.md
/codexspec:release-notes --from <ref> --to HEAD
/codexspec:tasks-to-issues <feature-dir>
```

- **commit-staged** analysiert den exakten Staging-Bereich und erstellt eine
  Nachricht gemäß Conventional Commits; `-p` zeigt eine Vorschau ohne Commit.
  Der aufrufende Workflow wählt Dateien aus und stellt sie bereit. Autorisierte
  Ausführung verwendet die abgesicherte Laufzeit und prüft erneut, dass der
  im Commit gespeicherte Inhalt mit der Analyse übereinstimmt. Die Commit-Hinweise für Agenten
  gelten in gewöhnlichen Gesprächen, SDD-, Blueprint- und auto-dev-Workflows;
  die bloße Verfügbarkeit des Befehls ruft ihn weder auf noch autorisiert sie einen Commit.
- **pr** erstellt aus der Differenz eine strukturierte GitHub-PR- oder GitLab-MR-
  Beschreibung. `--spec` ergänzt optional Feature-Kontext aus einem `spec.md`-
  Dateipfad oder einem Feature-Verzeichnisnamen bzw. Präfix, das zu dieser Datei
  aufgelöst wird. Die Standardausgabe ist Text zur Verwendung auf der Hosting-Plattform.
- **release-notes** leitet einen Eintrag gemäß Keep a Changelog und einen
  Veröffentlichungstext aus dem Git-Verlauf ab. Der Standardabschnitt ist
  `[Unreleased]`; `--version` verwendet eine angegebene Bezeichnung. Es stellt
  keine Dateien bereit, erstellt keine Commits, erhöht keine Versionen, setzt
  keine Tags, veröffentlicht nichts und erstellt kein Release.
- **tasks-to-issues** erstellt GitHub-Issues aus bestehenden Aufgaben, einschließlich
  Abhängigkeiten und Abnahmekriterien. Es benötigt eine authentifizierte GitHub-CLI
  und prüft, dass das Issue-Repository mit dem konfigurierten Remote übereinstimmt.

Direkte Commit-Vorschau und autorisierte Commits im bestehenden Arbeitsverzeichnis
benötigen Python 3.11+ und Git; die Laufzeit wird mit CLI-Projekten installiert und
mit dem Claude-Plugin gebündelt. Vom Agenten erstellte Merges mit Inhaltsänderungen
verwenden ebenfalls die Staging-Analyse. Merges, die nur Historien verbinden,
behalten die Git-Standardnachricht bei und validieren Baum und Eltern; Fast-Forwards
erstellen keinen Commit.

## Verfügbare Befehle

Die CLI hat sechs öffentliche Befehle. Agentenintegrationen liefern 28 Befehle aus:
Claude verwendet `/codexspec:<name>`, Codex `$codexspec:<name>`.
Die folgenden Tabellen verwenden für bessere Lesbarkeit Claudes Schreibweise.

### CLI-Befehle

| Befehl | Zweck |
|---------|---------|
| `codexspec init` | Ein Projekt für Claude, Codex oder beide initialisieren oder erneuern |
| `codexspec check` | Installierte Werkzeuge und Abhängigkeiten prüfen |
| `codexspec version` | Versions- und Systeminformationen anzeigen |
| `codexspec config` | Projektkonfiguration anzeigen oder ändern |
| `codexspec list-commands` | Verfügbare Agentenbefehle nach Kategorie auflisten |
| `codexspec show-blueprint` | Den Blueprint des gemeinsamen Worktrees ausgeben, ohne ihn zu ändern |

### Befehle des Kern-Workflows

| Befehl | Zweck |
|---------|---------|
| `/codexspec:constitution` | Projektprinzipien erstellen/aktualisieren und artefaktübergreifend validieren |
| `/codexspec:specify` | Feature-Anforderungen besprechen, bestätigen und dauerhaft speichern |
| `/codexspec:blueprint` | Bestätigte ausstehende Blueprint-Anforderungen vorbereiten oder pflegen |
| `/codexspec:generate-spec` | Bestätigte Anforderungen in eine nachvollziehbare Spezifikation überführen; automatisches Review |
| `/codexspec:spec-to-design` | Architektur, Komponenten, Schnittstellen und Entscheidungen festlegen; automatisches Review |
| `/codexspec:design-to-plan` | Implementierungsphasen, Reihenfolge und Verifikation planen; automatisches Review |
| `/codexspec:plan-to-tasks` | Überprüfbare Aufgaben mit Abdeckung vorgelagerter Vorgaben erstellen; automatisches Review und analyze |
| `/codexspec:implement-tasks` | Aufgaben ausführen, Ergebnisse verifizieren, prüfen und korrigieren |
| `/codexspec:auto-dev` | Bestätigte Blueprint-Anforderungen autonom in Dokumentreihenfolge entwickeln |

### Befehle für Artefakt-Reviews

| Befehl | Zweck |
|---------|---------|
| `/codexspec:review-spec` | Übereinstimmung und interne Qualität der Spezifikation prüfen |
| `/codexspec:review-design` | Übereinstimmung, Machbarkeit und Planungsreife des Entwurfs prüfen |
| `/codexspec:review-plan` | Übereinstimmung, Machbarkeit und Implementierungsreife des Plans prüfen |
| `/codexspec:review-tasks` | Übereinstimmung, Abhängigkeiten, Ausführbarkeit und Verifikation der Aufgaben prüfen |

### Anforderungen, bestehender Code und Debugging

| Befehl | Zweck |
|---------|---------|
| `/codexspec:clarify` | Mehrdeutige Anforderungen klären und Anforderungen vor der Spezifikation aktualisieren |
| `/codexspec:analyze` | Durchgängige Nachvollziehbarkeit prüfen und nachgelagerte Artefakte an die maßgeblichen Vorgaben anpassen |
| `/codexspec:checklist` | Eine Checkliste zur Anforderungsqualität erstellen |
| `/codexspec:tasks-to-issues` | Bestehende Aufgaben in umsetzbare GitHub-Issues umwandeln |
| `/codexspec:debug` | Grundursachen untersuchen, bevor eine Korrektur angewendet wird |
| `/codexspec:reverse-spec` | Bestehende Architektur untersuchen, Modul-Artefakte entwerfen oder Abweichungen von der Ausgangsbasis melden |

### Befehle für Projektwissen

| Befehl | Zweck |
|---------|---------|
| `/codexspec:distill` | Wiederverwendbares Wissen erfassen oder Kandidaten im lokalen Arbeitsbereich prüfen |
| `/codexspec:evolve` | Geprüftes Wissen in einen Entwurf für einen Upstream-Beitrag überführen |
| `/codexspec:onboard` | Konventionskandidaten und belegte Einschränkungen aus bestehendem Code gewinnen |

### Git- und Code-Review-Befehle

| Befehl | Zweck |
|---------|---------|
| `/codexspec:commit-staged` | Nachrichten aus bereitgestellten Änderungen erstellen; Vorschau oder Ausführung eines autorisierten Commits |
| `/codexspec:pr` | Eine strukturierte PR/MR-Beschreibung erstellen |
| `/codexspec:release-notes` | Einen Changelog-Eintrag pflegen und einen Veröffentlichungstext aus dem Git-Verlauf erstellen |
| `/codexspec:review-code` | Ausgewählte Änderungen als Defekt-Gate auf Fehler prüfen, die die Freigabe verhindern; `--audit` für die Qualität von Pfaden verwenden |

### Hilfsbefehle

| Befehl | Zweck |
|---------|---------|
| `/codexspec:config` | Projektkonfiguration interaktiv erstellen/anzeigen/ändern/zurücksetzen |
| `/codexspec:quick` | Einen kompakten Requirements-First-SDD-Workflow für kleine Änderungen ausführen |

## Konfiguration und Internationalisierung

Die Konfiguration liegt in `.codexspec/config.yml`. Vorlagen bleiben auf Englisch;
Agenten schreiben Interaktionstext und erzeugte Artefakte in den konfigurierten
Sprachen. Die 13 standardmäßigen Sprachcodes sind `en`, `zh-CN`, `zh-TW`, `ja`,
`ko`, `es`, `fr`, `de`, `pt`, `ru`, `it`, `ar` und `hi`.
Der portugiesische CLI-Code ist `pt`; lokalisierte Dokumentation und
Übersetzungskataloge verwenden `pt-BR`.

### Sprachdimensionen

| Dimension | Konfigurationsschlüssel | Bei Initialisierung | Später setzen | Steuert |
|-----------|------------|-------------------|-----------|----------|
| Ausgabe/Basis | `language.output` | `--lang` | `config --set-lang` | Rückfallwert für die anderen Sprachdimensionen |
| Interaktion | `language.interaction` | `--interaction-lang` | `config --set-interaction-lang` | Gespräch und CLI-Ausgabe |
| Dokument | `language.document` | `--document-lang` | `config --set-document-lang` | Anforderungen, Spezifikationen, Entwürfe, Pläne, Aufgaben |
| Commit | `language.commit` | `--commit-lang` | `config --set-commit-lang` | Commit-Nachrichten und Inhalte für die Auslieferung über Git |

Jede spezifische Sprache fällt unabhängig auf `language.output` und anschließend
auf `en` zurück. `language.templates` bleibt `en`.

```bash
codexspec init my-project --ai both \
  --interaction-lang zh-CN --document-lang en --commit-lang en

codexspec config
codexspec config --set-document-lang en
codexspec config --list-langs
```

Bei der erstmaligen TTY-Initialisierung wird nach der Basissprache gefragt, sofern
Sie nicht `--lang` oder alle drei spezifischen Sprachoptionen angeben.
`--force` bestätigt andere Initialisierungsrückfragen automatisch; diese
Sprachauswahl unterdrückt es nicht. Ohne TTY wird standardmäßig Englisch verwendet.
Eine erneute Initialisierung erhält Sprachschlüssel, die Sie nicht explizit gesetzt haben.

### Workflow- und Review-Einstellungen

| Einstellung | Standard | Wirkung | CLI-Steuerung |
|---------|---------|--------|-------------|
| `workflow.auto_next` | `false` | Erfolgreiche gewöhnliche SDD-Phasen weiterführen | `config --auto-next on\|off` |
| `workflow.auto_distill` | `true` | Nicht interaktive Wissenserfassung nach erfolgreichem Abschluss | `config --auto-distill on\|off` |
| `workflow.auto_maintenance` | `true` | Verifizierte inkrementelle Wartung während automatischer Korrekturen anwenden | `config --auto-maintenance on\|off` |
| `workflow.worktrees` | `true` | Gewöhnliche Features und eigenständige Wartung isolieren | `config --worktrees on\|off` |
| `review.decided_by` | `reviewer` | Wer über Befunde entscheidet, deren Auslöser außerhalb des Betriebskontexts des Projekts liegen | `config --decided-by reviewer\|ask` |

Boolesche CLI-Schalter akzeptieren `on/true/1/yes` und `off/false/0/no` unabhängig
von Groß-/Kleinschreibung, einschließlich umgebender Leerzeichen. Ein boolescher
Schalter ohne Wert kehrt den aktuellen Wert des Ziel-Checkouts um; gespeicherte
YAML-Werte sind boolesch.

Bei `review.decided_by: reviewer` entscheidet der Reviewer über die Anerkennung
eines Fehlers. Bei `ask` führt ein Auslöser außerhalb des Kontexts zu einer
ausstehenden Szenarioentscheidung: Der Benutzer entscheidet einmal, ob der Fehler
behoben oder dieses Szenario ausgeschlossen wird; die bestätigte Entscheidung bleibt
für spätere Runden erhalten. Ausstehende Entscheidungen blockieren den Abschluss.
Ein einzelner `review-code`-Aufruf kann den konfigurierten Modus mit `--decided-by` überschreiben.

Konfigurationsänderungen folgen dem Worktree-Routing. Eine eigenständige Änderung
aus dem Haupt-Checkout wird im Wartungs-Worktree vorgenommen und ändert nicht sofort
die wirksame Einstellung des Haupt-Checkouts; Änderungen in einem Feature-Worktree
werden dort wirksam.

<details>
<summary>CLI-Initialisierungsoptionen</summary>

| Option | Bedeutung |
|--------|---------|
| `PROJECT_NAME` | Name des neuen Verzeichnisses; `.` für das aktuelle Verzeichnis verwenden |
| `--here`, `-h` | Das aktuelle Verzeichnis initialisieren |
| `--ai`, `-a` | `claude`, `codex` oder `both`; Standard `claude` |
| `--lang`, `-l` | Die Basissprache für die Ausgabe setzen |
| `--interaction-lang` | Die Interaktionssprache setzen |
| `--document-lang` | Die Dokumentsprache setzen |
| `--commit-lang` | Die Sprache für Commit-Nachrichten setzen |
| `--force`, `-f` | Installierte Artefakte neu erzeugen und Migrations-/Aktualisierungs-/Compliance-Rückfragen automatisch bestätigen; projektspezifische Kontextinhalte und nicht betroffene Konfiguration erhalten |
| `--no-git` | Initialisierung des Git-Repositorys überspringen |
| `--debug`, `-d` | Detaillierte Debug-Ausgabe anzeigen |

</details>

<details>
<summary>CLI-Konfigurationsoptionen</summary>

| Option | Bedeutung |
|--------|---------|
| `--set-lang`, `-l` | Die Basissprache für die Ausgabe setzen |
| `--set-interaction-lang` | Die Interaktionssprache setzen |
| `--set-document-lang` | Die Dokumentsprache setzen |
| `--set-commit-lang`, `-c` | Die Sprache für Commit-Nachrichten setzen |
| `--list-langs` | Unterstützte Sprachcodes auflisten |
| `--auto-next` | Automatisches Fortschreiten zwischen Phasen umschalten/setzen |
| `--auto-distill` | Automatische Wissenserfassung umschalten/setzen |
| `--auto-maintenance` | Automatische inkrementelle Wartung umschalten/setzen |
| `--worktrees` | Lokal pro Checkout geltende Worktree-Isolation umschalten/setzen |
| `--decided-by` | Den Review-Entscheidungsmodus `reviewer` oder `ask` setzen |

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

Details zum Sprach- und Einstellungsverhalten finden Sie unter
[Konfiguration](docs/en/reference/configuration.md) und
[Internationalisierung](docs/en/user-guide/i18n.md).

## Projektstruktur

Die Initialisierung installiert gemeinsame Ressourcen sowie die ausgewählte Assistentenintegration:

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

Der gemeinsame Blueprint liegt im dedizierten auto-dev-Worktree, nicht als separat
bearbeitbare Kopie in jedem gewöhnlichen Checkout. Entwürfe der manuellen
Wissensprüfung werden von Git ausgeschlossen.

## Materialien für Erweiterungen

Das Repository enthält eine Vorlage für ein Erweiterungsmanifest, einen
Beispielbefehl und eine [Entwicklungsanleitung für Erweiterungen](extensions/EXTENSION-DEVELOPMENT-GUIDE.md).
Dies sind Materialien zur Erstellung von Erweiterungen. Die aktuelle CLI hat keine
Befehle zum Installieren/Auflisten/Entfernen von Erweiterungen und lädt Befehle oder
Hooks aus `extension.yml` nicht automatisch. Gemeinsame Review-Ressourcen unterstützen
projektspezifische Ergänzungen unter `.codexspec/review-code/`; die Initialisierung
bewahrt vorhandene Ressourcenänderungen und zusätzliche Dateien, sofern kein Ersatz
angefordert wird.

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
Paketierung oder Initialisierung ändern. Ausgelieferte Befehls- und Skill-Kopien
sind generierte Installationsartefakte; bearbeiten Sie ihre maßgeblichen Quellen
und erzeugen Sie sie neu.

## Beitragen

Informationen zur lokalen Einrichtung und zu Beiträgen finden Sie in der
[Beitragsanleitung](docs/en/development/contributing.md). Beiträge sollten bestätigte
Anforderungen, Nachvollziehbarkeit der Quellen und die Paketierungsgrenze zwischen
Benutzern und Maintainer-Werkzeugen bewahren.

## Lizenz

MIT — siehe [LICENSE](LICENSE).

## Danksagungen

Inspiriert von [GitHub spec-kit](https://github.com/github/spec-kit).
Integriert sich mit Claude Code und OpenAI Codex.

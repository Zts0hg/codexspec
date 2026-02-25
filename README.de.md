# CodexSpec

[English](README.md) | [中文](README.zh-CN.md) | [日本語](README.ja.md) | [Español](README.es.md) | [Português](README.pt-BR.md) | [한국어](README.ko.md) | **Deutsch** | [Français](README.fr.md)

[![PyPI version](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**[📖 Dokumentation](https://zts0hg.github.io/codexspec/)**

**Ein Spec-Driven Development (SDD) Toolkit für Claude Code**

CodexSpec ist ein Toolkit, das Ihnen hilft, hochwertige Software mit einem strukturierten, spezifikationsgesteuerten Ansatz zu erstellen. Es kehrt die traditionelle Entwicklung um, indem es Spezifikationen in ausführbare Artefakte verwandelt, die die Implementierung direkt leiten.

## Design-Philosophie: Mensch-KI-Zusammenarbeit

CodexSpec basiert auf der Überzeugung, dass **effektive KI-gestützte Entwicklung aktive menschliche Beteiligung auf jeder Stufe erfordert**. Das Toolkit ist um ein Kernprinzip herum konzipiert:

> **Jedes Artefakt überprüfen und validieren, bevor weitergemacht wird.**

### Warum menschliche Aufsicht wichtig ist

Bei der KI-gestützten Entwicklung führt das Überspringen von Review-Phasen zu:

| Problem | Konsequenz |
|---------|------------|
| Unklare Anforderungen | KI trifft Annahmen, die von Ihrer Absicht abweichen |
| Unvollständige Spezifikationen | Features werden ohne kritische Edge Cases entwickelt |
| Fehlausgerichtete technische Pläne | Architektur passt nicht zu den Geschäftsanforderungen |
| Vage Aufgabenverteilungen | Implementierung gerät vom Kurs, erfordert teure Überarbeitung |

### Der CodexSpec-Ansatz

CodexSpec strukturiert die Entwicklung in **überprüfbare Checkpoints**:

```
Idee → Klären → Review → Plan → Review → Aufgaben → Review → Analysieren → Implementieren
              ↑                ↑                ↑
           Mensch prüft    Mensch prüft    Mensch prüft
```

**Jedes Artefakt hat einen entsprechenden Review-Befehl:**
- `spec.md` → `/codexspec.review-spec`
- `plan.md` → `/codexspec.review-plan`
- `tasks.md` → `/codexspec.review-tasks`
- Alle Artefakte → `/codexspec.analyze`

Dieser systematische Review-Prozess gewährleistet:
- **Frühe Fehlererkennung**: Missverständnisse erfassen, bevor Code geschrieben wird
- **Abstimmungsverifikation**: Bestätigen, dass die Interpretation der KI Ihrer Absicht entspricht
- **Qualitätstore**: Vollständigkeit, Klarheit und Machbarkeit auf jeder Stufe validieren
- **Reduzierte Überarbeitung**: Minuten in Review investieren, um Stunden an Neuimplementierung zu sparen

## Funktionen

### Kern-SDD-Workflow
- **Verfassungsbasiert**: Projektprinzipien etablieren, die alle nachfolgenden Entscheidungen leiten
- **Zwei-Phasen-Spezifikation**: Interaktive Klärung (`/specify`) gefolgt von Dokumentgenerierung (`/generate-spec`)
- **Plan-getriebene Entwicklung**: Technische Entscheidungen kommen nach validierten Anforderungen
- **TDD-bereite Aufgaben**: Aufgabenverteilungen erzwingen Test-First-Methodik

### Mensch-KI-Zusammenarbeit
- **Review-Befehle**: Dedizierte Review-Befehle für Spec, Plan und Aufgaben zur Validierung der KI-Ausgabe
- **Interaktive Klärung**: Q&A-basierte Anforderungsverfeinerung mit sofortigem Feedback
- **Artefaktübergreifende Analyse**: Inkonsistenzen zwischen Spec, Plan und Aufgaben vor der Implementierung erkennen
- **Qualitätschecklisten**: Automatisierte Qualitätsbewertung für Anforderungen

### Entwicklererfahrung
- **Claude Code Integration**: Native Slash-Befehle für Claude Code
- **Internationalisierung (i18n)**: Mehrsprachige Unterstützung durch LLM-Dynamische Übersetzung
- **Plattformübergreifend**: Unterstützung für Bash- und PowerShell-Skripte
- **Erweiterbar**: Plugin-Architektur für benutzerdefinierte Befehle

## Installation

### Voraussetzungen

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (empfohlen) oder pip

### Option 1: Mit uv installieren (Empfohlen)

Der einfachste Weg, CodexSpec zu installieren, ist mit uv:

```bash
uv tool install codexspec
```

### Option 2: Mit pip installieren

Alternativ können Sie pip verwenden:

```bash
pip install codexspec
```

### Option 3: Einmalige Verwendung

Direkt ausführen ohne Installation:

```bash
# Neues Projekt erstellen
uvx codexspec init my-project

# In einem bestehenden Projekt initialisieren
cd your-existing-project
uvx codexspec init . --ai claude
```

### Option 4: Von GitHub installieren (Entwicklungsversion)

Für die neueste Entwicklungsversion oder einen bestimmten Branch:

```bash
# Mit uv
uv tool install git+https://github.com/Zts0hg/codexspec.git

# Mit pip
pip install git+https://github.com/Zts0hg/codexspec.git

# Bestimmter Branch oder Tag
uv tool install git+https://github.com/Zts0hg/codexspec.git@main
uv tool install git+https://github.com/Zts0hg/codexspec.git@v0.2.0
```

## Schnellstart

Nach der Installation können Sie die CLI verwenden:

```bash
# Neues Projekt erstellen
codexspec init my-project

# Projekt mit deutscher Ausgabe erstellen
codexspec init my-project --lang de

# In bestehendem Projekt initialisieren
codexspec init . --ai claude
# oder
codexspec init --here --ai claude

# Installierte Tools überprüfen
codexspec check

# Version anzeigen
codexspec version
```

Upgrade auf die neueste Version:

```bash
# Mit uv
uv tool install codexspec --upgrade

# Mit pip
pip install --upgrade codexspec
```

## Verwendung

### 1. Projekt initialisieren

Nach der [Installation](#installation) erstellen oder initialisieren Sie Ihr Projekt:

```bash
codexspec init my-awesome-project
# oder im aktuellen Verzeichnis
codexspec init . --ai claude
```

### 2. Projektprinzipien festlegen

Starten Sie Claude Code im Projektverzeichnis:

```bash
cd my-awesome-project
claude
```

Verwenden Sie den Befehl `/codexspec.constitution`, um die Governance-Prinzipien des Projekts zu erstellen:

```
/codexspec.constitution Prinzipien erstellen, die sich auf Codequalität, Teststandards und Clean Architecture konzentrieren
```

### 3. Anforderungen klären

Verwenden Sie `/codexspec.specify`, um Ihre Anforderungen durch interaktives Q&A zu **explorieren und klären**:

```
/codexspec.specify Ich möchte eine Aufgabenverwaltungsanwendung erstellen
```

Dieser Befehl wird:
- Klärungsfragen stellen, um Ihre Idee zu verstehen
- Edge Cases erkunden, die Sie vielleicht nicht berücksichtigt haben
- Hochwertige Anforderungen durch Dialog gemeinschaftlich erstellen
- **Keine** Dateien automatisch generieren - Sie behalten die Kontrolle

### 4. Spezifikationsdokument generieren

Sobald die Anforderungen geklärt sind, verwenden Sie `/codexspec.generate-spec` um das `spec.md` Dokument zu erstellen:

```
/codexspec.generate-spec
```

Dieser Befehl fungiert als "Anforderungscompiler", der Ihre geklärten Anforderungen in ein strukturiertes Spezifikationsdokument umwandelt.

### 5. Spezifikation überprüfen (Empfohlen)

**Bevor mit der Planung fortgefahren wird, die Spezifikation validieren:**

```
/codexspec.review-spec
```

Dieser Befehl generiert einen detaillierten Review-Bericht mit:
- Analyse der Abschnittsvollständigkeit
- Bewertung der Klarheit und Testbarkeit
- Abstimmungsprüfung mit der Verfassung
- Priorisierte Empfehlungen

### 6. Technischen Plan erstellen

Verwenden Sie `/codexspec.spec-to-plan`, um zu definieren, wie implementiert werden soll:

```
/codexspec.spec-to-plan Python mit FastAPI für das Backend, PostgreSQL für die Datenbank und React für das Frontend verwenden
```

Der Befehl beinhaltet **Konstitutionalitäts-Review** - Verifizierung, dass der Plan mit den Projektprinzipien übereinstimmt.

### 7. Plan überprüfen (Empfohlen)

**Bevor Aufgaben erstellt werden, den technischen Plan validieren:**

```
/codexspec.review-plan
```

Dies verifiziert:
- Spezifikationsabstimmung
- Architekturqualität
- Technologie-Stack-Angemessenheit
- Verfassungskonformität

### 8. Aufgaben generieren

Verwenden Sie `/codexspec.plan-to-tasks`, um den Plan aufzuteilen:

```
/codexspec.plan-to-tasks
```

Aufgaben sind in Standardphasen organisiert mit:
- **TDD-Erzwingung**: Test-Aufgaben vor Implementierungs-Aufgaben
- **Parallel-Marker `[P]`**: Unabhängige Aufgaben identifizieren
- **Dateipfad-Spezifikationen**: Klare Ergebnisse pro Aufgabe

### 9. Aufgaben überprüfen (Empfohlen)

**Bevor mit der Implementierung begonnen wird, die Aufgabenverteilung validieren:**

```
/codexspec.review-tasks
```

Dies überprüft:
- Plan-Abdeckung
- TDD-Konformität
- Abhängigkeitskorrektheit
- Aufgabengranularität

### 10. Analysieren (Optional aber empfohlen)

Verwenden Sie `/codexspec.analyze` für artefaktübergreifende Konsistenzprüfung:

```
/codexspec.analyze
```

Dies erkennt Probleme über Spec, Plan und Aufgaben:
- Abdeckungslücken (Anforderungen ohne Aufgaben)
- Duplikate und Inkonsistenzen
- Verfassungsverletzungen
- Unterspezifizierte Elemente

### 11. Implementieren

Verwenden Sie `/codexspec.implement-tasks`, um die Implementierung auszuführen:

```
/codexspec.implement-tasks
```

Die Implementierung folgt dem **bedingten TDD-Workflow**:
- Code-Aufgaben: Test-First (Red → Green → Verifizieren → Refaktorieren)
- Nicht-testbare Aufgaben (Dokumentation, Konfiguration): Direkte Implementierung

## Verfügbare Befehle

### CLI-Befehle

| Befehl | Beschreibung |
|--------|--------------|
| `codexspec init` | Neues CodexSpec-Projekt initialisieren |
| `codexspec check` | Installierte Tools überprüfen |
| `codexspec version` | Versionsinformationen anzeigen |
| `codexspec config` | Projektkonfiguration anzeigen oder ändern |

### `codexspec init` Optionen

| Option | Beschreibung |
|--------|--------------|
| `PROJECT_NAME` | Name für Ihr neues Projektverzeichnis |
| `--here`, `-h` | Im aktuellen Verzeichnis initialisieren |
| `--ai`, `-a` | Zu verwendender KI-Assistent (Standard: claude) |
| `--lang`, `-l` | Ausgabesprache (z.B. en, zh-CN, ja) |
| `--force`, `-f` | Bestehende Dateien überschreiben |
| `--no-git` | Git-Initialisierung überspringen |
| `--debug`, `-d` | Debug-Ausgabe aktivieren |

### `codexspec config` Optionen

| Option | Beschreibung |
|--------|--------------|
| `--set-lang`, `-l` | Ausgabesprache festlegen |
| `--set-commit-lang`, `-c` | Commit-Nachrichten-Sprache festlegen (Standard: Ausgabesprache) |
| `--list-langs` | Alle unterstützten Sprachen auflisten |

### Slash-Befehle

Nach der Initialisierung sind diese Slash-Befehle in Claude Code verfügbar:

#### Kern-Workflow-Befehle

| Befehl | Beschreibung |
|--------|--------------|
| `/codexspec.constitution` | Projekt-Verfassung erstellen oder aktualisieren mit artefaktübergreifender Validierung und Sync-Impact-Reporting |
| `/codexspec.specify` | Anforderungen durch interaktives Q&A **klären** (keine Dateigenerierung) |
| `/codexspec.generate-spec` | `spec.md` Dokument nach Anforderungsklärung **generieren** |
| `/codexspec.spec-to-plan` | Spezifikation in technischen Plan umwandeln mit Konstitutionalitäts-Review und Modul-Abhängigkeitsgraph |
| `/codexspec.plan-to-tasks` | Plan in atomare, TDD-erzwungene Aufgaben mit Parallel-Markern `[P]` aufteilen |
| `/codexspec.implement-tasks` | Aufgaben mit bedingtem TDD-Workflow ausführen (TDD für Code, direkt für Docs/Konfiguration) |

#### Review-Befehle (Qualitätstore)

| Befehl | Beschreibung |
|--------|--------------|
| `/codexspec.review-spec` | Spezifikation auf Vollständigkeit, Klarheit, Konsistenz und Testbarkeit mit Bewertung validieren |
| `/codexspec.review-plan` | Technischen Plan auf Machbarkeit, Architekturqualität und Verfassungsabstimmung überprüfen |
| `/codexspec.review-tasks` | Aufgabenverteilung auf Plan-Abdeckung, TDD-Konformität, Abhängigkeiten und Granularität validieren |

#### Erweiterte Befehle

| Befehl | Beschreibung |
|--------|--------------|
| `/codexspec.clarify` | Vorhandene spec.md nach Unklarheiten durchsuchen mit 4 fokussierten Kategorien, Integration mit Review-Ergebnissen |
| `/codexspec.analyze` | Nicht-destruktive artefaktübergreifende Analyse (Spec, Plan, Aufgaben) mit schweregradbasierter Problemeerkennung |
| `/codexspec.checklist` | Qualitätschecklisten für Anforderungsvalidierung generieren |
| `/codexspec.tasks-to-issues` | Aufgaben in GitHub-Issues für Projektmanagement-Integration umwandeln |

#### Git-Workflow-Befehle

| Befehl | Beschreibung |
|--------|--------------|
| `/codexspec.commit` | Conventional Commits-Nachrichten basierend auf Git-Status und Sitzungskontext generieren |
| `/codexspec.commit-staged` | Commit-Nachricht nur aus gestageten Änderungen generieren |

## Workflow-Übersicht

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    CodexSpec Mensch-KI-Zusammenarbeit Workflow           │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. Constitution  ──►  Projektprinzipien definieren                      │
│         │                         mit artefaktübergreifender Validierung │
│         ▼                                                                │
│  2. Specify  ───────►  Interaktives Q&A zur Anforderungsklärung          │
│         │               (keine Datei erstellt - menschliche Kontrolle)   │
│         ▼                                                                │
│  3. Generate Spec  ─►  spec.md Dokument erstellen                        │
│         │                                                                │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ REVIEW-TOR 1: /codexspec.review-spec ★                         ║   │
│  ║  Validieren: Vollständigkeit, Klarheit, Testbarkeit, Verfassung   ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  4. Clarify  ───────►  Unklarheiten klären (iterativ)                    │
│         │               4 fokussierte Kategorien, max 5 Fragen           │
│         ▼                                                                │
│  5. Spec to Plan  ──►  Technischen Plan erstellen mit:                   │
│         │               • Konstitutionalitäts-Review (PFLICHT)           │
│         │               • Modul-Abhängigkeitsgraph                        │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ REVIEW-TOR 2: /codexspec.review-plan ★                         ║   │
│  ║  Validieren: Spec-Abstimmung, Architektur, Tech-Stack, Phasen     ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  6. Plan to Tasks  ─►  Atomare Aufgaben generieren mit:                  │
│         │               • TDD-Erzwingung (Tests vor Implementierung)     │
│         │               • Parallel-Marker [P]                            │
│         │               • Dateipfad-Spezifikationen                       │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ REVIEW-TOR 3: /codexspec.review-tasks ★                        ║   │
│  ║  Validieren: Abdeckung, TDD-Konformität, Abhängigkeiten, Granularität ║ │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  7. Analyze  ───────►  Artefaktübergreifende Konsistenzprüfung           │
│         │               Lücken, Duplikate, Verfassungsprobleme erkennen  │
│         ▼                                                                │
│  8. Implement  ─────►  Mit bedingtem TDD-Workflow ausführen              │
│                          Code: Test-First | Docs/Konfiguration: Direkt   │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

**Schlüsselerkenntnis**: Jedes Review-Tor (★) ist ein **menschlicher Checkpoint**, an dem Sie die KI-Ausgabe validieren, bevor Sie mehr Zeit investieren. Das Überspringen dieser Tore führt oft zu kostspieliger Überarbeitung.

### Schlüsselkonzept: Anforderungsklärungs-Workflow

CodexSpec bietet **zwei unterschiedliche Klärungsbefehle** für verschiedene Phasen des Workflows:

#### specify vs clarify: Wann welchen verwenden?

| Aspekt | `/codexspec.specify` | `/codexspec.clarify` |
|--------|----------------------|----------------------|
| **Zweck** | Initiale Anforderungsexploration | Iterative Verfeinerung existierender Specs |
| **Wann verwenden** | Mit neuer Idee starten, kein spec.md existiert | spec.md existiert, Lücken füllen |
| **Eingabe** | Ihre ursprüngliche Idee oder Anforderung | Existierende spec.md-Datei |
| **Ausgabe** | Keine (nur Dialog) | Aktualisiert spec.md mit Klärungen |
| **Methode** | Offenes Q&A | Strukturierter Unklarheiten-Scan (4 Kategorien) |
| **Fragenlimit** | Unbegrenzt | Maximal 5 Fragen |
| **Typische Verwendung** | "Ich möchte eine Todo-App erstellen" | "Spec fehlen Fehlerbehandlungsdetails" |

#### Zwei-Phasen-Spezifikation

Vor der Dokumentgenerierung:

| Phase | Befehl | Zweck | Ausgabe |
|-------|--------|-------|---------|
| **Exploration** | `/codexspec.specify` | Interaktives Q&A zur Anforderungsexploration und -verfeinerung | Keine (nur Dialog) |
| **Generierung** | `/codexspec.generate-spec` | Geklärte Anforderungen in strukturiertes Dokument kompilieren | `spec.md` |

#### Iterative Klärung

Nach Erstellung von spec.md:

```
spec.md ──► /codexspec.clarify ──► Aktualisiertes spec.md (mit Clarifications-Abschnitt)
                │
                └── Scannt nach Unklarheiten in 4 fokussierten Kategorien:
                    • Vollständigkeitslücken - Fehlende Abschnitte, leerer Inhalt
                    • Spezifitätsprobleme - Vage Begriffe, undefinierte Einschränkungen
                    • Verhaltensklarheit - Fehlerbehandlung, Zustandsübergänge
                    • Messbarkeitsprobleme - Nicht-funktionale Anforderungen ohne Metriken
```

#### Vorteile dieses Designs

- **Mensch-KI-Zusammenarbeit**: Sie nehmen aktiv an der Anforderungsentdeckung teil
- **Explizite Kontrolle**: Dateien werden nur erstellt, wenn Sie entscheiden
- **Qualitätsfokus**: Anforderungen werden vor der Dokumentation gründlich erkundet
- **Iterative Verfeinerung**: Specs können schrittweise verbessert werden, wenn das Verständnis vertieft

## Projektstruktur

Nach der Initialisierung hat Ihr Projekt diese Struktur:

```
my-project/
├── .codexspec/
│   ├── memory/
│   │   └── constitution.md    # Projekt-Governance-Prinzipien
│   ├── specs/
│   │   └── {feature-id}/
│   │       ├── spec.md        # Funktionsspezifikation
│   │       ├── plan.md        # Technischer Plan
│   │       ├── tasks.md       # Aufgabenverteilung
│   │       └── checklists/    # Qualitätschecklisten
│   ├── templates/             # Benutzerdefinierte Vorlagen
│   ├── scripts/               # Hilfsskripte
│   │   ├── bash/              # Bash-Skripte
│   │   └── powershell/        # PowerShell-Skripte
│   └── extensions/            # Benutzerdefinierte Erweiterungen
├── .claude/
│   └── commands/              # Slash-Befehle für Claude Code
└── CLAUDE.md                  # Kontext für Claude Code
```

## Internationalisierung (i18n)

CodexSpec unterstützt mehrere Sprachen durch **LLM-Dynamische Übersetzung**. Anstatt übersetzte Vorlagen zu pflegen, lässt Claude Inhalte zur Laufzeit basierend auf Ihrer Sprachkonfiguration übersetzen.

### Sprache festlegen

**Während der Initialisierung:**
```bash
# Ein Projekt mit chinesischer Ausgabe erstellen
codexspec init my-project --lang zh-CN

# Ein Projekt mit japanischer Ausgabe erstellen
codexspec init my-project --lang ja
```

**Nach der Initialisierung:**
```bash
# Aktuelle Konfiguration anzeigen
codexspec config

# Spracheinstellung ändern
codexspec config --set-lang zh-CN

# Unterstützte Sprachen auflisten
codexspec config --list-langs
```

### Commit-Nachrichten-Sprache

Sie können eine andere Sprache für Commit-Nachrichten als für die Ausgabe konfigurieren:

```bash
# Deutsch für Interaktionen, Englisch für Commit-Nachrichten
codexspec config --set-lang de
codexspec config --set-commit-lang en
```

**Sprachpriorität für Commit-Nachrichten:**
1. `language.commit` Einstellung (falls angegeben)
2. `language.output` (Alternative)
3. `"en"` (Standard)

**Hinweis:** Der Commit-Typ (feat, fix, docs usw.) und der Scope bleiben immer auf Englisch. Nur der Beschreibungsteil verwendet die konfigurierte Sprache.

### Konfigurationsdatei

Die Datei `.codexspec/config.yml` speichert die Spracheinstellungen:

```yaml
version: "1.0"

language:
  # Ausgabesprache für Claude-Interaktionen und generierte Dokumente
  output: "zh-CN"

  # Commit-Nachrichten-Sprache (Standard: Ausgabesprache)
  # Auf "en" setzen für englische Commit-Nachrichten unabhängig von der Ausgabesprache
  commit: "zh-CN"

  # Vorlagensprache - als "en" belassen für Kompatibilität
  templates: "en"

project:
  ai: "claude"
  created: "2026-02-15"
```

### Unterstützte Sprachen

| Code | Sprache |
|------|---------|
| `en` | English (Standard) |
| `zh-CN` | 中文（简体） |
| `zh-TW` | 中文（繁體） |
| `ja` | 日本語 |
| `ko` | 한국어 |
| `es` | Español |
| `fr` | Français |
| `de` | Deutsch |
| `pt` | Português |
| `ru` | Русский |
| `it` | Italiano |
| `ar` | العربية |
| `hi` | हिन्दी |

### Funktionsweise

1. **Einzelne englische Vorlagen**: Alle Befehlsvorlagen bleiben auf Englisch
2. **Sprachkonfiguration**: Das Projekt gibt die bevorzugte Ausgabesprache an
3. **Dynamische Übersetzung**: Claude liest englische Anweisungen, gibt in der Zielsprache aus
4. **Kontextbewusst**: Technische Begriffe (JWT, OAuth, etc.) bleiben bei Bedarf auf Englisch

### Vorteile

- **Keine Übersetzungspflege**: Keine Notwendigkeit, mehrere Vorlagenversionen zu pflegen
- **Immer aktuell**: Vorlagen-Updates kommen automatisch allen Sprachen zugute
- **Kontextbewusste Übersetzung**: Claude liefert natürliche, kontextgerechte Übersetzungen
- **Unbegrenzte Sprachen**: Jede von Claude unterstützte Sprache funktioniert sofort

### Constitution und Generierte Dokumente

Wenn Sie `/codexspec.constitution` verwenden, um Ihre Projekt-Verfassung zu erstellen, wird sie in der in Ihrer Konfiguration angegebenen Sprache generiert:

- **Ein-Datei-Ansatz**: Die Verfassung wird nur in einer Sprache generiert
- **Claude Versteht Alle Sprachen**: Claude kann mit Verfassungsdateien in jeder unterstützten Sprache arbeiten
- **Team-Zusammenarbeit**: Teams sollten eine konsistente Arbeitssprache verwenden

Dieses Design vermeidet Synchronisationsprobleme zwischen mehreren Sprachversionen und reduziert den Wartungsaufwand.

## Erweiterungssystem

CodexSpec unterstützt eine Plugin-Architektur für benutzerdefinierte Befehle:

### Erweiterungsstruktur

```
my-extension/
├── extension.yml          # Erweiterungs-Manifest
├── commands/              # Benutzerdefinierte Slash-Befehle
│   └── command.md
└── README.md
```

### Erweiterungen erstellen

1. Kopieren Sie die Vorlage aus `extensions/template/`
2. Modifizieren Sie `extension.yml` mit Ihren Erweiterungsdetails
3. Fügen Sie Ihre benutzerdefinierten Befehle in `commands/` hinzu
4. Testen Sie lokal und veröffentlichen Sie

Siehe `extensions/EXTENSION-DEVELOPMENT-GUIDE.md` für Details.

## Entwicklung

### Voraussetzungen

- Python 3.11+
- uv Paketmanager
- Git

### Lokale Entwicklung

```bash
# Repository klonen
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Entwicklungsabhängigkeiten installieren
uv sync --dev

# Lokal ausführen
uv run codexspec --help

# Tests ausführen
uv run pytest

# Code linten
uv run ruff check src/
```

### Bauen

```bash
# Paket bauen
uv build
```

## Vergleich mit spec-kit

CodexSpec ist von GitHub's spec-kit inspiriert, aber mit einigen wichtigen Unterschieden:

| Funktion | spec-kit | CodexSpec |
|----------|----------|-----------|
| Kernphilosophie | Spezifikationsgesteuerte Entwicklung | Spezifikationsgesteuerte Entwicklung + Mensch-KI-Zusammenarbeit |
| CLI-Name | `specify` | `codexspec` |
| Primäre KI | Multi-Agent-Unterstützung | Claude Code fokussiert |
| Befehlspräfix | `/speckit.*` | `/codexspec.*` |
| Verfassungssystem | Basis | Volle Verfassung mit artefaktübergreifender Validierung |
| Zwei-Phasen-Spezifikation | Nein | Ja (Klärung + Generierung) |
| Review-Befehle | Optional | 3 dedizierte Review-Befehle mit Bewertung |
| Clarify-Befehl | Ja | 4 fokussierte Kategorien, Review-Integration |
| Analyze-Befehl | Ja | Nur-Lese, schweregradbasiert, verfassungsbewusst |
| TDD in Aufgaben | Optional | Erzwungen (Tests vor Implementierung) |
| Implementierung | Standard | Bedingtes TDD (Code vs Docs/Konfiguration) |
| Erweiterungssystem | Ja | Ja |
| PowerShell-Skripte | Ja | Ja |
| i18n-Unterstützung | Nein | Ja (13+ Sprachen via LLM-Übersetzung) |

### Hauptunterschiede

1. **Review-First-Kultur**: Jedes wichtige Artefakt hat einen dedizierten Review-Befehl
2. **Verfassungs-Governance**: Prinzipien werden validiert, nicht nur dokumentiert
3. **TDD als Standard**: Test-First-Methodik in Aufgabengenerierung erzwungen
4. **Menschliche Checkpoints**: Workflow um Validierungstore herum konzipiert

## Philosophie

CodexSpec folgt diesen Kernprinzipien:

### SDD-Grundlagen

1. **Absichtsgesteuerte Entwicklung**: Spezifikationen definieren das "Was" vor dem "Wie"
2. **Umfangreiche Spezifikationserstellung**: Guardrails und Organisationsprinzipien verwenden
3. **Mehrstufige Verfeinerung**: Statt One-Shot-Codegenerierung
4. **Verfassungs-Governance**: Projektprinzipien leiten alle Entscheidungen

### Mensch-KI-Zusammenarbeit

5. **Mensch-in-der-Schleife**: KI generiert Artefakte, Menschen validieren sie
6. **Review-orientiert**: Jedes Artefakt validieren, bevor weitergemacht wird
7. **Progressive Offenlegung**: Komplexe Informationen schrittweise enthüllen
8. **Explizit vor implizit**: Anforderungen sollten klar sein, nicht angenommen

### Qualitätssicherung

9. **Test-getrieben als Standard**: TDD-Workflow in Aufgabengenerierung integriert
10. **Artefaktübergreifende Konsistenz**: Spec, Plan und Aufgaben gemeinsam analysieren
11. **Verfassungsabstimmung**: Alle Artefakte respektieren Projektprinzipien

### Warum Review wichtig ist

| Ohne Review | Mit Review |
|-------------|------------|
| KI trifft falsche Annahmen | Mensch erfasst Fehlinterpretationen früh |
| Unvollständige Anforderungen propagieren sich | Lücken vor Implementierung identifiziert |
| Architektur driftet von Absicht ab | Abstimmung auf jeder Stufe verifiziert |
| Aufgaben verpassen kritische Funktionalität | Abdeckung systematisch validiert |
| **Ergebnis: Überarbeitung, verschwendeter Aufwand** | **Ergebnis: Beim ersten Mal richtig** |

## Mitwirken

Beiträge sind willkommen! Bitte lesen Sie unsere Mitwirkungsrichtlinien, bevor Sie einen Pull-Request einreichen.

## Lizenz

MIT-Lizenz - siehe [LICENSE](LICENSE) für Details.

## Danksagung

- Inspiriert von [GitHub spec-kit](https://github.com/github/spec-kit)
- Erstellt für [Claude Code](https://claude.ai/code)

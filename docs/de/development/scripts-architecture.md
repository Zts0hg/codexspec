# Scripts-Architektur

Dieses Dokument beschreibt detailliert die Code-Logik der Skripte im CodexSpec-Projekt und wie sie in Claude Code verwendet werden.

## 1. Architektur-Überblick

CodexSpec ist ein **Spec-Driven-Development-(SDD)**-Toolkit mit einer Drei-Schichten-Architektur: CLI + Vorlagen + Hilfsskripte.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Nutzerebene (CLI)                        │
│  codexspec init | check | version | config                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Claude-Code-Interaktionsebene                │
│  /codexspec:specify | /codexspec:analyze | ...                  │
│  (.claude/commands/*.md)                                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Hilfsskript-Ebene                          │
│  .codexspec/scripts/*.sh (Bash) oder *.ps1 (PowerShell)         │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Bereitstellungsfluss der Skripte

### Phase 1: `codexspec init`-Initialisierung

In der Funktion `init()` in `src/codexspec/__init__.py` (Zeilen 343–368) werden plattformabhängig die passenden Skripte kopiert:

```python
# Hilfsskripte plattformabhängig kopieren
scripts_source_dir = get_scripts_dir()
if scripts_source_dir.exists():
    if sys.platform == "win32":
        # Windows: PowerShell-Skripte kopieren
        ps_scripts = scripts_source_dir / "powershell"
        for script_file in ps_scripts.glob("*.ps1"):
            dest_file = codexspec_dir / "scripts" / script_file.name
            dest_file.write_text(script_file.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        # macOS/Linux: Bash-Skripte kopieren
        bash_scripts = scripts_source_dir / "bash"
        for script_file in bash_scripts.glob("*.sh"):
            dest_file = codexspec_dir / "scripts" / script_file.name
            dest_file.write_text(script_file.read_text(encoding="utf-8"), encoding="utf-8")
```

**Ergebnis**: Abhängig vom Betriebssystem werden Skripte aus `scripts/bash/` oder `scripts/powershell/` in das Projektverzeichnis `.codexspec/scripts/` kopiert.

### Pfad-Auflösungsmechanismus

Die Funktion `get_scripts_dir()` (Zeilen 71–90) behandelt mehrere Installationsszenarien:

```python
def get_scripts_dir() -> Path:
    # Pfad 1: Wheel-Installation – Skripte im codexspec-Paket verpackt
    installed_scripts = Path(__file__).parent / "scripts"
    if installed_scripts.exists():
        return installed_scripts

    # Pfad 2: Entwicklungs-/Editable-Installation – Skripte im Projekt-Root
    dev_scripts = Path(__file__).parent.parent.parent / "scripts"
    if dev_scripts.exists():
        return dev_scripts

    # Pfad 3: Fallback
    return installed_scripts
```

## 3. Aufrufmechanismus der Skripte in Claude Code

### Kernmechanismus: YAML-Frontmatter-Deklaration

Vorlagen-Dateien deklarieren ihre Skript-Abhängigkeiten über den YAML-Frontmatter:

```yaml
---
description: Befehlsbeschreibung
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---
```

### Platzhalter-Ersetzung

In der Vorlage wird der Platzhalter `{SCRIPT}` verwendet:

```markdown
### 1. Kontext initialisieren

Führen Sie `{SCRIPT}` vom Repo-Root aus und parsen Sie das JSON nach:
- `FEATURE_DIR` – Pfad des Feature-Verzeichnisses
- `AVAILABLE_DOCS` – Liste verfügbarer Dokumente
```

### Aufruf-Fluss

1. Nutzer gibt in Claude Code `/codexspec:analyze` ein
2. Claude liest die Vorlage `.claude/commands/codexspec:analyze.md`
3. Abhängig vom Betriebssystem ersetzt Claude `{SCRIPT}` durch:
   - **macOS/Linux**: `.codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks`
   - **Windows**: `.codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks`
4. Claude führt das Skript aus, parst die JSON-Ausgabe und fährt fort

## 4. Funktionsdetails der Skripte

### 4.1 `check-prerequisites.sh/ps1` – Voraussetzungs-Prüfskript

Das wichtigste Skript: Es validiert den Umgebungszustand und liefert strukturierte Informationen zurück.

#### Kernfunktionen

- Validiert, ob Sie sich auf einem Feature-Branch befinden (Format: `2026-0613-1200ab-feature-name`)
- Erkennt, ob erforderliche Dateien existieren (`plan.md`, `tasks.md`)
- Liefert Pfad-Informationen im JSON-Format zurück

#### Parameter-Optionen

| Parameter | Bash | PowerShell | Wirkung |
|-----------|------|------------|---------|
| JSON-Ausgabe | `--json` | `-Json` | Ausgabe im JSON-Format |
| tasks.md verlangen | `--require-tasks` | `-RequireTasks` | Vorhandensein von tasks.md validieren |
| tasks.md einschließen | `--include-tasks` | `-IncludeTasks` | tasks.md in AVAILABLE_DOCS aufnehmen |
| Nur Pfade | `--paths-only` | `-PathsOnly` | Validierung überspringen, nur Pfade ausgeben |

#### Beispiel-JSON-Ausgabe

```json
{
  "FEATURE_DIR": "/path/to/.codexspec/specs/2026-0613-1200ab-my-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md", "tasks.md"]
}
```

### 4.2 `common.sh/ps1` – Allgemeine Hilfsfunktionen

Stellt plattformübergreifende gemeinsame Funktionen bereit:

#### Bash-Funktionen

| Funktion | Wirkung |
|----------|---------|
| `get_feature_id()` | Feature-ID aus Git-Branch oder Umgebungsvariable holen |
| `get_specs_dir()` | Pfad des specs-Verzeichnisses holen |
| `is_codexspec_project()` | Prüfen, ob es sich um ein CodexSpec-Projekt handelt |
| `require_codexspec_project()` | Sicherstellen, dass es ein CodexSpec-Projekt ist, sonst Abbruch |
| `log_info/success/warning/error()` | Farbiges Logging |
| `command_exists()` | Prüfen, ob ein Befehl existiert |

#### PowerShell-Funktionen

| Funktion | Wirkung |
|----------|---------|
| `Get-RepoRoot` | Wurzelverzeichnis des Git-Repositorys holen |
| `Get-CurrentBranch` | Aktuellen Branch-Namen holen |
| `Test-HasGit` | Erkennen, ob ein Git-Repository existiert |
| `Test-FeatureBranch` | Validieren, ob auf einem Feature-Branch |
| `Get-FeaturePathsEnv` | Alle Feature-bezogenen Pfade holen |
| `Test-FileExists` | Prüfen, ob eine Datei existiert |
| `Test-DirHasFiles` | Prüfen, ob ein Verzeichnis Dateien enthält |

### 4.3 `create-new-feature.sh/ps1` – Neues Feature anlegen

#### Funktion

- Erzeugt automatisch eine Feature-ID im Format `YYYY-MMDD-HHMMxx`
- Legt das Feature-Verzeichnis und eine initiale requirements.md an
- Legt den zugehörigen Git-Branch an
- Verlangt, dass der bereinigte Kurzname mindestens einen ASCII-Buchstaben oder eine ASCII-Ziffer enthält

#### Verwendungsbeispiel

```bash
./create-new-feature.sh -n "user authentication"
```

#### Feature-Namensvertrag

- Sequenzielle `NNN-name`-Bezeichner werden nicht unterstützt. Zeitstempel-Namen sind das einzige Feature-Namensformat.
- Legacy-Kompatibilität gilt für Artefakte: Ein bestehendes `spec.md` darf verwendet werden, wenn `requirements.md` fehlt. Das aktiviert aber keine alternativen Verzeichnis- oder Branch-Namensformate.
- Der vollständige Feature-Name identifiziert einen Workspace: `YYYY-MMDD-HHMMxx-short-name`. Unabhängig erzeugte Workspaces können dieselbe Zeitstempel-ID teilen, wenn ihre Kurznamen abweichen.
- Die Kurz-ID-Auflösung ist ausschließlich ein lokaler Komfort. Matchen mehrere Verzeichnisse, meldet die Auflösung Mehrdeutigkeit statt einen Workspace auszuwählen oder zu überschreiben.

## 5. Befehle, die Skripte verwenden

Die folgenden 4 Befehle nutzen Skripte:

| Befehl | Skript-Parameter | Wirkung |
|--------|------------------|---------|
| `/codexspec:clarify` | `--json --paths-only` | Pfade holen, keine Datei-Validierung |
| `/codexspec:checklist` | `--json` | Vorhandensein von plan.md validieren |
| `/codexspec:analyze` | `--json --require-tasks --include-tasks` | plan.md + tasks.md validieren |
| `/codexspec:tasks-to-issues` | `--json --require-tasks --include-tasks` | plan.md + tasks.md validieren |

## 6. Vollständiges Workflow-Diagramm

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        Initialisierungsphase                              │
│                                                                          │
│  $ codexspec init my-project                                             │
│       │                                                                  │
│       ├── .codexspec/-Verzeichnisstruktur anlegen                        │
│       ├── scripts/*.sh → .codexspec/scripts/ kopieren                    │
│       ├── templates/commands/*.md → .claude/commands/ kopieren           │
│       └── constitution.md, config.yml, CLAUDE.md anlegen                 │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────┐
│                        Verwendungsphase (Claude Code)                     │
│                                                                          │
│  Nutzer: /codexspec:analyze                                              │
│       │                                                                  │
│       ├── Claude liest .claude/commands/codexspec:analyze.md             │
│       │                                                                  │
│       ├── Skript-Deklaration im YAML-Frontmatter parsen                  │
│       │   scripts:                                                       │
│       │     sh: .codexspec/scripts/check-prerequisites.sh --json ...     │
│       │                                                                  │
│       ├── {SCRIPT}-Platzhalter ersetzen                                  │
│       │                                                                  │
│       ├── Skript ausführen:                                              │
│       │   $ .codexspec/scripts/check-prerequisites.sh --json ...         │
│       │                                                                  │
│       ├── JSON-Ausgabe parsen:                                           │
│       │   {"FEATURE_DIR": "...", "AVAILABLE_DOCS": [...]}                │
│       │                                                                  │
│       ├── spec.md, plan.md, tasks.md lesen                               │
│       │                                                                  │
│       └── Analyse-Bericht erzeugen                                       │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## 7. Design-Highlights

### 7.1 Plattformübergreifende Kompatibilität

Bash- und PowerShell-Versionen werden gepflegt und über `sys.platform` automatisch ausgewählt:

```python
if sys.platform == "win32":
    # PowerShell-Skripte kopieren
else:
    # Bash-Skripte kopieren
```

### 7.2 Deklarative Konfiguration

Skript-Abhängigkeiten werden über den YAML-Frontmatter deklariert – klar und intuitiv:

```yaml
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json
```

### 7.3 JSON-Ausgabe

Skripte geben strukturierte Daten aus, die Claude leicht parsen kann:

```json
{
  "FEATURE_DIR": "/path/to/.codexspec/specs/2026-0613-1200ab-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md"]
}
```

### 7.4 Progressive Validierung

Unterschiedliche Befehle nutzen unterschiedliche Parameter und validieren nach Bedarf:

| Phase | Befehl | Validierungs-Stufe |
|-------|--------|--------------------|
| Vor Planung | `/codexspec:clarify` | Nur Pfade |
| Nach Planung | `/codexspec:checklist` | plan.md |
| Nach Aufgaben | `/codexspec:analyze` | plan.md + tasks.md |

### 7.5 Git-Integration

- Automatische Extraktion der Feature-ID aus dem Branch-Namen
- Branch-Namen-Validierung (Format `^\d{3}-`)
- Umgebungsvariablen-Override unterstützt (`CODEXSPEC_FEATURE`)

## 8. Wichtige Code-Pfade

| Datei | Zeile/Position | Funktion |
|-------|----------------|----------|
| `src/codexspec/__init__.py` | 343–368 | Skript-Kopierlogik |
| `src/codexspec/__init__.py` | 71–90 | Pfad-Auflösung `get_scripts_dir()` |
| `scripts/bash/check-prerequisites.sh` | gesamte Datei | Bash-Voraussetzungs-Hauptskript |
| `scripts/powershell/check-prerequisites.ps1` | 56–146 | PowerShell-Voraussetzungs-Skript |
| `scripts/bash/common.sh` | gesamte Datei | Allgemeine Bash-Hilfsfunktionen |
| `scripts/powershell/common.ps1` | gesamte Datei | Allgemeine PowerShell-Hilfsfunktionen |
| `templates/commands/*.md` | YAML-Frontmatter | Skript-Deklaration |

## 9. Skript-Dateimanifest

### Bash-Skripte (`scripts/bash/`)

```
scripts/bash/
├── check-prerequisites.sh   # Voraussetzungs-Hauptskript
├── common.sh                # Allgemeine Hilfsfunktionen
└── create-new-feature.sh    # Neues Feature anlegen
```

### PowerShell-Skripte (`scripts/powershell/`)

```
scripts/powershell/
├── check-prerequisites.ps1  # Voraussetzungs-Hauptskript
├── common.ps1               # Allgemeine Hilfsfunktionen
└── create-new-feature.ps1   # Neues Feature anlegen
```

---

*Dieses Dokument hält die vollständige Architektur und den Verwendungsfluss der Skripte im CodexSpec-Projekt fest. Bei Aktualisierungen bitte entsprechend nachziehen.*

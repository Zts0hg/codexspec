# Scripts-Architekturanalyse

Dieses Dokument erlaeutert detailliert die Codelogik der Scripts im CodexSpec-Projekt und wie sie in Claude Code verwendet werden.

## 1. Gesamtarchitekturueberblick

CodexSpec ist ein **Spec-Driven Development (SDD)**-Toolkit mit einer Drei-Schichten-Architektur: CLI + Vorlagen + Hilfsskripte.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Benutzerebene (CLI)                       │
│  codexspec init | check | version | config                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code-Interaktionsebene                 │
│  /codexspec:specify | /codexspec:analyze | ...                  │
│  (.claude/commands/*.md)                                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Hilfsskriptebene                            │
│  .codexspec/scripts/*.sh (Bash) oder *.ps1 (PowerShell)         │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Skript-Bereitstellungsprozess

### Phase 1: `codexspec init` Initialisierung

In der `init()`-Funktion von `src/codexspec/__init__.py` (Zeilen 343-368) werden basierend auf dem Betriebssystem die entsprechenden Skripte kopiert:

```python
# Hilfsskripte basierend auf Plattform kopieren
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

**Ergebnis**: Basierend auf dem Betriebssystem werden Skripte aus `scripts/bash/` oder `scripts/powershell/` in das Projektverzeichnis `.codexspec/scripts/` kopiert.

### Pfadaufloesungsmechanismus

Die Funktion `get_scripts_dir()` (Zeilen 71-90) behandelt mehrere Installationsszenarien:

```python
def get_scripts_dir() -> Path:
    # Pfad 1: Wheel-Installation - Skripte im codexspec-Paket verpackt
    installed_scripts = Path(__file__).parent / "scripts"
    if installed_scripts.exists():
        return installed_scripts

    # Pfad 2: Entwicklungs-/Editable-Installation - Skripte im Projekt-Root
    dev_scripts = Path(__file__).parent.parent.parent / "scripts"
    if dev_scripts.exists():
        return dev_scripts

    # Pfad 3: Fallback
    return installed_scripts
```

## 3. Skript-Aufrufmechanismus in Claude Code

### Kernmechanismus: YAML-Frontmatter-Deklaration

Vorlagendateien deklarieren Skriptabhaengigkeiten durch YAML-Frontmatter:

```yaml
---
description: Befehlsbeschreibung
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---
```

### Platzhalterersetzung

Verwendung von `{SCRIPT}`-Platzhaltern in Vorlagen:

```markdown
### 1. Kontext initialisieren

Fuehren Sie `{SCRIPT}` vom Repository-Root aus und parsen Sie JSON fuer:
- `FEATURE_DIR` - Feature-Verzeichnispfad
- `AVAILABLE_DOCS` - Liste verfuegbarer Dokumente
```

### Aufrufablauf

1. Benutzer gibt `/codexspec:analyze` in Claude Code ein
2. Claude liest die Vorlage `.claude/commands/codexspec:analyze.md`
3. Basierend auf dem Betriebssystem ersetzt Claude `{SCRIPT}` durch:
   - **macOS/Linux**: `.codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks`
   - **Windows**: `.codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks`
4. Claude fuehrt das Skript aus, parst die JSON-Ausgabe und setzt den Vorgang fort

## 4. Skript-Funktionsdetails

### 4.1 `check-prerequisites.sh/ps1` - Vorauspruefungsskript

Dies ist das wichtigste Skript zur Validierung des Umgebungszustands und zur Rueckgabe strukturierter Informationen.

#### Kernfunktionen

- Validierung, ob sich in einem Feature-Branch (Format: `001-feature-name`)
- Erkennung, ob erforderliche Dateien existieren (`plan.md`, `tasks.md`)
- Rueckgabe von Pfadinformationen im JSON-Format

#### Parameteroptionen

| Parameter | Bash | PowerShell | Funktion |
|------|------|------------|------|
| JSON-Ausgabe | `--json` | `-Json` | JSON-Format ausgeben |
| tasks.md erforderlich | `--require-tasks` | `-RequireTasks` | Vorhandensein von tasks.md validieren |
| tasks.md einbeziehen | `--include-tasks` | `-IncludeTasks` | tasks.md in AVAILABLE_DOCS einbeziehen |
| Nur Pfade | `--paths-only` | `-PathsOnly` | Validierung ueberspringen, nur Pfade ausgeben |

#### JSON-Ausgabebeispiel

```json
{
  "FEATURE_DIR": "/path/to/.codexspec/specs/001-my-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md", "tasks.md"]
}
```

### 4.2 `common.sh/ps1` - Allgemeine Hilfsfunktionen

Bietet plattformuebergreifende allgemeine Funktionen:

#### Bash-Funktionen

| Funktion | Aufgabe |
|------|------|
| `get_feature_id()` | Feature-ID aus Git-Branch oder Umgebungsvariable abrufen |
| `get_specs_dir()` | specs-Verzeichnispfad abrufen |
| `is_codexspec_project()` | Pruefen, ob in CodexSpec-Projekt |
| `require_codexspec_project()` | Sicherstellen, dass in CodexSpec-Projekt, sonst beenden |
| `log_info/success/warning/error()` | Farbierte Log-Ausgabe |
| `command_exists()` | Pruefen, ob Befehl existiert |

#### PowerShell-Funktionen

| Funktion | Aufgabe |
|------|------|
| `Get-RepoRoot` | Git-Repository-Root-Verzeichnis abrufen |
| `Get-CurrentBranch` | Aktuellen Branch-Namen abrufen |
| `Test-HasGit` | Erkennen, ob Git-Repository vorhanden |
| `Test-FeatureBranch` | Validieren, ob in Feature-Branch |
| `Get-FeaturePathsEnv` | Alle Feature-bezogenen Pfade abrufen |
| `Test-FileExists` | Pruefen, ob Datei existiert |
| `Test-DirHasFiles` | Pruefen, ob Verzeichnis Dateien enthaelt |

### 4.3 `create-new-feature.sh/ps1` - Neues Feature erstellen

#### Funktionen

- Automatische Generierung inkrementeller Feature-IDs (001, 002, ...)
- Erstellung des Feature-Verzeichnisses und der initialen spec.md
- Erstellung des entsprechenden Git-Branch

#### Verwendungsbeispiel

```bash
./create-new-feature.sh -n "user authentication" -i 001
```

## 5. Skripte verwendende Befehle

Die folgenden 4 Befehle verwenden Skripte:

| Befehl | Skript-Parameter | Funktion |
|------|--------------|------|
| `/codexspec:clarify` | `--json --paths-only` | Pfade abrufen, Dateien nicht validieren |
| `/codexspec:checklist` | `--json` | Vorhandensein von plan.md validieren |
| `/codexspec:analyze` | `--json --require-tasks --include-tasks` | plan.md + tasks.md validieren |
| `/codexspec:tasks-to-issues` | `--json --require-tasks --include-tasks` | plan.md + tasks.md validieren |

## 6. Vollstaendiges Workflow-Diagramm

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        Initialisierungsphase                              │
│                                                                          │
│  $ codexspec init mein-projekt                                           │
│       │                                                                  │
│       ├── .codexspec/-Verzeichnisstruktur erstellen                      │
│       ├── scripts/*.sh → .codexspec/scripts/ kopieren                   │
│       ├── templates/commands/*.md → .claude/commands/ kopieren          │
│       └── constitution.md, config.yml, CLAUDE.md erstellen              │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────┐
│                        Verwendungsphase (Claude Code)                     │
│                                                                          │
│  Benutzer: /codexspec:analyze                                            │
│       │                                                                  │
│       ├── Claude liest .claude/commands/codexspec:analyze.md             │
│       │                                                                  │
│       ├── YAML-Frontmatter-Skriptdeklaration parsen                      │
│       │   scripts:                                                       │
│       │     sh: .codexspec/scripts/check-prerequisites.sh --json ...    │
│       │                                                                  │
│       ├── {SCRIPT}-Platzhalter ersetzen                                  │
│       │                                                                  │
│       ├── Skript ausfuehren:                                             │
│       │   $ .codexspec/scripts/check-prerequisites.sh --json ...        │
│       │                                                                  │
│       ├── JSON-Ausgabe parsen:                                           │
│       │   {"FEATURE_DIR": "...", "AVAILABLE_DOCS": [...]}               │
│       │                                                                  │
│       ├── spec.md, plan.md, tasks.md lesen                               │
│       │                                                                  │
│       └── Analysebericht generieren                                      │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## 7. Design-Highlights

### 7.1 Plattformuebergreifende Kompatibilitaet

Gleichzeitige Wartung von Bash- und PowerShell-Versionen, automatische Auswahl durch `sys.platform`:

```python
if sys.platform == "win32":
    # PowerShell-Skripte kopieren
else:
    # Bash-Skripte kopieren
```

### 7.2 Deklarative Konfiguration

Skriptabhaengigkeiten durch YAML-Frontmatter deklarieren, klar und intuitiv:

```yaml
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json
```

### 7.3 JSON-Ausgabe

Skripte geben strukturierte Daten aus, einfach von Claude zu parsen:

```json
{
  "FEATURE_DIR": "/path/to/.codexspec/specs/001-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md"]
}
```

### 7.4 Progressive Validierung

Verschiedene Befehle verwenden verschiedene Parameter, validieren nach Bedarf:

| Phase | Befehl | Validierungsstufe |
|------|------|----------|
| Vor Planung | `/codexspec:clarify` | Nur Pfade |
| Nach Planung | `/codexspec:checklist` | plan.md |
| Nach Aufgaben | `/codexspec:analyze` | plan.md + tasks.md |

### 7.5 Git-Integration

- Automatische Extraktion der Feature-ID aus dem Branch-Namen
- Unterstuetzung Branch-Namensvalidierung (`^\d{3}-` Format)
- Unterstuetzung Umgebungsvariablen-Ueberschreibung (`SPECIFY_FEATURE` / `CODEXSPEC_FEATURE`)

## 8. Wichtige Codepfade

| Datei | Zeilennummer/Position | Funktion |
|------|-----------|------|
| `src/codexspec/__init__.py` | 343-368 | Skript-Kopierlogik |
| `src/codexspec/__init__.py` | 71-90 | `get_scripts_dir()` Pfadaufloesung |
| `scripts/bash/check-prerequisites.sh` | Gesamte Datei | Bash-Vorauspruefungshauptskript |
| `scripts/powershell/check-prerequisites.ps1` | 56-146 | PowerShell-Vorauspruefungsskript |
| `scripts/bash/common.sh` | Gesamte Datei | Bash-Allgemeine Hilfsfunktionen |
| `scripts/powershell/common.ps1` | Gesamte Datei | PowerShell-Allgemeine Hilfsfunktionen |
| `templates/commands/*.md` | YAML-Frontmatter | Skriptdeklaration |

## 9. Skriptdateiliste

### Bash-Skripte (`scripts/bash/`)

```
scripts/bash/
├── check-prerequisites.sh   # Vorauspruefungshauptskript
├── common.sh                # Allgemeine Hilfsfunktionen
└── create-new-feature.sh    # Neues Feature erstellen
```

### PowerShell-Skripte (`scripts/powershell/`)

```
scripts/powershell/
├── check-prerequisites.ps1  # Vorauspruefungshauptskript
├── common.ps1               # Allgemeine Hilfsfunktionen
└── create-new-feature.ps1   # Neues Feature erstellen
```

---

*Dieses Dokument protokolliert die vollstaendige Architektur und Verwendung von Scripts im CodexSpec-Projekt. Bei Aktualisierungen bitte同步aendern.*

# CLI-Referenz

## Befehle

### `codexspec init`

Ein neues CodexSpec-Projekt initialisieren.

```bash
codexspec init [PROJECT_NAME] [OPTIONEN]
```

**Argumente:**

| Argument | Beschreibung |
|----------|-------------|
| `PROJECT_NAME` | Name für Ihr neues Projektverzeichnis (`.` oder `--here` für das aktuelle Verzeichnis) |

**Optionen:**

| Option | Kurz | Beschreibung |
|--------|------|-------------|
| `--here` | `-h` | Im aktuellen Verzeichnis initialisieren |
| `--ai` | `-a` | Zu verwendender AI-Assistent: `claude`, `codex` oder `both` (Standard: claude) |
| `--lang` | `-l` | Basis-Ausgabesprache; interaction/document/commit fallen darauf zurück (z. B. en, zh-CN, ja) |
| `--interaction-lang` | | Interaktionssprache (LLM-Dialog + `codexspec` CLI-Ausgabe); überschreibt `--lang` |
| `--document-lang` | | Dokumentensprache (generierte Anforderungen/Spec/Plan/Tasks); überschreibt `--lang` |
| `--commit-lang` | | Commit-Nachrichten-Sprache; überschreibt `--lang` |
| `--force` | `-f` | Vorhandene Dateien überschreiben und Prompts automatisch bestätigen; `config.yml` wird nie neu erzeugt |
| `--no-git` | | Git-Repository-Initialisierung überspringen |
| `--debug` | `-d` | Debug-Ausgabe aktivieren |

`--lang` legt die Basis-Sprache `output` fest; `--interaction-lang`, `--document-lang` und `--commit-lang` überschreiben sie für ihre jeweilige Dimension (jede fällt auf `output`, dann auf `en` zurück). Siehe [Internationalisierung](../user-guide/i18n.md) für das vollständige Modell.

Die erstmalige Initialisierung in einem TTY ohne `--lang` (und ohne alle drei Dimensions-Flags) fragt nach einer Basissprache; in einem Nicht-TTY (CI/Skripte) wird standardmäßig `en` verwendet – **vollständig nicht-interaktiv**. Ein erneuter `init`-Aufruf behält jeden Sprach-Schlüssel bei, den Sie nicht angegeben haben; `--force` erzeugt `config.yml` nie neu.

**Beispiele:**

```bash
# Neues Projekt erstellen
codexspec init my-project

# Im aktuellen Verzeichnis initialisieren
codexspec init . --ai claude

# Einmalige Verwendung (ohne Installation) – für Codex CLI oder both initialisieren
uvx codexspec init . --ai codex
uvx codexspec init . --ai both

# Vollständig nicht-interaktiv: zh-CN-Basis, englische Commit-Nachrichten
codexspec init my-project --lang zh-CN --commit-lang en

# Jede Dimension explizit festlegen (skriptbar, keine Prompts)
codexspec init my-project \
  --interaction-lang zh-CN --document-lang en --commit-lang en
```

---

### `codexspec check`

Auf installierte Tools prüfen.

```bash
codexspec check
```

---

### `codexspec version`

Versionsinformationen anzeigen.

```bash
codexspec version
```

---

### `codexspec config`

Projektkonfiguration anzeigen oder ändern.

```bash
codexspec config [OPTIONEN]
```

**Optionen:**

| Option | Kurz | Beschreibung |
|--------|------|-------------|
| `--set-lang` | `-l` | Die Basis-Ausgabesprache festlegen |
| `--set-interaction-lang` | | Die Interaktionssprache festlegen (LLM-Dialog + CLI-Ausgabe) |
| `--set-document-lang` | | Die Dokumentensprache festlegen (generierte Spec/Plan/Tasks) |
| `--set-commit-lang` | `-c` | Die Commit-Nachrichten-Sprache festlegen |
| `--list-langs` | | Alle unterstützten Sprachen auflisten |
| `--auto-next` | | `workflow.auto_next` umschalten/setzen (bare schaltet um; oder on/off) |

Jedes `--set-*-lang` aktualisiert eine [Sprach-Dimension](../user-guide/i18n.md); jede Dimension, die Sie nicht festlegen, fällt auf `output`, dann auf `en` zurück.

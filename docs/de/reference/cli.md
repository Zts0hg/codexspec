# CLI-Referenz

## Befehle

### `codexspec init`

Ein neues CodexSpec-Projekt initialisieren.

```bash
codexspec init [PROJEKT_NAME] [OPTIONEN]
```

**Argumente:**

| Argument | Beschreibung |
|----------|-------------|
| `PROJEKT_NAME` | Name fuer Ihr neues Projektverzeichnis (`.` oder `--here` fuer das aktuelle Verzeichnis) |

**Optionen:**

| Option | Kurz | Beschreibung |
|--------|------|-------------|
| `--here` | `-h` | Im aktuellen Verzeichnis initialisieren |
| `--ai` | `-a` | Zu verwendender KI-Assistent (Standard: claude) |
| `--lang` | `-l` | Basis-Ausgabesprache; interaction/document/commit fallen darauf zurueck (z.B. en, zh-CN, ja) |
| `--interaction-lang` | | Interaktionssprache (LLM-Dialog + `codexspec` CLI-Ausgabe); ueberschreibt `--lang` |
| `--document-lang` | | Dokumentensprache (generierte Anforderungen/Spec/Plan/Tasks); ueberschreibt `--lang` |
| `--commit-lang` | | Commit-Nachrichten-Sprache; ueberschreibt `--lang` |
| `--force` | `-f` | Vorhandene Dateien ueberschreiben und Prompts automatisch bestätigen; `config.yml` wird nie neu erzeugt |
| `--no-git` | | Git-Repository-Initialisierung ueberspringen |
| `--debug` | `-d` | Debug-Ausgabe aktivieren |

`--lang` legt die Basis-Ausgabesprache `output` fest; `--interaction-lang`, `--document-lang` und `--commit-lang` ueberschreiben sie fuer ihre jeweilige Dimension (jede faellt auf `output`, dann auf `en` zurueck). Siehe [Internationalisierung](../user-guide/i18n.md) fuer das vollstaendige Modell.

Die erstmalige Initialisierung in einem TTY ohne `--lang` (und ohne alle drei Dimensions-Flags) fragt nach einer Basissprache; in einem Nicht-TTY (CI/Skripte) wird standardmaessig `en` verwendet — **vollstaendig nicht-interaktiv**. Ein erneuter `init`-Aufruf behaelt jeden Sprach-Schluessel bei, den Sie nicht angegeben haben; `--force` erzeugt `config.yml` nie neu.

**Beispiele:**

```bash
# Neues Projekt erstellen
codexspec init mein-projekt

# Im aktuellen Verzeichnis initialisieren
codexspec init . --ai claude

# Vollstaendig nicht-interaktiv: zh-CN-Basis, englische Commit-Nachrichten
codexspec init mein-projekt --lang zh-CN --commit-lang en

# Jede Dimension explizit festlegen (skriptbar, keine Prompts)
codexspec init mein-projekt \
  --interaction-lang zh-CN --document-lang en --commit-lang en
```

---

### `codexspec check`

Auf installierte Tools pruefen.

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

Projektkonfiguration anzeigen oder aendern.

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
| `--list-langs` | | Alle unterstuetzten Sprachen auflisten |

Jedes `--set-*-lang` aktualisiert eine [Sprach-Dimension](../user-guide/i18n.md); jede Dimension, die Sie nicht festlegen, faellt auf `output`, dann auf `en` zurueck.

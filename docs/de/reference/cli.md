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
| `PROJEKT_NAME` | Name fuer Ihr neues Projektverzeichnis |

**Optionen:**

| Option | Kurz | Beschreibung |
|--------|------|-------------|
| `--here` | `-h` | Im aktuellen Verzeichnis initialisieren |
| `--ai` | `-a` | Zu verwendender KI-Assistent (Standard: claude) |
| `--lang` | `-l` | Ausgabesprache (z.B. en, zh-CN, ja) |
| `--force` | `-f` | Ueberschreiben vorhandener Dateien erzwingen |
| `--no-git` | | Git-Initialisierung ueberspringen |
| `--debug` | `-d` | Debug-Ausgabe aktivieren |

**Beispiele:**

```bash
# Neues Projekt erstellen
codexspec init mein-projekt

# Im aktuellen Verzeichnis initialisieren
codexspec init . --ai claude

# Mit deutscher Ausgabe
codexspec init mein-projekt --lang de
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
| `--set-lang` | `-l` | Die Ausgabesprache festlegen |
| `--list-langs` | | Alle unterstuetzten Sprachen auflisten |

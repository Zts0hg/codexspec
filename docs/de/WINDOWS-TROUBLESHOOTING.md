# Windows-Problembehebung

Dieser Leitfaden hilft Windows-Nutzern bei der Lösung häufiger Probleme bei der Installation und Ausführung von CodexSpec.

## Problem: „spawn codexspec access denied" (OSError 5) in CMD

### Symptome

- Das Ausführen von `codexspec --version` oder `codexspec init` in CMD schlägt mit „Access denied" oder „spawn codexspec access denied (OSError 5)" fehl
- Dieselben Befehle funktionieren in PowerShell korrekt

### Ursache

Verursacht wird dies durch Unterschiede, wie Windows-CMD und PowerShell Benutzer-Umgebungsvariablen behandeln:

1. **Aktualisierung der PATH-Umgebungsvariablen**: Wenn uv codexspec installiert, fügt es `%USERPROFILE%\.local\bin` zum Benutzer-PATH hinzu. PowerShell erkennt das normalerweise sofort, während CMD die Umgebungsvariablen möglicherweise erst nach einem Terminal-Neustart aktualisiert.

2. **Unterschiede bei der Prozesserzeugung**: CMD verwendet die Windows-CreateProcess-API, während PowerShell einen anderen Mechanismus nutzt, der bei Pfad-Auflösungsproblemen toleranter sein kann.

### Lösungen

#### Lösung 1: PowerShell verwenden (Empfohlen)

Die einfachste Lösung ist, PowerShell statt CMD zu verwenden:

```powershell
# codexspec in PowerShell installieren und ausführen
uv tool install codexspec
codexspec --version
```

#### Lösung 2: CMD neu starten

Schließen Sie alle CMD-Fenster und öffnen Sie ein neues. Das zwingt CMD, die Umgebungsvariablen neu zu laden.

#### Lösung 3: PATH in CMD manuell aktualisieren

```cmd
# Das bin-Verzeichnis von uv für die aktuelle Session zum PATH hinzufügen
set PATH=%PATH%;%USERPROFILE%\.local\bin

# Überprüfen
codexspec --version
```

#### Lösung 4: Vollständigen Pfad verwenden

```cmd
# codexspec mit vollständigem Pfad ausführen
%USERPROFILE%\.local\bin\codexspec.exe --version
```

#### Lösung 5: Dauerhaft zum System-PATH hinzufügen

1. **Systemeigenschaften** → **Umgebungsvariablen** öffnen
2. `Path` in **Benutzervariablen** oder **Systemvariablen** suchen
3. Hinzufügen: `%USERPROFILE%\.local\bin`
4. Auf OK klicken und alle Terminals neu starten

#### Lösung 6: pipx statt uv tool verwenden

Wenn uv weiterhin Probleme bereitet, verwenden Sie pipx als Alternative:

```cmd
# pipx installieren
pip install pipx
pipx ensurepath

# CMD neu starten, dann codexspec installieren
pipx install codexspec

# Überprüfen
codexspec --version
```

## Diagnose-Schritte

Um das Problem zu diagnostizieren, führen Sie diese Befehle in CMD aus:

```cmd
# Prüfen, ob das bin-Verzeichnis von uv im PATH ist
echo %PATH% | findstr ".local\bin"

# Prüfen, ob die codexspec-Executable existiert
dir %USERPROFILE%\.local\bin\codexspec.*

# Versuch mit vollständigem Pfad
%USERPROFILE%\.local\bin\codexspec.exe --version
```

## Häufige Probleme

### Problem: „uv is not recognized"

**Ursache**: uv ist nicht installiert oder nicht im PATH.

**Lösung**:

```powershell
# uv mit PowerShell installieren
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Terminal neu starten und überprüfen
uv --version
```

### Problem: „python is not recognized"

**Ursache**: Python ist nicht installiert oder nicht im PATH.

**Lösung**:

1. Python 3.11+ von [python.org](https://www.python.org/downloads/) installieren
2. Während der Installation „Add Python to PATH" aktivieren
3. Terminal neu starten

### Problem: Antivirus blockiert die Ausführung

**Symptome**: codexspec funktioniert kurz und stoppt dann oder zeigt intermittierende Fehler.

**Lösung**: codexspec zur Whitelist Ihres Antivirus hinzufügen:

- **Windows Defender**: Einstellungen → Update & Sicherheit → Windows-Sicherheit → Viren- & Bedrohungsschutz → Einstellungen verwalten → Ausschlüsse
- Pfad hinzufügen: `%USERPROFILE%\.local\bin\codexspec.exe`

## Verwandte Ressourcen

- [uv GitHub Issue #16747](https://github.com/astral-sh/uv/issues/16747) – Bekannte Windows-Berechtigungsprobleme mit uv
- [uv Windows-Installationsanleitung](https://docs.astral.sh/uv/getting-started/installation/)
- [pipx-Dokumentation](https://pypa.github.io/pipx/) – Alternativer Python-Anwendungs-Installer

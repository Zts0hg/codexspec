# Windows-Problemloesungshandbuch

Dieses Handbuch hilft Windows-Benutzern bei der Loesung haeufiger Probleme bei der Installation und Ausfuehrung von CodexSpec.

## Problem: "spawn codexspec access denied" (OSError 5) in CMD

### Symptome

- Das Ausfuehren von `codexspec --version` oder `codexspec init` in CMD schlaegt mit "Access denied" oder "spawn codexspec access denied (OSError 5)" fehl
- Dieselben Befehle funktionieren in PowerShell korrekt

### Ursache

Dies wird durch Unterschiede in der Behandlung von Benutzerumgebungsvariablen zwischen Windows CMD und PowerShell verursacht:

1. **Aktualisierung der PATH-Umgebungsvariable**: Wenn uv codexspec installiert, fuegt es `%USERPROFILE%\.local\bin` zum Benutzer-PATH hinzu. PowerShell erkennt dies normalerweise sofort, waehrend CMD die Umgebungsvariablen moeglicherweise erst nach einem Neustart des Terminals aktualisiert.

2. **Unterschiede bei der Prozess Erstellung**: CMD verwendet die Windows CreateProcess-API, waehrend PowerShell einen anderen Mechanismus verwendet, der toleranter gegenueber Pfadaufloesungsproblemen sein kann.

### Loesungen

#### Loesung 1: PowerShell verwenden (Empfohlen)

Die einfachste Loesung ist die Verwendung von PowerShell anstelle von CMD:

```powershell
# Installieren und ausfuehren von codexspec in PowerShell
uv tool install codexspec
codexspec --version
```

#### Loesung 2: CMD neu starten

Schliessen Sie alle CMD-Fenster und oeffnen Sie ein neues. Dies zwingt CMD, die Umgebungsvariablen neu zu laden.

#### Loesung 3: PATH in CMD manuell aktualisieren

```cmd
# Hinzufuegen des uv-bin-Verzeichnisses zum PATH fuer die aktuelle Sitzung
set PATH=%PATH%;%USERPROFILE%\.local\bin

# Ueberpruefen
codexspec --version
```

#### Loesung 4: Vollstaendigen Pfad verwenden

```cmd
# Ausfuehren von codexspec mit dem vollstaendigen Pfad
%USERPROFILE%\.local\bin\codexspec.exe --version
```

#### Loesung 5: Dauerhaft zum System-PATH hinzufuegen

1. Oeffnen Sie **Systemeigenschaften** → **Umgebungsvariablen**
2. Suchen Sie `Path` in **Benutzervariablen** oder **Systemvariablen**
3. Fuegen Sie hinzu: `%USERPROFILE%\.local\bin`
4. Klicken Sie auf OK und starten Sie alle Terminals neu

#### Loesung 6: pipx anstelle von uv tool verwenden

Wenn uv weiterhin Probleme hat, verwenden Sie pipx als Alternative:

```cmd
# pipx installieren
pip install pipx
pipx ensurepath

# CMD neu starten, dann codexspec installieren
pipx install codexspec

# Ueberpruefen
codexspec --version
```

## Ueberpruefungsschritte

Um das Problem zu diagnostizieren, fuehren Sie diese Befehle in CMD aus:

```cmd
# Pruefen, ob das uv-bin-Verzeichnis im PATH ist
echo %PATH% | findstr ".local\bin"

# Pruefen, ob die codexspec-Executable existiert
dir %USERPROFILE%\.local\bin\codexspec.*

# Versuch mit vollstaendigem Pfad
%USERPROFILE%\.local\bin\codexspec.exe --version
```

## Haeufige Probleme

### Problem: "uv is not recognized"

**Ursache**: uv ist nicht installiert oder nicht im PATH.

**Loesung**:
```powershell
# uv mit PowerShell installieren
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Terminal neu starten und ueberpruefen
uv --version
```

### Problem: "python is not recognized"

**Ursache**: Python ist nicht installiert oder nicht im PATH.

**Loesung**:
1. Installieren Sie Python 3.11+ von [python.org](https://www.python.org/downloads/)
2. Waehrend der Installation "Add Python to PATH" aktivieren
3. Terminal neu starten

### Problem: Antivirus blockiert die Ausfuehrung

**Symptome**: Codexspec funktioniert kurz und stoppt dann, oder zeigt intermittierende Fehler.

**Loesung**: Fuegen Sie codexspec zur Whitelist Ihres Antivirus hinzu:
- **Windows Defender**: Einstellungen → Update & Sicherheit → Windows-Sicherheit → Viren- & Bedrohungsschutz → Einstellungen verwalten → Ausschluesse
- Pfad hinzufuegen: `%USERPROFILE%\.local\bin\codexspec.exe`

## Verwandte Ressourcen

- [uv GitHub Issue #16747](https://github.com/astral-sh/uv/issues/16747) - Bekannte Windows-Berechtigungsprobleme mit uv
- [uv Windows-Installationsanleitung](https://docs.astral.sh/uv/getting-started/installation/)
- [pipx-Dokumentation](https://pypa.github.io/pipx/) - Alternativer Python-Anwendungsinstaller

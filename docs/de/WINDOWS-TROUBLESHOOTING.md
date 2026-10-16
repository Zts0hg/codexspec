# Windows-Fehlerbehebung

## Installation prüfen

Prüfen Sie in PowerShell, welche ausführbare Datei verwendet wird und ob die CLI startet. Der Versionsbefehl lautet `codexspec version`.

```powershell
Get-Command codexspec -All
codexspec version
codexspec check
```

## Befehl nicht gefunden

Fehlt uv, folgen Sie dessen Installationsanleitung. Wurde CodexSpec mit uv installiert, ist aber nicht in `PATH`, prüfen Sie das Verzeichnis der ausführbaren Dateien, aktualisieren Sie die Shell-Konfiguration und öffnen Sie ein neues Terminal. Starten Sie auch den Assistenten neu, falls er die alte Umgebung übernommen hat. Das Verzeichnis kann vom Standard abweichen; verwenden Sie den von uv gemeldeten Pfad.

```powershell
uv tool list
uv tool dir --bin
uv tool update-shell
```

[uv](https://docs.astral.sh/uv/getting-started/installation/) · [uv tool update-shell](https://docs.astral.sh/uv/reference/cli/#uv-tool-update-shell)

## Zugriff verweigert oder Start fehlgeschlagen

Eine Meldung über verweigerten Zugriff erklärt die Ursache noch nicht. Halten Sie den genauen Befehl, den Pfad der ausführbaren Datei, den Fehler und die Versionen fest. Prüfen Sie, ob die Datei vorhanden ist, ob eine andere Installation Vorrang hat und ob Dateirechte oder Sicherheitssoftware die Ausführung blockieren. Nutzen Sie auf verwalteten Geräten den freigegebenen administrativen Supportprozess. Vergleichen Sie PowerShell und CMD nur, um Umgebungsunterschiede einzugrenzen; ein Shell-Wechsel behebt nicht zwangsläufig die Ursache.

Wenn die CLI funktioniert, initialisieren Sie das ausgewählte Projekt mit der gewünschten Assistentenintegration. Voraussetzungen und das Aktualisieren bestehender Projekte beschreibt die Installationsanleitung.

[CodexSpec](getting-started/installation.md)

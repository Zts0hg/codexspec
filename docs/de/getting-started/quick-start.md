# Schnellstart

## 1. Projekt initialisieren

Nach der Installation erstellen oder initialisieren Sie Ihr Projekt:

```bash
# Neues Projekt erstellen
codexspec init mein-tolles-projekt

# Oder im aktuellen Verzeichnis initialisieren
codexspec init . --ai claude

# Mit chinesischer Ausgabe
codexspec init mein-projekt --lang zh-CN
```

## 2. Projektprinzipien festlegen

Starten Sie Claude Code im Projektverzeichnis:

```bash
cd mein-tolles-projekt
claude
```

Verwenden Sie den Constitution-Befehl:

```
/codexspec.constitution Erstelle Prinzipien mit Fokus auf Codequalitaet und Testing
```

## 3. Anforderungen klaeren

Verwenden Sie `/codexspec.specify` um Anforderungen zu erkunden:

```
/codexspec.specify Ich moechte eine Aufgabenverwaltungsanwendung erstellen
```

## 4. Spezifikation generieren

Nach der Klaerung generieren Sie das Spezifikationsdokument:

```
/codexspec.generate-spec
```

## 5. Ueberpruefen und Validieren

**Empfohlen:** Validieren Sie vor dem Fortfahren:

```
/codexspec.review-spec
```

## 6. Technischen Plan erstellen

```
/codexspec.spec-to-plan Verwende Python FastAPI fuer das Backend
```

## 7. Aufgaben generieren

```
/codexspec.plan-to-tasks
```

## 8. Implementieren

```
/codexspec.implement-tasks
```

## Projektstruktur

Nach der Initialisierung:

```
mein-projekt/
+-- .codexspec/
|   +-- memory/
|   |   +-- constitution.md
|   +-- specs/
|   |   +-- {feature-id}/
|   |       +-- spec.md
|   |       +-- plan.md
|   |       +-- tasks.md
|   +-- scripts/
+-- .claude/
|   +-- commands/
+-- CLAUDE.md
```

## Naechste Schritte

[Vollstaendiger Workflow-Leitfaden](../user-guide/workflow.md)

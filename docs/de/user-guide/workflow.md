# Workflow

<a id="core-workflow"></a>

## Kern-Workflow

Der Standard-Workflow für Features bewahrt eine durch Quellenverweise verknüpfte Kette:

```text
/specify          → requirements.md
/generate-spec    → spec.md       → review-spec
/spec-to-design   → design.md     → review-design
/design-to-plan   → plan.md       → review-plan
/plan-to-tasks    → tasks.md      → review-tasks → analyze
/implement-tasks  → implementation and complete-feature code review
```

Die folgenden Beispiele verwenden Claudes Präfix `/codexspec:`. Verwenden Sie in
Codex `$codexspec:` mit demselben Befehlsnamen und denselben Argumenten.

| Schritt | Befehl | Zweck und Ergebnis |
|------|---------|--------------------|
| Projektprinzipien | `/codexspec:constitution` | `constitution.md` erstellen oder aktualisieren und betroffene Artefakte validieren |
| Anforderungen | `/codexspec:specify <idea>` | Zielsetzung besprechen, die abschließende Zusammenfassung bestätigen und `requirements.md` dauerhaft speichern |
| Spezifikation | `/codexspec:generate-spec <feature-dir>` | Bestätigte Anforderungen mit Quellenverweisen in `spec.md` überführen |
| Systementwurf | `/codexspec:spec-to-design <feature-dir>` | `design.md` mit Komponenten, Schnittstellen und wesentlichen Entwurfsentscheidungen erstellen |
| Implementierungsplan | `/codexspec:design-to-plan <feature-dir>` | `plan.md` mit Phasen, Reihenfolge und Verifikation erstellen |
| Aufgaben | `/codexspec:plan-to-tasks <feature-dir>` | Nachvollziehbare, überprüfbare Aufgaben in `tasks.md` erstellen und die artefaktübergreifende Analyse ausführen |
| Implementierung | `/codexspec:implement-tasks <feature-dir>` | Aufgaben ausführen, Ergebnisse verifizieren und unabhängig bestätigte Review-Befunde beheben |

Ersetzen Sie `<feature-dir>` durch das Feature-Verzeichnis, das bei der
Anforderungsermittlung zurückgegeben wurde. Arbeiten Sie in dessen Worktree
weiter oder geben Sie seinen expliziten Pfad an. So beziehen sich alle Befehle
und Sitzungen weiterhin auf dasselbe Feature.

<a id="specify-clarify-and-analyze"></a>

### specify, clarify und analyze

- **specify** beginnt die Anforderungsermittlung oder nimmt sie wieder auf. Erst
  die explizite Bestätigung macht die Zusammenfassung der Anforderungen verbindlich.
- **clarify** klärt Mehrdeutigkeiten in vorhandenen Anforderungen und der
  Spezifikation. Pro Aufruf werden bis zu fünf Fragen aus vier Kategorien gestellt.
  Zuerst wird `requirements.md` aktualisiert, anschließend `spec.md` synchronisiert.
- **analyze** prüft die gesamte Kette Anforderungen → Spezifikation → Entwurf →
  Plan → Aufgaben. Es korrigiert nachgelagerte Artefakte automatisch, wenn sich
  die Korrektur eindeutig aus den maßgeblichen vorgelagerten Quellen ergibt.
  `requirements.md` wird niemals bearbeitet. Ungelöste Befunde werden gemeldet.
  Die Analyse läuft automatisch nach einem bestandenen Aufgaben-Review und dient
  der Information; sie ist kein Freigabekriterium für die Implementierung.

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

<a id="small-changes-with-quick"></a>

### Kleine Änderungen mit Quick

Nutzen Sie `quick` für kleine, klar abgegrenzte Änderungen, etwa eine punktuelle Korrektur:

```text
/codexspec:quick Fix the empty-state message on the task list
```

Quick bestätigt und speichert eine kompakte Zusammenfassung der Anforderungen.
Danach koordiniert es Spezifikation, Planung, Aufgaben und Implementierung
mitsamt den Reviews der Generierungsbefehle. Umfangreiche Änderungen oder noch
offene Produkt- und Entwurfsentscheidungen erfordern den Standard-Workflow.
Quick pausiert, sobald eine neue Entscheidung benötigt wird.

<a id="workflow-automation"></a>

### Workflow-Automatisierung

`workflow.auto_next` ist standardmäßig **false**. Steht es in der Konfiguration
des aktiven Arbeitsbereichs auf `true`, folgt auf die abschließende Bestätigung
der Anforderungen automatisch die Spezifikation. Jede Generierungsphase führt
nach `PASS` oder `PASS_WITH_WARNINGS` zur nächsten Phase. `NEEDS_REVISION` oder
`BLOCKED` hält die Kette an. Mit `implement-tasks` endet sie.

Artefakte werden automatisch nur bei verifizierten Fehlern korrigiert, deren
Behebung sich aus vorgelagerten Belegen ergibt. Dafür sind höchstens zwei
Korrektur- und Review-Runden vorgesehen. Empfehlungen werden separat behandelt.
Für die Review- und Korrekturschleife der Implementierung gelten eigene
Abschlussregeln, die weiter unten beschrieben sind.

<a id="shared-blueprint-and-autonomous-development"></a>

## Gemeinsamer Blueprint und autonome Entwicklung

Mit `blueprint` bereiten Sie mehrere bestätigte Anforderungen vor der Entwicklung
vor. Mit `auto-dev` lassen Sie diese Liste abarbeiten:

```text
/codexspec:blueprint Add a confirmed requirement for task reminders
/codexspec:auto-dev
```

Bei der Anforderungsermittlung für den Blueprint werden Richtung, Entscheidungen
und Einschränkungen, die der Benutzer festlegen muss, geklärt, bevor eine
Anforderung in die Liste aufgenommen wird. Die gemeinsame Datei
`.codexspec/blueprint.md` verwendet die Zustände `pending`, `in_progress` und
`completed`. Sie können ausstehende Anforderungen anhängen, ersetzen, löschen
oder neu anordnen. Aktive und abgeschlossene Einträge sind bei der
Blueprint-Pflege schreibgeschützt.

Auto-dev folgt der Reihenfolge im Dokument. Es setzt ein bereits begonnenes
Feature fort, bevor es ein weiteres beginnt, und liest die Liste nach jedem
Abschluss erneut. So können auch neu angehängte ausstehende Anforderungen in den
laufenden Durchgang aufgenommen werden. Es führt SDD-Phasen, Implementierung,
Verifikation, Reviews und Korrekturen innerhalb der bestätigten Anforderungen
aus. Ein Aufruf von `auto-dev` aktiviert diese Automatisierung unabhängig von
`workflow.auto_next`, ohne diese Einstellung zu ändern.

Beide Befehle nutzen `worktree-for-codexspec-auto-dev` auf dem Branch
`codexspec/auto-dev`. Unter den gemeinsamen Regeln zur Zuständigkeit und zum
Schreibschutz können sie gleichzeitig arbeiten. Die Anforderungen werden in
diesem Arbeitsbereich nacheinander entwickelt. Lässt sich eine Produktentscheidung
nicht aus den bestätigten Anforderungen ableiten, wird der Durchgang mit
entsprechenden Belegen angehalten. Während der normalen autonomen Ausführung
werden dazu keine Rückfragen gestellt.

Zeigen Sie den aktuellen gemeinsamen Blueprint an, ohne ihn zu ändern:

```bash
codexspec show-blueprint
```

<a id="worktree-development"></a>

## Entwicklung mit Worktrees

Ein Git-Worktree ist ein weiteres Arbeitsverzeichnis desselben Repositorys, in
dem ein eigener Branch ausgecheckt ist. CodexSpec nutzt standardmäßig einen
Worktree pro regulärem Feature. Er wird vor dem ersten Speichern von Anforderungen
angelegt und enthält sämtliche Dokumente, Implementierung, Tests und Korrekturen
des Features.

```text
projects/
├── my-project/
└── my-project-codexspec-worktrees/
    ├── <feature-id>-task-reminders/
    ├── <feature-id>-search/
    ├── worktree-for-codexspec-maintenance/
    └── worktree-for-codexspec-auto-dev/
```

Wenn Sie ein Feature fortsetzen, wird dessen Arbeitsbereich wiederverwendet.
Eigenständige Änderungen an Konfiguration, Projektverfassung und Profil erfolgen
im Wartungs-Worktree. Änderungen innerhalb eines aktiven Features bleiben in
dessen Worktree. Die Konfiguration gilt **lokal pro Checkout**: Eine Einstellung,
die in einem zugewiesenen Worktree geändert wird, wirkt zunächst dort und gelangt
über die Git-Integration in andere Checkouts. Führen Sie CLI-Befehle und Prüfungen
im zurückgegebenen Arbeitsbereich aus.

Für die Ausgangsbasis neuer Features wird der bereits in Commits gespeicherte
Verlauf des lokalen Hauptbranches mit dem abgerufenen Verlauf des entfernten
Hauptbranches anhand der Git-Abstammung verglichen. Bei auseinanderlaufenden
Verläufen erfolgt im neuen Worktree ein Merge, der verifiziert werden muss.
Schlägt der Abruf fehl, wird eine Warnung ausgegeben; lokal verfügbare Referenzen
dürfen dann verwendet werden. Schlägt die Erstellung fehl, wird nicht ersatzweise
in den Haupt-Checkout geschrieben.

`workflow.worktrees` ist standardmäßig **true**. Nur der wörtliche YAML-Wert
`false` deaktiviert die Isolation regulärer Features und Wartungsarbeiten.
Blueprint/auto-dev behalten unabhängig davon ihren festen gemeinsamen Worktree.
Initialisierung und Installationsaktualisierungen erfolgen in dem Checkout, den
Sie explizit auswählen. Abgeschlossene Worktrees bleiben erhalten; durch den
Abschluss werden sie weder automatisch zusammengeführt noch gelöscht.

Siehe [Entwicklung mit Worktrees](workflow.md#worktree-development)
und [Konfiguration](../reference/configuration.md#workflow-and-review-settings).

<a id="work-with-existing-code"></a>

## Mit bestehendem Code arbeiten

Für unterschiedliche Ziele gibt es zwei Einstiegspunkte:

| Befehl | Zweck | Ergebnis und Grenzen |
|---------|-----------|-----------------|
| `onboard [path]` | Wiederverwendbares Projektwissen aus einer bestehenden Codebasis aufbauen | Konventionseinträge mit Kandidatenstatus und nur eng gefasste und durch konkrete Belege gestützte Einschränkungen im Profil; der Code bleibt schreibgeschützt |
| `reverse-spec [path]` | Die vorhandene Architektur verstehen oder Code mit der bestätigten Zielsetzung vergleichen | Artefakte als Entwurf oder ein Abweichungsbericht; der Code bleibt schreibgeschützt |

```text
/codexspec:onboard src/
/codexspec:reverse-spec
/codexspec:reverse-spec src/auth
```

Onboard leitet Konventionen aus dem beobachtbaren Code ab und schlägt
Einschränkungen ausschließlich auf Grundlage expliziter Verbote vor.
Konventionseinträge mit Kandidatenstatus werden lokal sofort wirksam. Bei
Einschränkungen mit Kandidatenstatus ist in der Sitzung eine Entscheidung nötig:
speichern, bearbeiten oder verwerfen. Onboard bewahrt vorhandenes Wissen und
erfindet bei einer erstmaligen Untersuchung weder Begründungen früherer
Entscheidungen noch Erfahrungswissen über Fallstricke.

Reverse-spec bietet drei Modi:

- **Überblick**: Ohne Pfad oder bei Angabe des Repository-Stammverzeichnisses
  erstellt es einen knappen Architekturentwurf in `design.md` sowie `slices.md`
  zur Auswahl der zu untersuchenden Module.
- **Generieren**: Bei einem Modulpfad ohne bestätigte Ausgangsbasis entstehen
  Entwürfe von `spec.md`, `design.md` und offene oder abgeleitete Anforderungen.
- **Abgleichen**: Bei einem Modul mit bestätigter Ausgangsbasis entsteht
  `reconcile.md`. Es meldet undokumentiertes Verhalten, nicht implementierte
  Spezifikationen und semantische Abweichungen von der bestätigten Spezifikation
  und dem bestätigten Entwurf. Die Anforderungen bestimmen dabei die Zielsetzung.

Abgeleitete Entwürfe müssen von einem Menschen bestätigt werden, bevor sie als
Ausgangsbasis dienen können. Der Abgleich nennt die vorgeschlagene Vorgehensweise:
Code korrigieren, Dokumente aktualisieren oder die Zielsetzung klären. Er setzt
sie nicht automatisch um.

<a id="review-and-debugging"></a>

## Reviews und Debugging

Vier Artefakt-Reviewer prüfen Übereinstimmung mit den Vorgaben, Abdeckung,
Machbarkeit und interne Qualität: `review-spec`, `review-design`, `review-plan`
und `review-tasks`. Sie laufen nach der Generierung automatisch und lassen sich
auch manuell aufrufen. Ihre Berichte unterscheiden verifizierte Fehler von
nicht blockierenden Risikohinweisen und möglichen Verbesserungen des Entwurfs.
Sie enthalten außerdem eine Kompatibilitätsbewertung.

`review-code` bietet eine separate Fehlerprüfung für ausgewählte Änderungen als
Freigabekriterium (Defekt-Gate) sowie eine explizite Qualitätsbewertung des gesamten Codes:

```text
/codexspec:review-code --feature <feature-dir>
/codexspec:review-code --uncommitted
/codexspec:review-code --audit src/
```

Standardmäßig wird die vollständige Differenz des Feature-Branches geprüft:
Änderungen mit Commit, Änderungen im Staging-Bereich, Änderungen außerhalb des
Staging-Bereichs und nicht ignorierte unversionierte Änderungen. Sie können
explizit nur Änderungen mit Commit, Änderungen ohne Commit oder einen einzelnen
Commit als Prüfgrundlage auswählen. `--feature` ergänzt den Anforderungskontext,
ohne den Git-Prüfumfang einzuschränken. `--audit` bewertet die angegebenen Pfade
und erstellt eine beratende Bewertung statt eines Abschlussurteils.

Reviews laden gemeinsame Standards aus `.codexspec/review-code/` und wählen die
relevanten Verhaltensdimensionen sowie Prüfungen für Sprache und Framework aus.
Jeder Befund benötigt konkrete Belege, einen tatsächlich erreichbaren Auslöser,
eine Zuordnung zur ausgewählten Änderung und eine Beschreibung der Auswirkungen.
Der Reviewer meldet Fehler und belegte Wartungsempfehlungen, ohne Dateien zu
bearbeiten. Die Stelle, die die Korrektur ausführt, prüft diese Befunde unabhängig.

Bei Code-Aufgaben werden zuerst Tests geschrieben. Dokumentations- und
Konfigurationsaufgaben werden direkt umgesetzt und mit geeigneten Prüfungen
verifiziert. Nach Korrekturen kann ein inkrementelles Review die Prüfabdeckung
unveränderter Bereiche wiederverwenden. Für die endgültige Abnahme sind ein
frisches `PASS` für das vollständige Feature, vollständige Prüfabdeckung und
Verifikation sowie null anerkannte P0–P3-Fehler erforderlich. Belegte
Wartungsempfehlungen werden separat gemeldet.

`workflow.auto_maintenance` ist standardmäßig **true** und bestimmt, ob bei
Korrekturen auch verifizierte, kompatible Wartungsverbesserungen umgesetzt werden.
Wird es deaktiviert, werden diese Empfehlungen weiterhin gemeldet; Fehler müssen
weiterhin behoben und erforderliche Prüfungen weiterhin ausgeführt werden. Die
Einstellung ist unabhängig vom automatischen Phasenübergang und kein Argument
von `implement-tasks`.

Für Debugging, bei dem zuerst die Ursache untersucht wird:

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

Debug folgt der Reihenfolge Untersuchung → Musteranalyse → Prüfung einer
Einzelhypothese → Korrektur mit einem zuerst fehlschlagenden Test. Bei der
Implementierung wird diese Untersuchung hinzugezogen, wenn Korrekturen nicht
vorankommen, ein nicht trivialer Korrektheitsfehler nachvollzogen werden muss
oder Fehler derselben Ursachenklasse in mehreren Review-Runden wiederkehren.
Nach drei fehlgeschlagenen Korrekturen wird die Architektur neu bewertet.

Mit `checklist` prüfen Sie die Klarheit, Vollständigkeit und Konsistenz der Anforderungen:

```text
/codexspec:checklist Check the authentication requirements for completeness
```

Die [Befehlsreferenz](commands.md) erläutert die Auswahl des
Review-Umfangs, die Argumente und die Verfahren im Detail.

<a id="project-knowledge"></a>

## Projektwissen

Das Projektprofil speichert wiederverwendbares Wissen unter `.codexspec/profile/`:

| Kategorie | Inhalt |
|----------|----------|
| `constraints/` | Explizite Verbote und feste Grenzen; zuerst lesen |
| `conventions/` | Muster, Namensgebung und featureübergreifende Hinweise |
| `pitfalls/` | Erlebte Fallstricke, Ursachen, Lösungswege und Lehren |
| `decisions/` | Wiederverwendbare Entscheidungen zur Architektur und zu featureübergreifenden Fragen |
| `strategies/` | Signale dafür, dass ein anderer Arbeitsansatz nötig ist |
| `runbooks/` | Geordnete Verfahren und Wiederherstellung nach Fehlern |

`distill` erfasst wiederverwendbares Wissen aus der Arbeit. Die Zielsetzung eines
bestimmten Features bleibt in dessen Anforderungen, Entwurf und Plan. Init
installiert in CLAUDE.md und/oder AGENTS.md Hinweise, vor inhaltlicher Arbeit alle
Einschränkungen und das relevante Wissen zu lesen. Später hinzugefügtes Wissen
kann ohne erneute Initialisierung wirksam werden. Einträge mit Kandidatenstatus
werden vorsichtig verwendet. Geprüfte Einträge setzen verifizierte Ergebnisse und
menschliche Zustimmung voraus.

```text
/codexspec:distill Capture the reusable lessons from this work
/codexspec:distill review
/codexspec:evolve
```

Ein manuelles `distill review` oder ein direktes `distill`, bei dem kein neues
Material zu erfassen ist, öffnet einen lokalen Offline-Arbeitsbereich im Browser.
Dort können Sie Einträge überarbeiten, prüfen und bestätigen, verwerfen,
zurückstellen oder zusammenführen. Anschließend können Sie das endgültige Markdown
in der Vorschau ansehen und **Alle anwenden** auswählen. Bis zur Anwendung bleiben
die Entscheidungen in einem wiederherstellbaren Entwurf gespeichert.
Konfliktprüfungen verhindern eine teilweise Anwendung oder stillschweigendes
Überschreiben. Für Umgebungen ohne Browser gibt es eine explizite textbasierte Alternative.

`workflow.auto_distill` ist standardmäßig **true** und steuert drei Abschluss-Hooks:
erfolgreiches `implement-tasks`, über `commit-staged` ausgeführte Commits und die
Generierung durch `pr`. Eine Commit-Vorschau löst keine Erfassung aus.

Die installierten Projekthinweise fordern Agenten außerdem auf, wiederverwendbares
Wissen zu erfassen, sobald es entsteht: in gewöhnlichen Gesprächen, bei Korrekturen
außerhalb von SDD und während langer `implement-tasks`-Durchgänge. Diese Hinweise
gelten unabhängig von der Einstellung für Abschluss-Hooks. Die Erfassung am
Aufgabenende dient als letzte Absicherung.

Innerhalb einer Sitzung verarbeiten wiederholte Auslöser nur neues Material.
Über Sitzungen hinweg liest `distill` das Profil und überspringt bereits erfasstes
Wissen. Gibt es nichts Wiederverwendbares mehr, endet die Erfassung ohne
Schreibvorgang. Die automatische Erfassung öffnet niemals die manuelle Prüfung,
wartet nicht auf Menschen und blockiert nicht den aufrufenden Workflow.

`evolve` wählt nur geprüftes Wissen aus, das auch außerhalb des Projekts nützlich
ist, und erstellt daraus einen Befehls- oder Skill-Entwurf. Vor einem Push oder
dem Öffnen eines Beitrags-PRs zur menschlichen Prüfung holt es explizite Zustimmung ein.

Weitere Hinweise finden Sie unter [Projektwissen](commands.md#codexspecdistill).

<a id="reusing-historical-decisions"></a>

### Frühere Entscheidungen wiederverwenden

Bevor der Agent Sie zu einer Änderung befragt, liest er unter
`.codexspec/specs/` die Entwicklungsgeschichte der betroffenen Features nach.
Er prüft die bestätigten Entscheidungen in `requirements.md`, verfolgt spätere
Ergänzungen und ausdrücklich ersetzte Entscheidungen und zieht bei Bedarf
Entwurfsbegründungen oder Belege aus der Implementierung heran. Diese Vorbereitung
ist auch vor inhaltlichen Urteilen zu Entwurf, Implementierung, Debugging und
Reviews erforderlich – in gewöhnlichen Gesprächen ebenso wie in SDD-Workflows.

Die Zeitstempel der Feature-Verzeichnisse helfen dabei, die Reihenfolge der
Iterationen nachzuvollziehen. Ein neueres Dokument setzt eine ältere Entscheidung
nicht automatisch außer Kraft. Frühere, unveränderte Anforderungen bleiben gültig;
offene Vorschläge gelten nicht als bestätigte Zielsetzung. Die Recherche
beschränkt sich auf die aktuelle Aufgabe und endet, sobald genügend Hintergrund
vorliegt. Dieser wird in späteren Phasen weiterverwendet.

Wenn etwa eine Schnittstelle geändert werden soll, könnte ein Agent ohne
Kenntnis der Vorgeschichte fragen:

> „Wie soll dieses Feature mit Abwärtskompatibilität umgehen?“

Nach Prüfung der relevanten Entscheidungen und der aktuellen Implementierung
kann er stattdessen gezielt fragen:

> „Sie hatten bestätigt, dass die alte Schnittstelle erhalten bleiben soll.
> Die aktuelle Implementierung unterstützt sie weiterhin. Ich schlage vor,
> sie auch bei dieser Änderung beizubehalten. Soll es dabei bleiben?“

Bereits geklärte Informationen, die eindeutig weiterhin gelten, können ohne
erneute Nachfrage übernommen werden. Haben Sie bereits gesagt: „Entfernen Sie
die alte Schnittstelle bei dieser Änderung“, folgt der Agent dieser Entscheidung
und erläutert die Auswirkungen auf die Migration. **Ihre neueste explizite
Entscheidung hat immer Vorrang.** Die Historie hilft, gezieltere Fragen zu stellen
und Wiederholungen zu vermeiden.

Erneuern Sie bestehende Projektinstallationen, um diese Hinweise zu erhalten.

<a id="git-workflow"></a>

## Git-Workflow

```text
/codexspec:commit-staged -p
/codexspec:pr --spec <feature-dir>/spec.md
/codexspec:release-notes --from <ref> --to HEAD
/codexspec:tasks-to-issues <feature-dir>
```

- **commit-staged** analysiert den exakten Staging-Bereich und erstellt eine
  Nachricht gemäß Conventional Commits. Mit `-p` sehen Sie eine Vorschau, ohne
  einen Commit zu erstellen. Der aufrufende Workflow wählt die Dateien aus und
  übernimmt sie in den Staging-Bereich. Die autorisierte Ausführung nutzt die
  abgesicherte Laufzeitumgebung und prüft erneut, ob der tatsächlich im Commit
  gespeicherte Inhalt mit der Analyse übereinstimmt. Die Commit-Hinweise für
  Agenten gelten in gewöhnlichen Gesprächen sowie in SDD-, Blueprint- und
  auto-dev-Workflows. Die bloße Verfügbarkeit des Befehls ruft ihn weder auf noch
  autorisiert sie einen Commit.
- **pr** erstellt aus der Differenz eine strukturierte Beschreibung für einen
  GitHub-PR oder GitLab-MR. `--spec` ergänzt optional den Feature-Kontext. Dazu
  dient ein Dateipfad zu `spec.md` oder ein Name beziehungsweise Präfix eines
  Feature-Verzeichnisses, der zu dieser Datei aufgelöst wird. Standardmäßig wird
  Text zur Verwendung auf der Hosting-Plattform ausgegeben.
- **release-notes** erstellt aus dem Git-Verlauf einen Eintrag nach Keep a
  Changelog und einen Veröffentlichungstext. Der Standardabschnitt ist
  `[Unreleased]`; `--version` verwendet die angegebene Bezeichnung. Es übernimmt
  keine Dateien in den Staging-Bereich, erstellt keine Commits, erhöht keine
  Versionen, setzt keine Tags, veröffentlicht nichts und erstellt kein Release.
- **tasks-to-issues** erstellt GitHub-Issues aus bestehenden Aufgaben, einschließlich
  Abhängigkeiten und Abnahmekriterien. Es benötigt eine authentifizierte GitHub-CLI
  und prüft, ob das Issue-Repository dem konfigurierten Remote entspricht.

Für die direkte Commit-Vorschau und autorisierte Commits im aktuellen
Arbeitsverzeichnis sind Python 3.11+ und Git erforderlich. Die Laufzeitumgebung wird mit
CLI-Projekten installiert und mit dem Claude-Plugin ausgeliefert. Auch vom
Agenten erstellte Merges mit Inhaltsänderungen nutzen die Staging-Analyse.
Merges, die nur Historien verbinden, behalten die Standardnachricht von Git
bei; Baum und Eltern-Commits werden dennoch validiert. Fast-Forwards erstellen keinen Commit.

## Rückverfolgbarkeit und Fortsetzung

Die bestätigte `requirements.md` bestimmt die Absicht des Features. Darauf folgt die Kette `spec.md` → `design.md` → `plan.md` → `tasks.md`, ergänzt durch anwendbare Projektgrundsätze und geprüfte Repository-Fakten. Anforderungen haben stabile IDs, Spezifikationseinträge verweisen mit `Sources` auf ihre Quellen und nachgelagerte Arbeiten mit `Covers` auf ihre Abdeckung. Ein nachgelagertes Artefakt darf eine vorgelagerte Entscheidung nicht stillschweigend neu definieren. Widersprüchliche maßgebliche Quellen oder neue Produktentscheidungen müssen vom Nutzer geklärt werden. Ältere Features ohne Anforderungen weisen auf die fehlende ursprüngliche Bestätigung hin; bei fehlendem Entwurf gilt der dokumentierte Rückfallpfad.

Geben Sie bei mehrdeutiger Auswahl einen expliziten Feature-Pfad an. Befehle wählen nicht stillschweigend das neueste Verzeichnis. Das übergeordnete Worktree-Verzeichnis wird vom primären Repository abgeleitet, auch bei Aufrufen aus Unterverzeichnissen oder anderen verknüpften Worktrees. Bei Bare-Repositories ist es ein benachbartes Verzeichnis namens `<bare-repository-name>-codexspec-worktrees`. Eigenständige Wartung nutzt den Branch `codexspec/maintenance`.

Eine fehlgeschlagene Worktree-Vorbereitung behält ihre Identität für die Fortsetzung. Merges divergierender Ausgangshistorien müssen die Projektprüfungen bestehen, bevor Feature-Anforderungen geschrieben werden oder die Entwicklung beginnt. Schreibgeschützte Untersuchungen behalten ihre Quelle; Berichte nutzen den ermittelten Ausgabe-Checkout. Die Commit-Ausführung behält den ausgewählten Index und überträgt keine in main indexierten Änderungen in einen anderen Worktree. Fehlen einem neuen Worktree erforderliche installierte Ressourcen, initialisieren Sie zuerst dieses Ziel.

## Review-Modell

Reviews trennen drei Arten von Aussagen:

- **Fidelity-Mängel**: Konflikt mit einer autorisierenden Quelle oder fehlende geforderte Abdeckung.
- **Intrinsische Mängel**: das Artefakt ist intern widersprüchlich, nicht überprüfbar oder nicht durchführbar.
- **Risiko-Hinweise / Design-Möglichkeiten**: optionale Verbesserungen ohne Beweis für einen aktuellen Mangel.

Jeder Mangel muss seine Beweise, Position, Abweichung, Auswirkung und minimale Behebung identifizieren. Befunde mit derselben Ursache werden zusammengeführt. Hinweise beeinflussen Status, Score oder automatische Fixes nicht.

Der Review-Status ist:

- `PASS`: keine kritischen, Warn- oder Minor-Mängel.
- `PASS_WITH_WARNINGS`: nur Minor-Mängel verbleiben.
- `NEEDS_REVISION`: eine oder mehrere Warnungen verbleiben.
- `BLOCKED`: ein kritischer Konflikt verhindert zuverlässiges Fortfahren.

Der Kompatibilitäts-Score wird aus denselben klassifizierten Befunden abgeleitet statt aus festen Vorlagen-Abschnitten. Der Status ist autorisierend; der Score existiert für Integrationen, die noch eine Zahl erwarten.

## Begrenztes Auto-Review

Generierungsbefehle führen das passende Review automatisch aus. Das ist die **evidenzbasierte Review**-Disziplin in Aktion: Sie dürfen nur evidenzbasierte Mängel reparieren und für höchstens zwei Runden erneut prüfen. Sie stoppen früher bei `PASS` und stoppen für Nutzereingabe, wenn:

- eine autorisierende Quelle mit einer anderen Quelle konfligiert;
- ein Fix bestätigte Absicht ändern würde;
- das verbleibende Element eher ein Hinweis als ein Mangel ist;
- zwei Reparatur-Runden aufgebraucht sind.

Manuelle `/codexspec:review-*`-Befehle können jederzeit für einen frischen Bericht ausgeführt werden.

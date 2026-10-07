# Produktionsplan Berliner Wirtschaft

Web-Seite, die aus **Planungsjahr + Erscheinungsterminen** den kompletten
Produktionsplan des Magazins *Berliner Wirtschaft* rückwärts terminiert –
alle 24 Produktionsschritte je Heft, unter Berücksichtigung von Wochenenden,
Berliner Feiertagen und festen Ziel-Wochentagen.

Die Seite ersetzt die Excel-Vorlage `BW_2027_Produktionsplan_automatisierungsplan.xlsx`
(Blätter *Plan*, *Feiertage*, *Eingabe*, *Stammdaten*). Der Rechenkern ist eine
1:1-Portierung der dortigen LAMBDA-Funktion `fnPlantermin` und liefert für 2027
**exakt dieselben 240 Termine** wie die Excel.

## Benutzung

```
python3 build.py     # erzeugt index.html aus src/app.html
```

Danach `index.html` im Browser öffnen – kein Server, kein Build-Werkzeug,
keine Abhängigkeiten. Die Datei läuft auch von einem Netzlaufwerk oder als
GitHub Page. Alle Eingaben werden im Browser (localStorage) gespeichert.

## Als Webseite veröffentlichen (GitHub Pages)

`index.html` liegt im Wurzelverzeichnis und ist vollständig eigenständig –
GitHub Pages kann das Repository ohne Bauschritt ausliefern.

1. Im Repository **Settings → Pages** öffnen
2. Unter *Build and deployment* → *Source* **Deploy from a branch** wählen
3. Branch auswählen, Ordner `/ (root)`, **Save**
4. Nach ein bis zwei Minuten ist die Seite unter
   `https://<benutzer>.github.io/<repository>/` erreichbar

Die leere Datei `.nojekyll` schaltet die Jekyll-Verarbeitung ab, damit die
Dateien unverändert ausgeliefert werden.

**Wichtig zur Datenhaltung:** Auf GitHub Pages gibt es keine geteilte Ablage.
Jede Besucherin und jeder Besucher arbeitet in der eigenen Browser-Kopie;
Pläne, Aufgaben und Team werden nicht zwischen Rechnern abgeglichen. Für die
gemeinsame Arbeit im Team ist die veröffentlichte Artifact-Fassung mit
geteilter Datenbank gedacht. Nach einer Änderung an `src/app.html` immer
`python3 build.py` laufen lassen und `index.html` mit committen – Pages
liefert genau diese Datei aus.

## Aufbau

| Datei | Inhalt |
|---|---|
| `src/app.html` | Die komplette Anwendung: Styles, Markup, Rechenkern (einzige Quelle) |
| `build.py` | Verpackt `src/app.html` in ein vollständiges HTML-Dokument |
| `index.html` | Erzeugt – die auslieferbare Seite |

`src/app.html` ist bewusst ohne `<!doctype>`/`<html>`/`<head>`/`<body>` geschrieben,
damit dieselbe Quelle als eigenständige Seite **und** als eingebettetes Artifact läuft.

## Gestaltung

Die Seite folgt dem Corporate Design der IHK-Organisation: Hausfarbe ist
IHK-Blau (Pantone 294, hier `#003087`), die Produktionsphasen tragen die
Sekundärtöne der IHK-Geschäftsfelder (Pantone Orange 021, 376, Rot 032), für
Fließtext auf lesbaren Kontrast abgedunkelt. Der Zeitschriftenkopf zitiert den
Bogen aus dem IHK-Zeichen als abstraktes Motiv – kein Nachbau des Logos.
Schriften: Newsreader für Überschriften und den Titelkopf, Archivo für die
Oberfläche, IBM Plex Mono für alle Datumsangaben.

Sämtliche Markenwerte stehen als CSS-Variablen im Block `:root` ganz oben in
`src/app.html` (`--ihk-blau`, `--ihk-orange`, `--ihk-gruen`, `--ihk-rot`,
`--sans`, `--serif`). Wer die verbindlichen Hausfarben oder die Hausschrift
zur Hand hat, tauscht sie dort an einer Stelle aus.

## Rechenregel

Jeder Schritt ist definiert durch **Anker**, **Versatz**, **Ziel-Wochentag** und
**Suchrichtung**:

1. `Basis = Termin des Ankerschritts + Versatz` (Kalendertage).
   Schritt 24 (E-Tag) ist die Wurzel und rechnet vom Erscheinungstermin.
2. Ist die Basis ein Wochenende, ein Feiertag oder – bei festem Ziel-Wochentag –
   der falsche Wochentag, wird der nächste zulässige Tag gesucht:
   * `Richtung = rückwärts` (Standard): letzter zulässiger Tag ≤ Basis
   * `Richtung = vorwärts`: erster zulässiger Tag ≥ Basis (nur Schritt 7)
3. Bei festem Ziel-Wochentag zählen nur Tage dieses Wochentags, die kein
   Feiertag sind; bei „flexibel“ jeder Arbeitstag (Mo–Fr, kein Feiertag).

Der Erscheinungstermin selbst wird vorab auf den letzten Arbeitstag gezogen,
falls er auf ein Wochenende oder einen Feiertag fällt.

Anker, Versatz, Ziel-Wochentag, Richtung und Phase sind im Reiter **Regelwerk**
frei änderbar; Zirkelbezüge werden erkannt und gemeldet.

## Pläne, Aufgaben und Freigabe

Die Seite verwaltet **mehrere Pläne**. Jeder Plan hat eine Bezeichnung, ein
Jahr und einen Status (*In Arbeit* oder *Freigegeben*) und speichert seine
kompletten Eingaben – Erscheinungstermine, Feiertagsauswahl, Regelwerk und
manuelle Termine. Über *Duplizieren* entsteht aus dem laufenden Jahr die
Vorlage für das nächste; die Aufgaben werden mitkopiert und auf offen
zurückgesetzt.

Im Reiter **Aufgaben** wird festgehalten, was für einen Plan zu erledigen ist.
Jede Aufgabe gehört zu einer Abteilung und wahlweise zu einer Person. Beide
Auswahlfelder legen über ihren letzten Eintrag *+ Neue …* direkt einen neuen
Eintrag an; umbenennen und entfernen lassen sich Abteilungen und Personen
unter *Abteilungen & Personen*. Eine Aufgabe lässt sich an einen
Produktionsschritt und eine Ausgabe koppeln – dann übernimmt sie deren
berechneten Termin als Fälligkeit und wandert mit, wenn sich der Plan
verschiebt. Überfällige Aufgaben sind rot markiert.

**Sind alle Aufgaben erledigt, gilt der Plan als freigegeben**: Er wird gegen
weitere Änderungen gesperrt, mit Datum abgelegt und steht im Reiter *Pläne*
unter *Aktueller Plan*. Beim nächsten Öffnen der Seite ist er die
Standardansicht. Über *Entsperren* geht er zurück in Arbeit.

### Wo die Daten liegen

| Umgebung | Ablage |
|---|---|
| veröffentlichte Seite (Artifact) | geteilte Datenbank – alle im Team sehen denselben Stand, Änderungen erscheinen live |
| `index.html` als Datei oder GitHub Page | Browserspeicher des jeweiligen Rechners |

Beide Wege nutzen dieselbe Schnittstelle (`Ablage` in `src/app.html`), die
Seite funktioniert also in jedem Fall vollständig. Die geteilte Ablage legt
Pläne unter `plaene/<id>`, Aufgaben unter `plaene/<id>/aufgaben/<id>` und das
Team unter `team/<id>` ab.

## Zugriff und Rollen

Abgesichert ist nur die veröffentlichte Artifact-Fassung. Den Zugang selbst regelt
das **Teilen-Menü** von claude.ai: Wer dort nicht freigegeben ist, kann die
Seite nicht öffnen. Die Anmeldung läuft über das claude.ai-Konto, also über die
Mailadresse.

Im Reiter **Zugriff** (nur für Admins) trägt man die freigegebenen Personen über
die Suche nach Name oder Mailadresse ein und vergibt die Rolle:

| Rolle | Freigabe im Teilen-Menü | darf |
|---|---|---|
| Admin | Bearbeiten | alles: Pläne, Termine, Regelwerk, Aufgaben, Team, Zugriffsliste |
| Beobachter | Ansehen | alles ansehen und exportieren, nichts ändern |
| Zugewiesene Aufgaben | Ansehen | wie Beobachter, dazu bei den eigenen Aufgaben: abhaken, Rückmeldung schreiben und – wenn bei der Aufgabe „Die zuständige Person darf den Termin des Schritts ändern“ gesetzt ist – den Termin des verknüpften Schritts setzen |

Die Besitzerin oder der Besitzer der Seite ist immer Admin. Geteilte, aber nicht
eingetragene Personen sehen nur einen Hinweis „Kein Zugriff“. Ist jemand als
Admin eingetragen, aber nur mit *Ansehen* geteilt, bleibt die Seite für diese
Person schreibgeschützt und zeigt einen Hinweis.

Durchgesetzt werden die Rechte von den Regeln der Datenbank, nicht nur von der
Oberfläche:

```json
{"db":{"rules":[
  {"path":"",                "read":"interact", "write":"admin"},
  {"path":"freigaben",       "read":"interact", "write":"admin"},
  {"path":"freigaben/{self}",                    "write":"interact"}
]}, "user":{"scopes":["profile"]}, "downloads":true}
```

Schreiben darf also nur, wer *Bearbeiten* hat. Alle anderen dürfen nur ihr
eigenes Dokument `freigaben/<kennung>` schreiben, und daraus übernimmt die
Seite nur Einträge zu Aufgaben, die dieser Person zugewiesen sind und deren
Rolle *Zugewiesene Aufgaben* ist. Die Zugriffsliste unter `zugriff/<kennung>`
speichert nur die Kennung, die Rolle und die Abteilung. Namen kommen bei jedem
Aufruf frisch aus dem Verzeichnis. Die Suche findet Personen auch über die
Mailadresse. Angezeigt wird die Adresse nur, wenn die Organisation den Bereich
`email` freigibt; derzeit ist er nicht verfügbar. Wird ein Plan freigegeben,
schreibt die Seite Haken, Termine und Rückmeldungen der zuständigen Personen in
den Plan fest. Spätere Änderungen an ihren Dokumenten wirken dann nicht mehr.

Der Hinweis „Kein Zugriff“ ist eine Sperre der Oberfläche: Wer im Teilen-Menü
freigegeben ist, kann die Daten technisch lesen. Wer nichts sehen soll, wird
im Teilen-Menü gar nicht erst freigegeben. Die Datei- und die GitHub-Pages-Fassung
haben keine Anmeldung. Dort arbeitet jede Person als Admin in ihrem eigenen
Browserspeicher.

## Manuelle Termine

Einzelne Termine lassen sich pro Ausgabe von Hand setzen – für Urlaubszeiten,
Feiertagsbrücken oder Sonderfälle. Ein Klick auf eine Zelle im Terminplan oder
auf eine Zeile in der Ausgaben-Ansicht öffnet ein Fenster; es zeigt den
automatischen Termin zum Vergleich und warnt, wenn das gewählte Datum auf ein
Wochenende, einen Feiertag oder den falschen Wochentag fällt – ohne es zu
verhindern, denn die Entscheidung trifft die Redaktion. Das Fenster schließt
über *Übernehmen*, *Abbrechen*, das Kreuz, die Escape-Taste oder einen Klick
daneben.

Dasselbe Fenster stellt auch Rückfragen und erfragt Namen. Es ersetzt
`confirm()` und `prompt()`, die in eingebetteten Seiten blockiert sein können.

Ein fester Termin wird unverändert übernommen. **Alle Schritte, die ihn als
Anker haben, rechnen von dort aus weiter** – in der Rückwärtskette sind das die
vorgelagerten Schritte. Zieht man etwa den Start der Seitenfreigabe im Mai-Heft
eine Woche vor, wandern Redaktionsschluss, Anzeigenschluss, beide
Redaktionskonferenzen und der Druckunterlagenschluss mit; alles nach dem
Seitenfreigabe-Start bleibt am E-Tag verankert.

Gesetzte Termine sind blau markiert, stehen gesammelt in der Karte *Manuelle
Termine* und lassen sich einzeln oder gesamt auf Automatik zurückstellen. Der
Export weist sie in der Spalte *Herkunft* aus. Ein Jahreswechsel oder ein neuer
Terminvorschlag verwirft sie (mit „Rückgängig“ wiederherstellbar), weil die
Daten sonst nicht mehr zum Plan passen.

## Feiertage

Die Feiertage werden für jedes Jahr **gerechnet**, nicht abgerufen – die Seite
braucht dafür keine Internetverbindung. Grundlage sind die feste Kalenderlage
(Neujahr, 1. Mai, 3. Oktober, Weihnachten), die Osterformel (Karfreitag,
Ostermontag, Christi Himmelfahrt, Pfingstmontag, Fronleichnam) und die Regel
„Mittwoch vor dem 23. November" für den Buß- und Bettag.

Aufgelistet sind **alle gesetzlichen Feiertage in Deutschland**, jeder mit
Länderkennung, damit keiner untergeht. Voreingestellt frei sind die
bundesweiten Feiertage sowie alles, was in **Berlin oder Hessen** gilt – die
Chips *BE* und *HE* über der Liste schalten das um, weitere Länder lassen sich
über *+ Land* dazunehmen. Jeder Tag bleibt einzeln an- und abwählbar; die
Länderauswahl bestimmt nur die Voreinstellung. Länderabhängige
Einführungsjahre sind berücksichtigt (Frauentag in Berlin seit 2019, in
Mecklenburg-Vorpommern seit 2023; Reformationstag in HB/HH/NI/SH seit 2018;
Weltkindertag in Thüringen seit 2019).

Ostersonntag und Pfingstsonntag sind als Sonntage gekennzeichnet und ohnehin
arbeitsfrei. Heiligabend und Silvester stehen als abwählbare Vorschläge für
Betriebsruhe bereit, ebenso lassen sich eigene freie Tage eintragen. Der Filter
*nur aktive* verkürzt die Liste über drei Jahre auf das Wesentliche.

Für Berlin und Hessen bedeutet die Voreinstellung 2027 dreizehn freie Tage,
darunter der **Internationale Frauentag** (Mo 08.03.) und **Fronleichnam**
(Do 27.05., Hessen).

## Unterschiede zur Excel-Vorlage

| Punkt | Excel | Diese Seite |
|---|---|---|
| Feiertagsjahre | nur das Planungsjahr | Vor-, Planungs- und Folgejahr – das Januar/Februar-Heft wird im Dezember des Vorjahres produziert, dessen Weihnachtsfeiertage die Excel nicht kennt |
| Umfang | 11 Einträge für Berlin | alle deutschen Feiertage mit Länderkennung, Voreinstellung Berlin + Hessen |
| Internationaler Frauentag (8.3.) | fehlt | enthalten (seit 2019 gesetzlicher Feiertag in Berlin) |
| Fronleichnam | fehlt | enthalten (gesetzlicher Feiertag in Hessen) |
| Reformationstag (31.10.) | enthalten | aus, weil weder in Berlin noch in Hessen gesetzlicher Feiertag |
| Heiligabend / Silvester | – | abschaltbare Vorschläge für Betriebsruhe |

Die Schaltfläche **„Feiertage wie in der Excel"** stellt den Excel-Stand her
(nur Berlin, ohne Frauentag, mit Reformationstag). Für 2027 unterscheiden sich
beide Varianten in **8 von 240 Terminen**: Der Frauentag am Montag, 8.3.2027
trifft den Redaktionsschluss der April-Ausgabe und zieht deren gesamten Vorlauf
um eine Woche nach vorn. Fronleichnam 2027 fällt in ein produktionsfreies
Fenster und wirkt sich in diesem Jahr nicht aus – in anderen Jahren schon.

## Prüfungen

Der Reiter *Prüfung* meldet unter anderem verschobene Erscheinungstermine,
Schritte, die durch Feiertagsketten um drei Tage oder mehr wandern, Termine
zwischen den Jahren, Schritte hinter ihrem Anker, Ausgaben in falscher
Reihenfolge und ungewöhnliche Vorlaufzeiten.

## Export

**Excel (.xlsx)** – über *Excel-Datei* in der Seitenspalte oder im Reiter
*Export*. Eine Arbeitsmappe mit drei Blättern:

| Blatt | Inhalt |
|---|---|
| Terminplan | die Matrix wie auf dem Bildschirm, nach Phasen gegliedert; manuelle Termine blau, verschobene gelb, E-Tag rot hinterlegt |
| Anzeigenplan | je Ausgabe Erscheinungstermin, Anzeigenschluss, Druckunterlagenschluss, Anlieferungstermin Beilagen/Einhefter und Anzeigenschluss Advertorials (Schritte 24, 7, 9, 14, 3) |
| Redaktionsplan | je Ausgabe Anmeldung Fachabteilungen, Kleine und Große Redaktionskonferenz, Redaktionsschluss, Auflagenmeldung, Start der Seitenfreigabe, Layout-Imprimatur und E-Tag (Schritte 4, 5, 6, 8, 10, 12, 15, 24) |

Im Anzeigen- und Redaktionsplan sind manuell gesetzte Termine orange
hinterlegt. Die Spalten beider Pläne stehen in `ANZEIGENPLAN` und
`REDAKTIONSPLAN` in `src/app.html`; wird ein Schritt im Regelwerk umbenannt,
übernimmt der Spaltenkopf den neuen Namen.

Alle Datumsangaben sind echte Excel-Daten. Kopfzeilen sind fixiert und
wiederholen sich beim Drucken; jedes Blatt ist auf Seitenbreite eingestellt.
Die Datei wird ohne Fremdbibliothek in der Seite selbst erzeugt (`Xlsx` in
`src/app.html`), funktioniert also auch ohne Internetverbindung.

Daneben: CSV-Matrix und CSV-Terminliste (Semikolon + BOM), `.ics` mit jedem
Termin als ganztägiger Kalendereintrag, JSON-Konfiguration zum Sichern und
Weitergeben sowie *Drucken / PDF* (A4 quer).

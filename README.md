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

Die Seite gibt es in drei Fassungen, alle aus derselben Quelle `src/app.html`:

| Fassung | Anmeldung | Ablage |
|---|---|---|
| **Website** (GitHub Pages + Firebase) | Mail und Passwort, nur Personen auf der Zugriffsliste | gemeinsam, live, Rechte auf dem Server |
| claude.ai-Artifact | claude.ai-Konto, Teilen-Menü | gemeinsam, live |
| `index.html` als Datei | keine | Browserspeicher dieses Rechners |

Ohne `firebase-config.json` ist `index.html` die Datei-Fassung: Doppelklick
genügt, kein Server, keine Abhängigkeiten.

## Website mit Anmeldung einrichten

Die Website liegt auf GitHub Pages. Anmeldung und gemeinsame Ablage kommen von
Firebase (Google), im kostenlosen Spark-Tarif, ohne Kreditkarte. Einmalig:

**1. Firebase-Projekt**
1. <https://console.firebase.google.com> → *Projekt hinzufügen*, Name z. B.
   `bw-produktionsplan`, Google Analytics aus.
2. *Build → Authentication → Jetzt starten → Sign-in method*: **E-Mail-Adresse/Passwort**
   aktivieren (nur den oberen Schalter, nicht „E-Mail-Link“) → Speichern.
3. *Authentication → Einstellungen → Autorisierte Domains*: `cedric472000.github.io`
   hinzufügen, damit die Links in den Mails auf die Seite zurückführen.
4. *Authentication → Vorlagen*: Vorlagensprache **Deutsch**. Optional den
   Absendernamen auf „Produktionsplan Berliner Wirtschaft“ setzen.
5. *Build → Firestore Database → Datenbank erstellen*: Standort
   **europe-west3 (Frankfurt)**, im **Produktionsmodus** starten.
6. *Firestore → Regeln*: den Inhalt von [`firestore.rules`](firestore.rules)
   vollständig einfügen → **Veröffentlichen**.
7. *Projekteinstellungen (Zahnrad) → Allgemein → Meine Apps → Web (`</>`)*:
   App registrieren (ohne Hosting). Die angezeigten Werte von `firebaseConfig`
   als `firebase-config.json` neben `build.py` ablegen:
   ```json
   {"apiKey": "…", "authDomain": "….firebaseapp.com", "projectId": "…",
    "storageBucket": "…", "messagingSenderId": "…", "appId": "…"}
   ```
   Diese Werte sind kein Geheimnis. Sie stehen in jeder Firebase-Website im
   Quelltext; geschützt wird über die Regeln aus Schritt 6.
8. `python3 build.py`, `index.html` und `firebase-config.json` committen.

**2. GitHub Pages**
1. Pages ist bei privaten Repositories nur mit bezahltem GitHub-Tarif möglich.
   Kostenlos: *Settings → General → Danger Zone → Change visibility → Public*.
   Im Repository liegen nur Code und Regeln, keine Pläne und keine Personen.
2. *Settings → Pages → Build and deployment → Deploy from a branch*,
   Branch `main`, Ordner `/ (root)` → **Save**.
3. Nach ein bis zwei Minuten läuft die Seite unter
   <https://cedric472000.github.io/BW_Produktionsplan/>.

**3. Erster Login**
Die erste Person, die sich nach der Einrichtung mit bestätigter Mailadresse
anmeldet, wird **Besitzer** (immer Admin). Das also sofort selbst erledigen:
*Konto anlegen*, Mail bestätigen, *Als Besitzer übernehmen*. Danach im Reiter
**Zugriff** die Kolleginnen und Kollegen mit Name, Mailadresse und Rolle eintragen
und ihnen den Link schicken. Den Besitz ändern lässt sich nur in der
Firebase-Konsole (*Firestore → meta → besitzer*).

**Grenzen des kostenlosen Tarifs:** täglich 50 000 Lese- und 20 000
Schreibvorgänge, 1 000 Bestätigungs- und 150 Passwort-Mails. Für eine
Redaktion reicht das weit. Ein Login per Mail-Link ohne Passwort wäre im
kostenlosen Tarif auf 5 Mails am Tag begrenzt, deshalb Mail und Passwort.

`.nojekyll` schaltet die Jekyll-Verarbeitung von GitHub Pages ab. Nach jeder
Änderung an `src/app.html`: `python3 build.py` und `index.html` mit committen.

## Aufbau

| Datei | Inhalt |
|---|---|
| `src/app.html` | Die komplette Anwendung: Styles, Markup, Rechenkern (einzige Quelle) |
| `build.py` | Verpackt `src/app.html` in ein vollständiges HTML-Dokument |
| `index.html` | Erzeugt – die auslieferbare Seite |
| `firebase-config.json` | Zugangsdaten des Firebase-Projekts; fehlt sie, wird die Datei-Fassung gebaut |
| `firestore.rules` | Zugriffsregeln der Website – hier wird über Rechte entschieden |
| `vendor/firebase.js` | Firebase-Bibliothek, gebündelt (neu bauen: `cd tools/firebase && npm install && npm run bundle`) |
| `firebase.json` | für die Firebase-Werkzeuge: Regeln hochladen, Emulator für Tests |

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

### Rechenweise „Arbeitstage“ (Standard) – gelernt aus alten Plänen

So wie oben beschrieben rechnet die Excel – und springt dabei bei Feiertagen
oft eine ganze Woche: Fällt der Druck-Montag auf Ostermontag, liegt der Druck
eine Woche früher, und die ganze Kette davor springt mit. Wie die Redaktion
tatsächlich plant, ist aus den Produktionsplänen 2025 und 2026 und dem von
Hand erstellten Redaktionsplan 2027 abgeleitet:

1. **Normalraster**: die Regel oben ohne Feiertage – so liegen die Termine in
   einem Monat ohne Feiertag. Ein von Hand gesetzter E-Tag ist dessen Grundlage.
2. Wie Feiertage wirken, legt je Schritt die Spalte **Bindung** im Regelwerk fest:

| Bindung | Verhalten | voreingestellt für |
|---|---|---|
| Kette | hält zu seinem Bezug die Arbeitstage des Normalrasters – ein Feiertag dazwischen zieht ihn um einen Arbeitstag vor | die Produktionskette |
| Verschiebung | übernimmt die Verschiebung seines Bezugs in Arbeitstagen | Druckunterlagenschluss, Auflagenmeldung IHK/dpv (Bezug: Imprimatur) |
| Wochentermin | bleibt in seiner Kalenderwoche; bei einem Feiertag der Nachbartag, in der Weihnachtswoche und zwischen den Jahren die Woche davor | Anmeldung Fachabteilungen, Kleine und Große Redaktionskonferenz, Anzeigenschluss, Beilagenanlieferung |
| Fester Termin | bleibt auf seinem Tag; bei einem Feiertag der Arbeitstag davor | Druck, Postversand |

Dazu: Die **Prooffreigabe** hängt in der Kette am Postversand (immer 5
Arbeitstage davor), und der **Redaktionsschluss** fällt nicht auf einen
Freitag. Wochentermine wandern nicht mit, wenn die Kette sich verschiebt – nur
mit dem E-Tag und mit ihrem eigenen Block (etwa der Konferenzblock über
Weihnachten).

**Trefferquote** (Schritte 4–24; die Schritte 1–2 hatten 2025/26 noch andere
Abstände):

| Vergleich | Excel-Regel | gelernte Regeln |
|---|---|---|
| Produktionsplan 2026 | 176 von 210 | **210 von 210** |
| Redaktionsplan 2027 (mit den drei grün markierten Terminen) | 61 von 80 | **78 von 80** |
| Produktionsplan 2025 | 199 von 210 | 191 von 210 |

2025 wurden Feiertage im Mai und Juni noch anders gelöst (Proof zusammengeschoben
statt die Kette zu verschieben); 2026 und 2027 verschieben die Kette – dem folgt
die Seite. Die beiden übrigen Abweichungen 2027 (Auflagenmeldung April,
Seitenfreigabe Mai) sind Einzelentscheidungen; 2026 wurden dieselben Lagen nach
der Regel gelöst. Ältere Pläne (2021–2024) hatten andere Wochentage für die
Konferenzen und sind daher nur zum Vergleich herangezogen. Die alten Pläne
selbst liegen nicht im Repository.

In Monaten ohne Feiertag im Zeitraum ist das Ergebnis dasselbe wie in der
Excel. Über den Schalter **wie Excel** im Regelwerk rechnet die Seite wieder
genau wie die Excel-Vorlage; die Prüfung meldet dann Verschiebungen wieder als
Warnungen.

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
| Website mit Anmeldung | Firestore (Firebase) – alle im Team sehen denselben Stand, Änderungen erscheinen live |
| veröffentlichte Seite (Artifact) | geteilte Datenbank in claude.ai, ebenso live |
| `index.html` als Datei | Browserspeicher des jeweiligen Rechners |

Alle Wege nutzen dieselbe Schnittstelle (`Ablage` in `src/app.html`), die
Seite funktioniert also in jedem Fall vollständig. Die Website fällt nie
stillschweigend auf den Browserspeicher zurück. Die geteilte Ablage legt
Pläne unter `plaene/<id>`, Aufgaben unter `plaene/<id>/aufgaben/<id>` und das
Team unter `team/<id>` ab.

## Zugriff und Rollen

Im Reiter **Zugriff** (nur für Admins) stehen die Personen, die an die Pläne
dürfen, jeweils mit einer Rolle:

| Rolle | darf |
|---|---|
| Admin | alles: Pläne, Termine, Regelwerk, Aufgaben, Team, Zugriffsliste |
| Beobachter | alles ansehen und exportieren, nichts ändern |
| Zugewiesene Aufgaben | wie Beobachter, dazu bei den eigenen Aufgaben: abhaken, Rückmeldung schreiben und – wenn bei der Aufgabe „Die zuständige Person darf den Termin des Schritts ändern“ gesetzt ist – den Termin des verknüpften Schritts setzen |

Der Besitzer der Seite ist immer Admin. Damit eine Aufgabe als „eigene“ gilt,
wählt man beim Anlegen die Person mit dem Zusatz „· mit Login“. Wird ein Plan
freigegeben, schreibt die Seite Haken, Termine und Rückmeldungen der zuständigen
Personen in den Plan fest. Spätere Änderungen an ihren Rückmeldungen wirken
dann nicht mehr.

### Website (Firebase)

Anmelden kann sich nur, wer ein Konto mit **bestätigter** Mailadresse hat. Ein
Konto anlegen kann zwar jede Person – an die Daten kommt aber nur, wer in der
Zugriffsliste steht. Alle anderen sehen „Noch nicht freigeschaltet“. Die
Kennung einer Person ist ihre Mailadresse in Kleinbuchstaben.

Entschieden wird auf dem Server, in [`firestore.rules`](firestore.rules):

| Ablage | lesen | schreiben |
|---|---|---|
| `meta/besitzer` | alle Angemeldeten | einmalig von der ersten Person, danach niemand |
| `zugriff/<mail>` | alle auf der Liste, jede Person ihren eigenen Eintrag | Admins (nur Kleinbuchstaben, nur gültige Rollen) |
| `plaene`, `plaene/<id>/aufgaben`, `team` | alle auf der Liste | Admins |
| `freigaben/<mail>` | alle auf der Liste | Admins und die Person selbst, wenn ihre Rolle *Zugewiesene Aufgaben* ist |

Wer nicht auf der Liste steht oder seine Mail nicht bestätigt hat, bekommt
vom Server nichts – auch nicht mit den Entwicklerwerkzeugen des Browsers. Wer
von der Liste genommen wird, verliert den Zugriff sofort. Das Konto bleibt
bestehen, beim erneuten Eintragen ist die Person sofort wieder drin. Passwörter
liegen nur bei Firebase und sind für Admins nicht einsehbar. Wer seins vergisst,
setzt es über *Passwort vergessen* selbst neu.

### claude.ai-Fassung

Hier regelt das **Teilen-Menü** den Zugang: Admins mit *Bearbeiten*, alle
anderen mit *Ansehen*. Im Reiter Zugriff sucht man die Personen im Verzeichnis
der Organisation. Ist jemand als Admin eingetragen, aber nur mit *Ansehen*
geteilt, bleibt die Seite für diese Person schreibgeschützt und zeigt einen
Hinweis.

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
`email` freigibt; derzeit ist er nicht verfügbar.

Der Hinweis „Kein Zugriff“ ist hier nur eine Sperre der Oberfläche: Wer im
Teilen-Menü freigegeben ist, kann die Daten technisch lesen. Wer nichts sehen
soll, wird im Teilen-Menü gar nicht erst freigegeben.

Die Datei-Fassung hat keine Anmeldung. Dort arbeitet jede Person als Admin in
ihrem eigenen Browserspeicher.

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

Ein fester Termin wird unverändert übernommen. **Was auf ihm aufbaut, wandert
mit – im selben Abstand in Arbeitstagen wie im automatischen Plan.** In der
Rückwärtskette sind das die vorgelagerten Schritte. Die Regel mit ihren
Ziel-Wochentagen wird dafür bewusst nicht noch einmal angewendet: Sie würde
aus kleinen Änderungen Wochensprünge machen. Beispiel Mai 2027: Der Start der
Seitenfreigabe zwei Arbeitstage früher (Do 15.04. statt Mo 19.04.) zieht
Redaktionsschluss, Anzeigenschluss, Druckunterlagenschluss, beide
Redaktionskonferenzen und die Anmeldungen um genau zwei Arbeitstage vor, über
Ostern hinweg. Nach der Regel wäre die Große Redaktionskonferenz eine ganze
Woche gesprungen.

Was nach dem gesetzten Termin kommt, bleibt am Erscheinungstag und am Druck
verankert. Gerät dadurch die Reihenfolge durcheinander, etwa weil die
Seitenfreigabe jetzt nach „EPSe bereitstellen“ beginnt, warnen das Terminfenster
und die *Prüfung*. Dann setzt man den Folgeschritt ebenfalls, und alles, was auf
ihm aufbaut, wandert wieder mit. Das Terminfenster zeigt schon vor dem
Übernehmen, wie viele Schritte mitwandern. Mitgewanderte Termine sind in hellem
Blau mit kleiner Ecke markiert. Die Prüfung nennt sie und weist auf Schritte
hin, die dadurch nicht mehr auf ihrem Wochentag liegen (z. B. eine
Redaktionskonferenz am Donnerstag statt am Mittwoch); die lassen sich bei
Bedarf von Hand setzen. Ohne manuelle Termine rechnet die Seite unverändert
wie die Excel.

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

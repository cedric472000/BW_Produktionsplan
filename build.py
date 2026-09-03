#!/usr/bin/env python3
"""Wraps src/app.html (Seiteninhalt) in ein vollstaendiges HTML-Dokument -> index.html.

Der Inhalt in src/app.html ist absichtlich ohne <!doctype>/<html>/<head>/<body>
geschrieben, damit dieselbe Quelle sowohl als eigenstaendige Seite (index.html,
z.B. auf GitHub Pages) als auch als eingebettetes Artifact laufen kann.
"""
import pathlib

ROOT = pathlib.Path(__file__).parent
body = (ROOT / "src" / "app.html").read_text(encoding="utf-8")

doc = """<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Produktionsplan fuer das Magazin Berliner Wirtschaft: Rueckwaertsterminierung aller Produktionsschritte aus Jahr und Erscheinungsterminen.">
<style>
:root{color-scheme:light dark}
body{margin:0;font:14px/1.5 system-ui,sans-serif}
img{max-width:100%}
[hidden]{display:none!important}
</style>
</head>
<body>
__BODY__
</body>
</html>
"""

doc = doc.replace("__BODY__", body)

(ROOT / "index.html").write_text(doc, encoding="utf-8")
print("index.html geschrieben (%d Zeichen)" % len(doc))

#!/usr/bin/env python3
"""Wraps src/app.html (Seiteninhalt) in ein vollstaendiges HTML-Dokument -> index.html.

Der Inhalt in src/app.html ist absichtlich ohne <!doctype>/<html>/<head>/<body>
geschrieben, damit dieselbe Quelle sowohl als eigenstaendige Seite (index.html,
z.B. auf GitHub Pages) als auch als eingebettetes Artifact laufen kann.

Liegt firebase-config.json neben diesem Skript, bekommt die Website die
Anmeldung und die gemeinsame Ablage ueber Firebase (siehe README).
  python3 build.py [--config DATEI] [--out DATEI]
"""
import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
ap = argparse.ArgumentParser()
ap.add_argument("--config", default=str(ROOT / "firebase-config.json"))
ap.add_argument("--out", default=str(ROOT / "index.html"))
args = ap.parse_args()

body = (ROOT / "src" / "app.html").read_text(encoding="utf-8")
cfg_path = pathlib.Path(args.config)
konfig = ""
if cfg_path.exists():
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    konfig = "<script>window.BW_FIREBASE = %s;</script>\n" % json.dumps(cfg, ensure_ascii=False)

doc = """<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Produktionsplan fuer das Magazin Berliner Wirtschaft: Rueckwaertsterminierung aller Produktionsschritte aus Jahr und Erscheinungsterminen.">
<meta name="robots" content="noindex">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 40 40%27%3E%3Crect width=%2740%27 height=%2740%27 rx=%276%27 fill=%27%23003087%27/%3E%3Cpath d=%27M6 31a14 14 0 0 1 28 0%27 fill=%27none%27 stroke=%27%23fff%27 stroke-width=%273.5%27/%3E%3Cpath d=%27M13 31a7 7 0 0 1 14 0%27 fill=%27none%27 stroke=%27%23fff%27 stroke-width=%273.5%27 opacity=%27.55%27/%3E%3C/svg%3E">
<style>
:root{color-scheme:light dark}
body{margin:0;font:14px/1.5 system-ui,sans-serif}
img{max-width:100%}
[hidden]{display:none!important}
</style>
__KONFIG__</head>
<body>
__BODY__
</body>
</html>
"""

doc = doc.replace("__KONFIG__", konfig).replace("__BODY__", body)

pathlib.Path(args.out).write_text(doc, encoding="utf-8")
print("%s geschrieben (%d Zeichen, %s)" % (pathlib.Path(args.out).name, len(doc),
      "mit Anmeldung" if konfig else "ohne Anmeldung"))

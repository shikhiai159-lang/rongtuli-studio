#!/usr/bin/env python3
"""Patch generated Capacitor Android manifest with microphone permission."""
from pathlib import Path
import xml.etree.ElementTree as ET
p = Path("android/app/src/main/AndroidManifest.xml")
if not p.exists():
    raise SystemExit(f"AndroidManifest not found: {p}")
ET.register_namespace("android", "http://schemas.android.com/apk/res/android")
tree = ET.parse(p)
root = tree.getroot()
ns = "{http://schemas.android.com/apk/res/android}"
perm = "android.permission.RECORD_AUDIO"
if not any(el.tag == "uses-permission" and el.get(ns + "name") == perm for el in root.findall("uses-permission")):
    el = ET.Element("uses-permission")
    el.set(ns + "name", perm)
    # Keep permission declarations before <application>.
    app = root.find("application")
    if app is not None:
        root.insert(list(root).index(app), el)
    else:
        root.append(el)
tree.write(p, encoding="utf-8", xml_declaration=True)
print("Added android.permission.RECORD_AUDIO to", p)

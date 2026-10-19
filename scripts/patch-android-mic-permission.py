#!/usr/bin/env python3
from pathlib import Path
import xml.etree.ElementTree as ET

manifest = Path('android/app/src/main/AndroidManifest.xml')
if not manifest.exists():
    raise SystemExit(f'AndroidManifest not found: {manifest}')
ET.register_namespace('android', 'http://schemas.android.com/apk/res/android')
tree = ET.parse(manifest)
root = tree.getroot()
ns = '{http://schemas.android.com/apk/res/android}'
permissions = [
    'android.permission.RECORD_AUDIO',
    'android.permission.MODIFY_AUDIO_SETTINGS',
]
for permission in permissions:
    if not any(el.tag == 'uses-permission' and el.get(ns + 'name') == permission for el in root.findall('uses-permission')):
        el = ET.Element('uses-permission')
        el.set(ns + 'name', permission)
        app = root.find('application')
        root.insert(list(root).index(app), el) if app is not None else root.append(el)
tree.write(manifest, encoding='utf-8', xml_declaration=True)
print('Ensured RECORD_AUDIO and MODIFY_AUDIO_SETTINGS manifest permissions')

print('Done: Capacitor will request microphone permission when getUserMedia is called from the Record button.')

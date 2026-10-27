#!/usr/bin/env python3
"""Patch the freshly generated Capacitor android/ project.

0. Launcher icon: copy resources/mipmap-*/ (adaptive + legacy + round) over the default Capacitor icon.

1. Gradle: stop the "Duplicate class kotlin.collections.jdk7/jdk8 ..." build error.
2. AndroidManifest: add microphone permissions (the Audio Lab records with getUserMedia).

Safe to run more than once. Run from the repository root, after `npx cap add android`.
"""
import re
import sys
from pathlib import Path

root = Path("android")
GRADLE_MARKER = "// Rongtuli Kotlin dependency alignment"
GRADLE_BLOCK = f"""
{GRADLE_MARKER}
// kotlin-stdlib-jdk7 / jdk8 older than 1.8.0 still contain classes that were merged into
// kotlin-stdlib 1.8+, which causes "Duplicate class" errors. Bump only those two (empty,
// forwarding) artifacts; kotlin-stdlib itself keeps the version Gradle resolves normally.
subprojects {{
    configurations.configureEach {{
        resolutionStrategy.eachDependency {{ details ->
            if (details.requested.group == 'org.jetbrains.kotlin' &&
                    (details.requested.name == 'kotlin-stdlib-jdk7' || details.requested.name == 'kotlin-stdlib-jdk8')) {{
                details.useVersion '1.8.22'
                details.because 'Avoid duplicate Kotlin classes (jdk7/jdk8 merged into kotlin-stdlib in 1.8.0)'
            }}
        }}
    }}
}}
"""

PERMISSIONS = [
    "android.permission.RECORD_AUDIO",
    "android.permission.MODIFY_AUDIO_SETTINGS",
]


def die(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


# ---- 1. Gradle ----
gradle = root / "build.gradle"
if not gradle.exists():
    gradle = root / "build.gradle.kts"
    if gradle.exists():
        die("android/build.gradle.kts found; this script only patches the Groovy build.gradle")
    die("android/build.gradle was not generated (run `npx cap add android` first)")
text = gradle.read_text(encoding="utf-8")
if GRADLE_MARKER not in text:
    gradle.write_text(text.rstrip() + "\n" + GRADLE_BLOCK, encoding="utf-8")
    print("Patched android/build.gradle (Kotlin jdk7/jdk8 alignment)")
else:
    print("android/build.gradle already patched")

# ---- 2. Manifest ----
manifest = root / "app" / "src" / "main" / "AndroidManifest.xml"
if not manifest.exists():
    die("AndroidManifest.xml not found")
mtext = manifest.read_text(encoding="utf-8")
missing = [p for p in PERMISSIONS if p not in mtext]
if missing:
    lines = "".join(f'    <uses-permission android:name="{p}" />\n' for p in missing)
    if not re.search(r"</manifest>", mtext):
        die("AndroidManifest.xml has no </manifest>")
    mtext = re.sub(r"</manifest>", lines + "</manifest>", mtext, count=1)
    manifest.write_text(mtext, encoding="utf-8")
    print("Added permissions:", ", ".join(missing))
else:
    print("AndroidManifest.xml already has the microphone permissions")

# ---- 3. Launcher icon ----
import shutil
res_src = Path("resources")
res_dst = root / "app" / "src" / "main" / "res"
copied = 0
if res_src.is_dir():
    for f in res_src.glob("mipmap-*/*.png"):
        dst = res_dst / f.parent.name / f.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(f, dst)
        copied += 1
    # background colour of the adaptive icon (matches the icon gradient)
    bg = res_dst / "values" / "ic_launcher_background.xml"
    bg.parent.mkdir(parents=True, exist_ok=True)
    bg.write_text('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#5741C9</color>\n</resources>\n', encoding="utf-8")
    # adaptive icon definition: make sure it exists and uses our files
    any26 = res_dst / "mipmap-anydpi-v26"
    any26.mkdir(parents=True, exist_ok=True)
    adaptive = '<?xml version="1.0" encoding="utf-8"?>\n<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n    <background android:drawable="@color/ic_launcher_background"/>\n    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>\n</adaptive-icon>\n'
    for name in ("ic_launcher.xml", "ic_launcher_round.xml"):
        (any26 / name).write_text(adaptive, encoding="utf-8")
    print(f"Installed launcher icon ({copied} PNG files)")
else:
    print("WARNING: resources/ folder not found; default Capacitor icon will be used")

# ---- verify ----
if GRADLE_MARKER not in gradle.read_text(encoding="utf-8"):
    die("Gradle patch verification failed")
final = manifest.read_text(encoding="utf-8")
for p in PERMISSIONS:
    if p not in final:
        die(f"Manifest verification failed: {p}")
if res_src.is_dir() and not (res_dst / "mipmap-xxxhdpi" / "ic_launcher_foreground.png").exists():
    die("Icon verification failed")
print("Android project patch verified.")

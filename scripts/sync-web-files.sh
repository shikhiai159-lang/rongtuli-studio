#!/usr/bin/env bash
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$ROOT/www"
cp "$ROOT/rongtuli_studio_500/index.html" "$ROOT/www/index.html"
cp "$ROOT/rongtuli_studio_500/manifest.webmanifest" "$ROOT/www/manifest.webmanifest"
cp "$ROOT/rongtuli_studio_500/sw.js" "$ROOT/www/sw.js"
echo 'www/ ফোল্ডারের ওয়েব ফাইল আপডেট হয়েছে।'

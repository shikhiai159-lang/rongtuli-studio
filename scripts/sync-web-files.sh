#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
test -s "$ROOT/www/index.html"
echo "Canonical Android web entry: www/index.html (no duplicate HTML copied)."

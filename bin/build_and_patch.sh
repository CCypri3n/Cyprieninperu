#!/usr/bin/env bash
set -euo pipefail

# Build script: runs Pelican then post-processes feeds to append UTM params.
# Usage: bin/build_and_patch.sh [pelican-args...]

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON="$PROJECT_ROOT/venv/bin/python"
if [ ! -x "$PYTHON" ]; then
  PYTHON="$(command -v python3 || command -v python || true)"
fi
if [ -z "$PYTHON" ]; then
  echo "No Python interpreter found. Install Python or create venv at ./venv." >&2
  exit 1
fi

echo "Using Python: $PYTHON"

echo "Fetching data from Goatcounter API"
$PYTHON scripts/goatcounter_viewcount.py

PELICAN_CMD=("-m" "pelican" "content" "-o" "__site/" "-s" "publishconf.py")
if [ "$#" -gt 0 ]; then
  # allow extra pelican args from caller
  PELICAN_CMD=("-m" "pelican" "$@")
fi

echo "Running Pelican..."
$PYTHON "${PELICAN_CMD[@]}"

echo "Running UTM post-processing script on __site and __static..."
$PYTHON scripts/add_utm_to_feeds.py --dirs __site __static output

echo "Done. Check __site/feeds/*.atom.xml or __static/feeds/*.atom.xml for utm_source=atomfeed"

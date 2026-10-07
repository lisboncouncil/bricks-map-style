#!/usr/bin/env bash
# Build the static site published on GitHub Pages into _site/.
# Usage: ./build.sh [BASE_URL]
#   BASE_URL defaults to https://lisboncouncil.github.io/bricks-map-style
#   For local testing: ./build.sh http://localhost:8765 && python3 -m http.server 8765 -d _site
set -euo pipefail
BASE="${1:-https://lisboncouncil.github.io/bricks-map-style}"
rm -rf _site && mkdir -p _site
python3 scripts/make_style.py "${BASE}/fonts/{fontstack}/{range}.pbf" _site/bricks-style.json
cp -r fonts _site/fonts
cp preview/index.html _site/index.html
cp LICENSE LICENSE-CODE README.md _site/
touch _site/.nojekyll
echo "Built _site with glyphs from ${BASE}"

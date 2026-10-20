#!/bin/sh
# Optional packaging helper. The scaffold itself needs no shell, Git or runtime.
# Run at the DEVELOPMENT repository root: sh scripts/package-scaffold.sh [output.zip]
set -eu
OUT="${1:-aos-w-portable.zip}"
if [ ! -f "scaffold/aos-w/VERSION.json" ]; then
  echo "Run this from the digzoman/aos-workflows repository root." >&2
  exit 1
fi
if command -v zip >/dev/null 2>&1; then
  cd scaffold
  zip -q -r "../$OUT" aos-w
  echo "Created ${OUT}"
else
  echo "The optional zip utility is not installed. Download the repository ZIP and copy scaffold/aos-w/ instead." >&2
  exit 2
fi

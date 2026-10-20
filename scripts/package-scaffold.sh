#!/bin/sh
# Optional safe maintainer package wrapper. The downloaded aos-w core needs NO script.
set -eu
if [ ! -f "scaffold/aos-w/VERSION.json" ]; then
  echo "Run from development repository root." >&2
  exit 2
fi
if ! command -v python3 >/dev/null 2>&1; then
  echo "Safe distribution packaging requires optional Python 3; use GitHub Actions artifact instead." >&2
  exit 2
fi
exec python3 scripts/aosw-distribution.py build scaffold/aos-w "${1:-dist/aos-w-portable-0.6.0.zip}"

#!/bin/bash
# Builds the installable copy from work.html in a temp folder, serves it at /forge/ like GitHub Pages, runs qa_pwa.
set -u
S="$(cd "$(dirname "$0")/.." && pwd)"; T="$(mktemp -d)"
cp "$S/work.html" "$T/" && (cd "$T" && python3 "$S/pwa.py" >/dev/null) && mv "$T/pwa" "$T/forge" || exit 1
python3 -m http.server 8765 --directory "$T" >/dev/null 2>&1 & SRV=$!
sleep 1; cd "$S/qa"; python3 qa_pwa.py; rc=$?
kill $SRV; rm -rf "$T"; exit $rc

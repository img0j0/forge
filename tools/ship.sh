#!/bin/bash
# ship.sh "message" (after pwa.py): commits and pushes dev, main + gh-pages, ios-app; prints SHAs; copies app.html to $OUT.
# Expects clones: $ROOT/forge (dev), $ROOT/forge-main (main), $ROOT/forge-ios (ios-app). Set SESSION to this chat's session URL.
set -e
MSG="$1"; ROOT=${ROOT:-/home/claude}; OUT=${OUT:-$ROOT/forgelings.html}
TR="

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>${SESSION:+
Claude-Session: $SESSION}"
A="img0j0 <hunterabrams95@gmail.com>"
cd $ROOT/forge; git add -A; git commit -q --author="$A" -m "$MSG$TR"; git push -q origin HEAD:dev
cd $ROOT/forge-main; git fetch -q; G=$(git ls-remote origin gh-pages|cut -f1); cp $ROOT/forge/pwa/* .; git add -A; git commit -q --author="$A" -m "$MSG$TR"; git push -q origin main; git push -q --force-with-lease=gh-pages:$G origin main:gh-pages
echo MAIN $(git rev-parse HEAD) BLOB $(git hash-object index.html)
cd $ROOT/forge-ios; cp $ROOT/forge/app.html forgelings.html; git add -A; git commit -q --author="$A" -m "$MSG$TR"; git push -q origin HEAD:ios-app
echo IOS $(git rev-parse HEAD)
cp $ROOT/forge/app.html $OUT

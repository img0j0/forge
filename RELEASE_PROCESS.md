# Release audit and working procedure
Audited 2026-10-26.

Update: 0.38.7 addresses the save-write warning, cache cleanup, HTTP fallback/cache-write lifetime and QA runner exit-status findings below. See RELEASE_0.38.7.md for validation and remaining limits; the audit bullets below describe the pre-fix state. Browser regression remains outstanding.

## Branch ownership
- dev/work.html is the editable source. dev includes pwa.py, historical builds, legal pages, art tooling, and qa/.
- main is the generated website mirror, NOT the publishing trigger.
- gh-pages publishes https://img0j0.github.io/forge/. A main merge alone does not deploy.
- ios-app contains the Capacitor/Xcode project. forgelings.html is a source snapshot; build-www.py creates www/index.html. Source synchronization is not an iOS binary release.

## Reconciliation completed
The pre-update dev/work.html, transformed by pwa.py's page transformations, exactly matched the pre-update main/index.html.
The They Remember changes have now been backported to dev/work.html and ios-app/forgelings.html.
Repacking the reconciled source reproduces the current live index.html byte for byte.
base386.html remains the historical pre-update snapshot. work.html is no longer identical to it.
Update 0.38.9: base388.html is 0.38.8 as Hunter committed it; base389.html is identical to work.html again (They Remember, 0.38.7 and the 0.38.9 fix included). Patches from now on read base389.html.
They Remember shipped without a version bump: VERSION and the service-worker cache still say 0.38.6. Do not use that version alone to identify this release; use commit 1031617c9ec46d9a7d433307a0515c8e73d1b1f9 or hAffection.
Do not run a historical patch against base386 and replace work.html without retaining the memory changes.
Update 0.40.2: the old root copies base34 to base401 (and base386/388/389) were removed; git history keeps them. Patches now read base402.html, which equals work.html. base.html, base12-14.html and forge-pilot.html stay because qa_mig and qa_15 load them.
Update 0.41.0: patches now read base41.html (= work.html). base402.html was removed; git history keeps it.

## Size budget
The budget is 1 MB (qa_22, qa_30, qa_301) and is a soft guide set by Hunter on 2026-10-26: when a wanted feature needs more room, raise it and note it rather than cutting the feature. Prefer loading heavy optional extras on first use as separate cached files.

## Every release
1. Read this file, forge-handoff.md, and current branch heads. Fetch fresh source; do not reuse a prior chat's cached file.
2. Work from dev/work.html. Use a focused branch/commit. Preserve local-storage key forge-app-v1, origin, and /forge/ path.
3. Increment VERSION and title together. Update user-facing What's New/SEEN_V when appropriate. pwa.py derives its cache version from VERSION.
4. Run JavaScript syntax checks, the new feature checks, and relevant existing QA suites. Before a broad release run qa/runall.sh and inspect both individual process exit codes and logs. The 0.38.7 runner returns nonzero for failed, crashed, empty or timed-out suites; still inspect individual logs.
5. Exercise an existing save, a new player, save/reload, export/restore, reward caps, narrow layout, reduced motion, and offline navigation. Include real iPhone checks for native/browser behavior; Chromium cannot establish Safari equivalence.
6. Run python3 pwa.py. Inspect generated changes, legal pages, manifest and assets. Ensure index.html is exactly the expected transformation of work.html.
7. Commit generated output to main. Compare gh-pages...main: proceed with a non-forced fast-forward only when gh-pages has no independent commits. Use expected SHA to reject concurrent edits. Investigate divergence instead of overwriting it.
8. Advance gh-pages to the tested release SHA. Watch the Pages workflow for THAT SHA until completed/success; an older green deployment does not count.
9. Fetch the live HTML and verify a release identifier or feature marker. Only then claim the hosted release is verified. A resumed Home Screen process may still hold old JavaScript until navigation/relaunch; never clear player storage to refresh code.
10. Sync source to ios-app/forgelings.html. Run build-www.py and the native sync/build process in a suitable environment. Report separately whether native source, binary build, device tests, and TestFlight upload are complete.
11. Update handoff/version notes and save test results with the release commit references.

## Recovery
Keep the preceding release SHA. Prefer a revert commit on main, then fast-forward gh-pages to it, rather than rewriting branch history.
Assess save schema compatibility BEFORE rollback. Older code may discard fields from a newer save.
Never reset or clear player data as a deployment remedy.

## Audit findings / follow-up work
- Extensive QA exists on dev; its presence was missed in the initial main-only review. It has not all been executed in this audit.
- qa/README.md has stale version notes. Several tests encode historical size/layout behavior and need interpretation.
- qa/runall.sh records output but does not aggregate failures into a reliable nonzero exit code; improve before using it as a CI gate.
- No repository-owned CI workflow was found on main/dev/ios-app. Pages deployment is not a gameplay test.
- save() swallows storage errors; user-visible failure/recovery handling remains needed. (Addressed in 0.43.1: save() returns success, Update/Restore respect it, a daily safety copy and a recovery sheet cover unreadable saves, and a second tab steps the first aside.)
- sw.js deletes all other origin caches on activation. Scope deletion to this app in the pwa.py generator, not only generated sw.js.
- Network-first navigation falls back on thrown errors/timeouts, but an HTTP failure response can be returned directly. Test server-error fallback.
- The navigation cache write is not extended with event.waitUntil; test interrupted navigation/offline persistence.
- Runtime sanitizer and backup/restore should get regression tests for snackKnown and firstFind, including malformed dates.
- Native README's claim that storage can never be wiped is too absolute. Native persistence is additional protection, not an unconditional guarantee.
- Native project exists, but no Xcode build or physical-device validation was performed here.

## They Remember focused checks already performed
JavaScript parse check; first find is immutable after later finds; JSON round-trip preserves memory; origin callbacks distinguish daily and pack creatures; repeated affection does not consume visits or increase bond; sleeping state blocks affection.
These are targeted checks, not a substitute for full browser regression.
Update 0.41.1: patches now read base411.html (= work.html); base41.html removed (git keeps it).
Update 0.42.0: patches now read base42.html (= work.html); base411.html removed (git keeps it). qa_17 and qa_181 run over http in runall.sh.

Update 0.43.0: patches now read base43.html (= work.html); base42.html removed (git keeps it). qa_43 caps page lengths; put new features in sheets.
Update 0.43.1: patches now read base431.html (= work.html); base43.html removed (git keeps it). runall.sh now also runs qa_431, qa_ref (fixed-seed appearance references in qa/ref; regenerate with REF_UPDATE=1 only when art changes on purpose, and say so in the handoff) and reliability.cjs.

Update 0.44.0: patches now read base44.html (= work.html); base431.html removed (git keeps it). runall.sh now also runs qa_44; qa_ref adds the Meadow island reference (isle00).

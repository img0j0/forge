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

Update 0.44.1: patches now read base441.html (= work.html); base44.html removed (git keeps it). runall.sh adds qa_441 and runs qa_21 and qa_clock over http with qa_17/qa_181 (their failures were the file:// storage wipe, not the time of day).

Update 0.44.2: patches now read base442.html (= work.html); base441.html removed (git keeps it). runall.sh adds qa_contrast (day and night, light and dark text contrast on every screen).

Update 0.45.0: patches now read base45.html (= work.html); base442.html removed (git keeps it). runall.sh adds qa_45.

Update 0.46.0: patches now read base46.html (= work.html); base45.html removed (git keeps it). patch46.py reads journal46.css (kept in history/ with it) and the Caveat subset from the scratchpad at build time; base46.html already contains both, so later patches need neither. runall.sh adds qa_46.
Update 0.47.0: patches now read base47.html (= work.html); base46.html removed (git keeps it). patch47.py reads journal47.css (both in history/). qa_ref references regenerated on purpose (journal backdrop at the card corners; art unchanged).
Update 0.47.1: patches now read base471.html (= work.html); base47.html removed (git keeps it).
Update 0.48.0: patches now read base48.html (= work.html); base471.html removed (git keeps it). patch48.py reads motion48.css (both in history/).
Update 0.48.1: patches now read base481.html (= work.html); base48.html removed (git keeps it). Icons come from art/make_icons.py (run it after changing art/forgelings-icon.svg, before pwa.py; copy AppIcon-1024.png and splash-2732.png to the ios-app branch's art/).
Update 0.48.2: patches now read base482.html (= work.html); base481.html removed (git keeps it).
Update 0.48.3: patches now read base483.html (= work.html); base482.html removed (git keeps it). The card back art comes from art/cardback.py.
Update 0.48.4: patches now read base484.html (= work.html); base483.html removed (git keeps it).
Update 0.49.0: patches now read base49.html (= work.html); base484.html and base485.html removed (git keeps them). 0.48.5 (the day fix) shipped inside 0.49.
Update 0.50.0: patches now read base50.html (= work.html); base49.html removed (git keeps it). qa_50 joins runall.sh. Monkey seeds 4–6 can push the full run past two hours; if the background run stops at its time limit, run `python3 monkey.py N` for the remaining seeds. Shipped: main/gh-pages 670236c (Pages deploy success, live blob matches), ios-app 9c24a3b, Claude page version 92.
Update 0.50.1: patches now read base501.html (= work.html); base50.html removed (git keeps it). qa_501 joins runall.sh. `MONKEYS="1 2 3" bash runall.sh` keeps the main run under two hours; run `python3 monkey.py N` for 4, 5 and 6 afterwards. Shipped 2026-11-08: main/gh-pages 0522056 (Pages deploy success, live index.html blob 636b173 matches), ios-app 55a3aa2, Claude copy version 93. Full run: all suites pass (qa_50 had two timing flakes in the long run; 58/58 on rerun); monkeys 1–6 pass.
Update 0.50.2: patches now read base502.html (= work.html); base501.html removed (git keeps it). qa_502 joins runall.sh. Shipped 2026-11-08: main/gh-pages f9d751d (Pages deploy success, live index.html blob 2496b59 matches), ios-app 2254166, Claude copy version 94. Full run: all 81 suites pass; monkeys 1–6 pass.
Update 0.51.0: patches now read base51.html (= work.html); base502.html removed (git keeps it). qa_51 joins runall.sh. The Map/Tales/Journal highlight also fills the chosen button once its slide ends, so the contrast check reads it. Shipped: main/gh-pages 9ddbb99 (Pages run success, live index.html blob 1062fb2 matches), ios-app 1b885eb, Claude copy version 95.
Update 0.52.0: patches now read base52.html (= work.html); base51.html removed (git keeps it). qa_52 joins runall.sh. The ios-app branch now also holds the Android project (android/, android-setup.py) and .github/workflows/native.yml, which builds a debug APK and compiles the iPhone app on every push to ios-app; check that run as part of shipping. reliability.cjs stubs cloudSoon. Shipped: main/gh-pages e99366d (Pages run success, live index.html blob 24c3b82 matches), ios-app 55d7a02 (Native builds success), Claude copy version 96.

Update (Nov 12, 2026): Hunter tests each release himself. Do not run the full suite (runall.sh, journey, monkeys) before pushing; run only the checks for what changed, then ship and tell him what to test.
Update 0.53.0: patches now read base53.html (= work.html); base52.html removed (git keeps it). Checked qa_axe and qa_contrast plus day/night screenshots; full suite not run (Hunter tests). Shipped: main/gh-pages bc20532 (Pages run success, live index.html blob 0d66868 matches), ios-app b7c2fc9 (Native builds success), Claude copy version 97.
Update 0.54.0: patches now read base54.html (= work.html); base53.html removed (git keeps it). Creature art source and checks in creatures/ (same.py must print SAME). Shipped: main/gh-pages 034ef50 (Pages run success, live index.html blob 6b724b4 matches), ios-app 0633992 (Native builds success), Claude copy version 98.
Update 0.54.1: patches now read base541.html (= work.html); base54.html removed. creatures/check.py (0 problems) joins same.py as the creature checks. Shipped: main/gh-pages f9e60ab (Pages run success, live index.html blob 55e61da matches), ios-app c9fa9f1 (Native builds success), Claude copy version 99.
Update 0.55.0: patches now read base55.html (= work.html); base541.html removed. Rendering changes must pass creatures/identity.py, check.py and float.py. Shipped: main/gh-pages d83f30a (Pages run success, live index.html blob 864aa32 matches), ios-app 7e07d28 (Native builds success), Claude copy version 100.
Update 0.55.1: patches now read base551.html (= work.html); base55.html removed. Rendering changes must also pass creatures/foil.py (holo foil). Shipped: main/gh-pages a658438 (Pages run success, live index.html blob 4a1d528 matches), ios-app 49462a9 (Native builds success), Claude copy version 101.
Update 0.56.0: patches now read base56.html (= work.html); base551.html removed. Sprites are 40x40 (SPN); art changes must also pass creatures/clip.py. Shipped: main/gh-pages fd6e3d6 (Pages run success, live index.html blob 009b602 matches), ios-app 62fd35e (Native builds success), Claude copy version 102.
Update 0.56.1: patches now read base561.html (= work.html); base56.html removed. Art changes must also pass creatures/bob.py. Shipped: main/gh-pages dade08d (Pages run success, live index.html blob 9ea6553 matches), ios-app 940c76e (Native builds success), Claude copy version 103.
Update 0.57.0: patches now read base57.html (= work.html, English); base561.html removed. What ships is app.html: pwa.py runs i18n/build.mjs over work.html first, and ios-app/forgelings.html, the Claude page and the project copy are app.html too. A patch that adds English text must add its Japanese (i18n/README.md; `node scan.mjs ../work.html`, then build.mjs must report 0 refused). Checked: qa_axe and qa_contrast with the app forced to Japanese, English unchanged, the language switch both ways, onboarding in Japanese. Shipped: main/gh-pages 4dbeb30 (Pages run success, live index.html blob 85b0f99 matches), ios-app 1ce0fce (Native builds success), Claude copy version 104.
Update 0.57.1: patches now read base571.html (= work.html); base57.html removed. Katakana names (KANA_P/KANA_S) and feelings as whole texts. Checked: saved names unchanged after a Japanese session, feelings and week letters in both languages. Shipped: main/gh-pages fe0c458 (Pages run success, live index.html blob 878f7b3 matches), ios-app 2224d5e (Native builds success), Claude copy version 105.
Update 0.57.2: patches now read base572.html (= work.html); base571.html removed. Dates follow the app's language (LOC()); text shown later is written when shown, never saved in one language. Shipped: main/gh-pages 28f0ea3 (Pages run success, live index.html blob 576b1a0 matches), ios-app 9d5d473 (Native builds success), Claude copy version 106.
Update 0.58.0 to 0.62.0 (November 12; Hunter: "Please prioritize and execute the additions"): patches read base62.html now (= work.html); base572 to base611 removed. Each release checked with targeted checks (qa_axe where markup changed, screenshots in English and Japanese, `scan.mjs` with no warnings). Shipped: 0.58.0 main 5df4d31 / ios-app fea9718; 0.59.0 main 633b5ff / ios-app f849aed; 0.60.0 main 56172d2 / ios-app 20ce876; 0.61.0 main e28c0b6 / ios-app 25c8340; 0.61.1 main 20fcef7 / ios-app e617aca (Pages and Native builds success for each). The widget's native code: ios-app de823b3 (Native builds success, extension embedded). Claude copy versions 107 to 111.
Update 0.62.0: shipped main/gh-pages 9301e55 (Pages run success, live index.html blob d9aa3a7 matches), ios-app ed8f6f2 (Native builds success), Claude copy version 112.
Update 0.63.0 to 0.65.0 (November 12; Hunter: "Execute the plan", from the design doc "Forgelings: reworking the daily card and journal"): patches read base65.html now (= work.html); base62 to base64 removed. Targeted checks only (screenshots in English and Japanese, light and dark, qa_axe on the changed screens, `scan.mjs` with no warnings). Shipped: 0.63.0 main 0a97b6c / ios-app 5c0bde1 (Pages and Native builds success), Claude copy version 113; 0.64.0 main f9eb25d (Pages success, live blob 28df3da matches) / ios-app 22f6397, Claude copy version 114; 0.65.0 below. 0.65 also changes ios-setup.py: NSCameraUsageDescription and NSPhotoLibraryUsageDescription, and en.lproj/ja.lproj InfoPlist.strings (a PBXVariantGroup, knownRegions gains ja) so the permission sentences are in both languages. The privacy page has a "Photo postcards" paragraph.
Update 0.65.0: shipped main/gh-pages 6bfbbd4 (Pages run success, live index.html blob c92d7c1 matches), ios-app 9f6ab53 (Native builds success, with the new InfoPlist.strings), Claude copy version 115. 0.64.0 ios-app 22f6397 Native builds success too.
Update 0.65.1: patches read base651.html now; base65.html removed. Sharper photo postcards (96x72). Checked: screenshots, a 0.65.0 postcard still renders at 64x48, no page errors, axe clean on Today, the wall, the journal and Your year.
Shipped 0.65.1: main/gh-pages 9cf805c (Pages success, live blob 244c851 matches), ios-app 4f8db85 (Native builds success), Claude copy version 116.
Update 0.66.0: patches read base66.html; base651.html removed. Widget code changed on ios-app (WidgetBridgePlugin.swift, ForgelingsWidget.swift, Android WidgetBridgePlugin/ForgelingsWidgetProvider/layout). Checked: peek in English and Japanese, the widget snapshot through a mocked bridge (post PNG 288x216), no page errors.
Update 0.67.0: patches read base67.html; base66.html removed. Checked: a 30-page player gets one letter in English and Japanese, bright and dark voice, Today row clears once read, Letters list reopens it, axe clean on Today, the letter and the list.
Shipped 0.67.0: main/gh-pages f0488f3 (Pages success, live blob 250db0d matches), ios-app 4f7737f (Native builds success), Claude copy version 118.
Update 0.68.0: patches read base68.html; base67.html removed. Checked: a road postcard mid-wander and on the wall after return (English bright, Japanese dark), On this day row and sheet, axe clean on each.
Shipped 0.68.0: main/gh-pages 9adb0b7 (Pages success, live blob d362b05 matches), ios-app cca1759 (Native builds success), Claude copy version 119.
Update 0.69.0: patches read base69.html; base68.html removed. Checked: pocket a card, it waits on top the next day with the same words, choosing it empties the pocket; the welcome back page in both languages; axe clean.
Update 0.70.0: patches read base70.html; base69.html removed. Checked: Close the day at 10 pm (Dubai time zone) in English and Japanese, dark theme, Goodnight clears it; a habit after five answers; axe clean.
Shipped 0.69.0: main/gh-pages 116ffab, ios-app 923fde0 (see monitor), Claude copy version 120. Shipped 0.70.0: main/gh-pages 83ec273, ios-app 8a74d88, Claude copy version 121.
Update 0.71.0: patches read base71.html; base70.html removed. Checked: with the clock at December 3, Today offers November's book; pages flip with focus kept; the share picture has no photos or words; English and Japanese; axe clean.
Native builds: 0.69.0's iOS job was cancelled when 0.70.0 was pushed (Android passed); 0.70.0 (8a74d88) and 0.71.0 (b694407) Native builds success, so the same native code built. Shipped 0.71.0: main/gh-pages 1881a7a (Pages success, live blob aeed276 matches), Claude copy version 122.
Update 0.72.0: patches read base72.html; base71.html removed. New art script art/cardback72.py (imports cardback.py; patch72 embeds its packed SVGs). Checked: frame-by-frame screenshots of choosing, the pack and a Legend build-up (a test copy dealing one card per rarity), English and Japanese, day and night, reduced motion, axe clean on the choose sheet and the summary.

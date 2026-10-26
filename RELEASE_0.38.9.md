# 0.38.9 fix release

Released 2026-10-26. Main and gh-pages at 5ddb972 (Pages deploy for that SHA: success). Source synced to ios-app (no native binary built).

- Fix: 0.38.8 put the "Sit with ..." button in the sleeping Hearth (`sleepHTML` has no `away`/`n`), so the Hearth threw a ReferenceError while Forgelings slept and the awake Hearth had no button. It now sits right under the awake scene.
- They Remember: `snackKnown` is kept only when true, so a restored backup matches the exported cards.
- Room: styles for 8 unused classes removed; icons recompressed losslessly. 629.3 KB (test line 630 KB).
- Tests: qa_389 (9); Hearth suites open folding sections by name; qa_386 opens a drawn realm; reliability.cjs reads the cache name from pwa/sw.js; qa_axe/qa_axe2 print PASS/FAIL lines for the stricter runner.

Validation: syntax check; qa/reliability.cjs; qa_pwa (11/11); full browser suite (53 suites, 125-day journey, 6 monkey seeds) all clean, run in batches after two container restarts. qa_21's noon/greeting checks depend on a fake clock that occasionally slips; they passed on rerun.
Not verified here: fetching the live page (this environment blocks github.io), iPhone/Safari device checks, native build. Check Settings shows "prototype 0.38.9" on the phone after relaunching.

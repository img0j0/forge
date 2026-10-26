# 0.38.7 reliability patch

Released 2026-10-26. Preserves They Remember and the existing save key/schema.

- Persistent save warning provides backup/export and retry access after local-storage or native Preferences write failure. Independent failure channels prevent one successful copy from hiding failure of another.
- PWA cleanup only deletes versioned Forge caches. Navigation matches the app scope exactly, falls back for HTTP errors, and extends cache-write lifetime.
- QA runner returns nonzero for FAIL output, crashes, timeouts and runs with no PASS output; accepts optional suite names for focused checks.

Validation: all inline JavaScript and generated worker parse; qa/reliability.cjs passes storage-warning/retry/export, memory JSON persistence, independent native error, scoped cache cleanup, network cache update, HTTP-503 and offline fallback checks. Temporary fixtures verified runner pass/fail/crash/empty/timeout exit behavior.

Limitations: full historical browser suite and iPhone/Xcode tests not run. Playwright package exists but browser installation failed. Native source is synchronized; no native binary was built.

Run from dev root: node qa/reliability.cjs (requires generated pwa/sw.js; run python3 pwa.py first). Existing Python browser suite remains separate.

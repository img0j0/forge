# Forgelings: build workspace (dev branch)

This branch holds everything needed to keep building Forgelings in a fresh session. The live site is on `gh-pages` (mirrored on `main`), and the iPhone project is on `ios-app`.

**Read `RELEASE_PROCESS.md` and `forge-handoff.md` first.** It has the design rules, the technical facts, the QA notes and what's next.

## Set up a new session (about 2 minutes)

    git clone -b dev https://github.com/img0j0/forge forge-dev
    cd forge-dev/qa && npm i axe-core && cd ..
    pip install playwright pillow --break-system-packages   # Chromium is usually preinstalled; if not: playwright install chromium

## What's here

| Path | What it is |
|---|---|
| `work.html`, `base731.html` | The current build, 0.73.1, in English (identical files) |
| `app.html` | What ships: `work.html` with its Japanese built in (`i18n/build.mjs`; `pwa.py` makes it) |
| `history/patchNN.py` | Every version's patch script, for reference |
| `pwa.py` | Packs `work.html` into `pwa/` (the website) |
| `legal/` | `page.py` builds privacy, terms and support pages into `legal/out/` |
| `curios/` | Curio pixel art: edit `sprites.py`, run it, then `tojs.py` |
| `slim/` | The SVG slimming tool used in 0.30.1 |
| `tools/` | Game tuning simulations |
| `qa/` | The regression suite: `bash qa/runall.sh`, about 80 minutes, then read `qa/full_summary.txt`. The offline suite runs through `qa/pwa_serve.sh`, which serves a fresh build at /forge/ |
| `base.html`, `base12-14.html`, `forge-pilot.html`, `cal.js` | Old builds and helpers that `qa_mig` and `qa_15` need |

## Making the next version

`RELEASE_PROCESS.md` is the source of truth; in short:

1. Write `history/patchNNN.py`: it reads the current `baseNNN.html` (see the table above), applies count-asserted `rep(old, new)` edits, writes `work.html` and runs `node --check`. Copy the shape of the latest patch. Bump the title and `VERSION`.
2. New English text needs its Japanese in `i18n/ja/*.json`; `node i18n/scan.mjs work.html` must show no warnings.
3. `cp work.html baseNNN.html`, `git rm` the old base, `python3 pwa.py` (builds `app.html` and `pwa/`).
4. Targeted checks only (Hunter tests each release himself; don't run the full suite): screenshots in English and Japanese, day and night, and `qa_axe` when markup changes.
5. Update this file's build line, `forge-handoff.md` and `RELEASE_PROCESS.md`, then `SESSION=<chat session URL> tools/ship.sh "message"` (pushes dev, main, gh-pages fast-forward only, and ios-app).
6. Publish `app.html` to the Claude page, swap the project copy, check the Pages and Native builds runs for the printed SHAs and the live blob, then add the "Shipped" line.

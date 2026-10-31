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
| `work.html`, `base45.html` | The current build, 0.45.0 (identical files) |
| `history/patchNN.py` | Every version's patch script, for reference |
| `pwa.py` | Packs `work.html` into `pwa/` (the website) |
| `legal/` | `page.py` builds privacy, terms and support pages into `legal/out/` |
| `curios/` | Curio pixel art: edit `sprites.py`, run it, then `tojs.py` |
| `slim/` | The SVG slimming tool used in 0.30.1 |
| `tools/` | Game tuning simulations |
| `qa/` | The regression suite: `bash qa/runall.sh`, about 80 minutes, then read `qa/full_summary.txt`. The offline suite runs through `qa/pwa_serve.sh`, which serves a fresh build at /forge/ |
| `base.html`, `base12-14.html`, `forge-pilot.html`, `cal.js` | Old builds and helpers that `qa_mig` and `qa_15` need |

## Making the next version

1. Write `patch46.py` at the top of this folder. It reads `base45.html`, applies count-asserted `rep(old, new)` edits and writes `work.html`. Copy the shape of `history/patch45.py`. Bump the title, `VERSION`, `SEEN_V` (to 51) and add a What's New entry.
2. Check the script: extract the `<script>` and run `node --check` on it.
3. Add `qa/qa_44.py` for the new feature, add it to `qa/runall.sh`, and run the full suite.
4. Ship: `python3 pwa.py`, copy `pwa/` into a clone of `main`, commit, then `git push origin main` and `git push origin main:gh-pages`.
5. Copy `work.html` to the `ios-app` branch as `forgelings.html`, then run `python3 build-www.py` and `npx cap sync ios` there, and push.
6. Here: `cp work.html base45.html`, `git rm` the previous base copy, move `patch45.py` into `history/`, update `forge-handoff.md`, and push this branch.

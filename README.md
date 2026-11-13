# Forgelings: build workspace (dev branch)

Everything needed to keep building Forgelings in a fresh session. The live site is on `gh-pages` (mirrored on `main`); the iPhone and Android project is on `ios-app`.

**Current build: prototype 0.82.1** (`work.html` = `base821.html`). Read `forge-handoff.md` (state, rules, what's next) and `RELEASE_PROCESS.md` (how to ship) first.

## Set up a new session (about 2 minutes)

    git clone -b dev https://github.com/img0j0/forge forge
    git clone -b main https://github.com/img0j0/forge forge-main
    git clone -b ios-app https://github.com/img0j0/forge forge-ios
    cd forge/i18n && npm install && cd ..        # needed by pwa.py (Japanese build)
    cd qa && npm i axe-core && cd ..             # for the axe suites
    pip install playwright pillow --break-system-packages   # Chromium is usually preinstalled

## What's here

| Path | What it is |
|---|---|
| `work.html`, `base821.html` | The current build in English (identical files). Patches read the base |
| `app.html` (built) | What ships: `work.html` with its Japanese built in. `python3 pwa.py` makes it and the website in `pwa/` |
| `history/patchNNN.py` | Every version's patch script; copy the shape of the latest |
| `i18n/` | Japanese: `ja/*.json`, `scan.mjs` (what needs translating), `build.mjs`, `GLOSSARY.md`, `README.md` |
| `tools/ship.sh` | Commits and pushes dev, main, gh-pages (fast-forward only) and ios-app; prints SHAs |
| `tools/lived_save.py` | Plays the build for N days through real taps and saves a lived-in save (store screenshots, demos) |
| `qa/` | The regression suite (`qa/README.md`). Full run about 75 minutes; before store submissions, not every release |
| `creatures/` | Forgeling art source and its checks (`creatures/README.md`) |
| `curios/`, `art/`, `slim/` | Curio sprites, card backs and icons, the SVG slimming tool |
| `legal/` | Privacy, terms and support pages (`page.py`), the Japanese store listing, App Store In-App Events |
| `tools/`, `prototypes/`, `statue_src.js` | Game tuning simulations, the voxel prototype, the statue code inlined in 0.39 |
| `base.html`, `base12-14.html`, `forge-pilot.html`, `cal.js` | Old builds and helpers that `qa_mig` and `qa_15` need |
| `RELEASE_0.38.7.md`, `RELEASE_0.38.9.md` | Notes from those two releases |

## Making the next version

`RELEASE_PROCESS.md` is the source of truth; in short:

1. Write `history/patchNNN.py`: it reads the current base, applies count-asserted `rep(old, new)` edits, writes `work.html` and runs `node --check`. Bump the title and `VERSION`.
2. New English text needs its Japanese in `i18n/ja/*.json`; `cd i18n && node scan.mjs ../work.html` must show no warnings.
3. `cp work.html baseNNN.html`, `git rm` the old base, `python3 pwa.py`.
4. Targeted checks only (Hunter tests each release himself): screenshots in English and Japanese, day and night, and `qa_axe` when markup changes.
5. Update this file's build line, `forge-handoff.md` and `RELEASE_PROCESS.md`, then `SESSION=<chat session URL> tools/ship.sh "message"`.
6. Publish `app.html` to the Claude page, swap the project copy, check the Pages and Native builds runs for the printed SHAs and the live blob, then add the "Shipped" line.

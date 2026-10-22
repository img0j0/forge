# Forge regression suite

Everything here tests `work.html`, the current build of the Forge app (single file). Replace `work.html` with a new build and run the suites to check it.

## One-time setup
    pip install playwright && playwright install chromium
    cd qa && npm i axe-core

## Run everything (about 75 minutes, including the journey)
    bash qa/runall.sh      # then read qa/full_summary.txt

## Run one suite
    cd qa && python3 qa_13.py        # PASS/FAIL lines, then a count

| Suite | What it covers |
|---|---|
| qa_core | every dev tool, backup export/restore, overnight rollover, 28 damaged-save cases |
| qa_layout | 7 screen widths: overflow, tap-target size, text content, console errors, outside requests |
| qa_axe, qa_axe2 | accessibility (axe-core): map, then every screen and dialog, light and dark, both moods |
| qa_map, qa_map2 | the sketched map: stages, names, shade, world marks, reduced motion |
| qa_13, qa_131 | Map tab, realm pages, Today map card, callings in the binder, bundled fonts |
| qa_14 | The Kept Day: second reading, gating, legacy and damaged cards |
| qa_15 | world events (history frozen, 12 kinds) and all 12 solo Alone-Hours behaviours |
| qa_17 | Echoes (anniversaries, month-end, oldest wins, only after the calling), the mirror counts, the shared-world line, axe on the new states |
| qa_18 | design rules: one hero and one filled button per Today state, 44px targets on every screen, Hearth folds, Binder sentence, 320px fit |
| qa_181 | living sky: right colours for dawn, day, dusk and night in light and dark; the Sky setting (follow your day, always day, always night, plain); live redraw at 5pm and on rotation; damaged settings repaired |
| qa_19 | bond stories (five chapters per Forgeling, unique, locked by bond level, shown on bond-up and from the card) and the growing Hearth (16 things by the fire from your callings, drawn into the scene, announced once); reduced-motion Hearth draws |
| qa_20 | wanders to a realm, realm curios, requests (when they come, spacing, never expire, answered by anyone, +3 bond, thank-you keepsakes drawn on the sprite), Map send button, damaged saves |
| qa_21 | first impressions: title scene by time of day, the age rules behind it (adult, teen, under 13 blocked and nothing saved, leaning younger), small and sideways phones, reduced motion, home-screen icon, first-day close, ribbon notes that never land on another screen, greeting, arrival |
| qa_22 | aesthetic polish: pixel card back and paper face, the night stage for the reveal, packs and card close-up (still under reduced motion), Journal flame and moon stamps, ribbon rosettes with dots instead of bars, the one-row Binder filter and its sheet, app size under 600 KB |
| qa_222 | adults only while testing (17 turned away, nothing saved), the privacy note and terms, erase everything (confirm tap, stays erased) |
| qa_223 | pixel panel frames on Today and Settings, the pedestal and firelight behind the Forgeling, no sideways scroll, 320px fit |
| qa_23 | the five realm games (title, Forgeling in the scene, 44px controls, rewards within visits, lantern rounds, sit together, free play and Play again, leaving mid-game, once-a-day curio, damaged records, reduced motion) and the fuller first week |
| qa_24 | share picture (size, art, rivets, alt text, share sheet and fallbacks), backup nudge timing and file save, restore from a file, calling phrasings, your own small thing (Settings, Today tick, Journal, no rewards), damaged records, What's new, layout at 320/430 and axe |
| qa_241 | soft music on by default, really plays after a tap, off is remembered, older saves get it on, never plays with all sound off |
| qa_242 | plays all five games with real touch taps on visible targets and real finger drags at 390x844, 375x667 and with reduced motion: each opens, scores, grows bond, never scrolls the page |
| qa_25 | 0.25 games with real touch: Start cards (trait, gift, twist), streaks, sparkles, 20 s finish, each trait's effect, each bond gift, each dark twist, results, reduced motion, Start-card fit at 320/430 and axe |
| qa_251 | the game chooser (0.25.2): any Forgeling by the fire plays any of the five games; who-plays chips, Home game first, traits and twists follow the player, bond to the player, Play again keeps the game, wanderers skipped, axe |
| qa_26 | old tales: 20 pages map to curios by realm, Tales tab with all five, missing-page hints, whole tale and ribbon, page shown on a wander find, repeat curio shows none, realm page progress, lore off hides it, damaged curios, 320/430 layout and axe |
| qa_27 | places on the map: first place per known realm, wander to a realm and anywhere, trail, fully charted gold mark and ribbon, no counts on the Map, realm page list, damaged records, all 25 places fit inside their realms and clear of names, 320/430 layout and axe |
| qa_pwa | the installable copy served from /forge/ like GitHub Pages: manifest and icons, offline helper, opens with no connection, prototype tools hidden, no outside requests. Serve pwa/ first (see pwa.py) |
| qa_fit, mo | worst-case card back fit; inspect screen reachable on small and landscape screens |
| qa_odds | published odds equal the code, legendary rate per year, safety net |
| qa_time | Sleeper's Welcome tiers, sprout growth, wanderers, all 20 curios |
| qa_clock | midnight with the app open, daylight saving, clock moved back, 400-day absence, time zones |
| qa_mig | saves from 0.9.8, 0.11, 0.12, 0.13, 0.14 opening in the current build; blocked or full storage |
| qa_journey | about 4 months of real taps (do, all in, rest, gaps; packs, Hearth, wanderers, journal, echoes), save checked every day, then backup and restore. Set JOURNEY_DAYS and JOURNEY_SEED |
| monkey.py N | seeded random-tap stress run (260 actions), seed N |

Old builds used for migration and history comparison are in this folder (`base*.html`, `forge-pilot.html`). `work.html` is prototype 0.27.0; `base26.html` is 0.26.0; `base252.html` is 0.25.2; `base251.html` is 0.25.1; `base25.html` is 0.25.0; `base242.html` is 0.24.2; `base241.html` is 0.24.1; `base24.html` is 0.24.0; `base23.html` is 0.23.0; `base223.html` is 0.22.3; `base222.html` is 0.22.2; `base221.html` is 0.22.1; `base22.html` is 0.22.0; `base21.html` is 0.21.0; `base20.html` is 0.20.0; `base19.html` is 0.19.0; `base181.html` is 0.18.1; `base18.html` is 0.18.0; `base171.html` is 0.17.1; `base17.html` is 0.17.0; `base16.html` is 0.16.0; `base15.html` is 0.15.4. `patch17.py` turns base16 into 0.17.0; `patch171.py` turns base17 into 0.17.1; `patch18.py` turns base171 into 0.18.0; `patch181.py` turns base18 into 0.18.1; `patch19.py` turns base181 into 0.19.0; `patch20.py` turns base19 into 0.20.0; `patch21.py` turns base20 into 0.21.0; `patch22.py` turns base21 into 0.22.0; `patch221.py` turns base22 into 0.22.1; `patch222.py` turns base221 into 0.22.2; `patch223.py` turns base222 into 0.22.3; `patch23.py` turns base223 into 0.23.0; `patch24.py` turns base23 into 0.24.0; `patch241.py` turns base24 into 0.24.1; `patch242.py` turns base241 into 0.24.2; `patch25.py` turns base242 into 0.25.0; `patch251.py` turns base25 into 0.25.1; `patch252.py` turns base251 into 0.25.2; `patch26.py` turns base252 into 0.26.0; `patch27.py` turns base26 into 0.27.0. `pwa.py` (run in the build folder) packs work.html into the installable site that lives at img0j0.github.io/forge. New players now see a title screen first; `first_card()` in lib.py taps Begin for you.
`audit.js` is a static scan of the build. `cal.js` proves past world events did not change.

## Known limits
`qa_16.py` (margin notes, realm page revisions) is not in this kit and needs rebuilding.
The faked clock is stored in both session and local storage: headless Chromium sometimes drops session storage across an immediate reload.
Remember `cd qa && npm i axe-core` after unzipping, or the two axe suites cannot run.
Headless Chromium only, no real phone. Clock tests fake `Date` rather than waiting. A few suites take 2 to 4 minutes each.

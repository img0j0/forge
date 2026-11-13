# Forgelings regression suite

Everything here tests `work.html` (the English build; most suites) or the built site in `pwa/` (qa_pwa, reliability.cjs). The current build is 0.73.1.

## One-time setup
    pip install playwright pillow --break-system-packages   # Chromium is usually preinstalled
    cd qa && npm i axe-core

## Run everything (about 75 minutes, plus the monkeys)
    bash qa/runall.sh                 # then read qa/full_summary.txt; exits nonzero on any failure
    MONKEYS="1 2 3" bash qa/runall.sh # keeps the main run under two hours; run python3 monkey.py 4..6 afterwards
    bash qa/runall.sh qa_45 qa_46     # chosen suites only

Hunter tests each release himself, so a full run is for App Store submissions, not every release (see `RELEASE_PROCESS.md`). The last full run was on 0.73.0: everything passes except qa_52's intermittent "newer iCloud save while open" check (needs real devices); journey 9/9; monkeys clean.

## Run one suite
    cd qa && python3 qa_45.py        # PASS/FAIL lines, then a count

## Helpers
- `lib.py`: `first_card()` (Begin, then the age question as an adult), `turn_card(pg)` (the three-card choice, 0.64+), `tabto(pg, tab)` (opens every Settings section; `fold=True` keeps them folded).
- `pwa_serve.sh`: builds and serves `pwa/` at `http://localhost:8765/forge/` for qa_pwa.
- `../audit.js` is a static scan of the build; `../cal.js` proves past world events never change.
- Old builds `../base.html`, `../base12-14.html`, `../forge-pilot.html` are kept for qa_mig and qa_15.

## Suites

Each file names the version it was written for; many have been updated since. Releases 0.53 onward were checked with screenshots, qa_axe, qa_contrast and `i18n/scan.mjs` instead of new suites. `qa_52dbg.py` is a debugging copy of qa_52.

| Suite | What it covers |
|---|---|
| qa_13 | Map tab, realm pages, Today map card, callings in the binder, bundled fonts |
| qa_131 | Map tab, realm pages, Today map card, callings in the binder, bundled fonts (part 2) |
| qa_14 | The Kept Day: second reading, gating, legacy and damaged cards |
| qa_15 | world events (history frozen, 12 kinds) and all 12 solo Alone-Hours behaviours |
| qa_17 | 0.17.0: Echoes (anniversaries on Today), the mirror (what you have done), and the shared-world line. |
| qa_18 | 0.18.0 design rules: one hero and one filled button per Today state, quiet grouped rows, 44px targets, |
| qa_181 | 0.18.1: the living sky. 0.46: the field journal replaced the drawn sky; the same setting now chooses the page (paper by day, |
| qa_19 | 0.19.0: bond stories (a chapter of each Forgeling's own story per bond level) and the Hearth that grows from your callings. |
| qa_20 | 0.20.0: wanders go to a realm on your map, curios belong to realms, and Forgelings make requests. |
| qa_21 | 0.21.0: first impressions. The title scene and the age rules behind it, the home-screen icon, |
| qa_22 | 0.22.0: aesthetic polish. Pixel card back and paper face, the night stage for big moments, |
| qa_222 | 0.22.2: adults only while testing, the privacy note and terms, and erasing everything. |
| qa_223 | 0.22.3: panels in pixel material; the Forgeling stands on a pedestal in firelight. |
| qa_23 | 0.23.0: a game for each realm (with your Forgeling in it), rewards within visits, free play after, and a fuller first week. |
| qa_24 | 0.24.0: share a Forgeling picture, the backup nudge and file save/restore, calling variety, your own small thing. |
| qa_241 | 0.24.1: soft music is on by default until the player turns it off. |
| qa_242 | 0.24.2: every game is played the way a person plays it: real touch taps on what is visible on screen, and real finger |
| qa_25 | 0.25.0: your Forgeling shapes its game (trait from a stat, a bond gift at Close, a dark twist), and every game feels |
| qa_251 | 0.25.2: Play opens a chooser where any Forgeling by the fire can play any of the five games. (Was 0.25.1's |
| qa_26 | 0.26.0: the old tales. Each realm's four curios each remember one page; four pages make the tale whole. |
| qa_27 | 0.27.0: places on the map. First place with your first Forgeling in a realm; each wander there uncovers the next. |
| qa_271 | 0.27.1: gaps from the full walkthrough. One realm name everywhere; no nudge promise; first-day note points to the |
| qa_28 | 0.28.0: a Forgeling that notices your days. Showing up warms the bond of the Forgeling by the fire; the Hearth brings |
| qa_281 | 0.28.1: the app is called Forgelings; "the Forge" stays as the world. Support email in the privacy note. |
| qa_29 | 0.29.0: gift links. A curio travels to a friend inside a link; played with real taps on both phones. |
| qa_30 | 0.30.0: pixel-art curios, a real shelf, a curio by the fire, the gift unwrap. Real taps. |
| qa_301 | 0.30.1: room to grow. Slimmer pixel SVGs and one unused font face dropped; nothing visible changes. |
| qa_31 | 0.31.0: the inked map. Paper, inked coasts, watercolour realms, sea waves, trails, fog, compass and ribbon. |
| qa_32 | 0.32.0: the iPhone app layer, tested with a stand-in for Capacitor's plugins (kept on the test side so it survives |
| qa_33 | 0.33.0: pacing for the long run. One new find a day; the map inks more slowly; nothing ever goes backwards. |
| qa_34 | 0.34.0: a favourite Forgeling on Today (after each day's new find), and campfire card backs. Real taps. |
| qa_35 | 0.35.0: the Forge. Embers from done days (two on all-in days), spares as ingredients, a Forge panel at the Hearth, |
| qa_351 | 0.35.1: Living Sky. 0.46: the field journal replaces it: a paper page by day, lamplit at dusk, night or Dark; ribbons for tabs; |
| qa_36 | 0.36.0: Your small things. What you want more of (leaning the deck), up to three own small things on the card, |
| qa_37 | 0.37.0: Ink. How did it feel? (one tap), ink-touched Forgelings on line days, the book that grows with total lines, |
| qa_38 | 0.38.0: The Scribe (60 lines in total; since 0.63, 60 pages: days done plus days with a line of your own), its reading by the fire, Hearth lines about your own small things, ribbon. |
| qa_383 | 0.38.3: Settings folds into sections, each showing its current choice. Real taps. |
| qa_384 | 0.38.4: today's card has a real face: the deck's indigo and gold frame, a pixel emblem per calling, a ribbon |
| qa_385 | 0.38.5: the daily set. Week tiles (flame, moon), a This week panel with Latest finds on a shelf, feeling faces, |
| qa_386 | 0.38.6: emblems for games, snacks and wander realms; parchment for the map's notes and the realm page; gold wander button. |
| qa_389 | 0.38.9: the companionship button sits beside the awake Hearth scene; the sleeping Hearth renders without errors. |
| qa_39 | 0.39.0: Voxel Statues. Cast at the Forge at bond 5 for 6 embers, one per Forgeling, keepsake as worn, 10 stands, |
| qa_40 | 0.40.0: Living Hearth. Tap-to-hop with a line, dozing after 10 pm (a tap wakes one), weather from the seated realm, |
| qa_401 | 0.40.1: preview a statue in clay before it can be cast (companion panel, Forge), no colour, no stand, no picture. |
| qa_402 | 0.40.2: the audit fixes. Loops sleep when nothing moves, a new release is offered on return, backups keep this |
| qa_41 | 0.41: the other side. The Crossing Lantern (visible from the start, first once a realm is charted), turning the map |
| qa_411 | 0.41.1: statue links. Share a cast statue as a link; a friend's browser rebuilds it in 3D from the link alone, |
| qa_42 | 0.42: the living map. Pixel landmarks for every place (front and back) with 44-point targets and a close-up; |
| qa_43 | 0.43: tidier pages. On a well-played save every everyday page fits about one phone screen, and everything that |
| qa_431 | 0.43.1: safe saves. One tab at a time; an unreadable save gets a recovery sheet (safety copy, restore, copy, start over); |
| qa_44 | 0.44: realm dioramas. A fully charted realm's page on the Map opens a small floating voxel island of its five places, |
| qa_441 | 0.44.1 interface pass: the fireside picker fits every phone width, the Binder's summary stays clear of the sky's |
| qa_45 | 0.45: relics and gifts. A realm relic is forged from a spare of each of the realm's four curios and 8 embers; it sits on |
| qa_46 | 0.46: the field journal. Cover, taped-in find with its calling stamped, the Binder as an album of captioned prints, |
| qa_47 | 0.47: the rest of the journal. Hearth photo, letter, note, ink boxes and index; Forge sorted Ready / Still / Made; |
| qa_471 | 0.47.1: How did it feel? (0.63: the faces are the day's question every third day, data-ask; answering turns them into today's page) Each face and its word sit inside the journal's ink circle, centred, by day and lamplight, |
| qa_48 | 0.48: ink and paper, moving. The pack is a sealed envelope; a new Forgeling is pencilled, inked, coloured and stamped, |
| qa_482 | 0.48.2: the cover (Hunter, on his phone). The Forgeling on the label is drawn at a real size, scaled to the screen; |
| qa_485 | 0.48.5: the phone's date moving back a day or two (travel west after midnight, a clock changed by hand) holds the |
| qa_49 | 0.49: the binder finds Forgelings by name and filters by realm (in the Filter sheet); on the website in a browser tab, |
| qa_50 | 0.50: the games get little worlds and one new thing each; the game sheet is postcards; your Forgeling reacts; a round |
| qa_501 | 0.50.1: sky lanterns lift off the lantern that finished the round and settle along the top in its colour; |
| qa_502 | 0.50.2: the update note ("Load it") and toasts are easy to read by day and by night. |
| qa_51 | 0.51: your Forgeling on Today, a binder that scrolls, a joined Map/Tales/Journal switch, toasts from the top. |
| qa_52 | 0.52: the iCloud copy (iPhone app), Android back button, backup and edge wording, and Android screen edges. |
| qa_axe | accessibility (axe-core) on the map; prints one AXE line |
| qa_axe2 | accessibility (axe-core) on every screen and dialog, light and dark; prints one AXE line |
| qa_clock | midnight with the app open, daylight saving, clock moved back, 400-day absence, time zones |
| qa_contrast | 0.44.2: text contrast on every screen, by day and by night, in light and dark themes (axe skips text on translucent |
| qa_core | every dev tool, backup export/restore, overnight rollover, 28 damaged-save cases |
| qa_fit | worst-case card back fit |
| qa_journey | A long, realistic run: ~4 months of days played only through taps a person would make. |
| qa_layout | 7 screen widths: overflow, tap-target size, text content, console errors, outside requests |
| qa_map | the sketched map: stages, names, shade, world marks, reduced motion |
| qa_map2 | the map, part 2 |
| qa_mig | saves from 0.9.8, 0.11, 0.12, 0.13, 0.14 opening in the current build; blocked or full storage |
| qa_odds | published odds equal the code, legendary rate per year, safety net |
| qa_pwa | The installable copy: served from a /forge/ path the way GitHub Pages serves it. |
| qa_ref | 0.43.1: appearance references. Ten fixed-seed cards (every rarity, light and dark, all five realms) and one statue are |
| qa_time | Sleeper's Welcome tiers, sprout growth, wanderers, all 20 curios |
| monkey.py N | seeded random-tap stress run (260 actions), seed N |
| mo | inspect screen reachable on small and landscape screens |
| monkey.py N | seeded random-tap stress run (260 actions), seed N |
| reliability.cjs | node: save warning and retry, cache cleanup, HTTP and offline fallback (run `python3 pwa.py` first) |

## Notes
- Don't run other browsers during a full run: concurrent browsers make the clock and sky suites flake. qa_40 and qa_clock can flake inside the long run; rerun them alone first.
- This Chromium can wipe `file://` storage mid-run, so runall.sh serves the journey, qa_17, qa_181, qa_21 and qa_clock over http.
- qa_ref compares fixed-seed cards, a statue and the Meadow island with `ref/`; after an intended art change rerun it with `REF_UPDATE=1` and say so in the handoff.
- Test games with real touch (qa_242 style): events fired straight at elements once hid two broken games.
- Headless Chromium only; no real phone. Clock tests fake `Date`.
- `qa_16.py` (margin notes, realm page revisions) was lost and could be rebuilt.

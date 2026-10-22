# Forge handoff (start of a new chat)

Last updated October 22, 2026, at prototype **0.34.0**. This replaces the 0.16.0 handoff PDF.

## Starting a new session

1. Attach the repo with push access: owner `img0j0`, repo `forge`.
2. Clone the **`dev` branch**. It holds the whole build workspace: the current build (`work.html` = `base34.html`), every patch script, `pwa.py`, the legal pages, curio art, tools and the full QA suite. Its README has the setup commands and the step-by-step for a new version. Nothing needs to be attached.
3. Clone the **`ios-app`** branch separately when shipping, and copy each new build there.
4. **Next job: build 0.35, the Forge,** from the design doc (https://claude.ai/artifact/WvF6qntNFo6CfAbRyji9Wj). Hunter loved the doc. The seven decisions in it were put to him on October 22 with recommendations; if he hasn't answered, ask once, and anything left open uses the recommendation.
5. After shipping, push the updated `dev` branch and handoff, swap the project's `claude/Forge (prototype X).html` copy, and republish the Claude page.

## Where things stand

**Forgelings** (renamed from Forge in 0.28.1; "the Forge" is the world's name) is a cozy pixel-creature daily-habit app in one HTML/JS file. Each day you turn over a card with one small thing to do. Do it, and you find a unique Forgeling. Forgelings sit by your Hearth, tell their stories and wander the Map.

- **Live app:** https://img0j0.github.io/forge/. It's installable (Add to Home Screen) and works offline. Hunter uses it daily on his iPhone, and it also works in Edge.
- **Testing:** Hunter uses it himself, then friends and family. The invite text asks testers to send feedback with **Settings → Send my report**.
- **Claude copy:** the Forge page at https://claude.ai/artifact/QgLcL9SXJ3BWaWHzJSQo5w (version 53 = 0.34.0). This copy still shows the prototype tools, so use it for testing and demos. The Claude page can't save files, so Save picture and the backup file do nothing there; they work on the live link. A separate artifact (7Dwvf5MirwuPuAGLm3aypU) is stuck at 0.21.0 and can be ignored or deleted.
- **Project copy:** `claude/Forge (prototype 0.34.0).html`.

## Design rules

- Unique, not a copy of any existing creature game. Every Forgeling is one of a kind.
- Calm. No fear of missing out: no streak loss, nothing expires, and gaps are just gaps.
- Packs are earned, never sold. Odds are published, and there's a pity rule.
- Requests never expire. Only one is open at a time, and a new one waits at least two days.
- Everything stays on the device. No accounts, server, tracking or ads.
- **Adults only (18+) while testing.** This was changed from 13+ on purpose, to avoid teen-privacy legal costs early on.
- Accessible: 44px touch targets, zero axe violations, and reduced motion respected everywhere.

## Shipped since 0.16.0

| Version | What |
|---|---|
| 0.17.0–0.17.1 | Echoes (anniversary cards, at most weekly), the monthly mirror line, "every Forge shares this calendar" |
| 0.18.0 | Design upgrade: one hero and one filled button on Today, grouped rows, Hearth extras folded away, Binder sentence |
| 0.18.1 | Living sky that follows the time of day, plus a Sky setting (follow your day / always day / always night / plain) |
| 0.19.0 | Bond stories (5 chapters per Forgeling); a Hearth that grows 16 things from your callings; fixed the Hearth showing blank with reduced motion on |
| 0.20.0 | Wanders go to a realm; curios belong to realms; Forgeling requests; 5 thank-you keepsakes |
| 0.21.0 | Title scene (sky, fire, sleeping Forgeling), campfire icon, first-day close, ribbon notes that wait their turn, greeting and gentle arrival |
| 0.22.0 | Pixel card back and paper card face; reveal and packs staged at night by the fire; Journal flame and moon stamps; ribbon rosettes; one-row Binder filter |
| 0.22.1 | Installable web app: manifest, offline helper, prototype tools hidden in the hosted copy, home-screen tip, "Send my report" opens the share sheet |
| 0.22.2 | 18+ during testing; plain-English privacy note and terms in Settings; "Erase everything on this device"; larger Ember charm |
| 0.22.3 | Panels in pixel material (stepped frame, lit edge, gold corner rivets, faint texture); the Forgeling stands on a pixel pedestal in firelight. The living sky is unchanged |
| 0.23.0 | A game for each realm with your Forgeling in the scene: Dandelion Drift (Meadow, tap), Keep the Fire (Ember), Skipping Stones (Tide, timing), Snowflake Catch (Frost, steering), Lantern Lights (Dusk, memory). Within the 3 daily visits a round gives +1 to +3 bond, and a great round can find a realm curio once a day; after that, free play just for fun with personal bests. Fuller first week: first wander about 20 minutes, rug after the first calling, lanterns at 5, tree at 15, fireflies at 40, requests from day 2 |
| 0.24.0 | Share a Forgeling: a 720×960 picture card (art, name, rarity, realm, what it was found for, date, Forge mark) sent through the share sheet or saved. Backups: from day 7 with 5+ Forgelings, Today offers once a month to save a copy as a dated .json file; "Remind me next month" snoozes it; Restore accepts the file. Four phrasings per calling (`TASK_ALT`, `taskFor(v,date)`). Your own small thing: one optional habit set in Settings, a tick on Today, dots and a count in the Journal, no rewards. What's new trimmed to the latest ten notes |
| 0.24.1 | Soft music on by default (`settings.music!==false`); turning it off is remembered as `false` |
| 0.24.2 | Game fixes from real touch: Dandelion Drift's seeds never rose (its `drift` keyframes clashed with the sky's; seeds now move by script); Snowflake Catch drags became page scrolls (`.pg` now `touch-action:none`, drag follows the finger with pointer capture); every game now plays with Reduce Motion on |
| 0.25.0 | Deeper games. Each game has a Start card (trait, bond gift, dark twist) and nothing moves until Start. Traits from one stat (normalised 15–99): Drift = Spark (more golden seeds, worth 3), Fire = Grit (slower burn), Stones = Calm (wider calm water), Snow = Calm (gentler fall), Lanterns = Spark (longer glow). Bond gift at Close (`GIFT_LV=3`): dandelion puff (5 seeds), logs (+35 heat, worth 3), lucky stone every 5th skip, big snowflakes (3), evening star forgives one slip. Dark twists: Bramble burrs and Wraith hail (−2, break streak), Inferno cold gusts (2× burn), Abyss drifting calm water, Void quickening lanterns; dark targets ×0.8. 20 s rounds that ramp up, streaks (+2 every 5 in a row; broken by a 2 s pause or a hazard), sparkles and floating +N (off with reduced motion), per-game sounds (`GT`, `gTone`), lantern notes, a 'Time!' finish. Targets from human-paced simulation: Drift 25/42, Fire 24/40, Snow 18/30, Stones 5/9, Lanterns 4/7 (mid/hi). Skipping Stones eased (zone .34, speed 1.4 +.12). Nunito Sans 800 removed (unused) to stay under 600 KB |
| 0.25.1 | Game chooser: Hearth Play opens `openGames(c)` with all five games. `playerFor(ti,c)` picks the Forgeling by the fire if it is from that realm, else the closest-bonded one from that realm, never one out wandering; bond goes to whoever plays. Realms with no Forgeling show “Find a/an … Forgeling to play this one.” (Hunter could only reach the fire Forgeling's game before.) |
| 0.25.2 | Any Forgeling plays any game (Hunter still found 0.25.1 too set: realm-locked games stayed closed). Chooser: pick who plays from the Forgelings by the fire (`gPlayers()`, wanderers skipped; `data-gwho` chips), then any game (`openPlay(c,gi)`). Stats shape every game; a dark Forgeling gets the chosen game's twist, named for that game's realm. Its own realm game is marked Home and listed first. Play again keeps the game (`data-gi`) |
| 0.26.0 | Old tales (a tester asked what curios are for). `TALES[ti]` = title, four pages keyed by curio id (story order), ending. A new curio shows its page in the wander return sheet (`talePageHTML`), and a game curio says so in the Hearth line. Tales tab opens with 'Old tales of the realms' (`oldTalesHTML`), missing pages hint at the realm, whole tales framed in gold. Realm page: 'Old tale: … n of 4 pages found.' Ribbons `tale1` Tale Keeper and `tales5` Keeper of Old Tales. All hidden when lore is off. User-facing copy says 'on the Map tab, under Tales' (the nav tab is Map; 'Chronicle' is internal). Size budget raised to 640 KB (app ~601 KB; both pixel fonts are used on cards) |
| 0.27.0 | Places on the map (Hunter wanted the map to gain detail through exploration). `PLACES[ti]` = five named places with an icon kind and a line. `placesFound(ti)` = 1 once the realm is known, plus `state.explore[ti]` (0–4, one per wander there; 'anywhere' wanders pick a known realm with places left). `placePts` finds five spots per realm clear of the name and glyphs; `placesSVG` draws icons (`iconD`) and a dotted trail. Fully charted: the name's underline turns gold with a diamond; ribbons `chart1` Cartographer, `chart5` Every Corner. Realm page lists found places plus 'There is more to find here.' **No counts on the Map** (qa_map rule): notes say 'One place drawn in so far' / 'A few places' / 'Most of it' / 'Fully charted' |
| 0.27.1 | Gaps from a full new-player and week-one walkthrough. **One name per realm:** `mapName(ti)` gives the name the Map shows (mood plus tier hash), and `rName`, wander sheet and returns, old tales, places and world events all use it (before, a lone Shade Forgeling made the wander say Bramble while the map said Meadow). Not to be confused with `realmName(c)`, a card's own home realm. **No nudge promise:** the morning nudge never sent anything, so the first-day note now suggests a first wander, shows the home-screen tip and has Go to the Hearth (`#fdHearth`); the Settings nudge block is gone (`settings.nudge` is left in saves, unused). Copy: 'Whispers and tales' switch, no 'Chronicle' in player text, journal says 'You showed up today.' on day 1, Tales tab says how to start once, and no 'back from wandering' toast over an open sheet. No SEEN_V bump |
| 0.28.0 | A Forgeling that notices your days (Hunter asked for a deeper experience; the walkthrough showed Today and the Hearth barely touched). **Showing up warms the bond:** `earnDaily` calls `compNotice()`: `companion()` = first by the fire that is not today's new card and not out wandering; +1 bond and a voice line from `COMP_L[dark]`, stored as `state.comp={date,cid,line,up,seen}`. Today's done hero shows `compHTML()`; the Hearth shows the line once that day. Rest and missed days do nothing. **Margin echoes:** from day 8, every 5+ days, `mEchoPick()` picks the oldest journal line 7–60 days old with no reply and not echoed (`state.mEcho={date,k,ans,cid}`, `state.mEchoed`). Hearth card `.mecho` with I did it / Still on it / Let it go (`data-mecho`), stored as `journal[k].reply`, shown in the Journal as 'Later: …'. Answering uses no visit and gives no bond. An unanswered note can come back. SEEN_V=32 |
| 0.28.1 | **The app is now called Forgelings** (Hunter's decision: plain "Forge" is crowded in app stores and trademarks). Title wordmark (`clamp(40px,14.5vw,64px)` so it fits at 320px), home-screen name, manifest, page title, feedback, report, backup file `forgelings-backup-DATE.json`, privacy note and terms all say Forgelings. "The Forge" stays as the world (the Forge asks, every Forge, Forgebound). The save key stays `forge-app-v1`, and the URL stays /forge/. Support email forgelings.app@gmail.com is in the privacy note, the terms and the public pages. SEEN_V=33 |
| 0.29.0 | **Gift links** (from the market review: Forgelings had no way for one player to bring in the next). The curio shelf at the Hearth has 'Send a curio to a friend' (`openGiftSend`: who sends it, which curio, an optional note of up to 80 characters). `giftSend` builds `GIFT_BASE#gift=<base64url JSON>` with {v,g gift id,s sender id `state.sid`,c curio,n name,t theme,d dark,r rarity,e seed,k calling,m note} and shares or copies it. The sender keeps their curio, and `state.giftsSent` counts sends. On load, `giftRead` validates the link (`giftCheck`), stores it in localStorage `forge-gift-in` and clears the hash; it also runs on hashchange. `giftMaybe` (after the boot and after every modal closes) opens `openGiftIn` once the player is onboarded and nothing else is on screen. It draws the sender's Forgeling with `spriteURL(giftSender(g))`; `k` is needed for the sprite. Opening your own link only says it's yours, and a gift opens once (`state.giftsGot`). The title screen shows 'X sent you a gift'. A visitor turned away at the age screen keeps nothing. Ribbons `gift1` Kind Gesture and `giftgot` Well Loved. The privacy note and public page explain that the #fragment never reaches the host. SEEN_V=34. App size about 624 KB of the 640 KB budget |
| 0.30.0 | **Curios get a real look** (Hunter chose curios over the map for an aesthetic pass). All 20 curios and a gift bundle are 16x16 pixel sprites, authored in `curios/sprites.py` (palette letters, 'k' = outline, auto-centred; it also renders a contact sheet). They're exported by `curios/tojs.py` to `curios/csprites.js` (`CSPR`), which patch30 inlines. `cpix(id)` gives pixels, `curioURL(id,sil)` gives a cached data URL (sil = silhouette), and `cImg(id,size,{cls,sil,alt})` gives the img. Emoji are gone from the shelf, wander return, tales list, gift picker and gift sheet. **Shelf** (`shelfHTML`): a wooden plank per realm with 4 places. Found curios are drawn, missing ones are faint outlines, and unknown realms are labelled 'A realm not yet on your map'. Each is a button opening `openCurio`: large sprite, story line (or 'X sent this as a gift' via record `from`), date, count, tale page, and 'Set it by the fire' (`state.hearth.curio`). **Hearth scene**: `fireCurio()` (chosen, else the latest found) is drawn at (39,55), behind the Forgelings and inside the firelight. **Gift unwrap**: the bundle wiggles and fades (1.1 s), then the curio pops in; with reduced motion the curio just shows. Dark theme gives sprites a soft light edge. Made room by dropping the unused Fredoka 400 face (about 21 KB). The app is about 614 KB. SEEN_V=35 |
| 0.30.1 | **Room to grow, nothing visible changed** (614 KB down to 555 KB). `slim/svgslim.py` rewrites the pixel-art SVG data URIs (card backs `--cbT/--cbP` were 25 KB each, plus frames, pedestals and the pack art) from one `<rect>` per pixel run into one `<path>` per run of same-coloured rects, keeping the painting order. `slim/verify.py` confirms identical rendering. Nunito Sans 600 was used by only four small labels, which now use 700, so that face is dropped. Bundled faces are now Fredoka 500/600, Nunito Sans 400/700, Press Start 2P and VT323 (qa_301 checks the list). **Rule: any new pixel-art SVG should go through svgslim, and any new font weight needs a reason.** |
| 0.31.0 | **The map, inked** (Hunter wanted the map more beautiful after a week of use). The SVG sheet now has: paper (`--mpaper`; night paper in dark), grain (`mpGrain`, feTurbulence), burnt edges (`mpEdge` radial gradient with `--mburn`), a double ruled border with corner marks, a ribbon behind the title (`--mrib`), and a compass rose. Realms get a watercolour wash (`mpWash`: turbulence-modulated alpha), a soft pigment edge (`mpBleed`, opacity `--mbleed` = .4 in dark) and an inked outline that wobbles like a pen (`mpInk`: feDisplacementMap 2.6). `seaPts()` puts ink waves on a jittered grid at least 13px from every realm polygon (`polyD`). `TRAILS` pairs draw dotted trails (`trailD`, nearest vertices, gently bent) once both realms are known. `fogSVG(ti)` puts blurred cloud puffs (`--mfog`) over unknown realms, under the faint sketch and the '?'. No counts were added. Sizes and classes the old tests rely on (.mp-faint, .mp-shade, .mk, labels) are unchanged. About 561 KB. SEEN_V=36 |
| 0.32.0 | **Native groundwork** (no visible change on the web). `NATIVE` = running inside Capacitor (`window.Capacitor.isNativePlatform()`), with plugins on `PL` = `Capacitor.Plugins`, which iOS injects with no bundler needed. `STORE` = NATIVE or `<meta name=forge-build content=store>`. **Safe saves:** `save()` bumps `state._sv`, writes localStorage, then `nset(KEY)` (Preferences, debounced 250 ms, flushed when hidden). Boot is wrapped in `boot()`; in native, `nrestore()` runs first and the copy with the higher `_sv` wins. BLOCK is mirrored too, and Erase clears both copies. **Reminders** (`remindSync`, LocalNotifications id 1 and 2): one nudge at `settings.nudge`, scheduled for tomorrow if today's card is already done or rested. It's rescheduled 1 s after every save (`remindSoon`), so a lapsed player gets one nudge, never a pile. A wanderer note (`settings.wnote`) fires at `wander.ready`. Permission is asked when a time is chosen, or once on the first wander (`settings.wAsked`). `remindHTML()` shows the Settings block in native only. **Haptics:** `buzz()` runs from `sfx` (tap/select/tab light, save/no medium), `chime` (success) and `gHit`, with a `settings.haptics` toggle. **Share:** `shareOrCopy` uses `PL.Share`, and backup and share picture use `nshareFile` (Filesystem cache, then Share files). **Store edition:** hides the feedback ask, Share your thoughts, My report and Prototype tools. Cards say `EDITION` = First Edition, and the version label reads 'Forgelings 1.0.0' (`APPVER`). qa_32 tests all of this against a Capacitor stand-in exposed via `expose_binding` (sessionStorage on file:// is unreliable across reloads) |
| 0.33.0 | **Pacing for the long run.** Hunter found nearly all curios and most of the map in about a week, because every wander was guaranteed a new curio and place. Now there's **one new find a day**: `state.disc` = the date of today's discovery. The first wander of a day, or a great game round, can bring a new curio, and that first wander also brings a new place. Later wanders that day bring a spare from that realm, a 'quiet path' note, +1 bond, and 'Tomorrow's first wander will find something new' while anything is left. The destination sheet says so up front. Requests still complete on quiet days. **Map:** `mapTier` is now 1/4/10 Forgelings (was 1/3/6), and `state.mapMax[ti]` remembers the highest stage reached, so a realm never fades. Older saves without mapMax are grandfathered on load with `mapTierOld`. **Test note:** qa_map's `build()` drops mapMax, so older suites test grandfathered saves; qa_26 and qa_27's `ready()` drop `disc`, so each test wander counts as a new day. qa_33 covers the new rules. Rough pace for a daily player: curios in about 3 weeks, the map inked in about 5. SEEN_V=37 |
| 0.34.0 | Two asks from Hunter's daily use. **Favourite on Today:** 'Show on Today' (`#inspHome`) on any card sets `state.homeFav`. In the done state, today's find shows first, with 'Show X here' (`#btnFavBack`). Once the find has been seen (`markFindSeen` on leaving Today or hiding the app sets `state.findSeen` = date), the hero shows the favourite ('X is keeping you company', `#btnShowFav`) with 'See today's find' (`#btnSeeFind`, `ui.showFind`). Rest days show the favourite card too. The fresh state keeps the card back as the call to action. No favourite means no change. **Campfire card backs:** `.cbk` now uses the `--cbT` campfire art (the same as Today's card back), with the details in `.binfo` below the fire. The diamond emblem and the old 'FORGE' wordmark are gone. SEEN_V=38 |

## Key technical facts

- Saves live in localStorage under `forge-app-v1`; seen notes are under `forge-app-v1-seen`. `SEEN_V=38` (0.35 sets 39). The age block key is `forge-age-block`, and `MIN_AGE=18`.
- `sanitize()` repairs damaged saves, and `migrate()` fills new fields from `fresh()`. Newer fields: `explore` (wanders per realm, 0–4), `own` (`text`, `days`), `backup` (`at`, `ask`), `games` (best scores, rounds played, the day a game last found a curio), `settings.sky`, `hearth.fseen`, `request`, `reqLast`, `reqDone`, `keepsR`, `wander.realm`, `echo`.
- The world calendar is a pure function of the date (epoch 2026-01-01). ERAS and EVENTS are append-only, and EV2=287 gates new events, so history never changes.
- Bond stories and Hearth furnishings are derived, not stored: stories from each Forgeling's seed, realm and calling; furnishings from the history of completed callings.
- The script runs inside a closure, so tests drive the screen and read canvas pixels rather than calling functions directly.
- The hosted copy carries `<meta name="forge-build" content="release">`. That switches on the offline helper, hides the prototype tools and shows the install tip.
- **Patch method:** a Python script per version, with count-asserted `rep(old,new)` applied to a preserved base copy (`patchNNN.py` reads `baseNNN.html` and writes `work.html`), then `node --check` on the extracted script.

## Hosting and updates

- **Repo:** github.com/img0j0/forge (public). The site is served from the **gh-pages** branch, and **main** mirrors it.
- **To ship an update:**
  1. Run the full test suite.
  2. Run `python3 pwa.py` in the build folder. It packs `work.html` into `pwa/`, adding the manifest, `sw.js` and icons.
  3. Copy `pwa/` into a clone of the repo, commit, then `git push origin main` and `git push origin main:gh-pages`.
  4. Pages updates within about two minutes. Users get it the next time they open Forge online.
- **In a new chat:** attach the repo with push access (owner `img0j0`, repo `forge`). Clone it into its own folder, not the build folder.
- **After an update, an installed app on iPhone may keep the old version until it is fully closed (swiped away) and reopened online.** Tell Hunter this when he reports something already fixed.
- **The offline helper** loads the page network-first and falls back to the saved copy offline. Its cache name follows the version, so old caches clear themselves.
- **Each device and browser keeps its own save.** To move between them, use Settings → Backup → Save a copy, then Restore a copy.

## QA

- Kit: the **`dev` branch** of the repo (since October 22; the old kit zips are no longer needed). Run `cd qa && npm i axe-core` once, then `bash qa/runall.sh`, then read `qa/full_summary.txt`.
- A full run takes about 75 minutes, so start it detached (`setsid`) and check back. Don't run anything else in a browser while the full run is going, not even a screenshot script. Concurrent browsers make the clock and sky suites flake.
- `first_card()` in `lib.py` taps Begin, then answers the age question as an adult.
- **qa_pwa** tests the installable copy. Serve `pwa/` at `http://localhost:8765/forge/` first.
- Accessibility scans wait for the arrival fade to finish before measuring.
- **Test games with real input.** qa_242 plays every game with real touch taps on what is visible and real finger drags (CDP touch events), at 390×844, 375×667 and with reduced motion. Firing events straight at elements (as qa_23 does) hid two broken games until 0.24.2. New game work must be tested this way.
- CSS animation names are global: check new `@keyframes` names for clashes (`rise` is defined twice, harmlessly).
- **The Map never shows counts or progress bars** (a deliberate early decision; qa_map checks for 'n of 5'). Use gentle words there.
- **Tabs are named Today, Hearth, Binder, Map, Settings in the app.** Never send players to 'the Chronicle' in new copy. Two older strings still say it: the 'Whispers and Chronicle' setting and 'Your Chronicle begins with your first Forgeling.'
- **Ask what the player wants to do, not what the code allows.** Twice Hunter said he couldn't choose his game: first nothing reached other games, then realm locks did. Freedom to choose matters to him.
- **Check a feature can be reached, not just that it works.** Tests opened each game directly, so nothing noticed that Hunter could only reach one of them from the Hearth.
- Timing-sensitive checks belong inside the page (rAF), not driven from Python, which adds 50–150 ms per step. Scans must wait for animations to finish (`document.getAnimations()`), as qa_21 now does.
- qa_22 holds the whole app under 640 KB (raised from 600 KB in 0.26.0; the app is about 601 KB).
- qa_axe and qa_axe2 print one AXE line instead of PASS lines, so their summary shows pass=0 fail=0. Read their logs.

**Status on 0.34.0:** everything passes, including the full run. qa_21's 'title at noon' check fails now and then on 0.26.0 too: a clock-dependent flake, not a regression. qa_21 failed once on the title sky and contrast, then passed 36/36 three times alone on both 0.24.0 and 0.24.1, so treat it as an occasional timing flake.

| Suite | Checks |
|---|---|
| core | 32 |
| layout | 35 |
| map / map2 | 20 / 6 |
| 13 / 131 | 21 / 10 |
| 14 / 15 | 19 / 17 |
| 17 / 18 / 181 | 43 / 41 / 30 |
| 19 / 20 | 31 / 38 |
| 21 / 22 / 222 / 223 / 23 / 24 / 241 / 242 / 25 / 251 / 26 / 27 / 271 / 28 / 281 / 29 / 30 / 301 / 31 / 32 / 33 / 34 | 36 / 30 / 12 / 11 / 50 / 74 / 9 / 69 / 70 / 18 / 25 / 31 / 24 / 29 / 12 / 31 / 26 / 6 / 45 / 23 / 19 / 19 |
| fit / mo / odds | 3 / 18 / 10 |
| time / clock / mig | 30 / 12 / 37 |
| pwa | 11 |

On top of that: the 125-day journey passes 9/9 (all 16 Hearth items, 14 requests and all 5 keepsakes reached), random-tapping seeds 1–6 are clean, and axe reports zero violations.

## Next up

The gameplan doc is https://claude.ai/artifact/H6jmn6CXRKzg4t2E8i9BaE. Phase 1's four build items shipped in 0.24.0 and are marked Done there.

0. **Build 0.35, the Forge, next** (see "Starting a new session" and the Forge section below). Then 0.36 the other side, 0.37 relics and gifts, and the Keeper purchase in 1.1.
0a. **Games (0.25.0):** Watch for tester notes on difficulty, the +2/+3 targets and whether streaks feel good; retune from real scores. Simulation tools used for tuning live in the kit's `tools/` folder.
1. **Remaining Phase 1 items wait on testers:** the simplicity pass (fold away what testers don't find or use in week one) and game tuning (difficulty and the +2/+3 bond thresholds, from real scores).
2. **Native app:** the Capacitor groundwork shipped in 0.32.0 (safe saves, real reminders, haptics, share sheet) and lives on the `ios-app` branch. What's left is in the iPhone app section below. No formal lawyer review (Hunter's call); see the launch prep notes.
4. **For the next build:** write `patch35.py` reading `base34.html` (a copy of the 0.34.0 build), and set `SEEN_V=39`. After shipping, copy the build into the ios-app branch as `forgelings.html`. The app is about 567 KB of the 640 KB budget; What's New keeps 8 entries. Further savings if ever needed: strip JS comments (about 10 KB) and the prototype tools from the release build only, in `pwa.py`. To change a curio's art, edit `curios/sprites.py`, run it and `tojs.py`, then rebuild. **Naming rule:** the app is Forgelings, and the world is the Forge. Never call the app plain "Forge" (qa_281 checks this).
5. **Companion, part 3 (not built yet):** weave the player's own margin lines and stories into each Forgeling's five story chapters. Wait for tester reactions to 0.28.0 first.

## App Store launch prep (October 20, 2026)

- Launch prep doc: https://claude.ai/code/artifact/e434b0bf-1fd9-40b6-865a-09dce1efacb5 (App Store Connect answers, name and trademark findings, review risk, low-cost legal path, checklist).
- Hunter wants to avoid a formal lawyer. The plan is a free USPTO law school clinic (Richmond, Liberty, Howard, GWU or American) for the trademark, plus a flat-fee online review of the pages if needed.
- Public pages are live: `privacy.html`, `terms.html` and `support.html` on the Forge site. They're built by `legal/page.py` (set `FORGE_CONTACT` to add the support email). `pwa.py` copies `legal/out/*.html` into `pwa/`.
- `sw.js` now caches only the app page as the app (`appPage` test). Other pages load normally, so they can't overwrite the cached app.
- Name: "Forge" is crowded (habit apps and 2026 USPTO software filings). The recommendation is to list and register as **Forgelings**, with "the Forge" kept as the world's name. Undecided.
- Decided: the support email is forgelings.app@gmail.com, and the store and app name is **Forgelings** (shipped in 0.28.1).

## iPhone app (October 21, 2026)

- The project lives on the **`ios-app` branch** of github.com/img0j0/forge (kept separate so it isn't served by Pages). It's Capacitor 8 with Swift Package Manager (no CocoaPods), plugins Preferences, LocalNotifications, Haptics, Share and Filesystem, and bundle ID `com.forgelings.app` (changeable until the first upload).
- `forgelings.html` is a copy of the latest build. `build-www.py` marks it as the store edition, then `npm run sync` and `npm run open`. `ios-setup.py` re-applies the icon (pixel campfire, 1024), a dark launch screen, portrait iPhone-only, arm64, and ITSAppUsesNonExemptEncryption=false. The README walks Hunter through the Mac setup, running on his iPhone, and TestFlight.
- `store/`: `listing.md` (name, subtitle, promo text, keywords, description, URLs, App Privacy answer), `screens/forgelings-1..7.png` (1320x2868), `shots.py` (raw captures of a curated state, store edition, @3x) and `compose.py` (captions, frame, and the 'Kind by design' slide).
- **Hunter has no Mac.** He's considering a used M1 Mac mini or MacBook Air (Apple Silicon only: Xcode 26.4+ needs macOS Tahoe 26.2, and macOS 27 drops Intel). A cloud build service is the fallback.
- **Revenue plan (agreed in the Forge design doc, October 22):** free forever, launching 1.0 free, plus a one-time 'Keeper' unlock with the Keeper's Anvil cosmetic patterns (about $9.99) in 1.1. Never materials, packs, odds or progress. Apple Small Business Program = 15%. Charging makes him an EU trader (an LLC or PO box keeps his address private), and the terms need updating.
- Still to do before submission: Apple Developer Program enrollment, testing on a real iPhone (reminders, storage, haptics, share), TestFlight with testers, and wording the terms for a public release ('early version shared for testing').

## The Forge (design approved, October 22, 2026)

- Design doc: https://claude.ai/artifact/WvF6qntNFo6CfAbRyji9Wj. Embers (one per day you do the small thing) plus spare curios (never your last copy) are forged into signed charms, tools (bell, compass, lantern), Hearth pieces and realm relics. The lantern opens the Shade side of the map (5 Shade realms, 25 places, 20 curios, 5 tales). No weapons, and no paid materials or randomness. Revenue is the Keeper unlock with the Anvil's cosmetic patterns (about $9.99, in 1.1).
- Planned versions: 0.35 the Forge, 0.36 the other side, 0.37 relics and gifts, 1.1 the purchase.
- Hunter approved the doc ("absolutely love the forge design doc"). The seven decisions and their recommendations: (1) a Forge panel at the Hearth beside Wander, no new tab; (2) one ember per day of the small thing, plus one on all-in days; (3) a small charm badge in the card corner, charm worn at the Hearth, card art untouched; (4) bright names on the map's front and Shade names on the back, for everyone; (5) 0.35 ships charms, bell, compass and Hearth pieces, with the lantern held for 0.36; (6) $9.99 one time for the Keeper unlock in 1.1; (7) spare counts only on a curio's close-up, never on the shelf.

## Long-lasting play (October 21, 2026)

Hunter flagged that content ran out in about a week. The plan has three layers:
1. **Pace** (0.33.0, done): one new find a day, slower inking, never backwards.
2. **Turn the map over** (next, at launch or in 1.1): a fully charted realm lets you flip to its Shade twin (Bramble, Inferno, Abyss, Wraith, Void). That adds a second sheet with its own places, 20 more curios and five more old tales, doubling what there is to find and paying off lore the tales already hint at.
3. **A world that keeps growing**: each era of the world calendar (56 to 104 days) permanently adds a curio per realm, a place or two, and an era tale. Nothing expires.

Also considered: a field guide showing the 12 callings x 10 realms combinations (a long tail that's already in the app), and longer multi-Forgeling expeditions.

## Market review (October 20, 2026)

Compared with Finch, Habitica, Streaks, Fabulous and Habitify, Forgelings is missing (in priority order):

1. A home-screen widget plus real reminders (native, in the iPhone build).
2. A gentle social loop: gift links shipped in 0.29.0. A real friends list would need a server.
3. A fair business model (one-time unlock or supporter tier, cosmetic only), to decide before launch.
4. More say over your own habits (choose callings, up to 3 own small things).
5. Seasons that come back every year.

Don't chase focus timers, app blockers, leaderboards or heavy stats. Pitch: the gentlest habit app, and a real collection, with Data Not Collected up front.

## Open items

1. **Real-use feedback.** Hunter uses Forge daily and shares it with friends and family. The number to watch is how many testers still open it after three weeks without a reminder.
2. **Reminders exist only in the iPhone app** (0.32.0, local notifications). The website has none, by design.
3. **Legal, taking the cheap route (no formal lawyer, per Hunter):**
   - Keep 18+ and collect nothing for now.
   - Use a law school clinic or a flat-fee online review before charging money, adding a server or analytics, or opening to teens. See the launch prep doc.
   - Do a trademark search on "Forge" and "Forgelings" before investing in branding.
   - The privacy note and terms were drafted by Claude and are not legal advice.
4. **Money:** the Keeper unlock with the Anvil in 1.1 (see the Forge section). Never sell odds, materials or progress.
5. **Sprint doc** (https://claude.ai/code/artifact/297a5ff6-7bd6-4a02-9555-f5aa43618f02) is stale since 0.15.4.
6. **qa_16** was lost from the kit and could be rebuilt.
7. **Ideas not built:**
   - Map border shifts on era change (idea 52). Map ideas not built yet: a sea creature doodle in open water, gently drifting waves, and fog that thins as a realm gets close to being found.
   - Parked: Edge of the Light, a Sleep-Talking experiment, rhythm identity, unseen archivists.
   - Possible later: seasonal content, so a year of daily use stays fresh.
8. **Lore:** the five old tales and the 25 map places are also written into the Lore Bible doc. Ideas raised but not built: curios as gifts to Forgelings; placing curios around the Hearth.
9. **Known tradeoff:** setting the phone's clock back lets someone farm days, since there's no server to check.
9. **Housekeeping:**
   - Hunter is archiving or deleting his unused GitHub repos himself.
   - The 0.9.8 pilot copy is superseded by the live link.

## Links

- Live app: https://img0j0.github.io/forge/
- Forge page in Claude: https://claude.ai/artifact/QgLcL9SXJ3BWaWHzJSQo5w
- Design review doc: https://claude.ai/artifact/RRArQYwBjxntidDhHR2FJS
- Lore bible: https://claude.ai/artifact/FGuFQKYi6gPZpM2Pis9ofz
- Sprint doc: https://claude.ai/code/artifact/297a5ff6-7bd6-4a02-9555-f5aa43618f02

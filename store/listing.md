# Forgelings: App Store listing

Updated November 12, 2026, for 0.73 (choose your card, the journal that writes itself, postcards, letters, seasons, the widget, Japanese). Character limits are Apple's. Counts are included so edits stay inside them.

**Name** (30 max): Forgelings  (10)

**Subtitle** (30 max): One small thing a day  (21)

**Promotional text** (170 max, can be changed any time without review):
A cozy habit journal with no streaks to lose. Do one small thing a day, and a pixel creature is inked into your journal. Miss a day? Nothing is lost.  (149)

**Keywords** (100 max, comma separated, no spaces needed):
habit,cozy,pixel,pet,daily,routine,self care,collect,gentle,mindful,tracker,creature,calm,journal  (97)

**Category:** Primary: Health & Fitness. Secondary: Games (Simulation) or Lifestyle.

**Age rating:** answer the questionnaire honestly (no violence, no mature content), then **Override to 18+** while the terms say 18+.

**Support URL:** https://img0j0.github.io/forge/support.html
**Privacy Policy URL:** https://img0j0.github.io/forge/privacy.html
**Copyright:** 2026 Hunter Abrams (or the LLC's name)

## Description (4,000 max; this one is 2938)

Forgelings is a habit journal that is gentle with you.

Each day, choose one of three face-down cards. Each holds one small thing to do: give one task your full attention, reach out to someone, fix one small annoyance for good. Do it, and a new Forgeling is inked into your journal. Every one is a pixel creature drawn just for that day, from ten realms, each with its own look, stats and story.

MISS A DAY? NOTHING IS LOST.
There are no streaks to break. Rest days are always fine. Your progress never resets, and nothing is ever taken away.

A JOURNAL THAT WRITES ITSELF
The whole app is a field journal: ruled paper by day, lamplit pages at night. After each card, your Forgeling asks one small question, and your answer becomes that day's page. Add your own words if you like, or turn a photo into a pixel postcard for the page (the photo itself is never kept). Each month is bound into a little book, and your companion writes you a letter at milestones.

A HEARTH TO COME BACK TO
Your favourite Forgelings sit by a small fire. Give them a snack, tell them a story, or play one of five little games together. Send one out to wander, and they come back with a curio for your shelf and a postcard from the road. Grow a bond far enough and a Forgeling becomes Forgebound, with a golden glow it keeps for good.

A MAP THAT DRAWS ITSELF
The world starts as blank paper. Each Forgeling you find inks in more of its realm, with places to uncover and old tales to piece back together, one curio at a time. Chart a realm fully, light the Crossing Lantern, and turn the map over to find its Shade side.

MAKE THINGS AT THE FORGE
Every day you show up earns an ember. Bring embers and spare curios to the Forge to make charms your Forgelings can wear, tools for wandering, pieces for the Hearth and relics that finish the old tales. Each one is signed by the Forgeling who helped. A Forgebound Forgeling can even be cast as a little 3D statue.

SEASONS THAT COME BACK
Seven seasons return every year, from Blossom Days to First Snow, each with its own weather by the fire and a stamp for your journal. At the end of the year, look back on your year in Forgelings.

KIND BY DESIGN
- Nothing is for sale. Every Forgeling and every pack is earned by showing up, and the odds are shown in the app.
- No accounts, no ads, no tracking. Your journal stays on your phone, with a quiet copy in your own iCloud so a new phone brings it back. We never see it.
- One gentle reminder a day, only if you want it, and only on days your card is still waiting.
- A home-screen widget, and a Live Activity while a Forgeling is out wandering.
- Send a curio, a charm or a statue to a friend, or send a Forgeling to visit their fire.
- In English and Japanese. Larger text, reduced motion, plain print, and a spoken description of every Forgeling for VoiceOver.

Forgelings is a small, independent app, shaped by a group of early testers. Thank you for trying it.

## Screenshots

`screens/forgelings-1.png` to `forgelings-7.png`, 1320 x 2868 (iPhone 6.9-inch), in the field journal look. **They date from 0.48 (October 31): retake them before submission** so they show the three-card choice, the 0.72 card backs, a written page with a postcard and a season by the fire. Apple scales these
down for the smaller iPhone sizes, so one set is enough. Upload them in order:

1. One small thing a day (Today)
2. Each one drawn just for you (a rare Forgeling, close up)
3. They keep you company (the Hearth, by lamplight)
4. A binder that fills up (the Binder)
5. A map that draws itself (the Map)
6. Make things together (the Forge)
7. Kind by design

Rebuild: `python3 build-www.py`, serve `www/` over http, then `shots.py URL SAVE.json RAW_DIR QA_DIR` (raw captures of the
store edition from a lived-in save; the dev branch's `qa/` supplies the helpers) and `compose.py RAW_DIR FONTS_CSS screens`
(captions, desk, tape). FONTS_CSS is the app's own `@font-face` rules, pulled out of the build.

## App Privacy

Data collection: **No, we do not collect data from this app.** (The iCloud copy lives in the player's own iCloud account, which only their devices can read; Apple does not count that as collection.)

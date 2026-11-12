# Forgeling art (0.54 second generation)

- `genSpec.js`, `cute2.js`, `buildSprite.js`: the creature code as it is in the build (patch54 swaps them in).
- `genSpec.v1.js`, `buildSprite.v1.js`: the 0.53 code, kept for the sameness check.
- `python3 sheet.py OUT.png GEN DARK COUNT COLS SEED0`: a contact sheet (GEN 1 or 2, DARK 0 or 1).
- `python3 same.py`: first-generation sprites must be pixel-identical to 0.53 (prints SAME).

New finds carry `gen:2`. Never change what the first generation draws: people's Forgelings keep their look.

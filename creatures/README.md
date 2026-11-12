# Forgeling art (0.54 second generation, 0.55 rendering, 0.56 40x40 grid)

- `helpers.js`: the 40x40 grid (creature coordinates 0..31 plus a 4-pixel margin; `SPI(x,y)`, `SPN`, `SPC`, `SPP`).
- `genSpec.js`, `cute2.js`, `buildSprite.js`, `render.js` (commit, selout, OL), `palette.js` (makePal): the creature code as
  it is in the build. `mk.py` swaps them into the current build as /tmp/c54.html with a test hook, so edits can be seen
  before a patch.
- `compare.py OUT.png DARK GEN`: before (shipped build) and after (these files), side by side.
- `identity.py GEN`: silhouettes and faces must match the shipped build (run it before shipping a rendering change).
- `clip.py [gen]`: nothing may be cut by the 40x40 frame (a part's fill on the edge). Must print 0.
- `pick.py OUT.png 'JS filter' GEN`: before/after for chosen Forgelings.
- `bob.py [html]`: above the feet, the bob frame must be the rest frame one pixel lower. Must print 0.
- `float.py`: head keepsakes must rest on the head.
- `foil.py OUT.png`: pixels holo foil paints (pink), a build (`BEFORE=`, default /tmp/c541.html) against these files. Any new
  palette slot must be checked against FOIL3, FOIL4 and OL().
- `genSpec.v1.js`, `buildSprite.v1.js`: the 0.53 code, kept for the sameness check.
- `python3 sheet.py OUT.png GEN DARK COUNT COLS SEED0`: a contact sheet (GEN 1 or 2, DARK 0 or 1).
- `python3 check.py 3000`: layout check (faces never covered, off the body, at an edge or on a line). Must print problems 0.
- `python3 same.py`: first-generation sprites must be pixel-identical to 0.53 (prints SAME).

New finds carry `gen:2`. Never change what the first generation draws: people's Forgelings keep their look.

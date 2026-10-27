# Forgelings 0.38.10: room before the Shade side. The two pixel fonts keep exactly the same characters, shapes and
# layout features, but drop TrueType hinting (instructions phones do not use at these sizes). The two pixel fonts
# carried most of it (VT323 18 KB -> 7 KB, Press Start 2P 12.5 KB -> 4.3 KB). About 26 KB lighter. Fredoka and Nunito Sans are untouched (dropping their hints
# moved one curly quote by a pixel, for only 2.5 KB). Reads base389.html.
import re, base64, io
from fontTools.ttLib import TTFont
from fontTools import subset
src = open('base389.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)
def unhint(m):
    raw = base64.b64decode(m.group(1)); t = TTFont(io.BytesIO(raw)); cps = sorted(t.getBestCmap())
    o = subset.Options(); o.flavor = 'woff2'; o.hinting = False; o.layout_features = ['*']; o.name_IDs = ['*']; o.name_languages = ['*']
    o.notdef_outline = True; o.glyph_names = False; o.legacy_kern = True
    sub = subset.Subsetter(options=o); sub.populate(unicodes=cps); sub.subset(t); b = io.BytesIO(); t.flavor = 'woff2'; t.save(b)
    t3 = TTFont(io.BytesIO(b.getvalue())); assert sorted(t3.getBestCmap()) == cps
    return m.group(0).replace(m.group(1), base64.b64encode(b.getvalue()).decode())
n0 = len(src)
src, k = re.subn(r"@font-face\{font-family:'(?:Press Start 2P|VT323)'[^}]*?base64,([A-Za-z0-9+/=]+)", unhint, src)
assert k == 2, k
print('fonts', k, 'saved', n0 - len(src))
rep('<title>Forgelings (prototype 0.38.9)</title>', '<title>Forgelings (prototype 0.38.10)</title>')
rep("const VERSION='prototype 0.38.9'", "const VERSION='prototype 0.38.10'")
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src.encode()))

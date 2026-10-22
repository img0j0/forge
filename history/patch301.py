# Forgelings 0.30.1: room to grow, with nothing visible changed.
# 1. Pixel-art SVG backgrounds (card backs, frames, pedestals, the pack art) are rewritten from one <rect> per pixel
#    run to one <path> per run of same-coloured rects (slim/svgslim.py). Painting order is kept, so they render
#    pixel-identically (slim/verify.py checks this).
# 2. Nunito Sans 600 was used in only four small labels; they now use 700 and the 600 face is dropped.
# Reads base30.html.
import re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'slim'))
from svgslim import slim, conv_svg
src = open('base30.html', encoding='utf8').read()
before = len(src.encode())
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

src, saved, n = slim(src); assert n >= 6, n
# the pack art drawn inside a template string
i = src.index('<g transform="translate(53 60) scale(3)" shape-rendering="crispEdges">'); j = src.index('</g></g>', i) + 8
seg = src[i:j]; new = conv_svg(seg, '"'); assert new.count('<rect') < seg.count('<rect')
src = src[:i] + new + src[j:]

# Nunito Sans 600 -> 700, drop the face
rep("details.more>summary::after{content:'+';margin-left:auto;font-size:20px;font-weight:600}", "details.more>summary::after{content:'+';margin-left:auto;font-size:20px;font-weight:700}")
rep("ul.furn li b{display:block;font-weight:600}", "ul.furn li b{display:block;font-weight:700}")
rep("font:600 12px var(--body)", "font:700 12px var(--body)", 2)
m = re.search(r"@font-face\{font-family:'Nunito Sans';font-style:normal;font-weight:600;[^}]*\}\n?", src)
assert m and 'base64' in m.group(0); src = src[:m.start()] + src[m.end():]

rep('<title>Forgelings (prototype 0.30.0)</title>', '<title>Forgelings (prototype 0.30.1)</title>')
rep("const VERSION='prototype 0.30.0';", "const VERSION='prototype 0.30.1';")
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', before, '->', len(src.encode()), 'saved', before - len(src.encode()))

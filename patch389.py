# Forgelings 0.38.9: fix 0.38.8. The "Sit with ..." companionship button was meant to sit beside the Hearth scene,
# but the edit landed in the sleeping Hearth, which has no `away` or `n`: opening the Hearth while your Forgelings
# were asleep threw a ReferenceError, and the awake Hearth had no button at all. The button now sits right under the
# scene in the awake Hearth; the sleeping Hearth is as before (affection is not offered while they sleep).
# Reads base388.html (0.38.8 with They Remember and the 0.38.7 reliability fixes).
src = open('base388.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)
rep("""    <button class="outline" id="hAffection" ${away?'disabled':''} aria-describedby="hmsg" style="width:100%;min-height:44px;margin-top:8px">Sit with ${esc(n)}<small> · Just for company</small></button>
    <p class="hmsg" id="hmsg" aria-live="polite" aria-atomic="true">${esc(msg)}</p>""",
    """    <p class="hmsg" id="hmsg">${esc(msg)}</p>""")
rep("""    <div class="hearthwrap"><canvas id="hearthCv" width="${HW}" height="${HH}" role="img" aria-label="Your Forgelings sitting around a campfire"></canvas></div>
    <p class="hmsg" id="hmsg">${esc(hf.msg||(!away&&memoryLine(c))||'The fire crackles. Everyone is settling in.')}</p>""",
    """    <div class="hearthwrap"><canvas id="hearthCv" width="${HW}" height="${HH}" role="img" aria-label="Your Forgelings sitting around a campfire"></canvas></div>
    <button class="outline" id="hAffection" ${away?'disabled':''} aria-describedby="hmsg" style="width:100%;min-height:44px;margin-top:8px">Sit with ${esc(n)}<small> · Just for company</small></button>
    <p class="hmsg" id="hmsg" aria-live="polite" aria-atomic="true">${esc(hf.msg||(!away&&memoryLine(c))||'The fire crackles. Everyone is settling in.')}</p>""")

# ---- room: styles for classes nothing uses any more (checked: none is built dynamically), and lossless icon recompression
import re as _re, base64 as _b64, io as _io
for sel in ['.deck','.filters','.moodbtn.gwait','.mini-back','.rowl.ownrow[aria-pressed="true"] .ri','.cbk .rule','.cbk .wm','.stat-line']:
    pat=_re.compile(r'(?<=[}\n])'+_re.escape(sel)+r'\{[^{}]*\}')
    n=len(pat.findall(src)); assert n==1,(sel,n); src=pat.sub('',src,count=1)
rep('.cbk.dense .emb,.cbk.dense .wm,.cbk.dense .rule{','.cbk.dense .emb{')
from PIL import Image as _Im
def _opt(m):
    raw=_b64.b64decode(m.group(1)); im=_Im.open(_io.BytesIO(raw)); b=_io.BytesIO(); im.save(b,'PNG',optimize=True); d=b.getvalue()
    assert list(_Im.open(_io.BytesIO(d)).convert('RGBA').getdata())==list(im.convert('RGBA').getdata())
    return 'data:image/png;base64,'+_b64.b64encode(d if len(d)<len(raw) else raw).decode()
src=_re.sub(r'data:image/png;base64,([A-Za-z0-9+/=]+)',_opt,src)
# ---- They Remember: keep snackKnown only when true, so a restored backup matches the cards that were exported
rep("    c.snackKnown=c.snackKnown===true;\n","    if(c.snackKnown===true)c.snackKnown=true;else delete c.snackKnown;\n")
rep('<title>Forgelings (prototype 0.38.8)</title>', '<title>Forgelings (prototype 0.38.9)</title>')
rep("const VERSION='prototype 0.38.8'", "const VERSION='prototype 0.38.9'")
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src.encode()))

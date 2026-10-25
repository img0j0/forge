# Forgelings 0.38.4: today's card gets a real face. Hunter: the daily card was "just a generic white card". It now comes
# from the same deck as its back: night indigo with a gold pixel frame, an art window glowing in the calling's colour
# with its own pixel emblem (twelve callings, plus a quill for your own small things), a ribbon banner with the
# calling's name and ability, the small thing on a parchment plate, and a card number. Today's card on the Today tab
# is the same card in a row. Reads base383.html.
src = open('base383.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

SIG = '["...######.../..#++#####../.#++#######./############/.##########./..########../...######.../....####..../.....##.....", ".........##./........####/........####/.........##./......###.../....####..../..####....../####......../#...##....../...####...../..######....", ".....##...../....#..#..../.....##...../..########../.....##...../.....##...../.....##...../#....##....#/##...##...##/.##..##..##./..########../....####....", ".......####./......#+##../.....#+##.../....####..../...########./.......###../......###.../.....###..../....###...../...##......./..#.........", ".###....###./#++##..#####/#+##########/############/############/.##########./..########../...######.../....####..../.....##.....", ".....##...../.....###..../.....#....../....###...../...#+###..../...#+####.../..#+######../..#+#######./.#+#########/############", ".....##...../.....##...../....#+##..../############/.##+#######./..########../...######.../..########../..###..###../.##......##.", "..######..../.##+#######./.##+########/.#######..../....##....../....##....../....##....../....##....../....##....../....##....../...####.....", ".....#....../...##......./..##......../.###......../.###......../####......../#####......./.####......./.######...../..########../...######.../.....##.....", "############/#++#########/#+##########/#+##########/############/.##########./.##########./..########../...######.../....####..../.....##.....", "............/..###..###../...######.../...######.../..###..###../####....####/####....####/..###..###../...######.../...######.../..###..###../............", "............/....####..../.###++#####./###++..#####/####....####/#####..#####/.##########./....####..../............", "..........##/........####/.......#+##./......#+##../.....####.../....####..../...####...../...###....../..##......../.#........../#..........."]'

# ---- emblems
rep("const PEN='<svg class=\"pi pen\"",
    "const SIGIL=" + SIG + ";\n"
    "const sigCache={};\n"
    "function sigDark(c){const n=parseInt(c.slice(1),16);return '#'+[16,8,0].map(s=>Math.round(((n>>s)&255)*.68).toString(16).padStart(2,'0')).join('');}\n"
    "/* a 12x12 pixel emblem: fill, a shaded lower-right edge, white glints, and a dark outline, all in one small SVG */\n"
    "function sigilSVG(i,c){const k=i+c;if(sigCache[k])return sigCache[k];const rows=SIGIL[i].split('/'),off=(12-rows.length)>>1,g=new Map(),P={ol:'',hi:'',fi:'',sh:''};\n"
    "  rows.forEach((r,y)=>[...r].forEach((ch,x)=>{if(ch!=='.')g.set((x+1)+','+(y+1+off),ch);}));\n"
    "  const at=(x,y,t)=>{P[t]+=`M${x} ${y}h1v1h-1z`;};\n"
    "  g.forEach((ch,key)=>{const [x,y]=key.split(',').map(Number);at(x,y,ch==='+'?'hi':(!g.has(x+','+(y+1))||!g.has((x+1)+','+y))?'sh':'fi');});\n"
    "  const ol=new Set();g.forEach((ch,key)=>{const [x,y]=key.split(',').map(Number);[[1,0],[-1,0],[0,1],[0,-1]].forEach(([dx,dy])=>{const q=(x+dx)+','+(y+dy);if(!g.has(q)&&!ol.has(q)){ol.add(q);at(x+dx,y+dy,'ol');}});});\n"
    "  return sigCache[k]=`<svg class=\"sigil\" viewBox=\"0 0 14 14\" shape-rendering=\"crispEdges\" aria-hidden=\"true\"><path fill=\"#1A1433\" d=\"${P.ol}\"/><path fill=\"${c}\" d=\"${P.fi}\"/><path fill=\"${sigDark(c)}\" d=\"${P.sh}\"/><path fill=\"#fff\" d=\"${P.hi}\"/></svg>`;}\n"
    "/* the look of today's card: its colour, emblem, ability line and number */\n"
    "function todayLook(){const o=todayOwnObj(),i=state.todayV,V=VECTORS[i];const n=todayBand().length,nc=n>12?'n3':n>7?'n2':'';return o?{c:'#FFD36B',sig:sigilSVG(12,'#FFD36B'),ab:'',nc,no:'Yours'}:{c:V.color,sig:sigilSVG(i,V.color),ab:V.ability,nc,no:'No. '+String(i+1).padStart(2,'0')};}\n"
    "const PEN='<svg class=\"pi pen\"")

# ---- the full card face
rep("""      <div class="vface vfront"><div class="vband" style="background:${V.color}"><b>${esc(todayBand())}</b></div><div class="vbody"><p>${todayOwnObj()?'Something you chose for yourself.':V.blurb}</p><p><strong>${todayOwnObj()?PEN+'Your small thing':'Today\\'s small thing'}</strong>${esc(todayTask())}</p><p><strong>The Forge asks</strong>${V.question}</p></div></div>""",
    """      <div class="vface vfront cc" style="--cc:${L.c}"><div class="ccart">${L.sig}</div><div class="vband"><b class="${L.nc}">${esc(todayBand())}</b>${L.ab?`<small>${L.ab}</small>`:''}</div><div class="vbody"><p class="ccblurb">${todayOwnObj()?'Something you chose for yourself.':V.blurb}</p><p class="ccplate"><strong>${todayOwnObj()?PEN+'Your small thing':'Today\\'s small thing'}</strong>${esc(todayTask())}</p><p class="ccask"><strong>The Forge asks</strong>${V.question}</p></div><span class="ccno" aria-hidden="true">${L.no}</span></div>""")
rep("function openVector(){\n  const V=VECTORS[state.todayV],",
    "function openVector(){\n  const L=todayLook(),V=VECTORS[state.todayV],")

# ---- today's card in the Today hero
rep("""hero=`<div class="taskface"><div class="band" style="background:${V.color}">${esc(todayBand())}</div><p>${todayOwnObj()?PEN:''}${esc(todayTask())}</p></div>""",
    """hero=`<div class="taskface" style="--cc:${todayLook().c}"><div class="tfart">${todayLook().sig}</div><div class="tfmain"><div class="band"><span>${esc(todayBand())}</span></div><p>${todayOwnObj()?PEN:''}${esc(todayTask())}</p></div></div>""")

# ---- styles: the old paper card rules are replaced
rep(""".taskface{width:100%;text-align:left;border:2px solid var(--ink);border-radius:14px;overflow:hidden;background:#FFFDF8;color:#2E2A47}
.taskface .band{padding:10px 14px;font:600 22px var(--display);border-bottom:2px solid #2E2A47}
.taskface p{padding:12px 14px 14px;font-size:17px;line-height:1.4}""", "")
rep(""".vface.vfront,.taskface{background:var(--paper) 0 0/32px 32px repeat,#FBF5E6 !important;color:#2E2A47}
.vface.vfront{border:3px solid #2E2A47 !important;border-radius:6px !important;box-shadow:0 0 0 3px #FBF5E6 inset,0 10px 0 rgba(46,42,71,.22)}""", "")
rep(""".vband,.taskface .band{position:relative;border-bottom:0 !important;background-image:linear-gradient(90deg,#2E2A47 50%,transparent 50%);background-size:6px 3px;background-repeat:repeat-x;background-position:0 100%;padding-bottom:16px !important}
.vbody strong,.taskface strong{font:600 15px var(--display);letter-spacing:.01em}
.taskface{border-width:3px !important;border-radius:6px !important}""", "")
CROSS = 'url("data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%2224%22 height=%2224%22 shape-rendering=%22crispEdges%22><path fill=%22%23ffffff%22 fill-opacity=%22.07%22 d=%22M11 9h2v2h2v2h-2v2h-2v-2H9v-2h2z%22/></svg>")'
rep(""".vface.vfront{transform:rotateY(180deg);background:#FFFDF8;color:#2E2A47;display:flex;flex-direction:column;border:2px solid #2E2A47}
.vband{flex:none;display:flex;align-items:center;gap:10px;padding:14px;border-bottom:2px solid #2E2A47}
.vband b{font:600 30px/1 var(--display)}
.vbody{padding:12px 14px;display:grid;gap:10px;font-size:clamp(13px,3.5vw,15px);line-height:1.4}
.vbody strong{display:block;font-weight:700}""",
"""/* 0.38.4: today's card, from the same deck as its back */
.vface.vfront{transform:rotateY(180deg);display:flex;flex-direction:column;color:#FFF7EC;border-radius:6px;padding:12px;background:""" + CROSS + """ 0 0/24px 24px,radial-gradient(120% 70% at 50% 0,color-mix(in srgb,var(--cc) 34%,#2B2152),#2B2152 70%);box-shadow:0 10px 0 rgba(46,42,71,.22)}
.cc::before,.taskface::before{content:'';position:absolute;inset:6px;border:3px dashed #F2C14E;pointer-events:none;z-index:2}
.ccart{flex:1 1 0;min-height:44px;display:grid;place-items:center;position:relative;margin:4px 4px 0;background:radial-gradient(closest-side,color-mix(in srgb,var(--cc) 55%,transparent),transparent)}
.ccart .sigil{height:min(100%,112px);width:auto;max-width:112px;image-rendering:pixelated;filter:drop-shadow(0 4px 0 rgba(10,6,28,.45))}
.vband{flex:none;position:relative;z-index:3;display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:2px 8px;margin:6px -4px 0;padding:6px 16px 4px;background:var(--cc);color:#2E2A47;clip-path:polygon(0 0,100% 0,calc(100% - 8px) 50%,100% 100%,0 100%,8px 50%);box-shadow:inset 0 -3px 0 rgba(46,42,71,.22)}
.vband b{font:400 34px/1 'VT323',monospace;letter-spacing:.02em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
.vband b.n2{font-size:30px}.vband b.n3{font-size:26px}
.vband small{font:700 16px/1 inherit;letter-spacing:.08em;font-variant-caps:all-small-caps;opacity:.85;flex:none}
.vbody{flex:none;padding:8px 8px 20px;display:grid;gap:8px;font-size:clamp(13px,3.5vw,14.5px);line-height:1.38;position:relative;z-index:3}
.vbody strong{display:block;font:600 17px/1.15 var(--display);letter-spacing:.05em;font-variant-caps:all-small-caps;margin-bottom:1px}
.ccblurb{color:#D2C9EE;font-style:italic;text-align:center;margin:0}
.ccplate{margin:0;background:#FBF5E6;color:#2E2A47;padding:8px 10px 9px;clip-path:polygon(0 3px,3px 3px,3px 0,calc(100% - 3px) 0,calc(100% - 3px) 3px,100% 3px,100% calc(100% - 3px),calc(100% - 3px) calc(100% - 3px),calc(100% - 3px) 100%,3px 100%,3px calc(100% - 3px),0 calc(100% - 3px));font-size:clamp(14px,3.8vw,15.5px)}
.ccplate strong{color:#5A4A9E}
.ccask{margin:0}.ccask strong{color:#FFD36B}
.ccno{position:absolute;right:16px;bottom:11px;z-index:3;font:400 15px/1 'VT323',monospace;color:#F2C14E;letter-spacing:.04em}
.taskface{position:relative;width:100%;display:flex;align-items:stretch;gap:12px;text-align:left;padding:16px 14px;border-radius:4px;color:#FFF7EC;background:""" + CROSS + """ 0 0/24px 24px,linear-gradient(90deg,color-mix(in srgb,var(--cc) 30%,#2B2152),#2B2152 55%);box-shadow:0 6px 0 rgba(10,6,28,.35)}
.tfart{flex:none;width:72px;display:grid;place-items:center;background:radial-gradient(closest-side,color-mix(in srgb,var(--cc) 60%,transparent),transparent)}
.tfart .sigil{width:60px;height:60px;image-rendering:pixelated;filter:drop-shadow(0 3px 0 rgba(10,6,28,.45))}
.tfmain{flex:1;min-width:0;display:flex;flex-direction:column;gap:8px;position:relative;z-index:3;padding:2px 4px 2px 0}
.taskface .band{align-self:flex-start;max-width:100%;padding:3px 14px 2px 10px;background:var(--cc);color:#2E2A47;font:400 26px/1 'VT323',monospace;letter-spacing:.02em;clip-path:polygon(0 0,100% 0,calc(100% - 7px) 50%,100% 100%,0 100%);box-shadow:inset 0 -3px 0 rgba(46,42,71,.22)}
.taskface .band span{display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
html .taskface p{margin:0;color:#FFF7EC;font-size:17px;line-height:1.4}
@media (prefers-reduced-motion:no-preference){.flipped .ccart .sigil,.taskface .sigil{animation:sigBob 3.2s steps(4) infinite}}
@media (max-width:380px){.flip{width:min(268px,82vw)}}
@keyframes sigBob{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}""")

rep('<title>Forgelings (prototype 0.38.3)</title>', '<title>Forgelings (prototype 0.38.4)</title>')
rep("const VERSION='prototype 0.38.3'", "const VERSION='prototype 0.38.4'")
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src.encode()))

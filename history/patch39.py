# Forgelings 0.39.0: Voxel Statues (design doc https://claude.ai/artifact/FbYyU4cfKKgLQwEJ8DBdTo, Hunter said go with
# every recommendation on October 26). A Forgebound Forgeling (bond 5) can be cast at the Forge as a 3D voxel statue
# for 6 embers: one per Forgeling, keeping the keepsake it wore, on a stand from its realm (10 looks). Seen from the
# Statues shelf at the Hearth and "See the statue" on the card's close-up; the card gets a small statue mark; Save
# picture makes a square image for the share sheet. The statue code is in statue_src.js (inlined: about 20 KB, it does
# no work until a statue is opened). Reads base3810.html.
src = open('base3810.html', encoding='utf8').read()
STATUE = open('statue_src.js', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

rep("function openWhatsNew(){", STATUE + "\nfunction openWhatsNew(){")
rep("function closeModal(){if(pgT){pgT.stop();pgT=null;}", "function closeModal(){if(pgT){pgT.stop();pgT=null;}if(stv){stv.stop();stv=null;}")
# the Forge sheet and the Hearth's Forge panel
rep('<ul class="furn forgel">${rows}</ul>', '<ul class="furn forgel">${rows}</ul>${statueForgeHTML()}')
rep('<button class="outline" id="hForge" style="margin-top:8px">Open the Forge</button></div>`;',
    '${statueShelfHTML()}<button class="outline" id="hForge" style="margin-top:8px">Open the Forge</button></div>`;')
# clicks
rep("""  const b=e.target.closest('button');if(!b)return;
  const cs=slotCards(),c=cs[hf.sel];""",
    """  const b=e.target.closest('button');if(!b)return;
  if(b.dataset.statue){openStatue(+b.dataset.statue);return;}
  const cs=slotCards(),c=cs[hf.sel];""")
rep("  if(b.hasAttribute('data-close')||b.id==='ovClose')closeModal();",
    "  if(b.hasAttribute('data-close')||b.id==='ovClose')closeModal();\n"
    "  else if(b.dataset.statue)openStatue(+b.dataset.statue);\n"
    "  else if(b.dataset.scast)statueCast(+b.dataset.scast);\n"
    "  else if(b.id==='stTurn'||b.id==='stBase'){if(stv){const k=b.id==='stTurn'?'turn':'base';stv.v[k]=!stv.v[k];stv.v.idle=9;b.setAttribute('aria-pressed',String(stv.v[k]));}}\n"
    "  else if(b.id==='stPic'){const c=cardById(stvId);if(c)statuePicture(c);}\n"
    "  else if(b.id==='stBack')openStatue(+b.dataset.cid);")
# remember which statue is open, for Save picture
rep("  const cv=$('#stCv');stv=statueView(cv,c,{rise:o.fresh});", "  const cv=$('#stCv');cv.dataset.cid=c.id;stvId=c.id;stv=statueView(cv,c,{rise:o.fresh});")
rep("let stv=null; /* the open viewer: {stop, shot} */", "let stv=null,stvId=null; /* the open viewer: {v, stop, frame} */")
# the card's close-up, the card mark, the bond-up sheet
rep('<button class="ghost" id="inspShare">Share</button>', '<button class="ghost" id="inspShare">Share</button>${c.statue?`<button class="ghost" data-statue="${c.id}">See the statue</button>`:\'\'}')
rep("""${ch?`<img class="chb" src="${fgURL(ch.id)}" alt="Wearing the ${esc(ch.name)}" title="${esc(ch.name)}">`:''}</div>""",
    """${ch?`<img class="chb" src="${fgURL(ch.id)}" alt="Wearing the ${esc(ch.name)}" title="${esc(ch.name)}">`:''}${c.statue?'<i class="stb" role="img" aria-label="Has a statue" title="Has a statue"></i>':''}</div>""")
rep("lv===5?`Forgebound. A golden glow now outlines ${esc(n)}, and it will keep it for good.`",
    "lv===5?`Forgebound. A golden glow now outlines ${esc(n)}, and it will keep it for good. The Forge could cast ${esc(n)} as a statue now, for ${STATUE_EMB} embers.`")
# saves: keep a statue only when it is well formed
rep("    if(c.snackKnown===true)c.snackKnown=true;else delete c.snackKnown;\n",
    "    if(c.snackKnown===true)c.snackKnown=true;else delete c.snackKnown;\n"
    "    if(c.statue!==undefined){if(!c.statue||typeof c.statue!=='object'||typeof c.statue.at!=='string'||!/^\\d{4}-\\d{2}-\\d{2}$/.test(c.statue.at))delete c.statue;else c.statue={at:c.statue.at,keep:typeof c.statue.keep==='string'?c.statue.keep.slice(0,24):''};}\n")
# What's new
rep("const SEEN_V=43;", "const SEEN_V=44;")
rep("""<ul class="newlist"><li><b>The Scribe.</b>""",
    """<ul class="newlist"><li><b>Voxel statues.</b> When a Forgeling becomes Forgebound, the Forge can cast it as a 3D statue for 6 embers, on a stand from its realm, wearing the keepsake it had on. Turn it with a finger, zoom in, and save a picture to share. Find statues on the Forge panel at the Hearth and on the card's close-up.</li>
    <li><b>The Scribe.</b>""")
# styles
STB = 'url("data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 8 10%22 shape-rendering=%22crispEdges%22><path fill=%22%231A1433%22 d=%22M2 0h4v1h1v4H6v1h2v4H0V6h2V5H1V1h1z%22/><path fill=%22%23C9C2E8%22 d=%22M3 1h2v1h1v2H5v1H3V4H2V2h1z%22/><path fill=%22%23FFD36B%22 d=%22M1 7h6v2H1z%22/></svg>")'
rep(".chb{position:absolute;right:.3em;bottom:.3em;",
    ".stb{position:absolute;left:.35em;bottom:.3em;width:1.7em;height:2.1em;background:" + STB + " center/contain no-repeat;image-rendering:pixelated;filter:drop-shadow(0 .1em 0 #0A0814)}\n"
    ".mini .stb{left:.45em;bottom:.45em;width:2.6em;height:3.25em}\n"
    ".stview{width:100%;display:grid;justify-items:center;gap:8px}\n"
    ".stsub{margin:-6px 0 0;font:700 14px/1.3 var(--body,inherit);color:var(--sg)}\n"
    ".stcan{position:relative;width:min(100%,560px);height:min(58vh,520px);background:radial-gradient(70% 60% at 50% 45%,color-mix(in srgb,var(--sg) 18%,transparent),transparent)}\n"
    ".stcan canvas{position:absolute;inset:0;width:100%;height:100%;touch-action:none;cursor:grab;outline:none}\n"
    ".stcan canvas:focus-visible{box-shadow:inset 0 0 0 3px #FFD36B}\n"
    ".stno{position:absolute;inset:0;display:grid;place-items:center;align-content:center;gap:12px;text-align:center;color:#D2C9EE;padding:16px}\n"
    ".stno img{width:160px;height:160px;image-rendering:pixelated}\n"
    ".stbtns{justify-content:center;gap:8px;flex-wrap:wrap}\n"
    ".stshelf{display:flex;gap:8px;overflow-x:auto;padding:2px 0 6px}\n"
    ".stshelf button{flex:none;display:grid;justify-items:center;gap:2px;min-width:64px;min-height:44px;padding:6px 6px 4px;border:0;background:var(--chip);color:var(--ink);font:600 12px inherit;cursor:pointer}\n"
    ".stshelf img{width:40px;height:40px;image-rendering:pixelated}\n"
    ".fgh{font:600 16px var(--display);margin:14px 0 4px}\n"
    ".chb{position:absolute;right:.3em;bottom:.3em;")
# What's new keeps the latest eight notes: the oldest (The map, inked) rolls off
_i=src.index('function openWhatsNew(){'); _j=src.index('</ul>',_i); _k=src.rindex('<li><b>The map, inked.</b>',_i,_j)
_e=src.rindex('\n',_i,_k); src=src[:_e]+src[_j:]
rep('<title>Forgelings (prototype 0.38.10)</title>', '<title>Forgelings (prototype 0.39.0)</title>')
rep("const VERSION='prototype 0.38.10'", "const VERSION='prototype 0.39.0'")
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src.encode()))

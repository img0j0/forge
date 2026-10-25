# Forgelings 0.38.5: the daily set. The week is seven little pixel tiles (the Journal's flame for days you showed
# up, its moon for rests) in a "This week" panel that also holds Latest finds, now standing on a wooden shelf.
# How did it feel? is three pixel faces. Toasts are pixel banners, and a new ribbon gets a gold one with a medal.
# The age check's month and year, and every text field, get stepped pixel corners and a pixel arrow.
# Reads base384.html.
src = open('base384.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

# ---- pixel drawing: 'o' is a dark ink pixel, so faces can have eyes and mouths
rep("function sigilSVG(i,c){const k=i+c;if(sigCache[k])return sigCache[k];const rows=SIGIL[i].split('/'),",
    "function sigilSVG(i,c){return pixSVG(SIGIL[i],c,'sigil');}\n"
    "function pixSVG(src,c,cls){const k=src+c;if(sigCache[k])return sigCache[k];const rows=src.split('/'),")
rep("g.forEach((ch,key)=>{const [x,y]=key.split(',').map(Number);at(x,y,ch==='+'?'hi':",
    "g.forEach((ch,key)=>{const [x,y]=key.split(',').map(Number);at(x,y,ch==='o'?'ol':ch==='+'?'hi':")
rep('return sigCache[k]=`<svg class="sigil" viewBox=',
    'return sigCache[k]=`<svg class="${cls}" viewBox=')
rep("const FEELS=['easy','good','hard'];",
    "const FEELS=['easy','good','hard'];\n"
    "/* 0.38.5: three pixel faces for How did it feel? */\n"
    "const FACE={easy:['#B5DDB5','....####..../..########../.##########./.#+########./##+#o####o##/#+#o#o##o#o#/############/###o####o###/.###oooo###./.##########./..########../....####....'],"
    "good:['#FFD36B','....####..../..########../.##########./.#+########./##+#o####o##/#+##o####o##/############/##o######o##/.##oooooo##./.###oooo###./..########../....####....'],"
    "hard:['#F5A5AA','....####..+./..#######.++/.##########./.#+oo##oo##./##+#########/#+##o####o##/############/############/.##oooooo##./.##########./..########../....####....']};")

# ---- the week tiles
rep("""    out+=`<span class="${cls}" role="img" aria-label="${dateLabel(k)}: ${label}"></span>`;""",
    """    out+=`<span class="${cls}" role="img" aria-label="${dateLabel(k)}: ${label}" data-d="${'SMTWTFS'[d.getDay()]}"></span>`;""")
rep("""    <div class="row" style="margin:0 2px 14px"><div class="dots" aria-label="This week">${weekDots()}</div><span class="muted small">${done} ${done===1?'day':'days'} showed up</span></div>
    ${latest.length?`<h2 class="sub3">Latest finds</h2><div class="latest">${latest.map(c=>`<button data-insp="${c.id}" aria-label="Look at ${esc(c.name)}">${cardHTML(c,{w:92,mini:true})}</button>`).join('')}</div>`:''}`;""",
    """    <div class="panel-box weekbox"><div class="weekhead"><h2 class="sub3">This week</h2><span class="muted small">${done} ${done===1?'day':'days'} showed up</span></div><div class="dots" role="group" aria-label="This week">${weekDots()}</div>
    ${latest.length?`<h2 class="sub3">Latest finds</h2><div class="latest shelf">${latest.map(c=>`<button data-insp="${c.id}" aria-label="Look at ${esc(c.name)}">${cardHTML(c,{w:92,mini:true})}</button>`).join('')}</div>`:''}</div>`;""")

# ---- feeling faces
rep("""${FEELS.map(f=>`<button class="chip" data-feel="${f}" aria-pressed="${fl===f}">${f[0].toUpperCase()+f.slice(1)}</button>`).join('')}""",
    """${FEELS.map(f=>`<button class="facebtn" data-feel="${f}" aria-pressed="${fl===f}">${pixSVG(FACE[f][1],FACE[f][0],'feelface')}<span>${f[0].toUpperCase()+f.slice(1)}</span></button>`).join('')}""")

# ---- toasts: a ribbon toast wears gold
rep("let toastT;function toast(m){const t=$('#toast');t.textContent=m;t.classList.add('show');",
    "let toastT;function toast(m){const t=$('#toast');t.textContent=m;t.classList.toggle('medal',/^New ribbon/.test(m));t.classList.add('show');")

# ---- styles
STEP2 = "polygon(0 2px,2px 2px,2px 0,calc(100% - 2px) 0,calc(100% - 2px) 2px,100% 2px,100% calc(100% - 2px),calc(100% - 2px) calc(100% - 2px),calc(100% - 2px) 100%,2px 100%,2px calc(100% - 2px),0 calc(100% - 2px))"
ARROW = 'url("data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 7 4%22 shape-rendering=%22crispEdges%22><path fill=%22%23FFD36B%22 d=%22M0 0h7v1H6v1H5v1H4v1H3V3H2V2H1V1H0z%22/></svg>")'
MEDAL = 'url("data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 10 12%22 shape-rendering=%22crispEdges%22><path fill=%22%23C0392B%22 d=%22M2 0h2v4H2zM6 0h2v4H6z%22/><path fill=%22%231A1433%22 d=%22M3 4h4v1h1v1h1v4H8v1H7v1H3v-1H2v-1H1V6h1V5h1z%22/><path fill=%22%23FFD36B%22 d=%22M3 5h4v1h1v4H7v1H3v-1H2V6h1z%22/><path fill=%22%23fff%22 d=%22M3 6h1v2H3z%22/></svg>")'
rep(".dots{display:flex;gap:9px;align-items:center}\n.dot{width:14px;height:14px;border-radius:50%;border:2px solid var(--plum)}\n.dot.done{background:var(--plum)} .dot.rest{border-style:dashed;opacity:.55} .dot.skipped{opacity:.25} .dot.now{box-shadow:0 0 0 3px var(--butter)}",
    ".dots{display:flex;gap:9px;align-items:center}\n"
    "/* 0.38.5: the week as pixel tiles */\n"
    ".weekbox .dots{justify-content:space-between;gap:4px;margin:4px 0 28px}\n"
    ".weekhead{display:flex;align-items:baseline;justify-content:space-between;gap:10px}.weekhead h2.sub3{margin:0 0 8px}\n"
    ".dot{position:relative;flex:none;width:34px;height:34px;background:transparent;box-shadow:inset 0 0 0 2px var(--line)}\n"
    ".dot::after{content:attr(data-d);position:absolute;left:0;right:0;top:calc(100% + 3px);text-align:center;font:400 15px/1 'VT323',monospace;color:var(--muted)}\n"
    ".dot.done{background:var(--stF) 50% 55%/66% auto no-repeat,var(--stamp);box-shadow:inset 0 0 0 2px var(--stampEdge),0 3px 0 rgba(10,6,28,.35)}\n"
    ".dot.rest{background:var(--stM) 50% 52%/58% auto no-repeat,transparent;box-shadow:inset 0 0 0 2px var(--line)}\n"
    ".dot.skipped{opacity:.45}\n"
    ".dot.now{outline:3px solid var(--butter);outline-offset:2px}.dot.now::after{color:var(--butter)}\n"
    ".shelf{position:relative;padding:4px 6px 22px;gap:12px;background:linear-gradient(#C68A4E,#C68A4E) 0 calc(100% - 10px)/100% 3px no-repeat,linear-gradient(#8A5A32,#8A5A32) 0 calc(100% - 4px)/100% 7px no-repeat,linear-gradient(rgba(10,6,28,.35),rgba(10,6,28,.35)) 0 100%/100% 4px no-repeat}\n"
    ".shelf button{flex:none}\n"
    ".feel .chips{gap:10px;justify-content:center}\n"
    ".facebtn{display:flex;flex-direction:column;align-items:center;gap:4px;min-width:64px;min-height:44px;padding:8px 8px 6px;border:0;background:var(--chip);color:var(--ink);font:600 14px inherit;cursor:pointer;clip-path:" + STEP2 + "}\n"
    ".facebtn .feelface{width:36px;height:36px;image-rendering:pixelated;filter:saturate(.8);transition:transform .15s,filter .15s}\n"
    ".facebtn[aria-pressed=true]{background:rgba(255,211,107,.18);box-shadow:inset 0 0 0 2px #FFD36B;color:var(--ink)}\n"
    ".facebtn[aria-pressed=true] .feelface{filter:none;transform:translateY(-2px)}\n"
    ".facebtn:focus-visible{outline:none;box-shadow:inset 0 0 0 3px #FFD36B}\n"
    "@media (hover:hover){.facebtn:hover .feelface{filter:none}}\n"
    "@media (prefers-reduced-motion:reduce){.facebtn .feelface{transition:none}.facebtn[aria-pressed=true] .feelface{transform:none}}")
rep("html.ls .toast{border-radius:0;clip-path:var(--step);bottom:calc(92px + env(safe-area-inset-bottom,0px))}",
    "html.ls .toast{border-radius:0;clip-path:var(--step);bottom:calc(92px + env(safe-area-inset-bottom,0px))}\n"
    "/* 0.38.5: toasts are pixel banners; a new ribbon gets gold and a medal */\n"
    ".toast{border-radius:0;clip-path:" + STEP2 + ";background:#1E1740;color:#FFF7EC;box-shadow:inset 0 0 0 2px #F2C14E,inset 0 -4px 0 rgba(0,0,0,.25);padding:12px 18px 13px}\n"
    ".toast.medal{background:#FFD36B;color:#2E2A47;box-shadow:inset 0 0 0 2px #8A5A32,inset 0 -4px 0 rgba(138,90,50,.35);padding-left:46px;text-align:left}\n"
    ".toast.medal::before{content:'';position:absolute;left:14px;top:50%;width:20px;height:24px;margin-top:-12px;background:" + MEDAL + " center/contain no-repeat;image-rendering:pixelated}\n"
    "@media (prefers-reduced-motion:no-preference){.toast.medal.show::before{animation:medalDrop .6s steps(3) 1}}\n"
    "@keyframes medalDrop{0%{transform:translateY(-6px)}100%{transform:none}}")

# ---- fields and the age check: stepped corners, pixel arrow, an inset focus ring
rep(".field select{width:100%;border:1.5px solid var(--line);background:var(--surface);color:var(--ink);border-radius:12px;padding:11px 12px;font:inherit}",
    ".field select{width:100%;border:1.5px solid var(--line);background:var(--surface);color:var(--ink);border-radius:12px;padding:11px 12px;font:inherit}\n"
    "/* 0.38.5: fields share the pixel corners */\n"
    ".field :is(input,textarea,select){border-radius:0 !important;border-width:2px !important;clip-path:" + STEP2 + "}\n"
    ".field :is(input,textarea,select):focus{outline:none !important;box-shadow:inset 0 0 0 3px #FFD36B !important}\n"
    ".field select{appearance:none;-webkit-appearance:none;padding-right:40px !important;background-image:" + ARROW + " !important;background-repeat:no-repeat !important;background-position:right 14px center !important;background-size:14px 8px !important;cursor:pointer}\n"
    ".field select option{color:#2E2A47;background:#FBF5E6}")

rep(".title-card{width:100%;max-width:400px;background:rgba(22,18,46,.9);border:1px solid rgba(255,255,255,.14);border-radius:22px;",
    ".title-card{width:100%;max-width:400px;background:linear-gradient(#FFD36B,#FFD36B) left 8px top 8px/4px 4px no-repeat,linear-gradient(#FFD36B,#FFD36B) right 8px top 8px/4px 4px no-repeat,linear-gradient(#FFD36B,#FFD36B) left 8px bottom 8px/4px 4px no-repeat,linear-gradient(#FFD36B,#FFD36B) right 8px bottom 8px/4px 4px no-repeat,rgba(20,15,48,.94);border:0;border-radius:0;clip-path:var(--step);")
rep('<title>Forgelings (prototype 0.38.4)</title>', '<title>Forgelings (prototype 0.38.5)</title>')
rep("const VERSION='prototype 0.38.4'", "const VERSION='prototype 0.38.5'")
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src.encode()))

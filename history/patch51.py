# 0.51.0: UI upgrade after comparing with the App Store's leading apps (Hunter, November 9).
#   1. Your Forgeling on Today: a small taped photo of your companion at the top of Today (it replaces the Hearth row there),
#      saying where they are: by the fire, asleep, out wandering, back. Tapping it opens the Hearth.
#   2. Binder scrolls: no more Previous/Next pages. Cards load 24 at a time as you scroll (with a "Show more" button too);
#      empty slots only finish the last row, quietly. Filter and Sort are round pills with icons.
#   3. Map / Tales / Journal is one joined switch with a highlight that slides (still with reduced motion).
#   4. Toasts drop in from the top, on one line where they fit, instead of covering rows above the tab bar.
import re,subprocess,os
S=open('base502.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.50.2'","const VERSION='prototype 0.51.0'")
rep("<title>Forgelings (prototype 0.50.2)</title>","<title>Forgelings (prototype 0.51.0)</title>")

# ---- 1. companion photo on Today
rep("""    if(waits)rows.push(row('btnHearth',IC.hearth,'The Hearth',(state.hearth.sleep?'The fire has burned low and your Forgelings are asleep.':(nf.length?'Something new is waiting by the fire. ':'')+(state.request&&reqAsker()?`${esc(reqAsker().nick||reqAsker().name)} has a small request. `:'')+(hv>0?`${hv} ${hv===1?'visit':'visits'} left today.`:'Your companions are here for company.'))+(wl?' '+wl:''),'',nf.length>0));}""",
"""    const hsub=(state.hearth.sleep?'The fire has burned low and your Forgelings are asleep.':(nf.length?'Something new is waiting by the fire. ':'')+(state.request&&reqAsker()?`${esc(reqAsker().nick||reqAsker().name)} has a small request. `:'')+(hv>0?`${hv} ${hv===1?'visit':'visits'} left today.`:'Your companions are here for company.'));
    if(s!=='done'){const mc=mateNow();if(mc){const mn=esc(mc.nick||mc.name),wo=state.wander&&state.wander.id===mc.id,mt=wo&&wReady()?`${mn} is back from wandering`:wo&&wOut()?`${mn} is out wandering`:state.hearth.sleep?`${mn} is asleep by the fire`:`${mn} is by the fire`;
      const ms=wo&&wOut()?`Back in ${wLeftText()}. `+(nf.length?'Something new is waiting by the fire.':''):wo&&wReady()?'Come see what they found. '+hsub:hsub+(waits&&wl&&!wo?' '+wl:'');CMAP[ckey(mc)]=mc;
      mate=`<button class="rowl matestrip${nf.length||(wo&&wReady())?' ready':''}" id="${waits?'btnHearth':'btnMate'}"><span class="mport" aria-hidden="true"><canvas class="pcv" width="48" height="37" data-k="${ckey(mc)}"></canvas></span><span class="rt"><b>${mt}</b><span class="rs">${ms}</span></span><span class="chev" aria-hidden="true">›</span></button>`;}}
    else if(waits)rows.push(row('btnHearth',IC.hearth,'The Hearth',hsub+(wl?' '+wl:''),'',nf.length>0));}""")
rep("""  let hero='';
  if(s==='fresh')hero=""","""  let hero='',mate='';
  if(s==='fresh')hero=""")
rep("""  el.innerHTML=`<div class="herowrap"><div class="hero pixcut">${hero}</div></div>${reflect}""","""  el.innerHTML=`${mate}<div class="herowrap"><div class="hero pixcut">${hero}</div></div>${reflect}""")
rep("""const homeFav=()=>{""","""function mateNow(){if(!state.cards.length)return null;const w=state.wander;if(w&&(wOut()||wReady())&&cardById(w.id))return cardById(w.id);const cs=slotCards();return cs.length?cs[Math.min(hf.sel||0,cs.length-1)]:null;}
const homeFav=()=>{""")
rep("""  else if(b.id==='btnHearth'){tab='hearth';""","""  else if(b.id==='btnHearth'||b.id==='btnMate'){tab='hearth';""")

# ---- 2. binder scrolls
rep("""  const pages=Math.max(1,Math.ceil(list.length/9));bf.page=Math.min(bf.page,pages-1);
  const jrb=document.documentElement.classList.contains('jr'),slice=list.slice(bf.page*9,bf.page*9+9),w=Math.floor((vw()-32-24-20-(jrb?36:0))/3),slots=[];
  for(let i=0;i<(filtN()?slice.length:9);i++){""","""  if(bIO){bIO.disconnect();bIO=null;}
  const pages=Math.max(1,Math.ceil(list.length/24));bf.page=Math.min(bf.page,pages-1);
  const jrb=document.documentElement.classList.contains('jr'),slice=list.slice(0,bf.page*24+24),w=Math.floor((vw()-32-24-20-(jrb?36:0))/3),slots=[],more=list.length-slice.length;
  const nSlots=filtN()||more?slice.length:Math.max(3,Math.ceil(slice.length/3)*3);
  for(let i=0;i<nSlots;i++){""")
rep("""`<div class="empty" style="width:${w}px;height:${Math.round(w*1.4)}px" aria-hidden="true">?</div>`""","""`<div class="empty quiet" style="width:${w}px;height:${Math.round(w*1.4)}px" aria-hidden="true">?</div>`""")
rep("""    <div class="row" style="margin:4px 0 10px"><button class="pill" id="btnFilter" aria-haspopup="dialog">Filter${filtN()?' \\u00B7 '+filtN():''}</button><button class="pill" id="btnSort">Sort: ${bf.sort==='new'?'Newest':'Rarest'}</button></div>""",
"""    <div class="row bbar" style="margin:4px 0 10px"><button class="pill" id="btnFilter" aria-haspopup="dialog"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 5h16l-6 7.5V19l-4-2v-4.5z"/></svg>Filter${filtN()?' \\u00B7 '+filtN():''}</button><button class="pill" id="btnSort"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 4v16M4.5 16.5 8 20l3.5-3.5M16 20V4M12.5 7.5 16 4l3.5 3.5"/></svg>Sort: ${bf.sort==='new'?'Newest':'Rarest'}</button></div>""")
rep("""    <div class="pager"><button class="pill" id="pgPrev" ${bf.page===0?'disabled style="opacity:.45"':''}>Previous</button><span class="muted small">Page ${bf.page+1} of ${pages}</span><button class="pill" id="pgNext" ${bf.page>=pages-1?'disabled style="opacity:.45"':''}>Next</button></div>`;
  hydrate(el);""","""    ${more?`<div class="bmore"><button class="pill" id="pgNext">Show more <span class="muted">(${more} more)</span></button></div>`:''}`;
  hydrate(el);
  const nx=$('#pgNext');if(nx&&'IntersectionObserver' in window){bIO=new IntersectionObserver(es=>{if(tab==='binder'&&es.some(e=>e.isIntersecting)){bIO.disconnect();bIO=null;bf.page++;renderBinder();}},{rootMargin:'0px 0px 320px 0px'});bIO.observe(nx);}""")
rep("""function renderBinder(){""","""let bIO=null;
function renderBinder(){""")

# ---- 3. joined Map / Tales / Journal switch
rep("""  el.innerHTML=`<div class="chips" role="group" aria-label="Map sections">${subs.map(""","""  const si=subs.findIndex(x=>x[0]===ch.sub),sp=ch.pi==null?si:ch.pi;ch.pi=si;
  el.innerHTML=`<div class="chips seg" role="group" aria-label="Map sections" style="--i:${si};--p:${sp}">${subs.map(""")

CSS="""
/* 0.51: your Forgeling on Today, a taped photo */
.app .rowl.matestrip{border-top:0;gap:14px;padding:4px 2px 14px;margin:-2px 0 6px;min-height:76px}
.matestrip .mport{flex:none;display:block;width:78px;height:61px;padding:4px 4px 7px;background:#FBF6EA;box-shadow:0 2px 0 rgba(0,0,0,.12),0 4px 10px rgba(0,0,0,.14);transform:rotate(-3deg);position:relative}
.matestrip .mport::after{content:'';position:absolute;left:24px;top:-7px;width:30px;height:12px;background:rgba(240,207,120,.75);transform:rotate(4deg)}
.matestrip .mport canvas{width:100%;height:100%}
html.jr .app .matestrip .rt b{font-size:calc(var(--hs,1)*21px)}
html.jr[data-page="lamp"] .matestrip .mport{background:#E9DFC8;filter:brightness(.88)}
/* 0.51: binder toolbar pills and quiet empty slots */
html .app .bbar .pill{display:inline-flex;align-items:center;gap:7px;border-radius:999px !important;clip-path:none !important;background:transparent !important;border:0 !important;box-shadow:inset 0 0 0 1.5px var(--ink) !important;color:var(--ink);padding:0 16px}
html.jr .app .binder .empty.quiet{opacity:.5;border-width:1.5px}
html.jr .app .binder .empty.quiet::after{content:none}
.bmore{display:flex;justify-content:center;margin:14px 0 4px}
/* 0.51: Map / Tales / Journal as one joined switch */
.app .chips.seg{display:grid;grid-template-columns:repeat(3,1fr);gap:0;position:relative;padding:3px;border-radius:13px;background:color-mix(in srgb,var(--ink) 7%,transparent);box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--ink) 16%,transparent);margin:4px 0 14px}
.app .chips.seg::before{content:'';position:absolute;top:3px;bottom:3px;left:3px;width:calc((100% - 6px)/3);border-radius:10px;background:#FFD36B;box-shadow:0 1px 0 #C98A12,0 2px 6px rgba(0,0,0,.12);transform:translateX(calc(var(--i)*100%));animation:segsl .24s cubic-bezier(.3,.7,.4,1)}
@keyframes segsl{from{transform:translateX(calc(var(--p)*100%))}}
html .app .chips.seg .chip{position:relative;z-index:1;margin:0;background:transparent !important;border:0 !important;box-shadow:none !important;clip-path:none !important;border-radius:10px !important;color:var(--ink) !important;font-weight:700}
html .app .chips.seg .chip[aria-pressed="true"]{color:#2E2A47 !important;background:#FFD36B !important;animation:segfill .01s linear .24s backwards}
@keyframes segfill{from{background:transparent}}
@media (prefers-reduced-motion:reduce){.app .chips.seg::before,html .app .chips.seg .chip{animation:none !important}}
html.reduce .app .chips.seg::before,html.reduce .app .chips.seg .chip{animation:none !important}
/* 0.51: toasts drop in from the top instead of covering rows above the tab bar */
.toast{top:calc(10px + env(safe-area-inset-top,0px));bottom:auto;transform:translate(-50%,-16px);width:max-content;max-width:min(94vw,440px)}
html.ls .toast,html.jr .toast{top:calc(10px + env(safe-area-inset-top,0px));bottom:auto}
"""
i=S.index("</style>",S.index("</style>")+1); S=S[:i]+CSS+S[i:]
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk51.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk51.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)

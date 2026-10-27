# Forgelings 0.40.2: the audit fixes. Nothing new to play; the app gets kinder to batteries and testers.
# 1. An installed copy notices a new release when it comes back to the front and offers "Load it" (a small bar).
# 2. The two always-on animation loops sleep when there is nothing to draw (another tab, hidden page, reduced motion),
#    and the card loop draws only canvases that are on screen. A wake-up on tab change, return and settings.
# 3. A restored backup keeps this device's age answer, and long nicknames and tales are trimmed on load.
# 4. Dead code removed (old realms list, callings list, two unused names).
# Reads base401.html.
src = open('base401.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

rep("const VERSION='prototype 0.40.1'", "const VERSION='prototype 0.40.2'")

# ---- 2. loops that sleep ----
rep("""function loop(ts){
  if(!REDUCE&&!document.hidden&&ts-last>72){
    last=ts;REG=REG.filter(cv=>cv.isConnected);
    REG.forEach(cv=>{const st=cv._st||(cv._st=cv.closest('.stage')||{});drawFrame(cv._e,cv,ts,st._ph==null?null:st._ph);});
  }
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);""",
"""/* 0.40.2: the loops sleep (a slow check, not 60 wake-ups a second) when nothing on screen moves; wakeLoops() rouses them at once. */
var cardSleep=0,hearthSleep=0;
function loop(ts){
  if(REDUCE||document.hidden){cardSleep=setTimeout(()=>{cardSleep=0;requestAnimationFrame(loop);},600);return;}
  if(ts-last>72){
    last=ts;REG=REG.filter(cv=>cv.isConnected);const vis=REG.filter(cv=>cv.getClientRects().length);
    if(!vis.length){cardSleep=setTimeout(()=>{cardSleep=0;requestAnimationFrame(loop);},600);return;}
    vis.forEach(cv=>{const st=cv._st||(cv._st=cv.closest('.stage')||{});drawFrame(cv._e,cv,ts,st._ph==null?null:st._ph);});
  }
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
function wakeLoops(){
  if(cardSleep){clearTimeout(cardSleep);cardSleep=0;requestAnimationFrame(loop);}
  if(hearthSleep&&typeof hearthLoop==='function'){clearTimeout(hearthSleep);hearthSleep=0;requestAnimationFrame(hearthLoop);}
}
document.addEventListener('visibilitychange',()=>{if(!document.hidden)wakeLoops();});""")
rep("function hearthLoop(ts){if(!REDUCE&&!document.hidden&&tab==='hearth'&&ts-hLast>80){hLast=ts;drawHearth(ts);}requestAnimationFrame(hearthLoop);}",
    "function hearthLoop(ts){if(REDUCE||document.hidden||tab!=='hearth'){hearthSleep=setTimeout(()=>{hearthSleep=0;requestAnimationFrame(hearthLoop);},600);return;}if(ts-hLast>80){hLast=ts;drawHearth(ts);}requestAnimationFrame(hearthLoop);}")
rep("function hydrate(root){\n  (root||document).querySelectorAll('canvas.pcv').forEach(cv=>{\n    if(cv._e)return;const c=CMAP[cv.dataset.k];if(!c)return;\n    cv._e=prep(c);REG.push(cv);drawFrame(cv._e,cv,performance.now(),null);\n  });\n}",
    "function hydrate(root){\n  (root||document).querySelectorAll('canvas.pcv').forEach(cv=>{\n    if(cv._e)return;const c=CMAP[cv.dataset.k];if(!c)return;\n    cv._e=prep(c);REG.push(cv);drawFrame(cv._e,cv,performance.now(),null);\n  });\n  wakeLoops();\n}")
rep("function renderNav(){\n", "function renderNav(){\n  wakeLoops();\n")
rep("document.documentElement.classList.toggle('reduce',REDUCE);", "document.documentElement.classList.toggle('reduce',REDUCE);wakeLoops();")

# ---- 1. a new version is ready ----
rep("""  if('serviceWorker' in navigator&&/^https?:$/.test(location.protocol))window.addEventListener('load',()=>{navigator.serviceWorker.register('sw.js').catch(()=>{});});""",
"""  if('serviceWorker' in navigator&&/^https?:$/.test(location.protocol)){
    window.addEventListener('load',()=>{navigator.serviceWorker.register('sw.js').catch(()=>{});});
    /* 0.40.2: an installed copy often resumes instead of reloading, so look for a new release on each return and offer it. */
    const hadSW=!!navigator.serviceWorker.controller;let updLast=0;
    navigator.serviceWorker.addEventListener('controllerchange',()=>{if(hadSW)updBar();});
    document.addEventListener('visibilitychange',()=>{if(document.hidden||Date.now()-updLast<30*60*1000)return;updLast=Date.now();
      navigator.serviceWorker.getRegistration().then(r=>{if(r)return r.update();}).catch(()=>{});});
  }""")
rep("function installTipHTML(){",
"""function updBar(){
  if(document.getElementById('updBar')||!document.body)return;
  const b=document.createElement('div');b.id='updBar';b.className='updbar';b.setAttribute('role','status');
  b.innerHTML='<span>A new version of Forgelings is ready.</span><button type="button" id="updGo">Load it</button><button type="button" class="later" id="updLater">Later</button>';
  document.body.appendChild(b);
  b.querySelector('#updGo').onclick=()=>{try{save();}catch(e){}location.reload();};
  b.querySelector('#updLater').onclick=()=>b.remove();
}
function installTipHTML(){""")
rep(".toast.show{opacity:1;transform:translate(-50%,0)}",
    ".toast.show{opacity:1;transform:translate(-50%,0)}\n"
    ".updbar{position:fixed;left:50%;bottom:calc(84px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);background:var(--ink);color:var(--bg);padding:6px 6px 6px 16px;border-radius:24px;font-weight:700;font-size:14px;z-index:69;display:flex;gap:6px;align-items:center;width:max-content;max-width:92vw;box-shadow:0 6px 18px rgba(0,0,0,.28)}\n"
    ".updbar span{flex:1;line-height:1.3}\n"
    ".updbar button{min-height:44px;min-width:44px;border-radius:22px;padding:0 14px;border:0;font:inherit;font-weight:800;background:var(--bg);color:var(--ink);cursor:pointer}\n"
    ".updbar button.later{background:transparent;color:var(--bg);text-decoration:underline;text-underline-offset:3px}")

# ---- 3. restore and repair ----
rep("c.name=str(c.name,'Mystery Forgeling');c.nick=str(c.nick,'');c.note=str(c.note,'');c.tale=str(c.tale,c.note);",
    "c.name=str(c.name,'Mystery Forgeling').slice(0,40);c.nick=str(c.nick,'').slice(0,24);c.note=str(c.note,'').slice(0,200);c.tale=str(c.tale,c.note).slice(0,200);")
rep("s.ageBand=s.ageBand||state.ageBand;state=migrate(s);", "s.ageBand=state.ageBand||s.ageBand;state=migrate(s);")

# ---- 4. dead code ----
i = src.index('function realmsHTML(){'); j = src.index('\n}\n', i) + 3
assert src.count('realmsHTML') == 1; src = src[:i] + src[j:]
rep("const callingsHTML=()=>VECTORS.map((V,i)=>callingNoteHTML(i)).join('');\n", "")
rep("const n=c.nick||c.name,art=$('#stage .art'),h=$('#inspHint');", "const n=c.nick||c.name,h=$('#inspHint');")
rep("function renderToday(){\n  const V=VECTORS[state.todayV],s=state.status,", "function renderToday(){\n  const s=state.status,")

open('work.html', 'w', encoding='utf8').write(src)
print('ok', len(src))

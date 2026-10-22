# Forgelings 0.34.0: two things Hunter asked for after a week of daily use.
# 1. A favourite on Today: pick any Forgeling from its card ("Show on Today"). Today's new find still shows first;
#    once you've seen it (left Today or closed the app), your favourite takes the spot, with a link back to the find.
#    Rest days show your favourite too. With no favourite picked, nothing changes.
# 2. Campfire card backs: every Forgeling's back now wears the same campfire art as Today's card, with its details
#    below the fire, so the whole collection reads as one set. (The old diamond emblem and "FORGE" wordmark go.)
# Reads base33.html.
src = open('base33.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

# ---- 2. campfire card backs ----
rep('''    <div class="face cbk${(c.tale||c.gossip)?' dense':''}"><svg class="emb" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l7 6-7 12L5 9z"/><path d="M5 9h14M9 9l3 12M15 9l-3 12"/></svg>
      <div class="wm">FORGE</div><div class="rule"></div>
      <div class="m1">''', '''    <div class="face cbk${(c.tale||c.gossip)?' dense':''}"><div class="bsp" aria-hidden="true"></div><div class="binfo">
      <div class="m1">''')
rep('''<div class="m4">${EDITION}, No. ${pad(c.serial)}</div></div>''', '''<div class="m4">${EDITION}, No. ${pad(c.serial)}</div></div></div>''')
rep('/* Nav */', '''.card .face.cbk{background:var(--cbT) 0 0/100% 100% no-repeat,#4D3E8C;justify-content:flex-start;padding:0;gap:0;border:.14em solid #2E2A47}
.card .cbk .bsp{flex:0 0 46%}
.card .cbk .binfo{flex:1 1 auto;width:76%;min-height:0;margin:0 0 12%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.28em;overflow-y:auto;text-shadow:0 .1em 0 #241B4C}
.card .cbk .binfo .m1{font-size:1.4em}.card .cbk .binfo .m2{font-size:1.15em}.card .cbk .binfo .m3{font-size:1.15em;max-width:none}.card .cbk .binfo .m4{font-size:.95em;margin-top:.2em}.card .cbk .binfo .m5,.card .cbk .binfo .m6{font-size:1em;max-width:none}
.card .cbk.dense .binfo{justify-content:safe center;padding:0}
.hero:has(#btnShowFav){background:var(--ped) center 192px/176px 22px no-repeat,radial-gradient(circle at 50% 104px,var(--glow) 0,transparent 128px),var(--dot) 0 0/8px 8px repeat,var(--surface) !important;background-clip:padding-box !important}
.hero #btnShowFav{margin-bottom:10px}
.hero .favswap{margin-top:6px}
/* Nav */''')

# ---- 1. a favourite on Today ----
OLD_DONE = """  else if(s==='done'){const c=cardById(state.todayCard);hero=`${c?`<button class="herocard" id="btnShowToday" aria-label="Look at today's Forgeling">${cardHTML(c,{w:136,mini:true})}</button>`:''}<h2>${c?esc(c.nick||c.name)+' joined your binder':'Today’s Forgeling is in your binder'}</h2><p class="muted">${esc(mirrorLine()||'Come back tomorrow for the next card.')}</p>${compHTML()}"""
NEW_DONE = r"""  else if(s==='done'&&favShows()){const c=cardById(state.todayCard),f=homeFav(),fn=esc(f.nick||f.name);hero=`<button class="herocard" id="btnShowFav" aria-label="Look at ${fn}">${cardHTML(f,{w:136,mini:true})}</button><h2>${fn} is keeping you company</h2><p class="muted">${c?'Today’s find, '+esc(c.nick||c.name)+', is in your binder. ':''}${esc(mirrorLine()||'Come back tomorrow for the next card.')}</p>${compHTML()}${c?'<button class="ghost favswap" id="btnSeeFind">See today’s find</button>':''}${state.packs>0?`<button class="primary" id="btnPack">Open ${state.packs>1?'a pack ('+state.packs+' ready)':'your pack'}</button>`:''}<div style="width:100%;text-align:left">${echoHTML()}</div>`;}
  else if(s==='done'){const c=cardById(state.todayCard),f=homeFav();hero=`${c?`<button class="herocard" id="btnShowToday" aria-label="Look at today's Forgeling">${cardHTML(c,{w:136,mini:true})}</button>`:''}<h2>${c?esc(c.nick||c.name)+' joined your binder':'Today’s Forgeling is in your binder'}</h2><p class="muted">${esc(mirrorLine()||'Come back tomorrow for the next card.')}</p>${compHTML()}${f&&c&&f.id!==c.id?`<button class="ghost favswap" id="btnFavBack">Show ${esc(f.nick||f.name)} here</button>`:''}"""
rep(OLD_DONE, NEW_DONE)
rep('''  else hero=`<h2>Resting today</h2>''', '''  else hero=`${homeFav()?`<button class="herocard" id="btnShowFav" aria-label="Look at ${esc(homeFav().nick||homeFav().name)}">${cardHTML(homeFav(),{w:136,mini:true})}</button>`:''}<h2>Resting today</h2>''')
FAV_JS = r'''/* ---- 0.34: a favourite Forgeling on Today ---- */
const homeFav=()=>{const f=state.homeFav!=null?cardById(state.homeFav):null;return f||null;};
function favShows(){const f=homeFav();return !!f&&f.id!==state.todayCard&&state.findSeen===state.date&&!ui.showFind;}
function markFindSeen(){if(state&&state.status==='done'&&state.findSeen!==state.date&&homeFav()){state.findSeen=state.date;ui.showFind=false;save();}}
'''
rep("function renderToday(){", FAV_JS + "function renderToday(){")
rep("let ui={editJ:false};", "let ui={editJ:false,showFind:false};")
# leaving Today (or the app) after seeing the find hands the spot to the favourite
rep("document.querySelectorAll('.tab').forEach(b=>b.addEventListener('click',()=>{tab=b.dataset.tab;",
    "document.querySelectorAll('.tab').forEach(b=>b.addEventListener('click',()=>{if(tab==='today'&&b.dataset.tab!=='today'){markFindSeen();ui.showFind=false;}tab=b.dataset.tab;if(tab==='today')renderToday();")
rep("document.addEventListener('visibilitychange',()=>{if(document.hidden)nflush();});", "document.addEventListener('visibilitychange',()=>{if(document.hidden){if(typeof markFindSeen==='function'&&state&&tab==='today')markFindSeen();nflush();}});")
rep("  else if(b.id==='btnShowToday')inspect(state.todayCard);", """  else if(b.id==='btnShowToday')inspect(state.todayCard);
  else if(b.id==='btnShowFav'){const f=homeFav();if(f)inspect(f.id);}
  else if(b.id==='btnSeeFind'){ui.showFind=true;renderToday();}
  else if(b.id==='btnFavBack'){state.findSeen=state.date;ui.showFind=false;save();renderToday();}""")
# choosing it, from a card
rep("""<button class="ghost" id="ovClose">Close</button></div>`,true);""",
    """<button class="ghost" id="ovClose">Close</button></div><div class="row" style="justify-content:center;margin-top:0"><button class="ghost" id="inspHome" aria-pressed="${state.homeFav===c.id}">${state.homeFav===c.id?'On Today \\u2713':'Show on Today'}</button></div>`,true);""")
rep("  else if(b.id==='inspFav'){", """  else if(b.id==='inspHome'){const c=cardById(inspId);if(c){const on=state.homeFav!==c.id;state.homeFav=on?c.id:null;save();b.textContent=on?'On Today \\u2713':'Show on Today';b.setAttribute('aria-pressed',String(on));renderToday();toast(on?`${c.nick||c.name} will keep you company on Today, after each day\\u2019s new find.`:'Today shows your newest find again.');}}
  else if(b.id==='inspFav'){""")
# save repair
rep("""  if(s.disc!==undefined&&typeof s.disc!=='string')delete s.disc;""", """  if(s.disc!==undefined&&typeof s.disc!=='string')delete s.disc;
  if(s.homeFav!==undefined&&s.homeFav!==null&&!Number.isInteger(s.homeFav))delete s.homeFav;
  if(s.findSeen!==undefined&&typeof s.findSeen!=='string')delete s.findSeen;""")

rep('<title>Forgelings (prototype 0.33.0)</title>', '<title>Forgelings (prototype 0.34.0)</title>')
rep("const VERSION='prototype 0.33.0'", "const VERSION='prototype 0.34.0'")
rep('const SEEN_V=37;', 'const SEEN_V=38;')
rep("""<ul class="newlist"><li><b>A slower, longer road.</b>""",
    """<ul class="newlist"><li><b>Your favourite, on Today.</b> Open any Forgeling’s card and tap Show on Today. Each day’s new find still shows first, then your favourite keeps you company there. Every card back now wears the campfire, too.</li>
    <li><b>A slower, longer road.</b>""")
import re
_i=src.index('<ul class="newlist">'); _j=src.index('</ul>',_i)
_items=re.findall(r'\s*<li>.*?</li>',src[_i+len('<ul class="newlist">'):_j],re.S)
src=src[:_i]+'<ul class="newlist">'+''.join(_items[:8])+src[_j:]
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src.encode()))

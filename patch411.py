# Forgelings 0.41.1: statue links (Hunter, October 28). A cast statue can be shared as a link that opens the real,
# turnable 3D statue in a friend's browser. The link carries only what the statue is built from (seed, realm, Shade or
# bright, rarity, calling, the keepsake it was cast with, its name and cast date) after a # sign, so it never reaches
# the website. Display only: opening one never adds anything to the friend's collection. A new visitor can look before
# the 18+ check; "Get Forgelings" then goes to it. No SEEN_V bump; the statues What's New note mentions links.
# Reads base41.html.
src = open('base41.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

rep("const VERSION='prototype 0.41.0'", "const VERSION='prototype 0.41.1'")
rep("<title>Forgelings (prototype 0.41.0)</title>", "<title>Forgelings (prototype 0.41.1)</title>")

# ---- the share button in the statue viewer ----
rep("""<button class="chip" id="stPic">Save picture</button></div>
    <button class="ghost" id="ovClose">Close</button></div>`,true);
  ovMode='statue';
  const cv=$('#stCv');cv.dataset.cid=c.id;stvId=c.id;stv=statueView(cv,c,{rise:o.fresh});
  if(!stv){cv.hidden=true;$('#stNo').hidden=false;['stTurn','stBase','stPic'].forEach(i=>{const b=$('#'+i);if(b)b.hidden=true;});}""",
"""<button class="chip" id="stPic">Save picture</button><button class="chip" id="stLink">Share a link</button></div>
    <button class="ghost" id="ovClose">Close</button></div>`,true);
  ovMode='statue';
  const cv=$('#stCv');cv.dataset.cid=c.id;stvId=c.id;stv=statueView(cv,c,{rise:o.fresh});
  if(!stv){cv.hidden=true;$('#stNo').hidden=false;['stTurn','stBase','stPic'].forEach(i=>{const b=$('#'+i);if(b)b.hidden=true;});}""")
rep("  else if(b.id==='stBack')openStatue(+b.dataset.cid);",
    "  else if(b.id==='stBack')openStatue(+b.dataset.cid);\n  else if(b.id==='stLink'){const c=cardById(stvId);if(c)statueLinkSend(c);}\n  else if(b.id==='stGet'){closeModal();}")

# ---- the link: build, read, check, open ----
rep("/* 0.40.1: preview a statue in clay before it can be cast */",
"""/* ---- 0.41.1: statue links. The statue travels inside the link (after #), is rebuilt from its seed in the friend's
   browser, and is only ever shown: nothing is added to their collection. ---- */
let stLinkIn=null,stLinkOpen=false;
const stKeepOK=k=>k===''||KEEPS.some(x=>x.id===k)||KEEPR.some(x=>x.id===k)||FORGE_R.some(r=>r.ti!==undefined&&r.id===k);
function statueLinkCheck(o){
  if(!o||typeof o!=='object'||o.v!==1)return null;
  const int=(x,lo,hi)=>Number.isInteger(x)&&x>=lo&&x<=hi;
  if(!int(o.e,0,4294967295)||!int(o.t,0,4)||!int(o.d,0,1)||!int(o.r,0,4)||!int(o.k,0,11))return null;
  if(typeof o.n!=='string'||!o.n.trim()||o.n.length>24||typeof o.a!=='string'||!/^\\d{4}-\\d{2}-\\d{2}$/.test(o.a))return null;
  const p=typeof o.p==='string'?o.p:'';if(!stKeepOK(p))return null;
  return {v:1,e:o.e,t:o.t,d:o.d,r:o.r,k:o.k,n:o.n.trim(),a:o.a,p};
}
const statueLinkCard=s=>({id:-2,seed:s.e,rarity:s.r,dark:!!s.d,theme:s.t,v:s.k,keep:s.p,bond:BOND_AT[4],name:s.n,nick:'',statue:{at:s.a,keep:s.p}});
function statueLinkSend(c){
  if(!c||!c.statue)return;const n=(c.nick||c.name).slice(0,24);
  const s={v:1,e:c.seed>>>0,t:c.theme,d:c.dark?1:0,r:c.rarity,k:c.v,n,a:c.statue.at,p:c.statue.keep||''};
  const url=GIFT_BASE+'#statue='+b64u.enc(JSON.stringify(s));
  state.statueLinks=(state.statueLinks||0)+1;save();
  shareOrCopy(`Here is ${n}, my Forgebound statue from Forgelings. Turn it around: ${url}`,'Statue link copied. Paste it to a friend.',n+'’s statue');
}
function statueLinkRead(){
  const h=location.hash||'';const m=h.match(/^#statue=([A-Za-z0-9_-]{10,600})$/);
  if(m){let s=null;try{s=statueLinkCheck(JSON.parse(b64u.dec(m[1])));}catch(e){}
    if(s)stLinkIn=s;else setTimeout(()=>toast('That statue link looks broken. Ask your friend to send it again.'),900);}
  if(h.startsWith('#statue=')){try{history.replaceState(null,'',location.pathname+location.search);}catch(e){}}
}
function statueLinkMaybe(force){
  if(!stLinkIn||!state)return;if(!force&&(!modal.hidden||rv||pk))return;
  const s=stLinkIn;stLinkIn=null;openStatueLink(s);
}
function openStatueLink(s){
  const c=statueLinkCard(s);if(stv){stv.stop();stv=null;}
  const n=c.name,R=RAR[c.rarity],gc=c.dark?THEMES[c.theme].dark.glow:THEMES[c.theme].cute.accent,newp=!state.onboarded;
  stLinkOpen=true;ovMode='statue';
  openOverlay(`<div class="stview" style="--sg:${gc}"><p class="rv-title">${esc(n)}</p><p class="stsub">A friend’s statue · ${R.name} · ${esc(realmName(c))}</p>
    <div class="stcan"><canvas id="stCv" tabindex="0" role="img" aria-label="${esc(n)} as a 3D statue on a ${esc(realmName(c))} stand. Drag to turn it, pinch or scroll to zoom, arrow keys to turn."></canvas><p class="stno" id="stNo" hidden>This phone could not start 3D drawing, so here is ${esc(n)} as on the card.<img src="${spriteURL(c)}" alt="${esc(n)}"></p></div>
    <p class="rv-hint">Cast at the Forge ${esc(dateLabel(s.a))}, once ${esc(n)} became Forgebound. Drag to turn, pinch to zoom. Looking adds nothing to your own collection.</p>
    <div class="row stbtns"><button class="chip" id="stTurn" aria-pressed="${!REDUCE}">Turntable</button><button class="chip" id="stBase" aria-pressed="true">Stand</button></div>
    ${newp?'<p class="rv-hint">Forgelings is a calm daily-habit game: do one small thing a day, find a one-of-a-kind creature, and one day cast your own.</p><button class="primary" id="stGet">Get Forgelings</button>':''}
    <button class="ghost" id="ovClose">${newp?'Just looking':'Close'}</button></div>`,true);
  ovMode='statue';const cv=$('#stCv');stvId=null;stv=statueView(cv,c,{});
  if(!stv){cv.hidden=true;$('#stNo').hidden=false;['stTurn','stBase'].forEach(i=>{const b=$('#'+i);if(b)b.hidden=true;});}
  const f=$(newp?'#stGet':'#ovClose');if(f)f.focus({preventScroll:true});
}
/* 0.40.1: preview a statue in clay before it can be cast */""")
# after the friend's statue closes, a new visitor goes on to the title and the age check
rep("function closeModal(){if(pgT){pgT.stop();pgT=null;}if(stv){stv.stop();stv=null;}",
    "function closeModal(){const wasLink=stLinkOpen;stLinkOpen=false;if(wasLink&&state&&!state.onboarded)setTimeout(()=>{if(!state.ageBand)openAgeGate();else if(!state.onboarded)openVector();},60);if(pgT){pgT.stop();pgT=null;}if(stv){stv.stop();stv=null;}")
# boot: read the link; a new visitor sees the statue first (over the title), a player sees it once nothing else is open
rep("""  giftRead();
  if(!state.ageBand)openAgeGate();else if(!state.onboarded)openVector();else if(state.seen<SEEN_V){state.seen=SEEN_V;save();openWhatsNew();}
  setTimeout(giftMaybe,1200);window.addEventListener('hashchange',()=>{giftRead();giftMaybe();});""",
"""  giftRead();statueLinkRead();
  if(!state.ageBand)openAgeGate();else if(!state.onboarded)openVector();else if(state.seen<SEEN_V){state.seen=SEEN_V;save();openWhatsNew();}
  if(stLinkIn&&!state.ageBand)statueLinkMaybe(true);
  setTimeout(giftMaybe,1200);setTimeout(statueLinkMaybe,1300);window.addEventListener('hashchange',()=>{giftRead();giftMaybe();statueLinkRead();statueLinkMaybe(!state.ageBand);});""")
# a modal closing gives a waiting statue link its turn (as gifts do)
src_close_hook = "lastFocus=null;setTimeout(()=>{if(state&&s"
assert src.count(src_close_hook) == 1
src = src.replace(src_close_hook, "lastFocus=null;setTimeout(statueLinkMaybe,800);setTimeout(()=>{if(state&&s")

rep("if(s.giftsSent!==undefined&&!(Number.isInteger(s.giftsSent)&&s.giftsSent>=0))s.giftsSent=0;",
    "if(s.giftsSent!==undefined&&!(Number.isInteger(s.giftsSent)&&s.giftsSent>=0))s.giftsSent=0;\n  if(s.statueLinks!==undefined&&!(Number.isInteger(s.statueLinks)&&s.statueLinks>=0))s.statueLinks=0;")
# ---- privacy wording ----
rep("A gift link holds only the curio, your Forgeling’s name and look, and your note, and the part of the link that holds them is never sent to the website.",
    "A gift link holds only the curio, your Forgeling’s name and look, and your note. A statue link holds only what the statue is built from: its look, name and the day it was cast. The part of a link that holds them is never sent to the website.")
rep("preview any Forgeling's statue in clay before it is Forgebound.",
    "preview any Forgeling's statue in clay before it is Forgebound. Share a statue as a link, and a friend can turn it in 3D too.")
# report
rep("\\nShade curios: ${SCURIOS.filter(x=>state.curios[x.id]).length}", "\\nShade curios: ${SCURIOS.filter(x=>state.curios[x.id]).length}\\nStatue links sent: ${state.statueLinks||0}")

open('work.html', 'w', encoding='utf8').write(src)
# the public privacy page says the same
lp = open('legal/page.py', encoding='utf8').read()
old = "That part of the link comes after a # sign, which browsers never send to the website, so not even the host sees it.</p>"
assert lp.count(old) == 1
lp = lp.replace(old, "A statue link holds only what a statue is built from: its look, its name and the day it was cast. That part of a link comes after a # sign, which browsers never send to the website, so not even the host sees it.</p>")
lp = lp.replace("a text report, or a gift link for a friend.", "a text report, or a gift or statue link for a friend.")
open('legal/page.py', 'w', encoding='utf8').write(lp)
print('ok', len(src))

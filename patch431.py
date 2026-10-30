# 0.43.1: safe saves (from the ChatGPT reliability review, Hunter, October 30).
# One tab saves at a time; save() reports success so Update and Restore respect it; a daily safety copy and a calm
# recovery screen replace quietly starting over when a save can't be read; the statue viewer stops redrawing under reduced motion.
import re,subprocess,sys
S=open('base43.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old)
    assert c==n,(c,n,old[:90])
    S=S.replace(old,new)

rep("const VERSION='prototype 0.43.0'","const VERSION='prototype 0.43.1'")
rep("<title>Forgelings (prototype 0.43.0)</title>","<title>Forgelings (prototype 0.43.1)</title>")

# ---------------- load: repair what can be repaired, and remember what can't ----------------
rep("""function load(){
  let raw=null;try{raw=localStorage.getItem(KEY);}catch(e){return null;}
  if(!raw)return null;
  try{const s=JSON.parse(raw);if(s&&typeof s==='object'&&s.v===1&&Array.isArray(s.cards)&&s.settings&&typeof s.settings==='object')return migrate(s);}catch(e){}
  try{localStorage.setItem(KEY+'-recovery',raw);}catch(e){}
  return null;
}""","""/* 0.43.1: a whole save loads as before; one missing its settings or version is filled in from a fresh one; anything else
   is kept untouched (in -recovery) and the recovery sheet offers the daily safety copy instead of quietly starting over. */
function loadParse(raw){
  try{const s=JSON.parse(raw);if(!s||typeof s!=='object'||Array.isArray(s))return null;
    if(s.v===1&&Array.isArray(s.cards)&&s.settings&&typeof s.settings==='object')return {s:migrate(s),fixed:false};
    if(Array.isArray(s.cards)&&(s.v===1||s.v==null)){const f=fresh(),st=s.settings&&typeof s.settings==='object'&&!Array.isArray(s.settings)?s.settings:{};
      return {s:migrate(Object.assign(f,s,{v:1,settings:Object.assign({},f.settings,st)})),fixed:true};}
  }catch(e){}
  return null;
}
function load(){
  let raw=null;try{raw=localStorage.getItem(KEY);}catch(e){return null;}
  if(!raw)return null;
  const r=loadParse(raw);
  if(r&&!r.fixed)return r.s;
  try{localStorage.setItem(KEY+'-recovery',raw);}catch(e){}
  if(r){loadFixed=true;return r.s;}
  let dr=null,d=null;try{dr=localStorage.getItem(KEY+'-daily');}catch(e){}
  if(dr){const x=loadParse(dr);if(x)d={raw:dr,date:x.s.date,n:x.s.cards.length};}
  loadBad={raw,daily:d};
  return null;
}
let loadFixed=false;""")

# ---------------- save: report success, guard other tabs, keep a daily copy ----------------
rep("""const saveProblems=new Set();""","""const saveProblems=new Set();
let tabAway=false,loadBad=null,dailyAt=null;""")
rep("""function save(){
  try{let s=state;if(!s)return;s._sv=(s._sv||0)+1;
    if(sleepRun&&s.hearth&&s.hearth.sleep)s=Object.assign({},s,{hearth:Object.assign({},s.hearth,{sleep:null})});
    const j=JSON.stringify(s);saveProblem('encode',false);
    try{localStorage.setItem(KEY,j);saveProblem('web',false);}catch(e){saveProblem('web',true);}
    nset(KEY,j);remindSoon();
  }catch(e){saveProblem('encode',true);}
}""","""/* 0.43.1: returns true only when this device kept the save. Another tab in charge, or an unreadable save still waiting on
   the person's choice, means nothing is written. The first save of each session or day also keeps a safety copy;
   when space runs short the safety copy gives way to the real save. */
function save(){
  if(tabAway||loadBad)return false;
  try{let s=state;if(!s)return false;s._sv=(s._sv||0)+1;
    if(sleepRun&&s.hearth&&s.hearth.sleep)s=Object.assign({},s,{hearth:Object.assign({},s.hearth,{sleep:null})});
    const j=JSON.stringify(s);saveProblem('encode',false);let ok=true;
    try{localStorage.setItem(KEY,j);saveProblem('web',false);}
    catch(e){try{localStorage.removeItem(KEY+'-daily');dailyAt=null;localStorage.setItem(KEY,j);saveProblem('web',false);}catch(e2){ok=false;saveProblem('web',true);}}
    if(ok&&dailyAt!==s.date){try{localStorage.setItem(KEY+'-daily',j);dailyAt=s.date;}catch(e){}}
    nset(KEY,j);remindSoon();return ok;
  }catch(e){saveProblem('encode',true);return false;}
}""")

# every erase also clears the safety copy
rep("""localStorage.removeItem(KEY+'-recovery');""","""localStorage.removeItem(KEY+'-recovery');localStorage.removeItem(KEY+'-daily');""",3)

# ---------------- restore respects save() ----------------
rep("""const prevState=state;try{const s=JSON.parse($('#resText').value.trim());if(!(s&&typeof s==='object'&&s.v===1&&Array.isArray(s.cards)&&s.settings&&typeof s.settings==='object'))throw 0;s.ageBand=state.ageBand||s.ageBand;state=migrate(s);rollover();save();applySettings();closeModal();tab='today';render();toast('Restored.');}
    catch(err){state=prevState;save();try{applySettings();render();}catch(e2){}b.dataset.armed='0';b.textContent='Restore';sfx('no');toast('That does not look like a saved copy. Nothing was changed.');}""",
"""const prevState=state,wasBad=loadBad;try{const s=JSON.parse($('#resText').value.trim());if(!(s&&typeof s==='object'&&s.v===1&&Array.isArray(s.cards)&&s.settings&&typeof s.settings==='object'))throw 0;s.ageBand=state.ageBand||s.ageBand;state=migrate(s);rollover();loadBad=null;if(!save())throw 'nosave';applySettings();closeModal();tab='today';render();toast('Restored.');if(!state.ageBand)openAgeGate();else if(!state.onboarded)openVector();}
    catch(err){state=prevState;loadBad=wasBad;save();try{applySettings();render();}catch(e2){}b.dataset.armed='0';b.textContent='Restore';sfx('no');toast(err==='nosave'?'This device could not keep the restored copy, so nothing was changed. Free up a little space and try again.':'That does not look like a saved copy. Nothing was changed.');}""")
rep("""    <div class="stack"><button class="primary" id="doRestore">Restore</button><button class="ghost" data-close>Cancel</button></div>`);""",
"""    <div class="stack"><button class="primary" id="doRestore">Restore</button>${loadBad?'<button class="ghost" id="recBack">Back</button>':'<button class="ghost" data-close>Cancel</button>'}</div>`,loadBad?false:undefined);""")

# ---------------- the recovery sheet ----------------
rep("""function openRestore(){""","""function openRecover(){
  const d=loadBad&&loadBad.daily;
  openSheet(`<h2>Your collection needs a moment</h2><p>This device could not read your saved collection. Nothing has been deleted.</p>
    ${d?`<p>A safety copy from <b>${esc(dateLabel(d.date))}</b> is here, with ${d.n} ${d.n===1?'Forgeling':'Forgelings'}.</p><button class="primary" id="recUse" style="width:100%">Use the safety copy</button>`:''}
    <p class="muted small" style="margin:14px 0 4px">If you saved a backup copy, you can restore it instead.</p>
    <div class="stack"><button class="${d?'ghost':'primary'}" id="recRestore">Restore a backup</button><button class="ghost" id="recCopy">Copy the unreadable save</button><button class="ghost" id="recFresh">Start over</button></div>
    <p class="muted small">Starting over keeps the unreadable save on this device, in case it can be mended later.</p>`,false);
}
function openRestore(){""")
rep("""  else if(b.id==='doRestore'){""","""  else if(b.id==='recUse'&&loadBad&&loadBad.daily){let ok=true;try{localStorage.setItem(KEY,loadBad.daily.raw);}catch(e){ok=false;}if(ok)location.reload();else toast('This device is out of space. Restore a backup, or start over.');}
  else if(b.id==='recRestore')openRestore();
  else if(b.id==='recBack')openRecover();
  else if(b.id==='recCopy'&&loadBad)shareOrCopy(loadBad.raw,'Copied. Keep it somewhere safe.','My Forgelings save');
  else if(b.id==='recFresh'){
    if(b.dataset.armed!=='1'){b.dataset.armed='1';b.textContent='Tap again to start over';return;}
    loadBad=null;closeModal();openAgeGate();
  }
  else if(b.id==='doRestore'){""")

# ---------------- one tab at a time ----------------
rep("""function updBar(){""","""/* 0.43.1: the newest tab is in charge. Any other copy stops saving and offers to take over, by reloading the latest save. */
const TAB_ID=Math.random().toString(36).slice(2);
function tabAwayOn(){
  if(tabAway||!document.body)return;tabAway=true;
  const ub=document.getElementById('updBar');if(ub)ub.remove();
  const o=document.createElement('div');o.id='tabAway';o.className='tabaway';o.setAttribute('role','dialog');o.setAttribute('aria-modal','true');o.setAttribute('aria-labelledby','tabAwayH');
  o.innerHTML='<div class="tabbox"><h2 id="tabAwayH">Forgelings is open somewhere else</h2><p>Only one copy keeps your progress at a time, so nothing gets written over.</p><button type="button" class="primary" id="tabHere">Use it here</button></div>';
  document.body.appendChild(o);['.app','.tabs','#modal','#toast'].forEach(s=>{const e=document.querySelector(s);if(e)e.inert=true;});
  o.querySelector('#tabHere').onclick=()=>location.reload();o.querySelector('#tabHere').focus({preventScroll:true});
}
function tabWatch(){
  try{const ch=new BroadcastChannel('forgelings-tabs');ch.onmessage=e=>{if(e.data&&e.data.t==='here'&&e.data.id!==TAB_ID)tabAwayOn();};ch.postMessage({t:'here',id:TAB_ID});}catch(e){}
  window.addEventListener('storage',e=>{if(e.key===KEY||e.key===null)tabAwayOn();});
}
function updBar(){""")
rep("""  b.querySelector('#updGo').onclick=()=>{try{save();}catch(e){}location.reload();};""",
"""  b.querySelector('#updGo').onclick=()=>{let ok=true;try{ok=tabAway||!!loadBad||save();}catch(e){ok=false;}if(!ok){toast('Your progress could not be saved just now, so the update will wait. Save a backup copy first.');return;}location.reload();};""")

# ---------------- boot ----------------
rep("""function boot(){
state=load()||migrate(fresh());""","""function boot(){
state=load()||migrate(fresh());tabWatch();""")
rep("""  if(!state.ageBand)openAgeGate();else if(!state.onboarded)openVector();else if(state.seen<SEEN_V){state.seen=SEEN_V;save();openWhatsNew();}""",
"""  if(loadBad)openRecover();else if(!state.ageBand)openAgeGate();else if(!state.onboarded)openVector();else if(state.seen<SEEN_V){state.seen=SEEN_V;save();openWhatsNew();}
  if(loadFixed&&!loadBad)setTimeout(()=>toast('Your save needed a small repair. Everything that could be read is here.'),900);""")
rep("""  if(stLinkIn&&!state.ageBand)statueLinkMaybe(true);""","""  if(stLinkIn&&!state.ageBand&&!loadBad)statueLinkMaybe(true);""")
rep("""  setTimeout(giftMaybe,1200);setTimeout(statueLinkMaybe,1300);""","""  if(!loadBad){setTimeout(giftMaybe,1200);setTimeout(statueLinkMaybe,1300);}""")

# ---------------- statue viewer: still under reduced motion ----------------
rep("""    v.raf=requestAnimationFrame(draw);}
  const ptr=new Map();""","""    v.raf=0;if(!REDUCE||v.rise<1)v.raf=requestAnimationFrame(draw);}
  /* 0.43.1: with reduced motion the statue is drawn once and again only when touched, turned or zoomed. */
  const kick=()=>{if(!v.raf&&!v.dead)v.raf=requestAnimationFrame(draw);};
  const ptr=new Map();""")
rep("""  v.raf=requestAnimationFrame(draw);
  return {v,stop(){""","""  ['pointerdown','pointermove','wheel','keydown'].forEach(n=>cv.addEventListener(n,kick));window.addEventListener('resize',kick);
  v.raf=requestAnimationFrame(draw);
  return {v,kick,stop(){window.removeEventListener('resize',kick);""")

# ---------------- What's New ----------------
rep("""<ul class="newlist"><li><b>Tidier pages.</b>""","""<ul class="newlist"><li><b>Safer saving.</b> If Forgelings is open in two places, only one keeps your progress, so nothing gets written over. Updates and restores wait until your progress is safely saved, and if a save ever can't be read, a daily safety copy is there to bring it back.</li><li><b>Tidier pages.</b>""")

# ---------------- CSS ----------------
CSS="""
/* 0.43.1 safe saves */
.tabaway{position:fixed;inset:0;z-index:95;background:rgba(14,11,34,.86);display:flex;align-items:center;justify-content:center;padding:16px}
.tabbox{background:#1C1840;color:#FFF7EC;border:3px solid #FFD36B;max-width:360px;width:100%;padding:20px;border-radius:16px;text-align:center}.tabbox h2{margin:0 0 8px;color:#FFF7EC}.tabbox p{margin:0 0 16px}.tabbox button{width:100%;min-height:48px}
"""
rep(""".ribsheet .dots i.on{background:var(--plum);border-color:var(--plum)}""",""".ribsheet .dots i.on{background:var(--plum);border-color:var(--plum)}"""+CSS)

open('work.html','w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S)
open('/tmp/chk431.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk431.js'],capture_output=True,text=True)
print('node --check',r.returncode,r.stderr[:800])

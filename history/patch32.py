# Forgelings 0.32.0: native groundwork. Nothing changes on the web; inside the iPhone app (Capacitor) Forgelings:
# 1. Keeps saves safe: every save is mirrored to native storage (Preferences = UserDefaults), and on launch the newer
#    of the two copies wins, so iOS clearing web storage can never lose a collection. The age block is mirrored too.
# 2. Real reminders (Local Notifications): one gentle nudge at a chosen time on days today's card isn't done yet,
#    rescheduled after every save, and a note when a wanderer is back. Never a pile of them.
# 3. Haptics on taps, saves, reveals and game catches (Settings toggle).
# 4. The native share sheet for gift links, reports, share pictures and backup files.
# 5. A store edition (meta forge-build=store, or any native run): tester-only pieces hidden (feedback questions,
#    pilot report, prototype tools), "First Edition" on cards, and a plain version label.
# Reads base31.html.
import re
src = open('base31.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

APPVER = '1.0.0'
rep("const VERSION='prototype 0.31.0';", f"""const VERSION='prototype 0.32.0',APPVER='{APPVER}';
/* ---- 0.32: running inside the iPhone app? (Capacitor injects window.Capacitor with its plugins.) ---- */
const CAP=window.Capacitor,NATIVE=!!(CAP&&CAP.isNativePlatform&&CAP.isNativePlatform()),PL=(NATIVE&&CAP.Plugins)||{{}};
const STORE=NATIVE||!!document.querySelector('meta[name="forge-build"][content="store"]'),EDITION=STORE?'First Edition':'Pilot Edition';""")

# ---- 1. safe saves ----
rep("const KEY='forge-app-v1',BLOCK='forge-age-block',MIN_AGE=18;", r"""const KEY='forge-app-v1',BLOCK='forge-age-block',MIN_AGE=18;
const NQ={q:{},t:null};
function nset(k,v){if(!NATIVE||!PL.Preferences)return;NQ.q[k]=v;clearTimeout(NQ.t);NQ.t=setTimeout(nflush,250);}
function nflush(){const q=NQ.q;NQ.q={};clearTimeout(NQ.t);Object.keys(q).forEach(k=>{try{const p=q[k]===null?PL.Preferences.remove({key:k}):PL.Preferences.set({key:k,value:q[k]});if(p&&p.catch)p.catch(()=>{});}catch(e){}});}
async function nrestore(){
  if(!NATIVE||!PL.Preferences)return;
  const sv=t=>{try{return (JSON.parse(t)||{})._sv||0;}catch(e){return -1;}};
  for(const k of [KEY,BLOCK]){
    let nv=null,lv=null;try{nv=(await PL.Preferences.get({key:k})).value||null;}catch(e){}try{lv=localStorage.getItem(k);}catch(e){}
    if(k===KEY&&nv&&lv){if(sv(nv)>sv(lv)){try{localStorage.setItem(k,nv);}catch(e){}}else if(sv(lv)>sv(nv))nset(k,lv);}
    else if(nv&&!lv){try{localStorage.setItem(k,nv);}catch(e){}}
    else if(lv&&!nv)nset(k,lv);
  }
  nflush();
}
document.addEventListener('visibilitychange',()=>{if(document.hidden)nflush();});""")
rep("""function save(){try{let s=state;if(sleepRun&&s&&s.hearth&&s.hearth.sleep)s=Object.assign({},s,{hearth:Object.assign({},s.hearth,{sleep:null})});localStorage.setItem(KEY,JSON.stringify(s));}catch(e){}}""",
    """function save(){try{let s=state;if(!s)return;s._sv=(s._sv||0)+1;if(sleepRun&&s.hearth&&s.hearth.sleep)s=Object.assign({},s,{hearth:Object.assign({},s.hearth,{sleep:null})});const j=JSON.stringify(s);try{localStorage.setItem(KEY,j);}catch(e){}nset(KEY,j);remindSoon();}catch(e){}}""")
rep("""  if(a<MIN_AGE){try{localStorage.setItem(BLOCK,String(Date.now()));localStorage.removeItem(KEY);localStorage.removeItem(KEY+'-recovery');}catch(e){}showBlocked();return;}""",
    """  if(a<MIN_AGE){try{localStorage.setItem(BLOCK,String(Date.now()));localStorage.removeItem(KEY);localStorage.removeItem(KEY+'-recovery');}catch(e){}nset(BLOCK,String(Date.now()));nset(KEY,null);nflush();showBlocked();return;}""")
rep("""    try{localStorage.removeItem(KEY);localStorage.removeItem(KEY+'-recovery');localStorage.removeItem(QSEEN);}catch(e){}
    state=migrate(fresh());""", """    try{localStorage.removeItem(KEY);localStorage.removeItem(KEY+'-recovery');localStorage.removeItem(QSEEN);}catch(e){}
    nset(KEY,null);nflush();if(NATIVE&&PL.LocalNotifications){try{PL.LocalNotifications.cancel({notifications:[{id:1},{id:2}]}).catch(()=>{});}catch(e){}}
    state=migrate(fresh());""")
# boot waits for the native copy
rep("""/* ================= Start ================= */
state=load()||migrate(fresh());""", """/* ================= Start ================= */
function boot(){
state=load()||migrate(fresh());""")
rep("""  if(state.ageBand)arrive();
  wanderTick();
}""", """  if(state.ageBand)arrive();
  wanderTick();remindSync(false);
}
}
if(NATIVE)nrestore().then(boot,boot);else boot();""")

# ---- 2. reminders ----
REM_JS = r'''/* ---- 0.32: reminders in the iPhone app. One gentle nudge, never a pile. ---- */
let remT=null;
const remindSoon=()=>{if(!NATIVE||!PL.LocalNotifications)return;clearTimeout(remT);remT=setTimeout(()=>remindSync(false),1000);};
const NUDGE_L=['Today’s card is waiting by the fire.','Your Forgelings saved you a warm spot.','One small thing today? Your card is ready when you are.','The fire is lit. Today’s card is face down, waiting.'];
function nudgeAt(t){const m=/^(\d{1,2}):(\d{2}) (am|pm)$/.exec(t||'');if(!m)return null;let h=+m[1]%12;if(m[3]==='pm')h+=12;return [h,+m[2]];}
async function remindSync(ask){
  if(!NATIVE||!PL.LocalNotifications||!state)return false;const LN=PL.LocalNotifications;
  try{
    const want=!!state.settings.nudge||(!!state.wander&&state.settings.wnote!==false);
    let p=await LN.checkPermissions();
    if(p.display!=='granted'){if(!ask||!want)return false;p=await LN.requestPermissions();if(p.display!=='granted'){toast('Notifications are off for Forgelings in your phone’s settings.');return false;}}
    await LN.cancel({notifications:[{id:1},{id:2}]});const list=[],now=new Date(),hm=nudgeAt(state.settings.nudge);
    if(hm){const d=new Date(now);d.setHours(hm[0],hm[1],0,0);if(d<=now||state.status==='done'||state.status==='rest')d.setDate(d.getDate()+1);
      list.push({id:1,title:'Forgelings',body:NUDGE_L[dnum(dkey(d))%NUDGE_L.length],schedule:{at:d,allowWhileIdle:true}});}
    const w=state.wander,c=w&&cardById(w.id);
    if(c&&state.settings.wnote!==false&&w.ready>Date.now()+30000)list.push({id:2,title:'Forgelings',body:`${c.nick||c.name} is back from wandering, with something for your shelf.`,schedule:{at:new Date(w.ready),allowWhileIdle:true}});
    if(list.length)await LN.schedule({notifications:list});
    return true;
  }catch(e){return false;}
}
function remindHTML(){
  if(!NATIVE)return '';const S=state.settings;
  return `<div class="setblock"><b>Reminders</b><p class="muted small">One gentle nudge on days today’s card is still waiting. Never more than one, and missing a day never costs anything.</p>
    <div class="chips" role="group" aria-label="Daily reminder">${[[null,'Off'],['8:00 am','8:00 am'],['12:00 pm','12:00 pm'],['6:00 pm','6:00 pm']].map(a=>`<button class="chip" data-setnudge="${a[0]||''}" aria-pressed="${(S.nudge||null)===a[0]}">${a[1]}</button>`).join('')}</div>
    <div class="chips"><button class="chip" id="setWnote" aria-pressed="${S.wnote!==false}">Tell me when a wanderer is back ${S.wnote!==false?'on':'off'}</button><button class="chip" id="setHaptic" aria-pressed="${S.haptics!==false}">Haptics ${S.haptics!==false?'on':'off'}</button></div></div>`;
}
/* ---- 0.32: haptics ---- */
function buzz(k){if(!NATIVE||!PL.Haptics||(state&&state.settings.haptics===false))return;try{const p=k==='success'?PL.Haptics.notification({type:'SUCCESS'}):PL.Haptics.impact({style:k||'LIGHT'});if(p&&p.catch)p.catch(()=>{});}catch(e){}}
/* ---- 0.32: the native share sheet, for text and for files ---- */
function nshareFile(blob,name,title){
  return new Promise((res,rej)=>{const fr=new FileReader();fr.onerror=rej;fr.onload=async()=>{try{
    const b64=String(fr.result).split(',')[1],w=await PL.Filesystem.writeFile({path:name,data:b64,directory:'CACHE'});
    await PL.Share.share({title,files:[w.uri],dialogTitle:title});res();}catch(e){rej(e);}};fr.readAsDataURL(blob);});
}
'''
rep("/* ================= Start ================= */", REM_JS + "/* ================= Start ================= */")
rep("    ${installTipHTML()}\n", "    ${remindHTML()}${installTipHTML()}\n")
rep("""  else if(b.dataset.setnudge!==undefined){state.settings.nudge=b.dataset.setnudge||null;save();renderSettings();}""",
    """  else if(b.dataset.setnudge!==undefined){state.settings.nudge=b.dataset.setnudge||null;save();renderSettings();if(state.settings.nudge)remindSync(true).then(ok=>{if(ok)toast(`A gentle nudge at ${state.settings.nudge}, only on days your card is still waiting.`);});else remindSync(false);}
  else if(b.id==='setWnote'){state.settings.wnote=state.settings.wnote===false;save();renderSettings();if(state.settings.wnote!==false)remindSync(true);}
  else if(b.id==='setHaptic'){state.settings.haptics=state.settings.haptics===false;save();renderSettings();buzz('MEDIUM');}""")
# a wander start may ask once for permission to say when they're back
rep("""  state.wstat.sent++;save();hf.msg=to>=0?""", """  state.wstat.sent++;save();if(NATIVE&&!state.settings.wAsked){state.settings.wAsked=true;save();remindSync(true);}hf.msg=to>=0?""")
rep("  if(!RELEASE||STANDALONE())return '';", "  if(!RELEASE||STANDALONE()||NATIVE)return '';")

# ---- 3. haptics hooks ----
rep("function sfx(n){if(!state||state.settings.sfx===false||!sOn())return;",
    "function sfx(n){if(n==='tap'||n==='select'||n==='tab')buzz('LIGHT');else if(n==='save'||n==='no')buzz('MEDIUM');if(!state||state.settings.sfx===false||!sOn())return;")
rep("function chime(n){if(!state||state.settings.sfx===false||!sOn())return;",
    "function chime(n){if(n>=2)buzz('success');if(!state||state.settings.sfx===false||!sOn())return;")
rep("function gHit(pts,x,y,col,tone){const g=game;", "function gHit(pts,x,y,col,tone){buzz('LIGHT');const g=game;")

# ---- 4. native share ----
rep("function shareOrCopy(txt,done,title){\n", "function shareOrCopy(txt,done,title){\n  if(NATIVE&&PL.Share){PL.Share.share({title,text:txt,dialogTitle:title}).catch(err=>{if(!/cancel/i.test(String(err&&err.message||err)))copyText(txt,done);});return;}\n")
rep("""  let f=null;try{f=new File([blob],name,{type:'application/json'});}catch(e){}
  try{if(f&&navigator.share""", """  if(NATIVE&&PL.Share&&PL.Filesystem){nshareFile(blob,name,'Forgelings backup').then(()=>done('Saved. Keep it somewhere safe.')).catch(err=>{if(!/cancel/i.test(String(err&&err.message||err)))toast('That copy could not be saved here.');});return;}
  let f=null;try{f=new File([blob],name,{type:'application/json'});}catch(e){}
  try{if(f&&navigator.share""")
rep("""  let f=null;try{f=new File([s.blob],name,{type:'image/png'});}catch(e){}
  if(f&&canShareFiles())""", """  if(NATIVE&&PL.Share&&PL.Filesystem){nshareFile(s.blob,name,nm).then(()=>toast('Shared.')).catch(err=>{if(!/cancel/i.test(String(err&&err.message||err)))toast('That picture could not be shared here.');});return;}
  let f=null;try{f=new File([s.blob],name,{type:'image/png'});}catch(e){}
  if(f&&canShareFiles())""")

# ---- 5. store edition ----
rep("<div class=\"foot\"><span>Pilot Edition</span>", "<div class=\"foot\"><span>${EDITION}</span>")
rep("<div class=\"m4\">Pilot Edition, No. ${pad(c.serial)}</div>", "<div class=\"m4\">${EDITION}, No. ${pad(c.serial)}</div>")
rep("  else if(!state.feedbackAsked&&doneDays()>=5){", "  else if(!STORE&&!state.feedbackAsked&&doneDays()>=5){")
rep('    <div class="setblock"><b>Share your thoughts</b>', '    ${STORE?\'\':`<div class="setblock"><b>Share your thoughts</b>')
i = src.index('    <details class="dev"><summary>Prototype tools</summary>'); j = src.index('</details>', i) + len('</details>')
blk = src[i:j]
src = src[:i] + blk + '`}' + src[j:]
rep('<p class="muted small center" style="margin:14px 0 0">${VERSION}</p>', '<p class="muted small center" style="margin:14px 0 0">${STORE?\'Forgelings \'+APPVER:VERSION}</p>')

rep('<title>Forgelings (prototype 0.31.0)</title>', '<title>Forgelings (prototype 0.32.0)</title>')
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src.encode()))

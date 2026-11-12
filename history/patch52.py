# 0.52.0: native groundwork from the competitor review (Hunter, November 11).
#   1. A quiet copy in the player's own iCloud (iPhone app; CloudSavePlugin.swift on the ios-app branch). The same journal
#      (jid) on both sides: the newer save wins quietly. A different journal in iCloud is never swapped in silently: the
#      player chooses. Settings shows it and can turn it off (which removes the iCloud copy). Erase clears iCloud too.
#   2. Android: the back button closes what's open, then goes to Today, then leaves the app; screen edges come from the
#      Android app's --safe-area-inset-* values where the WebView's env() reports zero.
#   3. Wording: privacy note and Settings say where the copy lives on each platform; the monthly backup nudge rests while
#      iCloud holds a fresh copy.
import re,subprocess,os
S=open('base51.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.51.0'","const VERSION='prototype 0.52.0'")
rep("<title>Forgelings (prototype 0.51.0)</title>","<title>Forgelings (prototype 0.52.0)</title>")

# ---- a journal id, so two different journals are never confused for one
rep("function migrate(s){sanitize(s);","function migrate(s){sanitize(s);if(typeof s.jid!=='string'||!/^[a-z0-9]{6,24}$/.test(s.jid))s.jid=rid();")

# ---- 1. the iCloud copy
CLOUD=r"""
/* ---- 0.52: a quiet copy in the player's own iCloud (iPhone app only: CloudSavePlugin.swift, Apple's key-value
   storage, 1 MB per app). Android keeps its copy through Android's own app backup. The copy is the save, gzipped
   (about 13 KB a year). Same journal (jid) on both sides: the newer _sv wins quietly. A different journal in iCloud is
   never swapped in silently: the player chooses. ---- */
const CLOUD_OFF='forge-cloud-off',CLOUD_AT='forge-cloud-at';
const CS={t:null,busy:false,offer:null,avail:null,err:null};
const cloudPlug=()=>NATIVE&&PL.CloudSave?PL.CloudSave:null;
const cloudOn=()=>{if(!cloudPlug())return false;try{return localStorage.getItem(CLOUD_OFF)!=='1';}catch(e){return true;}};
const cloudAt=()=>{try{return +localStorage.getItem(CLOUD_AT)||0;}catch(e){return 0;}};
const ANDROID=NATIVE&&((CAP.getPlatform&&CAP.getPlatform()==='android')||/Android/i.test(navigator.userAgent));
async function czip(t){try{if(typeof CompressionStream==='undefined')throw 0;const u=new Uint8Array(await new Response(new Blob([t]).stream().pipeThrough(new CompressionStream('gzip'))).arrayBuffer());let s='';for(let i=0;i<u.length;i+=0x8000)s+=String.fromCharCode.apply(null,u.subarray(i,i+0x8000));return 'gz1:'+btoa(s);}catch(e){return 'j1:'+t;}}
async function cunzip(v){if(typeof v!=='string')return null;if(v.startsWith('j1:'))return v.slice(3);if(!v.startsWith('gz1:'))return null;const b=atob(v.slice(4)),u=new Uint8Array(b.length);for(let i=0;i<b.length;i++)u[i]=b.charCodeAt(i);return await new Response(new Blob([u]).stream().pipeThrough(new DecompressionStream('gzip'))).text();}
const cparse=t=>{try{const o=JSON.parse(t);return o&&typeof o==='object'&&!Array.isArray(o)?o:null;}catch(e){return null;}};
async function cloudRead(){const p=cloudPlug();if(!p)return null;try{const st=await p.status();CS.avail=!!(st&&st.available);if(!CS.avail)return null;const r=await p.get({key:KEY});const t=await cunzip(r&&r.value);const o=t&&cparse(t);return o?{t,o}:null;}catch(e){CS.err=String(e&&e.message||e);return null;}}
// which save to keep: 'cloud' (take iCloud's), 'local' (keep this phone's), 'offer' (two different journals: ask)
function cloudPick(lo,co){
  const n=o=>o&&Array.isArray(o.cards)?o.cards.length:0;
  if(!co||!n(co))return 'local';if(!lo||!n(lo))return 'cloud';
  if(lo.jid&&co.jid&&lo.jid!==co.jid)return 'offer';
  return (co._sv||0)>(lo._sv||0)?'cloud':'local';
}
async function cloudRestore(){
  if(!cloudOn())return;const c=await cloudRead();if(!c)return;
  let lt=null;try{lt=localStorage.getItem(KEY);}catch(e){}
  const r=cloudPick(lt&&cparse(lt),c.o);
  if(r==='cloud'){try{localStorage.setItem(KEY,c.t);localStorage.removeItem(KEY+'-daily');}catch(e){}nset(KEY,c.t);}
  else if(r==='offer')CS.offer=c;
}
function cloudSoon(){if(!cloudOn()||CS.offer)return;clearTimeout(CS.t);CS.t=setTimeout(cloudPush,4000);}
async function cloudPush(){
  clearTimeout(CS.t);if(!cloudOn()||CS.offer||CS.busy)return;let t=null;try{t=localStorage.getItem(KEY);}catch(e){}if(!t)return;
  CS.busy=true;try{const p=cloudPlug(),st=await p.status();CS.avail=!!(st&&st.available);
    if(CS.avail){await p.set({key:KEY,value:await czip(t)});CS.err=null;try{localStorage.setItem(CLOUD_AT,String(Date.now()));}catch(e){}}
  }catch(e){CS.err=String(e&&e.message||e);}CS.busy=false;
  const l=document.getElementById('cloudLine');if(l)l.textContent=cloudLine();
}
function cloudLine(){
  if(!cloudOn())return 'Off. Your collection lives only on this phone, so save a copy now and then.';
  if(CS.avail===false)return 'Sign in to iCloud in your iPhone’s Settings to keep a copy there.';
  const a=cloudAt();if(!a)return 'A copy is kept in your own iCloud, so a new iPhone brings your Forgelings back.';
  const m=Math.round((Date.now()-a)/60000);
  return 'A copy is kept in your own iCloud, so a new iPhone brings your Forgelings back. Last saved '+(m<2?'just now':m<60?m+' minutes ago':m<1440?Math.round(m/60)+(Math.round(m/60)===1?' hour ago':' hours ago'):'on '+new Date(a).toLocaleDateString())+'.';
}
function cloudSetHTML(){
  if(cloudPlug())return `<div class="lbl2">iCloud</div><p class="muted small" id="cloudLine">${esc(cloudLine())}</p><button class="pill" id="btnCloud">${cloudOn()?'Turn off the iCloud copy':'Keep a copy in iCloud'}</button>`;
  if(ANDROID)return `<div class="lbl2">Android backup</div><p class="muted small">If backup is on for this phone, Android keeps a copy of Forgelings with your other apps, and a new phone brings it back.</p>`;
  return '';
}
async function cloudLive(){
  if(!cloudOn()||!state||CS.offer)return;const c=await cloudRead();if(!c)return;const r=cloudPick(state,c.o);
  if(r==='cloud'){try{localStorage.setItem(KEY,c.t);localStorage.removeItem(KEY+'-daily');}catch(e){}nset(KEY,c.t);nflush();tabAway=true;setTimeout(()=>location.reload(),300);}
  else if(r==='offer'){CS.offer=c;cloudOfferSoon();}
}
function cloudOfferSoon(){if(!CS.offer)return;if(!state||!state.ageBand||!modal.hidden){setTimeout(cloudOfferSoon,2000);return;}cloudOffer();}
function cloudOffer(){
  const c=CS.offer;if(!c)return;const n=c.o.cards.length,m=state.cards.length,pl=k=>k+' Forgeling'+(k===1?'':'s');
  const d=c.o.date&&/^\d{4}-\d{2}-\d{2}$/.test(c.o.date)?new Date(c.o.date+'T12:00:00').toLocaleDateString(undefined,{month:'long',day:'numeric',year:'numeric'}):'';
  openSheet(`<h2>A journal in your iCloud</h2><p class="muted">Your iCloud holds a Forgelings journal from another phone, with ${pl(n)}${d?', last opened '+esc(d):''}. This phone has its own, with ${pl(m)}.</p><p class="muted small">iCloud keeps one journal. The one you don’t choose is replaced, so save a copy of this phone’s journal first if you want to keep both.</p><div class="stack"><button class="primary" id="cloudUse">Use the iCloud journal (${pl(n)})</button><button class="ghost" id="cloudKeep">Keep this phone’s journal (${pl(m)})</button><button class="ghost" id="cloudCopy">Save a copy of this phone’s journal</button></div>`);
}
document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('#cloudUse,#cloudKeep,#cloudCopy');if(!b)return;
  if(b.id==='cloudCopy'){openExport();return;}
  const c=CS.offer;CS.offer=null;
  if(b.id==='cloudUse'&&c){try{localStorage.setItem(KEY+'-replaced',JSON.stringify(state));localStorage.setItem(KEY,c.t);localStorage.removeItem(KEY+'-daily');}catch(e){}nset(KEY,c.t);nflush();tabAway=true;closeModal();setTimeout(()=>location.reload(),300);}
  else{closeModal();cloudPush();toast('This phone\u2019s journal is now the one in iCloud.');}
});
if(cloudPlug()){try{cloudPlug().addListener('change',ev=>{if(!ev||!Array.isArray(ev.keys)||ev.keys.includes(KEY))cloudLive();});}catch(e){}}
"""
rep("""  nflush();
}
document.addEventListener('visibilitychange',()=>{if(document.hidden){if(typeof markFindSeen==='function'&&state&&tab==='today')markFindSeen();nflush();}});""",
"""  await cloudRestore();
  nflush();
}
document.addEventListener('visibilitychange',()=>{if(document.hidden){if(typeof markFindSeen==='function'&&state&&tab==='today')markFindSeen();nflush();cloudPush();}else if(cloudOn()&&state)cloudLive();});"""+CLOUD)
rep("    nset(KEY,j);remindSoon();return ok;","    nset(KEY,j);cloudSoon();remindSoon();return ok;")
# after boot: the choice between two journals, once the app is settled
rep("  wanderTick();remindSync(false);\n}\n}\nif(NATIVE)nrestore().then(boot,boot);else boot();",
    "  wanderTick();remindSync(false);\n  if(CS.offer)setTimeout(cloudOfferSoon,900);else if(cloudOn())cloudSoon();\n}\n}\nif(NATIVE)nrestore().then(boot,boot);else boot();")
# Settings: the iCloud (or Android backup) line under Backup
rep("""Your collection lives on this device. Save a copy so you can move it or restore it.</p><div class="chips"><button class="pill" id="btnExport">Save a copy</button><button class="pill" id="btnRestore">Restore a copy</button></div>`)}""",
    """Your collection lives on this device. Save a copy so you can move it or restore it.</p><div class="chips"><button class="pill" id="btnExport">Save a copy</button><button class="pill" id="btnRestore">Restore a copy</button></div>${cloudSetHTML()}`)}""")
# buttons
rep("""  else if(b.id==='btnExport')openExport();""",
"""  else if(b.id==='btnExport')openExport();
  else if(b.id==='btnCloud'){
    if(cloudOn()){try{localStorage.setItem(CLOUD_OFF,'1');localStorage.removeItem(CLOUD_AT);}catch(e){}try{cloudPlug().remove({key:KEY}).catch(()=>{});}catch(e){}toast('The iCloud copy is off and removed.');}
    else{try{localStorage.removeItem(CLOUD_OFF);}catch(e){}cloudPush().then(()=>{const l=$('#cloudLine');if(l)l.textContent=cloudLine();});toast('Keeping a copy in your iCloud.');}
    renderSettings();
  }
""")
rep("""    if(b.dataset.armed!=='1'){b.dataset.armed='1';b.textContent='Tap again to erase everything. This cannot be undone.';return;}""",
    """    if(b.dataset.armed!=='1'){b.dataset.armed='1';b.textContent=cloudOn()?'Tap again to erase everything here and in iCloud. This cannot be undone.':'Tap again to erase everything. This cannot be undone.';return;}
    if(cloudPlug()){clearTimeout(CS.t);CS.offer=null;try{cloudPlug().remove({key:KEY}).catch(()=>{});}catch(e){}try{localStorage.removeItem(CLOUD_AT);localStorage.removeItem(KEY+'-replaced');}catch(e){}}""")
rep("""<button class="pill" id="btnErase">Erase everything on this device</button>""",
    """<button class="pill" id="btnErase">${cloudOn()?'Erase everything here and in iCloud':'Erase everything on this device'}</button>""")
# the monthly backup nudge rests while iCloud holds a copy from this week
rep("function backupDue(){const b=state.backup||{};",
    "function backupDue(){if(cloudOn()&&CS.avail!==false&&Date.now()-cloudAt()<7*864e5)return false;const b=state.backup||{};")

# ---- 3. privacy wording per platform
rep("""<div class="lbl2">Privacy</div><p class="muted small">Everything you do in Forgelings stays on this device. It has no accounts""",
    """<div class="lbl2">Privacy</div><p class="muted small">Everything you do in Forgelings stays on this device${cloudPlug()?', with a copy in your own iCloud if you keep that on. Forgelings can never see it':ANDROID?', and in Android\\u2019s own backup if that is on':''}. It has no accounts""")
rep("""<div class="tale"><b>Where it is kept</b><p>Only on this device, in this browser. Forgelings has no accounts""",
    """<div class="tale"><b>Where it is kept</b><p>${cloudPlug()?'On this device, and in your own iCloud unless you turn that off in Settings. The iCloud copy sits in your Apple account, where only you can reach it.':ANDROID?'On this device. If backup is on for this phone, Android also keeps a copy with your other apps, in your own Google account.':'Only on this device, in this browser.'} Forgelings has no accounts""")
rep("""<p>Use "Erase everything on this device" in Settings, or remove Forgelings and clear this site's data in your browser. There is no other copy anywhere.</p>""",
    """<p>${cloudPlug()?'Use "Erase everything" in Settings: it clears this device and the iCloud copy. Turning off the iCloud copy removes it from iCloud.':ANDROID?'Use "Erase everything on this device" in Settings, or remove Forgelings from your phone.':'Use "Erase everything on this device" in Settings, or remove Forgelings and clear this site\\'s data in your browser. There is no other copy anywhere.'}</p>""")
rep("const DOCS_DATE='October 20, 2026';","const DOCS_DATE='November 11, 2026';")

# ---- 2. Android back button: close what's open, then Today, then leave the app
rep("if(NATIVE)nrestore().then(boot,boot);else boot();",
"""if(NATIVE&&PL.App){try{PL.App.addListener('backButton',()=>{
  if(!modal.hidden){const s=modal.querySelector('.scrim'),c=[...modal.querySelectorAll('[data-close]')].find(x=>x.offsetParent!==null);
    if(c)c.click();else if(s&&s.dataset.dismiss==='true')closeModal();return;}
  if(tab!=='today'){const t=document.querySelector('.tab[data-tab="today"]');if(t){t.click();window.scrollTo(0,0);return;}}
  if(PL.App.minimizeApp)PL.App.minimizeApp();else if(PL.App.exitApp)PL.App.exitApp();
});}catch(e){}}
if(NATIVE)nrestore().then(boot,boot);else boot();""")

# ---- Android screen edges: Capacitor's SystemBars sets --safe-area-inset-* when the WebView's env() reports zero
for side in ('top','bottom'):
    a=f'env(safe-area-inset-{side},0px)'; c=S.count(a); assert c>0,side
    S=S.replace(a,f'max(env(safe-area-inset-{side},0px),var(--safe-area-inset-{side},0px))')

out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk52.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk52.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)

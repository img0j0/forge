# 0.49: two of the review's ideas (Hunter picked them, November 5).
# 1) The binder finds a Forgeling by name and filters by realm. Both live in the Filter sheet: a name field narrows the
#    binder as you type, and realm chips list only the realms you have found (Shade realms by their own names). One
#    predicate (bMatch) decides the binder, the Show count and the "Showing" line, so they cannot disagree; a filter
#    that matches nothing says so and offers Show all. A filtered page shows only its matches, with no "not yet"
#    placeholders (they meant unfound Forgelings, not the end of a search).
# 2) On the website in a browser tab (never in the iPhone app or once on the home screen), from the third Forgeling,
#    Today offers once to keep Forgelings on the home screen, because a browser can clear a site's data when it sits
#    unopened. On iPhone the home screen copy has its own storage, so the steps say to save a copy first and restore it
#    there. "It's on my home screen" ends it; "Not now" brings it back in a week.
import re,subprocess,os
S=open('base485.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.48.5'","const VERSION='prototype 0.49.0'")
rep("<title>Forgelings (prototype 0.48.5)</title>","<title>Forgelings (prototype 0.49.0)</title>")
rep("const SEEN_V=53;","const SEEN_V=54;")
rep("s.wantAsked=!!s.wantAsked;","s.wantAsked=!!s.wantAsked;if(typeof s.homeTip!=='string')s.homeTip='';")

# ---------- 1) binder: name and realm ----------
rep("  let list=state.cards.filter(c=>(bf.type==='all'||c.v===+bf.type)&&(bf.mood==='all'||(bf.mood==='dark')===c.dark)&&(!bf.fav||c.fav));",
    "  let list=state.cards.filter(bMatch);")
rep("const binderCount=()=>state.cards.filter(c=>(bf.type==='all'||c.v===+bf.type)&&(bf.mood==='all'||(bf.mood==='dark')===c.dark)&&(!bf.fav||c.fav)).length;",
"""const realmKey=c=>c.theme+'-'+(c.dark?1:0),realmLabel=k=>{const [t,d]=k.split('-').map(Number),T=THEMES[t];return T?(d?T.dark.name:T.name):'';};
const bMatch=c=>(bf.type==='all'||c.v===+bf.type)&&(bf.mood==='all'||(bf.mood==='dark')===c.dark)&&(!bf.fav||c.fav)&&(!bf.realm||bf.realm==='all'||bf.realm===realmKey(c))&&(!bf.q||((c.nick||'')+' '+c.name).toLowerCase().includes(bf.q.toLowerCase()));
const binderCount=()=>state.cards.filter(bMatch).length;
const showLabel=()=>{const n=binderCount();return n?`Show ${n} ${n===1?'Forgeling':'Forgelings'}`:'Nothing matches yet';};""")
rep("const filtN=()=>(bf.type!=='all'?1:0)+(bf.mood!=='all'?1:0)+(bf.fav?1:0);",
    "const filtN=()=>(bf.type!=='all'?1:0)+(bf.mood!=='all'?1:0)+(bf.fav?1:0)+(bf.realm&&bf.realm!=='all'?1:0)+(bf.q?1:0);")
rep("function filtText(){const p=[];if(bf.type!=='all'&&VECTORS[+bf.type])p.push(VECTORS[+bf.type].name);if(bf.mood!=='all')p.push(bf.mood==='dark'?'Dark':'Cute');if(bf.fav)p.push('favourites');return p.join(', ')+' only';}",
    "function filtText(){const p=[];if(bf.q)p.push(`names with “${bf.q}”`);if(bf.realm&&bf.realm!=='all')p.push(realmLabel(bf.realm));if(bf.type!=='all'&&VECTORS[+bf.type])p.push(VECTORS[+bf.type].name);if(bf.mood!=='all')p.push(bf.mood==='dark'?'Dark':'Cute');if(bf.fav)p.push('favourites');return p.join(', ')+' only';}")
rep("""  return `<h2>Filter your binder</h2><div class="lbl2">Calling</div>""",
"""  const rc={};state.cards.forEach(c=>{const k=realmKey(c);rc[k]=(rc[k]||0)+1;});
  const rks=Object.keys(rc).sort((a,b)=>{const [ta,da]=a.split('-').map(Number),[tb,db]=b.split('-').map(Number);return da-db||ta-tb;});
  return `<h2>Filter your binder</h2><div class="field"><label for="fName">Find by name</label><input id="fName" type="search" autocomplete="off" autocapitalize="words" enterkeyhint="done" maxlength="24" placeholder="A name or nickname" value="${esc(bf.q||'')}"></div>
    ${rks.length>1?`<div class="lbl2">Realm</div><div class="chips" role="group" aria-label="Filter by realm"><button class="chip" data-frealm="all" aria-pressed="${!bf.realm||bf.realm==='all'}">All</button>${rks.map(k=>`<button class="chip" data-frealm="${k}" aria-pressed="${bf.realm===k}">${esc(realmLabel(k))} ${rc[k]}</button>`).join('')}</div>`:''}
    <div class="lbl2">Calling</div>""")
rep("""    <div class="stack"><button class="primary" data-close>Show ${binderCount()} ${binderCount()===1?'Forgeling':'Forgelings'}</button></div>`;""",
    """    <div class="stack"><button class="primary" id="fShow" data-close>${showLabel()}</button></div>`;""")
rep("""  if(b.dataset.ftype!==undefined){bf.type=b.dataset.ftype;hit=true;}else if(b.dataset.fmood){bf.mood=b.dataset.fmood;hit=true;}else if(b.id==='fFav'){bf.fav=!bf.fav;hit=true;}""",
    """  if(b.dataset.ftype!==undefined){bf.type=b.dataset.ftype;hit=true;}else if(b.dataset.fmood){bf.mood=b.dataset.fmood;hit=true;}else if(b.dataset.frealm){bf.realm=b.dataset.frealm;hit=true;}else if(b.id==='fFav'){bf.fav=!bf.fav;hit=true;}""")
rep("""const f=modal.querySelector(b.id?'#'+b.id:b.dataset.ftype!==undefined?`[data-ftype="${b.dataset.ftype}"]`:`[data-fmood="${b.dataset.fmood}"]`);""",
    """const f=modal.querySelector(b.id?'#'+b.id:b.dataset.ftype!==undefined?`[data-ftype="${b.dataset.ftype}"]`:b.dataset.frealm?`[data-frealm="${b.dataset.frealm}"]`:`[data-fmood="${b.dataset.fmood}"]`);""")
rep("function openFilter(){openSheet(filterSheetHTML());}",
"""function openFilter(){openSheet(filterSheetHTML());}
/* 0.49: the name field narrows the binder as you type; the sheet stays put so the keyboard never drops */
document.addEventListener('input',e=>{if(!e.target||e.target.id!=='fName')return;bf.q=e.target.value.trim().slice(0,24);bf.page=0;renderBinder();const s=modal.querySelector('#fShow');if(s)s.textContent=showLabel();});
document.addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target&&e.target.id==='fName'){e.preventDefault();e.target.blur();}});""")
rep("  if(b.id==='fClear'){bf.type='all';bf.mood='all';bf.fav=false;bf.page=0;renderBinder();return;}",
    "  if(b.id==='fClear'){bf.type='all';bf.mood='all';bf.fav=false;bf.realm='all';bf.q='';bf.page=0;renderBinder();return;}")
rep("""    ${state.cards.length?'':'<p class="muted" style="margin:6px 0 12px">Your binder is empty. Turn over today\\u2019s card to find your first Forgeling.</p>'}""",
    """    ${state.cards.length?'':'<p class="muted" style="margin:6px 0 12px">Your binder is empty. Turn over today\\u2019s card to find your first Forgeling.</p>'}
    ${state.cards.length&&filtN()&&!list.length?'<p class="muted" style="margin:6px 0 12px">No Forgelings match this yet. Try another name, or show them all.</p>':''}""")

rep("for(let i=0;i<9;i++){const c=slice[i];slots.push(c?","for(let i=0;i<(filtN()?slice.length:9);i++){const c=slice[i];slots.push(c?")

# ---------- 2) Today: keep it on the home screen (website in a browser tab only) ----------
rep("""  if(backupDue())rows.push(row('btnBackup',IC.save,'Save a copy of your collection','It all lives on this phone. A copy once a month keeps it safe.'));""",
"""  if(backupDue())rows.push(row('btnBackup',IC.save,'Save a copy of your collection','It all lives on this phone. A copy once a month keeps it safe.'));
  if(homeTipDue())rows.push(row('btnHomeTip',IC.home,'Keep Forgelings on your home screen','A browser can clear a website\\u2019s saved data if it sits unopened for a while. On your home screen, your collection is kept.'));""")
rep("""    save:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v11M7.5 10l4.5 4.5 4.5-4.5"/><path d="M4 15v4a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-4"/></svg>'};""",
"""    save:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v11M7.5 10l4.5 4.5 4.5-4.5"/><path d="M4 15v4a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-4"/></svg>',
    home:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="6" y="2.5" width="12" height="19" rx="2.5"/><rect x="9" y="6" width="2.5" height="2.5" rx=".6"/><rect x="12.5" y="6" width="2.5" height="2.5" rx=".6"/><rect x="9" y="9.5" width="2.5" height="2.5" rx=".6"/><path d="M10.5 18h3"/></svg>'};""")
rep("  if(b.id==='btnBackup'){openBackupNudge();return;}","  if(b.id==='btnBackup'){openBackupNudge();return;}\n  if(b.id==='btnHomeTip'){openHomeTip();return;}")
rep("function openFilter(){openSheet(filterSheetHTML());}","""function openFilter(){openSheet(filterSheetHTML());}
/* 0.49: keep Forgelings on the home screen. Only on the website in a browser tab, from the third Forgeling, until done. */
const IOSDEV=()=>/iPhone|iPad|iPod/.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
function homeTipDue(){return RELEASE&&!NATIVE&&!STANDALONE()&&state.cards.length>=3&&state.homeTip!=='done'&&!(state.homeTip&&state.homeTip>todayKey());}
function openHomeTip(){
  const ios=IOSDEV();
  openSheet(`<h2>Keep Forgelings on your home screen</h2><p class="muted">On the home screen it opens like an app, works offline, and your collection is kept. In a browser tab, the browser may clear a website\\u2019s data if it sits unopened for a while.</p>
    ${ios?`<ol class="htsteps"><li><b>Save a copy first.</b> On iPhone, the home screen app keeps its own collection, so you will bring yours across.</li><li>In Safari, tap the <b>Share</b> button, then <b>Add to Home Screen</b>, then <b>Add</b>.</li><li>Open Forgelings from your home screen, go to <b>Settings</b>, then <b>Your collection</b>, and tap <b>Restore a copy</b>.</li></ol>`
    :`<ol class="htsteps"><li>Open your browser\\u2019s menu and tap <b>Install app</b> or <b>Add to Home screen</b>.</li><li>Open Forgelings from your home screen. Your collection comes with it.</li></ol>`}
    <div class="stack">${ios?'<button class="primary" id="htSave">Save a copy first</button>':''}<button class="${ios?'outline':'primary'}" id="htDone">It\\u2019s on my home screen</button><button class="ghost" id="htLater">Not now</button></div>`);
}
modal.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('#htSave,#htDone,#htLater');if(!b)return;
  if(b.id==='htSave'){closeModal();openExport();return;}
  if(b.id==='htDone')state.homeTip='done';else{const d=new Date(state.date+'T12:00:00');d.setDate(d.getDate()+7);state.homeTip=dkey(d);}
  save();closeModal();renderToday();});""")

CSS='''
/* 0.49: the home-screen steps */
.htsteps{margin:10px 0 14px;padding-left:22px;display:grid;gap:8px;text-align:left}
.htsteps li{line-height:1.45}
'''
i=S.index("</style>",S.index("</style>")+1); S=S[:i]+CSS+S[i:]
rep("""<ul class="newlist"><li><b>Ink and paper, moving.</b>""","""<ul class="newlist"><li><b>Find any Forgeling.</b> The binder's Filter has a name search and a realm filter, so a Forgeling from months ago is a few letters away. On the website, Today now offers once to keep Forgelings on your home screen, where your collection is kept safe.</li><li><b>Ink and paper, moving.</b>""")
m=re.search(r'<ul class="newlist">(.*?)</ul>',S,re.S); items=re.findall(r'<li>.*?</li>',m.group(1),re.S)
assert len(items)==9,len(items); rep(items[-1],"")
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk49.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk49.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)

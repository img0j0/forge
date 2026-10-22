# Forgelings 0.29.0: gift links. Send a curio to a friend as a link; it opens in their own app.
# No server: everything rides in the link's #fragment, which browsers never send to the host. The link holds only the
# curio, the sending Forgeling's name and look, an optional note, and random ids that stop double-opening.
# Opening your own link does nothing but say so. A new player sees the gift waiting on the title screen and gets it
# after their first Forgeling. Reads base281.html.
src = open('base281.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

rep('/* Nav */', '''.gpick{display:grid;grid-template-columns:repeat(auto-fill,minmax(92px,1fr));gap:8px;margin:8px 0}
.gpick button{min-height:64px;border-radius:12px;border:2px solid var(--line);background:var(--surface);color:var(--ink);font:600 13px var(--display);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;padding:6px}
.gpick button .gl{font-size:24px;line-height:1}
.gpick button[aria-pressed="true"]{border-color:var(--plum);background:var(--chip)}
.giftcard{text-align:center}
.giftcard .gfrom{display:flex;align-items:center;justify-content:center;gap:10px;margin:6px 0 2px}
.giftcard .gfrom img{width:64px;height:64px;image-rendering:pixelated}
.giftcard .gcur{font-size:52px;line-height:1.1;margin:8px 0 0}
.giftnote{margin:10px 0 0;font:600 15px var(--display);color:#3B2E6E;background:rgba(255,246,207,.85);border-radius:12px;padding:8px 12px;display:inline-block}
/* Nav */''')

GIFT_JS = r'''/* ---- 0.29: gift links. A curio travels to a friend inside a link; nothing is stored anywhere else. ---- */
const GIFT_BASE='https://img0j0.github.io/forge/',GIFT_KEY='forge-gift-in';
const b64u={enc:s=>btoa(unescape(encodeURIComponent(s))).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,''),
  dec:s=>decodeURIComponent(escape(atob(s.replace(/-/g,'+').replace(/_/g,'/'))))};
const rid=()=>{let s='';const a='abcdefghijklmnopqrstuvwxyz0123456789';for(let i=0;i<12;i++)s+=a[Math.floor(Math.random()*36)];return s;};
function giftCheck(o){
  if(!o||typeof o!=='object'||o.v!==1)return null;
  const ok=(x,re)=>typeof x==='string'&&re.test(x),int=(x,lo,hi)=>Number.isInteger(x)&&x>=lo&&x<=hi;
  if(!ok(o.g,/^[a-z0-9]{6,24}$/)||!ok(o.s,/^[a-z0-9]{6,24}$/)||!CURIOS.some(c=>c.id===o.c))return null;
  if(typeof o.n!=='string'||!o.n.trim()||o.n.length>24||!int(o.t,0,4)||!int(o.d,0,1)||!int(o.r,0,4)||!int(o.e,0,4294967295)||!int(o.k,0,11))return null;
  if(o.m!==undefined&&(typeof o.m!=='string'||o.m.length>80))return null;
  return {v:1,g:o.g,s:o.s,c:o.c,n:o.n.trim(),t:o.t,d:o.d,r:o.r,e:o.e,k:o.k,m:(o.m||'').trim()};
}
function giftRead(){
  const h=location.hash||'';const m=h.match(/^#gift=([A-Za-z0-9_-]{10,1200})$/);
  if(m){let g=null;try{g=giftCheck(JSON.parse(b64u.dec(m[1])));}catch(e){}
    if(g){try{localStorage.setItem(GIFT_KEY,JSON.stringify(g));}catch(e){}}
    else if(state&&state.ageBand)setTimeout(()=>toast('That gift link looks broken. Ask your friend to send it again.'),900);}
  if(h.startsWith('#gift=')){try{history.replaceState(null,'',location.pathname+location.search);}catch(e){}}
}
function giftPending(){let g=null;try{g=giftCheck(JSON.parse(localStorage.getItem(GIFT_KEY)||'null'));}catch(e){}return g;}
const giftClear=()=>{try{localStorage.removeItem(GIFT_KEY);}catch(e){}};
const giftSender=g=>({id:-1,seed:g.e,rarity:g.r,dark:!!g.d,theme:g.t,v:g.k,keep:'',bond:0,name:g.n,nick:''});
function giftMaybe(){
  if(!state||!state.ageBand||!state.onboarded||!state.cards.length||!modal.hidden||rv||pk)return;
  const g=giftPending();if(!g)return;
  setTimeout(()=>{if(modal.hidden&&!rv&&!pk&&giftPending())openGiftIn(giftPending());},700);
}
function openGiftIn(g){
  if(!g)return;$('#toast').classList.remove('show');const cu=CURIOS.find(x=>x.id===g.c),n=esc(g.n),img=spriteURL(giftSender(g));
  if(g.s===state.sid){giftClear();openSheet(`<h2>This is your own gift</h2><p class="muted">Gift links are for friends. Send this one to someone, and it will open in their Forgelings.</p><div class="stack"><button class="primary" data-close>Got it</button></div>`);return;}
  if((state.giftsGot||[]).includes(g.g)){giftClear();openSheet(`<h2>Already opened</h2><p class="muted">You opened this gift from ${n} before. It is on your curio shelf.</p><div class="stack"><button class="primary" data-close>Got it</button></div>`);return;}
  openSheet(`<div class="giftcard"><p class="muted small" style="margin:0">A gift from a friend</p>
    <div class="gfrom">${img?`<img src="${img}" alt="${n}, the Forgeling who sent it">`:''}<h2 style="margin:0">${n} sent you something</h2></div>
    <p class="gcur" aria-hidden="true">${cu.g}</p><p style="margin:0"><b>${esc(cu.name)}</b></p>
    ${g.m?`<p class="giftnote">“${esc(g.m)}”</p>`:''}</div>
    <div class="stack" style="margin-top:14px"><button class="primary" id="giftKeep">Put it on my shelf</button></div>`);
}
function giftKeep(){
  const g=giftPending();if(!g){closeModal();return;}
  const cu=CURIOS.find(x=>x.id===g.c),isNew=!state.curios[cu.id];
  const cur=state.curios[cu.id]||{n:0,cid:0,at:todayKey(),gift:1};cur.n++;state.curios[cu.id]=cur;
  state.giftsGot=(state.giftsGot||[]).concat(g.g).slice(-200);giftClear();save();sfx('save');chime(2);
  const have=Object.keys(state.curios).length;
  openSheet(`<h2>${esc(cu.name)} is on your shelf</h2><p class="muted">${isNew?'A new curio, from '+esc(g.n)+'.':'You had one already. Now you have a spare, from '+esc(g.n)+'.'} Curios found: ${have} of ${CURIOS.length}.</p>
    ${isNew?talePageHTML(cu.id):''}<p class="muted small">Want to send one back? Open the curio shelf at the Hearth.</p><div class="stack"><button class="primary" data-close>Lovely</button></div>`);
  renderHearth();renderChronicle();
}
let gs={cid:0,cur:''};
function openGiftSend(c){
  const own=CURIOS.filter(x=>state.curios[x.id]);if(!own.length){toast('Find a curio first. Send a Forgeling wandering.');return;}
  const cs=slotCards().filter(x=>!(wOut()&&state.wander.id===x.id));if(!cs.length){toast('Everyone is out wandering. Try again when they are back.');return;}
  if(!cs.some(x=>x.id===gs.cid))gs.cid=(c&&cs.some(x=>x.id===c.id)?c:cs[0]).id;if(!own.some(x=>x.id===gs.cur))gs.cur=own[0].id;
  const who=cs.length>1?`<div class="lbl2">Who sends it</div><div class="gwho" role="group" aria-label="Who sends it">${cs.map(x=>{const u=spriteURL(x);return `<button data-gsw="${x.id}" aria-pressed="${x.id===gs.cid}">${u?`<img src="${u}" alt="">`:''}${esc(x.nick||x.name)}</button>`;}).join('')}</div>`:'';
  openSheet(`<h2>Send a curio to a friend</h2><p class="muted small">Your friend gets a link that opens in their own Forgelings, and the curio goes on their shelf. You keep yours.</p>
    ${who}<div class="lbl2">Which curio</div><div class="gpick" role="group" aria-label="Which curio">${own.map(x=>`<button data-gcur="${x.id}" aria-pressed="${x.id===gs.cur}"><span class="gl" aria-hidden="true">${x.g}</span>${esc(x.name)}</button>`).join('')}</div>
    <label class="field"><span>A short note (optional)</span><input id="giftNote" maxlength="80" autocomplete="off" placeholder="For example: this made me think of you"></label>
    <p class="muted small">The link holds only the curio, your Forgeling’s name and look, and your note. It goes only where you send it.</p>
    <div class="stack"><button class="primary" id="giftGo">Send the link</button></div><div class="row" style="justify-content:center"><button class="ghost" data-close>Not now</button></div>`);
}
function giftSend(){
  const c=cardById(gs.cid),cu=CURIOS.find(x=>x.id===gs.cur);if(!c||!cu)return;
  if(!state.sid){state.sid=rid();}
  const note=(($('#giftNote')||{}).value||'').trim().slice(0,80),n=(c.nick||c.name).slice(0,24);
  const g={v:1,g:rid(),s:state.sid,c:cu.id,n,t:c.theme,d:c.dark?1:0,r:c.rarity,e:c.seed>>>0,k:c.v};if(note)g.m=note;
  const url=GIFT_BASE+'#gift='+b64u.enc(JSON.stringify(g));
  state.giftsSent=(state.giftsSent||0)+1;save();closeModal();
  shareOrCopy(`${n} found a ${cu.name.toLowerCase()} and wants you to have it. Open it in Forgelings: ${url}`,'Gift link copied. Paste it to your friend.','A gift from '+n);
  hf.msg=`${n} wraps up the ${cu.name.toLowerCase()} and sends it off.`;renderHearth();setTimeout(checkRibbons,600);
}
'''
rep("function wPanelHTML(c,n){", GIFT_JS + "function wPanelHTML(c,n){")
# the shelf gets a Send button
rep("""<details class="more"><summary>Curio shelf, ${have} of ${CURIOS.length}</summary>${shelf}</details></div>`;""",
    """<details class="more"><summary>Curio shelf, ${have} of ${CURIOS.length}</summary>${shelf}${have?'<button class="outline" id="hGift" style="margin-top:10px">Send a curio to a friend</button>':''}</details></div>`;""")
rep("""  if(b.dataset.mecho&&c){""", """  if(b.id==='hGift'){openGiftSend(c);return;}
  if(b.dataset.mecho&&c){""")
# sheet buttons (modal clicks)
rep("""  else if(b.id==='fdHearth'){""", """  else if(b.id==='giftKeep')giftKeep();
  else if(b.id==='giftGo')giftSend();
  else if(b.dataset.gsw!==undefined){gs.cid=+b.dataset.gsw;modal.querySelectorAll('[data-gsw]').forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false'));}
  else if(b.dataset.gcur!==undefined){gs.cur=b.dataset.gcur;modal.querySelectorAll('[data-gcur]').forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false'));}
  else if(b.id==='fdHearth'){""")
# after any sheet closes, a waiting gift gets its turn
rep("setTimeout(()=>{if(state&&state.ageBand)checkRibbons();},350);}", "setTimeout(()=>{if(state&&state.ageBand){checkRibbons();giftMaybe();}},350);}")
# read the link at start, and if one arrives while open
rep("  if(!state.ageBand)openAgeGate();else if(!state.onboarded)openVector();else if(state.seen<SEEN_V){state.seen=SEEN_V;save();openWhatsNew();}",
    "  giftRead();\n  if(!state.ageBand)openAgeGate();else if(!state.onboarded)openVector();else if(state.seen<SEEN_V){state.seen=SEEN_V;save();openWhatsNew();}\n  setTimeout(giftMaybe,1200);window.addEventListener('hashchange',()=>{giftRead();giftMaybe();});")
# the title screen mentions a waiting gift
rep('<p class="tagline">One small thing a day.<br>A small creature to keep it.</p></div>',
    '<p class="tagline">One small thing a day.<br>A small creature to keep it.</p>${(()=>{const g=giftPending();return g?`<p class="giftnote" id="titleGift">${esc(g.n)} sent you a gift. Begin, and it will be waiting.</p>`:\'\';})()}</div>')
# a blocked visitor keeps nothing
rep("function showBlocked(){", "function showBlocked(){\n  giftClear();")
# save repair
rep("""  if(s.mEchoed!==undefined&&!Array.isArray(s.mEchoed))s.mEchoed=[];""",
    """  if(s.mEchoed!==undefined&&!Array.isArray(s.mEchoed))s.mEchoed=[];
  if(s.sid!==undefined&&!(typeof s.sid==='string'&&/^[a-z0-9]{6,24}$/.test(s.sid)))delete s.sid;
  if(s.giftsGot!==undefined)s.giftsGot=Array.isArray(s.giftsGot)?s.giftsGot.filter(x=>typeof x==='string').slice(-200):[];
  if(s.giftsSent!==undefined&&!(Number.isInteger(s.giftsSent)&&s.giftsSent>=0))s.giftsSent=0;""")
# ribbons
rep("  {id:'tales5',name:'Keeper of Old Tales',desc:'Make all five old tales whole.',g:5,f:()=>talesDone()},",
    "  {id:'tales5',name:'Keeper of Old Tales',desc:'Make all five old tales whole.',g:5,f:()=>talesDone()},\n  {id:'gift1',name:'Kind Gesture',desc:'Send a curio to a friend.',g:1,f:()=>state.giftsSent||0},\n  {id:'giftgot',name:'Well Loved',desc:'Open a gift from a friend.',g:1,f:()=>(state.giftsGot||[]).length},")
# privacy note
rep("""<div class="tale"><b>When you choose to share</b><p>"Save a copy" and "Send my report" create text that goes only where you put it, for example a message to the person testing Forgelings with you.</p></div>""",
    """<div class="tale"><b>When you choose to share</b><p>"Save a copy", "Send my report" and gift links create something that goes only where you put it, for example a message to a friend. A gift link holds only the curio, your Forgeling’s name and look, and your note, and the part of the link that holds them is never sent to the website.</p></div>""")

rep('<title>Forgelings (prototype 0.28.1)</title>', '<title>Forgelings (prototype 0.29.0)</title>')
rep("const VERSION='prototype 0.28.1';", "const VERSION='prototype 0.29.0';")
rep('const SEEN_V=33;', 'const SEEN_V=34;')

rep("""<ul class="newlist"><li><b>A new name: Forgelings.</b>""",
    """<ul class="newlist"><li><b>Gifts for friends.</b> Send a curio to a friend from the curio shelf at the Hearth. They get a link that opens in their own Forgelings, and the curio goes on their shelf. You keep yours.</li>
    <li><b>A new name: Forgelings.</b>""")
import re as _re
_i=src.index('<ul class="newlist">'); _j=src.index('</ul>',_i)
_items=_re.findall(r'\s*<li>.*?</li>',src[_i+len('<ul class="newlist">'):_j],_re.S)
src=src[:_i]+'<ul class="newlist">'+''.join(_items[:10])+src[_j:]
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src))

# 0.61: visiting a friend's fire (Hunter, November 12: "Please prioritize and execute the additions"; fourth of five).
#   At the Hearth, "Send <name> to visit a friend" makes a link. When the friend opens it, your Forgeling comes to sit
#   by their fire until the end of the next day, with your note if you wrote one: it appears on their Hearth photo, and
#   tapping it says hello. Nothing is compared or counted, and there are no accounts: the link holds only the
#   Forgeling's name and look and the note, like gift links. Your own Forgeling stays home. One visitor at a time; a
#   visit already received doesn't come twice; your own link tells you it is yours.
import re,subprocess,os
S=open('base60.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.60.0'","const VERSION='prototype 0.61.0'")
rep("<title>Forgelings (prototype 0.60.0)</title>","<title>Forgelings (prototype 0.61.0)</title>")

rep("function giftRead(){","""/* ================= 0.61: visiting a friend's fire ================= */
const VISIT_KEY='forge-visit-in';
function visitCheck(o){
  if(!o||typeof o!=='object'||o.v!==1)return null;
  const ok=(x,re)=>typeof x==='string'&&re.test(x),int=(x,lo,hi)=>Number.isInteger(x)&&x>=lo&&x<=hi;
  if(!ok(o.g,/^[a-z0-9]{6,24}$/)||!ok(o.s,/^[a-z0-9]{6,24}$/))return null;
  if(typeof o.n!=='string'||!o.n.trim()||o.n.length>24||!int(o.t,0,4)||!int(o.d,0,1)||!int(o.r,0,4)||!int(o.e,0,4294967295)||!int(o.k,0,11))return null;
  if(o.m!==undefined&&(typeof o.m!=='string'||o.m.length>80))return null;
  if(o.p!==undefined&&!stKeepOK(o.p))return null;
  const out={v:1,g:o.g,s:o.s,n:o.n.trim(),t:o.t,d:o.d,r:o.r,e:o.e,k:o.k,m:(o.m||'').trim(),p:o.p||''};if(o.w===2)out.w=2;return out;}
const nmJ=x=>typeof LANG!=='undefined'&&LANG==='ja'?kanaName(x):x;
const visitCard=v=>({id:-2,seed:v.e,rarity:v.r,dark:!!v.d,theme:v.t,v:v.k,keep:v.p||'',bond:0,name:nmJ(v.n),nick:'',...(v.w===2?{gen:2}:{})});
function visitRead(){
  const h=location.hash||'';const m=h.match(/^#visit=([A-Za-z0-9_-]{10,1000})$/);
  if(m){let v=null;try{v=visitCheck(JSON.parse(b64u.dec(m[1])));}catch(e){}
    if(v){try{localStorage.setItem(VISIT_KEY,JSON.stringify(v));}catch(e){}}
    else setTimeout(()=>toast('That visit link looks broken. Ask your friend to send it again.'),900);}
  if(h.startsWith('#visit=')){try{history.replaceState(null,'',location.pathname+location.search);}catch(e){}}}
function visitPending(){let v=null;try{v=visitCheck(JSON.parse(localStorage.getItem(VISIT_KEY)||'null'));}catch(e){}return v;}
const visitClear=()=>{try{localStorage.removeItem(VISIT_KEY);}catch(e){}};
const visitorNow=()=>{const v=state&&state.visitor;return v&&visitCheck(v)&&typeof v.until==='string'&&todayKey()<=v.until?v:null;};
function visitMaybe(){
  if(!state||!state.ageBand||!state.onboarded||!state.cards.length||!modal.hidden||rv||pk)return;
  if(!visitPending())return;
  setTimeout(()=>{if(modal.hidden&&!rv&&!pk&&visitPending())openVisitIn(visitPending());},700);}
function openVisitIn(v){
  if(!v)return;const n=esc(nmJ(v.n)),img=spriteURL(visitCard(v));
  if(v.s===state.sid){visitClear();openSheet(`<h2>This is your own visit link</h2><p class="muted">Visit links are for friends. Send this one to someone, and ${n} will visit their fire.</p><div class="stack"><button class="primary" data-close>Got it</button></div>`);return;}
  if((state.visitsGot||[]).includes(v.g)){visitClear();openSheet(`<h2>${n} has visited already</h2><p class="muted">This visit came by before. Ask your friend for a new link if they would like ${n} to come again.</p><div class="stack"><button class="primary" data-close>Got it</button></div>`);return;}
  const cur=visitorNow();
  openSheet(`<div class="giftcard"><p class="muted small" style="margin:0">A visitor from a friend's fire</p>
    <div class="gfrom">${img?`<img src="${img}" alt="${esc(flDesc(visitCard(v)))}">`:''}<h2 style="margin:0">${n} would like to sit by your fire</h2></div>
    ${v.m?`<p class="mine">\\u201C${esc(v.m)}\\u201D</p>`:''}<p class="muted small">${n} can stay until the end of tomorrow. Nothing is shared back: your fire stays yours.</p>
    ${cur?`<p class="muted small">${esc(nmJ(cur.n))} is visiting now, and will head home so ${n} can sit down.</p>`:''}</div>
    <div class="stack" style="margin-top:12px"><button class="primary" id="visitYes">Welcome ${n}</button><button class="ghost" id="visitNo">Not this time</button></div>`);}
function visitAccept(yes){
  const v=visitPending();visitClear();if(!v){closeModal();return;}
  state.visitsGot=(state.visitsGot||[]).concat(v.g).slice(-200);
  if(yes){const d=new Date(todayKey()+'T12:00:00');d.setDate(d.getDate()+1);state.visitor=Object.assign({},v,{until:dkey(d),at:todayKey()});
    state.visitsIn=(state.visitsIn||0)+1;hf.msg=`${nmJ(v.n)} has come from a friend's fire, and sits down by yours.`;}
  save();closeModal();if(yes){tab='hearth';render();window.scrollTo(0,0);}else renderHearth();}
const VISIT_HI=['{n} waves a little paw. It is nice to be somewhere new.','{n} looks around your fire and seems to approve.','{n} says your Forgelings are very good company.','{n} warms their paws, and hums.'];
const VISIT_HI_D=['{n} nods once. Your fire passes inspection.','{n} settles in, and keeps an eye on the dark for you.','{n} rumbles something friendly.'];
function visitorHTML(){const v=visitorNow();if(!v)return '';const c=visitCard(v),u=spriteURL(c);if(!u)return '';
  return `<button class="visitor" id="hVisitor" aria-label="${esc(nmJ(v.n))} is visiting from a friend's fire. Say hello"><img src="${u}" alt=""><span aria-hidden="true">${esc(nmJ(v.n))}</span></button>`;}
function openVisitor(){const v=visitorNow();if(!v)return;const n=esc(nmJ(v.n)),c=visitCard(v),L=v.d?VISIT_HI_D:VISIT_HI,line=L[whash(dnum(todayKey())+v.e%997)%L.length].replace(/\\{n\\}/g,nmJ(v.n));
  openSheet(`<div class="giftcard"><div class="gfrom"><img src="${spriteURL(c)}" alt="${esc(flDesc(c))}"><h2 style="margin:0">${n} is visiting</h2></div>
    <p>${esc(line)}</p>${v.m?`<p class="mine">\\u201C${esc(v.m)}\\u201D</p>`:''}<p class="muted small">${n} came from a friend's fire on ${esc(dateLabel(v.at||todayKey()))}, and heads home after ${esc(dateLabel(v.until))}.</p></div>
    <div class="stack" style="margin-top:12px"><button class="primary" data-close>Lovely</button><button class="ghost" id="visitBye">Say goodbye now</button></div>`);}
function openVisitSend(c){
  if(!c)return;const n=esc(c.nick||c.name);
  openSheet(`<h2>Send ${n} to visit a friend</h2><p class="muted small">Your friend gets a link. When they open it in their Forgelings, ${n} comes to sit by their fire until the end of the next day. ${n} also stays here with you.</p>
    <label class="field"><span>A short note (optional)</span><input id="visitNote" maxlength="80" autocomplete="off" placeholder="For example: thinking of you today"></label>
    <p class="muted small">The link holds only ${n}'s name and look, and your note. It goes only where you send it.</p>
    <div class="stack"><button class="primary" id="visitGo" data-cid="${c.id}">Send the link</button></div><div class="row" style="justify-content:center"><button class="ghost" data-close>Not now</button></div>`);}
function visitSend(c){
  if(!c)return;if(!state.sid)state.sid=rid();
  const note=(($('#visitNote')||{}).value||'').trim().slice(0,80),n=(c.nick||c.nameEn||c.name).slice(0,24);
  const v={v:1,g:rid(),s:state.sid,n,t:c.theme,d:c.dark?1:0,r:c.rarity,e:c.seed>>>0,k:c.v};if(c.gen===2)v.w=2;if(c.keep&&stKeepOK(c.keep))v.p=c.keep;if(note)v.m=note;
  const url=GIFT_BASE+'#visit='+b64u.enc(JSON.stringify(v));
  state.visitsSent=(state.visitsSent||0)+1;save();closeModal();
  shareOrCopy(`${c.nick||c.name} would like to visit your fire in Forgelings. Open this to let them in: ${url}`,'Visit link copied. Paste it to your friend.',(c.nick||c.name)+' would like to visit');
  hf.msg=`${c.nick||c.name} packs a little bag, ready to visit.`;renderHearth();}
function giftRead(){""")

# startup and hash changes read visit links too; the arrival sheet waits its turn like gifts
rep("""  giftRead();statueLinkRead();
  if(loadBad)""","""  giftRead();statueLinkRead();visitRead();
  if(loadBad)""")
rep("""  if(!loadBad){setTimeout(giftMaybe,1200);setTimeout(statueLinkMaybe,1300);}window.addEventListener('hashchange',()=>{giftRead();giftMaybe();statueLinkRead();statueLinkMaybe(!state.ageBand);});""",
"""  if(!loadBad){setTimeout(giftMaybe,1200);setTimeout(statueLinkMaybe,1300);setTimeout(visitMaybe,1500);}window.addEventListener('hashchange',()=>{giftRead();giftMaybe();statueLinkRead();statueLinkMaybe(!state.ageBand);visitRead();visitMaybe();});""")
rep("""setTimeout(()=>{if(state&&state.ageBand){checkRibbons();giftMaybe();}},350);}""","""setTimeout(()=>{if(state&&state.ageBand){checkRibbons();giftMaybe();visitMaybe();}},350);}""")

# the Hearth: the visitor on the photo, and the button to send one
rep("""role="img" aria-label="Your Forgelings sitting around a campfire"></canvas>${seasonFX()}</div>""","""role="img" aria-label="Your Forgelings sitting around a campfire"></canvas>${seasonFX()+visitorHTML()}</div>""")
rep("""<button class="chip" id="hChange">Change who is here</button></div>`;""","""<button class="chip" id="hChange">Change who is here</button>${c?`<button class="chip" id="hVisit">Send ${esc(n)} to visit a friend</button>`:''}</div>`;""")
rep("""  if(b.id==='hGift'){openGiftSend(c);return;}""","""  if(b.id==='hGift'){openGiftSend(c);return;}
  if(b.id==='hVisit'){openVisitSend(c);return;}
  if(b.id==='hVisitor'){openVisitor();return;}""")
# sheet buttons (in #modal)
rep("""  else if(b.id==='yearPic')yearPicture();""","""  else if(b.id==='yearPic')yearPicture();
  else if(b.id==='visitYes')visitAccept(true);
  else if(b.id==='visitNo')visitAccept(false);
  else if(b.id==='visitGo')visitSend(cardById(+b.dataset.cid));
  else if(b.id==='visitBye'){const v=visitorNow();if(v){hf.msg=`${nmJ(v.n)} waves goodbye and heads home.`;state.visitor=null;save();}closeModal();renderHearth();}""")
# 0.57.1 sent katakana names in gift and statue links from a phone in Japanese; links carry the Latin name, and a
# phone in Japanese shows a sender's name in katakana
n0=S.count("(c.nick||c.name).slice(0,24)");assert n0==2,n0
S=S.replace("(c.nick||c.name).slice(0,24)","(c.nick||c.nameEn||c.name).slice(0,24)")
rep("const giftSender=g=>({id:-1,seed:g.e,rarity:g.r,dark:!!g.d,theme:g.t,v:g.k,keep:'',bond:0,name:g.n,","const giftSender=g=>({id:-1,seed:g.e,rarity:g.r,dark:!!g.d,theme:g.t,v:g.k,keep:'',bond:0,name:nmJ(g.n),")
rep("cu=fr?null:cuById(g.c),n=esc(g.n),","cu=fr?null:cuById(g.c),n=esc(nmJ(g.n)),")
# the save
rep("""  if(s.seasons!==undefined){""","""  if(s.visitor!==undefined&&s.visitor!==null){const v=visitCheck(s.visitor);s.visitor=v&&typeof s.visitor.until==='string'&&/^\\d{4}-\\d{2}-\\d{2}$/.test(s.visitor.until)?Object.assign(v,{until:s.visitor.until,at:typeof s.visitor.at==='string'?s.visitor.at:s.visitor.until}):null;}
  if(s.visitsGot!==undefined&&!(Array.isArray(s.visitsGot)&&s.visitsGot.every(x=>typeof x==='string')))s.visitsGot=[];
  if(s.seasons!==undefined){""")

css="""
/* 0.61: a visitor on the Hearth photo */
.visitor{position:absolute;left:5%;bottom:9%;width:21%;min-width:44px;min-height:44px;z-index:2;background:none;border:0;padding:0;cursor:pointer;display:flex;flex-direction:column;align-items:center}
.visitor img{width:100%;image-rendering:pixelated;filter:drop-shadow(0 2px 0 rgba(0,0,0,.25))}
.visitor span{font:700 11px/1.2 var(--body);background:rgba(255,248,230,.92);color:#2E2A47;padding:1px 6px;border-radius:8px;margin-top:-4px;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.visitor:focus-visible{outline:3px solid #FFD36B;outline-offset:2px}
html:not(.reduce) .visitor img{animation:vbob 2.4s ease-in-out infinite}
@keyframes vbob{0%,100%{transform:translateY(0)}50%{transform:translateY(-2px)}}
"""
i=S.rindex("</style>",0,S.index("<body")); S=S[:i]+css+S[i:]

out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk61.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk61.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)

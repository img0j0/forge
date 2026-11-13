# 0.75: one book, in chapters (design doc https://claude.ai/artifact/P9KAXd64JbAGFALG1KTwvk, "Forgelings: a journal worth
#   keeping"; Hunter, November 13: "I love it. Also let's go with your recommendations").
#   - The book is one reader (`openBook`, `bookPages`): a cover with the bookplate, the contents, then a chapter per month
#     (oldest first): its title page, its days, its closing page; and the back (letters, Your year, an old page).
#     The monthly books of 0.71 are now its chapters; the Journal's "Monthly books" button is "Open your book".
#   - Chapter title pages: "Chapter n", a name the month earns (`chInfo`: the first month is "Where it began"; a month
#     with a season stamp takes the season's name; otherwise the realm your answers leaned to most, three names each,
#     picked by the month), the month's closest Forgeling ("Named by ..."), the realm's colour as a wash, the stamp.
#   - Every day is a spread: the date, the calling as a red stamp, the day's Forgeling taped in as a print, the photo
#     postcard; then the day's page in world ink and your words. Side by side from 700 px wide, stacked on a phone.
#   - The ribbon remembers: `state.bookAt` is the page you were on (a key such as d:2026-12-15, so new pages never move
#     it); "Open your book" opens there, else at the contents. Contents lists the chapters newest first.
#   - Page turns: Back and Next, a swipe, or the arrow keys; a short turn (`bkIn`, 260 ms) that reduced motion skips.
#   - The book's paper keeps its own ink at night; your words are handwritten. Fixed in passing (0.71): the month's
#     words glued the feeling's save key ("Most days felt good", 「good」 in Japanese); now whole sentences.
import re,subprocess,os
S=open('base74.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.74.0'","const VERSION='prototype 0.75.0'")
rep("<title>Forgelings (prototype 0.74.0)</title>","<title>Forgelings (prototype 0.75.0)</title>")
# --- the book ---
rep("function zinesHTML(){const M=zineMonths();","""/* ================= 0.75: one book, in chapters ================= */
const CH_FIRST='Where it began',CH_ANY='A month by the fire';
const CH_SEASON={lantern:'The lanterns came back',blossom:'The month of petals',firefly:'Firefly evenings',star:'A month of wishes',moon:'Under the harvest moon',maple:'When the maples turned',snow:'The month of first snow'};
const CH_LEAN=[['A month of good company','Friends by the fire','The month of open doors'],['The month of making','Sparks and small projects','Hands always busy'],['A slower month','The month of rest','Low tide, easy days'],['A clear-headed month','The month of quiet focus','Clear skies'],['A dreaming month','The month of far-off thoughts','Lanterns in the dark']];
const CH_WASH=['#B5DDB5','#FFB27A','#8CC7F0','#CFE0F5','#C9B8FF'];
const chMonths=()=>zineMonths().slice().reverse();
function chLean(ym){const n=[0,0,0,0,0];let any=0;
  zineDays(ym).forEach(k=>{const a=askAns(k);if(a&&a[2]>=0&&a[2]<=4){n[a[2]]++;any++;}});
  if(!any)state.cards.forEach(c=>{if(typeof c.date==='string'&&c.date.slice(0,7)===ym&&c.theme>=0&&c.theme<5){n[c.theme]++;any++;}});
  return any?n.indexOf(Math.max(...n)):-1;}
function chSeason(ym){const S2=state.seasons||{};return SEASONS.find(s=>Object.keys(S2).some(k=>k.indexOf(s.id+'-')===0&&String(S2[k]).slice(0,7)===ym))||null;}
function chInfo(ym){const M=chMonths(),i=M.indexOf(ym),r=chLean(ym),s=chSeason(ym);let h=7;for(const ch of ym)h=(h*31+ch.charCodeAt(0))>>>0;
  const name=i===0?CH_FIRST:s?CH_SEASON[s.id]:r>=0?CH_LEAN[r][h%3]:CH_ANY;
  const c=state.cards.filter(x=>typeof x.date==='string'&&x.date.slice(0,7)===ym).sort((a,b)=>(b.bond||0)-(a.bond||0)||a.id-b.id)[0]||null;
  return {n:i+1,name,r,s,c};}
function bookPages(){const P=[{k:'c'},{k:'t'}];chMonths().forEach(ym=>{P.push({k:'ch',ym});zineDays(ym).forEach(d=>P.push({k:'d',d}));P.push({k:'end',ym});});P.push({k:'b'});return P;}
const bkKey=p=>p.k==='d'?'d:'+p.d:p.ym?p.k+':'+p.ym:p.k;
function bkCover(){const L=entryDays().size,n=state.cards.length;
  return `<div class="zpage zcover bcov">${bookSVG(L)}<h3>Your book</h3><p>${L===1?'One page':`${L} pages`} \\u00B7 ${n===1?'one Forgeling':`${n} Forgelings`}</p><p class="muted small">Started ${esc(dateLabel(state.startDate))}</p></div>`;}
function bkToc(){const M=zineMonths(),cur=todayKey().slice(0,7);
  return `<div class="zpage btoc"><p class="zk">Contents</p>${M.map(ym=>{const I=chInfo(ym),n=zineDays(ym).length;
    return `<button class="btrow" data-bkgo="ch:${ym}">${I.c?`<img src="${spriteURL(I.c)}" alt="" width="40" height="40">`:''}<span><b>${I.name}</b><span class="muted small">${ym===cur?`${ymName(ym)}, still being written`:`${ymName(ym)} ${ym.slice(0,4)} \\u00B7 ${n===1?'one page':`${n} pages`}`}</span></span></button>`;}).join('')}</div>`;}
function bkChapter(ym){const I=chInfo(ym),nm=I.c?(I.c.nick||I.c.name):'';
  return `<div class="zpage bch" style="--wash:${I.r>=0?CH_WASH[I.r]:'#E9DFC8'}"><p class="zk">Chapter ${I.n}</p><h3>${I.name}</h3>${I.c?`<img class="bchs" src="${spriteURL(I.c)}" alt="" width="96" height="96">`:''}${I.s?`<p class="bstamp">${seasonStampSVG(I.s,28,true)}<span>${I.s.name} ${ym.slice(0,4)}</span></p>`:''}<p class="muted small">${ymName(ym)} ${ym.slice(0,4)}${nm?` \\u00B7 named by ${esc(nm)}`:''}</p></div>`;}
function bkDay(k){const h=state.history.find(x=>x&&x.date===k&&x.status==='done'),c=h&&h.card!=null?cardById(h.card):null,V=VECTORS[h&&VECTORS[h.v]?h.v:0];
  const w=entryLine(k),e=state.journal[k],j=e&&e.text?e.text:'',f=(state.feel||{})[k],p=(state.posts||{})[k],n=c?(c.nick||c.name):'';
  return `<div class="zpage bday"><div class="bsp"><div class="bl"><p class="bdate">${esc(dateLabel(k))}</p><span class="bcall">${c&&c.own?'Yours':V.name}</span>${c?`<figure class="bprint"><img src="${spriteURL(c)}" alt="${esc(n)}" width="104" height="104"><figcaption>${esc(n)}</figcaption></figure>`:''}${p?pcFig(k,p,'inb'):''}</div><div class="br">${w?`<p class="world entry">${esc(w)}</p>`:''}${j?`<p class="mine">\\u201C${esc(j)}\\u201D</p>`:''}${!w&&FEEL_DAY[f]?`<p class="muted small">${FEEL_DAY[f]}</p>`:''}${e&&e.reply&&LATER[e.reply]?`<p class="later">${LATER[e.reply]}</p>`:''}</div></div></div>`;}
function bkEnd(ym){const w=monthWords(ym),mn=ymName(ym);
  return `<div class="zpage zback">${w?`<p>${w}</p>`:''}<p class="zend">The end of ${mn}.</p><div class="stack"><button class="ghost" data-bkpic="${ym}">Save ${mn} as a picture</button></div></div>`;}
function bkBack(){const nL=(state.letters||[]).length,L=entryDays().size;
  return `<div class="zpage bback"><p class="zk">At the back</p>${nL?`<button class="outline" id="bookLetters">Letters (${nL})</button>`:''}<button class="outline" id="jYear">Your year</button>${L>=30?'<button class="outline" id="bookRibbon">Open to an old page</button>':''}<p class="zend">More pages are written every day you show up.</p></div>`;}
function bookPageHTML(pg){return pg.k==='c'?bkCover():pg.k==='t'?bkToc():pg.k==='ch'?bkChapter(pg.ym):pg.k==='d'?bkDay(pg.d):pg.k==='end'?bkEnd(pg.ym):bkBack();}
function bookHTMLAt(i){const P=bookPages();i=Math.max(0,Math.min(P.length-1,i));ui.book={i};state.bookAt=bkKey(P[i]);
  return `<div class="csheet zine jbook" data-k="jbook"><h2 class="vh">Your book</h2><div class="zbox" aria-live="polite">${bookPageHTML(P[i])}</div><p class="muted small center" style="margin:6px 0">Page ${i+1} of ${P.length}</p><div class="row znav"><button class="outline" id="bkPrev" ${i?'':'disabled'}>Back a page</button><button class="primary" id="bkNext" ${i<P.length-1?'':'disabled'}>Next page</button></div><div class="stack"><button class="ghost" id="bkToc">Contents</button><button class="ghost" data-close>Close the book</button></div></div>`;}
function bookIdx(key){const P=bookPages(),i=P.findIndex(p=>bkKey(p)===key);return i;}
function openBook(key){let i=key?bookIdx(key):-1;if(i<0)i=1;openSheet(bookHTMLAt(i));save();}
function bookGo(d,focusId,to){const b=ui.book;if(!b)return;const sh=modal.querySelector('.sheet');if(!sh)return;const ni=to!=null?to:b.i+d;
  sh.innerHTML=bookHTMLAt(ni);nameDialog();sfx('select');save();
  const pg=sh.querySelector('.zbox .zpage');if(pg&&!REDUCE){pg.classList.add(ni<b.i?'bkb':'bkf');}
  const f=focusId&&document.getElementById(focusId);if(f&&!f.disabled)f.focus({preventScroll:true});else{const o=document.getElementById(focusId==='bkNext'?'bkPrev':'bkNext');if(o)o.focus({preventScroll:true});}
  const z=sh.querySelector('.zbox');if(z)z.scrollTop=0;}
function zinesHTML(){const M=zineMonths();""")
# swipe and arrow keys inside the book
rep("function openSheet(html,dismiss){","""let bkSw=null;
document.addEventListener('pointerdown',e=>{if(e.target.closest&&e.target.closest('.jbook .zbox'))bkSw={x:e.clientX,y:e.clientY};},true);
document.addEventListener('pointerup',e=>{const s=bkSw;bkSw=null;if(!s||!ui.book||!document.querySelector('.jbook'))return;const dx=e.clientX-s.x,dy=e.clientY-s.y;
  if(Math.abs(dx)>56&&Math.abs(dx)>Math.abs(dy)*1.5)bookGo(dx<0?1:-1,dx<0?'bkNext':'bkPrev');},true);
document.addEventListener('keydown',e=>{if(!document.querySelector('.jbook')||!ui.book)return;const t=e.target;if(t&&/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))return;
  if(e.key==='ArrowRight'){e.preventDefault();bookGo(1,'bkNext');}else if(e.key==='ArrowLeft'){e.preventDefault();bookGo(-1,'bkPrev');}});
function openSheet(html,dismiss){""")
# clicks
rep("  if(e.target.closest('#bookZines')){openSheet(zinesHTML());return;}","""  if(e.target.closest('#bookZines')){openSheet(zinesHTML());return;}
  if(e.target.closest('#bookOpen')){openBook(state.bookAt);return;}
  if(e.target.closest('#bookToc')){openBook('t');return;}
  if(e.target.closest('#bkPrev')){bookGo(-1,'bkPrev');return;}
  if(e.target.closest('#bkNext')){bookGo(1,'bkNext');return;}
  if(e.target.closest('#bkToc')){bookGo(0,null,1);return;}
  {const g=e.target.closest('[data-bkgo]');if(g){const i=bookIdx(g.dataset.bkgo);if(i>=0)bookGo(0,'bkNext',i);return;}}
  {const pz=e.target.closest('[data-bkpic]');if(pz){zinePicture(pz.dataset.bkpic);return;}}""")
# the Journal's panel and Today's "is bound" row open the book
rep("""${L?'<button class="outline" id="bookZines" style="margin-top:6px">Monthly books</button>':''}""","""${L?'<button class="primary" id="bookOpen" style="margin-top:6px">Open your book</button>':''}""")
rep("else if(b.id==='btnZine'){const pm=prevYM();state.zineSeen=pm;save();renderToday();openSheet(zineHTML(pm,0));}","else if(b.id==='btnZine'){const pm=prevYM();state.zineSeen=pm;save();renderToday();openBook('ch:'+pm);}")
# the ribbon is kept and checked
rep("  s.zineSeen=typeof s.zineSeen==='string'&&/^\\d{4}-\\d{2}$/.test(s.zineSeen)?s.zineSeen:'';","""  s.zineSeen=typeof s.zineSeen==='string'&&/^\\d{4}-\\d{2}$/.test(s.zineSeen)?s.zineSeen:'';
  s.bookAt=typeof s.bookAt==='string'&&/^(c|t|b|(ch|end):\\d{4}-\\d{2}|d:\\d{4}-\\d{2}-\\d{2})$/.test(s.bookAt)?s.bookAt:'';""")
# styles
rep("""html.jr .app .binder .jcap{width:0;min-width:100%}
</style>""","""html.jr .app .binder .jcap{width:0;min-width:100%}
/* 0.75: the book */
.jbook .zbox{min-height:420px}
.jbook .zpage{min-width:0;overflow-wrap:anywhere}
.bcov{align-items:center}.bcov .pi.book{width:120px;height:152px;margin:0 auto 6px}
.btoc .zk,.bch .zk,.bback .zk{font:20px VT323,monospace;letter-spacing:.06em;color:#6B5E7A;margin:0 0 8px}
.btrow{display:flex;gap:12px;align-items:center;width:100%;min-height:56px;padding:6px 4px;background:none;border:0;border-bottom:1px dotted #B9AE96;color:#3A2E25;text-align:left;font:inherit;cursor:pointer}
.btrow img{image-rendering:pixelated;background:#fff;padding:2px;box-shadow:0 1px 2px rgba(0,0,0,.25);flex:none}
.btrow b{display:block;font:700 22px/1.1 var(--hand,cursive)}.btrow .muted{color:#6B5E7A}
.bch{text-align:center;display:flex;flex-direction:column;justify-content:center;background:radial-gradient(circle at 50% 38%,var(--wash) 0,transparent 62%),#FFF8EA}
.bch h3{font:700 36px/1.05 var(--hand,cursive);margin:0 0 10px;color:#2E2A47}
.bchs{image-rendering:pixelated;margin:0 auto 8px;display:block}
.bstamp{display:flex;gap:8px;align-items:center;justify-content:center;margin:2px 0 8px;font:18px VT323,monospace;color:#4A4366}
.bsp{display:grid;gap:12px}
@media (min-width:700px){.jbook .bsp{grid-template-columns:1fr 1fr}.jbook .br{border-left:1px solid rgba(90,70,50,.15);padding-left:14px}}
.bl{position:relative;min-height:60px}
.bdate{font:19px VT323,monospace;margin:0;color:#4A4366}
.bcall{position:absolute;right:2px;top:0;border:2px solid #C8394B;color:#C8394B;font:18px VT323,monospace;padding:0 6px;transform:rotate(-5deg)}
.bprint{position:relative;background:#fff;padding:8px 8px 2px;margin:12px auto 8px;width:max-content;transform:rotate(-2deg);box-shadow:0 1px 3px rgba(0,0,0,.3)}
.bprint::before{content:'';position:absolute;left:-10px;top:-6px;width:46px;height:14px;background:rgba(255,214,107,.75);transform:rotate(-30deg)}
.bprint img{display:block;image-rendering:pixelated}
.bprint figcaption{text-align:center;font:700 22px/1.2 var(--hand,cursive);color:#2E2A47}
.bday .pcard.inb{margin:4px auto 0;transform:rotate(3deg)}
.bday .br .mine{font-size:24px;line-height:1.2}
.bback{display:flex;flex-direction:column;gap:10px}.bback button{min-height:44px}
.jbook .zpage.bkf{animation:bkIn .26s ease-out}.jbook .zpage.bkb{animation:bkInB .26s ease-out}
@keyframes bkIn{from{opacity:.35;transform:perspective(900px) translateX(26px) rotateY(-10deg)}}
@keyframes bkInB{from{opacity:.35;transform:perspective(900px) translateX(-26px) rotateY(10deg)}}
html.reduce .jbook .zpage{animation:none !important}
</style>""")
# fixes from the first look: night ink on the book's paper, handwriting for your words, the cover title, the season's wash
rep("""html.reduce .jbook .zpage{animation:none !important}""","""html.reduce .jbook .zpage{animation:none !important}
.jbook .zpage:not(.zcover){color:#3A2E25}
.jbook .zpage:not(.zcover) .mine{color:#2E2A47;background:none;border:0;padding:0;font:700 24px/1.2 var(--hand,cursive)}
.jbook .zpage:not(.zcover) .world{color:#4F3F86}
.jbook .zpage:not(.zcover) :is(button.outline,button.ghost){color:#2E2A47;border-color:#2E2A47;background:transparent;box-shadow:none}
.jbook .zpage:not(.zcover) button.ghost{text-decoration-color:#2E2A47}
.bcov h3{font:700 44px/1.05 var(--hand,cursive);color:#FFD36B;margin:4px 0 6px}""")
rep("""style="--wash:${I.r>=0?CH_WASH[I.r]:'#E9DFC8'}">""","""style="--wash:${I.s?I.s.px[1]+'99':I.r>=0?CH_WASH[I.r]:'#E9DFC8'}">""")
rep("""${nL?`<button class="outline" id="bookLetters">Letters (${nL})</button>`:''}""","""${nL?`<button class="outline" id="bookLetters">${nL===1?'One letter':`${nL} letters`}</button>`:''}""")
# 0.71's month words glued the feeling's save key ("Most days felt good"): whole sentences now
rep("out.push(top==='hard'?'A lot of it was hard, and you did it anyway.':`Most days felt ${top}.`);","out.push(top==='hard'?'A lot of it was hard, and you did it anyway.':top==='easy'?'Most days felt easy.':'Most days felt good.');")
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk75.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk75.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)

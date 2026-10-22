# Forge 0.19.0: bond stories (a chapter of each Forgeling's own story at every bond level)
# and a Hearth that grows from the callings you actually do. Reads base181.html, writes work.html.
src = open('base181.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

# ---------- CSS ----------
rep('/* Nav */', '''.tale{border-top:1px solid var(--line);padding:10px 0 8px}
.tale b{display:block;font:600 15px/1.3 var(--display)}
.tale p{margin:4px 0 0}
.tale.new{border-top:0;background:var(--chip);border-radius:14px;padding:10px 12px;margin:10px 0}
ul.furn{list-style:none;margin:6px 0 0;padding:0}
ul.furn li{display:flex;gap:10px;align-items:flex-start;padding:7px 0;border-top:1px solid var(--line)}
ul.furn li .fi{flex:none;width:22px;height:22px;border-radius:7px;background:var(--chip);display:grid;place-items:center;font-size:13px;color:var(--plum)}
ul.furn li.on .fi{background:var(--butter);color:#2E2A47}
ul.furn li b{display:block;font-weight:600}
ul.furn li small{display:block;color:var(--muted);font-size:13px;line-height:1.35}
ul.furn li:not(.on) b{color:var(--muted)}
/* Nav */''')

STORY_JS = r'''
/* ---- Bond stories: each Forgeling's own story, one chapter per bond level. Built from its seed, realm and
   calling, so no two are alike, and it never changes once read (only the name follows a new nickname). ---- */
const STORY_T=['Where it began','What it loves','What it keeps','The day it found you','Why it stays'];
const STORY_PLACE={
 '0-0':['under a dandelion clock that never quite finished striking','in a hollow where the grass grows in circles','beside a bee who refused to give directions'],
 '0-1':['in a thicket that has forgotten whose garden it was','under a thorn arch nobody walks through any more','where a hedge grew over an old gate and kept going'],
 '1-0':['in the warm ash of a kiln that never cools','on a rock that stays warm all night','between two sparks that were arguing'],
 '1-1':['at the bottom of a furnace older than the hills','in a crack where the ground glows red','beside a coal that has been burning for a thousand years'],
 '2-0':['in a rock pool the tide visits twice a day','on a beach made of very small shells','inside a wave that took a long time to break'],
 '2-1':['below the last place the light reaches','in a trench where the water hums','beside a lantern-fish who has never once blinked'],
 '3-0':['on a windowpane, in the first frost of the year','in a snowdrift shaped like a sleeping bear','at the top of a hill where the air is very clear'],
 '3-1':['in a whiteout so thick it had no edges','in the silence after a heavy snowfall','under ice that rings when you tap it'],
 '4-0':['on a workbench, between a half-built clock and a cup of cold tea','in the purple hour, just as the first lamp was lit','in a drawer full of things that might be useful one day'],
 '4-1':['in the unlit room at the end of a long hall','where the last streetlamp gives up','beside a candle someone forgot, which did not forget them']
};
const STORY_C={
 hatch:['Its first word was a sneeze.','It sat very still for a whole day, deciding whether to be brave.','The first thing it ever did was look for someone.','It wobbled for a week before it walked anywhere on purpose.','It hatched twice, to be sure.'],
 love:['the sound of rain on a roof it is under','the first warm hour of the morning','being carried, though it will deny this','counting pebbles, losing count, and starting again','very small hats','the moment just before a sneeze','the smell of toast it is not allowed to have'],
 quirk:['If you look away, it shuffles a little closer.','It keeps a list of everyone who has been kind to it. You are on it.','It hums when it thinks nobody is listening.','It has never once finished a snack without offering you half.','It practises this when you are not around.'],
 thing:['a button from a coat it has never seen','a drawing of the fire, slightly wrong','a stone shaped almost exactly like you','a feather it insists came from a dragon','a crumb from the first snack you shared'],
 where:['Tucked under its arm when it sleeps','In a spot by the fire only it knows','In a pocket it does not technically have'],
 why:['It shows it to nobody. Today it showed you.','It says it is for emergencies. It will not say what kind.','It checks on it every night, just in case.'],
 found:'{n} remembers the day it found you: {d}. You had just {did}. It decided right then that you were worth staying near.',
 pack:'{n} came out of a pack on {d}, blinking. You were the first thing it saw, and it has not found a reason to look anywhere else.',
 stay:'{n} was forged from a spark of {cv}. It says sparks like that always know where they are meant to land. {t} {n} is staying.'
};
const STORY_D={
 hatch:['It did not cry. It watched.','It waited a long time before it trusted the light.','It was guarding something before it knew what.','Its first sound was a low hum, like a question.','It stood up once, and has not needed to again.'],
 love:['the quiet just after a storm','the last ember in a fire','being asked rather than told','old doors, and what is behind them','standing guard over something asleep','the hour when nobody needs anything'],
 quirk:['It will not admit this. Please do not mention it.','It pretends this is a duty.','It has told no one else.','It considers this information classified.','If asked, it will deny everything, slowly.'],
 thing:['a cracked lantern lens','the name of something it once lost','a key to a door it will not open yet','a map of a place that is not there any more','one of your old worries, which it took when you were not looking'],
 where:['Beneath the stone it sits on','Somewhere the firelight does not reach','Close by, always,'],
 why:['It has never shown anyone. It showed you.','It says it is waiting for the right day.','It guards it the way it guards you: without being asked.'],
 found:'{n} remembers the day it found you: {d}. You had just {did}. It watched you do it, and quietly decided to keep watch over you.',
 pack:'{n} came out of a pack on {d}. It looked at you for a long time. Then it stopped looking for the way out.',
 stay:'{n} was forged from a spark of {cv}, and sparks like that do not end up anywhere by accident. {t} It has chosen this fire to guard.'
};
function storyOf(c){
  const S=c.dark?STORY_D:STORY_C,r=mulberry32((((c.seed|0)^0x51A7E)>>>0)),pick=a=>a[Math.floor(r()*a.length)],n=c.nick||c.name;
  const key=(c.theme|0)+'-'+(c.dark?1:0),realm=(REALM_PAGES[key]||{t:'the Forge'}).t,place=pick(STORY_PLACE[key]||['somewhere warm']),hatch=pick(S.hatch);
  const love=pick(S.love),quirk=pick(S.quirk),thing=pick(S.thing),where=pick(S.where),why=pick(S.why);
  const d=c.dateLabel||dateLabel(c.date),daily=c.source==='daily'||(c.source==null&&(state.history||[]).some(h=>h&&h.card===c.id));
  const days=Math.max(0,dayDiff(c.date,todayKey())),t=days<1?'You only met today.':days===1?'You have known each other for one day.':`You have known each other for ${days} days.`;
  const fill=s=>s.replace(/\{n\}/g,n).replace(/\{d\}/g,d).replace(/\{did\}/g,DID[c.v]||'shown up').replace(/\{cv\}/g,(VECTORS[c.v]||VECTORS[0]).name.toLowerCase()).replace(/\{t\}/g,t);
  return [`${n} began in ${realm}, ${place}. ${hatch}`,`${n} loves ${love}. ${quirk}`,`${where.replace(/,$/,'')}, ${n} keeps ${thing}. ${why}`,fill(daily?S.found:S.pack),fill(S.stay)];
}
function taleSheetHTML(c){
  const lv=bondLevel(c),n=c.nick||c.name,ch=storyOf(c);
  return `<h2>${esc(n)}’s story</h2><p class="muted small">${lv} of 5 chapters. A new one opens each time your bond grows.</p>`+
    ch.map((x,i)=>i<lv?`<div class="tale"><b>${i+1}. ${STORY_T[i]}</b><p>${esc(x)}</p></div>`:`<div class="tale"><b class="muted">${i+1}. ${STORY_T[i]}</b><p class="muted small">Opens when you are ${BOND_NAMES[i]}.</p></div>`).join('')+
    `<div class="stack"><button class="primary" id="taleBack">Close</button></div>`;
}
let taleFrom=null;
function taleOpen(id){const c=cardById(id);if(!c)return;taleFrom=ovMode==='inspect'?id:null;openSheet(taleSheetHTML(c),true);}
document.addEventListener('click',e=>{
  const k=e.target.closest&&e.target.closest('[data-tale]');if(k){taleOpen(+k.dataset.tale);return;}
  if(e.target.closest&&e.target.closest('#taleBack')){const f=taleFrom;taleFrom=null;closeModal();if(f&&cardById(f))inspect(f);}
});

/* ---- The Hearth grows from what you actually do. A few things appear by the fire for every kind of calling you
   keep coming back to. Worked out from your history, so it can never be bought, lost or reset. ---- */
const FURN=[
 {id:'rug',name:'A woven rug',need:3},{id:'lights',name:'A string of lanterns',need:10},{id:'tree',name:'A little tree',need:30},{id:'flies',name:'Fireflies',need:60},
 {id:'hedge',name:'A trimmed hedge',v:0},{id:'stones',name:'Balanced stones',v:1},{id:'pond',name:'A small pond',v:2},{id:'kite',name:'A paper kite',v:3},
 {id:'mail',name:'A mailbox',v:4},{id:'stump',name:'A chopping stump',v:5},{id:'ball',name:'A bright ball',v:6},{id:'lamp',name:'A lamp post',v:7},
 {id:'menhir',name:'A standing stone',v:8},{id:'bell',name:'A little bell',v:9},{id:'fence',name:'A mended fence',v:10},{id:'fern',name:'A potted fern',v:11}];
const FURN_V=3;
function doneTally(){const t={all:0,v:VECTORS.map(()=>0)},seen=new Set();(state.history||[]).forEach(h=>{if(h&&h.status==='done'&&!seen.has(h.date)){seen.add(h.date);t.all++;if(Number.isInteger(h.v)&&h.v>=0&&h.v<VECTORS.length)t.v[h.v]++;}});return t;}
const furnHave=(f,t)=>f.v!=null?t.v[f.v]>=FURN_V:t.all>=f.need;
function furnEarned(){const t=doneTally();return FURN.filter(f=>furnHave(f,t)).map(f=>f.id);}
let fcK='',fcV=[];
function furnNow(){const h=state.history||[],l=h[h.length-1],k=h.length+'|'+(l?l.date+l.status+l.v:'');if(k!==fcK){fcK=k;fcV=furnEarned();}return fcV;}
function furnNew(){const seen=state.hearth.fseen||[];return furnNow().filter(id=>!seen.includes(id));}
function furnListHTML(){
  const t=doneTally(),have=FURN.filter(f=>furnHave(f,t)).length;
  return `<details class="more"><summary>By the fire, ${have} of ${FURN.length}</summary><p class="muted small" style="margin-top:6px">Things appear by the fire as you keep doing your callings. Nothing here can be bought or lost.</p><ul class="furn">${FURN.map(f=>{
    const ok=furnHave(f,t),V=f.v!=null?VECTORS[f.v]:null;
    const how=V?(ok?`You have ${DID[f.v]} ${t.v[f.v]} times.`:`After ${FURN_V} ${V.name} days. ${t.v[f.v]} so far.`):(ok?`For ${f.need} callings done.`:`After ${f.need} callings done. ${t.all} so far.`);
    return `<li class="${ok?'on':''}"><span class="fi" aria-hidden="true">${ok?'✓':''}</span><span><b>${f.name}</b><small>${how}</small></span></li>`;}).join('')}</ul></details>`;
}
const FCOL={k:'#6B4A2E',w:'#A0703F',g:'#4FA36A',G:'#2F7A4A',l:'#8FD08A',s:'#B4B9C1',S:'#767B85',b:'#4F93C8',B:'#A6D8F2',r:'#D9475A',p:'#F29BB5',W:'#F4F0E8',m:'#4D5262',o:'#C8743E',a:'#E3B341',y:'#FFD36B',Y:'#FFF6CF',P:'#9B7BD8'};
const FSPR={
 menhir:['.SS.','SssS','Sss.','SsSs','Ssss','SsSs','Ssss','SSSS'],
 bell:['wwwwwww','w..k..w','w..a..w','w.aaa.w','w.aaa.w','waaaaaw','w..a..w','w.....w','w.....w','k.....k'],
 hedge:['..GgG....','.GgllGg..','GgglggGG.','GgggggggG','GGgggggGG','.GGGGGGG.'],
 mail:['.mmmm.','mmmmmr','mmmmmr','mWWWmm','mmmmmm','..kk..','..kk..','..kk..','..kk..','..kk..','.kkkk.'],
 stones:['...ss...','..sSSs..','...ss...','.ssssss.','.sSSSSs.','..ssss..','ssssssss','sSSSSSSs','.ssssss.'],
 ball:['.rrr.','rrWrr','rWrrr','rrrrr','.rrr.'],
 stump:['...m....','..mm....','...k....','.wwkwww.','wkwwwwkw','wwwwwwww','wwkwwwww','.wwwwww.'],
 fern:['g.l...l','.gl.lg.','l.ggg.g','.lgGgl.','..gGg..','.ooooo.','.oooooo','..ooo..','..ooo..'],
 kite:['....p....','...ppp...','..ppPpp..','.ppPPPpp.','..ppPpp..','...ppp...','....p....','....k....','.....r...','....k....','...r.....','....k....']
};
/* Drawn into the Hearth background, under the firelight. Things that glow keep their colour at night. */
function furnDraw(put,fs,dim){
  if(!fs||!fs.length)return;const has=id=>fs.includes(id);
  const C=(ch)=>{const h=FCOL[ch],q=hexRGB(h);return 'yY'.includes(ch)?q:[Math.round(q[0]*dim),Math.round(q[1]*dim),Math.round(q[2]*dim)];};
  const spr=(x,y,rows)=>rows.forEach((row,j)=>{for(let i=0;i<row.length;i++){const ch=row[i];if(ch!=='.')put(x+i,y+j,C(ch));}});
  if(has('fence'))for(let x=0;x<HW;x++){put(x,GYH-6,C('w'));put(x,GYH-3,C('w'));if(x%7===2)for(let y=GYH-8;y<GYH;y++)put(x,y,C('k'));}
  if(has('tree')){for(let y=37;y<GYH;y++)for(let x=5;x<=7;x++)put(x,y,C(x===5?'k':'w'));for(let y=-8;y<=8;y++)for(let x=-8;x<=8;x++)if(x*x+y*y<=64)put(6+x,30+y,C(x+y<-6&&((x+y)&1)?'l':((x*3+y)&3)?'g':'G'));}
  if(has('lights')){const sag=x=>2+Math.round(6*(1-Math.pow((x-64)/64,2)));for(let x=0;x<HW;x++)put(x,sag(x),C('m'));['y','p','B','a'].forEach((_,k)=>{});for(let x=4,k=0;x<HW;x+=9,k++){const ch=['y','p','B','y'][k%4],q=hexRGB(FCOL[ch]);put(x,sag(x)+1,q);put(x,sag(x)+2,q);put(x-1,sag(x)+1,q);}}
  if(has('kite')){spr(28,9,FSPR.kite);}
  if(has('bell'))spr(41,41,FSPR.bell);
  if(has('menhir'))spr(82,43,FSPR.menhir);
  if(has('hedge'))spr(111,45,FSPR.hedge);
  if(has('lamp')){const x=124;for(let y=31;y<GYH-1;y++)put(x,y,C('m'));for(let i=-1;i<=1;i++)put(x+i,GYH-1,C('m'));const Y=hexRGB(FCOL.Y),y2=hexRGB(FCOL.y);[[0,27],[-1,28],[0,28],[1,28],[-1,29],[0,29],[1,29],[0,30]].forEach(p=>put(x+p[0],p[1],p[0]===0&&p[1]===28?Y:y2));}
  if(has('pond')){for(let y=63;y<=70;y++)for(let x=0;x<=19;x++){const e=((x-9.5)*(x-9.5))/90+((y-66.5)*(y-66.5))/12;if(e<=1)put(x,y,C(e>.72?'S':(e<.25&&(x+y)&1)?'B':'b'));}}
  if(has('ball'))spr(23,61,FSPR.ball);
  if(has('stones'))spr(31,60,FSPR.stones);
  if(has('rug'))for(let y=64;y<=69;y++)for(let x=44;x<=84;x++){if(y===64||y===69){if(x&1)put(x,y,C('W'));continue;}const dpat=(Math.abs(((x-44)%8)-4)+Math.abs(y-66.5))<3;put(x,y,C(y===65||y===68?'r':dpat?'a':'o'));}
  if(has('stump'))spr(89,61,FSPR.stump);
  if(has('fern'))spr(106,60,FSPR.fern);
  if(has('mail'))spr(119,57,FSPR.mail);
}
'''
rep('/* ================= Start ================= */', STORY_JS + '\n/* ================= Start ================= */')

# ---------- Hearth background: draw furnishings, include them in the cache key ----------
rep("function buildHearthBG(mode,style){", "function buildHearthBG(mode,style,fs){")
rep("""  if(style==='gilded'){for(let i=0;i<30;i++)put(r()*HW,r()*30,'#FFD36B');}
  return rgb;""", """  if(style==='gilded'){for(let i=0;i<30;i++)put(r()*HW,r()*30,'#FFD36B');}
  furnDraw(put,fs,style?({glade:1,snow:.72,cave:.6,gilded:.62}[style]||1):({day:1,dusk:.78,night:.56}[mode]||1));
  return rgb;""")
rep("""const mode=todMode(),bdk=(state.hearth.bd&&backdropOK(state.hearth.bd))?state.hearth.bd:'',key=mode+'|'+bdk;if(!hbg||hbgMode!==key){hbg=buildHearthBG(mode,bdk);hbgMode=key;}""",
    """const mode=todMode(),bdk=(state.hearth.bd&&backdropOK(state.hearth.bd))?state.hearth.bd:'',fs=furnNow(),key=mode+'|'+bdk+'|'+fs.join(',');if(!hbg||hbgMode!==key){hbg=buildHearthBG(mode,bdk,fs);hbgMode=key;}""")
# fireflies, drawn over the firelight so they glow
rep("""  if(lvl<1){const mm=.62+.38*lvl;for(let qq=0;qq<HW*HH;qq++){d[qq*4]*=mm;d[qq*4+1]*=mm;d[qq*4+2]*=mm;}}""",
    """  if(fs.includes('flies')&&!heapOn)for(let k=0;k<7;k++){const ph=t/1700+k*1.7,on=REDUCE?(k%2===0):Math.sin(t/430+k*2.1)>.2;if(on)setpx(14+((k*37)%100)+Math.round(Math.sin(ph)*5),24+((k*13)%22)+Math.round(Math.cos(ph*1.3)*3),[214,255,140]);}
  if(lvl<1){const mm=.62+.38*lvl;for(let qq=0;qq<HW*HH;qq++){d[qq*4]*=mm;d[qq*4+1]*=mm;d[qq*4+2]*=mm;}}""")

# ---------- Hearth panel: story row, the list of things by the fire, and the "something new" line ----------
rep("""  hf.sel=Math.min(hf.sel,cs.length-1);
  const c=cs[hf.sel],lv=bondLevel(c)""", """  hf.sel=Math.min(hf.sel,cs.length-1);
  if(tab==='hearth'){const nf=furnNew();if(nf.length){const f=FURN.find(x=>x.id===nf[0]);hf.msg=nf.length===1?`Something new by the fire: ${f.name.toLowerCase()}.`:`${nf.length} new things by the fire. Have a look around.`;state.hearth.fseen=(state.hearth.fseen||[]).concat(nf);save();setTimeout(renderToday,0);}}
  const c=cs[hf.sel],lv=bondLevel(c)""")
rep("""'Forgebound. A golden glow outlines '+esc(n)+'.'}</p>
      <div class="actions">""", """'Forgebound. A golden glow outlines '+esc(n)+'.'}</p>
      <button class="rowl" data-tale="${c.id}" style="border-top:0;padding:6px 0;min-height:48px"><span class="rt"><b>${esc(n)}’s story</b><span class="rs">${lv} of 5 chapters${lv<5?'. The next opens at '+BOND_NAMES[lv]+'.':'. All told.'}</span></span><span class="chev" aria-hidden="true">›</span></button>
      <div class="actions">""")
rep("""<details class="more"><summary>Keepsakes and backdrops</summary><div class="lbl2">Keepsake</div><div class="chips" role="group" aria-label="Keepsake">${keeps}</div><div class="lbl2">Backdrop</div><div class="chips" role="group" aria-label="Backdrop">${bds}</div></details></div>`;""",
    """<details class="more"><summary>Keepsakes and backdrops</summary><div class="lbl2">Keepsake</div><div class="chips" role="group" aria-label="Keepsake">${keeps}</div><div class="lbl2">Backdrop</div><div class="chips" role="group" aria-label="Backdrop">${bds}</div></details>${furnListHTML()}</div>`;""")

# ---------- Bond-up sheet shows the new chapter ----------
rep("""'Your bond is growing.'}</p>
    <div class="stack">${k?""", """'Your bond is growing.'}</p>
    <div class="tale new"><b>New chapter: ${STORY_T[lv-1]}</b><p>${esc(storyOf(c)[lv-1])}</p></div>
    <div class="stack">${k?""")

# ---------- Card view: open the story ----------
rep("""<button class="ghost" id="inspFav">${c.fav?'\\u2605 Favorited':'\\u2606 Favorite'}</button>""",
    """<button class="ghost" id="inspFav">${c.fav?'\\u2605 Favorited':'\\u2606 Favorite'}</button><button class="ghost" data-tale="${c.id}">Story</button>""")

# ---------- Today: the Hearth row mentions something new by the fire ----------
rep("""rows.push(row('btnHearth',IC.hearth,'The Hearth',(state.hearth.sleep?'The fire has burned low and your Forgelings are asleep.':hv>0?`${hv} ${hv===1?'visit':'visits'} left today.`:'The fire is low for today.')+(wl?' '+wl:'')));}""",
    """const nf=state.hearth.sleep?[]:furnNew();rows.push(row('btnHearth',IC.hearth,'The Hearth',(state.hearth.sleep?'The fire has burned low and your Forgelings are asleep.':(nf.length?'Something new is waiting by the fire. ':'')+(hv>0?`${hv} ${hv===1?'visit':'visits'} left today.`:'The fire is low for today.'))+(wl?' '+wl:''),'',nf.length>0));}""")

# ---------- Fix: with reduced motion the Hearth was drawn while still hidden and never again, so it showed blank ----------
rep("  audioSync();\n}", "  audioSync();\n  if(tab==='hearth'&&REDUCE)requestAnimationFrame(()=>drawHearth(performance.now()));\n}")

# ---------- State ----------
rep("hearth:{slots:[],visits:{date:k,used:0},total:0,bd:''}", "hearth:{slots:[],visits:{date:k,used:0},total:0,bd:'',fseen:[]}")
rep("""  if(!hh.visits||typeof hh.visits!=='object')hh.visits={date:'',used:0};""",
    """  hh.fseen=Array.isArray(hh.fseen)?hh.fseen.filter((x,i,a)=>typeof x==='string'&&a.indexOf(x)===i).slice(0,64):[];
  if(!hh.visits||typeof hh.visits!=='object')hh.visits={date:'',used:0};""")

# ---------- version and what is new ----------
rep('<title>Forge (prototype 0.18.1)</title>', '<title>Forge (prototype 0.19.0)</title>')
rep("const VERSION='prototype 0.18.1';", "const VERSION='prototype 0.19.0';")
rep('const SEEN_V=22;', 'const SEEN_V=23;')
rep("""<ul class="newlist"><li><b>A living sky.</b>""",
    """<ul class="newlist"><li><b>Every Forgeling has a story.</b> Each one has its own, five chapters long. A new chapter opens every time your bond grows. Read it from the Hearth or from the card.</li>
    <li><b>The Hearth grows with you.</b> Things appear by the fire as you keep doing your callings: a rug, a kite, a pond, a mailbox. Each kind of calling brings something of its own, so your Hearth ends up looking like your days.</li>
    <li><b>A living sky.</b>""")

open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src))

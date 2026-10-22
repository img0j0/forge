# Forge 0.20.0: wanders go somewhere (a realm on your map), curios belong to realms, and Forgelings by the fire
# sometimes ask for something from a realm. Requests never expire; one at a time; a thank-you keepsake per realm.
# Reads base19.html, writes work.html.
src = open('base19.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

REQ_JS = r'''
/* ---- Wandering somewhere: each curio belongs to a realm, and a wander can head for one realm on your map. ---- */
const CREALM={acorn:0,flower:0,feather:0,mushroom:0,leaf:1,spark:1,bone:1,crystal:1,shell:2,pebble:2,rain:2,coin:2,snow:3,moon:3,bell:3,glimmer:3,key:4,candle:4,thread:4,map:4};
const rKnown=()=>[0,1,2,3,4].filter(ti=>state.cards.some(c=>c.theme===ti));
function rName(ti){if(!(ti>=0&&ti<=4))return 'somewhere';const cs=state.cards.filter(c=>c.theme===ti);return REALM_PAGES[ti+'-'+(cs.length&&cs.every(c=>c.dark)?1:0)].t;}
const rCurios=ti=>CURIOS.filter(x=>CREALM[x.id]===ti);
let wPickId=null;
function openWanderTo(c){
  wPickId=c.id;const n=c.nick||c.name,rq=state.request,ra=rq?cardById(rq.cid):null;
  const opts=rKnown().map(ti=>{const all=rCurios(ti),f=all.filter(x=>state.curios[x.id]).length,asked=rq&&rq.realm===ti&&ra;
    return `<button class="moodbtn" data-wgo="${ti}"><div><b>${esc(rName(ti))}</b><span>${f} of ${all.length} curios from here found${asked?`. ${esc(ra.nick||ra.name)} asked for something from here.`:'.'}</span></div></button>`;}).join('');
  openSheet(`<h2>Where should ${esc(n)} wander?</h2><p class="muted small">Realms on your map. They are back in about three hours.</p>${opts}
    <button class="moodbtn" data-wgo="-1"><div><b>Anywhere</b><span>Wherever the path goes. Good for finding something new.</span></div></button>
    <div class="row" style="justify-content:center"><button class="ghost" data-close>Not now</button></div>`);
}
/* ---- Requests: now and then a Forgeling by the fire asks for something from a realm. They never expire. ---- */
const REQ_C=['Could someone bring me something from {r}? I miss how the grass smells after rain.','Could someone bring me something from {r}? Something that stays warm at night.','Could someone bring me something from {r}? I want to hear the sea in it.','Could someone bring me something from {r}? Just to see snow again.','Could someone bring me something from {r}? I am starting a collection of maybes.'];
const REQ_D=['Bring me something from {r}. Anything that grew where it was not meant to.','Bring me something from {r}. The fire there remembers me.','Bring me something from {r}. From deep down, if you can.','Bring me something from {r}. Something quiet.','Bring me something from {r}. Something that has waited in the dark.'];
const KEEPR=[{id:'daisies',name:'Flower crown'},{id:'charm',name:'Ember charm'},{id:'shells',name:'Shell necklace'},{id:'cap',name:'Knitted cap'},{id:'lantern',name:'Little lantern'}];
const reqLine=rq=>{const c=cardById(rq.cid);return ((c&&c.dark)?REQ_D:REQ_C)[rq.realm].replace(/\{r\}/g,rName(rq.realm));};
const reqAsker=()=>state.request?cardById(state.request.cid):null;
function reqMaybe(){
  if(state.request||state.hearth.sleep||dayN()<3||(state.wstat.back||0)<1)return;
  if(state.reqLast&&dayDiff(state.reqLast,todayKey())<2)return;
  const out=wOut()?state.wander.id:-1,who=slotCards().filter(c=>bondLevel(c)>=2&&c.id!==out),known=rKnown();
  if(!who.length||!known.length)return;
  const c=who[rand(who.length)],fresh=known.filter(ti=>rCurios(ti).some(x=>!state.curios[x.id])),pool=fresh.length?fresh:known;
  state.request={cid:c.id,realm:pool[rand(pool.length)],made:todayKey()};save();
  hf.msg=`${c.nick||c.name} has a small request.`;setTimeout(renderToday,0);
}
function reqHTML(){
  const rq=state.request,c=reqAsker();if(!rq||!c)return '';
  return `<div class="tale new"><b>A request from ${esc(c.nick||c.name)}</b><p>“${esc(reqLine(rq))}”</p><p class="muted small">Send anyone to ${esc(rName(rq.realm))}. No rush: requests never run out.</p></div>`;
}
let bondUpNext=null;
document.addEventListener('click',e=>{
  const g=e.target.closest&&e.target.closest('[data-wgo]');
  if(g){const c=cardById(wPickId);closeModal();if(c&&!state.wander)wanderStart(c,+g.dataset.wgo);return;}
  const t=e.target.closest&&e.target.closest('[data-wto]');
  if(t){const cs=slotCards(),c=cs[Math.min(hf.sel,cs.length-1)];if(c&&!state.wander&&!state.hearth.sleep){wanderStart(c,+t.dataset.wto);toast(`${c.nick||c.name} heads off toward ${rName(+t.dataset.wto)}.`);renderChronicle();}return;}
  if(e.target.closest&&e.target.closest('#wcOk')){closeModal();const b=bondUpNext;bondUpNext=null;if(b)setTimeout(()=>openBondUp(b.c,b.lv),250);}
});
'''
rep('/* ================= Start ================= */', REQ_JS + '\n/* ================= Start ================= */')

# ---------- wanders carry a destination ----------
rep("function wanderStart(c){", "function wanderStart(c,realm){")
rep("""  state.wander={id:c.id,start:now,ready:now+WANDER_MS,seed:((now^((c.seed|0)*2654435761))>>>0),notified:false};
  state.wstat.sent++;save();hf.msg=`${c.nick||c.name} heads off down the path.`;sfx('select');""",
    """  const to=Number.isInteger(realm)&&realm>=0&&realm<=4?realm:-1;
  state.wander={id:c.id,start:now,ready:now+WANDER_MS,seed:((now^((c.seed|0)*2654435761))>>>0),notified:false,realm:to};
  state.wstat.sent++;save();hf.msg=to>=0?`${c.nick||c.name} heads off toward ${rName(to)}.`:`${c.nick||c.name} heads off down the path.`;sfx('select');""")
rep("""  const unfound=CURIOS.filter(x=>!state.curios[x.id]),pool=unfound.length?unfound:CURIOS,cu=pool[Math.floor(r()*pool.length)];""",
    """  const to=Number.isInteger(w.realm)&&w.realm>=0?w.realm:-1,base=to>=0?rCurios(to):CURIOS,unfound=base.filter(x=>!state.curios[x.id]),pool=unfound.length?unfound:base,cu=pool[Math.floor(r()*pool.length)];""")
# request fulfilment and the collect sheet
rep("""  state.wstat.back++;state.wander=null;save();
  const nm=c?(c.nick||c.name):'Your Forgeling',line=(c&&c.dark?cu.d:cu.c).replace(/\\{n\\}/g,nm),have=Object.keys(state.curios).length;
  const head=isNew?(have===CURIOS.length?'That is every curio. The shelf is complete.':'A new curio for your shelf'):'Another one for the pile';
  render();chime(2);
  openSheet(`<p class="muted center small">${head}</p>""",
    """  state.wstat.back++;state.wander=null;
  let done='';const rq=state.request,ra=rq?cardById(rq.cid):null;
  if(rq&&ra&&to===rq.realm){
    const before=bondLevel(ra);ra.bond=(ra.bond||0)+3;const K=KEEPR[rq.realm],nk=!state.keepsR.includes(K.id);if(nk)state.keepsR.push(K.id);
    const an=ra.nick||ra.name,after=bondLevel(ra);bondUpNext=after>before?{c:ra,lv:after}:null;
    state.request=null;state.reqLast=todayKey();state.reqDone=(state.reqDone||0)+1;
    done=`<div class="tale new"><b>${esc(an)}’s request is done</b><p>${esc(ra.dark?an+' takes it carefully and puts it somewhere safe. It looks at you a moment longer than usual.':an+' holds it up to the light, then hugs it. “Thank you. Really.”')}</p><p class="small">Bond with ${esc(an)} +3.${nk?` A thank-you keepsake: <b>${K.name}</b>. Any Forgeling can wear it.`:''}</p></div>`;
  }
  save();
  const nm=c?(c.nick||c.name):'Your Forgeling',line=(c&&c.dark?cu.d:cu.c).replace(/\\{n\\}/g,nm),have=Object.keys(state.curios).length;
  const head=(to>=0?'Back from '+rName(to)+'. ':'')+(isNew?(have===CURIOS.length?'That is every curio. The shelf is complete.':'A new curio for your shelf'):'Another one for the pile');
  render();chime(2);
  openSheet(`<p class="muted center small">${esc(head)}</p>""")
rep("""    <p class="muted small center">Curios found: ${have} of ${CURIOS.length}</p>
    <div class="stack"><button class="primary" data-close>Lovely</button></div>`);""",
    """    <p class="muted small center">Curios found: ${have} of ${CURIOS.length}</p>${done}
    <div class="stack"><button class="primary" id="wcOk" data-close>Lovely</button></div>`);""")

# ---------- the Hearth wander panel: request card + choose a destination ----------
rep("""Send ${esc(n)} out for a few hours. They come back with something small for your shelf.</p><button class="outline" id="hWander\"""",
    """Send ${esc(n)} out for a few hours, anywhere or to a realm on your map. They come back with something small for your shelf.</p><button class="outline" id="hWander\"""")
rep("""  return `<div class="panel-box" style="margin-top:8px">${body}<details class="more">""",
    """  return `<div class="panel-box" style="margin-top:8px">${reqHTML()}${body}<details class="more">""")
rep("""  else if(b.id==='hWander'&&c)wanderStart(c);""", """  else if(b.id==='hWander'&&c)openWanderTo(c);""")
# the out-wandering line names the realm
rep("""  else if(w&&wc)body=`<h2 style="margin:0">${wn} is out wandering</h2>""",
    """  else if(w&&wc)body=`<h2 style="margin:0">${wn} is out wandering${w.realm>=0?' in '+esc(rName(w.realm)):''}</h2>""")
# requests arrive when you visit the Hearth
rep("""  if(tab==='hearth'){const nf=furnNew();""", """  if(tab==='hearth'){reqMaybe();const nf=furnNew();""")

# ---------- keepsakes: thank-yous from requests, wearable by anyone ----------
rep("""  const keeps=[{id:'',name:'None',lvl:1}].concat(KEEPS).map(k=>""",
    """  const keeps=[{id:'',name:'None',lvl:1}].concat(KEEPS).concat(KEEPR.filter(k=>state.keepsR.includes(k.id)).map(k=>({id:k.id,name:k.name,lvl:1}))).map(k=>""")
rep("""<div class="lbl2">Keepsake</div><div class="chips" role="group" aria-label="Keepsake">${keeps}</div>""",
    """<div class="lbl2">Keepsake</div><div class="chips" role="group" aria-label="Keepsake">${keeps}</div>${state.keepsR.length<KEEPR.length?'<p class="muted small" style="margin-top:4px">More keepsakes come as thank-yous when you answer a request.</p>':''}""")
rep("""    else if(S.keep==='flower'){const fx=16+Math.round(half*.62),fy=top+3;stamp(g,fx-1,fy-1,['.c.','cyc','.c.'],false);}""",
    """    else if(S.keep==='flower'){const fx=16+Math.round(half*.62),fy=top+3;stamp(g,fx-1,fy-1,['.c.','cyc','.c.'],false);}
    else if(S.keep==='daisies'){[11,15,19].forEach(x=>stamp(g,x,top,['.c.','cyc','.c.'],false));}
    else if(S.keep==='charm'){const cy=mouthY+(dk?3:2);stamp(g,15,cy,['o..o','.oo.','.ya.','.aa.'],false);}
    else if(S.keep==='shells'){const sy=mouthY+(dk?4:3);for(let x=0;x<N;x++){const i=sy*N+x;if(M[i]&&g[i]!==1)g[i]=x%2?7:16;}}
    else if(S.keep==='cap'){const cm=mask();fillEll(cm,16,top+1.2,6.4,3.4);for(let y=Math.ceil(top+1.2);y<N;y++)for(let x=0;x<N;x++)cm[y*N+x]=0;commit(g,cm,{b:6,s:13,h:null});const bm=mask();fillEll(bm,16,top-2.6,1.6,1.4);commit(g,bm,{b:7,s:7,h:null});}
    else if(S.keep==='lantern'){const lx=16+half+2,ly=mouthY+1;stamp(g,Math.min(N-3,lx),ly,['.o.','ooo','yyy','yyy','yyy','ooo'],false);}""")

# ---------- the Map: send someone to wander in a realm ----------
rep("""  const mini=all.slice().sort((a,b)=>b.rarity-a.rarity||b.id-a.id).slice(0,6);
  return out+`<div class="latest" style="margin-top:6px">""",
    """  const mini=all.slice().sort((a,b)=>b.rarity-a.rarity||b.id-a.id).slice(0,6);
  const hc=slotCards(),hw=hc[Math.min(hf.sel,hc.length-1)],wc0=wCard(),rq=state.request,ra=rq&&rq.realm===ti?reqAsker():null;
  out+=hw?(state.wander&&wc0?`<p class="muted small" style="margin:8px 0 0">${esc(wc0.nick||wc0.name)} is out wandering${state.wander.realm>=0?' in '+esc(rName(state.wander.realm)):''}.</p>`:state.hearth.sleep?'':`<button class="outline" data-wto="${ti}" style="margin-top:10px">Send ${esc(hw.nick||hw.name)} to wander here</button>`):'';
  if(ra)out+=`<p class="muted small" style="margin:6px 0 0">${esc(ra.nick||ra.name)} asked for something from here.</p>`;
  return out+`<div class="latest" style="margin-top:6px">""")

# ---------- Today: the Hearth row mentions an open request ----------
rep("""(nf.length?'Something new is waiting by the fire. ':'')+""",
    """(nf.length?'Something new is waiting by the fire. ':'')+(state.request&&reqAsker()?`${esc(reqAsker().nick||reqAsker().name)} has a small request. `:'')+""")

# ---------- State ----------
rep("wander:null,curios:{},wstat:{sent:0,back:0}};}", "wander:null,curios:{},wstat:{sent:0,back:0},request:null,reqLast:'',reqDone:0,keepsR:[]};}")
rep("""  if(s.wander&&(typeof s.wander!=='object'||!Number.isFinite(s.wander.id)||!Number.isFinite(s.wander.ready)))s.wander=null;
  return s;""", """  if(s.wander&&(typeof s.wander!=='object'||!Number.isFinite(s.wander.id)||!Number.isFinite(s.wander.ready)))s.wander=null;
  if(s.wander)s.wander.realm=Number.isInteger(s.wander.realm)&&s.wander.realm>=0&&s.wander.realm<=4?s.wander.realm:-1;
  const rq=s.request;s.request=(rq&&typeof rq==='object'&&ids.has(rq.cid)&&Number.isInteger(rq.realm)&&rq.realm>=0&&rq.realm<=4)?{cid:rq.cid,realm:rq.realm,made:typeof rq.made==='string'?rq.made:''}:null;
  s.reqLast=typeof s.reqLast==='string'?s.reqLast:'';s.reqDone=int(s.reqDone,0,1e6,0);
  s.keepsR=Array.isArray(s.keepsR)?s.keepsR.filter((x,i,a)=>KEEPR.some(k=>k.id===x)&&a.indexOf(x)===i):[];
  return s;""")

# ---------- version and what is new ----------
rep('<title>Forge (prototype 0.19.0)</title>', '<title>Forge (prototype 0.20.0)</title>')
rep("const VERSION='prototype 0.19.0';", "const VERSION='prototype 0.20.0';")
rep('const SEEN_V=23;', 'const SEEN_V=24;')
rep("""<ul class="newlist"><li><b>Every Forgeling has a story.</b>""",
    """<ul class="newlist"><li><b>Wander somewhere.</b> Send a Forgeling to a realm on your map, from the Hearth or from the realm's page. Each realm has its own curios.</li>
    <li><b>Requests.</b> Now and then a Forgeling by the fire asks for something from a realm. Send anyone there. Requests never run out, and each realm has a thank-you keepsake any Forgeling can wear.</li>
    <li><b>Every Forgeling has a story.</b>""")

open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src))

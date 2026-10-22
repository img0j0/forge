# Forgelings 0.35.0: the Forge. Built from the design doc (October 22, 2026) with all seven recommended decisions:
#   (1) a Forge panel at the Hearth beside Wander, no new tab; (2) one ember per day of the small thing, two on all-in
#   days; (3) a small charm badge in the card's corner, the charm worn at the Hearth, card art untouched; (4) bright
#   realm names on the front of the map (the back comes in 0.36); (5) charms, the bell, the compass and Hearth pieces
#   now, the lantern held for 0.36; (6) the $9.99 Keeper unlock waits for 1.1; (7) spare counts only on a curio's
#   close-up, never on the shelf.
# How it works: embers are derived from history (one per done day, one more on all-in days), minus state.forge.spent,
#   so nothing fades and older saves are honoured. Spares are curio copies past the first (rec.n-1); the Forge never
#   takes the last. state.forge = {spent, made:[ids], log:{id:{by,at,used}}, bell:date, comp:date, compTo:ti}.
#   Pieces: five realm charms (keep ids charm0..charm4, drawn on the Hearth sprite and as a corner badge on the card),
#   the wanderer's bell (once a day, a wanderer comes home now), the compass (once a day, the needle settles toward a
#   realm that still holds something unfound; never a count), and three Hearth pieces drawn into the fire scene.
#   Every piece is signed "Forged by <name>, <date>" by the Forgeling selected at the Hearth.
# Reads base34.html.
src = open('base34.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

# ---- state ----
rep("own:{text:'',days:[]},backup:{at:'',ask:''},explore:{}};}", "own:{text:'',days:[]},backup:{at:'',ask:''},explore:{},forge:{spent:0,made:[],log:{},bell:'',comp:'',compTo:-1}};}")
rep("""  if(s.homeFav!==undefined&&s.homeFav!==null&&!Number.isInteger(s.homeFav))delete s.homeFav;""", """  if(s.homeFav!==undefined&&s.homeFav!==null&&!Number.isInteger(s.homeFav))delete s.homeFav;
  if(s.forge!==undefined){const f=s.forge;if(!f||typeof f!=='object')delete s.forge;else{if(!Number.isInteger(f.spent)||f.spent<0)f.spent=0;if(!Array.isArray(f.made))f.made=[];f.made=f.made.filter((x,i,a)=>typeof x==='string'&&a.indexOf(x)===i);if(!f.log||typeof f.log!=='object')f.log={};if(typeof f.bell!=='string')f.bell='';if(typeof f.comp!=='string')f.comp='';if(!Number.isInteger(f.compTo))f.compTo=-1;}}""")
rep("if(!s.curios)s.curios={};if(!s.wstat)", "if(!s.curios)s.curios={};if(!s.forge)s.forge={spent:0,made:[],log:{},bell:'',comp:'',compTo:-1};if(!s.wstat)")

# ---- the Forge: recipes, embers, spares, the sheet ----
FORGE_JS = r'''
/* ---- 0.35: the Forge. Embers from the days you show up, spares from wandering, forged into signed pieces. ---- */
const FORGE_R=[
 {id:'charm0',kind:'Keepsake',name:'Charm of Meadow',ti:0,sp:2,emb:2,what:'A charm any Forgeling can wear. It shows by the fire and in the corner of the card.'},
 {id:'charm1',kind:'Keepsake',name:'Charm of Ember',ti:1,sp:2,emb:2,what:'A charm any Forgeling can wear. It shows by the fire and in the corner of the card.'},
 {id:'charm2',kind:'Keepsake',name:'Charm of Tide',ti:2,sp:2,emb:2,what:'A charm any Forgeling can wear. It shows by the fire and in the corner of the card.'},
 {id:'charm3',kind:'Keepsake',name:'Charm of Frost',ti:3,sp:2,emb:2,what:'A charm any Forgeling can wear. It shows by the fire and in the corner of the card.'},
 {id:'charm4',kind:'Keepsake',name:'Charm of Dusk',ti:4,sp:2,emb:2,what:'A charm any Forgeling can wear. It shows by the fire and in the corner of the card.'},
 {id:'bell',kind:'Tool',name:'Wanderer’s bell',sp:2,emb:3,what:'Once a day, rings a wanderer home early.'},
 {id:'compass',kind:'Tool',name:'Compass',sp:3,emb:4,what:'Once a day, the needle settles toward a realm that still holds something unfound.'},
 {id:'kettle',kind:'Hearth',name:'A copper kettle',sp:2,emb:2,what:'Sits by the fire for good.'},
 {id:'stand',kind:'Hearth',name:'An iron stand',sp:2,emb:2,what:'Stands over the fire for good.'},
 {id:'chimes',kind:'Hearth',name:'Wind chimes',sp:2,emb:2,what:'Hang by the fire for good.'}];
const CHARM_COL=['#4FA36A','#FF8A2E','#4F93C8','#BFE6FF','#9B7BD8'];
const FGSPR={
 charm:['...kk...','..k..k..','..k..k..','...kk...','..kXXk..','.kXXXXk.','.kXYXXk.','.kXXXXk.','..kXXk..','...kk...'],
 bell:['...aa...','..a..a..','..aaaa..','.aaaaaa.','.aYaaaa.','.aaaaaa.','aaaaaaaa','...kk...'],
 compass:['..ssss..','.sWWWWs.','sWWrWWWs','sWWrWWWs','sWWWbWWs','sWWWbWWs','.sWWWWs.','..ssss..'],
 kettle:['...kk...','..kkkk..','.kooook.','kooooook','kooooook','.kooook.','..kkkk..','.k....k.'],
 stand:['mmmmmmmm','m..mm..m','m..mm..m','m..mm..m','m.aaaa.m','m......m','m......m','mm....mm'],
 chimes:['kkkkkkkk','.k.k.k.k','.s.a.s.a','.s.a.s.a','.s.a.s..','.s...s..','.....s..','........']};
const FG_URL={};
function fgRows(id){const m=/^charm([0-4])$/.exec(id);if(m)return FGSPR.charm.map(r=>r.replace(/X/g,m[1]));return FGSPR[id]||null;}
function fgURL(id){
  if(FG_URL[id])return FG_URL[id];const rows=fgRows(id);if(!rows)return '';
  try{const cv=document.createElement('canvas');cv.width=8;cv.height=10;const x=cv.getContext('2d'),im=x.createImageData(8,10);
    rows.forEach((row,j)=>{for(let i=0;i<8;i++){const ch=row[i];if(!ch||ch==='.')continue;const h=FCOL[ch];if(!h)continue;const q=hexRGB(h),o=(j*8+i)*4;im.data[o]=q[0];im.data[o+1]=q[1];im.data[o+2]=q[2];im.data[o+3]=255;}});
    x.putImageData(im,0,0);return FG_URL[id]=cv.toDataURL();}catch(e){return '';}
}
const fgImg=(id,sz,o)=>{o=o||{};const u=fgURL(id);return u?`<img class="cimg${o.cls?' '+o.cls:''}" src="${u}" width="${Math.round(sz*.8)}" height="${sz}" alt="${o.alt?esc(o.alt):''}">`:'';};
const fgState=()=>state.forge||(state.forge={spent:0,made:[],log:{},bell:'',comp:'',compTo:-1});
function embEarned(){const seen=new Set();let n=0;(state.history||[]).forEach(h=>{if(h&&h.status==='done'&&!seen.has(h.date)){seen.add(h.date);n+=h.allIn?2:1;}});return n;}
function embers(){return Math.max(0,embEarned()-(fgState().spent||0));}
const fgMade=id=>fgState().made.includes(id);
const forgedHearth=()=>FORGE_R.filter(r=>r.kind==='Hearth'&&fgMade(r.id)).map(r=>r.id);
const charmKeeps=()=>FORGE_R.filter(r=>r.ti!==undefined&&fgMade(r.id)).map(r=>({id:r.id,name:r.name,lvl:1}));
const charmOf=c=>{const m=c&&/^charm([0-4])$/.exec(c.keep||'');return m?FORGE_R.find(r=>r.id===c.keep):null;};
function spareList(ti){return CURIOS.filter(x=>(ti===undefined||CREALM[x.id]===ti)&&state.curios[x.id]&&state.curios[x.id].n>1).map(x=>({id:x.id,name:x.name,n:state.curios[x.id].n-1})).sort((a,b)=>b.n-a.n);}
const spareTotal=ti=>spareList(ti).reduce((s,x)=>s+x.n,0);
function fgCan(r){return !fgMade(r.id)&&embers()>=r.emb&&spareTotal(r.ti)>=r.sp;}
function fgNeeds(r){const sp=spareTotal(r.ti),e=embers(),rn=r.ti!==undefined?THEMES[r.ti].name+' ':'';
  return `Needs ${r.sp} ${rn}${r.sp===1?'spare':'spares'} and ${r.emb} embers. You have ${sp} ${rn}${sp===1?'spare':'spares'} and ${e} ${e===1?'ember':'embers'}.`;}
function fgSmith(){const cs=slotCards(),c=cs[Math.min(hf.sel,cs.length-1)],out=wOut()?state.wander.id:-1;if(c&&c.id!==out)return c;return cs.find(x=>x.id!==out)||c||null;}
function openForge(){
  const f=fgState(),s=fgSmith(),e=embers(),sp=spareTotal(),made=f.made.length;
  const rows=FORGE_R.map(r=>{const ok=fgMade(r.id),can=fgCan(r),L=f.log[r.id];
    return `<li class="${ok?'on':can?'can':''}"><span class="fi" aria-hidden="true">${fgImg(r.id,20)}</span><span><b>${esc(r.name)}</b><small>${r.kind}. ${esc(r.what)}</small><small>${ok?`Forged by ${esc(L?L.by:'a Forgeling')}, ${esc(L?dateLabel(L.at):'')}.`:esc(fgNeeds(r))}</small></span>${!ok&&can&&s?`<button class="chip" data-fmake="${r.id}">Make it</button>`:''}</li>`;}).join('');
  openSheet(`<h2>The Forge</h2><p class="muted small">${e} ${e===1?'ember':'embers'} and ${sp} spare ${sp===1?'curio':'curios'}. ${made} of ${FORGE_R.length} pieces made.${s?` Whoever helps signs the piece. Today that is ${esc(s.nick||s.name)}.`:' Seat a Forgeling by the fire to help.'}</p>
    <p class="muted small">Embers come from the days you do your small thing, two on days you go all in, and they never fade. Spares are extra copies of a curio. The Forge never takes your last one, and nothing here is ever sold.</p>
    <ul class="furn forgel">${rows}</ul>
    <div class="row" style="justify-content:center"><button class="ghost" data-close>Close</button></div>`);
}
function fgMake(id){
  const r=FORGE_R.find(x=>x.id===id),s=fgSmith();if(!r||!s||!fgCan(r))return;
  const f=fgState();let need=r.sp;const used=[];
  const sl=spareList(r.ti);for(let guard=0;need>0&&guard<40;guard++)sl.forEach(x=>{if(need>0&&state.curios[x.id].n>1){state.curios[x.id].n--;need--;used.push(x.name.toLowerCase());}});
  f.spent=(f.spent||0)+r.emb;f.made.push(r.id);f.log[r.id]={by:s.nick||s.name,at:todayKey(),used};
  if(r.kind==='Hearth'){hbg=null;}
  save();sfx('save');chime(2);hf.msg=`Forged with ${s.nick||s.name}: ${r.name.toLowerCase()}.`;renderHearth();renderToday();
  const cnt={};used.forEach(u=>cnt[u]=(cnt[u]||0)+1);const ul=Object.keys(cnt).map(k=>cnt[k]>1?`${k} ×${cnt[k]}`:k).join(', ');
  openSheet(`<p class="muted center small">Hot from the Forge</p><div class="cbig">${fgImg(r.id,90,{cls:'cpop',alt:r.name})}</div><h2 class="center">${esc(r.name)}</h2>
    <p class="center">Forged by ${esc(s.nick||s.name)}, ${esc(dateLabel(todayKey()))}.</p><p class="muted small center">Made with ${esc(ul)} and ${r.emb} embers. ${r.kind==='Hearth'?'It is by the fire now.':r.id==='bell'?'It hangs by the Wander path.':r.id==='compass'?'It sits on the Forge panel.':''}</p>
    <div class="stack">${r.ti!==undefined?`<button class="primary" data-equip="${r.id}" data-cid="${s.id}">${esc(s.nick||s.name)} wears it</button>`:''}<button class="${r.ti!==undefined?'ghost':'primary'}" data-close>Lovely</button></div>`);
}
function bellRing(){const f=fgState(),w=state.wander;if(!fgMade('bell')||!w||f.bell===todayKey())return;if(Date.now()>=w.ready)return;const c=cardById(w.id);w.ready=Date.now();w.notified=false;f.bell=todayKey();save();chime(1);toast(`The bell rings out. ${c?(c.nick||c.name):'Your wanderer'} turns for home.`);wanderTick();renderHearth();}
function compassAsk(){const f=fgState();if(!fgMade('compass'))return;if(f.comp!==todayKey()){const open=[0,1,2,3,4].filter(t=>rKnownTi(t)&&(rCurios(t).some(x=>!state.curios[x.id])||placesFound(t)<5));f.comp=todayKey();f.compTo=open.length?open[Math.floor(Math.random()*open.length)]:-1;save();}renderHearth();}
function compassLine(){const f=fgState();if(f.comp!==todayKey())return '';return f.compTo>=0?`The needle settles toward ${esc(mapName(f.compTo))}. Something there is still unfound.`:'The needle spins, then rests. Nothing on your map is left unfound.';}
function forgePanelHTML(){
  const f=fgState(),e=embers(),made=f.made.length;let tools='';
  if(fgMade('compass'))tools+=f.comp===todayKey()?`<p class="small" id="hCompLine" style="margin:8px 0 0">${compassLine()}</p>`:`<button class="outline" id="hCompass" style="margin-top:8px">Ask the compass</button>`;
  return `<div class="panel-box forgep" style="margin-top:8px"><div class="row" style="margin:0"><h2 style="margin:0">The Forge</h2><span class="muted small" id="hEmbers">${e} ${e===1?'ember':'embers'}</span></div>
    <p class="muted small">${made?`${made} of ${FORGE_R.length} pieces made.`:'Nothing forged yet.'} Embers come from the days you show up. Spare curios are the rest, never your last one.</p>${tools}
    <button class="outline" id="hForge" style="margin-top:8px">Open the Forge</button></div>`;
}
'''
rep("/* ---- Wandering somewhere: each curio belongs to a realm, and a wander can head for one realm on your map. ---- */",
    FORGE_JS + "/* ---- Wandering somewhere: each curio belongs to a realm, and a wander can head for one realm on your map. ---- */")
rep("const FCOL={k:'#6B4A2E',", "const FCOL={0:'#4FA36A',1:'#FF8A2E',2:'#4F93C8',3:'#BFE6FF',4:'#9B7BD8',k:'#6B4A2E',")

# ---- the panel at the Hearth, beside Wander; the bell in the wander panel ----
rep("""  else if(w&&wc)body=`<h2 style="margin:0">${wn} is out wandering${w.realm>=0?' in '+esc(rName(w.realm)):''}</h2><p class="muted small">Back in <span id="wLeft">${wLeftText()}</span>. There is no rush. If you are away, they will wait by the fire.</p>`;""",
    """  else if(w&&wc)body=`<h2 style="margin:0">${wn} is out wandering${w.realm>=0?' in '+esc(rName(w.realm)):''}</h2><p class="muted small">Back in <span id="wLeft">${wLeftText()}</span>. There is no rush. If you are away, they will wait by the fire.</p>${fgMade('bell')?(fgState().bell===todayKey()?'<p class="muted small">The bell has rung today.</p>':'<button class="outline" id="hBell" style="margin-top:8px">Ring the bell</button>'):''}`;""")
rep("""${have?'<button class="outline" id="hGift" style="margin-top:10px">Send a curio to a friend</button>':''}</details></div>`;""",
    """${have?'<button class="outline" id="hGift" style="margin-top:10px">Send a curio to a friend</button>':''}</details></div>${forgePanelHTML()}`;""")
rep("""  else if(b.id==='hCollect')wanderCollect();""", """  else if(b.id==='hCollect')wanderCollect();
  else if(b.id==='hForge')openForge();
  else if(b.id==='hBell')bellRing();
  else if(b.id==='hCompass')compassAsk();""")
rep("""  else if(b.dataset.equip){const c=cardById(+b.dataset.cid);if(c){c.keep=b.dataset.equip;save();closeModal();renderHearth();renderChronicle();}}""",
    """  else if(b.dataset.fmake){fgMake(b.dataset.fmake);}
  else if(b.dataset.equip){const c=cardById(+b.dataset.cid);if(c){c.keep=b.dataset.equip;save();closeModal();renderHearth();renderChronicle();}}""")
# forged charms join the keepsake chips at the Hearth
rep("""const keeps=[{id:'',name:'None',lvl:1}].concat(KEEPS).concat(KEEPR.filter(k=>state.keepsR.includes(k.id)).map(k=>({id:k.id,name:k.name,lvl:1}))).map(""",
    """const keeps=[{id:'',name:'None',lvl:1}].concat(KEEPS).concat(KEEPR.filter(k=>state.keepsR.includes(k.id)).map(k=>({id:k.id,name:k.name,lvl:1}))).concat(charmKeeps()).map(""")
# the compass points the way in the wander sheet, with no counts
rep("""${asked?`. ${esc(ra.nick||ra.name)} asked for something from here.`:'.'}</span></div></button>`;}).join('');""",
    """${asked?`. ${esc(ra.nick||ra.name)} asked for something from here.`:'.'}${fgState().comp===todayKey()&&fgState().compTo===ti?' The compass points here.':''}</span></div></button>`;}).join('');""")

# ---- Hearth pieces drawn into the fire scene ----
rep("fs=furnNow(),key=mode+'|'+bdk+'|'+fs.join(',');", "fs=furnNow().concat(forgedHearth()),key=mode+'|'+bdk+'|'+fs.join(',');")
rep("  if(has('mail'))spr(119,57,FSPR.mail);\n}", """  if(has('mail'))spr(119,57,FSPR.mail);
  if(has('stand')){for(let y=46;y<=59;y++){const o=Math.round((y-46)/3.5);put(60-o,y,C('m'));put(68+o,y,C('m'));}for(let x=59;x<=69;x++)put(x,46,C('m'));put(64,47,C('m'));put(64,48,C('m'));put(63,49,C('a'));put(65,49,C('a'));}
  if(has('kettle'))spr(76,55,FGSPR.kettle);
  if(has('chimes'))spr(16,12,FGSPR.chimes);
}""")

# ---- the charm worn: new palette slots and a pendant on the sprite ----
rep("const CH={o:1,b:2,s:3,h:4,l:5,a:6,w:7,p:8,g:9,G:10,k:11,c:16,t:14,y:17};", "const CH={o:1,b:2,s:3,h:4,l:5,a:6,w:7,p:8,g:9,G:10,k:11,c:16,t:14,y:17,A:19,B:20,C:21,D:22,E:23};")
rep("  const out=[[0,0,0]];for(let i=1;i<19;i++)out[i]=hexRGB(p[i]||'#000000');\n  const pulse=out.slice();",
    "  const out=[[0,0,0]];for(let i=1;i<19;i++)out[i]=hexRGB(p[i]||'#000000');\n  CHARM_COL.forEach((h,i)=>out[19+i]=hexRGB(h));\n  const pulse=out.slice();")
rep("""    else if(S.keep==='lantern'){const lx=16+half+2,ly=mouthY+1;stamp(g,Math.min(N-3,lx),ly,['.o.','ooo','yyy','yyy','yyy','ooo'],false);}""",
    """    else if(S.keep==='lantern'){const lx=16+half+2,ly=mouthY+1;stamp(g,Math.min(N-3,lx),ly,['.o.','ooo','yyy','yyy','yyy','ooo'],false);}
    else if(/^charm[0-4]$/.test(S.keep)){const L='ABCDE'[+S.keep[5]],cy=mouthY+(dk?2:1);stamp(g,13,cy,['o....o','.o..o.','..oo..','.oXXo.','oXXXXo','oXyXXo','.oXXo.','..oo..'].map(r=>r.replace(/X/g,L)),false);}""")
# the card: art untouched (the pendant is worn by the fire), a small badge in the corner
rep("""  const stars=[0,1,2,3,4].map(i=>`<i class="${i<=c.rarity?'on':''}"></i>`).join('');
  const SN=dk?['Might','Dread','Guile']:['Grit','Spark','Calm'];""", """  const stars=[0,1,2,3,4].map(i=>`<i class="${i<=c.rarity?'on':''}"></i>`).join('');
  const SN=dk?['Might','Dread','Guile']:['Grit','Spark','Calm'],ch=charmOf(c),cc=ch?Object.assign({},c,{keep:''}):c;if(ch)CMAP[ckey(cc)]=cc;""")
rep("""      <div class="art"><canvas class="pcv" width="48" height="37" data-k="${ckey(c)}" aria-label="${esc(c.name)}, a ${R.name} ${dk?'dark':'cute'} Forgeling"></canvas></div>""",
    """      <div class="art"><canvas class="pcv" width="48" height="37" data-k="${ckey(cc)}" aria-label="${esc(c.name)}, a ${R.name} ${dk?'dark':'cute'} Forgeling"></canvas>${ch?`<img class="chb" src="${fgURL(ch.id)}" alt="Wearing the ${esc(ch.name)}" title="${esc(ch.name)}">`:''}</div>""")
rep('/* Nav */', '''.art{position:relative}
.chb{position:absolute;right:.3em;bottom:.3em;width:1.6em;height:2em;image-rendering:pixelated;filter:drop-shadow(0 .1em 0 #0A0814)}
.mini .chb{right:.5em;bottom:.5em;width:2.4em;height:3em}
ul.forgel li{align-items:center}ul.forgel li .fi{width:28px;height:34px;background:none}ul.forgel li.on .fi{background:none}
ul.forgel li>span:nth-child(2){flex:1;min-width:0}ul.forgel li .chip{flex:none;margin-left:auto}
ul.forgel li.can b{color:var(--plum)}
/* Nav */''')

# ---- spare counts on a curio's close-up only ----
rep("""${rec.n>1?'You have '+rec.n+'.':''}</p>""", """${rec.n>1?'You have '+rec.n+', '+(rec.n-1)+' spare. Spares can go to the Forge, never your last one.':''}</p>""")
rep("wandered happily anyway and came back with a spare. Bond with", "wandered happily anyway and came back with a spare for the Forge. Bond with")

# ---- embers on the reveal, the report, ribbons, a prototype tool ----
rep("""      ${packGained?'<p class="rv-title" style="color:#FFD36B">That was your fifth day. A pack is ready!</p>':''}""",
    """      ${packGained?'<p class="rv-title" style="color:#FFD36B">That was your fifth day. A pack is ready!</p>':''}
      <p class="muted small" id="rvEmber">${allIn?'Two embers':'An ember'} for the Forge.</p>""")
rep("Curios found: ${Object.keys(state.curios).length} of ${CURIOS.length}\\n", "Curios found: ${Object.keys(state.curios).length} of ${CURIOS.length}\\nEmbers: ${embers()} (${(state.forge&&state.forge.spent)||0} spent)\\nForged: ${(state.forge&&state.forge.made.length)||0} of ${FORGE_R.length}\\n")
rep("""  {id:'gift1',name:'Kind Gesture',desc:'Send a curio to a friend.',g:1,f:()=>state.giftsSent||0},""",
    """  {id:'gift1',name:'Kind Gesture',desc:'Send a curio to a friend.',g:1,f:()=>state.giftsSent||0},
  {id:'forge1',name:'First Forging',desc:'Make something at the Forge.',g:1,f:()=>(state.forge&&state.forge.made.length)||0},
  {id:'forge5',name:'Smith',desc:'Make five pieces at the Forge.',g:5,f:()=>(state.forge&&state.forge.made.length)||0},""")
rep("""      <button class="tool" data-tool="wander"><b>Finish the wander</b><span>The wanderer comes back right now.</span></button>""",
    """      <button class="tool" data-tool="wander"><b>Finish the wander</b><span>The wanderer comes back right now.</span></button>
      <button class="tool" data-tool="spares"><b>Spares for the Forge</b><span>Two spares of every curio from realms on your map, for trying the Forge.</span></button>""")
rep("""  else if(name==='wander'){if(state.wander){""", """  else if(name==='spares'){const ks=rKnown();if(!ks.length){toast('Find a Forgeling first.');return;}CURIOS.filter(x=>ks.includes(CREALM[x.id])).forEach(x=>{const cur=state.curios[x.id]||{n:0,cid:0,at:todayKey()};cur.n=Math.max(cur.n,1)+2;state.curios[x.id]=cur;});save();tab='hearth';render();window.scrollTo(0,0);toast('Two spares of each curio. Open the Forge at the Hearth.');}
  else if(name==='wander'){if(state.wander){""")

# ---- version, What's New ----
rep('<title>Forgelings (prototype 0.34.0)</title>', '<title>Forgelings (prototype 0.35.0)</title>')
rep("const VERSION='prototype 0.34.0'", "const VERSION='prototype 0.35.0'")
rep('const SEEN_V=38;', 'const SEEN_V=39;')
rep("""<ul class="newlist"><li><b>Your favourite, on Today.</b>""",
    """<ul class="newlist"><li><b>The Forge.</b> Every day you do your small thing earns an ember (two when you go all in), and they never fade. At the Hearth, forge spare curios and embers into charms your Forgelings can wear, a bell that rings a wanderer home, a compass that points to something unfound, and pieces for the fire. Every piece is signed by the Forgeling who helped. The Forge never takes your last copy of a curio.</li>
    <li><b>Your favourite, on Today.</b>""")
import re
_i=src.index('<ul class="newlist">'); _j=src.index('</ul>',_i)
_items=re.findall(r'\s*<li>.*?</li>',src[_i+len('<ul class="newlist">'):_j],re.S)
src=src[:_i]+'<ul class="newlist">'+''.join(_items[:8])+src[_j:]
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src.encode()))

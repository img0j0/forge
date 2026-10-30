# 0.43.0: tidier pages. Every everyday page fits about one phone screen on a well-played save; nothing is removed,
# everything is one tap away (Hunter, October 30, from the tidier-pages canvas).
import re,subprocess,sys
S=open('base42.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old)
    assert c==n,(c,n,old[:90])
    S=S.replace(old,new)

rep("const VERSION='prototype 0.42.0'","const VERSION='prototype 0.43.0'")
rep("<title>Forgelings (prototype 0.42.0)</title>","<title>Forgelings (prototype 0.43.0)</title>")
rep("const SEEN_V=47","const SEEN_V=48")

# ---------------- Today ----------------
# The Hearth row only when something waits there; the Map row is gone (its news lives on the Map).
rep("""  if(state.cards.length){const hv=visitsLeft(),wl=wTodayLine().replace(/<[^>]+>/g,'');const nf=state.hearth.sleep?[]:furnNew();rows.push(""",
"""  if(state.cards.length){const hv=visitsLeft(),wl=wTodayLine().replace(/<[^>]+>/g,'');const nf=state.hearth.sleep?[]:furnNew();
    const waits=state.hearth.sleep||nf.length||(state.request&&reqAsker())||(state.wander&&wCard()&&wReady())||!state.wstat.sent;
    if(waits)rows.push(""")
rep("""  if(state.cards.length&&state.settings.lore!==false)rows.push(row('btnMapGo',IC.map,'The Map',esc(mapLatest()||'Nothing new in the margin today.')));
""","""  {const ml=state.cards.length&&state.settings.lore!==false?mapLatest():'';if(ml.startsWith('Today,'))rows.push(row('btnMapGo',IC.map,'The Map',esc(ml)));}
""")
rep("""${latest.map(c=>`<button data-insp="${c.id}" aria-label="Look at ${esc(c.name)}">${cardHTML(c,{w:92,mini:true})}</button>`).join('')}""",
"""${latest.map(c=>`<button data-insp="${c.id}" aria-label="Look at ${esc(c.name)}">${cardHTML(c,{w:58,mini:true})}</button>`).join('')}""")
rep("""<div class="group">${rows.join('')}</div>""","""${rows.length?`<div class="group">${rows.join('')}</div>`:''}""")

# ---------------- Hearth ----------------
old_start="""  el.innerHTML=`<p class="muted small" style="margin-bottom:8px">The Forge leaves a small fire burning in your corner of the world. Forgelings you trust come to sit by it.</p>"""
i=S.index(old_start); j=S.index("  drawHearth(performance.now());\n  bloomCheck();\n}",i)
S=S[:i]+"""  const wd=state.wander,wc=wCard(),wn=wc?esc(wc.nick||wc.name):'',e=embers(),fh=FURN.filter(f=>furnHave(f,doneTally())).length,have=haveN(),fg=fgState();
  const wbtn=wd&&wc&&wReady()?`<button class="act ready" id="hCollect">${HIC.wander}${wn} is back<small>See what they found</small></button>`
    :wd&&wc?`<button class="act" id="hWOut">${HIC.wander}Wandering<small>Back in <span id="wLeft">${wLeftText()}</span></small></button>`
    :`<button class="act" id="hWander">${HIC.wander}Wander<small>A few hours</small></button>`;
  let notes='';
  if(chartedCount()>=1&&!fgMade('xlantern'))notes+=`<p class="small" id="hLantern">A charted realm is waiting for a lantern. ${fgCan(FORGE_R.find(r=>r.id==='xlantern'))?'You have what it needs.':'See what it needs in the Forge.'}</p>`;
  if(fgMade('compass')&&fg.comp===todayKey())notes+=`<p class="small" id="hCompLine">${compassLine()}</p>`;
  el.innerHTML=`<div class="hearthwrap"><canvas id="hearthCv" width="${HW}" height="${HH}" role="img" aria-label="Your Forgelings sitting around a campfire"></canvas></div>
    <p class="hmsg" id="hmsg" aria-live="polite" aria-atomic="true">${esc(hf.msg||(!away&&memoryLine(c))||'The fire crackles. Everyone is settling in.')}</p>
    ${reqHTML()}${away?'':mEchoHTML(c)}
    ${cs.length>1?`<div class="chips hwho" role="group" aria-label="Companions">${cs.map((x,i)=>`<button class="chip" data-hslot="${i}" aria-pressed="${i===hf.sel}">${esc(x.nick||x.name)}</button>`).join('')}</div>`:''}
    <div class="group hcompg"><button class="rowl" id="hComp"><span class="rt"><b>${esc(n)}</b><span class="rs">${BOND_NAMES[lv-1]}, bond ${lv} of 5${c.statue?' · has a statue':''}</span><span class="bondbar" aria-hidden="true"><i style="width:${pct}%"></i></span></span><span class="chev" aria-hidden="true">›</span></button></div>
    <div class="actions hgrid">
      <button class="act" id="hAffection" ${away?'disabled':''} aria-describedby="hmsg">${HIC.sit}Sit with<small>Just for company</small></button>
      <button class="act" id="hSnack" ${left&&!away?'':'disabled'}>${HIC.snack}Snack<small>+1 or +2</small></button>
      <button class="act" id="hStory" ${left&&!away?'':'disabled'}>${HIC.story}Story<small>+2</small></button>
      <button class="act" id="hPlay" ${!away?'':'disabled'}>${HIC.play}Play<small>${left?'+1 to +3':'Just for fun'}</small></button>
      ${wbtn}
      <button class="act" id="hForge">${HIC.forge}The Forge<small id="hEmbers">${e} ${e===1?'ember':'embers'}</small></button>
    </div>
    <p class="muted small hvis">${away?`${esc(n)} is out wandering. Visits start again when they are back.`:left?`Visits left today: ${left} of 3. Play any of the five games.`:`Today's bond visits are complete. Sit together or play just for fun.`}</p>${notes}
    <div class="chips hmore">${fgMade('compass')&&fg.comp!==todayKey()?'<button class="chip" id="hCompass">Ask the compass</button>':''}<button class="chip" id="hShelf">Curio shelf · ${have} of ${shelfSet().length}</button><button class="chip" id="hFurn">By the fire · ${fh} of ${FURN.length}</button><button class="chip" id="hKeeps">Keepsakes</button><button class="chip" id="hChange">Change who is here</button></div>`;
"""+S[j:]

# sheets that hold what used to fold open on the Hearth
rep("""function furnListHTML(){
  const t=doneTally(),have=FURN.filter(f=>furnHave(f,t)).length;
  return `<details class="more"><summary>By the fire, ${have} of ${FURN.length}</summary><p class="muted small" style="margin-top:6px">""",
"""function furnListHTML(){
  const t=doneTally(),have=FURN.filter(f=>furnHave(f,t)).length;
  return `<h2>By the fire, ${have} of ${FURN.length}</h2><p class="muted small" style="margin-top:6px">""")
rep("""return `<li class="${ok?'on':''}"><span class="fi" aria-hidden="true">${ok?'✓':''}</span><span><b>${f.name}</b><small>${how}</small></span></li>`;}).join('')}</ul></details>`;""",
"""return `<li class="${ok?'on':''}"><span class="fi" aria-hidden="true">${ok?'✓':''}</span><span><b>${f.name}</b><small>${how}</small></span></li>`;}).join('')}</ul>`;""")

HEARTH_SHEETS=r"""
/* ---- 0.43: tidier Hearth. The long lists open as sheets; their buttons are routed to the Hearth's own handler. ---- */
const HIC=(()=>{const s=d=>`<svg class="hic" viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
  return {sit:s('<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/>'),snack:s('<path d="M12 8c-4-2-7 1-7 5s3 8 7 7c4 1 7-3 7-7s-3-7-7-5z"/><path d="M12 8V4"/>'),
    story:s('<path d="M4 5h7v14H4zM13 5h7v14h-7z"/>'),play:s('<path d="M12 3l2.6 5.6 6 .7-4.5 4 1.3 6L12 16.4 6.6 19.3l1.3-6L3.4 9.3l6-.7z"/>'),
    wander:s('<circle cx="12" cy="12" r="8"/><path d="M15 9l-2 5-4 1 2-5z"/>'),forge:s('<path d="M4 8h12l4 3h-6v3h2v4H8v-4h2v-3H4z"/>')};})();
function hSheetHTML(k){
  const cs=slotCards(),c=cs[hf.sel];const close='<div class="stack"><button class="ghost" data-close>Close</button></div>';
  if(k==='shelf'){const have=haveN();return `<h2>Curio shelf</h2><p class="muted small">${have} of ${shelfSet().length} found.</p>${shelfHTML()}${have?'<button class="outline" id="hGift" style="margin-top:10px;width:100%">Send a curio to a friend</button>':''}${close}`;}
  if(k==='furn')return furnListHTML()+close;
  if(k==='keeps'&&c){const lv=bondLevel(c);
    const keeps=[{id:'',name:'None',lvl:1}].concat(KEEPS).concat(KEEPR.filter(x=>state.keepsR.includes(x.id)).map(x=>({id:x.id,name:x.name,lvl:1}))).concat(charmKeeps()).map(x=>`<button class="chip" data-keep="${x.id}" ${lv<x.lvl?'disabled style="opacity:.45"':''} aria-pressed="${(c.keep||'')===x.id}">${x.name}${lv<x.lvl?' (level '+x.lvl+')':''}</button>`).join('');
    const unl=earnedIds(),bds=[{id:'',name:'Auto',ribbon:null}].concat(BACKDROPS).map(b=>{const ok=!b.id||unl.includes(b.ribbon),rb=b.ribbon?RIBBONS.find(r=>r.id===b.ribbon).name:'';return `<button class="chip" data-bd="${b.id}" ${ok?'':'disabled style="opacity:.45"'} aria-pressed="${(state.hearth.bd||'')===b.id}">${b.name}${ok?'':' (ribbon: '+rb+')'}</button>`;}).join('');
    return `<h2>Keepsakes and backdrops</h2><div class="lbl2">${esc(c.nick||c.name)} wears</div><div class="chips" role="group" aria-label="Keepsake">${keeps}</div>${state.keepsR.length<KEEPR.length?'<p class="muted small" style="margin-top:4px">More keepsakes come as thank-yous when you answer a request.</p>':''}<div class="lbl2">Backdrop</div><div class="chips" role="group" aria-label="Backdrop">${bds}</div>${close}`;}
  if(k==='comp'&&c){const lv=bondLevel(c),cur=BOND_AT[lv-1],nx=lv<5?BOND_AT[lv]:null,n=c.nick||c.name,pct=nx?Math.round(((c.bond||0)-cur)/(nx-cur)*100):100;
    return `<div class="row" style="margin:0"><h2 style="margin:0">${esc(n)}</h2><span class="muted small">${BOND_NAMES[lv-1]}, bond ${lv} of 5</span></div>
      <div class="bondbar" role="img" aria-label="Bond progress"><i style="width:${pct}%"></i></div>
      <p class="muted small">${nx?`${nx-(c.bond||0)} more ${nx-(c.bond||0)===1?'point':'points'} to ${BOND_NAMES[lv]}. Bond never fades.`:'Forgebound. A golden glow outlines '+esc(n)+'.'}</p>
      <p class="small stline">${c.statue?`<button class="ghost" data-statue="${c.id}">See ${esc(n)}’s statue</button>`:lv>=5?`${esc(n)}’s statue is ready to cast at the Forge. <button class="ghost" data-spre="${c.id}">Preview</button>`:`A statue waits at Forgebound. <button class="ghost" data-spre="${c.id}">Preview it in clay</button>`}</p>
      <button class="rowl" data-tale="${c.id}" style="border-top:0;padding:6px 0;min-height:48px"><span class="rt"><b>${esc(n)}’s story</b><span class="rs">${lv} of 5 chapters${lv<5?'. The next opens at '+BOND_NAMES[lv]+'.':'. All told.'}</span></span><span class="chev" aria-hidden="true">›</span></button>
      ${memoryHTML(c)}${statueShelfHTML()}${close}`;}
  if(k==='wout'){const w=state.wander,wc=wCard();if(!w||!wc)return '';const wn=esc(wc.nick||wc.name);
    if(wReady())return `<h2>${wn} is back</h2><p class="muted small">They have something to show you.</p><button class="primary" id="hCollect" style="margin-top:8px;width:100%">See what they found</button>${close}`;
    return `<h2>${wn} is out wandering${w.realm>=0?' in '+esc(rName(w.realm)):''}</h2><p class="muted small">Back in ${wLeftText()}. There is no rush. If you are away, they will wait by the fire.</p>${fgMade('bell')?(fgState().bell===todayKey()?'<p class="muted small">The bell has rung today.</p>':'<button class="outline" id="hBell" style="margin-top:8px;width:100%">Ring the bell</button>'):''}${close}`;}
  return '';
}
function openHSheet(k){const h=hSheetHTML(k);if(!h)return;openSheet(`<div class="hsheet" data-k="${k}">${h}</div>`);}
modal.addEventListener('click',e=>{
  const s=e.target.closest('.hsheet');if(!s)return;const b=e.target.closest('button');
  if(!b||b.disabled||b.hasAttribute('data-close')||b.dataset.statue||b.dataset.spre||b.dataset.tale!==undefined)return;
  const k=s.dataset.k,keep=b.dataset.keep,bd=b.dataset.bd;
  if(b.id==='hCollect'){closeModal();wanderCollect();return;}
  hearthBtn(b);
  if(s.isConnected&&!modal.hidden){const h=hSheetHTML(k);if(!h){closeModal();return;}s.innerHTML=h;nameDialog();
    const f=keep!==undefined?s.querySelector(`[data-keep="${keep}"]`):bd!==undefined?s.querySelector(`[data-bd="${bd}"]`):null;if(f)f.focus({preventScroll:true});}
});
"""
rep("""$('#view-hearth').addEventListener('click',e=>{
  if(e.target.id==='hearthCv'){if(!state.hearth.sleep&&hearthTap(e))return;hearthPoke();if(state.hearth.sleep&&!sleepRun)startWake();return;}
  const b=e.target.closest('button');if(!b)return;
  if(b.dataset.statue){openStatue(+b.dataset.statue);return;}""",
"""$('#view-hearth').addEventListener('click',e=>{
  if(e.target.id==='hearthCv'){if(!state.hearth.sleep&&hearthTap(e))return;hearthPoke();if(state.hearth.sleep&&!sleepRun)startWake();return;}
  const b=e.target.closest('button');if(!b)return;hearthBtn(b);
});
function hearthBtn(b){
  if(b.id==='hComp'){openHSheet('comp');return;}
  if(b.id==='hShelf'){openHSheet('shelf');return;}
  if(b.id==='hFurn'){openHSheet('furn');return;}
  if(b.id==='hKeeps'){openHSheet('keeps');return;}
  if(b.id==='hWOut'){openHSheet('wout');return;}
  if(b.dataset.statue){openStatue(+b.dataset.statue);return;}""")
rep("""  else if(b.id==='hPlay'&&c)openGames(c);
});
""","""  else if(b.id==='hPlay'&&c)openGames(c);
}
"""+HEARTH_SHEETS)

# ---------------- Tales ----------------
rep("""function oldTalesHTML(){
  if(!loreOn())return '';""","""function oldTalesHTML(){
  if(!loreOn())return '';
  if(OT_NEW){const any=Object.keys(state.curios).length,back=hasLantern()&&ch.tside;
    const side=hasLantern()?`<div class="tside" role="group" aria-label="Which side of the map"><button class="chip" data-tside="0" aria-pressed="${!back}">This side</button><button class="chip" data-tside="1" aria-pressed="${!!back}">Other side</button></div>`:'';
    return `<div class="group otales"><div class="otop"><h2>Old tales</h2>${side}</div><p class="muted small otint">${back?'Each Shade realm keeps its own side of the story. Cross with your lantern to bring its pages home.':'Every realm forgot a tale. Each of its four curios remembers one page.'+(any?'':' Your first wander starts at the Hearth.')}</p>${(back?[5,6,7,8,9]:[0,1,2,3,4]).map(taleRow).join('')}</div>`;}""")
TALES_JS=r"""
/* ---- 0.43: the tales as a bookshelf. One row per realm; a tale opens as a book, one page at a time. ---- */
const OT_NEW=true;
function taleRow(ti){
  const n=talePages(ti),T=TALES[ti],R=mapName(ti),locked=ti>=5&&!shadeOpen(ti)&&!n,b=ti>=5?THEMES[ti-5].name:'';
  const title=locked?`Across from ${b}: an untold tale`:n?T.t:R+': an untold tale';
  const sub=locked?`Chart ${b} fully, and your lantern lights the way.`:`${R}. ${n===4?'The tale is whole.':n+' of 4 pages'}`;
  const marks=T.p.map(([id])=>state.curios[id]?`<span class="g">${cImg(id,20)}</span>`:'<span class="g off"></span>').join('');
  return `<button class="rowl otale${n===4?' whole':''}" data-otale="${ti}"><span class="rt"><b>${title}</b><span class="rs">${sub}</span></span><span class="tmarks" aria-hidden="true">${marks}</span><span class="chev" aria-hidden="true">›</span></button>`;
}
let tbk={ti:0,p:0};
function taleBookHTML(){
  const ti=tbk.ti,T=TALES[ti],R=mapName(ti),n=talePages(ti),any=Object.keys(state.curios).length,locked=ti>=5&&!shadeOpen(ti)&&!n;
  const head=`<p class="tkick">${esc(R)} · ${n===4?'the tale is whole':n+' of 4 pages'}</p><h2 class="ttitle">${n?T.t:'An untold tale'}</h2>`;
  const close='<div class="stack"><button class="ghost" data-close>Close</button></div>';
  if(!n)return `<div class="csheet tbook" data-k="book">${head}<p class="world">${locked?`Chart ${esc(THEMES[ti-5].name)} fully on the front, and your lantern will light the way across.`:any?`No pages yet. Send a Forgeling to wander in ${esc(R)}.`:'No pages yet.'}</p>${close}</div>`;
  const p=tbk.p,[id,txt]=T.p[p],got=!!state.curios[id],last=p===3;
  const tabs=T.p.map(([cid],i)=>`<button class="tpg" data-tpage="${i}" aria-pressed="${i===p}" aria-label="Page ${i+1}${state.curios[cid]?'':', missing'}">${state.curios[cid]?cImg(cid,28):'<span class="g off"></span>'}</button>`).join('');
  return `<div class="csheet tbook" data-k="book">${head}<div class="tpgs" role="group" aria-label="Pages">${tabs}</div><p class="muted small">Page ${p+1} of 4</p>
    ${got?`<p class="world tpage">${esc(txt)}</p>`:`<p class="tpage gone">A page is missing. Another ${esc(R)} curio remembers it.</p>`}${last&&n===4?`<p class="done world">${esc(T.end)}</p>`:''}
    <div class="stack"><button class="primary" data-tpage="${last?0:p+1}">${last?'Back to page one':'Next page'}</button><button class="ghost" data-close>Close</button></div></div>`;
}
function openTaleBook(ti){tbk={ti,p:0};openSheet(taleBookHTML());}
function fgTalesHTML(){
  const cards=state.cards.slice().reverse(),shown=cards.slice(0,ch.more*12);
  return `<div class="csheet" data-k="fg"><h2>Your Forgelings' tales</h2><p class="muted small">Names, tales and second readings, newest first.</p>`+shown.map(c=>`<div class="chron"><button class="minibtn" data-insp="${c.id}" aria-label="Look at ${esc(c.nick||c.name)}">${cardHTML(c,{w:64,mini:true})}</button><div class="cbody">
    <b>${esc(c.nick||c.name)}</b><div class="muted small">${c.nick?'Born as '+esc(c.name)+', ':''}${realmName(c)}, ${esc(c.dateLabel)}</div>
    <p class="world">${esc(whisperFor(c))}</p>
    ${c.tale?`<p class="mine">\u201C${esc(c.tale)}\u201D</p>`:`<button class="ghost" data-edit="${c.id}" style="padding-left:0">Add a name or tale</button>`}${(c.fire||[]).slice(-2).map(f=>`<p class="mine">By the fire: \u201C${esc(f.text)}\u201D</p>`).join('')}${keptAge(c)>=KEPT_DAYS?'<div>'+keptLine(c).replace('class="ghost"','class="ghost" style="padding-left:0"')+'</div>':''}</div></div>`).join('')
    +(cards.length>shown.length?'<button class="pill" id="chMore" style="margin:6px auto;display:block">Show more</button>':'')+'<div class="stack"><button class="ghost" data-close>Close</button></div></div>';
}
function openCSheet(html){openSheet(html);hydrate(modal);}
"""
rep("""function talesHTML(){
  const cards=state.cards.slice().reverse(),ot=oldTalesHTML();
  if(!cards.length)return ot+'<p class="muted">Your Forgelings and their tales appear here once you find your first one.</p>';""",
TALES_JS+"""function talesHTML(){
  const cards=state.cards.slice().reverse(),ot=oldTalesHTML();
  if(!cards.length)return ot+'<p class="muted">Your Forgelings and their tales appear here once you find your first one.</p>';
  {const w=cards.filter(c=>c.tale).length;
    return ot+`<div class="group"><button class="rowl" id="fgTales"><span class="ri fgstack" aria-hidden="true">${cards.slice(0,3).map(c=>`<img src="${spriteURL(c)}" alt="">`).join('')}</span><span class="rt"><b>Your Forgelings' tales</b><span class="rs">${cards.length} ${cards.length===1?'Forgeling':'Forgelings'}${w?`, ${w} with a tale of yours`:''}. Names, tales and second readings.</span></span><span class="chev" aria-hidden="true">›</span></button></div>`;}""")

# ---------------- Journal ----------------
rep("""const journeyHTML=()=>bookHTML()+monthHTML()+recapHTML()+calendarHTML()+ribbonsHTML();""",
"""const journeyHTML=()=>bookHTML()+`<div class="chips jbtns"><button class="chip" id="jWeek">This week</button>${monthHTML()?'<button class="chip" id="jMonth">Your month in words</button>':''}</div>`+calendarHTML()+ribbonsHTML();
function jSheet(k){
  const close='<div class="stack"><button class="ghost" data-close>Close</button></div>';
  if(k==='week'){const d=didHTML(lastDays(35).filter(x=>x>=state.startDate));return `<div class="csheet" data-k="week">${recapHTML()}${d?`<div class="panel-box">${d}</div>`:''}${close}</div>`;}
  if(k==='month')return `<div class="csheet" data-k="month">${monthHTML()}${close}</div>`;
  if(k==='lines')return `<div class="csheet" data-k="lines"><h2>Your lines</h2>${journalHTML(true)}${close}</div>`;
  if(k&&k.startsWith('rib:')){const r=RIBBONS.find(x=>x.id===k.slice(4));if(!r)return '';const v=Math.min(r.g,r.f()),on=v>=r.g;
    return `<div class="csheet ribsheet" data-k="${k}"><span class="medal big${on?' on':''}" aria-hidden="true"><i></i></span><h2>${r.name}</h2><p>${r.desc}</p>${on?'<p class="small"><b>Earned.</b></p>':r.g<=12?`<div class="dots" role="img" aria-label="${v} of ${r.g}">${Array.from({length:r.g},(_,i)=>`<i class="${i<v?'on':''}"></i>`).join('')}</div><p class="muted small">${v} of ${r.g} so far. Missed days never count against it.</p>`:`<p class="muted small">${v} of ${r.g} so far.</p>`}${close}</div>`;}
  return '';
}""")
rep("""  return `<h3 style="margin-top:6px">Ribbons</h3><p class="muted small" style="margin-bottom:8px">${earned.length} of ${RV.length} earned. They are goals to enjoy, not chores.</p><div class="ribbons">${RV.map(r=>{
    const v=Math.min(r.g,r.f()),on=v>=r.g;
    return `<div class="rib${on?' on':''}"><div class="ico" role="img" aria-label="${on?'Earned':v+' of '+r.g}">${on?'\\u2713':v+'/'+r.g}</div><div style="flex:1;min-width:0"><b>${r.name}</b><small>${r.desc}</small>${on?'':r.g<=12?`<div class="dots" aria-hidden="true">${Array.from({length:r.g},(_,i)=>`<i class="${i<v?'on':''}"></i>`).join('')}</div>`:`<span class="soft">${v} of ${r.g} so far</span>`}</div></div>`;}).join('')}</div>`;""",
"""  return `<div class="panel-box ribp"><div class="row" style="margin:0"><h2 style="margin:0">Ribbons</h2><span class="muted small">${earned.length} of ${RV.length} earned</span></div><p class="muted small" style="margin:2px 0 6px">Goals to enjoy, not chores. Tap one to see it.</p><div class="medals">${RV.map(r=>{
    const v=Math.min(r.g,r.f()),on=v>=r.g;
    return `<button class="medal${on?' on':''}" data-rib="${r.id}"><i aria-hidden="true"></i><span class="sr">${r.name}. ${on?'Earned':v+' of '+r.g}</span></button>`;}).join('')}</div></div>`;""")
rep("""function journalHTML(){
  const ks=[...new Set(Object.keys(state.journal).concat(Object.keys(state.feel||{})))].sort().reverse();
  if(!ks.length)return '<p class="muted">Your journal starts with the first question you answer on the Today screen. It stays on this device.</p>';
  return '<p class="muted small" style="margin-bottom:8px">Private. Only on this device.</p>'+ks.slice(0,40).map(k=>{""",
"""function journalHTML(all){
  const ks=[...new Set(Object.keys(state.journal).concat(Object.keys(state.feel||{})))].sort().reverse();
  if(!ks.length)return '<p class="muted">Your journal starts with the first question you answer on the Today screen. It stays on this device.</p>';
  const more=!all&&ks.length>3?`<button class="outline" id="jLines" style="width:100%;margin-top:6px">All your lines (${Math.min(ks.length,40)})</button>`:'';
  return '<h2 class="sub3" style="margin-top:14px">Your lines</h2><p class="muted small" style="margin-bottom:8px">Private. Only on this device.</p>'+ks.slice(0,all?40:3).map(k=>{""")
rep("""${e&&e.reply?`<p class="later">${LATER[e.reply]}</p>`:''}</div>`;}).join('');
}""","""${e&&e.reply?`<p class="later">${LATER[e.reply]}</p>`:''}</div>`;}).join('')+more;
}""")

# the Map tab's click handler serves its sheets too
rep("""$('#view-chronicle').addEventListener('click',e=>{
  const ins=e.target.closest('[data-insp]');if(ins){inspect(+ins.dataset.insp);return;}""",
"""$('#view-chronicle').addEventListener('click',chronClick);
modal.addEventListener('click',e=>{if(e.target.closest('.csheet'))chronClick(e);});
function chronClick(e){
  const sh=e.target.closest('.csheet');
  const ins=e.target.closest('[data-insp]');if(ins){inspect(+ins.dataset.insp);return;}
  const tp=e.target.closest('[data-tpage]');if(tp){tbk.p=Math.max(0,Math.min(3,+tp.dataset.tpage));const s=modal.querySelector('.sheet');if(s){s.innerHTML=taleBookHTML();nameDialog();const f=s.querySelector(`.tpg[data-tpage="${tbk.p}"]`);if(f)f.focus({preventScroll:true});}sfx('select');return;}
  const ot=e.target.closest('[data-otale]');if(ot){openTaleBook(+ot.dataset.otale);return;}
  const ts=e.target.closest('[data-tside]');if(ts){ch.tside=ts.dataset.tside==='1';sfx('select');renderChronicle();const f=document.querySelector(`[data-tside="${ts.dataset.tside}"]`);if(f)f.focus({preventScroll:true});return;}
  const rb=e.target.closest('[data-rib]');if(rb){openSheet(jSheet('rib:'+rb.dataset.rib));return;}
  if(e.target.closest('#fgTales')){ch.more=1;openCSheet(fgTalesHTML());return;}
  if(e.target.closest('#jWeek')){openCSheet(jSheet('week'));return;}
  if(e.target.closest('#jMonth')){openSheet(jSheet('month'));return;}
  if(e.target.closest('#jLines')){openSheet(jSheet('lines'));return;}
  if(sh&&e.target.closest('#chMore')){ch.more++;const s=modal.querySelector('.sheet');if(s){s.innerHTML=fgTalesHTML();nameDialog();hydrate(modal);}return;}""")
rep("""  else if(b.id==='chMore'){ch.more++;renderChronicle();}
  else if(b.dataset.edit)openEdit(+b.dataset.edit,'none');
});""","""  else if(b.id==='chMore'){ch.more++;renderChronicle();}
  else if(b.dataset.edit)openEdit(+b.dataset.edit,'none');
}""")
rep("let ch={sub:'map',more:1,realm:null,side:0};","let ch={sub:'map',more:1,realm:null,side:0,tside:false};")

rep("${didHTML(days.filter(k=>k>=state.startDate))}","")
# ---------------- Map: only the latest margin note under the map ----------------
rep("""  const ev=evs.map(([a,e])=>{const m=ms[e.realm],dk=mood==='dark';""","""  const ev=evs.slice(0,1).map(([a,e])=>{const m=ms[e.realm],dk=mood==='dark';""")

# ---------------- Settings: every section starts folded ----------------
rep("""  if(!setOpen)setOpen=new Set(state.want.length||state.owns.length?[]:['cards']);""","""  if(!setOpen)setOpen=new Set();""")

# ---------------- What's New ----------------
S0=S.index('<ul class="newlist">');S1=S.index('</ul>',S0)
seg=S[S0:S1]
li=seg.rindex('\n    <li><b>Living Sky.</b>');seg=seg[:li]
seg=seg.replace('<ul class="newlist"><li><b>A living map.</b>','<ul class="newlist"><li><b>Tidier pages.</b> Each page now fits on about one screen. At the Hearth, everything you do with a Forgeling is one row of buttons under the fire, and the shelf, the things by the fire and keepsakes open on their own. Old tales sit on a bookshelf and open like a book, one page at a time, and ribbons are a row of medals you can tap.</li>\n    <li><b>A living map.</b>',1)
S=S[:S0]+seg+S[S1:]

# ---------------- CSS ----------------
CSS="""
/* 0.43 tidier pages */
.hgrid{margin-top:8px}.hgrid .act{min-height:72px;justify-content:center}.hgrid .act .hic{color:var(--plum);margin-bottom:2px}.hgrid .act.ready{box-shadow:inset 0 0 0 3px var(--plum)}
.hgrid .act[disabled]{opacity:.5}
.hcompg{margin:8px 0 0}.hcompg .rowl{min-height:56px;padding:8px 12px}.hcompg .bondbar{margin:6px 0 0}
.hwho{margin-top:8px}.hvis{margin:8px 0 0}.hmore{margin-top:8px}#hLantern,#hCompLine{margin:8px 0 0}
.otales .otop{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;padding:6px 10px 0}.otales .otop h2{margin:0}
.otales .otint{padding:0 10px;margin:4px 0 4px}.otales .rowl{min-height:58px;padding:8px 10px}
.tmarks{display:flex;gap:3px;flex:none}.tmarks .g,.tpg .g{width:20px;height:20px;display:inline-grid;place-items:center}.tmarks .g.off,.tpg .g.off{box-sizing:border-box;border:2px dashed var(--muted);opacity:.6}
.otale.whole b{color:var(--plum)}
.fgstack{display:flex !important;background:none !important;width:auto !important}.fgstack img{width:28px;height:28px;image-rendering:pixelated;margin-left:-8px}.fgstack img:first-child{margin-left:0}
.tbook .tkick{font:700 12px var(--body);letter-spacing:.06em;text-transform:none;color:var(--muted);margin:0}.tbook .ttitle{margin:2px 0 10px}
.tpgs{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:6px}.tpg{min-height:52px;display:grid;place-items:center;background:var(--chip);border:2px solid transparent}.tpg[aria-pressed="true"]{border-color:var(--plum)}
.tpg .g.off{width:28px;height:28px}.tpage{font-size:17px;line-height:1.55}.tpage.gone{color:var(--muted)}
.jbtns{margin:4px 0 10px}.tside{display:flex;gap:6px;flex-wrap:nowrap}
.otales .rowl.otale{border:0;border-top:1px solid var(--line);border-radius:0;margin:0;background:none;box-shadow:none}
#view-chronicle .cal span.c{aspect-ratio:auto;height:34px}.bookp .bookrow .book{width:52px;height:auto}.bookp{padding-top:10px;padding-bottom:10px}
.medals{display:grid;grid-template-columns:repeat(auto-fill,minmax(44px,1fr))}.medal{min-height:44px;background:none;border:0;padding:0;display:grid;place-items:center;color:var(--muted)}
.medal i,.medal.big i{display:block;width:22px;height:22px;box-sizing:border-box;border-radius:50%;border:2px solid currentColor;position:relative}
.medal i::after{content:'';position:absolute;left:3px;right:3px;top:17px;height:8px;background:linear-gradient(90deg,currentColor 0 40%,transparent 40% 60%,currentColor 60%)}
.medal.on i{background:#FFD36B;border-color:#A8791E}.medal.on i::after{background:linear-gradient(90deg,#E2703A 0 40%,transparent 40% 60%,#E2703A 60%)}
.medal.on{color:#A8791E}
.medal.big{display:grid;place-items:center;margin:4px auto 12px;color:var(--muted)}.medal.big i{width:64px;height:64px;border-width:4px}.medal.big i::after{left:12px;right:12px;top:54px;height:20px}
.medal.big.on i{background:#FFD36B;border-color:#A8791E}.ribsheet{text-align:center}.ribsheet .dots{justify-content:center;display:flex;gap:6px;margin:8px 0}
.ribsheet .dots i{width:14px;height:14px;display:block;box-sizing:border-box;border:2px solid var(--muted)}.ribsheet .dots i.on{background:var(--plum);border-color:var(--plum)}
"""
rep(".mapcap p{margin:6px 0}",".mapcap p{margin:6px 0}"+CSS)

open('work.html','w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S)
open('/tmp/chk43.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk43.js'],capture_output=True,text=True)
print('node --check',r.returncode,r.stderr[:800])

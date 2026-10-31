# 0.45: relics and gifts (from the Forge design doc, WvF6qntNFo6CfAbRyji9Wj).
# Realm relics: one per realm (five bright, five Shade with the lantern), forged from a spare of each of that realm's four
# curios and 8 embers. A relic sits on a shelf by the fire for good and adds a closing line to that realm's old tale.
# Gifts: a forged charm or ward can be sent to a friend (the sender keeps theirs, as with curios), and Shade curios can
# now be gifted too. Bright curio links stay v1 so older copies still open them; charms and Shade curios use v2.
import re,subprocess
S=open('base442.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)

rep("const VERSION='prototype 0.44.2'","const VERSION='prototype 0.45.0'")
rep("<title>Forgelings (prototype 0.44.2)</title>","<title>Forgelings (prototype 0.45.0)</title>")
rep("const SEEN_V=49;","const SEEN_V=50;")

# ---------- relic recipes (rt = the relic's realm; deliberately not `ti`, so relics are never worn like charms)
rep(""" {id:'ward4',kind:'Keepsake',name:'Ward of Void',ti:9,sp:2,emb:3,what:'',shade:1}];""",
""" {id:'ward4',kind:'Keepsake',name:'Ward of Void',ti:9,sp:2,emb:3,what:'',shade:1}]
 .concat(['Meadow','Ember','Tide','Frost','Dusk','Bramble','Inferno','Abyss','Wraith','Void'].map((n,t)=>({id:'relic'+t,kind:'Relic',name:'Relic of '+n,rt:t,sp:4,emb:8,what:'Sits by the fire for good and adds a closing line to the old tale.',shade:t>=5?1:0})));
/* 0.45: a relic's closing line, read at the end of its realm's old tale once the relic is by the fire. */
const RELIC_END=['By your fire now, the Meadow relic keeps all four together: the acorn, the crooked flower, the feather and the shy mushroom. Somewhere a hill is glad someone stayed for the view.',
 'The Ember relic sits by your fire with its leaf, its spark, its bone and its crystal. The spark that leapt has somewhere warm to land now, and it lands here.',
 'The Tide relic keeps a shell, a pebble, the rain and a coin by your fire. Hold it close on a quiet night. The sea is still in there, going wherever you bring it.',
 'The Frost relic rests by your fire: the snowfall, a little moon, a bell and a glimmer. The quiet came down from the mountain to keep you company here.',
 'The Dusk relic holds a key, a candle, a thread and a map, side by side by your fire. Every unfinished thing in the workshop has a way home, and this is one of the doors.',
 'The Bramble relic keeps its thorn, its seed, its nest and its rosehip by your fire. The edge sent it to say your place is still kept, for as long as you need.',
 'The Inferno relic sits by your fire with a banked cinder, black glass, a given ring and a pinch of warm ash. Inferno has handed back what it held for you, and it never asked why it took so long.',
 'The Abyss relic keeps a corked bottle, a deep pearl, a little anchor and sea glass by your fire. Every question you have not asked yet has room here too.',
 'The Wraith relic rests by your fire: a kept mitten, a still stone, a humming icicle and snow glass. It sits with you the way Wraith does, and does not need to say why.',
 'The Void relic holds an unsent letter, patient ink, a closed locket and a side-lit mirror by your fire. The things almost ready to be said are kept safe here, and kept company, until you are.'];
const relicsMade=()=>FORGE_R.filter(r=>r.rt!==undefined&&fgMade(r.id)).map(r=>r.id);""")

# sprite: a small reliquary in the realm's colour (X becomes the realm digit, as charms and wards do)
rep(""" chimes:['kkkkkkkk',""",""" relic:['...YY...','..aXXa..','.aaaaaa.','.aXXXXa.','.aXYXXa.','.aXXXXa.','.aaaaaa.','..a..a..','.aaaaaa.','........'],
 chimes:['kkkkkkkk',""")
rep("""const w=/^ward([0-4])$/.exec(id);if(w)return FGSPR.ward.map(r=>r.replace(/X/g,String(5+(+w[1]))));return FGSPR[id]||null;}""",
    """const w=/^ward([0-4])$/.exec(id);if(w)return FGSPR.ward.map(r=>r.replace(/X/g,String(5+(+w[1]))));const q=/^relic([0-9])$/.exec(id);if(q)return FGSPR.relic.map(r=>r.replace(/X/g,q[1]));return FGSPR[id]||null;}""")

# list: relics last, Shade relics with the lantern (fgList already hides r.shade without it)
# can / needs / make
rep("""function fgCan(r){if(r.multi)""","""const relicHave=t=>rCurios(t).filter(x=>state.curios[x.id]&&state.curios[x.id].n>1).length;
function fgCan(r){if(r.rt!==undefined)return !fgMade(r.id)&&embers()>=r.emb&&relicHave(r.rt)===4&&(r.rt<5||hasLantern());if(r.multi)""")
rep("""function fgNeeds(r){const sp=spareTotal(r.ti),e=embers(),rn=r.ti!==undefined?mapName(r.ti)+' ':'';""",
    """function fgNeeds(r){const sp=spareTotal(r.ti),e=embers(),rn=r.ti!==undefined?mapName(r.ti)+' ':'';
  if(r.rt!==undefined){const k=relicHave(r.rt);return `Needs a spare of each of ${mapName(r.rt)}’s four curios and ${r.emb} embers (you have spares of ${k} of 4, and ${e} ${e===1?'ember':'embers'}).`;}""")
rep("""  if(r.multi){spareRealms()""","""  if(r.rt!==undefined){rCurios(r.rt).forEach(x=>{state.curios[x.id].n--;need--;used.push(x.name.toLowerCase());});}
  else if(r.multi){spareRealms()""")
rep("""r.id==='xlantern'?'It lights the other side of every realm you have fully charted.':''}</p>""",
    """r.id==='xlantern'?'It lights the other side of every realm you have fully charted.':r.rt!==undefined?`It sits on the shelf by the fire now, and the old tale of ${esc(mapName(r.rt))} has a closing line.`:''}</p>""")
rep("""${r.id==='xlantern'?'<button class="primary" id="fgTurn">Turn the map over</button>':''}<button class="${r.ti!==undefined||r.id==='xlantern'?'ghost':'primary'}" data-close>Lovely</button></div>`);""",
    """${r.id==='xlantern'?'<button class="primary" id="fgTurn">Turn the map over</button>':''}${r.rt!==undefined&&loreOn()?`<button class="primary" data-otale="${r.rt}">Read the closing line</button>`:''}<button class="${r.ti!==undefined||r.id==='xlantern'||(r.rt!==undefined&&loreOn())?'ghost':'primary'}" data-close>Lovely</button></div>`);""")
# a relic opens the tale at its last page
rep("function openTaleBook(ti){tbk={ti,p:0};openSheet(taleBookHTML());}",
    "function openTaleBook(ti){tbk={ti,p:fgMade('relic'+ti)&&talePages(ti)===4?3:0};openSheet(taleBookHTML());}")
# Forge list rows: a gifted piece says who it came from
rep("""<small>${ok?`Forged by ${esc(L?L.by:'a Forgeling')}, ${esc(L?dateLabel(L.at):'')}.`:esc(fgNeeds(r))}</small>""",
    """<small>${ok?(L&&L.by?`${L.gift?'A gift from':'Forged by'} ${esc(L.by)}, ${esc(dateLabel(L.at))}.`:'Made.'):esc(fgNeeds(r))}</small>""")

# ---------- the closing line in the tale (book view and the older full view)
rep("""${last&&n===4?`<p class="done world">${esc(T.end)}</p>`:''}""",
    """${last&&n===4?`<p class="done world">${esc(T.end)}</p>${fgMade('relic'+ti)?`<p class="relicline world"><span class="ri" aria-hidden="true">${fgImg('relic'+ti,24)}</span>${esc(RELIC_END[ti])}</p>`:''}`:''}""")
rep("""${n===4?`<p class="done world">${esc(T.end)}</p>`:''}""",
    """${n===4?`<p class="done world">${esc(T.end)}</p>${fgMade('relic'+ti)?`<p class="relicline world">${esc(RELIC_END[ti])}</p>`:''}`:''}""")
rep("""out+=`<p class="muted small" style="margin:6px 0 0">Old tale: ${TALES[ti].t}. ${tp===4?'The tale is whole.':tp+' of 4 pages found.'}</p>`;""",
    """out+=`<p class="muted small" style="margin:6px 0 0">Old tale: ${TALES[ti].t}. ${tp===4?'The tale is whole.':tp+' of 4 pages found.'}${fgMade('relic'+ti)?' Its relic is by your fire.':''}</p>`;""")

# ---------- by the fire: a little shelf of relics, bright on the upper board, Shade on the lower
rep("""  if(has('chimes'))spr(16,12,FGSPR.chimes);
}""","""  if(has('chimes'))spr(16,12,FGSPR.chimes);
  const rl=fs.filter(x=>/^relic\\d$/.test(x));
  if(rl.length){const mini=['.Y.','aXa','XXX','aXa','aaa'];
    for(let x=85;x<=127;x++){put(x,21,C('w'));put(x,22,C('k'));}put(86,23,C('k'));put(126,23,C('k'));
    rl.forEach(id=>{const t=+id.slice(5);spr(87+t*4,16,mini.map(r=>r.replace(/X/g,String(t))));});}
}""")
rep("""fs=furnNow().concat(forgedHearth()),key=""","""fs=furnNow().concat(forgedHearth(),relicsMade()),key=""")
rep("""const C=(ch)=>{const h=FCOL[ch],q=hexRGB(h);""","""const C=(ch)=>{const h=FCOL[ch]||FCOL.k,q=hexRGB(h);""")

# ---------- gifts: v2 links carry a Shade curio (c) or a forged charm/ward (f); bright curios stay v1
rep("""function giftCheck(o){
  if(!o||typeof o!=='object'||o.v!==1)return null;
  const ok=(x,re)=>typeof x==='string'&&re.test(x),int=(x,lo,hi)=>Number.isInteger(x)&&x>=lo&&x<=hi;
  if(!ok(o.g,/^[a-z0-9]{6,24}$/)||!ok(o.s,/^[a-z0-9]{6,24}$/)||!CURIOS.some(c=>c.id===o.c))return null;""",
"""const GIFT_F=['charm0','charm1','charm2','charm3','charm4','ward0','ward1','ward2','ward3','ward4'];
function giftCheck(o){
  if(!o||typeof o!=='object'||(o.v!==1&&o.v!==2))return null;
  const ok=(x,re)=>typeof x==='string'&&re.test(x),int=(x,lo,hi)=>Number.isInteger(x)&&x>=lo&&x<=hi;
  if(!ok(o.g,/^[a-z0-9]{6,24}$/)||!ok(o.s,/^[a-z0-9]{6,24}$/))return null;
  if(o.v===1&&!CURIOS.some(c=>c.id===o.c))return null;
  if(o.v===2){const isC=o.c!==undefined,isF=o.f!==undefined;if(isC===isF)return null;if(isC&&!ALLC.some(c=>c.id===o.c))return null;if(isF&&!GIFT_F.includes(o.f))return null;}""")
rep("""  return {v:1,g:o.g,s:o.s,c:o.c,n:o.n.trim(),t:o.t,d:o.d,r:o.r,e:o.e,k:o.k,m:(o.m||'').trim()};""",
    """  const out={v:o.v,g:o.g,s:o.s,n:o.n.trim(),t:o.t,d:o.d,r:o.r,e:o.e,k:o.k,m:(o.m||'').trim()};if(o.f!==undefined)out.f=o.f;else out.c=o.c;return out;""")
# receiving
rep("""function openGiftIn(g){
  if(!g)return;$('#toast').classList.remove('show');const cu=CURIOS.find(x=>x.id===g.c),n=esc(g.n),img=spriteURL(giftSender(g));""",
"""function openGiftIn(g){
  if(!g)return;$('#toast').classList.remove('show');const fr=g.f?FORGE_R.find(x=>x.id===g.f):null,cu=fr?null:cuById(g.c),n=esc(g.n),img=spriteURL(giftSender(g));""")
rep("""You opened this gift from ${n} before. It is on your curio shelf.</p>""","""You opened this gift from ${n} before. ${fr?'It is in your Forge.':'It is on your curio shelf.'}</p>""")
rep("""    <div class="gcur" aria-hidden="true">${cImg('bundle',96,{cls:'gbun'})}${cImg(cu.id,96,{cls:'gitem'})}</div><p style="margin:0"><b>${esc(cu.name)}</b></p>
    ${g.m?`<p class="giftnote">“${esc(g.m)}”</p>`:''}</div>
    <div class="stack" style="margin-top:14px"><button class="primary" id="giftKeep">Put it on my shelf</button></div>`);""",
"""    <div class="gcur" aria-hidden="true">${cImg('bundle',96,{cls:'gbun'})}${fr?fgImg(fr.id,96,{cls:'gitem'}):cImg(cu.id,96,{cls:'gitem'})}</div><p style="margin:0"><b>${esc(fr?fr.name:cu.name)}</b></p>${fr?`<p class="muted small" style="margin:0">Forged by ${n}. Any of your Forgelings can wear it.</p>`:''}
    ${g.m?`<p class="giftnote">“${esc(g.m)}”</p>`:''}</div>
    <div class="stack" style="margin-top:14px"><button class="primary" id="giftKeep">${fr?'Keep it':'Put it on my shelf'}</button></div>`);""")
rep("""function giftKeep(){
  const g=giftPending();if(!g){closeModal();return;}""","""function giftKeep(){
  const g=giftPending();if(!g){closeModal();return;}
  if(g.f){const fr=FORGE_R.find(x=>x.id===g.f),f=fgState(),had=fgMade(fr.id);
    if(!had){f.made.push(fr.id);f.log[fr.id]={by:g.n,at:todayKey(),used:[],gift:1};}
    state.giftsGot=(state.giftsGot||[]).concat(g.g).slice(-200);giftClear();save();sfx('save');chime(2);
    openSheet(`<h2>${esc(fr.name)} is yours</h2><p class="muted">${had?'You had one already, so this one is kept as a thank-you from '+esc(g.n)+'.':'A gift from '+esc(g.n)+'. Any of your Forgelings can wear it: choose one at the Hearth, under Keepsakes.'}</p><div class="stack"><button class="primary" data-close>Lovely</button></div>`);
    renderHearth();renderChronicle();setTimeout(checkRibbons,600);return;}""")
# sending: Shade curios and forged charms join the picker
rep("""function openGiftSend(c){
  const own=CURIOS.filter(x=>state.curios[x.id]);if(!own.length){toast('Find a curio first. Send a Forgeling wandering.');return;}""",
"""function openGiftSend(c){
  const own=ALLC.filter(x=>state.curios[x.id]),fch=FORGE_R.filter(r=>GIFT_F.includes(r.id)&&fgMade(r.id));if(!own.length&&!fch.length){toast('Find a curio first. Send a Forgeling wandering.');return;}""")
rep("""if(!own.some(x=>x.id===gs.cur))gs.cur=own[0].id;""","""if(!own.some(x=>x.id===gs.cur)&&!fch.some(r=>r.id===gs.cur))gs.cur=(own[0]||fch[0]).id;""")
rep("""  openSheet(`<h2>Send a curio to a friend</h2><p class="muted small">Your friend gets a link that opens in their own Forgelings, and the curio goes on their shelf. You keep yours.</p>
    ${who}<div class="lbl2">Which curio</div><div class="gpick" role="group" aria-label="Which curio">${own.map(x=>`<button data-gcur="${x.id}" aria-pressed="${x.id===gs.cur}"><span class="gl" aria-hidden="true">${cImg(x.id,32)}</span>${esc(x.name)}</button>`).join('')}</div>""",
"""  openSheet(`<h2>Send a gift to a friend</h2><p class="muted small">Your friend gets a link that opens in their own Forgelings. A curio goes on their shelf, and a charm goes in their Forge. You keep yours.</p>
    ${who}${own.length?`<div class="lbl2">A curio</div><div class="gpick" role="group" aria-label="Which curio">${own.map(x=>`<button data-gcur="${x.id}" aria-pressed="${x.id===gs.cur}"><span class="gl" aria-hidden="true">${cImg(x.id,32)}</span>${esc(x.name)}</button>`).join('')}</div>`:''}
    ${fch.length?`<div class="lbl2">Or something you forged</div><div class="gpick" role="group" aria-label="Which forged charm">${fch.map(r=>`<button data-gcur="${r.id}" aria-pressed="${r.id===gs.cur}"><span class="gl" aria-hidden="true">${fgImg(r.id,32)}</span>${esc(r.name)}</button>`).join('')}</div>`:''}""")
rep("""<p class="muted small">The link holds only the curio, your Forgeling’s name and look, and your note. It goes only where you send it.</p>""",
    """<p class="muted small">The link holds only the gift, your Forgeling’s name and look, and your note. It goes only where you send it.</p>""")
rep("""  const c=cardById(gs.cid),cu=CURIOS.find(x=>x.id===gs.cur);if(!c||!cu)return;""",
    """  const c=cardById(gs.cid),fr=GIFT_F.includes(gs.cur)&&fgMade(gs.cur)?FORGE_R.find(x=>x.id===gs.cur):null,cu=fr?null:cuById(gs.cur);if(!c||(!cu&&!fr))return;""")
rep("""  const g={v:1,g:rid(),s:state.sid,c:cu.id,n,t:c.theme,d:c.dark?1:0,r:c.rarity,e:c.seed>>>0,k:c.v};if(note)g.m=note;""",
    """  const g={v:fr||!CURIOS.some(x=>x.id===cu.id)?2:1,g:rid(),s:state.sid,n,t:c.theme,d:c.dark?1:0,r:c.rarity,e:c.seed>>>0,k:c.v};if(fr)g.f=fr.id;else g.c=cu.id;if(note)g.m=note;""")
rep("""  shareOrCopy(`${n} found a ${cu.name.toLowerCase()} and wants you to have it. Open it in Forgelings: ${url}`,'Gift link copied. Paste it to your friend.','A gift from '+n);
  hf.msg=`${n} wraps up the ${cu.name.toLowerCase()} and sends it off.`;""",
"""  const what=(fr?fr.name:cu.name).replace(/^(A|An) /,'').toLowerCase().replace(/^(charm|ward) of (\\w)/,(m,a,b)=>a+' of '+b.toUpperCase());
  shareOrCopy(fr?`${n} forged a ${what} and wants you to have it. Open it in Forgelings: ${url}`:`${n} found a ${what} and wants you to have it. Open it in Forgelings: ${url}`,'Gift link copied. Paste it to your friend.','A gift from '+n);
  hf.msg=`${n} wraps up the ${what} and sends it off.`;""")

# the forge result's "Read the closing line" lives outside a .csheet, so route it here
rep("""modal.addEventListener('click',e=>{if(e.target.closest('.csheet'))chronClick(e);});""",
    """modal.addEventListener('click',e=>{if(e.target.closest('.csheet'))chronClick(e);});
modal.addEventListener('click',e=>{if(e.target.closest('.csheet'))return;const ot=e.target.closest('[data-otale]');if(ot)openTaleBook(+ot.dataset.otale);});""")

# the gift button says gift, and the Forge offers to send a charm you made
rep("""'<button class="outline" id="hGift" style="margin-top:10px">Send a curio to a friend</button>'""","""'<button class="outline" id="hGift" style="margin-top:10px">Send a gift to a friend</button>'""")
rep("""'<button class="outline" id="hGift" style="margin-top:10px;width:100%">Send a curio to a friend</button>'""","""'<button class="outline" id="hGift" style="margin-top:10px;width:100%">Send a gift to a friend</button>'""")
rep("""desc:'Send a curio to a friend.'""","""desc:'Send a gift to a friend.'""")
rep("""<ul class="furn forgel">${rows}</ul>${statueForgeHTML()}""","""<ul class="furn forgel">${rows}</ul>${GIFT_F.some(fgMade)?'<button class="outline" id="fgGift" style="margin-top:8px;width:100%">Send a charm to a friend</button>':''}${statueForgeHTML()}""")
rep("""modal.addEventListener('click',e=>{if(e.target.closest('.csheet'))return;const ot=""","""modal.addEventListener('click',e=>{if(!e.target.closest('#fgGift'))return;const r=FORGE_R.find(x=>GIFT_F.includes(x.id)&&fgMade(x.id));if(r)gs.cur=r.id;openGiftSend(fgSmith());});
modal.addEventListener('click',e=>{if(e.target.closest('.csheet'))return;const ot=""")

# ---------- styles
rep(".isgo{display:block;margin:8px 0 0;min-height:44px}",".isgo{display:block;margin:8px 0 0;min-height:44px}\n.relicline{display:flex;gap:8px;align-items:flex-start;margin-top:10px;padding-top:10px;border-top:1px dashed currentColor}.relicline .ri{flex:none}.relicline .ri img{image-rendering:pixelated}")

# ---------- What's New: newest first, keep eight
rep("""<ul class="newlist"><li><b>Realms in 3D.</b>""","""<ul class="newlist"><li><b>Relics and gifts.</b> At the Forge, make a relic from a spare of each of a realm’s four curios. It sits on a shelf by the fire for good and adds a closing line to that realm’s old tale. You can now send a charm you forged to a friend, and curios from the other side travel too.</li><li><b>Realms in 3D.</b>""")
m=re.search(r'<ul class="newlist">(.*?)</ul>',S,re.S); items=re.findall(r'<li>.*?</li>',m.group(1),re.S)
assert len(items)==9,len(items); rep(items[-1],"")

open('work.html','w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk45.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk45.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600])

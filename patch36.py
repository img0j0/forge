# Forgelings 0.36.0: Your small things (design doc https://claude.ai/artifact/Kt3TnuTRS44Ax69aMDsmy4, Hunter said go
# with every recommendation on October 23).
#  - "What do you want more of?" Pick up to three of eight (Moving, Calm, Connection, Making things, Focus, Rest,
#    Learning, Order). Each maps onto two or three of the twelve callings, and the daily card leans toward them about
#    two days in three. Asked from Today ("Make your cards yours", first row, once you have a Forgeling) rather than
#    before the first card, so day one stays quick. Always in Settings.
#  - Your own small things, up to three, each with a kind (one of the eight). With the Mix setting (default) one of
#    yours is the card about every other day; Most days, or Only the world's cards. On the card it reads "Yours ·
#    Moving" with a little pen, your words as the small thing, and the calling's Forge question. A done own-thing day
#    is a done day like any other: odds, embers, packs, pity, all unchanged.
#  - Realm leanings: a Forgeling found on one of your own small things leans (60%) to that kind's realm.
#  - Its card back says "Yours: <your words>".
#  - Migration: the old single "own small thing" (a separate tick on Today) becomes your first own small thing, with
#    its ticks kept for the Journal calendar. The separate tick row is gone.
# Reads base354.html.
src = open('base354.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

# ---- the eight wants ----
rep("const TASK_ALT=[", """/* 0.36: what you want more of. v = the callings it leans toward, t = the realm your own things of this kind lean to. */
const WANTS=[{n:'Moving',v:[11,6,5],t:0},{n:'Calm',v:[8,11],t:2},{n:'Connection',v:[4,9],t:1},{n:'Making things',v:[7,3,6],t:1},
  {n:'Focus',v:[2,1,0],t:3},{n:'Rest',v:[8,6,11],t:4},{n:'Learning',v:[2,7,10],t:3},{n:'Order',v:[10,0],t:2}];
const TASK_ALT=[""")

# ---- state ----
rep("explore:{},forge:{spent:0", "explore:{},want:[],wantAsked:false,owns:[],todayOwn:null,forge:{spent:0")
rep("settings:{mood:'mix',sound:true,reduce:false,nudge:null,lore:true,sky:'auto'}", "settings:{mood:'mix',sound:true,reduce:false,nudge:null,lore:true,sky:'auto',ownMix:'mix'}")
rep("s.backup={at:typeof bk.at==='string'&&DK.test(bk.at)?bk.at:'',ask:typeof bk.ask==='string'&&DK.test(bk.ask)?bk.ask:''};}",
    r"""s.backup={at:typeof bk.at==='string'&&DK.test(bk.at)?bk.at:'',ask:typeof bk.ask==='string'&&DK.test(bk.ask)?bk.ask:''};}
  {const DK=/^\d{4}-\d{2}-\d{2}$/;s.want=(Array.isArray(s.want)?s.want:[]).filter((x,i,a)=>Number.isInteger(x)&&x>=0&&x<WANTS.length&&a.indexOf(x)===i).slice(0,3);s.wantAsked=!!s.wantAsked;
   const ow=(Array.isArray(s.owns)?s.owns:[]).filter(o=>o&&typeof o==='object'&&typeof o.text==='string'&&o.text.trim()).slice(0,3).map((o,i)=>({id:Number.isInteger(o.id)&&o.id>0?o.id:i+1,text:o.text.trim().slice(0,60),k:Number.isInteger(o.k)&&o.k>=0&&o.k<WANTS.length?o.k:-1,days:(Array.isArray(o.days)?o.days:[]).filter((d,j,a)=>typeof d==='string'&&DK.test(d)&&a.indexOf(d)===j).sort().slice(-800)}));
   ow.forEach((o,i)=>{if(ow.findIndex(x=>x.id===o.id)!==i)o.id=Math.max(...ow.map(x=>x.id))+1;});
   if(!ow.length&&s.own&&s.own.text){ow.push({id:1,text:s.own.text,k:-1,days:s.own.days.slice()});s.own={text:'',days:[]};}
   s.owns=ow;s.todayOwn=Number.isInteger(s.todayOwn)&&ow.some(o=>o.id===s.todayOwn)?s.todayOwn:null;
   if(s.settings&&typeof s.settings==='object'&&!['mix','mine','surprise'].includes(s.settings.ownMix))s.settings.ownMix='mix';}""")
rep("c.keep=str(c.keep,'');", "c.keep=str(c.keep,'');c.own=str(c.own,'').slice(0,60);")

# ---- choosing today's card ----
rep("function pickVector(avoid){", r"""function wantVs(){return [...new Set((state.want||[]).flatMap(k=>WANTS[k]?WANTS[k].v:[]))];}
function todayOwnObj(){return state.todayOwn!=null?(state.owns||[]).find(o=>o.id===state.todayOwn)||null:null;}
function pickToday(avoid){
  const mode=(state.settings&&state.settings.ownMix)||'mix',ow=(state.owns||[]).filter(o=>o&&o.text);state.todayOwn=null;
  if(ow.length&&mode!=='surprise'&&Math.random()<(mode==='mine'?.8:.5)){
    const last=(state.history.filter(h=>h&&h.status==='done').slice(-1)[0]||{}).own,pool=ow.length>1?ow.filter(o=>o.id!==last):ow,o=pool[rand(pool.length)];state.todayOwn=o.id;
    const vs=o.k>=0?WANTS[o.k].v:wantVs(),p=vs.filter(v=>!avoid.includes(v));if(p.length)return p[rand(p.length)];if(vs.length)return vs[rand(vs.length)];return pickVector(avoid);}
  const lean=wantVs().filter(v=>!avoid.includes(v));if(lean.length&&Math.random()<2/3)return lean[rand(lean.length)];
  return pickVector(avoid);
}
function todayTask(){const o=todayOwnObj();return o?o.text:taskFor(state.todayV,state.date);}
function todayBand(){const o=todayOwnObj();return o?(o.k>=0?'Yours · '+WANTS[o.k].n:'Yours'):VECTORS[state.todayV].name;}
const PEN='<svg class="pi pen" viewBox="0 0 12 12" width="14" height="14" aria-hidden="true"><path fill="currentColor" d="M9 1h2v2h-2zM8 3h2v1h-2zM7 4h2v1h-2zM6 5h2v1h-2zM5 6h2v1h-2zM4 7h2v1h-2zM3 8h2v1h-2zM2 9h2v1h-2zM1 10h2v1h-2z"/></svg>';
function pickVector(avoid){""")
rep("state.date=k;state.todayV=pickVector(state.history.slice(-4).map(h=>h.v).filter(v=>v!=null).concat([state.todayV]));",
    "state.date=k;state.todayV=pickToday(state.history.slice(-4).map(h=>h.v).filter(v=>v!=null).concat([state.todayV]));")

# ---- the card face ----
rep("""<div class="taskface"><div class="band" style="background:${V.color}">${V.name}</div><p>${taskFor(state.todayV,state.date)}</p></div>""",
    """<div class="taskface"><div class="band" style="background:${V.color}">${esc(todayBand())}</div><p>${todayOwnObj()?PEN:''}${esc(todayTask())}</p></div>""")
rep("""<div class="vband" style="background:${V.color}"><b>${V.name}</b></div><div class="vbody"><p>${V.blurb}</p><p><strong>Today's small thing</strong>${taskFor(state.todayV,state.date)}</p>""",
    """<div class="vband" style="background:${V.color}"><b>${esc(todayBand())}</b></div><div class="vbody"><p>${todayOwnObj()?'Something you chose for yourself.':V.blurb}</p><p><strong>${todayOwnObj()?PEN+'Your small thing':'Today\\'s small thing'}</strong>${esc(todayTask())}</p>""")

# ---- earning: realm leaning, card record, own-thing days ----
rep("function earnDaily(allIn){\n  const c=makeCard({allIn,v:state.todayV,source:'daily',weights:allIn?ODDS.allIn:ODDS.daily});",
    "function earnDaily(allIn){\n  const ow=todayOwnObj(),lt=ow&&ow.k>=0&&Math.random()<.6?WANTS[ow.k].t:null;\n  const c=makeCard({allIn,v:state.todayV,source:'daily',weights:allIn?ODDS.allIn:ODDS.daily,theme:lt,own:ow?ow.text:''});\n  if(ow&&!ow.days.includes(state.date)){ow.days.push(state.date);ow.days.sort();if(ow.days.length>800)ow.days.splice(0,ow.days.length-800);}")
rep("state.history.push({date:state.date,status:'done',v:state.todayV,card:c.id,note:'',allIn:!!allIn});",
    "state.history.push(Object.assign({date:state.date,status:'done',v:state.todayV,card:c.id,note:'',allIn:!!allIn},ow?{own:ow.id}:{}));")
rep("theme:Math.floor(r()*THEMES.length),", "theme:(t=>o.theme!=null&&o.theme>=0&&o.theme<THEMES.length?o.theme:t)(Math.floor(r()*THEMES.length)),")
rep("allIn:!!o.allIn,source:o.source||'daily'}", "allIn:!!o.allIn,source:o.source||'daily',own:o.own||''}")
rep('<div class="m2">${V.name}${c.allIn?\', went all in\':\'\'}</div>', '<div class="m2">${c.own?\'Yours: \'+esc(c.own):V.name}${c.allIn?\', went all in\':\'\'}</div>')

# ---- Today: the old tick row goes; "Make your cards yours" is offered once ----
i = src.index("  if(state.own&&state.own.text){const on=state.own.days.includes(todayKey());rows.unshift("); j = src.index("\n", i)
src = src[:i] + "  if(!state.wantAsked&&state.cards.length&&state.status!=='fresh')rows.unshift(row('btnWant',PEN.replace('width=\"14\" height=\"14\"','width=\"21\" height=\"21\"'),'Make your cards yours','What do you want more of? Pick up to three, and add your own small things.','',true));" + src[j:]
rep("  if(b.id==='btnOwn'){toggleOwn();return;}", "  if(b.id==='btnOwn'){toggleOwn();return;}\n  if(b.id==='btnWant'){openWant();return;}")

# ---- the "want" sheet ----
rep("function openMargin(){", r"""function openWant(){
  ui.want=(state.want||[]).slice();
  openSheet(`<h2>What do you want more of?</h2><p class="muted">Pick up to three. Your daily card will lean toward them, and still surprise you now and then.</p>
    <div class="chips" role="group" aria-label="What you want more of" style="margin-top:10px">${WANTS.map((w,i)=>`<button class="chip" data-want="${i}" aria-pressed="${ui.want.includes(i)}">${w.n}</button>`).join('')}</div>
    <p class="muted small" style="margin-top:10px">You can also add up to three small things of your own, and change all of this any time, in Settings.</p>
    <div class="stack"><button class="primary" id="wantSave">Save</button></div>
    <div class="row" style="justify-content:center"><button class="ghost" id="wantSkip">Keep it a surprise</button></div>`);
}
function wantSaved(){state.wantAsked=true;if(state.status==='fresh')state.todayV=pickToday([]);save();renderToday();renderSettings();}
function openMargin(){""")
rep("  else if(b.id==='giftKeep')giftKeep();", r"""  else if(b.id==='giftKeep')giftKeep();
  else if(b.dataset.want!==undefined){const k=+b.dataset.want,i=ui.want.indexOf(k);if(i>=0)ui.want.splice(i,1);else if(ui.want.length<3)ui.want.push(k);else{sfx('no');toast('Three at most. Tap one to swap it out.');return;}modal.querySelectorAll('[data-want]').forEach(x=>x.setAttribute('aria-pressed',String(ui.want.includes(+x.dataset.want))));}
  else if(b.id==='wantSave'){state.want=ui.want.slice();closeModal();wantSaved();toast(state.want.length?'Your cards will lean that way. Add your own small things in Settings.':'Your cards stay a surprise.');}
  else if(b.id==='wantSkip'){closeModal();wantSaved();toast('Your cards stay a surprise. Settings has this whenever you want it.');}""")

# ---- Settings: Your cards ----
i = src.index('    <div class="setblock"><b>Your own small thing</b>'); j = src.index("</div></div>\n", i) + len("</div></div>\n")
src = src[:i] + r"""    <div class="setblock" id="yourCards"><b>Your cards</b><p class="muted small">What do you want more of? Pick up to three, and your daily card leans toward them.</p>
      <div class="chips" role="group" aria-label="What you want more of">${WANTS.map((w,i)=>`<button class="chip" data-swant="${i}" aria-pressed="${state.want.includes(i)}">${w.n}</button>`).join('')}</div>
      <div class="lbl2">Your own small things</div><p class="muted small">Up to three. Some days the card you turn over is one of yours, and doing it finds a Forgeling like any other day.</p>
      ${state.owns.map(o=>`<div class="ownitem"><span class="ot">${PEN}<b>${esc(o.text)}</b><small>${o.k>=0?WANTS[o.k].n:'Any kind'}</small></span><button class="pill" data-ownrm="${o.id}" aria-label="Remove ${esc(o.text)}">Remove</button></div>`).join('')}
      ${state.owns.length<3?`<label class="field"><span>A new small thing</span><input id="ownIn" maxlength="60" placeholder="For example: walk for ten minutes" autocomplete="off"></label><div class="lbl2">What kind of thing is it?</div><div class="chips" role="group" aria-label="What kind of thing is it">${WANTS.map((w,i)=>`<button class="chip" data-ownk="${i}" aria-pressed="${ownK()===i}">${w.n}</button>`).join('')}</div><div class="chips"><button class="pill" id="ownAdd">Add it</button></div>`:''}
      ${state.owns.length?`<div class="lbl2">How often yours come up</div><div class="chips" role="group" aria-label="How often yours come up">${[['mix','Every other day or so'],['mine','Most days'],['surprise','Only the world’s cards']].map(a=>`<button class="chip" data-ownmix="${a[0]}" aria-pressed="${(S.ownMix||'mix')===a[0]}">${a[1]}</button>`).join('')}</div>`:''}</div>
""" + src[j:]
rep("let ui={editJ:false,showFind:false};", "let ui={editJ:false,showFind:false,want:[],ownK:null};\nconst ownK=()=>ui.ownK!=null?ui.ownK:((state.want||[])[0]!=null?state.want[0]:0);")
i = src.index("  else if(b.id==='ownSave'){"); j = src.index("\n", src.index("  else if(b.id==='ownClear'){"))
src = src[:i] + r"""  else if(b.dataset.swant!==undefined){const k=+b.dataset.swant,w=state.want,i=w.indexOf(k);if(i>=0)w.splice(i,1);else if(w.length<3)w.push(k);else{sfx('no');toast('Three at most. Tap one to swap it out.');return;}state.wantAsked=true;if(state.status==='fresh')state.todayV=pickToday([]);save();renderSettings();renderToday();}
  else if(b.dataset.ownk!==undefined){ui.ownK=+b.dataset.ownk;document.querySelectorAll('#view-settings [data-ownk]').forEach(x=>x.setAttribute('aria-pressed',String(+x.dataset.ownk===ui.ownK)));}
  else if(b.id==='ownAdd'){const v=(($('#ownIn')||{}).value||'').trim().slice(0,60);if(!v){sfx('no');toast('Write a few words first.');return;}if(state.owns.length>=3)return;const id=Math.max(0,...state.owns.map(o=>o.id))+1;state.owns.push({id,text:v,k:ownK(),days:[]});state.wantAsked=true;save();renderSettings();renderToday();toast('Added. Some days, it will be the card you turn over.');}
  else if(b.dataset.ownrm!==undefined){const id=+b.dataset.ownrm,o=state.owns.find(x=>x.id===id);if(o){state.own.days=[...new Set(state.own.days.concat(o.days))].sort().slice(-800);state.owns=state.owns.filter(x=>x.id!==id);save();renderSettings();renderToday();toast('Removed. Its past days stay in the Journal.');}}
  else if(b.dataset.ownmix!==undefined){state.settings.ownMix=b.dataset.ownmix;save();renderSettings();}""" + src[j:]
rep('/* Nav */', """.pen{vertical-align:-2px;margin-right:6px}
.ownitem{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:8px 0;border-top:1px solid var(--line)}
.ownitem .ot{min-width:0}.ownitem .ot b{font-weight:700}.ownitem .ot small{display:block;color:var(--muted);font-size:13px;margin-left:20px}
/* Nav */""")

# ---- the Journal calendar marks your own things' days; the report counts them ----
rep("const ownSet=new Set((state.own&&state.own.days)||[]);", "const ownSet=new Set(((state.own&&state.own.days)||[]).concat(...(state.owns||[]).map(o=>o.days)));")
rep("\\nNudge: ${state.settings.nudge||'off'}", "\\nWants: ${(state.want||[]).map(k=>WANTS[k].n).join(', ')||'none'}\\nOwn small things: ${(state.owns||[]).length} (${(state.owns||[]).reduce((n,o)=>n+o.days.length,0)} days done)\\nCard mix: ${state.settings.ownMix||'mix'}\\nNudge: ${state.settings.nudge||'off'}")

# ---- heading order on Today (the margin panel's h2 used to sit between the title and Latest finds) ----
rep('<h3 style="margin-top:6px">Latest finds</h3>', '<h2 class="sub3">Latest finds</h2>')
rep('/* Nav */', 'h2.sub3{font:600 17px/1.2 var(--display);margin:20px 0 8px}\n/* Nav */')
# ---- version, What's New ----
rep('<title>Forgelings (prototype 0.35.4)</title>', '<title>Forgelings (prototype 0.36.0)</title>')
rep("const VERSION='prototype 0.35.4'", "const VERSION='prototype 0.36.0'")
rep('const SEEN_V=40;', 'const SEEN_V=41;')
rep("""<ul class="newlist"><li><b>Living Sky.</b>""",
    """<ul class="newlist"><li><b>Your small things.</b> Tell Forgelings what you want more of, and your daily card leans that way. Add up to three small things of your own, like a walk or a message to someone you love, and some days the card you turn over is yours. Find it in Settings, under Your cards.</li>
    <li><b>Living Sky.</b>""")
import re
_i=src.index('<ul class="newlist">'); _j=src.index('</ul>',_i)
_items=re.findall(r'\s*<li>.*?</li>',src[_i+len('<ul class="newlist">'):_j],re.S)
src=src[:_i]+'<ul class="newlist">'+''.join(_items[:8])+src[_j:]
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src.encode()))

# Forge 0.18.0: the design review's changes, applied to base171.html (0.17.1). Writes work.html.
# 1. Today: one hero (today's card, pixel-cut, full size), one filled button; everything else a quiet grouped list.
# 2. Hearth: progressive disclosure for keepsakes, backdrops and the curio shelf.
# 3. Binder: counters become a sentence (they looked tappable but were not).
# 4. Touch targets: chips, pills and text buttons reach 44px.
import re
src = open('base171.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

CSS = r'''
/* ---- design prototype ---- */
.chip,.fchip,.pill{min-height:44px}
details.dev summary{min-height:44px;display:flex;align-items:center}
.ghost{min-height:44px}
.pixcut{clip-path:polygon(0 8px,4px 8px,4px 4px,8px 4px,8px 0,calc(100% - 8px) 0,calc(100% - 8px) 4px,calc(100% - 4px) 4px,calc(100% - 4px) 8px,100% 8px,100% calc(100% - 8px),calc(100% - 4px) calc(100% - 8px),calc(100% - 4px) calc(100% - 4px),calc(100% - 8px) calc(100% - 4px),calc(100% - 8px) 100%,8px 100%,8px calc(100% - 4px),4px calc(100% - 4px),4px calc(100% - 8px),0 calc(100% - 8px))}
.herowrap{filter:drop-shadow(0 3px 0 var(--line));margin-bottom:16px}
.hero{background:var(--surface);padding:22px 18px 18px;display:grid;justify-items:center;gap:8px;text-align:center}
.hero h2{margin:6px 0 0;font-size:22px}
.hero .primary,.hero .btnrow{width:100%;margin-top:8px}
.heroback{width:136px;height:190px;border:0;padding:0;display:grid;align-content:center;justify-items:center;gap:10px;color:#fff;font:600 15px var(--display);background:radial-gradient(circle,rgba(255,255,255,.2) 0 1.8px,transparent 2.6px) 0 0/16px 16px,#5B4A9E;box-shadow:inset 0 0 0 6px #4A3B88}
.heroback svg{width:58px;height:58px}
@media (prefers-reduced-motion:no-preference){.heroback{animation:heroBob 3.4s ease-in-out infinite}}
html.reduce .heroback{animation:none}
@keyframes heroBob{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
.taskface{width:100%;text-align:left;border:2px solid var(--ink);border-radius:14px;overflow:hidden;background:#FFFDF8;color:#2E2A47}
.taskface .band{padding:10px 14px;font:600 22px var(--display);border-bottom:2px solid #2E2A47}
.taskface p{padding:12px 14px 14px;font-size:17px;line-height:1.4}
.herocard{background:none;border:0;padding:0}
.group{background:var(--surface);border:1.5px solid var(--line);border-radius:18px;overflow:hidden;margin-bottom:16px}
.rowl{display:flex;gap:12px;align-items:center;width:100%;text-align:left;background:none;border:0;border-top:1px solid var(--line);padding:12px 14px;min-height:60px;color:inherit}
.group>.rowl:first-child{border-top:0}
.rowl .ri{width:38px;height:38px;flex:none;border-radius:11px;background:var(--chip);color:var(--plum);display:grid;place-items:center}
.rowl .ri svg{width:21px;height:21px}
.rowl.ready .ri{background:var(--butter);color:#2E2A47}
.rowl .rt{min-width:0;flex:1}
.rowl b{display:block;font:600 16px/1.25 var(--display)}
.rowl .rs{display:block;color:var(--muted);font-size:14px;line-height:1.35;margin-top:2px}
.rowl .chev{flex:none;color:var(--muted);font-size:22px;line-height:1}
.rowl .pips{margin:6px 0 0;gap:5px}.rowl .pip{height:7px}
.summary{color:var(--muted);font-size:15px;margin:0 2px 6px}
details.more{margin-top:10px;border-top:1px solid var(--line)}
details.more>summary{min-height:44px;display:flex;align-items:center;font-weight:700;color:var(--plum);cursor:pointer;list-style:none}
details.more>summary::-webkit-details-marker{display:none}
details.more>summary::after{content:'+';margin-left:auto;font-size:20px;font-weight:600}
details.more[open]>summary::after{content:'\2013'}
'''
rep('/* Nav */', CSS + '\n/* Nav */')

# ---- Today ----
start = src.index('function renderToday(){'); end = src.index('  hydrate(el);\n}', start) + len('  hydrate(el);\n}')
TODAY = r'''function renderToday(){
  const V=VECTORS[state.todayV],s=state.status,el=$('#view-today');
  const EMB='<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l7 6-7 12L5 9z"/><path d="M5 9h14M9 9l3 12M15 9l-3 12"/></svg>';
  const IC={hearth:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3c1 3.5 5 5.5 5 10a5 5 0 0 1-10 0c0-2 1-3.2 2-4.2 0 2 1 3 2 3 0-3-1-5 1-8.8z"/></svg>',
    map:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 6.5l6-2.5 6 2.5 6-2.5v13.5l-6 2.5-6-2.5-6 2.5z"/><path d="M9 4v13.5M15 6.5V20"/></svg>',
    pack:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="3" width="16" height="18" rx="2"/><path d="M4 7h16M12 11l2.5 2-2.5 4-2.5-4z"/></svg>'};
  let hero='';
  if(s==='fresh')hero=`<button class="heroback pixcut" id="btnTurn" aria-label="Turn over today's card">${EMB}<span>Today's card</span></button><h2>Today's card is waiting</h2><p class="muted">Turn it over to see today's small thing.</p><button class="primary" id="btnTurnGo">Turn over today's card</button>`;
  else if(s==='revealed')hero=`<div class="taskface"><div class="band" style="background:${V.color}">${V.name}</div><p>${V.task}</p></div><div class="btnrow"><button class="primary" id="btnDone">I did it</button><button class="outline" id="btnAll">I went all in</button></div><p class="muted small">Going all in nudges your odds toward rarer Forgelings. The exact odds are in Settings.</p><div class="row" style="width:100%"><button class="ghost" id="btnCard">See the full card</button><button class="ghost" id="btnRest">Rest today</button></div>`;
  else if(s==='done'){const c=cardById(state.todayCard);hero=`${c?`<button class="herocard" id="btnShowToday" aria-label="Look at today's Forgeling">${cardHTML(c,{w:136,mini:true})}</button>`:''}<h2>${c?esc(c.nick||c.name)+' joined your binder':'Today’s Forgeling is in your binder'}</h2><p class="muted">${esc(mirrorLine()||'Come back tomorrow for the next card.')}</p>${state.packs>0?`<button class="primary" id="btnPack">Open ${state.packs>1?'a pack ('+state.packs+' ready)':'your pack'}</button>`:''}<div style="width:100%;text-align:left">${echoHTML()}</div>`;}
  else hero=`<h2>Resting today</h2><p class="muted">Your progress is safe and nothing is lost. A new card arrives tomorrow.</p><button class="ghost" id="btnUnrest">Actually, show me today's card</button><div style="width:100%;text-align:left">${echoHTML()}</div>`;
  const row=(id,ic,title,sub,extra,ready)=>`<button class="rowl${ready?' ready':''}" ${id?`id="${id}"`:'disabled'}><span class="ri">${ic}</span><span class="rt"><b>${title}</b><span class="rs">${sub}</span>${extra||''}</span>${id?'<span class="chev" aria-hidden="true">›</span>':''}</button>`;
  const pips=[0,1,2,3,4].map(i=>`<span class="pip${i<state.progress?' on':''}"></span>`).join('');
  const rows=[];
  if(state.packs>0&&s!=='done')rows.push(row('btnPack',IC.pack,'A pack is ready','Five new Forgelings, earned by showing up.','',true));
  else if(state.packs===0)rows.push(row('',IC.pack,'Next pack',`${5-state.progress} more ${5-state.progress===1?'day':'days'} to go. Rest days and missed days never reset this.`,`<div class="pips" role="img" aria-label="${state.progress} of 5 days toward your next pack">${pips}</div>`));
  if(state.cards.length){const hv=visitsLeft(),wl=wTodayLine().replace(/<[^>]+>/g,'');rows.push(row('btnHearth',IC.hearth,'The Hearth',(state.hearth.sleep?'The fire has burned low and your Forgelings are asleep.':hv>0?`${hv} ${hv===1?'visit':'visits'} left today.`:'The fire is low for today.')+(wl?' '+wl:'')));}
  if(state.cards.length&&state.settings.lore!==false)rows.push(row('btnMapGo',IC.map,'The Map',esc(mapLatest()||'Nothing new in the margin today.')));
  const jr=state.journal[state.date],reflect=s!=='fresh'?`<div class="panel-box"><h2>In the margin</h2><p class="muted"><i>The Forge asks:</i> ${esc(V.question)}</p>${jr&&!ui.editJ?`<p class="mine">“${esc(jr.text)}”</p><button class="ghost" id="jEdit" style="padding-left:0">Edit</button>`:`<label class="field" style="margin-top:8px"><span>Write one line in the margin. It stays on this device.</span><input id="jIn" maxlength="200" value="${esc(jr?jr.text:'')}" placeholder="Whatever comes to mind" autocomplete="off"></label><div class="row"><button class="pill" id="jSave">Save</button></div>`}</div>`:'';
  const latest=state.cards.slice(-5).reverse(),done=state.history.filter(h=>h.status==='done').length;
  el.innerHTML=`<div class="herowrap"><div class="hero pixcut">${hero}</div></div>${reflect}<div class="group">${rows.join('')}</div>
    <div class="row" style="margin:0 2px 14px"><div class="dots" aria-label="This week">${weekDots()}</div><span class="muted small">${done} ${done===1?'day':'days'} showed up</span></div>
    ${latest.length?`<h3 style="margin-top:6px">Latest finds</h3><div class="latest">${latest.map(c=>`<button data-insp="${c.id}" aria-label="Look at ${esc(c.name)}">${cardHTML(c,{w:92,mini:true})}</button>`).join('')}</div>`:''}`;
  hydrate(el);
}'''
src = src[:start] + TODAY + src[end:]
rep("  if(b.id==='btnTurn'||b.id==='btnCard')openVector();", "  if(b.id==='btnTurn'||b.id==='btnTurnGo'||b.id==='btnCard')openVector();")
rep('.echo{margin-top:14px;padding-top:12px;border-top:1.5px dashed var(--line)}', '.echo{margin-top:10px;padding-top:12px;border-top:1.5px dashed var(--line)}')

# ---- Hearth: fold away what is not needed every visit ----
rep('<div class="lbl2">Curios, ${have} of ${CURIOS.length}</div>${shelf}</div>`;',
    '<details class="more"><summary>Curio shelf, ${have} of ${CURIOS.length}</summary>${shelf}</details></div>`;')
rep('<div class="lbl2">Keepsake</div><div class="chips" role="group" aria-label="Keepsake">${keeps}</div><div class="lbl2">Backdrop</div><div class="chips" role="group" aria-label="Backdrop">${bds}</div></div>`;',
    '<details class="more"><summary>Keepsakes and backdrops</summary><div class="lbl2">Keepsake</div><div class="chips" role="group" aria-label="Keepsake">${keeps}</div><div class="lbl2">Backdrop</div><div class="chips" role="group" aria-label="Backdrop">${bds}</div></details></div>`;')

# ---- Binder: counters as a sentence ----
rep('''el.innerHTML=`<div class="stat-line"><span class="stat-chip">${state.cards.length} Forgelings</span><span class="stat-chip">${rareUp} rare or better</span><span class="stat-chip">${types} of 12 types</span><span class="stat-chip">${themes} of ${THEMES.length*2} realms</span></div>''',
    '''el.innerHTML=`<p class="summary">${state.cards.length} ${state.cards.length===1?'Forgeling':'Forgelings'}, ${rareUp} rare or better. ${types} of 12 callings and ${themes} of ${THEMES.length*2} realms found.</p>''')


# ---- version and what is new ----
rep('<title>Forge (prototype 0.17.1)</title>', '<title>Forge (prototype 0.18.0)</title>')
rep("const VERSION='prototype 0.17.1';", "const VERSION='prototype 0.18.0';")
rep('const SEEN_V=20;', 'const SEEN_V=21;')
rep('''<ul class="newlist"><li><b>On this day.</b>''',
    '''<ul class="newlist"><li><b>A clearer Today.</b> Today's card is front and centre, with one button for the one thing to do. The pack, the Hearth and the map sit in a short list below it.</li>
    <li><b>A calmer Hearth.</b> Keepsakes, backdrops and the curio shelf fold away until you want them.</li>
    <li><b>Easier to tap.</b> Chips and small buttons are a little bigger.</li>
    <li><b>On this day.</b>''')

open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src))

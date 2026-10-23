# Forgelings 0.37.0: Ink (design doc https://claude.ai/artifact/Kt3TnuTRS44Ax69aMDsmy4, part 3 and part 4, all
# recommendations). Writing is never the price of a Forgeling; it is rewarded, counted in totals, never runs.
#  - How did it feel? Right after a done day, Today asks once, with three taps: Easy, Good, Hard (state.feel[date]).
#    A tap is part of your record: the Journal lists the day, and month summaries use it.
#  - Ink-touched Forgelings: on a day you write a line (not just a tap), today's Forgeling is ink-touched: a soft
#    ink wash at the card's edge, a small ink drop by its number, and your line on its back (c.ink). Nothing about
#    stats or odds changes. Clearing the line takes the ink away again.
#  - Your book: the Journal opens with your book, which grows with the total lines you have written: 1 a plain cover,
#    10 leather in your favourite realm's colour, 30 a ribbon that opens to an old line, 60 a promise of someone
#    coming to the fire (the Scribe, 0.38), 100 gold edges and a clasp.
#  - Your month in words: a short, warm summary of this month (and last month) with no charts or percentages.
# Reads base36.html.
src = open('base36.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

# ---- state ----
rep("want:[],wantAsked:false,owns:[],todayOwn:null,", "want:[],wantAsked:false,owns:[],todayOwn:null,feel:{},")
rep("Object.keys(s.journal).forEach", r"""{const f=s.feel&&typeof s.feel==='object'&&!Array.isArray(s.feel)?s.feel:{},ok={};Object.keys(f).filter(k=>/^\d{4}-\d{2}-\d{2}$/.test(k)&&['easy','good','hard'].includes(f[k])).sort().slice(-800).forEach(k=>ok[k]=f[k]);s.feel=ok;}
  Object.keys(s.journal).forEach""")
rep("c.own=str(c.own,'').slice(0,60);", "c.own=str(c.own,'').slice(0,60);if(c.ink!==undefined){c.ink=str(c.ink,'').slice(0,200);if(!c.ink)delete c.ink;}")

# ---- How did it feel?, on Today after a done day; the line link now promises ink ----
rep("  const jr=state.journal[state.date];if(s==='done'||s==='rest')hero+=`<button class=\"ghost marginlink\" id=\"btnMargin\">${jr?'Edit today’s line':'Add a line to your journal'}</button>`;",
    "  const jr=state.journal[state.date],fl=(state.feel||{})[state.date];if(s==='done')hero+=`<div class=\"feel\"><p class=\"feelq\">${fl?'Today felt '+fl+'.':'How did it feel?'}</p><div class=\"chips\" role=\"group\" aria-label=\"How did it feel?\">${FEELS.map(f=>`<button class=\"chip\" data-feel=\"${f}\" aria-pressed=\"${fl===f}\">${f[0].toUpperCase()+f.slice(1)}</button>`).join('')}</div></div>`;if(s==='done'||s==='rest')hero+=`<button class=\"ghost marginlink\" id=\"btnMargin\">${jr?'Edit today’s line':s==='done'&&state.todayCard?'Add a line, and ink today’s Forgeling':'Add a line to your journal'}</button>`;")
rep("  if(b.id==='btnWant'){openWant();return;}", "  if(b.id==='btnWant'){openWant();return;}\n  if(b.dataset.feel){const f=b.dataset.feel;if(!FEELS.includes(f))return;state.feel=state.feel||{};if(state.feel[state.date]===f)delete state.feel[state.date];else{state.feel[state.date]=f;chime(0);}save();renderToday();renderChronicle();const n=$(`#view-today [data-feel=\"${f}\"]`);if(n)n.focus({preventScroll:true});return;}")

# ---- ink: saving a line on a done day inks today's Forgeling ----
rep("  if(!t)delete state.journal[state.date];else state.journal[state.date]={v:state.todayV,text:t};",
    "  if(!t)delete state.journal[state.date];else state.journal[state.date]={v:state.todayV,text:t};\n  {const c=state.status==='done'&&state.todayCard?cardById(state.todayCard):null;if(c&&c.date===state.date){if(t)c.ink=t.slice(0,200);else delete c.ink;}}")
rep('<div class="tilt idle"><div class="card ${dk?\'dk\':\'ct\'} r-${R.id}${o.mini?\' mini\':\'\'}"', '<div class="tilt idle"><div class="card ${dk?\'dk\':\'ct\'} r-${R.id}${o.mini?\' mini\':\'\'}${c.ink?\' inked\':\'\'}"')
rep('<div class="foot"><span>${EDITION}</span><span>No. ${pad(c.serial)}</span></div>', '<div class="foot"><span>${EDITION}</span><span>${c.ink?INKDROP:\'\'}No. ${pad(c.serial)}</span></div>${c.ink?\'<div class="inkwash" aria-hidden="true"></div>\':\'\'}')
rep('<div class="face cbk${(c.tale||c.gossip)?\' dense\':\'\'}">', '<div class="face cbk${(c.tale||c.gossip||c.ink)?\' dense\':\'\'}">')
rep('${c.tale?`<div class="m3">\\u201C${esc(c.tale)}\\u201D</div>`:\'\'}', '${c.ink?`<div class="m3 inkl">\\u201C${esc(c.ink)}\\u201D</div>`:\'\'}${c.tale?`<div class="m3">\\u201C${esc(c.tale)}\\u201D</div>`:\'\'}')

# ---- the book, the month in words, the journal list with feelings ----
rep("function journalHTML(){", r"""const FEELS=['easy','good','hard'];
const INKDROP='<svg class="pi inkdrop" viewBox="0 0 6 8" width="6" height="8" aria-label="Ink-touched" role="img"><path fill="#B9A6FF" d="M2 0h2v2h-2zM1 2h4v2h-4zM0 4h6v3h-6zM1 7h4v1h-4z"/></svg>';
const linesWritten=()=>Object.values(state.journal||{}).filter(j=>j&&j.text).length;
const BOOK_AT=[1,10,30,60,100];
function favRealm(){const n=[0,0,0,0,0];state.cards.forEach(c=>{if(c.theme>=0&&c.theme<5)n[c.theme]++;});return n.indexOf(Math.max(...n));}
function bookSVG(L){
  const tier=BOOK_AT.filter(x=>L>=x).length,leather=['#3E7A4A','#A4471F','#2F5F8A','#5F7FA0','#5B3F8E'][favRealm()],cov=tier>=2?leather:'#7C7090',edge=tier>=5?'#FFD36B':'#F4ECD8';
  return `<svg class="pi book" viewBox="0 0 30 38" width="90" height="114" role="img" aria-label="Your book${tier>=2?', bound in leather':''}${tier>=3?', with a ribbon':''}${tier>=5?', gold edges and a clasp':''}">
    <path fill="#1A1430" d="M3 1h24v1h1v34h-1v1h-24v-1h-1v-34h1z"/><path fill="${edge}" d="M25 3h2v32h-2z"/><path fill="${cov}" d="M3 2h22v34h-22z"/><path fill="rgba(0,0,0,.25)" d="M3 2h3v34h-3z"/>
    <path fill="rgba(255,255,255,.18)" d="M8 8h14v1h-14zM8 29h14v1h-14z"/><path fill="${tier>=2?'#FFD36B':'#E9E2F4'}" d="M10 12h10v1h-10zM11 14h8v1h-8zM12 16h6v1h-6z"/>
    ${tier>=3?'<path fill="#D9475A" d="M19 0h2v6h-1v-1h-1zM19 36h2v2h-2z"/>':''}${tier>=5?'<path fill="#FFD36B" d="M23 17h4v4h-4z"/><path fill="#C98A12" d="M24 18h2v2h-2z"/>':''}</svg>`;
}
function bookHTML(){
  const L=linesWritten(),nx=BOOK_AT.find(x=>L<x),nxt={1:'Your first line gives it a cover.',10:'At 10 lines, it is bound in leather.',30:'At 30, it gets a ribbon that opens to an old line.',60:'At 60, someone will come to the fire to read with you.',100:'At 100, gold edges and a clasp.'}[nx]||'Every line from here is just for you.';
  return `<div class="panel-box bookp"><div class="bookrow">${bookSVG(L)}<div><h2>Your book</h2><p class="muted small">${L?`${L} ${L===1?'line':'lines'} written. Every line counts, whenever you write it.`:'Nothing written yet. Writing is never needed, and every line counts whenever you write it.'}</p><p class="muted small">${nxt}</p>${L>=30?'<button class="outline" id="bookRibbon" style="margin-top:6px">Open to an old line</button>':''}</div></div></div>`;
}
const MONTHS_L=['January','February','March','April','May','June','July','August','September','October','November','December'];
const ORD=['first','second','third','fourth','fifth','sixth'];
const timesW=n=>n===1?'once':n===2?'twice':`on ${n} days`;
function monthWords(ym){
  const inM=k=>typeof k==='string'&&k.slice(0,7)===ym,hs=state.history.filter(h=>h&&inM(h.date));
  const seen=new Set(),done=hs.filter(h=>h.status==='done'&&!seen.has(h.date)&&seen.add(h.date)).length,rest=hs.filter(h=>h.status==='rest').length;
  const fe=Object.keys(state.feel||{}).filter(inM),cnt={easy:0,good:0,hard:0};fe.forEach(k=>cnt[state.feel[k]]++);
  const lines=Object.keys(state.journal||{}).filter(k=>inM(k)&&state.journal[k].text).length;
  if(!done&&!rest&&!fe.length&&!lines)return '';
  const mn=MONTHS_L[+ym.slice(5,7)-1],out=[];
  out.push(`In ${mn} you showed up on ${done} ${done===1?'day':'days'}${rest?`, and rested on ${rest}`:''}.`);
  (state.owns||[]).forEach(o=>{const n=o.days.filter(inM).length;if(n)out.push(`You did “${esc(o.text)}” ${timesW(n)}.`);});
  if(fe.length>=3){const top=['good','easy','hard'].sort((a,b)=>cnt[b]-cnt[a])[0];out.push(top==='hard'?'A lot of it was hard, and you did it anyway.':`Most days felt ${top}.`);
    if(cnt.hard>=2){const wk=[0,0,0,0,0,0];fe.forEach(k=>{if(state.feel[k]==='hard')wk[Math.floor((+k.slice(8,10)-1)/7)]++;});out.push(`Your hardest week was the ${ORD[wk.indexOf(Math.max(...wk))]}.`);}}
  if(lines)out.push(`You wrote ${lines} ${lines===1?'line':'lines'} in your book.`);
  return out.join(' ');
}
function monthHTML(){
  const k=todayKey(),cur=k.slice(0,7),d=new Date(k+'T00:00:00');d.setDate(1);d.setMonth(d.getMonth()-1);const prev=dkey(d).slice(0,7);
  const a=monthWords(cur),p=monthWords(prev);if(!a&&!p)return '';
  return `<div class="panel-box"><h2>Your month in words</h2>${a?`<p>${a}</p>`:''}${p?`<details class="more"><summary>${MONTHS_L[+prev.slice(5,7)-1]}</summary><p style="margin:4px 0 8px">${p}</p></details>`:''}</div>`;
}
function openRibbon(){
  const ks=Object.keys(state.journal).filter(k=>state.journal[k].text&&k!==state.date);if(!ks.length){toast('Your book opens to today. Older lines will be here.');return;}
  const k=ks[Math.floor(Math.random()*ks.length)],e=state.journal[k];
  openSheet(`<p class="muted center small">The ribbon falls open at</p><h2 class="center">${esc(dateLabel(k))}</h2><p class="mine" style="margin:12px 0">“${esc(e.text)}”</p>${(state.feel||{})[k]?`<p class="muted small center">It felt ${state.feel[k]} that day.</p>`:''}<div class="stack"><button class="primary" data-close>Close the book</button></div>`);
}
function journalHTML(){""")
rep("const journeyHTML=()=>recapHTML()+calendarHTML()+ribbonsHTML();", "const journeyHTML=()=>bookHTML()+monthHTML()+recapHTML()+calendarHTML()+ribbonsHTML();")
rep("  const ks=Object.keys(state.journal).sort().reverse();\n  if(!ks.length)return",
    "  const ks=[...new Set(Object.keys(state.journal).concat(Object.keys(state.feel||{})))].sort().reverse();\n  if(!ks.length)return")
i = src.index("  return '<p class=\"muted small\" style=\"margin-bottom:8px\">Private. Only on this device.</p>'+ks.slice(0,40).map(k=>{const e=state.journal[k],V=VECTORS[e.v];")
j = src.index("\n}", i)
src = src[:i] + r"""  return '<p class="muted small" style="margin-bottom:8px">Private. Only on this device.</p>'+ks.slice(0,40).map(k=>{const e=state.journal[k],h=state.history.find(x=>x.date===k),vv=e&&VECTORS[e.v]?e.v:h&&VECTORS[h.v]?h.v:0,V=VECTORS[vv],f=(state.feel||{})[k];
    return `<div class="calling" style="--rc:${V.color}"><div class="row" style="margin:0"><b>${V.name}</b><span class="muted small">${esc(dateLabel(k))}</span></div>${e?`<p class="muted small" style="margin:4px 0">${esc(V.question)}</p><p class="mine">“${esc(e.text)}”</p>`:''}${f?`<p class="muted small feelc">Felt ${f}.</p>`:''}${e&&e.reply?`<p class="later">${LATER[e.reply]}</p>`:''}</div>`;}).join('');""" + src[j:]
# the ribbon button lives in the Map view (Journal sub-tab)
rep("  const rh=e.target.closest('.mphit');", "  if(e.target.closest('#bookRibbon')){openRibbon();return;}\n  const rh=e.target.closest('.mphit');")

# ---- styles ----
rep('/* Nav */', """.feel{width:100%;margin-top:6px}.feel .feelq{font-weight:700;margin:0 0 2px}.feel .chips{justify-content:center}
.card .inkwash{position:absolute;inset:0;pointer-events:none;z-index:2;box-shadow:inset 0 0 0 .2em rgba(200,184,255,.85),inset 0 0 2.4em .7em rgba(96,64,205,.72),inset 0 0 .7em .2em rgba(185,166,255,.7)}
.card .inkdrop{vertical-align:-.05em;margin-right:.35em;width:.6em;height:.8em}
.card .cbk .binfo .inkl{color:#D9CCFF;font-style:italic}
.bookrow{display:flex;gap:14px;align-items:center}.bookrow .book{flex:none;filter:drop-shadow(0 4px 0 rgba(0,0,0,.25))}.bookrow h2{margin:0 0 2px}
.feelc{margin:4px 0 0}
/* Nav */""")

# ---- report ----
rep("\\nCard mix: ${state.settings.ownMix||'mix'}", "\\nCard mix: ${state.settings.ownMix||'mix'}\\nLines written: ${linesWritten()}\\nFeelings noted: ${Object.keys(state.feel||{}).length}\\nInk-touched Forgelings: ${state.cards.filter(c=>c.ink).length}")

# ---- version, What's New ----
rep('<title>Forgelings (prototype 0.36.0)</title>', '<title>Forgelings (prototype 0.37.0)</title>')
rep("const VERSION='prototype 0.36.0'", "const VERSION='prototype 0.37.0'")
rep('const SEEN_V=41;', 'const SEEN_V=42;')
rep("""<ul class="newlist"><li><b>Your small things.</b>""",
    """<ul class="newlist"><li><b>Ink.</b> After a done day, tap how it felt. Write a line too, and that day’s Forgeling is ink-touched, with your words on its back. Your Journal now opens with your book, which grows as you write, and a short note on your month, in words. Writing is never needed, and every line counts whenever you write it.</li>
    <li><b>Your small things.</b>""")
import re
_i=src.index('<ul class="newlist">'); _j=src.index('</ul>',_i)
_items=re.findall(r'\s*<li>.*?</li>',src[_i+len('<ul class="newlist">'):_j],re.S)
src=src[:_i]+'<ul class="newlist">'+''.join(_items[:8])+src[_j:]
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src.encode()))

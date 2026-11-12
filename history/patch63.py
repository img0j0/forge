# 0.63: the question and the journal that writes itself (Hunter, November 12, by voice: he rarely writes journal lines;
#   the design doc "Forgelings: reworking the daily card and journal", Parts 2 and 3; his answers: the answer nudges the
#   next wander, and the Scribe arrives at 60 days of entries so everyone meets it).
#   After today's card is done, today's companion asks one small question with three tap answers (twenty questions
#   rotate; every third day it is How did it feel?, which replaces the old faces, so it is still one tap). The answer
#   colours the companion's mood at the Hearth, and the next "Anywhere" wander leans toward a realm that fits it (most
#   of the time it finds something new from there; the wander sheet says so).
#   Every done day now gets a journal entry written for you, from the day's calling, who came to the fire, your answer
#   and the feeling, written when shown so it reads in any language. Your own words stay optional ("Add your own words")
#   and appear beside the entry in your hand. The Book grows by pages (days in the journal) rather than written lines,
#   and the Scribe and its ribbon come at 60 pages. Old lines and feelings are kept and shown as before.
import re,subprocess,os
S=open('base62.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.62.0'","const VERSION='prototype 0.63.0'")
rep("<title>Forgelings (prototype 0.62.0)</title>","<title>Forgelings (prototype 0.63.0)</title>")

# ---------- the questions ----------
rep("const FEELS=['easy','good','hard'];","""const FEELS=['easy','good','hard'];
/* 0.63: today's question. Each answer: [the chip, the journal's sentence, the realm it leans toward
   (0 Meadow: people, 1 Ember: making, 2 Tide: rest, 3 Frost: clarity, 4 Dusk: dreams)]. */
const ASKS=[
 {q:'What made today a bit better?',a:[['Someone','Someone made today a bit better.',0],['A pause','A pause made today a bit better.',2],['Something I made','Making something made today better.',1]]},
 {q:'Where was your head today?',a:[['With people','Your head was with people.',0],['Somewhere quiet','Your head was somewhere quiet.',3],['Far away','Your head was far away, dreaming.',4]]},
 {q:'What did you need most today?',a:[['Company','What you needed most was company.',0],['Rest','What you needed most was rest.',2],['Focus','What you needed most was focus.',3]]},
 {q:'What would you like more of tomorrow?',a:[['Time with people','Tomorrow, you would like more time with people.',0],['Calm','Tomorrow, you would like more calm.',2],['Something new','Tomorrow, you would like something new.',4]]},
 {q:'How was your energy?',a:[['Bright','Your energy was bright.',1],['Steady','Your energy was steady.',2],['Low, and that is fine','Your energy was low, and that was fine.',3]]},
 {q:'What did today sound like?',a:[['Voices','Today sounded like voices and laughter.',0],['Quiet','Today sounded quiet.',3],['Busy hands','Today sounded like busy hands.',1]]},
 {q:'What did you notice today?',a:[['A kindness','You noticed someone being kind.',0],['Something lovely','You noticed something lovely.',4],['Something to fix','You noticed something that needs fixing.',1]]},
 {q:'What would your Forgeling bring you?',a:[['A warm drink','Your Forgeling would bring you a warm drink.',2],['A good idea','Your Forgeling would bring you a good idea.',4],['A friend','Your Forgeling would bring you a friend.',0]]},
 {q:'What kind of day was it?',a:[['A making day','It was a making day.',1],['A people day','It was a people day.',0],['A thinking day','It was a thinking day.',3]]},
 {q:'What helped you keep going?',a:[['Someone cheering','Someone cheering helped you keep going.',0],['A small win','A small win helped you keep going.',1],['A quiet moment','A quiet moment helped you keep going.',2]]},
 {q:'Where would you like to be right now?',a:[['By the sea','Right now, you would like to be by the sea.',2],['Under the stars','Right now, you would like to be under the stars.',4],['With friends','Right now, you would like to be with friends.',0]]},
 {q:'What did you let go of today?',a:[['A worry','You let go of a worry.',2],['An old habit','You let go of an old habit.',1],['Nothing yet','You have not let go of anything yet, and that is fine.',3]]},
 {q:'What are you proud of today?',a:[['Showing up','You are proud you showed up.',1],['Being kind','You are proud you were kind.',0],['Staying calm','You are proud you stayed calm.',2]]},
 {q:'What is on your mind tonight?',a:[['Someone I care about','Someone you care about is on your mind.',0],['Tomorrow','Tomorrow is on your mind.',3],['A daydream','A daydream is on your mind.',4]]},
 {q:'What did you give today?',a:[['Time','You gave your time.',0],['Effort','You gave your effort.',1],['Patience','You gave your patience.',2]]},
 {q:'What would make tomorrow easy?',a:[['An early start','An early start would make tomorrow easy.',3],['A slow morning','A slow morning would make tomorrow easy.',2],['A friend nearby','A friend nearby would make tomorrow easy.',0]]},
 {q:'What colour was today?',a:[['Warm gold','Today was warm gold.',1],['Soft blue','Today was soft blue.',2],['Deep purple','Today was deep purple.',4]]},
 {q:'What did you learn today?',a:[['About someone','You learned something about someone.',0],['About myself','You learned something about yourself.',4],['Something useful','You learned something useful.',3]]},
 {q:'What did you make room for?',a:[['Rest','You made room for rest.',2],['People','You made room for people.',0],['Ideas','You made room for ideas.',4]]},
 {q:'How were you to yourself today?',a:[['Kind','You were kind to yourself.',2],['Brave','You were brave.',1],['Patient','You were patient with yourself.',3]]}];
const ASK_FEEL={q:'How did today’s small thing feel?',feel:1,a:[['Easy','It felt easy.',2],['Good','It felt good.',0],['Hard','It felt hard, and you did it anyway.',1]]};
/* the question for a day: every third day the feeling, otherwise the twenty in a shuffled order that only repeats
   after all twenty have come */
function askFor(k){const d=dnum(k);if(d%3===0)return ASK_FEEL;const n=ASKS.length,cyc=Math.floor(d/n),pos=d%n;
  const ord=[...Array(n).keys()];const r=mulberry32(cyc*7919+13);for(let i=n-1;i>0;i--){const j=Math.floor(r()*(i+1));[ord[i],ord[j]]=[ord[j],ord[i]];}
  return ASKS[ord[pos]];}
const askAns=k=>{const a=(state.ask||{})[k],Q=askFor(k);return a&&Number.isInteger(a.a)&&Q.a[a.a]?Q.a[a.a]:null;};
const MOOD_L=['{n} keeps glancing at the gate, as if a friend might come by.','{n} is fiddling with something, itching to make it.','{n} settles down, slow and easy.','{n} sits very still, thinking clearly.','{n} gazes up at the sky, dreaming a little.'];
const MOOD_LD=['{n} watches the gate. Friends are welcome here.','{n} sharpens something, ready to make.','{n} rests its heavy head and breathes slowly.','{n} stares into the dark, seeing it clearly.','{n} looks up, somewhere far away.'];
/* ---------- the journal that writes itself ---------- */
const FEEL_ENTRY={easy:'It felt easy.',good:'It felt good.',hard:'It felt hard, and you did it anyway.'};
/* the days that have a page: every done day, and any day with your own words */
function entryDays(){const s=new Set(Object.keys(state.journal||{}).filter(k=>state.journal[k]&&state.journal[k].text));state.history.forEach(h=>{if(h&&h.status==='done')s.add(h.date);});return s;}
function entryLine(k){
  const h=state.history.find(x=>x&&x.date===k&&x.status==='done');if(!h)return '';
  const V=VECTORS[h.v]||VECTORS[0],c=h.card!=null?cardById(h.card):null,n=c?(c.nick||c.name):'',out=[];
  out.push(c&&c.own?`You did your own small thing: \\u201C${c.own}\\u201D.`:`A ${V.name} day.`);
  if(c)out.push(h.allIn?`You went all in, and ${n} came to the fire.`:`${n} came to the fire.`);
  const a=askAns(k),f=(state.feel||{})[k];
  if(a)out.push(a[1]);
  if(f&&FEEL_ENTRY[f]&&!(askFor(k).feel&&a))out.push(FEEL_ENTRY[f]);
  return out.join(' ').replace(/([。！？]) /g,'$1');}
function askHTML(){
  const k=state.date,Q=askFor(k),a=askAns(k),c=companion()||mateNow(),n=c?(c.nick||c.name):'';
  if(!a){const btns=Q.feel?FEELS.map((f,i)=>`<button class="facebtn" data-ask="${i}">${pixSVG(FACE[f][1],FACE[f][0],'feelface')}<span>${FEEL_L[f]}</span></button>`).join(''):Q.a.map((x,i)=>`<button class="chip askchip" data-ask="${i}">${x[0]}</button>`).join('');
    return `<div class="feel ask"><p class="feelq">${n?`${esc(n)} asks: ${Q.q}`:Q.q}</p><div class="chips" role="group" aria-label="${Q.q}">${btns}</div></div>`;}
  const jr=state.journal[k];
  return `<div class="feel ask done"><p class="muted small" style="margin:0">Today’s page</p><p class="world entry">${esc(entryLine(k))}</p>${jr&&jr.text?`<p class="mine">\\u201C${esc(jr.text)}\\u201D</p>`:''}<button class="ghost" id="askAgain" style="min-height:44px">Change the answer</button></div>`;}
function askAnswer(i){
  const k=state.date,Q=askFor(k);if(!Q.a[i])return;state.ask=state.ask||{};state.ask[k]={a:i};
  if(Q.feel){state.feel=state.feel||{};state.feel[k]=FEELS[i];}
  const r=Q.a[i][2];state.lean={r,date:k};
  const c=companion()||mateNow();if(c){const L=c.dark?MOOD_LD:MOOD_L;hf.msg=L[r].replace(/\\{n\\}/g,c.nick||c.name);}
  chime(0);save();renderToday();renderChronicle();renderHearth();checkRibbons();}""")

# Today: the question replaces the faces; the margin link becomes "Add your own words"
rep("""if(s==='done')hero+=`<div class="feel"><p class="feelq">${fl&&FEEL_TODAY[fl]?FEEL_TODAY[fl]:'How did it feel?'}</p><div class="chips" role="group" aria-label="How did it feel?">${FEELS.map(f=>`<button class="facebtn" data-feel="${f}" aria-pressed="${fl===f}">${pixSVG(FACE[f][1],FACE[f][0],'feelface')}<span>${FEEL_L[f]}</span></button>`).join('')}</div></div>`;if(s==='done'||s==='rest')hero+=`<button class="ghost marginlink" id="btnMargin">${jr?'Edit today’s line':s==='done'&&state.todayCard?'Add a line, and ink today’s Forgeling':'Add a line to your journal'}</button>`;""",
"""if(s==='done')hero+=askHTML();if(s==='done'||s==='rest')hero+=`<button class="ghost marginlink" id="btnMargin">${jr?'Edit your own words':s==='done'&&state.todayCard?'Add your own words, and ink today’s Forgeling':'Add your own words to the journal'}</button>`;""")
rep("""  if(b.dataset.feel){""","""  if(b.dataset.ask!==undefined){askAnswer(+b.dataset.ask);const q=$('#view-today .ask');if(q){const t=q.querySelector('button,[tabindex]');if(t)t.focus({preventScroll:true});}return;}
  if(b.id==='askAgain'){const k=state.date;if(state.ask)delete state.ask[k];if(askFor(k).feel&&state.feel)delete state.feel[k];if(state.lean&&state.lean.date===k)state.lean=null;save();renderToday();renderChronicle();const q=$('#view-today [data-ask]');if(q)q.focus({preventScroll:true});return;}
  if(b.dataset.feel){""")

# the Book, the Scribe and its ribbon count pages
rep("const scribeHere=()=>linesWritten()>=SCRIBE_AT;","const scribeHere=()=>entryDays().size>=SCRIBE_AT;")
rep("""  const L=linesWritten(),nx=BOOK_AT.find(x=>L<x),nxt={1:'Your first line gives it a cover.',10:'At 10 lines, it is bound in leather.',30:'At 30, it gets a ribbon that opens to an old line.',60:'At 60, someone will come to the fire to read with you.',100:'At 100, gold edges and a clasp.'}[nx]||'Every line from here is just for you.';""",
"""  const L=entryDays().size,nx=BOOK_AT.find(x=>L<x),nxt={1:'Your first page gives it a cover.',10:'At 10 pages, it is bound in leather.',30:'At 30, it gets a ribbon that opens to an old page.',60:'At 60, someone will come to the fire to read with you.',100:'At 100, gold edges and a clasp.'}[nx]||'Every page from here is just for you.';""")
rep("""${L?`${L} ${L===1?'line':'lines'} written. Every line counts, whenever you write it.`:'Nothing written yet. Writing is never needed, and every line counts whenever you write it.'}""",
"""${L?`${L} ${L===1?'page':'pages'} in your journal. Every day you show up writes one for you.`:'No pages yet. Every day you show up writes one for you.'}""")
rep("""${L>=30?'<button class="outline" id="bookRibbon" style="margin-top:6px">Open to an old line</button>':''}""","""${L>=30?'<button class="outline" id="bookRibbon" style="margin-top:6px">Open to an old page</button>':''}""")
rep("""{id:'scribe',name:'The Scribe',desc:'Write 60 lines in your book, whenever you like.',g:60,f:()=>linesWritten()},""","""{id:'scribe',name:'The Scribe',desc:'Fill 60 pages of your journal, whenever you like.',g:60,f:()=>entryDays().size},""")
# the Scribe reads your own words when there are some, else a written page
rep("""  const ks=Object.keys(state.journal).filter(j=>state.journal[j].text&&dayDiff(j,k)>=7).sort();if(!ks.length)return '';
  const pool=ks.filter(j=>dayDiff(j,k)>=14),pick=(pool.length?pool:ks)[whash(dnum(k)*13)%((pool.length?pool:ks).length)],t=state.journal[pick].text,d=dayDiff(pick,k);""",
"""  const own=Object.keys(state.journal).filter(j=>state.journal[j].text&&dayDiff(j,k)>=7);const ks=(own.length?own:[...entryDays()].filter(j=>dayDiff(j,k)>=7)).sort();if(!ks.length)return '';
  const pool=ks.filter(j=>dayDiff(j,k)>=14),pick=(pool.length?pool:ks)[whash(dnum(k)*13)%((pool.length?pool:ks).length)],t=(state.journal[pick]&&state.journal[pick].text)||entryLine(pick),d=dayDiff(pick,k);""")
# the ribbon opens to an old page: your words if any, else the written page
rep("""  const ks=Object.keys(state.journal).filter(k=>state.journal[k].text&&k!==state.date);if(!ks.length){toast('Your book opens to today. Older lines will be here.');return;}
  const k=ks[Math.floor(Math.random()*ks.length)],e=state.journal[k];""","""  const ks=[...entryDays()].filter(k=>k!==state.date);if(!ks.length){toast('Your book opens to today. Older pages will be here.');return;}
  const k=ks[Math.floor(Math.random()*ks.length)],e=(state.journal[k]&&state.journal[k].text)?state.journal[k]:{text:entryLine(k)};""")
# the Scribe's arrival, for writers and everyone else
rep("""  state.cards.push(c);state.todayCard=c.id;state.status='done';seasonPress();""","""  const pagesWere=entryDays().size;state.cards.push(c);state.todayCard=c.id;state.status='done';seasonPress();
  if(pagesWere<SCRIBE_AT&&!(state.journal[state.date]&&state.journal[state.date].text)&&pagesWere+1>=SCRIBE_AT){ui.scribeArr=true;hf.msg='Someone new has come to the fire. It carries a quill, and it would like to read with you.';}""")
rep("""  const wasL=linesWritten();""","""  const wasL=entryDays().size;""")
rep("""  ui.scribeArr=wasL<SCRIBE_AT&&linesWritten()>=SCRIBE_AT;""","""  ui.scribeArr=wasL<SCRIBE_AT&&entryDays().size>=SCRIBE_AT;""")
rep("""toast(ui.scribeArr?'Sixty lines. The Scribe has come to your Hearth.':""","""toast(ui.scribeArr?'Sixty pages. The Scribe has come to your Hearth.':""")

# the journal: every page, with the written entry and your words beside it
rep("""  const ks=[...new Set(Object.keys(state.journal).concat(Object.keys(state.feel||{})))].sort().reverse();
  if(!ks.length)return '<p class="muted">Your journal starts with the first question you answer on the Today screen. It stays on this device.</p>';
  const more=!all&&ks.length>3?`<button class="outline" id="jLines" style="width:100%;margin-top:6px">All your lines (${Math.min(ks.length,40)})</button>`:'';
  return '<h2 class="sub3" style="margin-top:14px">Your lines</h2><p class="muted small" style="margin-bottom:8px">Private. Only on this device.</p>'+ks.slice(0,all?40:3).map(k=>{const e=state.journal[k],h=state.history.find(x=>x.date===k),vv=e&&VECTORS[e.v]?e.v:h&&VECTORS[h.v]?h.v:0,V=VECTORS[vv],f=(state.feel||{})[k];
    return `<div class="calling" style="--rc:${V.color}"><div class="row" style="margin:0"><b>${V.name}</b><span class="muted small">${esc(dateLabel(k))}</span></div>${e?`<p class="muted small" style="margin:4px 0">${esc(V.question)}</p><p class="mine">“${esc(e.text)}”</p>`:''}${FEEL_SHORT[f]?`<p class="muted small feelc">${FEEL_SHORT[f]}</p>`:''}${e&&e.reply?`<p class="later">${LATER[e.reply]}</p>`:''}</div>`;}).join('')+more;""",
"""  const ks=[...new Set([...entryDays()].concat(Object.keys(state.feel||{})))].sort().reverse();
  if(!ks.length)return '<p class="muted">Your journal starts with your first card. Every day you show up writes a page. It stays on this device.</p>';
  const more=!all&&ks.length>3?`<button class="outline" id="jLines" style="width:100%;margin-top:6px">All your pages (${Math.min(ks.length,40)})</button>`:'';
  return '<h2 class="sub3" style="margin-top:14px">Your pages</h2><p class="muted small" style="margin-bottom:8px">Private. Only on this device.</p>'+ks.slice(0,all?40:3).map(k=>{const e=state.journal[k]&&state.journal[k].text?state.journal[k]:null,h=state.history.find(x=>x.date===k),vv=e&&VECTORS[e.v]?e.v:h&&VECTORS[h.v]?h.v:0,V=VECTORS[vv],f=(state.feel||{})[k],w=entryLine(k);
    return `<div class="calling" style="--rc:${V.color}"><div class="row" style="margin:0"><b>${V.name}</b><span class="muted small">${esc(dateLabel(k))}</span></div>${w?`<p class="world small" style="margin:4px 0">${esc(w)}</p>`:''}${e?`<p class="mine">“${esc(e.text)}”</p>`:''}${!w&&FEEL_SHORT[f]?`<p class="muted small feelc">${FEEL_SHORT[f]}</p>`:''}${e&&e.reply?`<p class="later">${LATER[e.reply]}</p>`:''}</div>`;}).join('')+more;""")

# the margin sheet: your own words, optional
rep("""  openSheet(`<h2>In the margin</h2><p class="muted"><i>The Forge asks:</i> ${esc(V.question)}</p>
    <label class="field" style="margin-top:10px"><span>Write one line. It stays on this device, in your Journal.</span>""",
"""  openSheet(`<h2>Your own words</h2><p class="muted small">Today’s page is already written. Add a line of your own if you like: it sits beside the page, in your hand.</p><p class="muted"><i>The Forge asks:</i> ${esc(V.question)}</p>
    <label class="field" style="margin-top:10px"><span>One line. It stays on this device, in your Journal.</span>""")

# wanders: the next Anywhere wander leans toward the realm today's answer fits
rep("""  state.wander={id:c.id,start:now,ready:now+((state.wstat.sent||0)===0?20*60*1000:WANDER_MS),seed:((now^((c.seed|0)*2654435761))>>>0),notified:false,realm:to};""",
"""  const lean=to<0&&state.lean&&Number.isInteger(state.lean.r)?state.lean.r:-1;if(to<0)state.lean=null;
  state.wander={id:c.id,start:now,ready:now+((state.wstat.sent||0)===0?20*60*1000:WANDER_MS),seed:((now^((c.seed|0)*2654435761))>>>0),notified:false,realm:to,lean};""")
rep("""  const pool=unfound.length?unfound:owned.length?owned:fresh||!anyOwned.length?base:anyOwned,cu=pool[Math.floor(r()*pool.length)];""",
"""  const lu=to<0&&w.lean>=0&&w.lean<=4?unfound.filter(x=>rCurios(w.lean).some(y=>y.id===x.id)):[];
  const pool=lu.length&&r()<.75?lu:unfound.length?unfound:owned.length?owned:fresh||!anyOwned.length?base:anyOwned,cu=pool[Math.floor(r()*pool.length)];""")
rep("""    <button class="moodbtn" data-wgo="-1">${iconSVG(['spark','#C9B8FF'])}<div><b>Anywhere</b><span>Wherever the path goes. Good for finding something new.</span></div></button>""",
"""    <button class="moodbtn" data-wgo="-1">${iconSVG(['spark','#C9B8FF'])}<div><b>Anywhere</b><span>${state.lean&&state.lean.r>=0&&state.lean.r<=4?`After what you said today, ${esc(n)} feels drawn toward ${esc(rName(state.lean.r))}.`:'Wherever the path goes. Good for finding something new.'}</span></div></button>""")

# the save
rep("""  if(s.wander)s.wander.realm=Number.isInteger(s.wander.realm)&&s.wander.realm>=0&&s.wander.realm<=9?s.wander.realm:-1;""",
"""  if(s.wander)s.wander.realm=Number.isInteger(s.wander.realm)&&s.wander.realm>=0&&s.wander.realm<=9?s.wander.realm:-1;
  if(s.wander)s.wander.lean=Number.isInteger(s.wander.lean)&&s.wander.lean>=0&&s.wander.lean<=4?s.wander.lean:-1;
  if(s.ask!==undefined){if(!s.ask||typeof s.ask!=='object'||Array.isArray(s.ask))s.ask={};else Object.keys(s.ask).forEach(k=>{const v=s.ask[k];if(!/^\\d{4}-\\d{2}-\\d{2}$/.test(k)||!v||!Number.isInteger(v.a)||v.a<0||v.a>2)delete s.ask[k];});}
  if(s.lean!==undefined&&s.lean!==null&&(typeof s.lean!=='object'||!Number.isInteger(s.lean.r)||s.lean.r<0||s.lean.r>4))s.lean=null;""")

css="""
/* 0.63: today's question and the written page */
.ask .feelq{font-weight:600}
.ask .chips{justify-content:center}
.askchip{min-height:44px}
.ask.done{text-align:left;width:100%}
.ask .entry{margin:4px 0 6px;font-size:16px;line-height:1.45}
"""
i=S.rindex("</style>",0,S.index("<body")); S=S[:i]+css+S[i:]

out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk63.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk63.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)

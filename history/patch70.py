# 0.70: closing the day, and personalities that grow from your answers (brainstorm plan, ideas 8 and 9).
#   Closing the day: in the evening (7 pm to 4 am), once today's card is done or it is a rest day, Today offers
#   "Close the day": today's page read back (its postcard, its words, your own words), your companion's goodnight,
#   and, where the device can speak, "Read it to me" in the app's language. "Goodnight" closes it for the day.
#   Personalities: each answer to the day's question is counted on the companion of the moment (c.lq, one per day;
#   changing the answer moves it). After five, the realm it leans toward most gives it a habit ("Lately, Pippa has
#   started napping in sunbeams. It picked that up from you."), in its story sheet and now and then by the fire.
import re,subprocess,os
S=open('base69.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.69.0'","const VERSION='prototype 0.70.0'")
rep("<title>Forgelings (prototype 0.69.0)</title>","<title>Forgelings (prototype 0.70.0)</title>")

# ---- personalities ----
rep("""  const c=companion()||mateNow();if(c){const L=c.dark?MOOD_LD:MOOD_L;hf.msg=L[r].replace(/\\{n\\}/g,c.nick||c.name);}""",
    """  const c=companion()||mateNow();if(c){const L=c.dark?MOOD_LD:MOOD_L;hf.msg=L[r].replace(/\\{n\\}/g,c.nick||c.name);
    state.cards.forEach(x=>{if(x.lqa&&x.lqa.d===k&&x.lq){x.lq[x.lqa.r]=Math.max(0,x.lq[x.lqa.r]-1);delete x.lqa;}});
    c.lq=c.lq||[0,0,0,0,0];c.lq[r]++;c.lqa={d:k,r};}""")
rep("    c.v=int(c.v,0,VECTORS.length-1,0);","    c.lq=Array.isArray(c.lq)&&c.lq.length===5&&c.lq.every(x=>Number.isInteger(x)&&x>=0)?c.lq:undefined;if(c.lq===undefined)delete c.lq;if(!(c.lqa&&typeof c.lqa.d==='string'&&Number.isInteger(c.lqa.r)&&c.lqa.r>=0&&c.lqa.r<=4))delete c.lqa;\n    c.v=int(c.v,0,VECTORS.length-1,0);")
rep("function taleSheetHTML(c){","""const QUIRK_C=['Lately, {n} has started saving a seat by the fire for whoever comes by.','Lately, {n} has started tinkering with little gadgets. Most of them almost work.','Lately, {n} has started napping in sunbeams, and recommends it.','Lately, {n} has started keeping a very tidy notebook of everything it sees.','Lately, {n} has started folding paper cranes and letting them fly away.'];
const QUIRK_D=['Lately, {n} has started walking the edge of camp at night, making sure everyone is in.','Lately, {n} has started forging small, sharp things in the embers.','Lately, {n} has started sleeping in, and is not sorry.','Lately, {n} has started staring into the dark until it makes sense.','Lately, {n} has started drawing maps of places that do not exist.'];
function quirkOf(c){const q=c&&c.lq;if(!q)return '';const t=q.reduce((a,b)=>a+b,0);if(t<5)return '';return (c.dark?QUIRK_D:QUIRK_C)[q.indexOf(Math.max(...q))].replace(/\\{n\\}/g,c.nick||c.name);}
function taleSheetHTML(c){""")
rep("""    `<div class="stack"><button class="primary" id="taleBack">Close</button></div>`;
}""","""    (quirkOf(c)?`<div class="tale new"><b>Lately</b><p>${esc(quirkOf(c))} It picked that up from you.</p></div>`:'')+
    `<div class="stack"><button class="primary" id="taleBack">Close</button></div>`;
}""")
rep("  if(tab==='hearth'&&!hf.msg){const sr=scribeRead();if(sr)hf.msg=sr;}","  if(tab==='hearth'&&!hf.msg){const sr=scribeRead();if(sr)hf.msg=sr;}\n  if(tab==='hearth'&&!hf.msg&&Math.random()<.25){const qc=slotCards().find(x=>quirkOf(x));if(qc)hf.msg=quirkOf(qc);}")

# ---- closing the day ----
rep("function todayTask(){","""/* ================= 0.70: closing the day ================= */
const GN_C=['{n} yawns, very wide. “Goodnight. Today counted.”','{n} curls up by the embers. “See you tomorrow. Same fire.”','{n} tucks its nose under its tail. “That was a good page.”','{n} blinks slowly at you. “Sleep well. I will keep watch.”','{n} pulls the blanket over both of you. “Night night.”'];
const GN_D=['{n} settles into the dark. “Rest. The night is mine to keep.”','{n} turns once and lies down. “Done. Sleep.”','{n} watches the embers. “Go on. I have the watch.”','{n} closes one eye. “Tomorrow, then.”','{n} lets out a long, low breath. “Good. Now rest.”'];
const eveningNow=()=>{const h=new Date().getHours();return h>=19||h<4;};
const MOON='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>';
function closeDayHTML(){
  const k=state.date,c=companion()||mateNow()||(state.todayCard!=null?cardById(state.todayCard):null),n=c?(c.nick||c.name):'';
  const w=state.status==='rest'?'A rest day. The fire kept itself, and so did you.':entryLine(k),j=state.journal[k]&&state.journal[k].text?state.journal[k].text:'';
  const gn=c?(c.dark?GN_D:GN_C)[dnum(k)%5].replace(/\\{n\\}/g,n):'Goodnight. Today counted.';
  ui.gnText=[w,j,gn].filter(Boolean).join(' ');
  return `<p class="muted center small">${esc(dateLabel(k))}</p><h2 class="center">Closing the day</h2>${(state.posts||{})[k]?`<div class="center">${pcFig(k,state.posts[k])}</div>`:''}${w?`<p class="world entry" style="margin:12px 0 6px">${esc(w)}</p>`:''}${j?`<p class="mine" style="margin:6px 0">\\u201C${esc(j)}\\u201D</p>`:''}<div class="gnrow">${c?`<img src="${spriteURL(c)}" alt="" width="56" height="56">`:''}<p>${esc(gn)}</p></div><div class="stack">${'speechSynthesis' in window?'<button class="outline" id="gnRead">Read it to me</button>':''}<button class="primary" id="gnGo">Goodnight</button></div>`;}
function gnRead(){try{const s=window.speechSynthesis;s.cancel();const u=new SpeechSynthesisUtterance(ui.gnText||'');u.lang=curLang()==='ja'?'ja-JP':'en-US';u.rate=.92;s.speak(u);}catch(e){}}
function todayTask(){""")
rep("  {const o=otdKey();if(o&&state.otd!==todayKey())","""  if((s==='done'||s==='rest')&&eveningNow()&&state.closed!==state.date){const gc=companion()||mateNow();rows.unshift(row('btnClose',MOON,'Close the day',gc?`${esc(gc.nick||gc.name)} is getting sleepy. Read today’s page together and say goodnight.`:'Read today’s page and say goodnight.','',true));}
  {const o=otdKey();if(o&&state.otd!==todayKey())""")
rep("  else if(b.id==='btnOtd'){","  else if(b.id==='btnClose'){openSheet(closeDayHTML());}\n  else if(b.id==='btnOtd'){")
rep("""  else if(b.dataset.chgo!==undefined)chooseCard(+b.dataset.chgo);""","""  else if(b.dataset.chgo!==undefined)chooseCard(+b.dataset.chgo);
  else if(b.id==='gnRead')gnRead();
  else if(b.id==='gnGo'){state.closed=state.date;const gc=companion()||mateNow();if(gc)hf.msg=`${gc.nick||gc.name} is asleep by the fire.`;save();closeModal();renderToday();renderHearth();toast('Goodnight. See you tomorrow.');}""")
rep("function closeModal(){","function closeModal(){try{if(window.speechSynthesis)speechSynthesis.cancel();}catch(e){}")
rep("  if(s.ask!==undefined){if(!s.ask","  s.closed=typeof s.closed==='string'&&/^\\d{4}-\\d{2}-\\d{2}$/.test(s.closed)?s.closed:'';\n  if(s.ask!==undefined){if(!s.ask")
css="""
/* 0.70: closing the day */
.gnrow{display:flex;align-items:center;gap:12px;margin:14px 0 6px;padding:10px 12px;border-radius:12px;background:rgba(36,24,63,.08)}
.gnrow img{width:56px;height:56px;image-rendering:pixelated;flex:none}.gnrow p{margin:0;font-style:italic}
"""
i=S.rindex("</style>",0,S.index("<body")); S=S[:i]+css+S[i:]

out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk70.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk70.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)

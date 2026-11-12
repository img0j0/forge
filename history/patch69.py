# 0.69: keep a card for later, and a gentler welcome back (brainstorm plan, ideas 6 and 7).
#   Pocket: when you turn today's three cards over, any one you do not choose can go in your pocket ("Keep it for
#   later"); there is one pocket, and a new card swaps the old one out. On a later day the pocketed card waits at the
#   top of the three, face up, and choosing it empties the pocket. No expiry, no reminder.
#   Welcome back: after the fire is relit (three or more days away), a short "While you were gone" page says what
#   the Forgelings got up to, one line each, and your companion leaves a drawn postcard on the wall, "kept for you".
#   Nothing about missed days. Save: state.pocket = {v, o, d}; pcGifts entries may carry t:2 (kept while away).
import re,subprocess,os
S=open('base68.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.68.0'","const VERSION='prototype 0.69.0'")
rep("<title>Forgelings (prototype 0.68.0)</title>","<title>Forgelings (prototype 0.69.0)</title>")

# 0.64's face-down cards: the spoken name now contains the visible words (axe label-content-name-mismatch)
rep('aria-label="Card ${i+1}, face down. Turn it over"','aria-label="Card ${i+1}, face down. Tap to turn it over"')
# ---- the pocket ----
rep("""<button class="primary chgo" data-chgo="${i}">Choose this card</button></div>`;}).join('');""",
    """<button class="primary chgo" data-chgo="${i}">Choose this card</button>${pocketBtn(c,i)}</div>`;}).join('');""")
rep("""  openSheet(`<h2>Choose today’s card</h2><p class="muted small">Turn them over, then choose the one you will do today. The other two go back in the deck.</p><div class="chlist">${cards}</div>""",
    """  const pk=pocketOK()&&state.pocket.d!==state.date?state.pocket:null;
  const pkc=pk?`<div class="dcard dface pocket" style="--cc:${pk.o!=null?'#FFD36B':VECTORS[pk.v].color}"><span class="chsig" aria-hidden="true">${sigilSVG(pk.o!=null?12:pk.v,pk.o!=null?'#FFD36B':VECTORS[pk.v].color)}</span><div><small class="muted">From your pocket</small><b>${esc(choiceBand(pk))}</b><p>${esc(choiceTask(pk))}</p></div><button class="primary chgo" data-chpk="1">Choose this card</button></div>`:'';
  openSheet(`<h2>Choose today’s card</h2><p class="muted small">Turn them over, then choose the one you will do today. The others go back in the deck, or keep one in your pocket for another day.</p><div class="chlist">${pkc}${cards}</div>""")
rep("function chooseCard(i){","""function pocketOK(){const p=state.pocket;return !!(p&&Number.isInteger(p.v)&&VECTORS[p.v]&&(p.o==null||(state.owns||[]).some(o=>o.id===p.o)));}
function pocketBtn(c,i){const p=state.pocket;if(p&&p.d===state.date&&p.v===c.v&&(p.o==null?c.o==null:p.o===c.o))return '<p class="muted small chpk" style="width:100%;text-align:center;margin:4px 0 0">In your pocket</p>';
  return `<button class="ghost chkeep" data-chkeep="${i}">${pocketOK()&&p.d!==state.date?'Swap it into your pocket':'Keep it for later'}</button>`;}
function chooseCard(i){""")
rep("  else if(b.dataset.chgo!==undefined)chooseCard(+b.dataset.chgo);","""  else if(b.dataset.chgo!==undefined)chooseCard(+b.dataset.chgo);
  else if(b.dataset.chkeep!==undefined){const c=state.choices&&state.choices.list[+b.dataset.chkeep];if(c){state.pocket={v:c.v,o:c.o==null?null:c.o,d:state.date};save();sfx('select');openChoose();const g=modal.querySelector(`[data-chgo="${b.dataset.chkeep}"]`);if(g)g.focus({preventScroll:true});toast('It is in your pocket. It will wait at the top of your cards.');}}
  else if(b.dataset.chpk!==undefined){if(pocketOK()&&state.choices){const p=state.pocket;state.choices.list.push({v:p.v,o:p.o==null?null:p.o});state.pocket=null;chooseCard(state.choices.list.length-1);}}""")
# choosing the pocketed card on the day it was pocketed empties the pocket too
rep("  state.todayV=c.v;state.todayOwn=c.o;state.choices.chosen=i;","  if(state.pocket&&state.pocket.d===state.date&&state.pocket.v===c.v&&(state.pocket.o==null?c.o==null:state.pocket.o===c.o))state.pocket=null;\n  state.todayV=c.v;state.todayOwn=c.o;state.choices.chosen=i;")
rep("ch.list.length>=1&&ch.list.length<=3&&","ch.list.length>=1&&ch.list.length<=4&&")
rep("  if(s.ask!==undefined){if(!s.ask","""  {const p=s.pocket,DK=/^\\d{4}-\\d{2}-\\d{2}$/;s.pocket=p&&typeof p==='object'&&Number.isInteger(p.v)&&p.v>=0&&p.v<VECTORS.length&&typeof p.d==='string'&&DK.test(p.d)?{v:p.v,o:Number.isFinite(p.o)?p.o:null,d:p.d}:null;}
  if(s.ask!==undefined){if(!s.ask""")
rep("g.t===1?{t:1,l:Number.isInteger(g.l)&&g.l>=0&&g.l<=4?g.l:-1}:{}","g.t===1?{t:1,l:Number.isInteger(g.l)&&g.l>=0&&g.l<=4?g.l:-1}:g.t===2?{t:2}:{}")

# ---- while you were gone ----
rep("function endWake(){","""const AWAY_C=['{n} tidied the curio shelf, then untidied it to make it look lived in.','{n} practised its game in secret and got a little better.','{n} kept a spot by the fire warm for you.','{n} learned a new song from the wind and hums it now.','{n} counted the stars twice to be sure.','{n} made a small pile of interesting stones.'];
const AWAY_D=['{n} kept watch at the gate. Nothing got past.','{n} sharpened its claws on the old log, quietly.','{n} sat with the embers so they would not feel alone.','{n} chased something out of the dark. It did not come back.','{n} guarded your book. No one read a page.','{n} slept with one eye open, for you.'];
function awayHTML(T){
  const cs=slotCards().filter(c=>!(wOut()&&state.wander.id===c.id)).slice(0,3),seed=Date.now()>>>8,ls=cs.map((c,i)=>{const L=c.dark?AWAY_D:AWAY_C;return L[(seed+i*2+(c.wi||0))%L.length].replace(/\\{n\\}/g,c.nick||c.name);});
  const m=companion()||mateNow()||cs[0];let fig='';
  if(m){const g={d:todayKey(),r:m.theme>=0&&m.theme<5?m.theme:0,s:(seed%2147483646)+1,c:m.id,t:2};state.pcGifts=(state.pcGifts||[]).concat([g]).slice(-200);save();fig=`<div class="center">${giftFig(g)}</div>`;}
  return `<h2>While you were gone</h2>${ls.map(l=>`<p>${esc(l)}</p>`).join('')}${fig}<p class="muted small">Nothing was lost while you were away. Everything is where you left it.</p><div class="stack"><button class="primary" data-close>Back to the fire</button></div>`;}
function endWake(){""")
rep("""  hf.msg='Everyone is awake. The fire is warm.';
  renderHearth();renderToday();""","""  hf.msg='Everyone is awake. The fire is warm.';
  renderHearth();renderToday();
  setTimeout(()=>{if(state.cards.length&&modal.hidden)openSheet(awayHTML());},500);""")
rep("""<figcaption>${g.t===1?""","""<figcaption>${g.t===2?`Kept for you while you were away \\u2014 ${esc(n)}`:g.t===1?""")
# a pocketed card keeps its words: the task line is the one for the day it was dealt
rep("return o?o.text:taskFor(c.v,state.date);};","return o?o.text:taskFor(c.v,c.d||state.date);};")
rep("function todayTask(){const o=todayOwnObj();return o?o.text:taskFor(state.todayV,state.date);}","function todayTask(){const o=todayOwnObj(),ch=state.choices,cd=ch&&ch.date===state.date&&ch.chosen!=null&&ch.list[ch.chosen]&&ch.list[ch.chosen].d;return o?o.text:taskFor(state.todayV,typeof cd==='string'?cd:state.date);}")
rep("state.choices.list.push({v:p.v,o:p.o==null?null:p.o});","state.choices.list.push({v:p.v,o:p.o==null?null:p.o,d:p.d});")
css="""
/* 0.69: the pocket */
.chkeep{width:100%;min-height:44px;margin-top:4px}
.dcard.pocket{box-shadow:inset 0 0 0 2px var(--cc),0 0 0 3px rgba(255,211,107,.45)}
.dcard.pocket small{display:block;font-size:12px}
"""
i=S.rindex("</style>",0,S.index("<body")); S=S[:i]+css+S[i:]

out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk69.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk69.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)

# 0.64: choose your card (the design doc's Part 1; Hunter, November 12: "Execute the plan").
#   Each new day deals three cards instead of one: Today's "Turn over" opens them face down; tap each to turn it over,
#   then choose the one you will do today. The other two go back in the deck. The three are dealt the way one card was
#   (what you want more of, and your own small things, can be any of them; never the same calling twice in a day).
#   The first day of a new player keeps its single card. Going all in, rest days and everything after stay as they were.
import re,subprocess,os
S=open('base63.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.63.0'","const VERSION='prototype 0.64.0'")
rep("<title>Forgelings (prototype 0.63.0)</title>","<title>Forgelings (prototype 0.64.0)</title>")

rep("function todayTask(){","""/* 0.64: three cards a day. state.choices = {date, list:[{v, o}], chosen}; the first is today's until one is chosen. */
function newChoices(avoid){
  const out=[],usedV=avoid.slice();
  for(let i=0;i<3;i++){let v,o,t=0;do{v=pickToday(usedV);o=state.todayOwn;t++;}while(t<8&&out.some(x=>(o!=null&&x.o===o)||(o==null&&x.o==null&&x.v===v)));
    out.push({v,o:o==null?null:o});usedV.push(v);}
  state.choices={date:state.date,list:out,chosen:null};state.todayV=out[0].v;state.todayOwn=out[0].o;return out[0].v;}
const chooseOpen=()=>!!(state.onboarded&&state.status==='fresh'&&state.choices&&state.choices.date===state.date&&state.choices.chosen==null&&state.choices.list.length>1);
const choiceTask=c=>{const o=c.o!=null?(state.owns||[]).find(x=>x.id===c.o):null;return o?o.text:taskFor(c.v,state.date);};
const choiceBand=c=>{const o=c.o!=null?(state.owns||[]).find(x=>x.id===c.o):null;return o?(o.k>=0?'Yours · '+WANTS[o.k].n:'Yours'):VECTORS[c.v].name;};
function openChoose(){
  const L=state.choices.list,up=ui.chUp||(ui.chUp={});
  const cards=L.map((c,i)=>{const V=VECTORS[c.v],own=c.o!=null,col=own?'#FFD36B':V.color;
    if(!up[state.date+':'+i])return `<button class="dcard dback" data-chup="${i}" aria-label="Card ${i+1}, face down. Turn it over"><span class="chseal" aria-hidden="true"><svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#F4ECD8" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7 6-7 12L5 9z"/><path d="M5 9h14M9 9l3 12M15 9l-3 12"/></svg></span><span>Tap to turn it over</span></button>`;
    return `<div class="dcard dface" style="--cc:${col}"><span class="chsig" aria-hidden="true">${sigilSVG(own?12:c.v,col)}</span><div><b>${esc(choiceBand(c))}</b><p>${esc(choiceTask(c))}</p></div><button class="primary chgo" data-chgo="${i}">Choose this card</button></div>`;}).join('');
  openSheet(`<h2>Choose today’s card</h2><p class="muted small">Turn them over, then choose the one you will do today. The other two go back in the deck.</p><div class="chlist">${cards}</div><div class="row" style="justify-content:center"><button class="ghost" data-close>Not now</button></div>`);}
function chooseCard(i){
  const c=state.choices&&state.choices.list[i];if(!c)return;
  state.todayV=c.v;state.todayOwn=c.o;state.choices.chosen=i;state.status='revealed';save();sfx('select');
  closeModal();renderToday();openVector();}
function todayTask(){""")
rep("state.todayV=pickToday(state.history.slice(-4).map(h=>h.v).filter(v=>v!=null).concat([state.todayV]));","newChoices(state.history.slice(-4).map(h=>h.v).filter(v=>v!=null).concat([state.todayV]));")
rep("function wantSaved(){state.wantAsked=true;if(state.status==='fresh')state.todayV=pickToday([]);","function wantSaved(){state.wantAsked=true;if(state.status==='fresh')newChoices([]);")
m=S.count("state.todayV=pickToday([]);");assert m==1,m
S=S.replace("state.todayV=pickToday([]);","newChoices([]);")
# Today's turn-over opens the three while they wait
rep("""function openVector(){
  const L=todayLook()""","""function openVector(){
  if(chooseOpen()){openChoose();return;}
  const L=todayLook()""")
rep("""  if(b.hasAttribute('data-close')||b.id==='ovClose')closeModal();""","""  if(b.hasAttribute('data-close')||b.id==='ovClose')closeModal();
  else if(b.dataset.chup!==undefined){const i=+b.dataset.chup;(ui.chUp=ui.chUp||{})[state.date+':'+i]=1;sfx('select');openChoose();const g=modal.querySelector(`[data-chgo="${i}"]`);if(g)g.focus({preventScroll:true});}
  else if(b.dataset.chgo!==undefined)chooseCard(+b.dataset.chgo);""")
# the save
rep("""  if(s.ask!==undefined){""","""  if(s.choices!==undefined&&s.choices!==null){const ch=s.choices,owns=Array.isArray(s.owns)?s.owns:[];
    const ok=ch&&typeof ch==='object'&&typeof ch.date==='string'&&Array.isArray(ch.list)&&ch.list.length>=1&&ch.list.length<=3&&ch.list.every(x=>x&&Number.isInteger(x.v)&&x.v>=0&&x.v<VECTORS.length&&(x.o===null||x.o===undefined||owns.some(o=>o&&o.id===x.o)));
    if(!ok)s.choices=null;else{ch.list.forEach(x=>{if(x.o===undefined)x.o=null;});if(!(ch.chosen===null||(Number.isInteger(ch.chosen)&&ch.chosen>=0&&ch.chosen<ch.list.length)))ch.chosen=null;}}
  if(s.ask!==undefined){""")
css="""
/* 0.64: choose your card */
.chlist{display:flex;flex-direction:column;gap:10px;margin:10px 0}
.dcard{display:flex;align-items:center;gap:12px;padding:12px;border-radius:12px;min-height:72px;text-align:left}
.dcard.dback{border:0;background:linear-gradient(135deg,#5A2C2A,#3A1C22);color:#F4ECD8;font:600 15px var(--body);cursor:pointer;box-shadow:inset 0 0 0 2px #C9A15A}
.dcard.dback:focus-visible{outline:3px solid #FFD36B;outline-offset:2px}
.chseal svg,.chsig svg{width:40px;height:40px;display:block}
.dcard.dface{flex-wrap:wrap;background:var(--card,rgba(255,255,255,.6));box-shadow:inset 0 0 0 2px var(--cc)}
.dcard.dface>div{flex:1;min-width:0}.dcard.dface b{color:inherit;font-size:16px}.dcard.dface p{margin:2px 0 0;font-size:14px;line-height:1.4}
.chgo{width:100%}
html.reduce .dcard{transition:none}
"""
i=S.rindex("</style>",0,S.index("<body")); S=S[:i]+css+S[i:]

out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk64.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk64.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)

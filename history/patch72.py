# 0.72: animations and richer card backs (Hunter, November 12: "animations such as when you open packs or your daily
#   card, also maybe enhancing the art on the back side of the cards").
#   Card backs: art/cardback72.py, still the Leather journal he picked, with tooled leather, a bevelled gold frame,
#   corner flourishes, shaded ribbons and a shadow under the seal; a slow gold glint sweeps across every face-down card.
#   Today's card: the three cards are now real cards in a row. They are dealt in, each turns over in 3D with a little
#   spark, the one you tap lifts and shows its task below, and choosing it sends the others back while the chosen
#   card turns over into today's card. No sheet re-opening between taps.
#   Revealing a Forgeling (daily and packs): a true 3D turn instead of a squash. Rare and better cards build up first:
#   the card trembles and glows in its rarity's colour with light rays behind it (longer for Holo and Legend, which
#   end in a flash). Pack cards are dealt up from the pack one at a time and slide away to the pile; the summary fans in.
#   Reduced motion turns all of it off (cards simply appear turned over).
import re,subprocess,os,sys
sys.path.insert(0,'art');import cardback72
S=open('base71.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.71.0'","const VERSION='prototype 0.72.0'")
rep("<title>Forgelings (prototype 0.71.0)</title>","<title>Forgelings (prototype 0.72.0)</title>")

# ---- the new backs ----
for k in 'TP':
    m=re.search(r'--cb'+k+r':url\("data:image/svg\+xml,(.*?)"\)',S);assert m
    S=S[:m.start(1)]+cardback72.packed(cardback72.BACKS[k])+S[m.end(1):]

# ---- choosing today's card ----
m=re.search(r"function openChoose\(\)\{[\s\S]*?\n(?=function pocketOK\(\))",S);assert m
S=S[:m.start()]+"""function openChoose(){
  const L=state.choices.list,pk=pocketOK()&&state.pocket.d!==state.date?state.pocket:null;ui.chSel=null;
  const pkc=pk?`<div class="dcard dface pocket" style="--cc:${pk.o!=null?'#FFD36B':VECTORS[pk.v].color}"><span class="chsig" aria-hidden="true">${sigilSVG(pk.o!=null?12:pk.v,pk.o!=null?'#FFD36B':VECTORS[pk.v].color)}</span><div><small class="muted">From your pocket</small><b>${esc(choiceBand(pk))}</b><p>${esc(choiceTask(pk))}</p></div><button class="primary chgo" data-chpk="1">Choose this card</button></div>`:'';
  openSheet(`<h2>Choose today’s card</h2><p class="muted small">Turn them over, then choose the one you will do today. The others go back in the deck, or keep one in your pocket for another day.</p>${pkc}<div class="chrow">${L.map((c,i)=>dcHTML(c,i)).join('')}</div><div class="chdet" id="chDet" aria-live="polite"></div><div class="row" style="justify-content:center"><button class="ghost" data-close>Not now</button></div>`);
  const up=Object.keys(ui.chUp||{}).filter(k=>k.startsWith(state.date+':')).map(k=>+k.split(':')[1]);if(up.length)ui.chSel=up[up.length-1];chooseSync();}
function dcHTML(c,i){const V=VECTORS[c.v],own=c.o!=null,col=own?'#FFD36B':V.color;
  return `<button class="dc" data-chup="${i}" style="--cc:${col};--i:${i}"><span class="dci"><span class="dcb" aria-hidden="true"></span><span class="dcf" aria-hidden="true"></span></span></button>`;}
const dcFace=c=>{const own=c.o!=null,col=own?'#FFD36B':VECTORS[c.v].color;return `<span class="dcs">${sigilSVG(own?12:c.v,col)}</span><b>${esc(choiceBand(c))}</b>`;};
function chooseSync(){
  const L=state.choices.list,up=ui.chUp||{},s=ui.chSel;
  modal.querySelectorAll('.dc').forEach(b=>{const i=+b.dataset.chup,c=L[i],u=!!up[state.date+':'+i];b.classList.toggle('up',u);{const f=b.querySelector('.dcf');if(u&&f&&!f.firstChild)f.innerHTML=dcFace(c);}b.classList.toggle('sel',u&&s===i);
    b.setAttribute('aria-label',u?`${choiceBand(c)}. ${choiceTask(c)}`:`Card ${i+1}, face down. Tap to turn it over`);if(u)b.setAttribute('aria-pressed',String(s===i));else b.removeAttribute('aria-pressed');});
  const d=$('#chDet');if(!d)return;const c=s!=null?L[s]:null;
  d.innerHTML=c?`<div class="dcard dface" style="--cc:${c.o!=null?'#FFD36B':VECTORS[c.v].color}"><div><b>${esc(choiceBand(c))}</b><p>${esc(choiceTask(c))}</p></div><button class="primary chgo" data-chgo="${s}">Choose this card</button>${pocketBtn(c,s)}</div>`:'<p class="muted small center" style="margin:10px 0">Tap a card to turn it over.</p>';}
function chSpark(b){if(REDUCE||!b)return;for(let k=0;k<7;k++){const sp=document.createElement('i');sp.className='dcsp';const a=Math.PI*2*k/7+Math.random()*.5,d=38+Math.random()*30;sp.style.setProperty('--dx',(Math.cos(a)*d).toFixed(0)+'px');sp.style.setProperty('--dy',(Math.sin(a)*d).toFixed(0)+'px');b.appendChild(sp);setTimeout(()=>sp.remove(),700);}}
function chooseGo(i){
  const row=modal.querySelector('.chrow');if(REDUCE||!row){chooseCard(i);return;}
  row.classList.add('going');row.querySelectorAll('.dc').forEach(b=>b.classList.add(+b.dataset.chup===i?'picked':'away'));sfx('select');
  const d=$('#chDet');if(d)d.classList.add('going');setTimeout(()=>{ui.vecIn=true;chooseCard(i);},520);}
"""+S[m.end():]
rep("""  else if(b.dataset.chup!==undefined){const i=+b.dataset.chup;(ui.chUp=ui.chUp||{})[state.date+':'+i]=1;sfx('select');openChoose();const g=modal.querySelector(`[data-chgo="${i}"]`);if(g)g.focus({preventScroll:true});}""",
    """  else if(b.dataset.chup!==undefined){const i=+b.dataset.chup,k=state.date+':'+i,was=!!(ui.chUp&&ui.chUp[k]);(ui.chUp=ui.chUp||{})[k]=1;ui.chSel=i;chooseSync();if(!was){chime(0);setTimeout(()=>chSpark(b),260);}else sfx('select');}""")
rep("  else if(b.dataset.chgo!==undefined)chooseCard(+b.dataset.chgo);","  else if(b.dataset.chgo!==undefined)chooseGo(+b.dataset.chgo);")
rep("""save();sfx('select');openChoose();const g=modal.querySelector(`[data-chgo="${b.dataset.chkeep}"]`);if(g)g.focus({preventScroll:true});toast(""","""save();sfx('select');chooseSync();const g=modal.querySelector(`[data-chgo="${b.dataset.chkeep}"]`);if(g)g.focus({preventScroll:true});toast(""")
# today's card turns over into place after choosing
rep("""function flipVector(){""","""function vecInPlay(){if(!ui.vecIn)return;ui.vecIn=false;if(REDUCE)return;const f=$('#vflip');if(f){f.classList.add('vin');setTimeout(()=>f.classList.remove('vin'),900);}}
function flipVector(){""")
rep("  closeModal();renderToday();openVector();}","  closeModal();renderToday();openVector();vecInPlay();}")

# ---- revealing a Forgeling: build-up, then a 3D turn ----
rep("""function revealFlip(){""","""/* rare and better cards build up first: tremble, glow, rays; Holo and Legend end in a flash */
function chargeThen(st,c,go){
  if(REDUCE||!st||!c||c.rarity<2){go();return;}
  const R=RAR[c.rarity],ms=[0,0,450,750,1050][c.rarity];st.style.setProperty('--rc',R.glow);
  if(!st.querySelector('.rays'))st.insertAdjacentHTML('afterbegin','<i class="rays" aria-hidden="true"></i>');
  st.classList.add('charge','ch'+c.rarity);chime(0);
  setTimeout(()=>{if(!st.isConnected)return;st.classList.remove('charge');go();
    if(c.rarity>=3){st.insertAdjacentHTML('beforeend','<i class="flash" aria-hidden="true"></i>');setTimeout(()=>{const f=st.querySelector('.flash');if(f)f.remove();},800);}},ms);}
function dealIn(){if(REDUCE)return;const s=$('#stage');if(s){s.classList.add('dealin');setTimeout(()=>s.classList.remove('dealin'),700);}}
function revealFlip(){""")
for who in ("cardById(rv.id)","pk.cards[pk.i]"):
    old=f"  const c={who},st=$('#stage'),cv=$('#cover');inkStart(st,c);cv.classList.add('open');$('.card',st).classList.add('unveil');"
    rep(old,f"  const c={who},st=$('#stage');chargeThen(st,c,()=>{{const cv=$('#cover');if(!cv||!st.isConnected)return;inkStart(st,c);cv.classList.add('open');$('.card',st).classList.add('unveil');")
m=re.search(r"(function revealFlip\(\)\{[\s\S]*?)\},430\);\n\}",S);assert m;S=S[:m.start()]+m.group(1)+"},560);});\n}"+S[m.end():]
m=re.search(r"(function packFlip\(\)\{[\s\S]*?)\},430\);\n\}",S);assert m;S=S[:m.start()]+m.group(1)+"},560);});\n}"+S[m.end():]
rep("""      <button class="ghost" id="rvSkip">Skip for now</button></div>`,false);
  attachTilt($('#stage'));hydrate(modal);""","""      <button class="ghost" id="rvSkip">Skip for now</button></div>`,false);
  attachTilt($('#stage'));hydrate(modal);dealIn();""")
# packs: each card dealt up from the pack, slides to the pile; the summary fans in
rep("""  openOverlay(body,false);
  const st=$('#stage');if(st)attachTilt(st);hydrate(modal);""","""  openOverlay(body,false);
  const st=$('#stage');if(st)attachTilt(st);hydrate(modal);if(pk.step==='card')dealIn();""")
rep("  else if(b.id==='packNext'){if(pk.i<4){pk.i++;pk.flipped=false;drawPack();}else{pk.step='sum';drawPack();}}",
    "  else if(b.id==='packNext'){const nx=()=>{if(pk.i<4){pk.i++;pk.flipped=false;drawPack();}else{pk.step='sum';drawPack();}};const t=$('#stage .tilt');if(REDUCE||!t){nx();}else{b.disabled=true;t.classList.add('toPile');setTimeout(nx,300);}}")

css="""
/* ================= 0.72: animations and card backs ================= */
/* a slow gold glint across face-down cards */
.heroback{position:relative;overflow:hidden}
.cover::after,.vface.vback::after,.heroback::after,.dcb::after{content:"";position:absolute;inset:-30% -60%;pointer-events:none;background:linear-gradient(110deg,transparent 42%,rgba(255,230,160,.0) 45%,rgba(255,230,160,.34) 50%,rgba(255,230,160,0) 55%,transparent 58%);transform:translateX(-60%);animation:cbSheen 5.5s ease-in-out infinite}
.dcb::after{animation-delay:calc(var(--i,0)*.35s + 1s)}
@keyframes cbSheen{0%,58%{transform:translateX(-60%)}88%,100%{transform:translateX(60%)}}
.cover:active{filter:brightness(1.08)}
/* choosing today's card */
.chrow{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:14px 2px 6px;perspective:900px}
.dc{position:relative;border:0;padding:0;background:none;aspect-ratio:5/7;width:100%;cursor:pointer;animation:dcDeal .55s cubic-bezier(.2,.9,.3,1.18) backwards;animation-delay:calc(var(--i)*.09s + .12s);transition:transform .3s cubic-bezier(.3,1.4,.5,1),filter .3s}
.dc:focus-visible{outline:3px solid #FFD36B;outline-offset:4px;border-radius:6px}
.dci{position:absolute;inset:0;transform-style:preserve-3d;transition:transform .62s cubic-bezier(.3,1.3,.45,1)}
.dc.up .dci{transform:rotateY(180deg)}
.dcb,.dcf{position:absolute;inset:0;backface-visibility:hidden;-webkit-backface-visibility:hidden;border-radius:5px;overflow:hidden;box-shadow:0 6px 0 rgba(30,20,20,.25)}
.dcb{background:var(--cbP) 0 0/100% 100% no-repeat}
.dcf{transform:rotateY(180deg);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;padding:8px 6px;background:radial-gradient(circle at 50% 38%,color-mix(in srgb,var(--cc) 30%,transparent),transparent 62%),linear-gradient(#3A2F6A,#241D45);box-shadow:inset 0 0 0 3px var(--cc),0 6px 0 rgba(30,20,20,.25);color:#FFF7EC}
.dcf .dcs svg{width:46px;height:46px;display:block;filter:drop-shadow(0 2px 0 rgba(0,0,0,.35))}
.dcf b{font-size:13px;line-height:1.2;text-align:center}
.dc.sel{transform:translateY(-10px)}
.dc.sel .dcf{box-shadow:inset 0 0 0 3px var(--cc),0 0 18px color-mix(in srgb,var(--cc) 70%,transparent),0 12px 0 rgba(30,20,20,.2)}
.dcsp{position:absolute;left:50%;top:45%;width:6px;height:6px;margin:-3px;background:var(--cc);pointer-events:none;z-index:3;animation:burst .65s steps(7,end) forwards}
@keyframes dcDeal{from{opacity:0;transform:translateY(90px) rotate(calc((var(--i) - 1)*-14deg)) scale(.7)}to{opacity:1;transform:none}}
.chrow.going .dc{animation:none}
.dc.away{transition:transform .42s ease-in,opacity .42s ease-in;transform:translateY(120px) rotate(calc((var(--i) - 1)*12deg)) scale(.85);opacity:0}
.dc.picked{transition:transform .5s cubic-bezier(.3,1.3,.5,1);transform:translateY(-24px) scale(1.12);z-index:2}
.chdet{min-height:150px}.chdet.going{transition:opacity .25s;opacity:0}
.chdet .dcard{animation:fade .3s ease-out}
html[data-theme="dark"] :is(.chdet .dcard,.dcard.pocket){background:rgba(255,255,255,.07);color:var(--ink,#F4ECD8)}
.flip.vin .flip-in{animation:vecIn .85s cubic-bezier(.3,1.2,.45,1) both}
@keyframes vecIn{from{transform:rotateY(0) scale(.6) translateY(40px)}55%{transform:rotateY(195deg) scale(1.04)}to{transform:rotateY(180deg) scale(1)}}
/* revealing a Forgeling: a real turn, with a build-up for the rare ones */
.cover.open{transform:none !important;animation:covOut .56s linear forwards}
@keyframes covOut{0%,49%{opacity:1}50%,100%{opacity:0}}
.card.unveil{animation:flip3d .56s cubic-bezier(.45,.05,.3,1) both}
@keyframes flip3d{0%{transform:rotateY(0)}50%{transform:rotateY(90deg) scale(1.08)}50.01%{transform:rotateY(-90deg) scale(1.08)}100%{transform:rotateY(0) scale(1)}}
.stage>.tilt{z-index:1}
.stage .rays{position:absolute;left:50%;top:50%;width:175%;aspect-ratio:1;border-radius:50%;pointer-events:none;z-index:0;opacity:0;
  background:repeating-conic-gradient(from 0deg,var(--rc) 0 9deg,color-mix(in srgb,var(--rc) 35%,transparent) 9deg 12deg,transparent 12deg 22deg);filter:saturate(1.4);-webkit-mask:radial-gradient(circle,#000 0 22%,transparent 66%);mask:radial-gradient(circle,#000 0 22%,transparent 66%);
  transform:translate(-50%,-50%);animation:rays 9s linear infinite;transition:opacity .5s}
.stage.charge .rays{opacity:1}.stage.lit .rays{opacity:.6}
.stage.charge::after{content:"";position:absolute;inset:-14%;border-radius:50%;background:radial-gradient(circle,color-mix(in srgb,var(--rc) 55%,transparent),transparent 65%);z-index:0;pointer-events:none;animation:chGlow .5s ease-in-out infinite alternate}
@keyframes chGlow{from{opacity:.5;transform:scale(.92)}to{opacity:1;transform:scale(1.05)}}
html.reduce .stage.charge::after{display:none}
@keyframes rays{to{transform:translate(-50%,-50%) rotate(360deg)}}
.stage.charge .tilt{animation:tremble .1s linear infinite}
.stage.ch3 .tilt{animation-duration:.08s}.stage.ch4 .tilt{animation-duration:.06s}
.stage.charge .card{filter:drop-shadow(0 0 16px var(--rc)) drop-shadow(0 .45em .55em rgba(0,0,0,.4))}
@keyframes tremble{0%{translate:0 0}25%{translate:-2px 1px}50%{translate:2px -1px}75%{translate:-1px -1px}100%{translate:1px 1px}}
.stage .flash{position:fixed;inset:0;pointer-events:none;z-index:9;background:radial-gradient(circle,#fff 0,var(--rc) 35%,transparent 72%);opacity:0;animation:flash .8s ease-out}
@keyframes flash{0%{opacity:0}12%{opacity:.9}100%{opacity:0}}
/* dealt in, and off to the pile */
.stage.dealin .tilt{animation:dealIn .6s cubic-bezier(.2,.9,.3,1.12) both}
@keyframes dealIn{from{transform:translateY(60vh) rotate(10deg) scale(.75);opacity:0}60%{opacity:1}to{transform:none;opacity:1}}
.tilt.toPile{transition:transform .3s ease-in,opacity .3s ease-in !important;transform:translate(-130%,30px) rotate(-16deg) scale(.8) !important;opacity:0}
.sumgrid>*{animation:sumIn .5s cubic-bezier(.2,.9,.3,1.25) both}
.sumgrid>:nth-child(2){animation-delay:.08s}.sumgrid>:nth-child(3){animation-delay:.16s}.sumgrid>:nth-child(4){animation-delay:.24s}.sumgrid>:nth-child(5){animation-delay:.32s}
@keyframes sumIn{from{opacity:0;transform:translateY(40px) scale(.6) rotate(-8deg)}to{opacity:1;transform:none}}
/* reduced motion: everything simply appears */
html.reduce :is(.cover,.vface.vback,.heroback,.dcb)::after{animation:none;opacity:0}
html.reduce :is(.dc,.dci,.sumgrid>*,.stage.dealin .tilt,.flip.vin .flip-in,.tilt.toPile){animation:none !important;transition:none !important}
html.reduce .stage .rays,html.reduce .stage .flash{display:none}
html.reduce .stage.charge .tilt{animation:none}
@media (prefers-reduced-motion:reduce){:is(.cover,.vface.vback,.heroback,.dcb)::after{animation:none;opacity:0}.dc,.dci,.sumgrid>*{animation:none !important;transition:none !important}}
"""
i=S.rindex("</style>",0,S.index("<body")); S=S[:i]+css+S[i:]

out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk72.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk72.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)

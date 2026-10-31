# 0.48: ink and paper, moving (Hunter picked the four motion boards on the canvas, October 31).
# The pack is a sealed envelope: press the seal, the flap lifts, five cards fan out. A new Forgeling is pencilled,
# inked and coloured from the top down, then its rarity is stamped beside it, the same way for every card. Kept cards
# drift into the Binder ribbon, which dips with a +1 (+5 for a pack). Embers roll up on the Hearth. The Forge stamps
# MADE, signed. A newly found place pops onto the map inside an ink ring. Journal only; a tap skips; .reduce stops all.
import re,subprocess
S=open('base471.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)

rep("const VERSION='prototype 0.47.1'","const VERSION='prototype 0.48.0'")
rep("<title>Forgelings (prototype 0.47.1)</title>","<title>Forgelings (prototype 0.48.0)</title>")
rep("const SEEN_V=52;","const SEEN_V=53;")

# ---------- helpers: what the player has already seen move (kept beside the save, never in it) ----------
rep("function lsOn(){return !!(state&&state.settings&&state.settings.sky!=='plain');}",
"""function lsOn(){return !!(state&&state.settings&&state.settings.sky!=='plain');}
/* 0.48: motion. What has already been seen to move is kept beside the save, so a reload never replays it. */
let mSeenC=null,mSeenT=null;const mSeenP={};
function mSeen(){if(!mSeenC){try{mSeenC=JSON.parse(localStorage.getItem('forge-motion-v1')||'{}')||{};}catch(e){mSeenC={};}if(!mSeenC.pl)mSeenC.pl={};}return mSeenC;}
function mSeenLater(k,v){mSeenP[k]=v;if(mSeenT)return;mSeenT=setTimeout(()=>{mSeenT=null;const m=mSeen();Object.keys(mSeenP).forEach(k=>{if(k==='emb')m.emb=mSeenP[k];else m.pl[k]=mSeenP[k];delete mSeenP[k];});try{localStorage.setItem('forge-motion-v1',JSON.stringify(m));}catch(e){}},1200);}
function mOn(){return lsOn()&&!REDUCE;}
function embRoll(e,w){
  if(tab!=='hearth')return e+' '+w;
  const from=mSeen().emb;mSeenLater('emb',e);
  return typeof from==='number'&&e>from&&mOn()?`<span class="jroll" data-add="+${e-from}"><span><i data-from="${from}">${e}</i></span> ${w}</span>`:e+' '+w;
}
function snapCanvases(a,b){const x=a.querySelectorAll('canvas'),y=b.querySelectorAll('canvas');x.forEach((cv,i)=>{try{if(y[i])y[i].getContext('2d').drawImage(cv,0,0);}catch(e){}});}
function snapFly(el){
  if(!el||!mOn())return null;const r=el.getBoundingClientRect();if(!r.width)return null;
  const g=el.cloneNode(true);snapCanvases(el,g);g.querySelectorAll('[id]').forEach(x=>x.removeAttribute('id'));g.querySelectorAll('.jghost').forEach(x=>x.remove());
  const w=document.createElement('div');w.className='jfly';w.setAttribute('aria-hidden','true');w.style.cssText=`left:${r.left}px;top:${r.top}px;width:${r.width}px;height:${r.height}px`;w.appendChild(g);w._r=r;return w;
}
function flyToBinder(w,label){
  if(!w)return;const t=document.querySelector('.tab[data-tab="binder"]');if(!t||!w.animate)return;
  document.body.appendChild(w);const r=w._r,tr=t.getBoundingClientRect(),dx=tr.left+tr.width/2-(r.left+r.width/2),dy=tr.top+12-(r.top+r.height/2);
  const a=w.animate([{transform:'none',opacity:1},{transform:`translate(${dx.toFixed(0)}px,${dy.toFixed(0)}px) scale(.1) rotate(10deg)`,opacity:.7}],{duration:540,easing:'cubic-bezier(.55,0,.75,.95)'});
  const end=()=>{w.remove();t.classList.remove('jdip');void t.offsetWidth;t.classList.add('jdip');
    const p=document.createElement('span');p.className='jplus';p.setAttribute('aria-hidden','true');p.textContent=label;p.style.left=(tr.left+tr.width/2-12).toFixed(0)+'px';p.style.top=(tr.top-30).toFixed(0)+'px';document.body.appendChild(p);
    setTimeout(()=>{t.classList.remove('jdip');p.remove();},1600);};
  a.onfinish=end;a.oncancel=()=>w.remove();
}
/* a new Forgeling is pencilled, inked and coloured in; then its rarity is stamped beside it */
let inkT=null;
function stampHTML(c){const T=THEMES[c.theme];return `<div class="jrstamp" aria-hidden="true"><b>${RAR[c.rarity].name.toUpperCase()}</b><span>${esc((c.dark?T.dark.name:T.name).toUpperCase())} · ${c.dayN}</span></div>`;}
function inkStart(st,c){
  if(!st||!lsOn())return;clearTimeout(inkT);inkT=null;
  st.insertAdjacentHTML('beforeend',stampHTML(c));
  if(REDUCE){const s=$('.jrstamp',st);if(s)s.classList.add('jnow');return;}
  const fr=$('.card .face.front',st);if(!fr)return;
  const g=fr.cloneNode(true);snapCanvases(fr,g);g.classList.add('jghost');g.setAttribute('aria-hidden','true');
  g.querySelectorAll('[id]').forEach(x=>x.removeAttribute('id'));g.querySelectorAll('[aria-label],[role],[title]').forEach(x=>{x.removeAttribute('aria-label');x.removeAttribute('role');x.removeAttribute('title');});
  g.insertAdjacentHTML('beforeend','<i class="jwet"></i>');fr.after(g);st.classList.add('jinking');
  inkT=setTimeout(()=>inkDone(false),1500);
}
function inkDone(now){clearTimeout(inkT);inkT=null;const st=$('#stage');if(!st)return;st.querySelectorAll('.jghost').forEach(x=>x.remove());st.classList.remove('jinking');if(now){const s=$('.jrstamp',st);if(s)s.classList.add('jnow');}}""")

# ---------- the pack is a sealed envelope ----------
rep("function packSVG(){","""function envSVG(){
  const cb=(x,y,r)=>`<g transform="translate(${x} ${y}) rotate(${r})"><rect width="44" height="62" fill="#5B4A9E" stroke="#FFFFFF" stroke-width="3"/><rect x="6" y="6" width="32" height="50" fill="none" stroke="#FFD36B" stroke-width="1.2" stroke-dasharray="3 2.5"/><path d="M22 22l7 9-7 9-7-9z" fill="#FFD36B"/></g>`;
  return `<svg class="jenv" viewBox="0 -90 220 250" aria-hidden="true">
    <rect x="7" y="7" width="210" height="140" fill="rgba(40,28,20,.2)"/>
    <path class="e-flo" d="M0 0 L110 -70 L220 0 Z" fill="#E3D3AE" stroke="#CDB98E" stroke-width="2"/>
    <g class="e-peek">${cb(58,-34,-4)}${cb(118,-30,5)}</g>
    <rect width="220" height="140" fill="#EFE2C4"/><path d="M0 140 L110 74 L220 140" fill="none" stroke="#D9C69C" stroke-width="2"/>
    <path class="e-flc" d="M0 0 L110 82 L220 0 Z" fill="#E3D3AE" stroke="#CDB98E" stroke-width="2"/>
    <g class="e-seal"><circle cx="110" cy="80" r="21" fill="#A8323F"/><circle cx="110" cy="80" r="15" fill="none" stroke="#8A2230" stroke-width="2.5"/><path d="M110 69c4 5 8 8 8 13a8 8 0 0 1-16 0c0-4 3-6 4-9 1 3 2 4 4 4 0-3-1-5 0-8z" fill="#F3E8CC"/></g>
    <g class="e-bits" fill="#A8323F"><path d="M92 88l9-4 3 8-9 4z"/><path d="M118 92l8 2-2 8-8-2z"/><path d="M104 100h6v6h-6z"/></g>
    <g class="e-fan">${cb(22,-70,-16)}${cb(56,-82,-8)}${cb(88,-88,0)}${cb(120,-84,8)}${cb(152,-74,16)}</g></svg>`;
}
function packSVG(){""")
rep("""  if(pk.step==='sealed')body=`<p class="rv-title">Your pack is ready</p><button class="packbtn" id="packTear" aria-label="FORGELINGS 5 pixel Forgelings. Tear open the pack">${packSVG()}</button><p class="rv-hint">Tap the pack to tear it open</p>`;""",
"""  if(pk.step==='sealed')body=lsOn()?`<p class="rv-title">Your pack is ready</p><button class="packbtn" id="packTear" aria-label="An envelope holding 5 pixel Forgelings. Break the seal to open it">${envSVG()}</button><p class="rv-hint">Press the seal to open it</p>`:`<p class="rv-title">Your pack is ready</p><button class="packbtn" id="packTear" aria-label="FORGELINGS 5 pixel Forgelings. Tear open the pack">${packSVG()}</button><p class="rv-hint">Tap the pack to tear it open</p>`;""")
rep("""  else if(b.id==='packTear'){b.classList.add('opening');chime(1);setTimeout(()=>{if(!pk)return;pk.step='card';pk.i=0;pk.flipped=false;drawPack();},650);}""",
"""  else if(b.id==='packTear'){if(pkT){pkGo();return;}b.classList.add('opening');chime(1);pkT=setTimeout(pkGo,mOn()?850:650);}""")
rep("function openPack(){","""let pkT=null;
function pkGo(){clearTimeout(pkT);pkT=null;if(!pk||pk.step!=='sealed')return;pk.step='card';pk.i=0;pk.flipped=false;drawPack();}
function openPack(){""")

# ---------- the reveal: ink it in, stamp it; no sparks in the journal ----------
rep("""  if(!rv||rv.flipped)return;rv.flipped=true;
  const c=cardById(rv.id),st=$('#stage'),cv=$('#cover');cv.classList.add('open');""",
"""  if(!rv||rv.flipped)return;rv.flipped=true;
  const c=cardById(rv.id),st=$('#stage'),cv=$('#cover');inkStart(st,c);cv.classList.add('open');""")
rep("""  if(!pk||pk.step!=='card'||pk.flipped)return;pk.flipped=true;
  const c=pk.cards[pk.i],st=$('#stage'),cv=$('#cover');cv.classList.add('open');""",
"""  if(!pk||pk.step!=='card'||pk.flipped)return;pk.flipped=true;
  const c=pk.cards[pk.i],st=$('#stage'),cv=$('#cover');inkStart(st,c);cv.classList.add('open');""")
rep("""  if(!REDUCE)for(let i=0;i<R.sparks;i++){""","""  if(!REDUCE&&!stage.querySelector('.jrstamp'))for(let i=0;i<R.sparks;i++){""")
rep("""  if(e.target.closest('#cover')){if(ovMode==='reveal')revealFlip();else if(ovMode==='pack')packFlip();return;}""",
"""  if(e.target.closest('#cover')){if(ovMode==='reveal')revealFlip();else if(ovMode==='pack')packFlip();return;}
  if(inkT&&e.target.closest('#stage')){inkDone(true);return;}""")

# ---------- kept cards drift into the Binder ribbon ----------
rep("""function finishReveal(){
  const gained=rv&&rv.packGained;
  closeModal();tab='today';render();window.scrollTo(0,0);""",
"""function finishReveal(){
  const gained=rv&&rv.packGained,fly=snapFly($('#stage .tilt'));inkDone(false);
  closeModal();tab='today';render();window.scrollTo(0,0);flyToBinder(fly,'+1');""")
rep("""  else if(b.id==='packDone'){closeModal();tab='binder';""","""  else if(b.id==='packDone'){const fly=snapFly($('.sumgrid'));closeModal();flyToBinder(fly,'+5');tab='binder';""")

# ---------- embers roll up on the Hearth ----------
rep("""<small id="hEmbers">${e} ${e===1?'ember':'embers'}</small>""","""<small id="hEmbers">${embRoll(e,e===1?'ember':'embers')}</small>""")

# ---------- the Forge stamps what it makes ----------
rep("""openSheet(`<p class="muted center small">Hot from the Forge</p><div class="cbig">${fgImg(r.id,90,{cls:'cpop',alt:r.name})}</div>""",
"""openSheet(`<p class="muted center small">Hot from the Forge</p><div class="cbig">${fgImg(r.id,90,{cls:'cpop',alt:r.name})}<div class="jmade" aria-hidden="true"><b>MADE</b><span>signed, ${esc(s.nick||s.name)}</span></div></div>""")

# ---------- a newly found place is inked onto the map ----------
rep("""function placesSVG(ti){
  const n=placesFound(ti);if(!n)return '';const pts=placePts(ti),found=PLACES[ti].slice(0,n).map((p,i)=>[p,pts[i]]);""",
"""function placesSVG(ti){
  const n=placesFound(ti);let fresh=n;
  if(tab==='chronicle'){const k=String(ti),was=mSeen().pl[k];if(typeof was==='number'&&n>was&&mOn())fresh=was;mSeenLater(k,n);}
  if(!n)return '';const pts=placePts(ti),found=PLACES[ti].slice(0,n).map((p,i)=>[p,pts[i]]);""")
rep("""  s+=found.map(f=>`<g class="mp-place" shape-rendering="crispEdges">${lmPaths(f[0].k,ti,LMU,f[1][0],f[1][1]-lift(f[1]))}</g>`).join('');""",
"""  s+=found.map((f,i)=>`<g class="mp-place${i>=fresh?' jnew':''}" shape-rendering="crispEdges">${lmPaths(f[0].k,ti,LMU,f[1][0],f[1][1]-lift(f[1]))}</g>${i>=fresh?`<circle class="mp-ring" cx="${f[1][0]}" cy="${f[1][1]-lift(f[1])}" r="10"/>`:''}`).join('');""")


# ---------- the pack and the reveal open on a journal page too (as the close-up has since 0.47) ----------
rep("""  modal.innerHTML=`<div class="scrim dark" data-dismiss="${!!dismiss}"><div class="ov" role="dialog" aria-modal="true">${html}</div></div>`;modal.hidden=false;nameDialog();setTimeout(stageOn,0);""",
"""  modal.innerHTML=`<div class="scrim dark${lsOn()&&(ovMode==='reveal'||ovMode==='pack')?' jinsp jrv':''}" data-dismiss="${!!dismiss}"><div class="ov" role="dialog" aria-modal="true">${html}</div></div>`;modal.hidden=false;nameDialog();setTimeout(stageOn,0);""")

CSS=open('/home/claude/forge/motion48.css').read()
i=S.index("</style>",S.index("</style>")+1)
S=S[:i]+"\n"+CSS+"\n"+S[i:]

rep("""<ul class="newlist"><li><b>The whole journal.</b>""","""<ul class="newlist"><li><b>Ink and paper, moving.</b> A pack is a sealed envelope now: press the seal and the cards slide out. A new Forgeling is pencilled, inked and coloured in, then stamped. Kept cards drift into your binder, embers roll up on the Hearth, the Forge stamps what it makes, and new places are inked onto the map. A tap skips any of it, and it all stays still if you turn motion down.</li><li><b>The whole journal.</b>""")
m=re.search(r'<ul class="newlist">(.*?)</ul>',S,re.S); items=re.findall(r'<li>.*?</li>',m.group(1),re.S)
assert len(items)==9,len(items); rep(items[-1],"")

open('work.html','w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk48.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk48.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600])

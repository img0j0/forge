# Forge 0.23.0: a game for each realm, and a fuller first week. Reads base223.html, writes work.html.
src = open('base223.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

# ================= Games =================
rep('/* Nav */', r'''/* ---- 0.23: realm games ---- */
.pg{border-radius:0;border:3px solid rgba(255,255,255,.28)}
.pgbtnrow{display:flex;gap:10px;justify-content:center;width:100%;max-width:320px}
.pgbtnrow .ghost,.pgbtnrow .primary{flex:1}
.seed{position:absolute;bottom:-44px;width:48px;height:48px;border:0;background:none;padding:0;animation:drift linear forwards}
.seed::before{content:'';position:absolute;left:14px;top:8px;width:20px;height:20px;background:radial-gradient(circle,#FFFFFF 0 3px,transparent 3.5px),conic-gradient(from 0deg,#F4F0E8 0 10%,transparent 10% 25%,#F4F0E8 25% 35%,transparent 35% 50%,#F4F0E8 50% 60%,transparent 60% 75%,#F4F0E8 75% 85%,transparent 85%);border-radius:50%;opacity:.95}
.seed::after{content:'';position:absolute;left:23px;top:27px;width:2px;height:12px;background:#CFE8C0}
.seed.caught,.emb.caught,.flake.caught{animation:none;opacity:0;transform:scale(1.8);transition:.15s}
@keyframes drift{0%{transform:translate(0,0)}25%{transform:translate(14px,-110px)}50%{transform:translate(-10px,-220px)}75%{transform:translate(12px,-320px)}100%{transform:translate(0,-420px)}}
.fire{position:absolute;left:50%;bottom:40px;width:64px;height:120px;transform:translateX(-50%);transform-origin:50% 100%;pointer-events:none}
.fire i{position:absolute;left:0;right:0;bottom:0;height:var(--h,60%);background:linear-gradient(#FFF3B0,#FFD36B 30%,#FF8A2E 65%,#E5441E);clip-path:polygon(50% 0,64% 22%,78% 14%,82% 46%,100% 62%,92% 100%,8% 100%,0 62%,18% 46%,22% 14%,36% 22%);transition:height .15s}
.fire b{position:absolute;left:-16px;right:-16px;bottom:-12px;height:14px;background:repeating-linear-gradient(90deg,#6B4A2E 0 10px,#4B331F 10px 12px)}
.heat{position:absolute;left:12px;right:12px;top:10px;height:10px;background:rgba(255,255,255,.15)}
.heat i{display:block;height:100%;background:linear-gradient(90deg,#E5441E,#FFD36B);width:60%;transition:width .1s}
.emb{position:absolute;width:48px;height:48px;border:0;padding:0;background:none;animation:embIn .2s ease-out}
.emb::before{content:'';position:absolute;inset:12px;background:#FF8A2E;box-shadow:0 0 0 4px #E5441E,0 0 14px 4px rgba(255,140,40,.6);clip-path:polygon(25% 0,75% 0,100% 25%,100% 75%,75% 100%,25% 100%,0 75%,0 25%)}
@keyframes embIn{from{transform:scale(.3);opacity:0}}
.water{position:absolute;left:12px;right:12px;top:150px;height:40px;background:repeating-linear-gradient(90deg,#3E7FB8 0 8px,#4F93C8 8px 16px)}
.calm{position:absolute;top:0;bottom:0;background:#A6D8F2;box-shadow:inset 0 0 0 2px #FFFFFF}
.stone{position:absolute;top:-22px;width:22px;height:14px;margin-left:-11px;background:#9AA0A8;box-shadow:inset 0 -4px 0 #6E737C;clip-path:polygon(15% 0,85% 0,100% 50%,85% 100%,15% 100%,0 50%)}
.skips{position:absolute;left:0;right:0;top:220px;text-align:center;font:600 15px var(--display);color:#D9D2F5}
.ripple{position:absolute;top:160px;width:20px;height:20px;margin-left:-10px;border:2px solid #FFFFFF;border-radius:50%;animation:rip .5s ease-out forwards}
@keyframes rip{to{transform:scale(3);opacity:0}}
.basket{position:absolute;bottom:14px;width:64px;height:22px;margin-left:-32px;background:#B9A6F0;box-shadow:inset 0 -6px 0 #7E6BC4;clip-path:polygon(0 0,100% 0,88% 100%,12% 100%)}
.flake{position:absolute;width:20px;height:20px;margin-left:-10px;background:#FFFFFF;clip-path:polygon(45% 0,55% 0,55% 38%,88% 18%,94% 27%,62% 46%,62% 54%,94% 73%,88% 82%,55% 62%,55% 100%,45% 100%,45% 62%,12% 82%,6% 73%,38% 54%,38% 46%,6% 27%,12% 18%,45% 38%)}
.lanterns{position:absolute;inset:24px;display:grid;grid-template-columns:1fr 1fr;gap:18px}
.lant{border:0;background:#2B2352;box-shadow:inset 0 0 0 3px #4A4180;display:grid;place-items:center;min-height:44px;transition:background .12s,box-shadow .12s}
.lant::before{content:'';width:34px;height:46px;background:var(--lc);opacity:.35;clip-path:polygon(30% 0,70% 0,70% 10%,90% 22%,90% 84%,70% 100%,30% 100%,10% 84%,10% 22%,30% 10%)}
.lant.on{background:#4A3E86;box-shadow:inset 0 0 0 3px #FFE9A8,0 0 22px 6px color-mix(in srgb,var(--lc) 60%,transparent)}
.lant.on::before{opacity:1}
.lant:disabled{cursor:default}
.pgmsg{position:absolute;left:0;right:0;bottom:12px;text-align:center;color:#D9D2F5;font-size:14px}
.arrows{display:flex;gap:10px;justify-content:center;width:100%;max-width:320px}
.arrows button{flex:1;min-height:48px;font:600 22px var(--display)}
@media (prefers-reduced-motion: reduce){.lant{transition:none}}
.pg-meadow{background:linear-gradient(#1B2C4A,#2A4A5A 62%,#3F7A45 62%,#356A3C) !important}
.pg-ember{background:linear-gradient(#1E0F18,#3A1A1A 70%,#2B1B16 70%,#21140F) !important}
.pg-tide{background:linear-gradient(#18284A,#2B4870 44%,#C9B27A 74%,#B59C66) !important}
.pg-frost{background:linear-gradient(#162139,#2C3F66 80%,#DCE8F7 80%,#C7D6EE) !important}
.pg-dusk{background:linear-gradient(#21183F,#3A2B66 78%,#1B1633 78%) !important}
.pgmate{position:absolute;width:96px;height:96px;image-rendering:pixelated;pointer-events:none;z-index:1}
.pgmate.hop{animation:mateHop .28s ease-out}
@keyframes mateHop{40%{transform:translateY(-10px)}}
.pg-meadow .pgmate{left:8px;bottom:6px}
.pg-ember .pgmate{left:14px;bottom:30px}
.pg-tide .pgmate{left:10px;bottom:4px}
.pg-dusk .pgmate{left:50%;margin-left:-48px;bottom:-6px}
.pg-dusk .lanterns{inset:20px 24px 104px}
.basket{background:none !important;box-shadow:none !important;clip-path:none !important;width:80px;height:80px;margin-left:-40px;bottom:2px}
.basket .pgmate{position:static;width:80px;height:80px}
@media (prefers-reduced-motion: reduce){.pgmate.hop{animation:none}}
/* Nav */''')

GAMES_JS = r'''
/* ---- A game for each realm. Played from the Hearth: within your three visits it grows your bond (and, on a great
   round, might turn up a curio from that realm); after that you can keep playing just for fun. ---- */
const GAMES=[
 {id:'meadow',t:'Dandelion Drift',h:'Tap the seeds before they float away.',hi:10,mid:5,u:['seed','seeds']},
 {id:'ember',t:'Keep the Fire',h:'Tap the embers to feed the fire. Keep it burning.',hi:12,mid:6,u:['ember','embers']},
 {id:'tide',t:'Skipping Stones',h:'Tap Skip when the stone is over the calm water.',hi:6,mid:3,u:['skip','skips']},
 {id:'frost',t:'Snowflake Catch',h:'Slide to catch the falling snowflakes.',hi:10,mid:5,u:['snowflake','snowflakes']},
 {id:'dusk',t:'Lantern Lights',h:'Watch the lanterns, then light them in the same order.',hi:5,mid:3,u:['lantern','lanterns']}];
const gameFor=c=>GAMES[Math.abs(c.theme|0)%5];
const unitOf=(G,n)=>n+' '+G.u[n===1?0:1];
let game=null;
function openPlay(c){
  const n=c.nick||c.name,free=visitsLeft()<1,G=gameFor(c);
  if(REDUCE&&G.id!=='dusk'){if(!free)doVisit(c,'sit',1,lineFor(c,'sit',''));else toast('With reduced motion on, this game rests. Try a Dusk Forgeling’s lantern game.');return;}
  const best=state.games.best[G.id]||0;
  openOverlay(`<p class="rv-title">${G.t}</p><p class="rv-hint">${G.h}${best?` Best: ${unitOf(G,best)}.`:''}</p>
    <div class="pg pg-${G.id}" id="pg" aria-label="${G.t} play area"></div>
    <div class="row" style="width:100%;max-width:320px"><span class="rv-title" id="pgScore" aria-live="polite">0</span><span class="rv-hint" id="pgTime">${G.id==='dusk'?'':'15s'}</span></div>
    ${G.id==='tide'?'<div class="pgbtnrow"><button class="primary" id="pgSkip">Skip</button></div>':''}
    ${G.id==='frost'?'<div class="arrows"><button class="ghost" id="pgL" aria-label="Move left">←</button><button class="ghost" id="pgR" aria-label="Move right">→</button></div>':''}
    ${free?'<p class="rv-hint small" style="margin:0">Just for fun: your visits are used up for today.</p>':''}
    <button class="ghost" id="pgSit" data-cid="${c.id}">${free?'Stop playing':'Just sit together instead'}</button>`,false);
  game={c,G,free,score:0,alive:true,timers:[],raf:0};const pgEl=$('#pg');if(pgEl&&G.id!=='frost')pgEl.insertAdjacentHTML('beforeend',mateHTML(c));
  pgT={stop:()=>{if(!game)return;game.alive=false;game.timers.forEach(t=>{clearInterval(t);clearTimeout(t);});cancelAnimationFrame(game.raf);}};
  ({meadow:gMeadow,ember:gEmber,tide:gTide,frost:gFrost,dusk:gDusk})[G.id]();
}
const SPR_URL={};
function spriteURL(c){const k=ckey(c);if(SPR_URL[k])return SPR_URL[k];try{const e=prep(c);if(!e.sp[0])e.sp[0]=buildSprite(e.spec,0,0);const g=e.sp[0],cv=document.createElement('canvas');cv.width=32;cv.height=32;const x=cv.getContext('2d'),im=x.createImageData(32,32);for(let i=0;i<1024;i++){const sl=g[i];if(!sl)continue;const q=e.pal[sl];im.data[i*4]=q[0];im.data[i*4+1]=q[1];im.data[i*4+2]=q[2];im.data[i*4+3]=255;}x.putImageData(im,0,0);return SPR_URL[k]=cv.toDataURL();}catch(err){return '';}}
const mateHTML=c=>{const u=spriteURL(c);return u?`<img class="pgmate" src="${u}" alt="">`:'';};
const gScore=v=>{game.score=v;const s=$('#pgScore');if(s)s.textContent=v;const m=document.querySelector('#pg .pgmate');if(m){m.classList.remove('hop');void m.offsetWidth;m.classList.add('hop');}};
function gClock(sec){let left=sec;game.timers.push(setInterval(()=>{if(!game||!game.alive)return;left--;const t=$('#pgTime');if(t)t.textContent=Math.max(0,left)+'s';if(left<=0)finishGame();},1000));}
function gMeadow(){
  const area=$('#pg');
  const spawn=()=>{if(!game||!game.alive)return;const b=document.createElement('button');b.className='seed';b.type='button';b.setAttribute('aria-label','Seed');b.style.left=(4+Math.random()*78)+'%';b.style.animationDuration=(2.6+Math.random()*1.2)+'s';
    b.addEventListener('pointerdown',ev=>{ev.preventDefault();if(b._c||!game||!game.alive)return;b._c=1;gScore(game.score+1);b.classList.add('caught');chime(0);setTimeout(()=>b.remove(),160);});
    b.addEventListener('animationend',()=>b.remove());area.appendChild(b);};
  spawn();game.timers.push(setInterval(spawn,560));gClock(15);
}
function gEmber(){
  const area=$('#pg');area.innerHTML='<div class="heat" aria-hidden="true"><i></i></div><div class="fire" aria-hidden="true"><i></i><b></b></div><p class="pgmsg" id="pgMsg"></p>'+mateHTML(game.c);
  let heat=60;const draw=()=>{const f=area.querySelector('.fire i'),h=area.querySelector('.heat i');if(f)f.style.setProperty('--h',Math.max(8,heat)+'%');if(h)h.style.width=heat+'%';};draw();
  game.timers.push(setInterval(()=>{if(!game||!game.alive)return;heat=Math.max(0,heat-1.1);draw();if(heat<=0){const m=$('#pgMsg');if(m)m.textContent='The fire went out.';finishGame();}},100));
  const spawn=()=>{if(!game||!game.alive)return;const b=document.createElement('button');b.className='emb';b.type='button';b.setAttribute('aria-label','Ember');
    let x,y;do{x=6+Math.random()*80;y=14+Math.random()*70;}while(x>32&&x<62&&y>44);b.style.left=x+'%';b.style.top=y+'%';
    b.addEventListener('pointerdown',ev=>{ev.preventDefault();if(b._c||!game||!game.alive)return;b._c=1;heat=Math.min(100,heat+13);draw();gScore(game.score+1);b.classList.add('caught');chime(0);setTimeout(()=>b.remove(),160);});
    area.appendChild(b);setTimeout(()=>{if(!b._c)b.remove();},1400);};
  spawn();game.timers.push(setInterval(spawn,620));gClock(15);
}
function gTide(){
  const area=$('#pg');area.innerHTML='<div class="water" aria-hidden="true"><div class="calm" id="pgCalm"></div><div class="stone" id="pgStone"></div></div><p class="skips" id="pgSkips">Three misses and the stone sinks.</p>'+mateHTML(game.c);
  let zone=.30,miss=0,speed=1.6,t0=performance.now();const calm=$('#pgCalm'),stone=$('#pgStone');
  const place=()=>{calm.style.left=((1-zone)/2*100)+'%';calm.style.width=(zone*100)+'%';};place();
  const pos=()=>(Math.sin((performance.now()-t0)/1000*speed*Math.PI)+1)/2;
  const loop=()=>{if(!game||!game.alive)return;stone.style.left=(pos()*100)+'%';game.raf=requestAnimationFrame(loop);};loop();
  game.skip=()=>{if(!game||!game.alive)return;const p=pos(),hit=Math.abs(p-.5)<=zone/2;const r=document.createElement('div');r.className='ripple';r.style.left='calc(12px + '+(p*100)+'% - '+(p*24)+'px)';area.appendChild(r);setTimeout(()=>r.remove(),520);
    if(hit){gScore(game.score+1);zone=Math.max(.12,zone-.03);speed=Math.min(3.2,speed+.18);place();chime(0);$('#pgSkips').textContent=game.score===1?'One skip!':game.score+' skips!';}
    else{miss++;sfx('no');$('#pgSkips').textContent=miss>=3?'The stone sank.':(3-miss)+(3-miss===1?' miss left.':' misses left.');if(miss>=3)finishGame();}};
  area.addEventListener('pointerdown',ev=>{if(ev.target.closest('button'))return;ev.preventDefault();game&&game.skip&&game.skip();});
  gClock(15);
}
function gFrost(){
  const area=$('#pg');area.innerHTML='<div class="basket" id="pgBasket" aria-hidden="true">'+mateHTML(game.c)+'</div>';
  const W=()=>area.clientWidth,bk=$('#pgBasket');let bx=.5,flakes=[],last=performance.now();
  const setX=v=>{bx=Math.max(.08,Math.min(.92,v));bk.style.left=(bx*100)+'%';};setX(.5);
  const fromEv=ev=>{const r=area.getBoundingClientRect();setX((ev.clientX-r.left)/r.width);};
  area.addEventListener('pointerdown',ev=>{ev.preventDefault();fromEv(ev);});area.addEventListener('pointermove',ev=>{if(ev.pressure>0||ev.pointerType==='mouse')fromEv(ev);});
  game.nudge=d=>setX(bx+d);
  const spawn=()=>{if(!game||!game.alive)return;const f=document.createElement('div');f.className='flake';f.setAttribute('aria-hidden','true');const o={el:f,x:.06+Math.random()*.88,y:-20,v:70+Math.random()*60};f.style.left=(o.x*100)+'%';f.style.top='-20px';area.appendChild(f);flakes.push(o);};
  const loop=now=>{if(!game||!game.alive)return;const dt=Math.min(.05,(now-last)/1000);last=now;const H=area.clientHeight,bw=72/Math.max(1,W());
    flakes=flakes.filter(o=>{o.y+=o.v*dt;o.el.style.top=o.y+'px';if(o.y>H-84&&o.y<H-40&&Math.abs(o.x-bx)<bw/2+.03){gScore(game.score+1);chime(0);o.el.remove();return false;}if(o.y>H){o.el.remove();return false;}return true;});
    game.raf=requestAnimationFrame(loop);};
  game.raf=requestAnimationFrame(loop);spawn();game.timers.push(setInterval(spawn,480));gClock(15);
}
function gDusk(){
  const area=$('#pg'),cols=['#FFD36B','#F29BB5','#A6D8F2','#B5DDB5'],names=['Gold','Rose','Blue','Green'];
  area.innerHTML=`<div class="lanterns">${cols.map((c,i)=>`<button class="lant" data-lant="${i}" style="--lc:${c}" aria-label="${names[i]} lantern" disabled></button>`).join('')}</div><p class="pgmsg" id="pgMsg">Watch.</p>`+mateHTML(game.c);
  const L=[...area.querySelectorAll('.lant')],seq=[],t=$('#pgTime');let step=0,input=false;
  const flash=(i,ms)=>{L[i].classList.add('on');chime(0);game.timers.push(setTimeout(()=>L[i].classList.remove('on'),ms));};
  const round=()=>{if(!game||!game.alive)return;input=false;L.forEach(b=>b.disabled=true);seq.push(Math.floor(Math.random()*4));step=0;const m=$('#pgMsg');if(m)m.textContent='Watch.';if(t)t.textContent='Round '+seq.length;
    seq.forEach((v,k)=>game.timers.push(setTimeout(()=>flash(v,REDUCE?380:420),600+k*640)));
    game.timers.push(setTimeout(()=>{if(!game||!game.alive)return;input=true;L.forEach(b=>b.disabled=false);if(m)m.textContent='Your turn.';L[0].focus({preventScroll:true});},600+seq.length*640));};
  L.forEach((b,i)=>b.addEventListener('click',()=>{if(!input||!game||!game.alive)return;flash(i,220);
    if(i!==seq[step]){input=false;const m=$('#pgMsg');if(m)m.textContent='The lanterns flicker out.';sfx('no');game.timers.push(setTimeout(finishGame,700));return;}
    step++;if(step===seq.length){gScore(seq.length);if(seq.length>=12){game.timers.push(setTimeout(finishGame,500));return;}input=false;game.timers.push(setTimeout(round,700));}}));
  round();
}
function finishGame(){
  const g=game;if(!g||!g.alive)return;if(pgT){pgT.stop();}pgT=null;game=null;
  const G=g.G,score=g.score,best=state.games.best[G.id]||0,nb=score>best&&score>0;if(nb)state.games.best[G.id]=score;state.games.played=(state.games.played||0)+1;save();
  const n=g.c.nick||g.c.name;
  if(g.free){
    openOverlay(`<p class="rv-title">${G.t}</p><p class="rv-title" style="font-size:30px">${unitOf(G,score)}</p><p class="rv-hint">${nb?'A new best!':best?'Best: '+unitOf(G,best)+'.':''} ${esc(n)} ${g.c.dark?'seems quietly pleased.':'had a lovely time.'}</p>
      <div class="pgbtnrow"><button class="primary" id="pgAgain" data-cid="${g.c.id}">Play again</button><button class="ghost" id="pgDone">Done</button></div>`,false);
    return;
  }
  const pts=score>=G.hi?3:score>=G.mid?2:1;
  let line=g.c.dark?`${n} rumbles with approval. ${unitOf(G,score)}.`:`${n} cheers. ${unitOf(G,score)}!`;
  if(pts===3&&state.games.curioDay!==todayKey()&&Math.random()<.4){
    const ti=Math.abs(g.c.theme|0)%5,all=rCurios(ti),un=all.filter(x=>!state.curios[x.id]),pool=un.length?un:all,cu=pool[Math.floor(Math.random()*pool.length)];
    if(cu){const cur=state.curios[cu.id]||{n:0,cid:g.c.id,at:todayKey()};cur.n++;state.curios[cu.id]=cur;state.games.curioDay=todayKey();line+=` Afterwards, ${n} found something nearby: ${cu.name.toLowerCase()}.`;}
  }
  if(nb)line+=' A new best!';
  doVisit(g.c,'play',pts,line);
}
document.addEventListener('click',e=>{
  const b=e.target.closest&&e.target.closest('#modal button');if(!b)return;
  if(b.id==='pgSkip'&&game&&game.skip)game.skip();
  else if(b.id==='pgL'&&game&&game.nudge)game.nudge(-.12);
  else if(b.id==='pgR'&&game&&game.nudge)game.nudge(.12);
  else if(b.id==='pgAgain'){const c=cardById(+b.dataset.cid);closeModal();if(c)openPlay(c);}
  else if(b.id==='pgDone'){closeModal();renderHearth();}
});
document.addEventListener('keydown',e=>{if(!game||!game.alive)return;if(game.nudge&&(e.key==='ArrowLeft'||e.key==='ArrowRight')){e.preventDefault();game.nudge(e.key==='ArrowLeft'?-.08:.08);}else if(game.skip&&(e.key===' '||e.key==='Enter')&&document.activeElement&&document.activeElement.id!=='pgSit'){e.preventDefault();game.skip();}});
document.addEventListener('visibilitychange',()=>{if(document.hidden&&game&&game.alive)finishGame();});
'''
rep('/* ================= Start ================= */', GAMES_JS + '\n/* ================= Start ================= */')

# remove the old Spark Catch
start = src.index('function openPlay(c){\n  const n=c.nick||c.name;\n  if(REDUCE){doVisit')
end = src.index('let pickSel=[];')
src = src[:start] + src[end:]

# Sit together: in free play it simply stops
rep("  else if(b.id==='pgSit'){const c=cardById(+b.dataset.cid);if(c){if(pgT){pgT.stop();pgT=null;}doVisit(c,'sit',1,lineFor(c,'sit',''));}}",
    "  else if(b.id==='pgSit'){const c=cardById(+b.dataset.cid);if(c){const fr=game&&game.free;if(pgT){pgT.stop();pgT=null;}game=null;if(fr){closeModal();renderHearth();}else doVisit(c,'sit',1,lineFor(c,'sit',''));}}")

# The Play button: name the game, stay open for free play once visits are used up
rep("""        <button class="act" id="hPlay" ${left&&!away?'':'disabled'}>Play<small>+1 to +3</small></button>""",
    """        <button class="act" id="hPlay" ${!away?'':'disabled'}>Play<small>${left?'+1 to +3':'Just for fun'}</small></button>""")
rep("""      <p class="muted small" style="margin-top:8px">${away?`${esc(n)} is out wandering. Visits start again when they are back.`:left?`Visits left today: ${left} of 3.`:'The fire is low for today. Your Forgelings will be glad to see you tomorrow.'}</p>""",
    """      <p class="muted small" style="margin-top:8px">${away?`${esc(n)} is out wandering. Visits start again when they are back.`:left?`Visits left today: ${left} of 3. Play is ${esc(gameFor(c).t)}${state.games.best[gameFor(c).id]?`, best ${unitOf(gameFor(c),state.games.best[gameFor(c).id])}`:''}.`:`The fire is low for today. You can still play ${esc(gameFor(c).t)} just for fun.`}</p>""")

# state
rep("request:null,reqLast:'',reqDone:0,keepsR:[]};}", "request:null,reqLast:'',reqDone:0,keepsR:[],games:{best:{},played:0,curioDay:''}};}")
rep("  s.keepsR=Array.isArray(s.keepsR)?", """  {const g=s.games&&typeof s.games==='object'&&!Array.isArray(s.games)?s.games:{};const b=g.best&&typeof g.best==='object'&&!Array.isArray(g.best)?g.best:{};const ok={};['meadow','ember','tide','frost','dusk'].forEach(k=>{if(Number.isFinite(b[k])&&b[k]>0)ok[k]=Math.min(999,Math.round(b[k]));});s.games={best:ok,played:int(g.played,0,1e7,0),curioDay:typeof g.curioDay==='string'?g.curioDay:''};}
  s.keepsR=Array.isArray(s.keepsR)?""")

# ================= A fuller first week =================
rep("{id:'rug',name:'A woven rug',need:3},{id:'lights',name:'A string of lanterns',need:10},{id:'tree',name:'A little tree',need:30},{id:'flies',name:'Fireflies',need:60},",
    "{id:'rug',name:'A woven rug',need:1},{id:'lights',name:'A string of lanterns',need:5},{id:'tree',name:'A little tree',need:15},{id:'flies',name:'Fireflies',need:40},")
rep("(ok?`For ${f.need} callings done.`:`After ${f.need} callings done. ${t.all} so far.`)",
    "(ok?`For ${f.need===1?'your first calling':f.need+' callings done'}.`:`After ${f.need===1?'your first calling':f.need+' callings done'}. ${t.all} so far.`)")
rep("  if(state.request||state.hearth.sleep||dayN()<3||(state.wstat.back||0)<1)return;",
    "  if(state.request||state.hearth.sleep||dayN()<2||(state.wstat.back||0)<1)return;")
# the first wander is short, so day one has a return
rep("  state.wander={id:c.id,start:now,ready:now+WANDER_MS,",
    "  state.wander={id:c.id,start:now,ready:now+((state.wstat.sent||0)===0?20*60*1000:WANDER_MS),")
rep("""<p class="muted small">Realms on your map. They are back in about three hours.</p>""",
    """<p class="muted small">Realms on your map. ${(state.wstat.sent||0)===0?'This first time, they are back in about 20 minutes.':'They are back in about three hours.'}</p>""")

# A request and something new by the fire can arrive together: say both.
rep("hf.msg=nf.length===1?`Something new by the fire: ${f.name.toLowerCase()}.`", "hf.msg=(/small request\\.$/.test(hf.msg||'')?hf.msg+' ':'')+(nf.length===1?`Something new by the fire: ${f.name.toLowerCase()}.`")
rep(":`${nf.length} new things by the fire. Have a look around.`;state.hearth.fseen", ":`${nf.length} new things by the fire. Have a look around.`);state.hearth.fseen")

# ================= version and what's new =================
rep('<title>Forge (prototype 0.22.3)</title>', '<title>Forge (prototype 0.23.0)</title>')
rep("const VERSION='prototype 0.22.3';", "const VERSION='prototype 0.23.0';")
rep('const SEEN_V=26;', 'const SEEN_V=27;')
rep("""<ul class="newlist"><li><b>A new daily card.</b>""",
    """<ul class="newlist"><li><b>Play together.</b> Every realm has its own little game: Dandelion Drift, Keep the Fire, Skipping Stones, Snowflake Catch and Lantern Lights. Play from the Hearth to grow your bond. A great round might turn up a curio. Once your visits are used, you can keep playing just for fun.</li>
    <li><b>A fuller first week.</b> Your first wander comes back in about 20 minutes, the rug appears after your first calling, and requests can start on day two.</li>
    <li><b>A new daily card.</b>""")
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src))

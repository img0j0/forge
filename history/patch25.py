# Forge 0.25.0: the realm games, deepened. Your Forgeling shapes its game (a trait from its stats, a bond gift at
# Close, a twist for dark Forgelings), and every game feels better: a Start card, sounds, sparkles, streaks, rounds that
# build up, and a clear finish. Reads base242.html, writes work.html.
src = open('base242.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

# ================= CSS =================
rep('/* Nav */', r'''/* ---- 0.25: deeper games ---- */
.pgready{position:absolute;inset:0;z-index:4;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:7px;padding:12px 16px;background:rgba(16,11,34,.86);text-align:center;color:#F4EEFF}
.pgready img{width:64px;height:64px;image-rendering:pixelated}
.pgready p{margin:0;font-size:14px;line-height:1.35;color:#F4EEFF}
.pgready p b{color:#FFD36B;font-weight:700}
.pgready p.lock{color:#CFC6E8}
.pgready p.tw b{color:#FF9EB0}
.pgready .primary{min-width:150px;margin-top:4px}
.pgstreak{position:absolute;right:8px;top:6px;z-index:3;font:600 14px var(--display);color:#FFE9A8;text-shadow:0 1px 0 #000;pointer-events:none}
.pg .pgmsg{z-index:3;text-shadow:0 1px 0 #000;color:#F4EEFF;pointer-events:none}
.pt{position:absolute;width:6px;height:6px;margin:-3px 0 0 -3px;pointer-events:none;z-index:3;animation:ptFly .5s ease-out forwards}
@keyframes ptFly{to{transform:translate(var(--dx),var(--dy));opacity:0}}
.ptx{position:absolute;z-index:3;pointer-events:none;font:600 16px var(--display);color:#FFF3B0;text-shadow:0 1px 0 #000;white-space:nowrap;transform:translate(-50%,-50%);animation:ptUp .7s ease-out forwards}
@keyframes ptUp{to{transform:translate(-50%,-160%);opacity:0}}
.pgend{position:absolute;inset:0;z-index:5;display:grid;place-items:center;font:600 28px var(--display);color:#FFF3B0;text-shadow:0 2px 0 #000;background:rgba(0,0,0,.35);pointer-events:none;animation:pgPop .25s ease-out}
@keyframes pgPop{from{transform:scale(.7);opacity:0}}
.seed.gold::before{background:radial-gradient(circle,#FFF6C8 0 3px,transparent 3.5px),conic-gradient(from 0deg,#FFD36B 0 10%,transparent 10% 25%,#FFD36B 25% 35%,transparent 35% 50%,#FFD36B 50% 60%,transparent 60% 75%,#FFD36B 75% 85%,transparent 85%);box-shadow:0 0 10px 3px rgba(255,211,107,.55)}
.seed.thorn::before{background:#6B4A2E;box-shadow:0 0 0 2px #2E1E12;clip-path:polygon(50% 0,60% 30%,95% 20%,72% 48%,100% 70%,64% 68%,55% 100%,42% 70%,8% 82%,30% 52%,0 28%,38% 32%)}
.seed.thorn::after{background:#4B331F}
.seed.puff{width:64px;height:64px;z-index:2}
.seed.gold{z-index:1}
.seed.puff::before{left:12px;top:6px;width:40px;height:40px;background:radial-gradient(circle,#FFFFFF 0 5px,transparent 5.5px),repeating-conic-gradient(#F4F0E8 0 6deg,transparent 6deg 20deg);box-shadow:0 0 12px 4px rgba(255,255,255,.35)}
.seed.puff::after{left:31px;top:44px;height:18px}
.emb.log::before{inset:14px 6px;background:#9A6A3E;box-shadow:inset 0 -4px 0 #6B4A2E,0 0 0 3px #4B331F;clip-path:none;border-radius:2px}
.pg.wind{box-shadow:inset 0 0 50px 10px rgba(150,205,255,.55)}
.flake.big{width:32px;height:32px;margin-left:-16px;filter:drop-shadow(0 0 6px rgba(255,255,255,.8))}
.flake.hail{clip-path:none;border-radius:50%;width:18px;height:18px;margin-left:-9px;background:#8CA3BA;box-shadow:inset -3px -3px 0 #5E7690}
.pg-dusk .pgmsg{top:2px;bottom:auto}
@media (prefers-reduced-motion: reduce){.pgend{animation:none}}
/* Nav */''')

# ================= the games =================
start = src.index('/* ---- A game for each realm. Played from the Hearth')
end_marker = "document.addEventListener('visibilitychange',()=>{if(document.hidden&&game&&game.alive)finishGame();});\n"
end = src.index(end_marker) + len(end_marker)
assert src.count(end_marker) == 1

GAMES_JS = r'''/* ---- The realm games (0.25). Played from the Hearth. Your Forgeling shapes its game: one of its stats is a trait, bond
   at Close brings a gift, and a dark Forgeling plays its realm's twist. Within your three visits a round grows your bond
   (a great round may turn up a curio); after that you can keep playing just for fun. ---- */
const GAMES=[
 {id:'meadow',t:'Dandelion Drift',h:'Tap the seeds before they float away. Golden seeds are worth 3.',hi:42,mid:25,u:['point','points'],si:1,
  trait:'golden seeds turn up more often',gift:'now and then a dandelion puff drifts by. Tap it to scatter seeds.',twist:'thorny burrs drift up too. Tapping one costs 2 and breaks your streak.'},
 {id:'ember',t:'Keep the Fire',h:'Tap the embers to feed the fire. Keep it burning.',hi:40,mid:24,u:['point','points'],si:0,
  trait:'the fire burns down more slowly',gift:'logs turn up now and then. Tap one for a big blaze, worth 3.',twist:'cold gusts blow through, and the fire burns down twice as fast while they last.'},
 {id:'tide',t:'Skipping Stones',h:'Tap Skip, or anywhere on the water, when the stone is over the calm water.',hi:9,mid:5,u:['skip','skips'],si:2,
  trait:'the calm water is wider',gift:'every fifth skip, a lucky stone widens the calm water again.',twist:'the calm water drifts from side to side.'},
 {id:'frost',t:'Snowflake Catch',h:'Drag to move. Catch the snowflakes as they fall.',hi:30,mid:18,u:['point','points'],si:2,
  trait:'the snow falls more gently',gift:'big snowflakes fall now and then, worth 3.',twist:'hailstones fall too. Catching one costs 2 and breaks your streak.'},
 {id:'dusk',t:'Lantern Lights',h:'Watch the lanterns, then light them in the same order.',hi:7,mid:4,u:['lantern','lanterns'],si:1,
  trait:'the lanterns glow for longer',gift:'the evening star forgives one slip each game.',twist:'the lanterns are shown a little faster each round.'}];
const gameFor=c=>GAMES[Math.abs(c.theme|0)%5];
const unitOf=(G,n)=>n+' '+G.u[n===1?0:1];
const statName=(c,i)=>(c.dark?['Might','Dread','Guile']:['Grit','Spark','Calm'])[i];
const gTrait=(c,G)=>{const v=Array.isArray(c.stats)?+c.stats[G.si]:0;return Math.max(0,Math.min(1,((Number.isFinite(v)?v:15)-15)/84));};
const GIFT_LV=3;
let game=null;
function openPlay(c){
  const free=visitsLeft()<1,G=gameFor(c),best=state.games.best[G.id]||0,gift=bondLevel(c)>=GIFT_LV,twist=!!c.dark,si=G.si,sv=Array.isArray(c.stats)?c.stats[si]:'';
  const ready=`<div class="pgready" id="pgReady"><img src="${spriteURL(c)}" alt="">
      <p><b>${statName(c,si)} ${esc(String(sv))}</b>: ${G.trait}.</p>
      ${gift?`<p><b>Bond gift</b>: ${G.gift}</p>`:`<p class="lock">At ${BOND_NAMES[GIFT_LV-1]} bond: ${G.gift}</p>`}
      ${twist?`<p class="tw"><b>${esc(realmName(c))} twist</b>: ${G.twist}</p>`:''}
      <button class="primary" id="pgGo">Start</button></div>`;
  openOverlay(`<p class="rv-title">${G.t}</p><p class="rv-hint">${G.h}${best?` Best: ${unitOf(G,best)}.`:''}</p>
    <div class="pg pg-${G.id}" id="pg" aria-label="${G.t} play area"><span class="pgstreak" id="pgStreak" aria-hidden="true"></span><p class="pgmsg" id="pgMsg"></p>${G.id!=='frost'?mateHTML(c):''}${ready}</div>
    <div class="row" style="width:100%;max-width:320px"><span class="rv-title" id="pgScore" aria-live="polite">0</span><span class="rv-hint" id="pgTime">${G.id==='dusk'?'':'20s'}</span></div>
    ${G.id==='tide'?'<div class="pgbtnrow"><button class="primary" id="pgSkip">Skip</button></div>':''}
    ${G.id==='frost'?'<div class="arrows"><button class="ghost" id="pgL" aria-label="Move left">←</button><button class="ghost" id="pgR" aria-label="Move right">→</button></div>':''}
    ${free?'<p class="rv-hint small" style="margin:0">Just for fun: your visits are used up for today.</p>':''}
    <button class="ghost" id="pgSit" data-cid="${c.id}">${free?'Stop playing':'Just sit together instead'}</button>`,false);
  game={c,G,free,score:0,combo:0,alive:true,started:false,timers:[],raf:0,tr:gTrait(c,G),gift,twist};
  pgT={stop:()=>{if(!game)return;game.alive=false;game.started=false;game.timers.forEach(t=>{clearInterval(t);clearTimeout(t);});clearTimeout(game.ct);cancelAnimationFrame(game.raf);}};
  const go=$('#pgGo');if(go)go.focus({preventScroll:true});
}
function gStart(){
  const g=game;if(!g||!g.alive||g.started||g.ending)return;const r=$('#pgReady');if(r)r.remove();g.started=true;gTone('go');
  ({meadow:gMeadow,ember:gEmber,tide:gTide,frost:gFrost,dusk:gDusk})[g.G.id]();
}
const SPR_URL={};
function spriteURL(c){const k=ckey(c);if(SPR_URL[k])return SPR_URL[k];try{const e=prep(c);if(!e.sp[0])e.sp[0]=buildSprite(e.spec,0,0);const g=e.sp[0],cv=document.createElement('canvas');cv.width=32;cv.height=32;const x=cv.getContext('2d'),im=x.createImageData(32,32);for(let i=0;i<1024;i++){const sl=g[i];if(!sl)continue;const q=e.pal[sl];im.data[i*4]=q[0];im.data[i*4+1]=q[1];im.data[i*4+2]=q[2];im.data[i*4+3]=255;}x.putImageData(im,0,0);return SPR_URL[k]=cv.toDataURL();}catch(err){return '';}}
const mateHTML=c=>{const u=spriteURL(c);return u?`<img class="pgmate" src="${u}" alt="">`:'';};
/* ---- shared feel: score, streaks, sparkles, sounds, messages, the finish ---- */
const gOn=()=>!!(game&&game.alive&&game.started);
const gScore=v=>{game.score=v;const s=$('#pgScore');if(s)s.textContent=v;const m=document.querySelector('#pg .pgmate');if(m){m.classList.remove('hop');void m.offsetWidth;m.classList.add('hop');}};
function gPos(el){const a=$('#pg');if(!a||!el)return [0,0];const r=el.getBoundingClientRect(),q=a.getBoundingClientRect();return [r.left-q.left+r.width/2,r.top-q.top+r.height/2];}
function gStreak(){const e=$('#pgStreak');if(e&&game)e.textContent=game.combo>=3?'Streak '+game.combo:'';}
function gFloat(x,y,t){if(REDUCE)return;const a=$('#pg');if(!a)return;const e=document.createElement('span');e.className='ptx';e.setAttribute('aria-hidden','true');e.textContent=t;e.style.left=x+'px';e.style.top=y+'px';a.appendChild(e);setTimeout(()=>e.remove(),720);}
function gBurst(x,y,col){if(REDUCE)return;const a=$('#pg');if(!a)return;for(let i=0;i<7;i++){const e=document.createElement('i'),an=i/7*6.28+Math.random()*.5,d=16+Math.random()*16;e.className='pt';e.setAttribute('aria-hidden','true');e.style.cssText=`left:${Math.round(x)}px;top:${Math.round(y)}px;background:${col};--dx:${Math.round(Math.cos(an)*d)}px;--dy:${Math.round(Math.sin(an)*d)}px`;a.appendChild(e);setTimeout(()=>e.remove(),520);}}
function gMsg(t){const m=$('#pgMsg');if(m)m.textContent=t;}
function gHit(pts,x,y,col,tone){const g=game;g.combo++;clearTimeout(g.ct);g.ct=setTimeout(gBreak,2000);let add=pts;gFloat(x,y,'+'+pts);
  if(g.combo%5===0){add+=2;gFloat(x,y-22,'Streak! +2');gTone('gold');}else gTone(tone||'hit',Math.min(7,g.combo-1));
  gBurst(x,y,col);gScore(g.score+add);gStreak();}
function gMiss(cost,x,y){const g=game;g.combo=0;clearTimeout(g.ct);gStreak();if(cost){gScore(Math.max(0,g.score-cost));gFloat(x,y,'−'+cost);}sfx('no');}
function gBreak(){if(game&&game.combo){game.combo=0;gStreak();}}
function gClock(sec){let left=sec;game.timers.push(setInterval(()=>{if(!gOn())return;left--;const t=$('#pgTime');if(t)t.textContent=Math.max(0,left)+'s';if(left<=0)gEnd('Time!');},1000));}
function gEnd(txt){const g=game;if(!g||!g.alive||g.ending)return;g.ending=true;g.started=false;const a=$('#pg');
  if(a&&txt)a.insertAdjacentHTML('beforeend',`<div class="pgend" aria-hidden="true">${txt}</div>`);gTone('time');g.timers.push(setTimeout(finishGame,REDUCE?350:900));}
const PENTA=[523.25,587.33,659.25,783.99,880,1046.5,1174.66,1318.51];
const GT={hit:s=>[{f:PENTA[s],dur:.09,gain:.16,type:'triangle'}],
  gold:()=>[3,5,7].map((i,k)=>({f:PENTA[i],dur:.12,gain:.15,type:'triangle',delay:k*.05})),
  crackle:s=>[{f:200+s*30,f2:110,dur:.07,gain:.15}],
  plip:s=>[{f:PENTA[s],f2:PENTA[s]*1.5,dur:.11,gain:.15,type:'sine'}],
  lant:s=>[{f:[392,493.88,587.33,698.46][s&3],dur:.32,gain:.18,type:'triangle'}],
  log:()=>[{f:196,dur:.18,gain:.18,type:'triangle'},{f:294,dur:.22,gain:.16,type:'triangle',delay:.08}],
  wind:()=>[{f:340,f2:160,dur:.6,gain:.07,type:'sine'}],
  go:()=>[{f:523.25,dur:.08,gain:.15,type:'triangle'},{f:783.99,dur:.14,gain:.15,type:'triangle',delay:.09}],
  time:()=>[{f:659.25,dur:.12,gain:.15,type:'triangle'},{f:523.25,dur:.22,gain:.15,type:'triangle',delay:.12}]};
function gTone(k,s){if(!state||state.settings.sfx===false||!sOn()||!GT[k])return;try{s=s|0;playNotes(GT[k](s),'g'+k+s,.5);}catch(e){}}
/* ---- Dandelion Drift (Meadow): Spark brings golden seeds ---- */
function gMeadow(){
  const g=game,area=$('#pg'),gold=.06+.12*g.tr,t0=performance.now();let items=[],last=t0,nextPuff=t0+4000;
  const add=(kind,x,v,y0)=>{const b=document.createElement('button');b.type='button';b.className='seed'+(kind==='seed'?'':' '+kind);
    b.setAttribute('aria-label',{gold:'Golden seed',thorn:'Thorny burr',puff:'Dandelion puff'}[kind]||'Seed');b.style.left=x+'%';
    const o={el:b,kind,x,y:y0||0,v,ph:Math.random()*6.28};
    b.addEventListener('pointerdown',ev=>{ev.preventDefault();if(o.done||!gOn())return;o.done=1;const p=gPos(b);b.classList.add('caught');setTimeout(()=>b.remove(),160);
      if(kind==='thorn'){gMiss(2,p[0],p[1]);return;}
      if(kind==='puff'){gHit(1,p[0],p[1],'#FFFFFF');for(let i=0;i<5;i++)add('seed',Math.max(4,Math.min(82,o.x+(i-2)*9)),o.v*.7,Math.max(0,o.y-30+i*12));return;}
      gHit(kind==='gold'?3:1,p[0],p[1],kind==='gold'?'#FFD36B':'#F4F0E8');});
    area.appendChild(b);items.push(o);};
  const spawn=()=>{if(!gOn())return;const k=Math.min(1,(performance.now()-t0)/20000),H=area.clientHeight,r=Math.random();
    add(g.twist&&r<.2?'thorn':(r>1-gold?'gold':'seed'),4+Math.random()*78,(H+48)/((3.6-1.2*k)*(.9+Math.random()*.2)));
    g.timers.push(setTimeout(spawn,620-280*k));};
  const loop=now=>{if(!gOn())return;const dt=Math.min(.05,(now-last)/1000),H=area.clientHeight;last=now;
    if(g.gift&&now>nextPuff){nextPuff=now+6500;add('puff',10+Math.random()*60,(H+64)/5.5);}
    items=items.filter(o=>{if(o.done)return false;o.y+=o.v*dt;if(o.y>H+60){o.el.remove();return false;}
      o.el.style.transform=`translate(${Math.round(Math.sin(o.ph+o.y/60)*12)}px,${-Math.round(o.y)}px)`;return true;});
    g.raf=requestAnimationFrame(loop);};
  g.raf=requestAnimationFrame(loop);spawn();gClock(20);
}
/* ---- Keep the Fire (Ember): Grit slows the burn ---- */
function gEmber(){
  const g=game,area=$('#pg'),burn=1.1*(1-.3*g.tr),t0=performance.now();let heat=60,gust=0,nextLog=t0+5000,nextGust=t0+4500;
  area.insertAdjacentHTML('afterbegin','<div class="heat" aria-hidden="true"><i></i></div><div class="fire" aria-hidden="true"><i></i><b></b></div>');
  const draw=()=>{const f=area.querySelector('.fire i'),h=area.querySelector('.heat i');if(f)f.style.setProperty('--h',Math.max(8,heat)+'%');if(h)h.style.width=heat+'%';};draw();
  g.timers.push(setInterval(()=>{if(!gOn())return;const now=performance.now(),k=Math.min(1,(now-t0)/20000);
    if(g.twist&&now>nextGust){nextGust=now+5200+Math.random()*2000;gust=now+1800;area.classList.add('wind');gTone('wind');gMsg('A cold wind blows…');g.timers.push(setTimeout(()=>{area.classList.remove('wind');if(gOn())gMsg('');},1800));}
    heat=Math.max(0,heat-burn*(1+.6*k)*(now<gust?2:1));draw();if(heat<=0){gMsg('The fire went out.');gEnd(null);}},100));
  const spawn=()=>{if(!gOn())return;const now=performance.now(),k=Math.min(1,(now-t0)/20000),log=g.gift&&now>nextLog;if(log)nextLog=now+6500;
    const b=document.createElement('button');b.className='emb'+(log?' log':'');b.type='button';b.setAttribute('aria-label',log?'Log':'Ember');
    let x,y;do{x=6+Math.random()*80;y=14+Math.random()*70;}while(x>32&&x<62&&y>44);b.style.left=x+'%';b.style.top=y+'%';
    b.addEventListener('pointerdown',ev=>{ev.preventDefault();if(b._c||!gOn())return;b._c=1;heat=Math.min(100,heat+(log?35:13));draw();const p=gPos(b);b.classList.add('caught');setTimeout(()=>b.remove(),160);gHit(log?3:1,p[0],p[1],log?'#C98B4E':'#FF8A2E',log?'log':'crackle');});
    area.appendChild(b);g.timers.push(setTimeout(()=>{if(!b._c)b.remove();},(log?1900:1400-450*k)));
    g.timers.push(setTimeout(spawn,620-200*k));};
  spawn();gClock(20);
}
/* ---- Skipping Stones (Tide): Calm widens the calm water ---- */
function gTide(){
  const g=game,area=$('#pg'),base=.34+.08*g.tr,t0=performance.now();let zone=base,miss=0,speed=1.4,ph=0,last=t0,p=.5;
  area.insertAdjacentHTML('afterbegin','<div class="water" aria-hidden="true"><div class="calm" id="pgCalm"></div><div class="stone" id="pgStone"></div></div><p class="skips" id="pgSkips">Three misses and the stone sinks.</p>');
  const calm=$('#pgCalm'),stone=$('#pgStone'),ctr=()=>g.twist?.5+.16*Math.sin((performance.now()-t0)/1000*.9):.5;
  const place=()=>{const c=ctr();calm.style.left=((c-zone/2)*100)+'%';calm.style.width=(zone*100)+'%';};place();
  const loop=now=>{if(!gOn())return;const dt=Math.min(.05,(now-last)/1000);last=now;ph+=dt*speed*Math.PI*.5;p=(Math.sin(ph-Math.PI/2)+1)/2;stone.style.left=(p*100)+'%';if(g.twist)place();g.raf=requestAnimationFrame(loop);};
  g.raf=requestAnimationFrame(loop);
  game.skip=()=>{if(!gOn())return;const c=ctr(),d=Math.abs(p-c),hit=d<=zone/2,sk=$('#pgSkips');
    const r=document.createElement('div');r.className='ripple';r.style.left='calc(12px + '+(p*100)+'% - '+(p*24)+'px)';area.appendChild(r);setTimeout(()=>r.remove(),520);
    const x=12+p*(area.clientWidth-24);
    if(hit){g.combo++;gScore(g.score+1);gTone('plip',Math.min(7,g.score-1));gBurst(x,160,'#FFFFFF');gFloat(x,140,d<=zone*.15?'Perfect!':'+1');
      zone=Math.max(.14,zone-.025);speed=Math.min(3,speed+.12);
      if(g.gift&&g.score%5===0){zone=Math.min(base,zone+.09);gMsg('A lucky stone! The calm water widens.');}
      place();if(sk)sk.textContent=g.score===1?'One skip!':g.score+' skips!';}
    else{miss++;gMiss(0);if(sk)sk.textContent=miss>=3?'The stone sank.':(3-miss)+(3-miss===1?' miss left.':' misses left.');if(miss>=3)gEnd('Splash!');}};
  area.addEventListener('pointerdown',ev=>{if(ev.target.closest('button'))return;ev.preventDefault();game&&game.skip&&game.skip();});
  gClock(20);
}
/* ---- Snowflake Catch (Frost): Calm slows the snow ---- */
function gFrost(){
  const g=game,area=$('#pg'),slow=1-.22*g.tr,t0=performance.now();
  area.insertAdjacentHTML('afterbegin','<div class="basket" id="pgBasket" aria-hidden="true">'+mateHTML(g.c)+'</div>');
  const W=()=>area.clientWidth,bk=$('#pgBasket');let bx=.5,flakes=[],last=t0,nextBig=t0+4500;
  const setX=v=>{bx=Math.max(.08,Math.min(.92,v));bk.style.left=(bx*100)+'%';};setX(.5);
  const fromEv=ev=>{const r=area.getBoundingClientRect();setX((ev.clientX-r.left)/r.width);};
  let drag=false;area.addEventListener('pointerdown',ev=>{if(!gOn())return;ev.preventDefault();drag=true;try{area.setPointerCapture(ev.pointerId);}catch(e){}fromEv(ev);});
  area.addEventListener('pointermove',ev=>{if(gOn()&&(drag||ev.pointerType==='mouse'))fromEv(ev);});['pointerup','pointercancel','lostpointercapture'].forEach(t=>area.addEventListener(t,()=>{drag=false;}));
  game.nudge=d=>{if(gOn())setX(bx+d);};
  const spawn=()=>{if(!gOn())return;const now=performance.now(),k=Math.min(1,(now-t0)/20000),big=g.gift&&now>nextBig,hail=!big&&g.twist&&Math.random()<.2;if(big)nextBig=now+5500;
    const f=document.createElement('div');f.className='flake'+(big?' big':hail?' hail':'');f.setAttribute('aria-hidden','true');
    const o={el:f,kind:big?'big':hail?'hail':'flake',x:.06+Math.random()*.88,y:-30,v:(70+Math.random()*60)*slow*(1+.5*k)*(big?.8:1)};f.style.left=(o.x*100)+'%';f.style.top='-30px';area.appendChild(f);flakes.push(o);
    g.timers.push(setTimeout(spawn,520-220*k));};
  const loop=now=>{if(!gOn())return;const dt=Math.min(.05,(now-last)/1000);last=now;const H=area.clientHeight,bw=72/Math.max(1,W());
    flakes=flakes.filter(o=>{o.y+=o.v*dt;o.el.style.top=o.y+'px';
      if(o.y>H-84&&o.y<H-40&&Math.abs(o.x-bx)<bw/2+.03){const x=o.x*W(),y=o.y;o.el.remove();
        if(o.kind==='hail')gMiss(2,x,y);else gHit(o.kind==='big'?3:1,x,y,'#FFFFFF');return false;}
      if(o.y>H){o.el.remove();return false;}return true;});
    g.raf=requestAnimationFrame(loop);};
  g.raf=requestAnimationFrame(loop);spawn();gClock(20);
}
/* ---- Lantern Lights (Dusk): Spark makes each lantern glow longer ---- */
function gDusk(){
  const g=game,area=$('#pg'),cols=['#FFD36B','#F29BB5','#A6D8F2','#B5DDB5'],names=['Gold','Rose','Blue','Green'];
  area.insertAdjacentHTML('afterbegin',`<div class="lanterns">${cols.map((c,i)=>`<button class="lant" data-lant="${i}" style="--lc:${c}" aria-label="${names[i]} lantern" disabled></button>`).join('')}</div>`);
  const L=[...area.querySelectorAll('.lant')],seq=[],t=$('#pgTime'),show=Math.round(420*(1+.35*g.tr));let step=0,input=false,star=g.gift?1:0;
  const flash=(i,ms)=>{L[i].classList.add('on');gTone('lant',i);g.timers.push(setTimeout(()=>L[i].classList.remove('on'),ms));};
  const play=()=>{input=false;L.forEach(b=>b.disabled=true);step=0;gMsg('Watch.');if(t)t.textContent='Round '+seq.length;
    const gap=g.twist?Math.max(400,show+220-45*(seq.length-1)):show+220;
    seq.forEach((v,k)=>g.timers.push(setTimeout(()=>{if(gOn())flash(v,Math.min(show,gap-120));},600+k*gap)));
    g.timers.push(setTimeout(()=>{if(!gOn())return;input=true;L.forEach(b=>b.disabled=false);gMsg('Your turn.');L[0].focus({preventScroll:true});},600+seq.length*gap));};
  const round=()=>{if(!gOn())return;seq.push(Math.floor(Math.random()*4));play();};
  L.forEach((b,i)=>b.addEventListener('click',()=>{if(!input||!gOn())return;flash(i,220);
    if(i!==seq[step]){input=false;
      if(star){star=0;g.combo=0;gMsg('The evening star forgives you. Watch again.');g.timers.push(setTimeout(()=>{if(gOn())play();},1300));return;}
      gMsg('The lanterns flicker out.');sfx('no');gEnd(null);return;}
    step++;if(step===seq.length){gScore(seq.length);const p=gPos(area.querySelector('.lanterns'));gBurst(p[0],p[1],cols[i]);gFloat(p[0],p[1],seq.length+'!');
      if(seq.length>=12){gEnd('All twelve!');return;}input=false;g.timers.push(setTimeout(round,700));}}));
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
  const m=g.twist?.8:1,pts=score>=Math.ceil(G.hi*m)?3:score>=Math.ceil(G.mid*m)?2:1;
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
  if(b.id==='pgGo')gStart();
  else if(b.id==='pgSkip'&&game&&game.skip)game.skip();
  else if(b.id==='pgL'&&game&&game.nudge)game.nudge(-.12);
  else if(b.id==='pgR'&&game&&game.nudge)game.nudge(.12);
  else if(b.id==='pgAgain'){const c=cardById(+b.dataset.cid);closeModal();if(c)openPlay(c);}
  else if(b.id==='pgDone'){closeModal();renderHearth();}
});
document.addEventListener('keydown',e=>{if(!gOn())return;if(game.nudge&&(e.key==='ArrowLeft'||e.key==='ArrowRight')){e.preventDefault();game.nudge(e.key==='ArrowLeft'?-.08:.08);}else if(game.skip&&(e.key===' '||e.key==='Enter')&&document.activeElement&&document.activeElement.id!=='pgSit'){e.preventDefault();game.skip();}});
document.addEventListener('visibilitychange',()=>{if(!document.hidden||!game||!game.alive)return;if(game.started||game.ending)finishGame();else{if(pgT)pgT.stop();pgT=null;game=null;closeModal();}});
'''
src = src[:start] + GAMES_JS + src[end:]

# Sit together closes a not-yet-started game too (game is cleared there already); nothing else to change.

# Make room: the Nunito Sans 800 weight is bundled but nothing uses it (bold text uses 700).
import re as _re0
_m=_re0.findall(r"@font-face\{font-family:'Nunito Sans';font-style:normal;font-weight:800;[^}]*\}\n?",src)
assert len(_m)==1,len(_m)
src=src.replace(_m[0],'')

# ================= version and what's new =================
rep('<title>Forge (prototype 0.24.2)</title>', '<title>Forge (prototype 0.25.0)</title>')
rep("const VERSION='prototype 0.24.2';", "const VERSION='prototype 0.25.0';")
rep('const SEEN_V=28;', 'const SEEN_V=29;')
rep("""<ul class="newlist"><li><b>Share a Forgeling.</b>""",
    """<ul class="newlist"><li><b>Deeper games.</b> Your Forgeling now shapes its game. One of its stats is a trait, Close bond brings a gift, and dark Forgelings play their realm's twist. Every game has a Start card, sounds, sparkles, streaks and rounds that build up.</li>
    <li><b>Share a Forgeling.</b>""")
import re as _re
_i=src.index('<ul class="newlist">'); _j=src.index('</ul>',_i)
_items=_re.findall(r'\s*<li>.*?</li>',src[_i+len('<ul class="newlist">'):_j],_re.S)
src=src[:_i]+'<ul class="newlist">'+''.join(_items[:10])+src[_j:]
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src))

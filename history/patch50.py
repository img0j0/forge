# 0.50: the games and the Map, upgraded (Hunter picked all of it from the canvas, November 8).
# Games. Each game is played inside a small pixel scene of its realm (decor only, behind the play) and gets one new thing:
#   Dandelion Drift: swipe through seeds to gather several at once (3+ in one stroke earns a bonus), gusts bend the grass
#     before they push the seeds, and the dandelion clock loses its seeds as the round runs down.
#   Keep the Fire: the fire is the meter (Spark, Kindling, Campfire, Bonfire); embers fly up out of the fire and cool to
#     grey before they vanish; reaching a bonfire once is worth 3, and your Forgeling glows with the heat.
#   Skipping Stones: one stone, many skips. Five stones a round; tap as the stone touches the shimmer on the lake to keep
#     it skipping, ripples stay behind, and a stone that crosses the lake is worth 2 more.
#   Snowflake Catch: six kinds of flake fill a strip as you catch them (all six is worth 3), a one-of-a-kind flake may
#     fall once a round and is pressed into your journal, and hail shows a shadow on the snow first.
#   Lantern Lights: lanterns hang on a string over the rooftops, each finished round lets a sky lantern float up, the
#     first slip plays the tune once more slower, and at round 8 a fifth lantern joins.
#   Around them: the game sheet is a stack of postcards, your Forgeling hops, cheers a new best and yawns late at night,
#   and a round ends on a journal page (score written in, a line about your Forgeling, a red stamp for a new best).
# Map. Terrain is drawn (trees, smoking peaks, waves, pines and snowy peaks, lamp posts), clouds cover what you have
#   not found in a realm and thin with each place, the wanderer leaves footprints on its trail, the sea glints and
#   something surfaces now and then, and by lamplight stars come out over the sea, landmarks glint and Dusk's lamps glow.
import re,subprocess,os
S=open('base49.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
for cls in ('pgsc','pgink','fstage','ripr','flk0','hshad','lstr','skyl','pgzz','gres','gstamp','pcard','mp-ter','mp-cloud','mp-smoke','mp-glow','gsway'):
    assert not re.search(r'(?<![\w-])'+cls+r'(?![\w-])',S),cls
rep("const VERSION='prototype 0.49.0'","const VERSION='prototype 0.50.0'")
rep("<title>Forgelings (prototype 0.49.0)</title>","<title>Forgelings (prototype 0.50.0)</title>")
rep("const SEEN_V=54;","const SEEN_V=55;")
rep("games:{best:{},played:0,curioDay:''}","games:{best:{},played:0,curioDay:'',pressed:0}")
rep("s.games={best:ok,played:int(g.played,0,1e7,0),curioDay:typeof g.curioDay==='string'?g.curioDay:''};",
    "s.games={best:ok,played:int(g.played,0,1e7,0),curioDay:typeof g.curioDay==='string'?g.curioDay:'',pressed:int(g.pressed,0,1e6,0)};")

# ---------- game texts ----------
rep("{id:'meadow',t:'Dandelion Drift',h:'Tap the seeds before they float away. Golden seeds are worth 3.'",
    "{id:'meadow',t:'Dandelion Drift',h:'Tap the seeds, or swipe through several at once, before they float away. Golden seeds are worth 3.'")
rep("{id:'ember',t:'Keep the Fire',h:'Tap the embers to feed the fire. Keep it burning.'",
    "{id:'ember',t:'Keep the Fire',h:'Tap the embers as they fly up to feed the fire. Build it to a bonfire.'")
rep("""{id:'tide',t:'Skipping Stones',h:'Tap Skip, or anywhere on the water, when the stone is over the calm water.',hi:9,mid:5,u:['skip','skips'],si:2,
  trait:'the calm water is wider',gift:'every fifth skip, a lucky stone widens the calm water again.',twist:'the calm water drifts from side to side.'}""",
"""{id:'tide',t:'Skipping Stones',h:'Five stones. Tap Skip, or the water, as the stone touches the shimmer, and it skips again.',hi:18,mid:10,u:['skip','skips'],si:2,
  trait:'the shimmer on the water is wider',gift:'every fifth skip, a lucky stone widens the shimmer again.',twist:'the shimmer drifts from side to side.'}""")
rep("{id:'frost',t:'Snowflake Catch',h:'Drag to move. Catch the snowflakes as they fall.'",
    "{id:'frost',t:'Snowflake Catch',h:'Drag to move. Catch all six kinds of snowflake as they fall.'")
rep("{id:'dusk',t:'Lantern Lights',h:'Watch the lanterns, then light them in the same order.'",
    "{id:'dusk',t:'Lantern Lights',h:'Watch the lanterns, then light them in the same order. Slip once and they play again, slower.'")
rep("lant:s=>[{f:[392,493.88,587.33,698.46][s&3],dur:.32,gain:.18,type:'triangle'}],",
    "lant:s=>[{f:[392,493.88,587.33,698.46,783.99][s%5],dur:.32,gain:.18,type:'triangle'}],")

# ---------- scene, postcards, companion ----------
rep("""<div class="pg pg-${G.id}" id="pg" aria-label="${G.t} play area">""","""<div class="pg pg-${G.id}" id="pg" role="group" aria-label="${G.t} play area">${gScene(G.id)}""")
rep("game={c,G,free,score:0,combo:0,alive:true,started:false,timers:[],raf:0,tr:gTrait(c,G),gift,twist};",
    "game={c,G,free,score:0,combo:0,alive:true,started:false,timers:[],raf:0,tr:gTrait(c,G),gift,twist,best0:best};")
rep("""      return `<button class="moodbtn" data-game="${ti}" data-cid="${c.id}">${iconSVG(GAMEI[ti])}<div><b>${G.t}${ti===home?'<span class="home">Home</span>':''}</b><span>${esc(n)} plays${best?`. Best: ${unitOf(G,best)}`:''}</span></div></button>`;}).join('')}""",
"""      const pr=G.id==='frost'&&state.games.pressed?` · ${state.games.pressed} pressed`:'';
      return `<button class="moodbtn pcard" data-game="${ti}" data-cid="${c.id}" style="--r:${[-1,.8,-.5,1,-.8][ti]}deg">${gScene(G.id,true)}<div><b>${G.t}${ti===home?'<span class="home">Home</span>':''}</b><span>${esc(n)} plays${best?`. Best: ${unitOf(G,best)}`:''}${pr}</span></div></button>`;}).join('')}""")
rep("""  const g=game;if(!g||!g.alive||g.started||g.ending)return;const r=$('#pgReady');if(r)r.remove();g.started=true;gTone('go');""",
"""  const g=game;if(!g||!g.alive||g.started||g.ending)return;const r=$('#pgReady');if(r)r.remove();g.started=true;gTone('go');
  {const h=new Date().getHours(),m=document.querySelector('#pg .pgmate'),a=$('#pg');if((h>=21||h<5)&&m&&a){const p=gPos(m),z=document.createElement('span');z.className='pgzz';z.setAttribute('aria-hidden','true');z.textContent='z z';z.style.left=Math.round(p[0]+22)+'px';z.style.top=Math.round(p[1]-56)+'px';a.appendChild(z);g.timers.push(setTimeout(()=>z.remove(),2700));}}""")
rep("""const gScore=v=>{game.score=v;const s=$('#pgScore');if(s)s.textContent=v;const m=document.querySelector('#pg .pgmate');if(m){m.classList.remove('hop');void m.offsetWidth;m.classList.add('hop');}};""",
"""const gScore=v=>{game.score=v;const s=$('#pgScore');if(s)s.textContent=v;const m=document.querySelector('#pg .pgmate');if(m){m.classList.remove('hop');void m.offsetWidth;m.classList.add('hop');}
  const g=game;if(g.best0>0&&!g.nbs&&v>g.best0){g.nbs=1;if(m){m.classList.add('cheer');g.timers.push(setTimeout(()=>m.classList.remove('cheer'),900));}const p=m?gPos(m):[80,200];gFloat(p[0],p[1]-60,'New best!');}};""")
rep("""function gClock(sec){let left=sec;game.timers.push(setInterval(()=>{if(!gOn())return;left--;const t=$('#pgTime');if(t)t.textContent=Math.max(0,left)+'s';if(left<=0)gEnd('Time!');},1000));}""",
"""function gClock(sec){let left=sec;game.timers.push(setInterval(()=>{if(!gOn())return;left--;const t=$('#pgTime');if(t)t.textContent=Math.max(0,left)+'s';if(game.tick)game.tick(left,sec);if(left<=0)gEnd('Time!');},1000));}""")

SCENES=r"""
/* ---- 0.50: little worlds. Each game is played inside a small pixel scene of its realm, drawn behind the play
   (decor only). gScene(id,true) is the same scene cropped for its postcard on the game sheet. ---- */
function gR(x,y,w,h,c,a){return `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${c}"${a!=null?` opacity="${a}"`:''}/>`;}
function gpx(rows,x,y,s,c){let o='';rows.forEach((r,j)=>{let i=0;while(i<r.length){if(r[i]!=='#'){i++;continue;}let k=i;while(k<r.length&&r[k]==='#')k++;o+=gR(r1(x+i*s),r1(y+j*s),r1((k-i)*s),s,c);i=k;}});return o;}
function gStars(n,seed,h,c){let o='';for(let i=0;i<n;i++){const a=whash(seed*977+i*31);o+=gR(a%160,(a>>>8)%h,1,1,c,[.5,.8,1][i%3]);}return o;}
const GNIGHT=()=>{const h=new Date().getHours();return h>=19||h<6;};
const LANTP=['.###.','#####','#####','#####','.###.'];
function gScene(id,mini){
  const nt=GNIGHT();let s='',vb='0 0 160 170';
  if(id==='meadow'){
    s+=nt?gR(0,0,160,170,'#1B2C4A')+gStars(26,3,80,'#E9DCC0')+gpx(['.##','###','.##'],128,14,2,'#FFF3C4'):gR(0,0,160,170,'#9FD3EC')+gR(0,50,160,40,'#B7E0F0')+gpx(['.###.','#####','#####','.###.'],124,12,3,'#FFF3C4')+gpx(['..####....','.########.','##########'],14,22,2,'#FFFFFF')+gpx(['..###...','########'],80,38,2,'#FFFFFF');
    s+=`<path d="M0 104Q40 86 80 98T160 92V170H0Z" fill="${nt?'#2F5A3A':'#86C072'}"/><path d="M0 126Q50 112 100 122T160 118V170H0Z" fill="${nt?'#24482E':'#5E9E55'}"/>`;
    const fc=nt?'#4A3A2A':'#8B6A44';for(let x=22;x<112;x+=15)s+=gR(x,108,2,12,fc);s+=gR(20,111,94,2,fc)+gR(20,116,94,2,fc);
    s+='<g class="gsway">'+[[10,140],[42,152],[70,136],[98,154],[118,142]].map(([x,y])=>gpx(['#.#.#','#####'],x,y,2,nt?'#3E6E46':'#3E8A4A')).join('')+'</g>';
    s+=gR(141,96,2,60,nt?'#3E6E46':'#3E7A3E');let c='';for(let i=0;i<12;i++){const a=i/12*6.283;c+=gR(r1(141+Math.cos(a)*8),r1(91+Math.sin(a)*8),2,2,'#FFFFFF');}
    s+=`<g${mini?'':' id="pgClock"'}>${c}</g>`+gR(140,90,4,4,'#D9C69C');
    if(mini)vb='100 70 60 60';
  }else if(id==='ember'){
    s+=gR(0,0,160,170,'#1E0F18')+gStars(30,5,110,'#E9C77A')+'<path d="M0 128L20 116L38 124L60 108L84 122L104 112L126 124L146 114L160 120V128H0Z" fill="#2A1620"/>'+gR(0,128,160,42,'#2B1B16')+gR(0,128,160,2,'#3A261C');
    s+='<ellipse cx="80" cy="150" rx="46" ry="14" fill="#FF8A2E" opacity=".16"/>';
    [52,60,68,76,84,92,100].forEach((x,i)=>{s+=gR(x,150+(i%2),7,5,i%2?'#6B5A4A':'#7E6B58')+gR(x,150+(i%2),7,1,'#9A8670');});
    if(mini){s+=gpx(['...#....','..##..#.','..###.##','.#######','########','.######.'],66,124,2.5,'#FF8A2E')+gpx(['..#..','.###.','.###.'],73.5,134,2.5,'#FFD36B')+gR(64,148,32,4,'#6B4A2A');vb='48 100 64 64';}
  }else if(id==='tide'){
    s+=nt?gR(0,0,160,88,'#18284A')+gStars(20,7,60,'#E9DCC0')+gpx(['.##','###','.##'],120,14,2,'#FFF3C4'):gR(0,0,160,88,'#BFE3F2')+gR(0,60,160,28,'#D5ECF5')+gpx(['####','####','####','####'],118,16,3,'#FFF3C4');
    s+=`<path d="M0 88L18 78L40 84L66 74L92 84L120 76L142 82L160 78V88H0Z" fill="${nt?'#22365A':'#7FA8C4'}"/>`+gR(0,88,160,44,nt?'#24476E':'#3F7FB0')+gR(0,88,160,2,nt?'#1B3556':'#2F5E8C');
    [[94,6],[100,40],[108,18],[116,60],[124,30]].forEach(([y,o],i)=>{for(let x=o%40;x<160;x+=44+i*3)s+=gR(x,y,10+i%3*4,1,'#A6D8F2',.55);});
    s+=gR(0,132,160,38,nt?'#8C7A55':'#E9C98A')+gR(0,131,160,2,'#FFFFFF',.6);
    if(mini){s+=`<ellipse cx="62" cy="103" rx="7" ry="2" fill="none" stroke="#FFFFFF" stroke-width="1"/><ellipse cx="80" cy="100" rx="5" ry="1.5" fill="none" stroke="#FFFFFF" stroke-width="1" opacity=".8"/>`+gR(90,93,6,3,'#9AA0A8')+gR(91,92,4,1,'#C3C8CE');vb='40 70 64 64';}
  }else if(id==='frost'){
    s+=gR(0,0,160,170,'#22325A')+gStars(30,9,100,'#FFFFFF')+gpx(['.##','###','.##'],126,12,2,'#FFF3C4');
    [[6,30],[24,44],[44,26],[118,40],[140,30],[156,22]].forEach(([x,h])=>{s+=`<path d="M${x} ${136-h}L${x+10} 136H${x-10}Z" fill="#1E3A3A"/><path d="M${x} ${136-h-8}L${x+7} ${136-h+10}H${x-7}Z" fill="#244646"/>`;});
    s+=gR(0,136,160,34,'#E8F1F8')+'<path d="M0 136Q40 130 80 136T160 134V140H0Z" fill="#FFFFFF"/>';
    if(mini){s+=gpx(['..#..','#.#.#','.###.','#####','.###.','#.#.#','..#..'],86,92,2.5,'#FFFFFF')+gpx(['#...#','.#.#.','..#..','.#.#.','#...#'],104,112,2,'#DDEBFF');vb='60 76 64 64';}
  }else{
    s+=gR(0,0,160,170,'#3D2E5C')+gR(0,0,160,70,'#2A2048')+gStars(24,11,70,'#FFD36B');
    s+='<path d="M0 132V112H14V102L24 94L34 102V112H50V104L60 96L70 104V118H86V100L98 90L110 100V112H124V106L134 98L144 106V112H160V132Z" fill="#1E1638"/>';
    [[18,104],[26,104],[62,108],[94,102],[102,102],[136,108]].forEach(([x,y])=>{s+=gR(x,y,3,3,'#FFD36B',.85);});
    s+=gR(0,132,160,38,'#1B1633');
    if(mini){s+='<path d="M40 30Q80 70 120 30" fill="none" stroke="#8B7AB8" stroke-width="1"/>'+[[52,'#FFD36B'],[70,'#F29BB5'],[88,'#A6D8F2'],[104,'#B5DDB5']].map(([x,c],i)=>gpx(LANTP,x-5,30+[10,18,18,12][i],2,c)).join('');vb='40 26 80 80';}
  }
  return mini?`<svg class="rowsig pcs" viewBox="${vb}" width="56" height="56" aria-hidden="true" shape-rendering="crispEdges" preserveAspectRatio="xMidYMid slice">${s}</svg>`
    :`<svg class="pgsc" viewBox="${vb}" preserveAspectRatio="xMidYMax slice" aria-hidden="true" shape-rendering="crispEdges">${s}</svg>`;
}
/* a round ends on a journal page */
const GFLAV={meadow:['{n} chased a golden seed all the way to the fence.','{n} sneezed at a seed and laughed about it.','{n} watched the last seeds drift over the hill.'],
  ember:['{n} warmed its paws by the fire.','{n} counted the sparks going up.','{n} stayed close to the glow until the end.'],
  tide:['{n} cheered every ripple.','{n} found a flat stone for next time.','{n} watched the rings spread across the lake.'],
  frost:['{n} caught one on its nose.','{n} slid home on the sled.','{n} shook off the snow and wanted to go again.'],
  dusk:['{n} hummed the lantern tune afterwards.','{n} watched the sky lanterns drift away.','{n} said goodnight to every lantern.']};
const GFLAVD=['{n} watched the whole round, quietly pleased.','{n} rumbled, low and content.','{n} said nothing, but stayed until the very end.'];
let gBondLater=null;
function gResult(g,score,nb,best,extra,free){
  const G=g.G,n=g.c.nick||g.c.name,L=g.c.dark?GFLAVD:GFLAV[G.id],fl=L[Math.floor(Math.random()*L.length)].replace('{n}',n),again=free||!gBondLater;
  openOverlay(`<div class="gres"><p class="gd">Day ${dayN()} · By the fire</p><h2>Played ${G.t} with ${esc(n)}</h2><p class="gs">${score} <span>${G.u[score===1?0:1]}</span></p>
    <p class="gl">${esc(fl)}${nb?' A new best!':best?` Best: ${unitOf(G,best)}.`:''}</p>${extra.map(x=>`<p class="gx">${esc(x)}</p>`).join('')}${free?'<p class="gx">Just for fun: no visit used.</p>':''}
    ${nb?'<div class="gstamp" aria-hidden="true"><b>BEST</b><span>NEW</span></div>':''}</div>
    <div class="pgbtnrow">${again?`<button class="primary" id="pgAgain" data-cid="${g.c.id}" data-gi="${GAMES.indexOf(G)}">Play again</button>`:''}<button class="${again?'ghost':'primary'}" id="pgDone">Back to the fire</button></div>`,false);
  const f=$('#pgAgain')||$('#pgDone');if(f)f.focus({preventScroll:true});
}
"""
rep("/* ---- Dandelion Drift (Meadow): Spark brings golden seeds ---- */",SCENES+"/* ---- Dandelion Drift (Meadow): Spark brings golden seeds ---- */")

# ---------- Dandelion Drift ----------
i0=S.index("function gMeadow(){"); i1=S.index("/* ---- Keep the Fire (Ember)")
S=S[:i0]+r"""function gMeadow(){
  const g=game,area=$('#pg'),gold=.06+.12*g.tr,t0=performance.now(),nt=GNIGHT();let items=[],last=t0,nextPuff=t0+4000,nextGust=t0+3800,gust=0,gdir=1,stroke=null;
  area.insertAdjacentHTML('beforeend',`<svg class="pgink" aria-hidden="true"><polyline points="" style="stroke:${nt?'#FFF3C4':'#2E2A47'}"/></svg>`);
  const ink=area.querySelector('.pgink'),pl=ink.querySelector('polyline');
  const catchIt=o=>{if(o.done||!gOn())return;o.done=1;const b=o.el,p=gPos(b);b.classList.add('caught');setTimeout(()=>b.remove(),160);
    if(o.kind==='thorn'){gMiss(2,p[0],p[1]);return;}
    if(stroke)stroke.n++;
    if(o.kind==='puff'){gHit(1,p[0],p[1],'#FFFFFF');for(let i=0;i<5;i++)add('seed',Math.max(4,Math.min(82,o.x+(i-2)*9)),o.v*.7,Math.max(0,o.y-30+i*12));return;}
    gHit(o.kind==='gold'?3:1,p[0],p[1],o.kind==='gold'?'#FFD36B':'#F4F0E8');};
  const add=(kind,x,v,y0)=>{const b=document.createElement('button');b.type='button';b.className='seed'+(kind==='seed'?'':' '+kind);
    b.setAttribute('aria-label',{gold:'Golden seed',thorn:'Thorny burr',puff:'Dandelion puff'}[kind]||'Seed');b.style.left=x+'%';
    const o={el:b,kind,x,y:y0||0,v,ph:Math.random()*6.28,dx:0};
    b.addEventListener('pointerdown',ev=>{ev.preventDefault();catchIt(o);});
    area.appendChild(b);items.push(o);};
  /* a swipe: every seed the finger passes over is caught, and three or more in one stroke earn a bonus */
  const pt=ev=>{const r=area.getBoundingClientRect();return [ev.clientX-r.left,ev.clientY-r.top];};
  area.addEventListener('pointerdown',ev=>{if(!gOn())return;stroke={n:0,pts:[pt(ev)],id:ev.pointerId};try{area.setPointerCapture(ev.pointerId);}catch(e){}ink.classList.remove('fade');pl.setAttribute('points','');},true);
  area.addEventListener('pointermove',ev=>{if(!stroke||ev.pointerId!==stroke.id||!gOn())return;const q=pt(ev),a=stroke.pts[stroke.pts.length-1];if(Math.hypot(q[0]-a[0],q[1]-a[1])<6)return;
    stroke.pts.push(q);if(stroke.pts.length>40)stroke.pts.shift();pl.setAttribute('points',stroke.pts.map(p=>Math.round(p[0])+','+Math.round(p[1])).join(' '));
    const R=area.getBoundingClientRect();items.forEach(o=>{if(o.done)return;const r=o.el.getBoundingClientRect(),cx=r.left-R.left+r.width/2,cy=r.top-R.top+20;if(segD(cx,cy,a,q)<26)catchIt(o);});});
  const endS=()=>{if(!stroke)return;const s=stroke;stroke=null;ink.classList.add('fade');
    if(s.n>=3&&gOn()){const b=s.n-2,q=s.pts[s.pts.length-1];gScore(game.score+b);gFloat(q[0],q[1]-26,`Swept ${s.n}! +${b}`);gTone('gold');}};
  ['pointerup','pointercancel','lostpointercapture'].forEach(t=>area.addEventListener(t,endS));
  /* the dandelion clock loses its seeds as the round runs down */
  g.tick=(left,sec)=>{const d=area.querySelectorAll('#pgClock rect'),want=Math.ceil(Math.max(0,left)/sec*d.length);for(let i=d.length-1;i>=want&&i>=0;i--)d[i].remove();};
  const spawn=()=>{if(!gOn())return;const k=Math.min(1,(performance.now()-t0)/20000),H=area.clientHeight,r=Math.random();
    add(g.twist&&r<.2?'thorn':(r>1-gold?'gold':'seed'),4+Math.random()*78,(H+48)/((3.6-1.2*k)*(.9+Math.random()*.2)));
    g.timers.push(setTimeout(spawn,620-280*k));};
  const loop=now=>{if(!gOn())return;const dt=Math.min(.05,(now-last)/1000),H=area.clientHeight,W=area.clientWidth;last=now;
    if(g.gift&&now>nextPuff){nextPuff=now+6500;add('puff',10+Math.random()*60,(H+64)/5.5);}
    /* a gust bends the grass first, then pushes the seeds sideways for a moment */
    if(now>nextGust){nextGust=now+5200+Math.random()*2200;gdir=Math.random()<.5?-1:1;area.style.setProperty('--gd',gdir);area.classList.add('gust');
      g.timers.push(setTimeout(()=>{gust=performance.now()+1400;},600));g.timers.push(setTimeout(()=>area.classList.remove('gust'),2200));}
    items=items.filter(o=>{if(o.done)return false;o.y+=o.v*dt;if(o.y>H+60){o.el.remove();return false;}
      if(now<gust){const bx=o.x/100*W;o.dx=Math.max(14-bx,Math.min(W-62-bx,o.dx+gdir*38*dt));}
      o.el.style.transform=`translate(${Math.round(Math.sin(o.ph+o.y/60)*12+o.dx)}px,${-Math.round(o.y)}px)`;return true;});
    g.raf=requestAnimationFrame(loop);};
  g.raf=requestAnimationFrame(loop);spawn();gClock(20);
}
"""+S[i1:]

# ---------- Keep the Fire ----------
i0=S.index("function gEmber(){"); i1=S.index("/* ---- Skipping Stones (Tide)")
S=S[:i0]+r"""function gEmber(){
  const g=game,area=$('#pg'),burn=1.1*(1-.3*g.tr),t0=performance.now();let heat=60,gust=0,nextLog=t0+5000,nextGust=t0+4500,stage=-1,bon=false;
  area.insertAdjacentHTML('afterbegin','<div class="heat" aria-hidden="true"><i></i></div><div class="fstage" aria-hidden="true"><span>Spark</span><span>Kindling</span><span>Campfire</span><span>Bonfire</span></div><div class="fire" aria-hidden="true"><i></i><b></b></div>');
  const ST=area.querySelectorAll('.fstage span');
  /* the fire is the meter: Spark, Kindling, Campfire, Bonfire. Reaching a bonfire once is worth 3. */
  const draw=()=>{const f=area.querySelector('.fire i'),h=area.querySelector('.heat i');if(f)f.style.setProperty('--h',Math.max(8,heat)+'%');if(h)h.style.width=heat+'%';area.style.setProperty('--heat',Math.round(heat));
    const s=heat>=85?3:heat>=55?2:heat>=25?1:0;if(s!==stage){stage=s;ST.forEach((e,i)=>e.classList.toggle('on',i===s));}
    if(s===3&&!bon&&gOn()){bon=true;const p=gPos(area.querySelector('.fire'));gScore(game.score+3);gFloat(p[0],p[1]-60,'Bonfire! +3');gTone('gold');gBurst(p[0],p[1]-40,'#FFD36B');gMsg('A bonfire!');g.timers.push(setTimeout(()=>{if(gOn()&&$('#pgMsg').textContent==='A bonfire!')gMsg('');},1600));}};draw();
  g.timers.push(setInterval(()=>{if(!gOn())return;const now=performance.now(),k=Math.min(1,(now-t0)/20000);
    if(g.twist&&now>nextGust){nextGust=now+5200+Math.random()*2000;gust=now+1800;area.classList.add('wind');gTone('wind');gMsg('A cold wind blows…');g.timers.push(setTimeout(()=>{area.classList.remove('wind');if(gOn())gMsg('');},1800));}
    heat=Math.max(0,heat-burn*(1+.6*k)*(now<gust?2:1));draw();if(heat<=0){gMsg('The fire went out.');gEnd(null);}},100));
  /* embers fly up out of the fire to where you can catch them, and cool to grey before they vanish */
  const spawn=()=>{if(!gOn())return;const now=performance.now(),k=Math.min(1,(now-t0)/20000),log=g.gift&&now>nextLog;if(log)nextLog=now+6500;
    const b=document.createElement('button');b.className='emb'+(log?' log':'');b.type='button';b.setAttribute('aria-label',log?'Log':'Ember');
    let x,y;do{x=6+Math.random()*80;y=14+Math.random()*70;}while(x>32&&x<62&&y>44);b.style.left=x+'%';b.style.top=y+'%';
    b.addEventListener('pointerdown',ev=>{ev.preventDefault();if(b._c||!gOn())return;b._c=1;heat=Math.min(100,heat+(log?35:13));draw();const p=gPos(b);b.classList.add('caught');setTimeout(()=>b.remove(),160);gHit(log?3:1,p[0],p[1],log?'#C98B4E':'#FF8A2E',log?'log':'crackle');});
    if(!log&&!REDUCE){const W=area.clientWidth,H=area.clientHeight,dx=W/2-24-x/100*W,dy=H-40-Math.max(8,heat)*.8-24-y/100*H;b.classList.add('rise');b.style.transform=`translate(${Math.round(dx)}px,${Math.round(dy)}px) scale(.4)`;
      requestAnimationFrame(()=>requestAnimationFrame(()=>{b.style.transition='transform .45s cubic-bezier(.2,.8,.3,1)';b.style.transform='';}));}
    area.appendChild(b);const life=log?1900:1400-450*k;g.timers.push(setTimeout(()=>b.classList.add('cool'),life*.62));g.timers.push(setTimeout(()=>{if(!b._c)b.remove();},life));
    g.timers.push(setTimeout(spawn,620-200*k));};
  spawn();gClock(20);
}
/* ---- Skipping Stones (Tide), 0.50: one stone, many skips. Five stones a round. Each hop lands in a shimmer on the
   lake; tap while the stone is in the shimmer and it skips again (each skip shorter and quicker), miss it and the stone
   sinks. A stone that crosses the lake is worth 2 more. Calm widens the shimmer; the Abyss twist makes it drift. ---- */
function gTide(){
  const g=game,area=$('#pg'),base=.34+.08*g.tr,t0=performance.now();let zone=base,stones=0,st=null,total=0;
  area.insertAdjacentHTML('afterbegin','<div class="calm" id="pgCalm" aria-hidden="true"></div><div class="stone" id="pgStone" aria-hidden="true"></div><p class="skips" id="pgSkips">Stone 1 of 5</p>');
  const calm=$('#pgCalm'),stone=$('#pgStone'),sk=$('#pgSkips'),W=()=>area.clientWidth,Yw=()=>Math.round(area.clientHeight*.6);
  const hwOf=s=>Math.max(8,zone*(s.len*.55+20)),off=()=>g.twist?Math.sin((performance.now()-t0)/1000*1.3)*22:0;
  const place=()=>{if(!st){calm.style.opacity='0';return;}const hw=hwOf(st),c=st.L+off();calm.style.opacity='';calm.style.left=Math.round(c-hw)+'px';calm.style.width=Math.round(hw*2)+'px';calm.style.top=(Yw()-5)+'px';};
  const ripple=(x,big)=>{const r=document.createElement('i');r.className='ripr'+(big?' big':'');r.setAttribute('aria-hidden','true');r.style.left=Math.round(x)+'px';r.style.top=Yw()+'px';area.appendChild(r);setTimeout(()=>r.remove(),2500);};
  const say=t=>{if(sk)sk.textContent=t;};
  const throwStone=()=>{if(!gOn())return;if(stones>=5){gEnd('Five stones!');return;}stones++;say('Stone '+stones+' of 5');
    st={x0:58,y0:Yw()+52,L:110,len:52,t:performance.now(),dur:1000,hgt:46,skips:0,x:58};stone.style.opacity='1';place();};
  const next=()=>{st=null;stone.style.opacity='0';place();g.timers.push(setTimeout(throwStone,900));};
  const sink=why=>{if(!st)return;ripple(st.x,false);gMiss(0);say(why+(stones>=5?' That was the last stone.':` ${5-stones} ${5-stones===1?'stone':'stones'} left.`));next();};
  const loop=now=>{if(!gOn())return;
    if(st){const f=(now-st.t)/st.dur;let x,y;
      if(f<=1){x=st.x0+(st.L-st.x0)*f;y=st.y0+(Yw()-st.y0)*f-4*st.hgt*f*(1-f);}else{x=st.L+(st.L-st.x0)*(f-1);y=Yw();}
      st.x=x;stone.style.left=Math.round(x)+'px';stone.style.top=Math.round(y)+'px';if(g.twist)place();
      if(f>1&&x>st.L+off()+hwOf(st)+2)sink('It sank.');}
    g.raf=requestAnimationFrame(loop);};
  g.raf=requestAnimationFrame(loop);
  game.skip=()=>{if(!gOn()||!st)return;const x=st.x,c=st.L+off(),hw=hwOf(st);
    if(Math.abs(x-c)>hw){sink(x<c?'Too soon. It sank.':'It sank.');return;}
    g.combo++;st.skips++;total++;gScore(g.score+1);gTone('plip',Math.min(7,st.skips-1));ripple(x,true);gBurst(x,Yw()-6,'#FFFFFF');gFloat(x,Yw()-26,Math.abs(x-c)<=hw*.3?'Perfect!':'+1');
    zone=Math.max(.2,zone-.01);
    if(g.gift&&total%5===0){zone=Math.min(base+.09,zone+.09);gMsg('A lucky stone! The calm water widens.');}
    const len=Math.max(22,st.len*.88),nL=x+len;
    if(nL>W()-10){gScore(game.score+2);gFloat(x,Yw()-48,'Across the lake! +2');gTone('gold');say('Across the lake!');next();return;}
    st={x0:x,y0:Yw(),L:nL,len,t:performance.now(),dur:Math.max(360,st.dur*.9),hgt:st.hgt*.8,skips:st.skips,x};place();say(st.skips===1?'One skip!':st.skips+' skips!');};
  area.addEventListener('pointerdown',ev=>{if(ev.target.closest('button'))return;ev.preventDefault();game&&game.skip&&game.skip();});
  throwStone();gClock(20);
}
"""+S[S.index("/* ---- Snowflake Catch (Frost)"):]

# ---------- Snowflake Catch ----------
i0=S.index("function gFrost(){"); i1=S.index("/* ---- Lantern Lights (Dusk)")
S=S[:i0]+r"""function gFrost(){
  const g=game,area=$('#pg'),slow=1-.22*g.tr,t0=performance.now();
  area.insertAdjacentHTML('afterbegin','<div class="basket" id="pgBasket" aria-hidden="true">'+mateHTML(g.c)+'</div><div class="fcol" aria-hidden="true">'+[0,1,2,3,4,5].map(i=>`<i class="flk${i}"></i>`).join('')+'</div>');
  const W=()=>area.clientWidth,bk=$('#pgBasket'),fc=area.querySelectorAll('.fcol i'),got=new Set();let bx=.5,flakes=[],last=t0,nextBig=t0+4500,rareAt=Math.random()<.45?t0+4000+Math.random()*9000:0;
  const setX=v=>{bx=Math.max(.08,Math.min(.92,v));bk.style.left=(bx*100)+'%';};setX(.5);
  const fromEv=ev=>{const r=area.getBoundingClientRect();setX((ev.clientX-r.left)/r.width);};
  let drag=false;area.addEventListener('pointerdown',ev=>{if(!gOn())return;ev.preventDefault();drag=true;try{area.setPointerCapture(ev.pointerId);}catch(e){}fromEv(ev);});
  area.addEventListener('pointermove',ev=>{if(gOn()&&(drag||ev.pointerType==='mouse'))fromEv(ev);});['pointerup','pointercancel','lostpointercapture'].forEach(t=>area.addEventListener(t,()=>{drag=false;}));
  game.nudge=d=>{if(gOn())setX(bx+d);};
  const spawn=()=>{if(!gOn())return;const now=performance.now(),k=Math.min(1,(now-t0)/20000),rare=!!rareAt&&now>rareAt,big=!rare&&g.gift&&now>nextBig,hail=!rare&&!big&&g.twist&&Math.random()<.2;if(rare)rareAt=0;if(big)nextBig=now+5500;
    const kk=Math.floor(Math.random()*6)%6,f=document.createElement('div');f.className='flake'+(rare?' rare':hail?' hail':' flk'+kk+(big?' big':''));f.setAttribute('aria-hidden','true');
    const o={el:f,kind:rare?'rare':big?'big':hail?'hail':'flake',k:kk,x:.06+Math.random()*.88,y:-30,v:(70+Math.random()*60)*slow*(1+.5*k)*(big?.8:rare?.7:1)};f.style.left=(o.x*100)+'%';f.style.top='-30px';area.appendChild(f);
    if(hail){const sh=document.createElement('i');sh.className='hshad';sh.setAttribute('aria-hidden','true');sh.style.left=(o.x*100)+'%';area.appendChild(sh);o.sh=sh;}
    flakes.push(o);g.timers.push(setTimeout(spawn,520-220*k));};
  const loop=now=>{if(!gOn())return;const dt=Math.min(.05,(now-last)/1000);last=now;const H=area.clientHeight,bw=72/Math.max(1,W());
    flakes=flakes.filter(o=>{o.y+=o.v*dt;o.el.style.top=o.y+'px';if(o.sh)o.sh.style.opacity=Math.min(.55,Math.max(0,o.y/H)).toFixed(2);
      if(o.y>H-84&&o.y<H-40&&Math.abs(o.x-bx)<bw/2+.03){const x=o.x*W(),y=o.y;o.el.remove();if(o.sh)o.sh.remove();
        if(o.kind==='hail')gMiss(2,x,y);
        else if(o.kind==='rare'){gHit(5,x,y,'#FFD36B');g.pressed=1;state.games.pressed=(state.games.pressed|0)+1;save();gMsg('One of a kind! It will be pressed into your journal.');g.timers.push(setTimeout(()=>{if(gOn())gMsg('');},2400));}
        else{gHit(o.kind==='big'?3:1,x,y,'#FFFFFF');if(!got.has(o.k)){got.add(o.k);fc[o.k].classList.add('got');if(got.size===6){gScore(game.score+3);gFloat(x,y-30,'All six kinds! +3');gTone('gold');}}}
        return false;}
      if(o.y>H){o.el.remove();if(o.sh)o.sh.remove();return false;}return true;});
    g.raf=requestAnimationFrame(loop);};
  g.raf=requestAnimationFrame(loop);spawn();gClock(20);
}
"""+S[i1:]

# ---------- Lantern Lights ----------
i0=S.index("function gDusk(){"); i1=S.index("function finishGame(){")
S=S[:i0]+r"""function gDusk(){
  const g=game,area=$('#pg'),cols=['#FFD36B','#F29BB5','#A6D8F2','#B5DDB5','#C9A6F2'],names=['Gold','Rose','Blue','Green','Violet'];
  const lb=i=>`<button class="lant" data-lant="${i}" style="--lc:${cols[i]}" aria-label="${names[i]} lantern" disabled></button>`;
  area.insertAdjacentHTML('afterbegin',`<div class="lanterns"><svg class="lstr" viewBox="0 0 100 50" preserveAspectRatio="none" aria-hidden="true"><path d="M0 4Q50 84 100 4" fill="none" stroke-width="1.5" vector-effect="non-scaling-stroke"/></svg>${[0,1,2,3].map(lb).join('')}</div>`);
  const box=area.querySelector('.lanterns'),seq=[],t=$('#pgTime'),show=Math.round(420*(1+.35*g.tr));let L=[...area.querySelectorAll('.lant')],step=0,input=false,star=g.gift?1:0,spare=1,slow=1,sky=0;
  /* the lanterns hang along the string */
  const lay=()=>{const n=L.length,T=n===4?[.14,.38,.62,.86]:[.1,.3,.5,.7,.9];L.forEach((b,i)=>{b.style.left=`calc(${T[i]*100}% - 26px)`;b.style.top=Math.round(2+160*T[i]*(1-T[i]))+'px';});};lay();
  const wire=b=>b.addEventListener('click',()=>pick(+b.dataset.lant));
  const flash=(i,ms)=>{L[i].classList.add('on');gTone('lant',i);g.timers.push(setTimeout(()=>L[i].classList.remove('on'),ms));};
  const play=()=>{input=false;L.forEach(b=>b.disabled=true);step=0;gMsg('Watch.');if(t)t.textContent='Round '+seq.length;
    const gap=Math.round((g.twist?Math.max(400,show+220-45*(seq.length-1)):show+220)*slow);
    seq.forEach((v,k)=>g.timers.push(setTimeout(()=>{if(gOn())flash(v,Math.min(Math.round(show*slow),gap-120));},600+k*gap)));
    g.timers.push(setTimeout(()=>{if(!gOn())return;input=true;L.forEach(b=>b.disabled=false);gMsg('Your turn.');L[0].focus({preventScroll:true});},600+seq.length*gap));};
  const round=()=>{if(!gOn())return;slow=1;
    if(seq.length===7&&L.length===4){box.insertAdjacentHTML('beforeend',lb(4));const b=box.querySelector('[data-lant="4"]');L.push(b);wire(b);lay();gMsg('A fifth lantern joins the string.');
      g.timers.push(setTimeout(()=>{if(!gOn())return;seq.push(Math.floor(Math.random()*L.length));play();},1200));return;}
    seq.push(Math.floor(Math.random()*L.length));play();};
  /* each finished round lets a sky lantern float up */
  const skyL=()=>{if(sky>=12)return;sky++;const e=document.createElement('i');e.className='skyl';e.setAttribute('aria-hidden','true');e.style.left=(8+Math.random()*80)+'%';e.style.setProperty('--up',-Math.round(area.clientHeight*(.18+Math.random()*.3))+'px');area.appendChild(e);};
  const pick=i=>{if(!input||!gOn())return;flash(i,220);
    if(i!==seq[step]){input=false;g.combo=0;
      if(star){star=0;gMsg('The evening star forgives you. Watch again.');g.timers.push(setTimeout(()=>{if(gOn())play();},1300));return;}
      if(spare){spare=0;slow=1.5;gMsg('The lanterns flicker. Once more, slower.');g.timers.push(setTimeout(()=>{if(gOn())play();},1300));return;}
      gMsg('The lanterns flicker out.');sfx('no');gEnd(null);return;}
    step++;if(step===seq.length){gScore(seq.length);const p=gPos(L[i]);gBurst(p[0],p[1],cols[i]);gFloat(p[0],p[1],seq.length+'!');skyL();
      if(seq.length>=12){gEnd('All twelve!');return;}input=false;g.timers.push(setTimeout(round,700));}};
  L.forEach(wire);
  round();
}
"""+S[i1:]

# ---------- the finish: a journal page ----------
rep("""  const n=g.c.nick||g.c.name;
  if(g.free){
    openOverlay(`<p class="rv-title">${G.t}</p><p class="rv-title" style="font-size:30px">${unitOf(G,score)}</p><p class="rv-hint">${nb?'A new best!':best?'Best: '+unitOf(G,best)+'.':''} ${esc(n)} ${g.c.dark?'seems quietly pleased.':'had a lovely time.'}</p>
      <div class="pgbtnrow"><button class="primary" id="pgAgain" data-cid="${g.c.id}" data-gi="${GAMES.indexOf(G)}">Play again</button><button class="ghost" id="pgDone">Done</button></div>`,false);
    return;
  }""","""  const n=g.c.nick||g.c.name,extra=[];
  if(g.pressed)extra.push('A one-of-a-kind snowflake was pressed into your journal.');
  if(g.free){gResult(g,score,nb,best,extra,true);return;}""")
rep("""+(nw&&q&&loreOn()?(talePages(q.ti)===4?` It holds the last page of an old ${mapName(q.ti)} tale. The tale is whole. Read it on the Map tab, under Tales.`:` It remembers a page of an old ${mapName(q.ti)} tale. Read it on the Map tab, under Tales.`):'');}""",
"""+(nw&&q&&loreOn()?(talePages(q.ti)===4?` It holds the last page of an old ${mapName(q.ti)} tale. The tale is whole. Read it on the Map tab, under Tales.`:` It remembers a page of an old ${mapName(q.ti)} tale. Read it on the Map tab, under Tales.`):'');extra.push(`Afterwards, ${n} found something nearby: ${cu.name.toLowerCase()}.`);}""")
rep("""  if(nb)line+=' A new best!';
  doVisit(g.c,'play',pts,line);
}""","""  if(nb)line+=' A new best!';
  extra.unshift(pts===3?'A great round. The bond grew a lot.':pts===2?'A good round. The bond grew.':'The bond grew a little.');
  gBondLater=null;doVisit(g.c,'play',pts,line,true);gResult(g,score,nb,best,extra,false);
}""")
rep("function doVisit(c,kind,pts,line){","function doVisit(c,kind,pts,line,defer){")
rep("  const after=bondLevel(c);if(after>before)setTimeout(()=>openBondUp(c,after),700);\n  return true;",
    "  const after=bondLevel(c);if(after>before){if(defer)gBondLater=()=>openBondUp(c,after);else setTimeout(()=>openBondUp(c,after),700);}\n  return true;")
rep("""lastFocus=null;setTimeout(statueLinkMaybe,800);""","""lastFocus=null;if(gBondLater){const f=gBondLater;gBondLater=null;setTimeout(f,350);}setTimeout(statueLinkMaybe,800);""")

# ---------- the Map ----------
rep("""    if(gl.length)g+=`<path class="mp-st" fill="none" stroke-width="1.1" stroke-opacity="${m.tier===1?.5:.75}" d="${gl.map(p=>glyphD(ti,p[0],p[1])).join('')}"/>`;
    g+=placesSVG(ti);
""","""    if(gl.length)g+=terrainSVG(ti,gl,m.tier);
    g+=placesSVG(ti)+cloudsSVG(ti);
""")
MAPJS=r"""
/* ---- 0.50: the map's terrain is drawn, not marked: trees in Meadow, peaks in Ember (some smoking), waves in Tide,
   pines and snowy peaks in Frost, lamp posts in Dusk (their lamps glow by lamplight). Clouds cover what you have not
   found in a realm and thin with each place you find. ---- */
function terrainSVG(ti,gl,tier){
  const u=2.2,o=gl.map((p,i)=>{const x=p[0]-5.5,y=p[1]-4;
    if(ti===0)return i%3===2?gpx(['.###.','#####'],x,y+2,u,'#7DBF6E'):gpx(['.###.','#####','#####','.###.'],x,y-3,u,'#4E9A5C')+gpx(['..#..','..#..'],x,y+3,u,'#7A5636');
    if(ti===1)return gpx(['..#..','.###.','#####','#####'],x,y-2,u,'#B5483A')+gpx(['..#..'],x,y-2,u,'#E8875A')+(i%3===0?`<path class="mp-smoke" d="M${r1(p[0])} ${r1(p[1]-7)}q-2 -3 0 -5q2 -2 0 -5" fill="none" stroke="#9A8A80" stroke-width="1" stroke-linecap="round"/>`:'');
    if(ti===2)return gpx(['.##...','#..#.#','....#.'],x-.75,y,u,'#3F7FB0');
    if(ti===3)return i%2?gpx(['..#..','.###.','#####'],x,y,u,'#7A8FB8')+gpx(['..#..'],x,y,u,'#FFFFFF'):gpx(['..#..','.###.','..#..','.###.','#####'],x,y-4,u,'#2E5E58')+gpx(['..#..'],x,y+3.5,u,'#6B4A2A');
    return `<circle class="mp-glow" cx="${r1(p[0])}" cy="${r1(p[1]-6)}" r="7"/>`+gpx(['.#.','.#.','.#.','###'],x+1.1,y-2,u,'#4A3E78')+gpx(['###'],x+1.1,y-6.4,u,'#F2B23E');});
  return `<g class="mp-ter" shape-rendering="crispEdges" opacity="${tier===1?.55:1}" aria-hidden="true">${o.join('')}</g>`;
}
function cloudsSVG(ti){
  const pf=placesFound(ti);if(pf>=5)return '';const n=[4,3,3,2,1][pf],P=polyOf(ti),L=mapMid(P),pts=placePts(ti).slice(0,pf),C=['...##...','.#####..','########'];
  const cand=P.map((p,i)=>[L[0]+(p[0]-L[0])*.5,L[1]+(p[1]-L[1])*.5,i]).filter(c=>pts.every(q=>Math.hypot(q[0]-c[0],q[1]-c[1])>18)&&!(Math.abs(c[0]-L[0])<30&&Math.abs(c[1]-L[1])<12));
  cand.sort((a,b)=>whash(ti*71+a[2])-whash(ti*71+b[2]));
  return cand.slice(0,n).map((c,k)=>`<g class="mp-cloud" style="animation-delay:-${(whash(ti*13+k)%80)/10}s" aria-hidden="true"><g opacity=".22">${gpx(C,c[0]-13.6,c[1]-2.6,3.4,'#2E2A47')}</g>${gpx(C,c[0]-13.6,c[1]-5,3.4,'currentColor')}</g>`).join('');
}
"""
rep("function mapHTML(){",MAPJS+"function mapHTML(){")
rep("""  const back=cv.parentNode.classList.contains('mback'),tis=back?[5,6,7,8,9]:[0,1,2,3,4],s=t/1000;
  const dot=(px,py,sz,col,a)=>{x.globalAlpha=Math.max(0,Math.min(1,a));x.fillStyle=col;x.fillRect(px-sz/2,py-sz/2,sz,sz);};""",
"""  const back=cv.parentNode.classList.contains('mback'),tis=back?[5,6,7,8,9]:[0,1,2,3,4],s=t/1000,dark=document.documentElement.getAttribute('data-theme')==='dark';
  const dot=(px,py,sz,col,a)=>{x.globalAlpha=Math.max(0,Math.min(1,a));x.fillStyle=col;x.fillRect(px-sz/2,py-sz/2,sz,sz);};
  /* 0.50: the sea glints, something surfaces now and then, and by lamplight stars come out and found places glint */
  if(!back){const sp=seaPts(false);
    if(dark)sp.forEach((q,i)=>{if(q[2]!==0||i%2)return;dot(q[0]+3,q[1]-6,1.3,'#FFE9A8',still?.6:.3+.5*Math.abs(Math.sin(s*1.3+i)));});
    if(!still){sp.forEach((q,i)=>{if(q[2]!==2)return;const ph=(s/3+whash(i*7)%100/100)%1;dot(q[0]+Math.sin(i)*3,q[1]-1,1.4,dark?'#BFD9FF':'#FFFFFF',Math.max(0,Math.sin(ph*Math.PI*2))*.8);});
      const cyc=s%17;if(cyc<3.6&&sp.length>4){const q=sp[Math.floor(sp.length*.62)],up=Math.sin(cyc/3.6*Math.PI);x.globalAlpha=Math.min(1,up*1.6);x.fillStyle='#2F6B45';
        for(let h=0;h<3;h++){const hh=Math.round(up*3)+(h===2?1:0);x.fillRect(q[0]-8+h*6,q[1]-hh,4,hh+1);}x.fillRect(q[0]+9,q[1]-Math.round(up*4)-2,3,3);x.globalAlpha=1;}}
    if(dark)tis.forEach(ti=>{placePts(ti).slice(0,placesFound(ti)).forEach((q,k)=>{const tw=still?.5:Math.max(0,Math.sin(s*1.7+ti*2+k*1.3));if(tw<.05)return;x.globalAlpha=tw;x.fillStyle='#FFE9A8';x.fillRect(q[0]+5,q[1]-9,1,3);x.fillRect(q[0]+4,q[1]-8,3,1);x.globalAlpha=1;});});}""")
rep("""  const im=mapFxSprite(c);if(!im)return;const sz=20,""","""  /* 0.50: the trail ahead is dotted faintly, and footprints mark the way walked */
  {const bz=u=>{const r=1-u;return [r*r*A[0]+2*r*u*mx+u*u*B[0],r*r*A[1]+2*r*u*my+u*u*B[1]];},ik=dark?'#FFE9A8':'#2E2A47',fw=p<.55?f:1;
    for(let j=1;j<16;j++){const q=bz(j/16);dot(q[0],q[1]+2,1.4,ik,.28);}
    for(let j=1;j<=Math.floor(fw*16);j++){const q=bz(j/16);dot(q[0]+(j%2?1.6:-1.6),q[1]+3,2.2,ik,.6);}}
  const im=mapFxSprite(c);if(!im)return;const sz=20,""")

CSS=r'''
/* ---- 0.50: little worlds ---- */
#pg.pg{isolation:isolate}
.pgsc{position:absolute;inset:0;width:100%;height:100%;z-index:-1;pointer-events:none}
.pg .pgmsg:not(:empty){left:50%;right:auto;transform:translateX(-50%);width:max-content;max-width:88%;padding:3px 10px;background:rgba(16,11,34,.78);color:#F4EEFF}
.pg-meadow .seed::before{filter:drop-shadow(0 0 1px rgba(20,40,30,.95))}
.gsway{transform-box:fill-box;transform-origin:50% 100%;transition:transform .6s ease-in-out}
.pg.gust .gsway{transform:skewX(calc(var(--gd,1) * -16deg))}
.pgink{position:absolute;inset:0;width:100%;height:100%;z-index:2;pointer-events:none}
.pgink polyline{fill:none;stroke-width:3;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1 7;opacity:.8;transition:opacity .45s}
.pgink.fade polyline{opacity:0}
.pg-ember .heat{display:none}
.fstage{position:absolute;left:8px;right:8px;top:8px;display:flex;gap:4px;z-index:2;pointer-events:none}
.fstage span{flex:1;padding:4px 0 3px;text-align:center;font:400 14px/1 'VT323','Courier New',monospace;letter-spacing:.03em;color:#F3DFA6;background:rgba(0,0,0,.45);box-shadow:inset 0 0 0 1px rgba(255,211,107,.4)}
.fstage span.on{background:#FFD36B;color:#2E2A47}
.pg-ember .pgstreak{top:34px}
.pg-ember .fire{width:72px}
.pg-ember .fire i{background:linear-gradient(#FFF3C4,#FFD36B 28%,#FF8A2E 62%,#D9481E);clip-path:polygon(42% 0,58% 0,58% 12%,66% 12%,66% 24%,74% 24%,74% 8%,82% 8%,82% 36%,92% 36%,92% 56%,100% 56%,100% 100%,0 100%,0 56%,8% 56%,8% 36%,18% 36%,18% 8%,26% 8%,26% 24%,34% 24%,34% 12%,42% 12%)}
.pg-ember .fire::after{content:'';position:absolute;left:50%;bottom:-8px;width:calc(60px + var(--heat,60) * 1.6px);height:calc(30px + var(--heat,60) * .7px);transform:translateX(-50%);background:radial-gradient(closest-side,rgba(255,150,60,.38),transparent);z-index:-1}
.pg-ember .pgmate{filter:drop-shadow(0 0 calc(var(--heat,60) * .12px) rgba(255,160,70,.85))}
.pg-ember .emb{filter:drop-shadow(0 0 6px rgba(255,140,40,.75))}
.pg-ember .emb:not(.log)::before{inset:10px 12px;clip-path:polygon(40% 0,60% 0,60% 20%,80% 20%,80% 45%,100% 45%,100% 100%,0 100%,0 45%,20% 45%,20% 20%,40% 20%);background:linear-gradient(#FFE38A,#FF8A2E 55%,#E5441E);box-shadow:none;transition:background .4s}
.emb.rise{animation:none}
.pg-ember .emb.cool{filter:none}
.pg-ember .emb.cool:not(.log)::before{background:#8F857E}
.pg-tide .calm{position:absolute;bottom:auto;height:10px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,255,255,.95),rgba(205,238,255,.6) 60%,rgba(166,216,242,0));box-shadow:none;z-index:1;transition:opacity .2s}
.pg-tide .stone{top:0;left:0;margin:-7px 0 0 -11px;z-index:2;transition:opacity .25s}
.ripr{position:absolute;width:30px;height:8px;margin:-4px 0 0 -15px;border:2px solid rgba(255,255,255,.85);border-radius:50%;pointer-events:none;z-index:1;animation:ripr 2.4s ease-out forwards}
.ripr.big{border-width:2.5px}
@keyframes ripr{from{transform:scale(.4);opacity:1}to{transform:scale(2.4);opacity:0}}
.pg-tide .skips{top:10px;left:50%;right:auto;transform:translateX(-50%);width:max-content;max-width:90%;padding:3px 10px;background:rgba(16,11,34,.78);color:#F4EEFF;margin:0;z-index:3}
.fcol{position:absolute;left:8px;top:8px;display:flex;gap:3px;padding:4px;background:rgba(16,11,34,.5);z-index:2;pointer-events:none}
.fcol i{width:14px;height:14px;opacity:.28}
.fcol i.got{opacity:1}
.pg-frost .flake{filter:drop-shadow(0 0 1px #4B6A9E)}
.flake.rare{width:26px;height:26px;margin-left:-13px;filter:drop-shadow(0 0 6px rgba(255,211,107,.95))}
.hshad{position:absolute;bottom:22px;width:22px;height:6px;margin-left:-11px;border-radius:50%;background:#2A3A5C;opacity:0;pointer-events:none;z-index:0}
.pg-frost .basket::after{content:'';position:absolute;left:8px;right:8px;bottom:2px;height:8px;background:#A8323F;box-shadow:inset 0 -3px 0 #7E2230,0 3px 0 #3B2A22}
.pg-dusk .lanterns{inset:auto;left:8px;right:8px;top:24px;height:130px;display:block}
.lstr{position:absolute;left:0;top:0;width:100%;height:50px;stroke:#8B7AB8;pointer-events:none}
.pg-dusk .lant{position:absolute;width:52px;height:66px;min-height:44px;padding:0;background:transparent;box-shadow:none;display:grid;place-items:center}
.pg-dusk .lant::after{content:'';position:absolute;left:24px;top:0;width:4px;height:12px;background:#8B7AB8}
.pg-dusk .lant::before{width:30px;height:44px;margin-top:12px;opacity:.45}
.pg-dusk .lant.on{background:transparent;box-shadow:none;filter:drop-shadow(0 0 12px var(--lc))}
.pg-dusk .lant.on::before{opacity:1}
.skyl{position:absolute;bottom:42%;width:10px;height:13px;background:#FFB04A;clip-path:polygon(20% 0,80% 0,100% 30%,90% 100%,10% 100%,0 30%);pointer-events:none;z-index:0;animation:skyl 3s ease-out forwards}
@keyframes skyl{from{transform:translateY(0);opacity:.2}to{transform:translateY(var(--up));opacity:.9}}
.pgzz{position:absolute;z-index:3;font:700 22px/1 var(--hand);color:#FFF3C4;text-shadow:0 1px 0 #000;pointer-events:none;animation:pgzz 2.6s ease-out forwards}
@keyframes pgzz{from{opacity:0;transform:translateY(8px)}20%{opacity:1}to{opacity:0;transform:translateY(-14px)}}
.pgmate.cheer{animation:mateCheer .8s ease-out}
@keyframes mateCheer{30%{transform:translateY(-16px) scale(1.08)}60%{transform:none}80%{transform:translateY(-6px)}}
@media (prefers-reduced-motion: reduce){.gsway,.pgink polyline{transition:none}.ripr{animation:none;opacity:.6}.skyl{animation:none;transform:translateY(var(--up));opacity:.9}.pgzz,.pgmate.cheer{animation:none}}
html.reduce .gsway,html.reduce .pgink polyline{transition:none}
html.reduce .ripr{animation:none;opacity:.6}
html.reduce .skyl{animation:none;transform:translateY(var(--up));opacity:.9}
html.reduce .pgzz,html.reduce .pgmate.cheer{animation:none}
/* the game sheet: postcards */
#modal .pcard{background:#FBF5E6;color:#2E2A47;border:0;box-shadow:3px 3px 0 #D9C69C;transform:rotate(var(--r,0deg));margin-bottom:4px}
#modal .pcard b,#modal .pcard span{color:#2E2A47}
#modal .pcard .pcs{width:56px;height:56px;flex:none;box-shadow:0 0 0 2px #FFFFFF,2px 3px 0 2px rgba(0,0,0,.18)}
/* the result: a journal page */
.gres{position:relative;width:100%;max-width:330px;box-sizing:border-box;margin:4px auto 10px;padding:16px 16px 16px 34px;text-align:left;color:#2E2A47;background:repeating-linear-gradient(transparent 0 25px,rgba(91,74,158,.12) 25px 26px),#FBF5E6;box-shadow:4px 4px 0 #E3D3AE,8px 8px 0 #D9C69C}
.gres::before{content:'';position:absolute;left:22px;top:0;bottom:0;width:2px;background:rgba(168,50,63,.35)}
.gres .gd{margin:0;font:400 15px/1 'VT323','Courier New',monospace;letter-spacing:.08em;text-transform:uppercase;color:#6B5A3A}
.gres h2{margin:6px 0 0;max-width:calc(100% - 64px);font:700 28px/1.02 var(--hand);color:#2E2A47;text-align:left}
.gres .gs{margin:10px 0 0;font:400 46px/1 'VT323','Courier New',monospace;color:#2E2A47}
.gres .gs span{font:700 24px/1 var(--hand)}
.gres .gl{margin:8px 0 0;font:italic 400 15px/1.4 var(--body);color:#4B3C8C}
.gres .gx{margin:6px 0 0;font:400 14px/1.4 var(--body);color:#3A3550}
.gstamp{position:absolute;right:12px;top:50px;width:72px;height:72px;border-radius:50%;border:3px solid #A8323F;color:#A8323F;display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(-12deg);box-shadow:inset 0 0 0 3px #FBF5E6,inset 0 0 0 5px #A8323F;animation:gstamp .4s ease-out}
.gstamp b{font:400 24px/.9 'VT323','Courier New',monospace}
.gstamp span{font:700 9px/1.2 var(--body);letter-spacing:.12em}
@keyframes gstamp{from{transform:rotate(-12deg) scale(1.6);opacity:0}to{transform:rotate(-12deg) scale(1);opacity:1}}
@media (prefers-reduced-motion: reduce){.gstamp{animation:none}}
html.reduce .gstamp{animation:none}
/* ---- 0.50: the map's terrain, clouds and lamps ---- */
.mp-cloud{color:#FFFFFF;opacity:.94;animation:mpDrift 9s ease-in-out infinite alternate}
html[data-theme=dark] .mp-cloud{color:#9A90C4;opacity:.8}
@keyframes mpDrift{to{transform:translateX(4px)}}
.mp-smoke{opacity:.6;animation:mpSmoke 3.2s ease-in-out infinite}
@keyframes mpSmoke{50%{opacity:.2;transform:translateY(-1.5px)}}
.mp-glow{fill:#FFD36B;opacity:0}
html[data-theme=dark] .mp-glow{opacity:.4}
@media (prefers-reduced-motion: reduce){.mp-cloud,.mp-smoke{animation:none}}
html.reduce .mp-cloud,html.reduce .mp-smoke{animation:none}
'''
# six pixel snowflake kinds (and the one-of-a-kind) as tiny SVGs
K=[['..#..','#.#.#','.###.','#####','.###.','#.#.#','..#..'],['#...#','.#.#.','..#..','.#.#.','#...#'],['.#.#.','#####','.#.#.','#####','.#.#.'],
   ['...#...','.#.#.#.','..###..','#######','..###..','.#.#.#.','...#...'],['..#..','.###.','#####','.###.','..#..'],['#.#.#','.....','#.#.#','.....','#.#.#']]
RARE=['..#.#..','#.#.#.#','.#####.','##.#.##','.#####.','#.#.#.#','..#.#..']
def svgk(rows,col):
    w=max(len(r) for r in rows); h=len(rows); o=''
    for j,r in enumerate(rows):
        for i,ch in enumerate(r):
            if ch=='#': o+=f"<rect x='{i}' y='{j}' width='1' height='1'/>"
    return f"url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}' shape-rendering='crispEdges' fill='{col}'%3E{o}%3C/svg%3E\") center/contain no-repeat"
for i,rows in enumerate(K): CSS+=f".flk{i}{{background:{svgk(rows,'%23FFFFFF')}}}\n.flake.flk{i}{{clip-path:none}}\n"
CSS+=f".flake.rare{{clip-path:none;background:{svgk(RARE,'%23FFD36B')}}}\n"
i=S.index("</style>",S.index("</style>")+1); S=S[:i]+CSS+S[i:]

rep("""<ul class="newlist"><li><b>Find any Forgeling.</b>""","""<ul class="newlist"><li><b>Games with a world around them.</b> Each game is played in a little scene of its realm, and each has something new: swipe through dandelion seeds, build the fire to a bonfire, skip one stone across the lake, catch six kinds of snowflake, and watch sky lanterns rise. Your Forgeling reacts as you play, and a round ends on a journal page with a stamp for a new best. On the Map, the land is drawn in, clouds cover what you have not found yet, and by lamplight the stars come out.</li><li><b>Find any Forgeling.</b>""")
m=re.search(r'<ul class="newlist">(.*?)</ul>',S,re.S); items=re.findall(r'<li>.*?</li>',m.group(1),re.S)
assert len(items)==9,len(items); rep(items[-1],"")
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk50.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk50.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)

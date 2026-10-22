# Forge 0.24.2: game fixes found with real touch input. Reads base241.html, writes work.html.
# 1. Dandelion Drift: the seeds' "drift" animation clashed with the living sky's "drift", so seeds never rose into view.
#    Seeds now move by script (like the snowflakes and the stone), which also keeps the game playable with Reduce Motion.
# 2. Snowflake Catch: a finger drag became a page scroll (pointercancel). Game areas now take all touches, and dragging
#    follows the finger for as long as it is down.
# 3. Reduce Motion no longer turns four games into "sit together": the game's own motion is the activity the player asked
#    for, while decorative motion (hops, pop-ins, ripples) stays off as before.
src = open('base241.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

# 1. seeds move by script
rep('.seed{position:absolute;bottom:-44px;width:48px;height:48px;border:0;background:none;padding:0;animation:drift linear forwards}',
    '.seed{position:absolute;bottom:-44px;width:48px;height:48px;border:0;background:none;padding:0;will-change:transform}')
rep(".seed.caught,.emb.caught,.flake.caught{animation:none;opacity:0;transform:scale(1.8);transition:.15s}",
    ".seed.caught,.emb.caught,.flake.caught{animation:none;opacity:0;transition:opacity .15s}")
rep("@keyframes drift{0%{transform:translate(0,0)}25%{transform:translate(14px,-110px)}50%{transform:translate(-10px,-220px)}75%{transform:translate(12px,-320px)}100%{transform:translate(0,-420px)}}\n", "")
rep("""  const spawn=()=>{if(!game||!game.alive)return;const b=document.createElement('button');b.className='seed';b.type='button';b.setAttribute('aria-label','Seed');b.style.left=(4+Math.random()*78)+'%';b.style.animationDuration=(2.6+Math.random()*1.2)+'s';
    b.addEventListener('pointerdown',ev=>{ev.preventDefault();if(b._c||!game||!game.alive)return;b._c=1;gScore(game.score+1);b.classList.add('caught');chime(0);setTimeout(()=>b.remove(),160);});
    b.addEventListener('animationend',()=>b.remove());area.appendChild(b);};
  spawn();game.timers.push(setInterval(spawn,560));gClock(15);""",
"""  let seeds=[],last=performance.now();
  const spawn=()=>{if(!game||!game.alive)return;const b=document.createElement('button');b.className='seed';b.type='button';b.setAttribute('aria-label','Seed');b.style.left=(4+Math.random()*78)+'%';
    const o={el:b,y:0,v:(area.clientHeight+48)/(2.6+Math.random()*1.2),ph:Math.random()*6.28};
    b.addEventListener('pointerdown',ev=>{ev.preventDefault();if(b._c||!game||!game.alive)return;b._c=1;gScore(game.score+1);b.classList.add('caught');chime(0);setTimeout(()=>b.remove(),160);});
    area.appendChild(b);seeds.push(o);};
  const loop=now=>{if(!game||!game.alive)return;const dt=Math.min(.05,(now-last)/1000),H=area.clientHeight;last=now;
    seeds=seeds.filter(o=>{if(o.el._c)return false;o.y+=o.v*dt;if(o.y>H+52){o.el.remove();return false;}o.el.style.transform=`translate(${Math.round(Math.sin(o.ph+o.y/60)*12)}px,${-Math.round(o.y)}px)`;return true;});
    game.raf=requestAnimationFrame(loop);};
  game.raf=requestAnimationFrame(loop);spawn();game.timers.push(setInterval(spawn,560));gClock(15);""")

# 2. game areas take every touch; dragging follows the finger while it is down
rep('.pg{position:relative;width:100%;max-width:320px;height:340px;border:3px solid rgba(255,255,255,.3);background:rgba(0,0,0,.25);overflow:hidden;touch-action:manipulation}',
    '.pg{position:relative;width:100%;max-width:320px;height:340px;border:3px solid rgba(255,255,255,.3);background:rgba(0,0,0,.25);overflow:hidden;touch-action:none;-webkit-user-select:none;user-select:none;-webkit-touch-callout:none}')
rep("area.addEventListener('pointerdown',ev=>{ev.preventDefault();fromEv(ev);});area.addEventListener('pointermove',ev=>{if(ev.pressure>0||ev.pointerType==='mouse')fromEv(ev);});",
    "let drag=false;area.addEventListener('pointerdown',ev=>{ev.preventDefault();drag=true;try{area.setPointerCapture(ev.pointerId);}catch(e){}fromEv(ev);});area.addEventListener('pointermove',ev=>{if(drag||ev.pointerType==='mouse')fromEv(ev);});['pointerup','pointercancel','lostpointercapture'].forEach(t=>area.addEventListener(t,()=>{drag=false;}));")

# 3. every game can be played with Reduce Motion on
rep("  if(REDUCE&&G.id!=='dusk'){if(!free)doVisit(c,'sit',1,lineFor(c,'sit',''));else toast('With reduced motion on, this game rests. Try a Dusk Forgeling’s lantern game.');return;}\n", "")

rep('<title>Forge (prototype 0.24.1)</title>', '<title>Forge (prototype 0.24.2)</title>')
rep("const VERSION='prototype 0.24.1';", "const VERSION='prototype 0.24.2';")
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src))

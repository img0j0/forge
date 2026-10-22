# Forge 0.25.1: a game chooser. Play in the Hearth now opens all five games; each is played by a Forgeling from that
# realm (the one by the fire if it belongs there, otherwise your closest-bonded one), so every game you have a
# Forgeling for is one tap away. Reads base25.html, writes work.html.
src = open('base25.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

rep('/* Nav */', '''.moodbtn img.gpick{width:44px;height:44px;image-rendering:pixelated;flex:none}
.moodbtn.gwait{opacity:1;border-style:dashed}
/* Nav */''')

# the Hearth says Play opens every game
rep("Play is ${esc(gameFor(c).t)}${state.games.best[gameFor(c).id]?`, best ${unitOf(gameFor(c),state.games.best[gameFor(c).id])}`:''}.`",
    "Play opens all five games.`")
rep("You can still play ${esc(gameFor(c).t)} just for fun.", "You can still play the games just for fun.")
rep("else if(b.id==='hPlay'&&c)openPlay(c);", "else if(b.id==='hPlay'&&c)openGames(c);")

rep('function gStart(){', r'''/* 0.25.1: choose any game. A realm's game is played by its Forgeling: the one by the fire if it belongs to that realm,
   otherwise your closest-bonded one there (never one who is out wandering). */
const realmOf=c=>Math.abs(c.theme|0)%5;
function playerFor(ti,c){const away=state.wander&&state.wander.id;
  if(c&&realmOf(c)===ti&&c.id!==away)return c;
  return state.cards.filter(x=>realmOf(x)===ti&&x.id!==away).sort((a,b)=>(b.bond||0)-(a.bond||0)||b.rarity-a.rarity||a.id-b.id)[0]||null;}
function openGames(c){
  const left=visitsLeft(),mine=c?realmOf(c):0,order=[mine].concat([0,1,2,3,4].filter(i=>i!==mine));
  openSheet(`<h2>Play a game</h2><p class="muted small">${left?`Visits left today: ${left} of 3. A round grows the bond of the Forgeling who plays.`:'Your visits are used up for today, so these are just for fun.'}</p>
    ${order.map(ti=>{const G=GAMES[ti],p=playerFor(ti,c),best=state.games.best[G.id]||0;
      return p?`<button class="moodbtn" data-game="${ti}" data-cid="${p.id}"><img class="gpick" src="${spriteURL(p)}" alt=""><div><b>${G.t}</b><span>${esc(p.nick||p.name)} plays${best?`. Best: ${unitOf(G,best)}`:''}</span></div></button>`
        :`<div class="moodbtn gwait" role="note"><div><b>${G.t}</b><span>Find ${/^[AEIOU]/.test(THEMES[ti].name)?'an':'a'} ${THEMES[ti].name} Forgeling to play this one.</span></div></div>`;}).join('')}
    <div class="row" style="justify-content:center"><button class="ghost" data-close>Not now</button></div>`);
  const f=$('#modal [data-game]');if(f)f.focus({preventScroll:true});
}
function gStart(){''')
rep("  if(b.id==='pgGo')gStart();", "  if(b.id==='pgGo')gStart();\n  else if(b.dataset.game!==undefined){const p=cardById(+b.dataset.cid);if(p)openPlay(p);}")

rep('<title>Forge (prototype 0.25.0)</title>', '<title>Forge (prototype 0.25.1)</title>')
rep("const VERSION='prototype 0.25.0';", "const VERSION='prototype 0.25.1';")
rep("<li><b>Deeper games.</b> Your Forgeling now shapes its game.",
    "<li><b>Deeper games.</b> Play in the Hearth opens all five games, each played by a Forgeling from its realm. Your Forgeling now shapes its game.")
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src))

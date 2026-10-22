# Forge 0.25.2: any Forgeling can play any game. The chooser lets you pick who plays (from the Forgelings by the fire)
# and then any of the five games. Stats shape every game; dark Forgelings get each game's twist; a Forgeling's own
# realm game is marked Home and listed first. Reads base251.html, writes work.html.
src = open('base251.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

rep('/* Nav */', '''.gwho{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0 2px}
.gwho button{display:flex;align-items:center;gap:6px;min-height:44px;padding:4px 12px 4px 6px;border-radius:999px;border:2px solid var(--line);background:var(--surface);color:var(--ink);font:600 15px var(--display)}
.gwho button[aria-pressed="true"]{border-color:var(--plum);background:var(--chip)}
.gwho img{width:32px;height:32px;image-rendering:pixelated}
.moodbtn .home{display:inline-block;margin-left:6px;padding:1px 8px;border-radius:999px;background:var(--butter);color:#2E2A47;font:600 12px var(--body);vertical-align:2px}
/* Nav */''')

# openPlay takes the chosen game; the twist is named for the game's realm
rep("function openPlay(c){\n  const free=visitsLeft()<1,G=gameFor(c),",
    "function openPlay(c,gi){\n  const free=visitsLeft()<1,G=Number.isInteger(gi)&&GAMES[gi]?GAMES[gi]:gameFor(c),")
rep("twist?`<p class=\"tw\"><b>${esc(realmName(c))} twist</b>",
    "twist?`<p class=\"tw\"><b>${esc(THEMES[GAMES.indexOf(G)].dark.name)} twist</b>")
rep('data-cid="${g.c.id}">Play again', 'data-cid="${g.c.id}" data-gi="${GAMES.indexOf(G)}">Play again')
rep("else if(b.id==='pgAgain'){const c=cardById(+b.dataset.cid);closeModal();if(c)openPlay(c);}",
    "else if(b.id==='pgAgain'){const c=cardById(+b.dataset.cid);closeModal();if(c)openPlay(c,+b.dataset.gi);}")

# the chooser: who plays, then any game
start = src.index('/* 0.25.1: choose any game.')
end = src.index('function gStart(){')
src = src[:start] + r'''/* 0.25.2: any Forgeling plays any game. Pick who plays from the Forgelings by the fire (never one out wandering), then
   any of the five games. A Forgeling's own realm game is its Home game and comes first. */
const realmOf=c=>Math.abs(c.theme|0)%5;
function gPlayers(){const away=state.wander&&state.wander.id;return slotCards().filter(x=>x&&x.id!==away);}
function openGames(c){
  const ps=gPlayers();if(!c||!ps.some(x=>x.id===c.id))c=ps[0];if(!c){toast('Bring a Forgeling to the fire to play.');return;}
  const left=visitsLeft(),home=realmOf(c),order=[home].concat([0,1,2,3,4].filter(i=>i!==home)),n=c.nick||c.name;
  openSheet(`<h2>Play a game</h2><p class="muted small">${left?`Visits left today: ${left} of 3. A round grows the bond of the Forgeling who plays.`:'Your visits are used up for today, so these are just for fun.'}</p>
    ${ps.length>1?`<div class="gwho" role="group" aria-label="Who plays">${ps.map(p=>`<button data-gwho="${p.id}" aria-pressed="${p.id===c.id}"><img src="${spriteURL(p)}" alt="">${esc(p.nick||p.name)}</button>`).join('')}</div>`:''}
    ${order.map(ti=>{const G=GAMES[ti],best=state.games.best[G.id]||0;
      return `<button class="moodbtn" data-game="${ti}" data-cid="${c.id}"><img class="gpick" src="${spriteURL(c)}" alt=""><div><b>${G.t}${ti===home?'<span class="home">Home</span>':''}</b><span>${esc(n)} plays${best?`. Best: ${unitOf(G,best)}`:''}</span></div></button>`;}).join('')}
    <div class="row" style="justify-content:center"><button class="ghost" data-close>Not now</button></div>`);
  const f=$('#modal [data-game]');if(f)f.focus({preventScroll:true});
}
''' + src[end:]
rep("  else if(b.dataset.game!==undefined){const p=cardById(+b.dataset.cid);if(p)openPlay(p);}",
    "  else if(b.dataset.game!==undefined){const p=cardById(+b.dataset.cid);if(p)openPlay(p,+b.dataset.game);}\n  else if(b.dataset.gwho!==undefined){const p=cardById(+b.dataset.gwho);if(p){const i=slotCards().findIndex(x=>x&&x.id===p.id);if(i>=0)hf.sel=i;openGames(p);const w=$(`#modal [data-gwho=\"${p.id}\"]`);if(w)w.focus({preventScroll:true});}}")
rep("Play opens all five games.`", "Play any of the five games.`")

rep('<title>Forge (prototype 0.25.1)</title>', '<title>Forge (prototype 0.25.2)</title>')
rep("const VERSION='prototype 0.25.1';", "const VERSION='prototype 0.25.2';")
rep("<li><b>Deeper games.</b> Play in the Hearth opens all five games, each played by a Forgeling from its realm. Your Forgeling now shapes its game.",
    "<li><b>Deeper games.</b> Play in the Hearth lets any Forgeling by the fire play any of the five games. Your Forgeling's stats shape each one.")
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src))

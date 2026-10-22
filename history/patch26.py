# Forge 0.26.0: the old tales of the realms. Each realm's four curios each remember one page of that realm's old tale.
# A new curio shows its page right away; four pages make the tale whole. Tales live in the Chronicle (Tales tab), the
# realm page shows progress, and two ribbons mark finished tales. Lore off hides all of it. Reads base252.html.
src = open('base252.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

rep('/* Nav */', '''.otale{border:1.5px solid var(--line);border-radius:14px;padding:12px 14px;margin:10px 0;background:var(--surface)}
.otale h3{margin:0 0 2px;font:600 17px var(--display)}
.otale .meta{margin:0 0 8px;color:var(--muted);font-size:13px}
.otale ol{margin:0;padding:0;list-style:none;display:grid;gap:8px}
.otale li.gone{color:var(--muted);font-size:14px}
.otale li .g{display:inline-block;width:1.5em}
.otale li .world{border:0;padding:0;margin:0;display:inline}
.otale.whole{border-color:#E2B04A;box-shadow:inset 0 0 0 1px #E2B04A}
.otale .done{margin:8px 0 0;font-size:14px}
/* Nav */''')

TALES_JS = r'''/* ---- 0.26: the old tales. Every realm forgot a tale, and each of its four curios remembers one page. ---- */
const TALES=[
 {t:'The Slow Hill',p:[
  ['acorn','Before Meadow had a name, it was one bare hill. A Forgeling planted an acorn there and sat down to wait. Everyone said nothing would come of it. The Forgeling said that was fine. It liked the view.'],
  ['flower','The first spring, one flower came up crooked. The Forgeling did not straighten it. It watered it and said good morning. The next spring there were two, both crooked, both fine.'],
  ['feather','Birds came for the flowers and stayed for the company. One left a feather behind, which is how birds say they will be back. The hill began, very slowly, to hum.'],
  ['mushroom','Part of the hill grew wild while nobody looked. That edge became Bramble, and it kept the untended things safe until someone came back for them. Its mushrooms glow only when you look away. They are shy, not secret.']],
  end:'The hill is Meadow now. It still grows at its own speed, and it still likes the view.'},
 {t:'The Spark That Leapt',p:[
  ['spark','The Forge struck its first spark, and the spark did not wait to be finished. It leapt. Where it landed, the ground stayed warm, and the warm ground became Ember.'],
  ['leaf','The first tree in Ember grew red leaves that stay a little warm. They were never on fire. They just remember being near one.'],
  ['bone','Under Ember, pressure gathered into black stone. The Inferno guardians took the heavy things people kept putting off and held them there, safe and warm. They set a bone beside the first fire as a promise: we will hold it until you are ready.'],
  ['crystal','When someone finally picks the hard thing back up, the stone where it lay cools into crystal. Inferno is full of crystals now. Each one hums with something that got done.']],
  end:'Ember still burns on effort, and Inferno still holds what waits. Neither one is in a hurry for you.'},
 {t:'Where the Tide Goes',p:[
  ['shell','Tide was once still water that did not know what it wanted. A Forgeling dropped a shell in it to see what would happen. The water laughed, and that was the first wave.'],
  ['pebble','The waves carried one pebble back and forth for a hundred years, until it was perfectly round. They were never in a hurry. They just liked the company.'],
  ['coin','Deeper down, the Abyss keeps the questions nobody has asked yet. One was stamped onto a coin: a crown on one side, a warning on the other. It asks which matters more. The Abyss waits with you for the answer.'],
  ['rain','When the Abyss has held a question long enough, it lets the answer rise as rain. That is why Tide rain feels like a thought you almost had. Catch some. Keep it in your pocket.']],
  end:'Tide still goes wherever you bring it, and the Abyss still waits beside you, not ahead of you.'},
 {t:'The Quiet Mountain',p:[
  ['snow','Frost began as one snowflake that would not melt, because it had decided something. Every flake after it decided something too. That is why the air there is so clear.'],
  ['bell','A Frost Forgeling hung a bell on the highest peak to tell the others when to listen. It rang once a year. Everyone came, nobody spoke, and that was the point.'],
  ['glimmer','In the whiteout, Wraith grew so quiet the quiet took a shape. Its guardians found a glimmer in a hollow log and kept it lit, so nobody lost in the snow would think they were alone.'],
  ['moon','On the longest night, the moon came down to rest on the peak. When it left, a sliver stayed behind, as thanks for the quiet. Frost still keeps it, and has never once spent it.']],
  end:'The mountain is still quiet. It is the kind of quiet that keeps you company.'},
 {t:'The Workshop Between',p:[
  ['map','Dusk was the first workshop. Its makers drew a map of everywhere they had not been yet, and marked one small hill with care, in case anyone needed a place to start.'],
  ['candle','The first candle in Dusk lit itself the moment a maker asked to see their work more clearly. The workshops have never been fully dark since.'],
  ['key','Below the workshops lies the Void, where people leave the things they are afraid to say. Its guardians made one small iron key for all of it. It opens nothing until you are ready. Then it opens anything.'],
  ['thread','A red thread runs from the Void up to the workshop door, so whatever is said in the dark can find its way home. Orrun walked it first, carrying a small light. Others have followed since.']],
  end:'Dusk is still the hour between. Whatever you make there, and whatever you finally say, has a way home.'}];
const taleOf=id=>{for(let ti=0;ti<5;ti++){const k=TALES[ti].p.findIndex(x=>x[0]===id);if(k>=0)return {ti,k};}return null;};
const talePages=ti=>TALES[ti].p.filter(x=>state.curios[x[0]]).length;
const talesDone=()=>[0,1,2,3,4].filter(ti=>talePages(ti)===4).length;
const loreOn=()=>state.settings.lore!==false;
/* The page a new curio remembers, shown where you find it. */
function talePageHTML(id){
  if(!loreOn())return '';const q=taleOf(id);if(!q)return '';const T=TALES[q.ti],n=talePages(q.ti),R=THEMES[q.ti].name;
  return `<div class="tale new"><b>A page of an old ${R} tale: ${T.t}</b><p class="world">${esc(T.p[q.k][1])}</p>
    <p class="small">${n===4?`<b>The tale is whole.</b> ${esc(T.end)}`:`Pages found: ${n} of 4. The rest are with other ${R} curios.`} Read the whole tale on the Map tab, under Tales.</p></div>`;
}
function oldTalesHTML(){
  if(!loreOn())return '';
  const any=Object.keys(state.curios).length;
  return `<h2 style="margin-top:4px">Old tales of the realms</h2><p class="muted small">Every realm forgot a tale. Each of its four curios remembers one page. Wander a realm to bring its pages home.</p>`+
   TALES.map((T,ti)=>{const n=talePages(ti),R=THEMES[ti].name;
    return `<div class="otale${n===4?' whole':''}"><h3>${n?T.t:R+': an untold tale'}</h3><p class="meta">${R}. ${n} of 4 pages${n===4?'. The tale is whole.':''}</p>
      ${n?`<ol>${T.p.map(([id,txt])=>{const cu=CURIOS.find(x=>x.id===id);return state.curios[id]?`<li><span class="g" aria-hidden="true">${cu.g}</span><span class="world">${esc(txt)}</span></li>`:`<li class="gone">A page is missing. Another ${R} curio remembers it.</li>`;}).join('')}</ol>${n===4?`<p class="done world">${esc(T.end)}</p>`:''}`:`<p class="muted small" style="margin:0">${any?`No pages yet. Send a Forgeling to wander in ${R}.`:'Send a Forgeling wandering to find your first curio.'}</p>`}</div>`;}).join('');
}
'''
rep('function talesHTML(){', TALES_JS + 'function talesHTML(){')
# the Tales tab opens with the old tales
rep("""function talesHTML(){
  const cards=state.cards.slice().reverse();
  if(!cards.length)return '<p class="muted">Your Chronicle begins with your first Forgeling.</p>';""",
    """function talesHTML(){
  const cards=state.cards.slice().reverse(),ot=oldTalesHTML();
  if(!cards.length)return ot+'<p class="muted">Your Chronicle begins with your first Forgeling.</p>';""")
# the tale list must come first in the returned markup
src_i = src.index("  const shown=cards.slice(0,ch.more*12);\n  return shown.map(c=>`<div class=\"chron\">")
rep("  const shown=cards.slice(0,ch.more*12);\n  return shown.map(c=>`<div class=\"chron\">",
    "  const shown=cards.slice(0,ch.more*12);\n  return ot+(ot?'<h2 style=\"margin-top:18px\">Your Forgelings</h2>':'')+shown.map(c=>`<div class=\"chron\">")

# a new curio from wandering shows its page
rep("""    <p class="muted small center">Curios found: ${have} of ${CURIOS.length}</p>${done}""",
    """    <p class="muted small center">Curios found: ${have} of ${CURIOS.length}</p>${isNew?talePageHTML(cu.id):''}${done}""")
# a curio from a great game round says so in the Hearth
rep("line+=` Afterwards, ${n} found something nearby: ${cu.name.toLowerCase()}.`;}",
    "const nw=cur.n===1,q=taleOf(cu.id);line+=` Afterwards, ${n} found something nearby: ${cu.name.toLowerCase()}.`+(nw&&q&&loreOn()?(talePages(q.ti)===4?` It holds the last page of an old ${THEMES[q.ti].name} tale. The tale is whole. Read it on the Map tab, under Tales.`:` It remembers a page of an old ${THEMES[q.ti].name} tale. Read it on the Map tab, under Tales.`):'');}")

# the realm page shows the tale's progress
rep("""  if(ra)out+=`<p class="muted small" style="margin:6px 0 0">${esc(ra.nick||ra.name)} asked for something from here.</p>`;""",
    """  if(ra)out+=`<p class="muted small" style="margin:6px 0 0">${esc(ra.nick||ra.name)} asked for something from here.</p>`;
  if(loreOn()){const tp=talePages(ti);out+=`<p class="muted small" style="margin:6px 0 0">Old tale: ${TALES[ti].t}. ${tp===4?'The tale is whole.':tp+' of 4 pages found.'}</p>`;}""")

# ribbons
rep("  {id:'curios',name:'Curio Shelf',desc:'Find 10 different curios.',g:10,f:()=>Object.keys(state.curios).length},",
    "  {id:'curios',name:'Curio Shelf',desc:'Find 10 different curios.',g:10,f:()=>Object.keys(state.curios).length},\n  {id:'tale1',name:'Tale Keeper',desc:'Make a realm\\'s old tale whole.',g:1,f:()=>talesDone()},\n  {id:'tales5',name:'Keeper of Old Tales',desc:'Make all five old tales whole.',g:5,f:()=>talesDone()},")

rep('<title>Forge (prototype 0.25.2)</title>', '<title>Forge (prototype 0.26.0)</title>')
rep("const VERSION='prototype 0.25.2';", "const VERSION='prototype 0.26.0';")
rep('const SEEN_V=29;', 'const SEEN_V=30;')
rep("""<ul class="newlist"><li><b>Deeper games.</b>""",
    """<ul class="newlist"><li><b>Old tales.</b> Every realm forgot a tale, and each of its curios remembers one page. Find all four curios from a realm to make its tale whole. Read them on the Map tab, under Tales.</li>
    <li><b>Deeper games.</b>""")
import re as _re
_i=src.index('<ul class="newlist">'); _j=src.index('</ul>',_i)
_items=_re.findall(r'\s*<li>.*?</li>',src[_i+len('<ul class="newlist">'):_j],_re.S)
src=src[:_i]+'<ul class="newlist">'+''.join(_items[:10])+src[_j:]
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src))

# Forgelings 0.41.0: the other side (the Shade side), from the Forge design doc, with Hunter's eight decisions (October 28):
# 1. The forged tool is the Crossing Lantern (id xlantern), so it never mixes with the request keepsake "Little lantern".
# 2. Lantern costs 6 embers. Once a realm is fully charted it is listed first in the Forge, and the Forge panel says
#    "A charted realm is waiting for a lantern." Statues stay as they are.
# 3. The lantern is visible from the start ("Needs ... a fully charted realm"). Shade planks, the back of the map,
#    Shade tales, wards and the two Shade ribbons stay hidden until the lantern is made.
# 4. Any Forgeling can cross. The wander sheet marks a Shade Forgeling's own twin realm as Home (flavour only).
# 5. The front of the map shows bright names for every player; Shade names live on the back.
# 6. Wards can be worn by any Forgeling; a statue cast while wearing one keeps it.
# 7. Shade curios come from wanders only (one new find a day). Games stay front-side, the compass points to Shade
#    realms once they are open, requests stay front-side.
# 8. Shade curios stay out of gift links (0.42 brings forged-charm gifts).
# Shade realm index si = 5..9 is the twin of bright realm si-5. Opening is derived: lantern made and the twin's front
# realm fully charted. Shade places reuse state.explore[si] (first place drawn on crossing, one per first wander a day).
# Reads base402.html.
import re
src = open('base402.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

rep("const VERSION='prototype 0.40.2'", "const VERSION='prototype 0.41.0'")
rep("<title>Forgelings (prototype 0.40.1)</title>", "<title>Forgelings (prototype 0.41.0)</title>")
rep("const SEEN_V=45;", "const SEEN_V=46;")

# ---------- curio art: 20 Shade curios (curios/sprites.py -> curios/csprites.js) ----------
cs = open('curios/csprites.js', encoding='utf8').read().strip()
assert cs.startswith('const CSPR={') and cs.endswith('};')
n = len(re.findall(r'const CSPR=\{.*?\};\n', src)); assert n == 1, n
src = re.sub(r'const CSPR=\{.*?\};\n', lambda m: cs + '\n', src, count=1)

# ---------- palette slots 24-28 for wards, and the ward pendant on the sprite ----------
rep("const CH={o:1,b:2,s:3,h:4,l:5,a:6,w:7,p:8,g:9,G:10,k:11,c:16,t:14,y:17,A:19,B:20,C:21,D:22,E:23};",
    "const CH={o:1,b:2,s:3,h:4,l:5,a:6,w:7,p:8,g:9,G:10,k:11,c:16,t:14,y:17,A:19,B:20,C:21,D:22,E:23,F:24,H:25,I:26,J:27,K:28};")
rep("  CHARM_COL.forEach((h,i)=>out[19+i]=hexRGB(h));\n",
    "  CHARM_COL.forEach((h,i)=>out[19+i]=hexRGB(h));WARD_COL.forEach((h,i)=>out[24+i]=hexRGB(h));\n")
rep("""    else if(/^charm[0-4]$/.test(S.keep)){const L='ABCDE'[+S.keep[5]],cy=mouthY+(dk?2:1);stamp(g,13,cy,['o....o','.o..o.','..oo..','.oXXo.','oXXXXo','oXyXXo','.oXXo.','..oo..'].map(r=>r.replace(/X/g,L)),false);}
""", """    else if(/^charm[0-4]$/.test(S.keep)){const L='ABCDE'[+S.keep[5]],cy=mouthY+(dk?2:1);stamp(g,13,cy,['o....o','.o..o.','..oo..','.oXXo.','oXXXXo','oXyXXo','.oXXo.','..oo..'].map(r=>r.replace(/X/g,L)),false);}
    else if(/^ward[0-4]$/.test(S.keep)){const L='FHIJK'[+S.keep[4]],cy=mouthY+(dk?2:1);stamp(g,13,cy,['o....o','.o..o.','..oo..','.oXXo.','oXXXXo','oXyyXo','oXXXXo','.oXXo.','..oo..'].map(r=>r.replace(/X/g,L)),false);}
""")

# ---------- one name per realm: bright on the front for everyone, Shade names on the back ----------
rep("function mapName(ti){if(!(ti>=0&&ti<=4))return 'somewhere';const m=mapState()[ti],mood=state.settings.mood,dk=mood==='dark'||(mood==='mix'&&whash(m.ti*7+m.tier)%2===0);return dk?THEMES[ti].dark.name:THEMES[ti].name;}",
    "/* 0.41: the front always shows the bright names; the Shade names live on the back of the map (realms 5-9). */\nfunction mapName(ti){if(!(ti>=0&&ti<=9))return 'somewhere';return ti>=5?THEMES[ti-5].dark.name:THEMES[ti].name;}")
rep("const m=ms[e.realm],dk=mood==='dark'||(mood==='mix'&&whash(m.ti*7+m.tier)%2===0),nm=m.tier>0?(dk?THEMES[m.ti].dark.name:THEMES[m.ti].name):'somewhere not yet drawn'",
    "const m=ms[e.realm],nm=m.tier>0?THEMES[m.ti].name:'somewhere not yet drawn'")
rep("  const dkOf=m=>mood==='dark'||(mood==='mix'&&whash(m.ti*7+m.tier)%2===0),nameOf=m=>dkOf(m)?THEMES[m.ti].dark.name:THEMES[m.ti].name;",
    "  const dkOf=m=>false,nameOf=m=>THEMES[m.ti].name;")

# ---------- the Shade data: curios, places, tales, realm lines ----------
rep("const wOut=()=>{const w=state&&state.wander;return !!(w&&Date.now()<w.ready);};",
"""/* ---- 0.41: the other side. Each bright realm ti has a Shade twin at ti+5 (Bramble, Inferno, Abyss, Wraith, Void),
   lit by the Crossing Lantern once ti is fully charted. Four curios each, wander-only. ---- */
const SCURIOS=[
 {id:'thorn',name:'Patient thorn',c:'{n} found a thorn that had been guarding something for a very long time, and offered to take a turn.',d:'{n} brings home a thorn and sets it pointing outward, toward the door.'},
 {id:'seed',name:'Sleeping seed',c:'{n} carried home a seed so gently it never woke up.',d:'{n} found a seed asleep in the dark and decided it could keep sleeping here.'},
 {id:'nest',name:'Kept nest',c:'{n} came back with a tidy little nest, just in case a bird needs it.',d:'{n} sets an empty nest by the fire, carefully, the way it was found.'},
 {id:'rosehip',name:'Wild rosehip',c:'{n} found a rosehip where the thorns had lain down, and is very proud.',d:'{n} returns with a red rosehip. Somewhere, a thorn stepped aside for it.'},
 {id:'cinder',name:'Banked cinder',c:'{n} brought home a cinder that is still warm, and keeps checking on it.',d:'{n} cups a cinder that has been burning since the first spark. It is not in a hurry.'},
 {id:'obsidian',name:'Black glass',c:'{n} found a piece of black glass so smooth it cannot stop rubbing it.',d:'{n} sets down a shard of black glass. Something heavy rested here once.'},
 {id:'ring',name:'Given ring',c:'{n} was handed an iron ring by someone kind, and wears it on its tail.',d:'{n} returns with an iron ring. It was given, not taken. It wants you to know.'},
 {id:'ash',name:'Pinch of warm ash',c:'{n} brought back a pinch of ash and insists it is the warmest thing ever.',d:'{n} brings ash, soft as flour. It says this is what heavy things look like when they are ready.'},
 {id:'bottle',name:'Corked bottle',c:'{n} found a bottle with a question inside and politely did not open it.',d:'{n} sets a corked bottle by the fire. The question inside is not yours. Yet.'},
 {id:'pearl',name:'Deep pearl',c:'{n} found a pearl that glows a little brighter when you wonder about things.',d:'{n} rises from the dark holding a pearl that hums with a question.'},
 {id:'anchor',name:'Little anchor',c:'{n} dragged home a little anchor and sat on it for a while, thinking.',d:'{n} drops a small anchor by the fire. It means: stay as long as you like.'},
 {id:'seaglass',name:'Sea glass',c:'{n} found two pieces of sea glass and gave you the nicer one.',d:'{n} returns with smooth sea glass. An answer, washed soft.'},
 {id:'mitten',name:'Kept mitten',c:'{n} found a mitten, still warm, and is looking for its pair.',d:'{n} brings a mitten the quiet kept warm. It fits nobody here, and that is fine.'},
 {id:'stillstone',name:'Still stone',c:'{n} brought home a smooth stone and sat very still beside it. It worked.',d:'{n} places a stone by the fire. The room gets a little quieter, in a good way.'},
 {id:'icicle',name:'Humming icicle',c:'{n} brought back an icicle that hums one very soft note.',d:'{n} carries an icicle that sings when the room goes quiet.'},
 {id:'snowglass',name:'Snow glass',c:'{n} found a little glass of snow. It sparkles, which means someone got found.',d:'{n} sets down a glass of snow, perfectly still. Everyone it waited for is home.'},
 {id:'letter',name:'Unsent letter',c:'{n} found a letter nobody sent and is keeping it safe, unopened.',d:'{n} returns with an unsent letter, creases smoothed. It will not read it, and neither should you.'},
 {id:'inkpot',name:'Patient ink',c:'{n} brought back a pot of ink that never dries, for words that come late.',d:'{n} sets down an inkpot. Something almost wrote itself on the way home.'},
 {id:'locket',name:'Closed locket',c:'{n} found a locket that will not open, and decided that is part of its charm.',d:'{n} wears a closed locket home. Inside is a word someone was brave enough to keep.'},
 {id:'mirror',name:'Side-lit mirror',c:'{n} found a small mirror and keeps holding it up so you can see yourself kindly.',d:'{n} props a dark mirror by the fire. It lights you from the side, the way a friend would.'}];
const ALLC=CURIOS.concat(SCURIOS),cuById=id=>ALLC.find(x=>x.id===id);
const SREALM_TXT=['The other side of Meadow. Every thorn faces outward, and everything inside them is being kept for someone.',
 'The other side of Ember. Warm, low and patient. The heavy things people set down are held here, never burned.',
 'The other side of Tide. Deep, calm water full of soft lights, each one a question still waiting for its asker.',
 'The other side of Frost. A whiteout that hums. The quiet here has learned to sit beside you.',
 'The other side of Dusk. Not empty. Full of things almost ready to be said, kept safe and kept company.'];
PLACES.push(
 [{n:'Thornkeep Gate',k:'zig',x:'Where you cross over. The thorns lean aside for a lantern, and only for a lantern.'},
  {n:'The Sleeping Bed',k:'hill',x:'Seeds asleep under the moss. Walk softly; nothing here likes to be hurried.'},
  {n:'Nest Row',k:'tree',x:'Empty nests, kept tidy, one for every bird that might come back.'},
  {n:'The Waiting Rose',k:'star',x:'A rose that opens only when someone returns for something they left.'},
  {n:'Fernlow’s Other Seat',k:'stone',x:'The back of Fernlow’s stone. On this side it is always a little later in the day.'}],
 [{n:'Cinderfall',k:'star',x:'Where the other half of the first spark landed. Banked, never out.'},
  {n:'The Long Shelf',k:'cave',x:'Rows of heavy things, held for the people who will come back for them.'},
  {n:'Glassway',k:'gem',x:'A road of black glass, smooth from everything that rested here.'},
  {n:'The Ring Tree',k:'tree',x:'An iron tree hung with rings, each one waiting to be given away.'},
  {n:'Ashlight Rest',k:'hill',x:'A soft hill of warm ash. Guardians nap here between holdings.'}],
 [{n:'The Sinking Stair',k:'zig',x:'Steps down into calm dark water. Your lantern lights three at a time, which is enough.'},
  {n:'Bottle Shoal',k:'dots',x:'Unopened bottles bob here, each holding a question waiting for its asker.'},
  {n:'Pearl Hollow',k:'pool',x:'A pool where the brightest questions rest. The water glows faintly blue.'},
  {n:'Anchor Bend',k:'arch',x:'Where the guardians drop an anchor beside anyone who comes down to think.'},
  {n:'The Rising',k:'tower',x:'A column of light where answered questions float up toward Tide.'}],
 [{n:'The Whiteout Door',k:'arch',x:'Where the snow opens for a lantern and closes, gently, behind you.'},
  {n:'Mitten Hollow',k:'cave',x:'Lost mittens, kept warm and paired up whenever a match turns up.'},
  {n:'The Humming Eaves',k:'bell',x:'Icicles along a ridge, each one holding a single quiet note.'},
  {n:'Stillstone',k:'stone',x:'Sit here and the snow waits for you to finish your thought.'},
  {n:'The Found Light',k:'house',x:'A small hut whose window stays lit until every traveller is home.'}],
 [{n:'The Low Door',k:'house',x:'The workshop’s other door, around the back, at the foot of the stair.'},
  {n:'The Letter Vaults',k:'cave',x:'Every letter nobody sent, smoothed, filed and kept.'},
  {n:'Inkwell Spring',k:'pool',x:'Ink that never dries, for the words that come late.'},
  {n:'The Keeper’s Post',k:'tower',x:'A guardian keeps watch here. Mostly it watches for you to feel better.'},
  {n:'The Side-Lit Mirror',k:'star',x:'A small dark mirror that shows you the way a friend would.'}]);
TALES.push(
 {t:'The Keepers of the Edge',p:[
  ['thorn','From the other side, Bramble was never wild. It was a promise. When the Meadow Forgeling sat down to wait beside its acorn, the brambles grew up around it, thorns outward, so nothing would hurry it.'],
  ['seed','Some seeds fell where nobody would think to look. Bramble picked each one up and kept it in the dark, asleep, until the ground was ready. It never once asked a seed to hurry.'],
  ['nest','Birds that left the hill left their nests behind. Bramble kept every nest in its branches, empty and tidy, so that coming back would always be easy.'],
  ['rosehip','When someone finally came back for what they had left, Bramble let its thorns lie down. Where they lay, wild roses came up, red as a welcome.']],
  end:'Bramble still keeps the edge. It is not waiting for you to fail. It is keeping your place.'},
 {t:'What Inferno Holds',p:[
  ['cinder','Inferno remembers the first spark too. When it leapt, one cinder fell the other way, down into the dark, and stayed lit. The guardians banked it in ash so it would last. It is the oldest promise in the Forge.'],
  ['obsidian','People brought their heavy things down to the Holding Stone. The guardians did not ask what they were. Where a heavy thing rested long enough, the rock around it turned to black glass, smooth as a held breath.'],
  ['ring','One guardian wore an iron ring for every thing it held. When the thing was taken back, it gave the ring away. It has given away far more rings than it has ever worn.'],
  ['ash','Nothing in Inferno is burned up. It is only burned down, small enough to carry. That is what the ash is: heavy things made light enough for you to pick up again.']],
  end:'Inferno is not angry. It is warm, and patient, and it will hand you back what is yours whenever you ask.'},
 {t:'The Questions Deep',p:[
  ['bottle','Every question nobody asked out loud sank into the Abyss in a little bottle. The guardians caught them gently, one by one, and never opened a single one. A question belongs to whoever is going to ask it.'],
  ['pearl','Around each question, the deep water laid down light, layer on layer, the way a pearl grows. The longer a question waited, the brighter it got. Nothing down there stays dark for long.'],
  ['anchor','The guardians drop an anchor beside anyone who comes down to sit with their questions. It is not to keep them there. It is so they do not drift while they think.'],
  ['seaglass','When a question is finally asked, its bottle rises, breaks on the shore at Tide, and the pieces wash smooth. Tide calls it sea glass. The Abyss calls it a good day.']],
  end:'The Abyss is not deep because it is hiding something. It is deep so there is room for every question you have not asked yet.'},
 {t:'The Shape of the Quiet',p:[
  ['mitten','Wraith began as the quiet left over after Bell Peak rang. Someone dropped a mitten in the snow that day. The quiet picked it up and kept it warm, because it did not know yet what else to do.'],
  ['stillstone','The quiet sat very still for a long time, until it was heavy enough to be a stone. Travellers who rest on it say the snow stops falling for exactly as long as they need.'],
  ['icicle','It learned to hum from the icicles. Each one holds a single note, and when the wind is gentle the whole whiteout sings very softly, so nobody walks in silence.'],
  ['snowglass','The guardians keep a glass full of snow instead of sand. It runs only while someone is lost. When they are found it stops, and the snow inside begins to sparkle.']],
  end:'Wraith is still quiet. It is the quiet of someone who came to sit with you and did not need to say why.'},
 {t:'The Unsent Letters',p:[
  ['letter','Down in the Void, the guardians keep every letter nobody sent. They do not read them. They smooth the creases and file them by how brave they were to write.'],
  ['inkpot','Some letters were never even written. For those, the guardians keep a pot of ink that never dries, in case the words come late. They often do.'],
  ['locket','One guardian wears a locket that will not open. Inside is a word it was once afraid to say. It wears it so whoever comes down here knows they are not the only one.'],
  ['mirror','At the foot of the Red Thread Stair hangs a small dark mirror. It shows you exactly as you are, only lit from the side, the way a friend would see you. Most people stand there a while before climbing home.']],
  end:'The Void is not empty. It is full of things that are almost ready to be said, kept safe, and kept company.'});
const wOut=()=>{const w=state&&state.wander;return !!(w&&Date.now()<w.ready);};""")

# ---------- tales: ten tales, the Shade five shown once the lantern is made ----------
rep("const taleOf=id=>{for(let ti=0;ti<5;ti++){", "const taleOf=id=>{for(let ti=0;ti<TALES.length;ti++){")
rep("""function oldTalesHTML(){
  if(!loreOn())return '';
  const any=Object.keys(state.curios).length;
  return `<h2 style="margin-top:4px">Old tales of the realms</h2><p class="muted small">Every realm forgot a tale. Each of its four curios remembers one page. Wander a realm to bring its pages home.${any?'':' Your first wander starts at the Hearth.'}</p>`+
   TALES.map((T,ti)=>{const n=talePages(ti),R=mapName(ti);
    return""", """function oldTalesHTML(){
  if(!loreOn())return '';
  const any=Object.keys(state.curios).length;
  const shade=hasLantern()?`<h2 style="margin-top:18px">Tales from the other side</h2><p class="muted small">Each Shade realm keeps its own side of the story, and its four curios remember the pages. Cross with your lantern to bring them home.</p>`+[5,6,7,8,9].map(si=>{const n=talePages(si),T=TALES[si],R=mapName(si),b=THEMES[si-5].name;
    if(!shadeOpen(si)&&!n)return `<div class="otale"><h3>Across from ${b}: an untold tale</h3><p class="muted small" style="margin:0">Chart ${b} fully on the front, and your lantern will light the way across.</p></div>`;
    return taleBlock(si);}).join(''):'';
  return `<h2 style="margin-top:4px">Old tales of the realms</h2><p class="muted small">Every realm forgot a tale. Each of its four curios remembers one page. Wander a realm to bring its pages home.${any?'':' Your first wander starts at the Hearth.'}</p>`+
   [0,1,2,3,4].map(taleBlock).join('')+shade;
}
function taleBlock(ti){
  const any=Object.keys(state.curios).length,T=TALES[ti];
  {const n=talePages(ti),R=mapName(ti);
    return""")
rep("""<p class="muted small" style="margin:0">${any?`No pages yet. Send a Forgeling to wander in ${R}.`:'No pages yet.'}</p>`}</div>`;}).join('');
}""", """<p class="muted small" style="margin:0">${any?`No pages yet. Send a Forgeling to wander in ${R}.`:'No pages yet.'}</p>`}</div>`;}
}""")

# ---------- places, map polygons, the back of the map ----------
rep("const placesFound=ti=>rKnownTi(ti)?Math.min(5,1+((state.explore&&state.explore[ti])||0)):0;",
"""const placesFound=ti=>(ti>=5?shadeOpen(ti):rKnownTi(ti))?Math.min(5,1+((state.explore&&state.explore[ti])||0)):0;
/* 0.41: a Shade realm opens once the lantern is made and its bright twin is fully charted. All derived, nothing stored. */
const hasLantern=()=>!!(state&&state.forge&&state.forge.made.includes('xlantern'));
const shadeOpen=si=>si>=5&&si<=9&&hasLantern()&&placesFound(si-5)===5;
const shadeOpenList=()=>[5,6,7,8,9].filter(shadeOpen);
const rReach=t=>t>=5?shadeOpen(t):rKnownTi(t);""")
rep("let mapPreview=null;", "let mapPreview=null;\n/* The back of the sheet: the same outlines seen through the paper, mirrored. */\nconst SMAPP=MAPP.map(P=>P.map(([x,y])=>[340-x,y])),polyOf=ti=>ti>=5?SMAPP[ti-5]:MAPP[ti];")
rep("const P=MAPP[ti]", "const P=polyOf(ti)", 4)
rep("glyphPts(ti,MAXG[ti])", "glyphPts(ti,MAXG[ti%5])", 2)
rep("function glyphD(ti,x,y){\n", "function glyphD(ti,x,y){\n  ti%=5;\n")
rep("const A=MAPP[a],B=MAPP[b]", "const A=polyOf(a),B=polyOf(b)")
rep("""function seaPts(){
  if(SEA)return SEA;const out=[];""", """function seaPts(back){
  const K=back?'b':'f';if(SEA&&SEA[K])return SEA[K];const out=[],PS=back?SMAPP:MAPP;""")
rep("    if(MAPP.every(P=>polyD(x,y,P)>13)&&!(x>282&&y<52))out.push([x,y,h%3]);\n  }\n  return SEA=out;",
    "    if(PS.every(P=>polyD(x,y,P)>13)&&!(x>282&&y<52))out.push([x,y,h%3]);\n  }\n  return (SEA||(SEA={}))[K]=out;")
rep("${['','One place drawn in so far.','A few places drawn in.','A few places drawn in.','Most of it drawn in.','Fully charted.'][pf]}</p>",
    "${['','One place drawn in so far.','A few places drawn in.','A few places drawn in.','Most of it drawn in.','Fully charted.'][pf]}${pf===5&&hasLantern()?' Its twin is lit on the back.':''}</p>")
rep("  return `<div class=\"mapwrap\">${svg}</div>${sp||",
    "  return `${turnHTML()}<div class=\"mapwrap\">${svg}</div>${sp||")
rep("/* ---- The Quiet Thing: something by the fire grows only while you are away ---- */",
r"""/* ---- 0.41: turning the map over. The back is the same sheet in night ink, mirrored, lit realm by realm. ---- */
function turnHTML(){
  if(!hasLantern())return '';
  return `<div class="mapturn"><button class="outline" id="mapTurn" aria-pressed="${ch.side?'true':'false'}">${ch.side?'Turn back to the front':'Turn the map over'}</button></div>`;
}
const BACK_NOTES=['','Lit by your lantern. One place drawn in so far.','A few places drawn in.','A few places drawn in.','Most of it drawn in.','Fully charted, by lantern light.'];
function mapBackHTML(){
  const E=eraAt(dnum(todayKey())),era=ERAS[E.mood];
  const ms=[5,6,7,8,9].map(si=>{const pf=placesFound(si);return {ti:si,b:si-5,pf,tier:pf===0?0:pf>=5?3:pf>=2?2:1};});
  let g='';
  ms.forEach(m=>{
    const ti=m.ti,T=THEMES[m.b],acc=T.dark.glow,P=polyOf(ti),L=mapMid(P),d=blobPath(P,ti+1,[3.4,2.3,1.3,.5][m.tier]);
    if(m.tier===0){g+=fogSVG(ti)+`<path d="${d}" class="mp-faint" fill="none" stroke-width="1" pathLength="100" stroke-dasharray="20 80" stroke-dashoffset="${-(whash(ti*53+9)%100)}" filter="url(#mpBlur)"/><text x="${r1(L[0])}" y="${r1(L[1]+5)}" text-anchor="middle" class="mp-faint2" font-size="15">?</text>`;return;}
    g+=`<path d="${d}" fill="${acc}" fill-opacity="${[0,.16,.26,.36][m.tier]}" stroke="none" filter="url(#mpWash)"/><path d="${d}" fill="none" class="mp-bleed" stroke="${acc}" stroke-opacity="${[0,.4,.55,.7][m.tier]}" stroke-width="5" filter="url(#mpBleed)"/>`;
    g+=`<path d="${d}" fill="none" class="mp-st" stroke-width="${[0,1.1,1.5,1.9][m.tier]}" stroke-dasharray="${m.tier===1?'5 4':'none'}" stroke-opacity="${[0,.55,.8,1][m.tier]}" filter="url(#mpInk)"/>`;
    const gl=glyphPts(ti,Math.min([0,2,5,9][m.tier],MAXG[m.b]));
    if(gl.length)g+=`<path class="mp-st" fill="none" stroke-width="1.1" stroke-opacity="${m.tier===1?.5:.75}" d="${gl.map(p=>glyphD(m.b,p[0],p[1])).join('')}"/>`;
    g+=placesSVG(ti);
    g+=`<text x="${r1(L[0])}" y="${r1(L[1]+4)}" text-anchor="middle" class="${m.tier===1?'mp-mut':'mp-txt'}" font-size="13" letter-spacing="1"${m.tier===3?' font-weight="700"':''}>${esc(T.dark.name)}</text>`;
    if(m.pf===5)g+=`<path class="mp-gold" fill="none" stroke-width="1.6" d="M${r1(L[0]-15)} ${r1(L[1]+10)}Q${r1(L[0])} ${r1(L[1]+14)} ${r1(L[0]+15)} ${r1(L[1]+10)}"/><path class="mp-gold" fill="#E2B04A" stroke-width="1" d="M${r1(L[0])} ${r1(L[1]+9)}l3 3l-3 3l-3 -3z"/>`;
  });
  const sea=`<path class="mp-st" fill="none" stroke-width="1" stroke-opacity=".3" d="${seaPts(true).map(([x,y,k])=>waveD(x,y,k)).join('')}"/>`;
  const trails=TRAILS.filter(([a,b])=>ms[a].tier>0&&ms[b].tier>0).map(([a,b])=>`<path class="mp-st" fill="none" stroke-width="1.2" stroke-dasharray="0.1 4.2" stroke-opacity=".75" d="${trailD(a+5,b+5)}"/>`).join('');
  g=sea+trails+g;
  ms.forEach(m=>{
    const d=blobPath(polyOf(m.ti),m.ti+1,[3.4,2.3,1.3,.5][m.tier]),sel=ch.realm===m.ti;
    if(sel)g+=`<g class="mp-selg" aria-hidden="true"><path d="${d}" class="mp-selglow" fill="none" stroke-width="7" stroke-linejoin="round" filter="url(#mpGlow)"/><path d="${d}" class="mp-gold mp-sel" fill="none" stroke-width="2.2" stroke-linejoin="round" filter="url(#mpInk)"/></g>`;
    g+=`<path d="${d}" class="mphit" data-realm="${m.ti}" role="button" tabindex="0" aria-pressed="${sel}" aria-label="${m.tier>0?esc(THEMES[m.b].dark.name):'A dark corner across from '+THEMES[m.b].name}, ${sel?'close its page':'open its page'}" fill="transparent" stroke="none"/>`;
  });
  const lit=ms.filter(m=>m.tier>0),allC=ms.every(m=>m.pf===5);
  const foot=allC?'Both sides of the Forge, fully charted.':lit.length===5?'Every Shade realm is lit. Some are still faint.':'Lantern light reaches the realms you have charted.';
  const aria='The back of the map, in night ink. Shade realms your lantern has lit are drawn in, and the rest are dark. '+foot;
  const svg=`<svg class="mapsvg" viewBox="0 0 340 430" role="group" aria-label="${esc(aria)}">
    <defs><filter id="mpBlur" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="1"/></filter><filter id="mpGlow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.6"/></filter>
      <filter id="mpInk" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".045" numOctaves="2" seed="7" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="2.6" xChannelSelector="R" yChannelSelector="G"/></filter>
      <filter id="mpWash" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="3" seed="13" result="t"/><feColorMatrix in="t" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.1 1.38" result="m"/><feComposite in="SourceGraphic" in2="m" operator="in"/></filter>
      <filter id="mpBleed" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="1.6"/></filter>
      <filter id="mpFog" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="5"/></filter>
      <filter id="mpGrain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="1" seed="5" result="g"/><feColorMatrix in="g" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.4 1.25" result="a"/><feComposite in="SourceGraphic" in2="a" operator="in"/></filter>
      <radialGradient id="mpEdge" cx="50%" cy="48%" r="72%"><stop offset=".55" stop-opacity="0" class="mp-burn"/><stop offset="1" class="mp-burn"/></radialGradient></defs>
    <rect x="0" y="0" width="340" height="430" rx="16" class="mp-paper"/>
    <rect x="0" y="0" width="340" height="430" rx="16" class="mp-grain" opacity=".07" filter="url(#mpGrain)"/>
    <rect x="0" y="0" width="340" height="430" rx="16" fill="url(#mpEdge)"/>
    <rect x="5" y="5" width="330" height="420" rx="11" class="mp-st" fill="none" stroke-width="1.3" stroke-opacity=".45"/>
    <rect x="10" y="10" width="320" height="410" rx="7" class="mp-st" fill="none" stroke-width=".7" stroke-opacity=".28"/>
    <path class="mp-st" fill="none" stroke-width=".9" stroke-opacity=".4" d="M10 22q8 0 12 -12M330 22q-8 0 -12 -12M10 408q8 0 12 12M330 408q-8 0 -12 12"/>
    <path class="mp-rib" d="M12 14h214l-8 14l8 14h-214l8 -14z" opacity=".95"/><path class="mp-st" fill="none" stroke-width=".8" stroke-opacity=".4" d="M12 14h214l-8 14l8 14h-214l8 -14z"/>
    <text x="24" y="27" class="mp-txt" font-size="13.5">The other side, by lantern light</text>
    <text x="24" y="39" class="mp-mut" font-size="10">Turned over in the ${esc(era.n)}</text>
    <g transform="translate(305 34)"><circle r="15" class="mp-st" fill="none" stroke-width=".7" stroke-opacity=".45"/><path class="mp-lamp" d="M-4 -9h8v2h-8zM-5 -7h10v12h-10zM-3 5h6v2h-6z" fill-opacity=".9"/><path d="M-3 -5h6v8h-6z" fill="#FFF6CF"/><path class="mp-st" fill="none" stroke-width=".8" d="M-2 -9q2 -5 4 0"/></g>
    <g transform="translate(0 8)">${g}</g>
    <text x="170" y="414" text-anchor="middle" class="mp-mut" font-size="11">${esc(foot)}</text></svg>`;
  let notes=lit.map(m=>`<p class="small"><b>${esc(THEMES[m.b].dark.name)}.</b> ${BACK_NOTES[m.pf]}</p>`).join('');
  if(lit.length<5)notes+='<p class="muted small">The rest of the back is dark. Chart a realm fully on the front, and its twin lights up here.</p>';
  const sp=ch.realm!=null&&ch.realm>=5?`<div class="realmpage" aria-live="polite">${shadePageHTML(ch.realm)}</div>`:'';
  return `${turnHTML()}<div class="mapwrap mback">${svg}</div>${sp||'<p class="muted small center" style="margin:-4px 0 10px">Tap a lit corner to open its page.</p>'}<div class="mapcap parch">${notes}</div>`;
}
function shadePageHTML(si){
  const b=si-5,T=THEMES[b];
  if(!shadeOpen(si))return `<div class="realm locked" style="--rc:var(--line)"><div><b>Dark paper</b></div><p class="muted">Chart ${T.name} fully on the front, and your lantern will light this side.</p></div>`;
  let out=`<div class="realm" style="--rc:${T.dark.accent}"><div><b>${T.dark.name}</b><span class="tag">The other side of ${T.name}</span></div><p class="world">${esc(SREALM_TXT[b])}</p></div><div class="parch realmnotes">`;
  const hc=slotCards(),hw=hc[Math.min(hf.sel,hc.length-1)],wc0=wCard();
  out+=hw?(state.wander&&wc0?`<p class="muted small" style="margin:8px 0 0">${esc(wc0.nick||wc0.name)} is out wandering${state.wander.realm>=0?' in '+esc(rName(state.wander.realm)):''}.</p>`:state.hearth.sleep?'':`<button class="primary" data-wto="${si}">Send ${esc(hw.nick||hw.name)} across to wander here</button>`):'';
  out+=placesListHTML(si);
  if(loreOn()){const tp=talePages(si);out+=`<p class="muted small" style="margin:6px 0 0">Shade tale: ${TALES[si].t}. ${tp===4?'The tale is whole.':tp+' of 4 pages found.'}</p>`;}
  return out+'</div>';
}

/* ---- The Quiet Thing: something by the fire grows only while you are away ---- */""")
rep("return `<p class=\"muted small\" style=\"margin:8px 0 0\">Places on the map${n===5?'. Fully charted.':''}</p>",
    "return `<p class=\"muted small\" style=\"margin:8px 0 0\">Places on ${ti>=5?'the back of ':''}the map${n===5?'. Fully charted.':''}</p>")
rep("const cu=CURIOS.find(x=>x.id===id);return state.curios[id]", "const cu=cuById(id);return state.curios[id]")
rep("function realmPageHTML(ti){\n", "function realmPageHTML(ti){\n  if(ti>=5)return shadePageHTML(ti);\n")
rep("let ch={sub:'map',more:1,realm:null};", "let ch={sub:'map',more:1,realm:null,side:0};")
rep("ch.sub==='journal'?journeyHTML()+journalHTML():mapHTML();", "ch.sub==='journal'?journeyHTML()+journalHTML():(ch.side&&hasLantern()?mapBackHTML():mapHTML());")
rep("""  if(e.target.closest('#bookRibbon')){openRibbon();return;}
  const rh=e.target.closest('.mphit');""", """  if(e.target.closest('#bookRibbon')){openRibbon();return;}
  if(e.target.closest('#mapTurn')){ch.side=ch.side?0:1;ch.realm=null;sfx('select');renderChronicle();const t=document.getElementById('mapTurn');if(t)t.focus({preventScroll:true});return;}
  const rh=e.target.closest('.mphit');""")

# ---------- CSS: the back of the map, the turn button, the shelf's other side ----------
rep(".mapcap p{margin:6px 0}", """.mapcap p{margin:6px 0}
/* 0.41: the back of the map, in night ink, whatever the appearance */
.mapwrap.mback,html.ls .mapwrap.mback{--mpaper:#141030;--mburn:rgba(0,0,0,.55);--mfog:#2A2350;--mgrain:#FFFFFF;--mrib:#241D48;--mbleed:.55;--ink:#EDE6FF;--muted:#B9AEE0;--plum:#FFD36B;background:#141030;border-color:#3A2F6A;color:#EDE6FF}
.mp-lamp{fill:#FFD36B}
.mapturn{display:flex;justify-content:center;margin:0 0 10px}.mapturn button{min-height:44px;padding:0 18px}
.shelf .sside{display:block;margin:14px 0 4px;font-weight:700}""")

# ---------- curios everywhere: lookups, counts, sanitizing ----------
rep("if(c.firstFind&&(!CURIOS.some(x=>x.id===c.firstFind.id)", "if(c.firstFind&&(!ALLC.some(x=>x.id===c.firstFind.id)")
rep("typeof s.hearth.curio==='string'&&CURIOS.some(x=>x.id===s.hearth.curio)", "typeof s.hearth.curio==='string'&&ALLC.some(x=>x.id===s.hearth.curio)")
rep("const ok=new Set(CURIOS.map(x=>x.id));Object.keys(s.curios)", "const ok=new Set(ALLC.map(x=>x.id));Object.keys(s.curios)")
rep("[0,1,2,3,4].forEach(t=>{const v=e[t];if(Number.isFinite(v)&&v>0)ok[t]=Math.min(4,Math.round(v));});s.explore=ok;",
    "[0,1,2,3,4,5,6,7,8,9].forEach(t=>{const v=e[t];if(Number.isFinite(v)&&v>0)ok[t]=Math.min(4,Math.round(v));});s.explore=ok;")
rep("if(s.wander)s.wander.realm=Number.isInteger(s.wander.realm)&&s.wander.realm>=0&&s.wander.realm<=4?s.wander.realm:-1;",
    "if(s.wander)s.wander.realm=Number.isInteger(s.wander.realm)&&s.wander.realm>=0&&s.wander.realm<=9?s.wander.realm:-1;")
rep("const n=c.nick||c.name,cu=c.firstFind&&CURIOS.find(x=>x.id===c.firstFind.id);", "const n=c.nick||c.name,cu=c.firstFind&&cuById(c.firstFind.id);")
rep("const cu=c.firstFind&&CURIOS.find(x=>x.id===c.firstFind.id);", "const cu=c.firstFind&&cuById(c.firstFind.id);")
rep("const cu=CURIOS.find(x=>x.id===b.dataset.id);closeModal();hf.msg=", "const cu=cuById(b.dataset.id);closeModal();hf.msg=")
rep("const ks=rKnown();if(!ks.length){toast('Find a Forgeling first.');return;}CURIOS.filter(x=>ks.includes(CREALM[x.id]))",
    "const ks=rKnown();if(!ks.length){toast('Find a Forgeling first.');return;}ALLC.filter(x=>rReach(CREALM[x.id]))")
rep("""const cu=CURIOS.find(x=>x.id===g.c),isNew=!state.curios[cu.id];""", """const cu=cuById(g.c),isNew=!state.curios[cu.id];""")
rep("You had one already. Now you have a spare, from '+esc(g.n)+'.'} Curios found: ${have} of ${CURIOS.length}.</p>",
    "You had one already. Now you have a spare, from '+esc(g.n)+'.'} Curios found: ${haveN()} of ${shelfSet().length}.</p>")

# ---------- the shelf ----------
rep("""function shelfHTML(){
  return `<div class="shelf">${[0,1,2,3,4].map(ti=>{const known=rKnownTi(ti);
    return `<div class="srow"><span class="slab">${known?esc(mapName(ti)):'A realm not yet on your map'}</span>""",
"""const shelfSet=()=>hasLantern()?ALLC:CURIOS,haveN=()=>shelfSet().filter(x=>state.curios[x.id]).length;
function shelfHTML(){
  return `<div class="shelf">${[0,1,2,3,4].concat(hasLantern()?[5,6,7,8,9]:[]).map(ti=>{const known=rReach(ti);
    return `${ti===5?'<span class="slab sside">The other side</span>':''}<div class="srow"><span class="slab">${known?esc(mapName(ti)):ti>=5?'Across from '+THEMES[ti-5].name+', not crossed yet':'A realm not yet on your map'}</span>""")
rep("""  const cu=CURIOS.find(x=>x.id===id);if(!cu)return;const rec=state.curios[id],ti=CREALM[id];
  if(!rec){openSheet(`<div class="cbig">${cImg(id,96,{sil:1})}</div><h2 class="center">Not found yet</h2>
    <p class="muted center">${rKnownTi(ti)?`It is somewhere in ${esc(mapName(ti))}. Send a Forgeling to wander there.`:'It is somewhere you have not been yet. Your map will show the way when a Forgeling from there finds you.'}</p>""",
"""  const cu=cuById(id);if(!cu)return;const rec=state.curios[id],ti=CREALM[id];
  if(!rec){openSheet(`<div class="cbig">${cImg(id,96,{sil:1})}</div><h2 class="center">Not found yet</h2>
    <p class="muted center">${rReach(ti)?`It is somewhere in ${esc(mapName(ti))}. Send a Forgeling to wander there.`:ti>=5?`It is on the other side, across from ${esc(THEMES[ti-5].name)}. Chart ${esc(THEMES[ti-5].name)} fully, and your lantern will light the way.`:'It is somewhere you have not been yet. Your map will show the way when a Forgeling from there finds you.'}</p>""")
rep("const w=state.wander,wc=wCard(),wn=wc?esc(wc.nick||wc.name):'',have=Object.keys(state.curios).length;",
    "const w=state.wander,wc=wCard(),wn=wc?esc(wc.nick||wc.name):'',have=haveN();")
rep("<summary>Curio shelf, ${have} of ${CURIOS.length}</summary>", "<summary>Curio shelf, ${have} of ${shelfSet().length}</summary>")

# ---------- wandering: Shade realms as destinations, Shade finds and places ----------
rep("const to=Number.isInteger(realm)&&realm>=0&&realm<=4?realm:-1;", "const to=Number.isInteger(realm)&&realm>=0&&realm<=9&&rReach(realm)?realm:-1;")
rep("hf.msg=to>=0?`${c.nick||c.name} heads off toward ${rName(to)}.`", "hf.msg=to>=5?`${c.nick||c.name} takes the lantern and crosses over to ${rName(to)}.`:to>=0?`${c.nick||c.name} heads off toward ${rName(to)}.`")
rep("const fresh=state.disc!==todayKey(),to=Number.isInteger(w.realm)&&w.realm>=0?w.realm:-1,base=to>=0?rCurios(to):CURIOS,unfound=fresh?base.filter(x=>!state.curios[x.id]):[],owned=base.filter(x=>state.curios[x.id]),anyOwned=CURIOS.filter(x=>state.curios[x.id]);",
    "const fresh=state.disc!==todayKey(),to=Number.isInteger(w.realm)&&w.realm>=0?w.realm:-1,base=to>=0?rCurios(to):CURIOS.concat(...shadeOpenList().map(rCurios)),unfound=fresh?base.filter(x=>!state.curios[x.id]):[],owned=base.filter(x=>state.curios[x.id]),anyOwned=ALLC.filter(x=>state.curios[x.id]);")
rep("let place='';if(fresh){const open=[0,1,2,3,4].filter(t=>rKnownTi(t)&&placesFound(t)<5)",
    "let place='';if(fresh){const open=[0,1,2,3,4,5,6,7,8,9].filter(t=>rReach(t)&&placesFound(t)<5)")
rep("place=`<div class=\"tale new\"><b>A new place on your map: ${esc(pl.n)}</b><p class=\"world\">${esc(pl.x)}</p><p class=\"small\">${pf===5?`That is the last place in ${esc(mapName(dto))}. The realm is fully charted.`:`Another place is drawn on your map of ${esc(mapName(dto))}.`} See it on the Map tab.</p></div>`;",
    "place=`<div class=\"tale new\"><b>A new place on ${dto>=5?'the back of ':''}your map: ${esc(pl.n)}</b><p class=\"world\">${esc(pl.x)}</p><p class=\"small\">${pf===5?`That is the last place in ${esc(mapName(dto))}. The realm is fully charted.${dto<5?(hasLantern()?` Its Shade twin, ${esc(mapName(dto+5))}, is lit on the back of the map.`:' A lantern from the Forge could show you its other side.'):''}`:`Another place is drawn on your map of ${esc(mapName(dto))}.`} See it on the Map tab${dto>=5?', turned over':''}.</p></div>`;")
rep("more=CURIOS.some(x=>!state.curios[x.id])||[0,1,2,3,4].some(t=>rKnownTi(t)&&placesFound(t)<5)",
    "more=shelfSet().some(x=>!state.curios[x.id]&&(CREALM[x.id]<5||rReach(CREALM[x.id])))||[0,1,2,3,4,5,6,7,8,9].some(t=>rReach(t)&&placesFound(t)<5)")
rep("const nm=c?(c.nick||c.name):'Your Forgeling',line=(c&&c.dark?cu.d:cu.c).replace(/\\{n\\}/g,nm),have=Object.keys(state.curios).length;\n  const head=(to>=0?'Back from '+rName(to)+'. ':'')+(isNew?(have===CURIOS.length?",
    "const nm=c?(c.nick||c.name):'Your Forgeling',line=(c&&c.dark?cu.d:cu.c).replace(/\\{n\\}/g,nm),have=haveN();\n  const head=(to>=0?'Back from '+rName(to)+'. ':'')+(isNew?(have===shelfSet().length?")
rep("<p class=\"muted small center\">Curios found: ${have} of ${CURIOS.length}</p>${place}", "<p class=\"muted small center\">Curios found: ${have} of ${shelfSet().length}</p>${place}")
rep("const CREALM={acorn:0,flower:0,feather:0,mushroom:0,leaf:1,spark:1,bone:1,crystal:1,shell:2,pebble:2,rain:2,coin:2,snow:3,moon:3,bell:3,glimmer:3,key:4,candle:4,thread:4,map:4};",
    "const CREALM={acorn:0,flower:0,feather:0,mushroom:0,leaf:1,spark:1,bone:1,crystal:1,shell:2,pebble:2,rain:2,coin:2,snow:3,moon:3,bell:3,glimmer:3,key:4,candle:4,thread:4,map:4,\n thorn:5,seed:5,nest:5,rosehip:5,cinder:6,obsidian:6,ring:6,ash:6,bottle:7,pearl:7,anchor:7,seaglass:7,mitten:8,stillstone:8,icicle:8,snowglass:8,letter:9,inkpot:9,locket:9,mirror:9};")
rep("const rCurios=ti=>CURIOS.filter(x=>CREALM[x.id]===ti);", "const rCurios=ti=>ALLC.filter(x=>CREALM[x.id]===ti);")
rep("""    return `<button class="moodbtn" data-wgo="${ti}">${iconSVG(REALMI[ti])}<div><b>${esc(rName(ti))}</b><span>${f} of ${all.length} curios from here found${asked?`. ${esc(ra.nick||ra.name)} asked for something from here.`:'.'}${fgState().comp===todayKey()&&fgState().compTo===ti?' The compass points here.':''}</span></div></button>`;}).join('');""",
"""    return `<button class="moodbtn" data-wgo="${ti}">${iconSVG(REALMI[ti])}<div><b>${esc(rName(ti))}</b><span>${f} of ${all.length} curios from here found${asked?`. ${esc(ra.nick||ra.name)} asked for something from here.`:'.'}${fgState().comp===todayKey()&&fgState().compTo===ti?' The compass points here.':''}</span></div></button>`;}).join('')
   +(shadeOpenList().length?'<p class="muted small" style="margin:12px 0 4px">On the other side, by lantern</p>'+shadeOpenList().map(si=>{const all=rCurios(si),f=all.filter(x=>state.curios[x.id]).length,home=c.dark&&c.theme===si-5;
    return `<button class="moodbtn" data-wgo="${si}">${iconSVG([REALMI[si-5][0],THEMES[si-5].dark.glow])}<div><b>${esc(rName(si))}${home?' · Home':''}</b><span>${home?esc(n)+' was born on this side. ':''}${f} of ${all.length} curios from here found.${fgState().comp===todayKey()&&fgState().compTo===si?' The compass points here.':''}</span></div></button>`;}).join(''):'');""")
rep("const open=[0,1,2,3,4].filter(t=>rKnownTi(t)&&(rCurios(t).some(x=>!state.curios[x.id])||placesFound(t)<5));f.comp=todayKey();",
    "const open=[0,1,2,3,4,5,6,7,8,9].filter(t=>rReach(t)&&(rCurios(t).some(x=>!state.curios[x.id])||placesFound(t)<5));f.comp=todayKey();")

# ---------- the Forge: the Crossing Lantern and five wards ----------
rep(" {id:'chimes',kind:'Hearth',name:'Wind chimes',sp:2,emb:2,what:'Hang by the fire for good.'}];",
""" {id:'chimes',kind:'Hearth',name:'Wind chimes',sp:2,emb:2,what:'Hang by the fire for good.'},
 {id:'xlantern',kind:'Tool',name:'Crossing Lantern',multi:3,sp:3,emb:6,what:'Lights the other side of any fully charted realm. Turn the map over to see it.'},
 {id:'ward0',kind:'Keepsake',name:'Ward of Bramble',ti:5,sp:2,emb:3,what:'',shade:1},
 {id:'ward1',kind:'Keepsake',name:'Ward of Inferno',ti:6,sp:2,emb:3,what:'',shade:1},
 {id:'ward2',kind:'Keepsake',name:'Ward of Abyss',ti:7,sp:2,emb:3,what:'',shade:1},
 {id:'ward3',kind:'Keepsake',name:'Ward of Wraith',ti:8,sp:2,emb:3,what:'',shade:1},
 {id:'ward4',kind:'Keepsake',name:'Ward of Void',ti:9,sp:2,emb:3,what:'',shade:1}];
/* 0.41: the lantern is always listed (first, once a realm is charted); wards appear with the lantern. */
function fgList(){const L=FORGE_R.filter(r=>!r.shade||hasLantern());if(chartedCount()>=1&&!fgMade('xlantern')){const i=L.findIndex(r=>r.id==='xlantern');L.unshift(L.splice(i,1)[0]);}return L;}
const WARD_COL=['#FF4D5E','#FF7A2E','#37E6D0','#8FE3FF','#FF4FB0'];
const spareRealms=()=>[0,1,2,3,4].filter(t=>spareTotal(t)>0);""")
rep(" charm:['...kk...','..k..k..','..k..k..','...kk...','..kXXk..','.kXXXXk.','.kXYXXk.','.kXXXXk.','..kXXk..','...kk...'],",
    " charm:['...kk...','..k..k..','..k..k..','...kk...','..kXXk..','.kXXXXk.','.kXYXXk.','.kXXXXk.','..kXXk..','...kk...'],\n ward:['...kk...','..k..k..','...kk...','.kkkkkk.','kXXXXXXk','kXYXXXXk','kXXXXXXk','.kXXXXk.','..kXXk..','...kk...'],\n xlantern:['...kk...','..k..k..','.kkkkkk.','.kmYYmk.','.kYyyYk.','.kYyyYk.','.kmYYmk.','.kkkkkk.','..kaak..','........'],")
rep("function fgRows(id){const m=/^charm([0-4])$/.exec(id);if(m)return FGSPR.charm.map(r=>r.replace(/X/g,m[1]));return FGSPR[id]||null;}",
    "function fgRows(id){const m=/^charm([0-4])$/.exec(id);if(m)return FGSPR.charm.map(r=>r.replace(/X/g,m[1]));const w=/^ward([0-4])$/.exec(id);if(w)return FGSPR.ward.map(r=>r.replace(/X/g,String(5+(+w[1]))));return FGSPR[id]||null;}")
rep("function spareList(ti){return CURIOS.filter(", "function spareList(ti){return ALLC.filter(")
rep("const FCOL={0:'#4FA36A',1:'#FF8A2E',2:'#4F93C8',3:'#BFE6FF',4:'#9B7BD8',", "const FCOL={0:'#4FA36A',1:'#FF8A2E',2:'#4F93C8',3:'#BFE6FF',4:'#9B7BD8',5:'#FF4D5E',6:'#FF7A2E',7:'#37E6D0',8:'#8FE3FF',9:'#FF4FB0',")
rep("const charmOf=c=>{const m=c&&/^charm([0-4])$/.exec(c.keep||'');", "const charmOf=c=>{const m=c&&/^(charm|ward)([0-4])$/.exec(c.keep||'');")
rep("const FG_KIND={Keepsake:'Charms can be worn by any Forgeling, by the fire and on its card.'};",
    "const FG_KIND={Keepsake:'Charms and wards can be worn by any Forgeling, by the fire and on its card.'};")
rep("function fgCan(r){return !fgMade(r.id)&&embers()>=r.emb&&spareTotal(r.ti)>=r.sp;}",
    "function fgCan(r){if(r.multi)return !fgMade(r.id)&&embers()>=r.emb&&chartedCount()>=1&&spareRealms().length>=r.multi;return !fgMade(r.id)&&embers()>=r.emb&&spareTotal(r.ti)>=r.sp;}")
rep("""function fgNeeds(r){const sp=spareTotal(r.ti),e=embers(),rn=r.ti!==undefined?THEMES[r.ti].name+' ':'';""",
    """function fgNeeds(r){const sp=spareTotal(r.ti),e=embers(),rn=r.ti!==undefined?mapName(r.ti)+' ':'';
  if(r.multi){const k=spareRealms().length;return `Needs a spare from ${r.multi} different realms, ${r.emb} embers and a fully charted realm (you have spares from ${k} ${k===1?'realm':'realms'}, ${e} ${e===1?'ember':'embers'}, and ${chartedCount()?'a charted realm':'no realm fully charted yet'}).`;}""")
rep("""  const f=fgState(),s=fgSmith(),e=embers(),sp=spareTotal(),made=f.made.length;
  const rows=FORGE_R.map(r=>{""", """  const f=fgState(),s=fgSmith(),e=embers(),sp=spareTotal(),L=fgList(),made=L.filter(r=>fgMade(r.id)).length;
  const rows=L.map(r=>{""")
rep("${made} of ${FORGE_R.length} pieces made.${s?` Whoever helps signs the piece.", "${made} of ${L.length} pieces made.${s?` Whoever helps signs the piece.")
rep("""  const sl=spareList(r.ti);for(let guard=0;need>0&&guard<40;guard++)sl.forEach(x=>{if(need>0&&state.curios[x.id].n>1){state.curios[x.id].n--;need--;used.push(x.name.toLowerCase());}});""",
    """  if(r.multi){spareRealms().sort((a,b)=>spareTotal(b)-spareTotal(a)).slice(0,r.multi).forEach(t=>{const x=spareList(t)[0];state.curios[x.id].n--;need--;used.push(x.name.toLowerCase());});}
  else{const sl=spareList(r.ti);for(let guard=0;need>0&&guard<40;guard++)sl.forEach(x=>{if(need>0&&state.curios[x.id].n>1){state.curios[x.id].n--;need--;used.push(x.name.toLowerCase());}});}""")
rep("${r.kind==='Hearth'?'It is by the fire now.':r.id==='bell'?'It hangs by the Wander path.':r.id==='compass'?'It sits on the Forge panel.':''}</p>",
    "${r.kind==='Hearth'?'It is by the fire now.':r.id==='bell'?'It hangs by the Wander path.':r.id==='compass'?'It sits on the Forge panel.':r.id==='xlantern'?'It lights the other side of every realm you have fully charted.':''}</p>")
rep("<div class=\"stack\">${r.ti!==undefined?`<button class=\"primary\" data-equip=\"${r.id}\" data-cid=\"${s.id}\">${esc(s.nick||s.name)} wears it</button>`:''}<button class=\"${r.ti!==undefined?'ghost':'primary'}\" data-close>Lovely</button></div>`);",
    "<div class=\"stack\">${r.ti!==undefined?`<button class=\"primary\" data-equip=\"${r.id}\" data-cid=\"${s.id}\">${esc(s.nick||s.name)} wears it</button>`:''}${r.id==='xlantern'?'<button class=\"primary\" id=\"fgTurn\">Turn the map over</button>':''}<button class=\"${r.ti!==undefined||r.id==='xlantern'?'ghost':'primary'}\" data-close>Lovely</button></div>`);")
rep("""  return `<div class="panel-box forgep" style="margin-top:8px"><div class="row" style="margin:0"><h2 style="margin:0">The Forge</h2><span class="muted small" id="hEmbers">${e} ${e===1?'ember':'embers'}</span></div>
    <p class="muted small">${made?`${made} of ${FORGE_R.length} pieces made.`:'Nothing forged yet.'}""",
    """  if(chartedCount()>=1&&!fgMade('xlantern'))tools=`<p class="small" id="hLantern" style="margin:8px 0 0">A charted realm is waiting for a lantern. ${fgCan(FORGE_R.find(r=>r.id==='xlantern'))?'You have what it needs.':'See what it needs in the Forge.'}</p>`+tools;
  return `<div class="panel-box forgep" style="margin-top:8px"><div class="row" style="margin:0"><h2 style="margin:0">The Forge</h2><span class="muted small" id="hEmbers">${e} ${e===1?'ember':'embers'}</span></div>
    <p class="muted small">${made?`${made} of ${fgList().length} pieces made.`:'Nothing forged yet.'}""")
rep("  if(e.target.closest&&e.target.closest('#wcOk')){",
    "  if(e.target.closest&&e.target.closest('#fgTurn')){closeModal();tab='chronicle';ch.sub='map';ch.side=1;ch.realm=null;render();window.scrollTo(0,0);return;}\n  if(e.target.closest&&e.target.closest('#wcOk')){")

# ---------- ribbons (shown once the lantern is made) ----------
rep("  {id:'gift1',name:'Kind Gesture',", """  {id:'cross1',name:'Lantern Light',desc:'Cross to the other side of the map.',g:1,f:()=>shadeOpenList().length,hide:()=>!hasLantern()},
  {id:'shade5',name:'Both Sides',desc:'Fully chart all five Shade realms.',g:5,f:()=>[5,6,7,8,9].filter(t=>placesFound(t)===5).length,hide:()=>!hasLantern()},
  {id:'gift1',name:'Kind Gesture',""")
rep("""  return `<h3 style="margin-top:6px">Ribbons</h3><p class="muted small" style="margin-bottom:8px">${earned.length} of ${RIBBONS.length} earned. They are goals to enjoy, not chores.</p><div class="ribbons">${RIBBONS.map(r=>{""",
    """  const RV=RIBBONS.filter(r=>!r.hide||!r.hide());
  return `<h3 style="margin-top:6px">Ribbons</h3><p class="muted small" style="margin-bottom:8px">${earned.length} of ${RV.length} earned. They are goals to enjoy, not chores.</p><div class="ribbons">${RV.map(r=>{""")

# ---------- report and a prototype tool ----------
rep("\\nCurios found: ${Object.keys(state.curios).length} of ${CURIOS.length}", "\\nCurios found: ${haveN()} of ${shelfSet().length}")
rep("\\nRibbons: ${earnedIds().length} of ${RIBBONS.length}", "\\nRibbons: ${earnedIds().length} of ${RIBBONS.length}\\nLantern: ${hasLantern()?'yes':'no'}\\nShade realms lit: ${shadeOpenList().length}\\nShade curios: ${SCURIOS.filter(x=>state.curios[x.id]).length}")
rep("""      <button class="tool" data-tool="spares"><b>Spares for the Forge</b><span>Two spares of every curio from realms on your map, for trying the Forge.</span></button>""",
    """      <button class="tool" data-tool="spares"><b>Spares for the Forge</b><span>Two spares of every curio from realms on your map, for trying the Forge.</span></button>
      <button class="tool" data-tool="shade"><b>The other side</b><span>Fully charts every realm on your map and forges the Crossing Lantern.</span></button>""")
rep("  else if(name==='wander'){", """  else if(name==='shade'){const ks=rKnown();if(!ks.length){toast('Find a Forgeling first.');return;}if(!state.explore)state.explore={};ks.forEach(t=>state.explore[t]=4);const f=fgState();if(!f.made.includes('xlantern')){f.made.push('xlantern');f.log.xlantern={by:'a Forgeling',at:todayKey(),used:[]};}save();tab='chronicle';ch.sub='map';ch.side=1;ch.realm=null;render();window.scrollTo(0,0);toast('The lantern is lit. The map is turned over.');}
  else if(name==='wander'){""")

# ---------- What's New (keeps eight) ----------
rep("""    <ul class="newlist"><li><b>A living Hearth.</b>""", """    <ul class="newlist"><li><b>The other side.</b> Fully chart a realm, then forge a Crossing Lantern at the Hearth, and you can turn the map over. Each realm has a Shade twin on the back, with its own places, four new curios, an old tale told from the other side, and a ward to forge. The Shade names now live on the back of the map, so the front always shows the bright ones.</li>
    <li><b>A living Hearth.</b>""")
src2 = re.sub(r"\n    <li><b>Your favourite, on Today\.</b>.*?</li>(</ul>)", r"\1", src, count=1, flags=re.S)
assert src2 != src; src = src2

open('work.html', 'w', encoding='utf8').write(src)
print('ok', len(src))

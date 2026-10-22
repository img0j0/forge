# Forgelings 0.30.0: curios get a real look and feel.
# 1. Pixel-art curios: all 20 drawn as 16x16 sprites (curios/sprites.py -> CSPR), replacing emoji everywhere.
# 2. A real shelf: wooden shelves by realm; found curios sit on them, missing ones show as faint outlines. Tap one to
#    see it close up, its story, who found it, its tale page, and to set it by the fire.
# 3. By the fire: the chosen curio (or the latest found) sits beside the fire in the Hearth scene.
# 4. Gift unwrap: a gift arrives as a little bundle that opens.
# Makes room by dropping Fredoka 400, which nothing uses. Reads base29.html.
import re, os
src = open('base29.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)
CSPR = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'curios', 'csprites.js'), encoding='utf8').read()

# ---- room: drop the unused Fredoka 400 face ----
m = re.search(r"@font-face\{font-family:'Fredoka';font-style:normal;font-weight:400;[^}]*\}\n?", src)
assert m and 'base64' in m.group(0); src = src[:m.start()] + src[m.end():]

# ---- styles ----
rep('.shelf{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}.shelf span{width:36px;height:36px;display:grid;place-items:center;border-radius:11px;background:rgba(127,127,127,.14);font-size:21px}.shelf span.off{opacity:.4;font-size:14px;font-weight:700}',
    '.shelf{margin-top:6px}')
rep('/* Nav */', '''.cimg{image-rendering:pixelated;display:inline-block;vertical-align:middle}
.srow{margin:10px 0 0}.slab{font:600 13px var(--display);color:var(--muted)}
.splank{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;padding:2px 6px 0;border-bottom:7px solid #9A6A3E;box-shadow:0 3px 0 #5A3A22;border-radius:2px}
.scur{min-height:52px;background:none;border:0;padding:0 0 2px;display:grid;place-items:end center;cursor:pointer;border-radius:8px}
.scur:focus-visible{outline:3px solid var(--plum);outline-offset:2px}
.scur.off .cimg{opacity:.32}
.cbig{display:grid;place-items:center;margin:4px 0 2px}
.cbig .cimg{filter:drop-shadow(0 4px 0 rgba(0,0,0,.18))}
.cpop{animation:cpop .5s cubic-bezier(.3,1.6,.5,1) both}
@keyframes cpop{from{transform:scale(.4);opacity:0}to{transform:none;opacity:1}}
.gcur{position:relative;height:104px;margin:6px 0 0}
.gcur .cimg{position:absolute;left:50%;top:4px;margin-left:-48px}
.gcur .gbun{animation:gbun 1.1s ease-in both}.gcur .gitem{animation:gitem .5s cubic-bezier(.3,1.6,.5,1) 1s both}
@keyframes gbun{0%{transform:none}15%{transform:rotate(-8deg)}30%{transform:rotate(8deg)}45%{transform:rotate(-6deg)}60%{transform:rotate(0) scale(1.08);opacity:1}100%{transform:scale(1.25);opacity:0}}
@keyframes gitem{from{transform:scale(.3);opacity:0}to{transform:none;opacity:1}}
.reduce .cpop,.reduce .gcur .gitem{animation:none}.reduce .gcur .gbun{display:none}
@media (prefers-reduced-motion: reduce){.cpop,.gcur .gitem{animation:none}.gcur .gbun{display:none}}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .scur:not(.off) .cimg,:root:not([data-theme="light"]) .cbig .cimg,:root:not([data-theme="light"]) .gcur .cimg,:root:not([data-theme="light"]) .gpick .cimg{filter:drop-shadow(0 0 1px rgba(255,246,207,.6))}}
:root[data-theme="dark"] .scur:not(.off) .cimg,:root[data-theme="dark"] .cbig .cimg,:root[data-theme="dark"] .gcur .cimg,:root[data-theme="dark"] .gpick .cimg{filter:drop-shadow(0 0 1px rgba(255,246,207,.6))}
/* Nav */''')

# ---- sprites and helpers ----
CUR_JS = CSPR + r'''
const CURL={},CPIX={};
function cpix(id){
  if(CPIX[id])return CPIX[id];const s=CSPR[id];if(!s)return null;const [pp,g]=s.split('|'),pal={k:[46,42,71]};
  pp.split(',').forEach(e=>{const h=e.slice(1);pal[e[0]]=[parseInt(h.slice(0,2),16),parseInt(h.slice(2,4),16),parseInt(h.slice(4,6),16)];});
  const px=[];for(let i=0;i<256;i++){const ch=g[i];if(ch!=='.'&&pal[ch])px.push([i%16,i>>4,pal[ch]]);}return CPIX[id]=px;
}
function curioURL(id,sil){
  const k=id+(sil?'-s':'');if(CURL[k])return CURL[k];const px=cpix(id);if(!px)return '';
  try{const cv=document.createElement('canvas');cv.width=16;cv.height=16;const x=cv.getContext('2d'),im=x.createImageData(16,16);
    px.forEach(([X,Y,c])=>{const o=(Y*16+X)*4;if(sil){im.data[o]=127;im.data[o+1]=120;im.data[o+2]=150;}else{im.data[o]=c[0];im.data[o+1]=c[1];im.data[o+2]=c[2];}im.data[o+3]=255;});
    x.putImageData(im,0,0);return CURL[k]=cv.toDataURL();}catch(e){return '';}
}
const cImg=(id,sz,o)=>{o=o||{};const u=curioURL(id,o.sil);return u?`<img class="cimg${o.cls?' '+o.cls:''}" src="${u}" width="${sz}" height="${sz}" alt="${o.alt?esc(o.alt):''}">`:'';};
function fireCurio(){
  const h=state.hearth;if(h.curio&&state.curios[h.curio])return h.curio;
  const ks=Object.keys(state.curios);return ks.length?ks[ks.length-1]:null;
}
function shelfHTML(){
  return `<div class="shelf">${[0,1,2,3,4].map(ti=>{const known=rKnownTi(ti);
    return `<div class="srow"><span class="slab">${known?esc(mapName(ti)):'A realm not yet on your map'}</span><div class="splank">${rCurios(ti).map(x=>state.curios[x.id]
      ?`<button class="scur" data-cur="${x.id}" aria-label="${esc(x.name)}">${cImg(x.id,40)}</button>`
      :`<button class="scur off" data-cur="${x.id}" aria-label="A curio not found yet">${cImg(x.id,40,{sil:1})}</button>`).join('')}</div></div>`;}).join('')}</div>`;
}
function openCurio(id){
  const cu=CURIOS.find(x=>x.id===id);if(!cu)return;const rec=state.curios[id],ti=CREALM[id];
  if(!rec){openSheet(`<div class="cbig">${cImg(id,96,{sil:1})}</div><h2 class="center">Not found yet</h2>
    <p class="muted center">${rKnownTi(ti)?`It is somewhere in ${esc(mapName(ti))}. Send a Forgeling to wander there.`:'It is somewhere you have not been yet. Your map will show the way when a Forgeling from there finds you.'}</p>
    <div class="stack"><button class="primary" data-close>Got it</button></div>`);return;}
  const c=rec.cid?cardById(rec.cid):null,who=c?(c.nick||c.name):'A Forgeling';
  const line=rec.from?`${rec.from} sent this as a gift.`:(c&&c.dark?cu.d:cu.c).replace(/\{n\}/g,who);
  const by=fireCurio()===id;
  openSheet(`<div class="cbig">${cImg(id,96,{cls:'cpop',alt:cu.name})}</div><h2 class="center">${esc(cu.name)}</h2><p class="center">${esc(line)}</p>
    <p class="muted small center">${rec.at?'Found '+esc(dateLabel(rec.at))+'. ':''}${rec.n>1?'You have '+rec.n+'.':''}</p>
    ${talePageHTML(id).replace('class="tale new"','class="tale"')}
    <div class="stack"><button class="${by?'outline':'primary'}" id="curFire" data-id="${id}" ${by?'disabled':''}>${by?'It is by the fire':'Set it by the fire'}</button></div>
    <div class="row" style="justify-content:center"><button class="ghost" data-close>Close</button></div>`);
}
'''
rep("function wPanelHTML(c,n){", CUR_JS + "function wPanelHTML(c,n){")
# the shelf inside the wander panel
rep("""  const shelf=`<div class="shelf" role="img" aria-label="Curios found: ${have} of ${CURIOS.length}">${CURIOS.map(x=>state.curios[x.id]?`<span title="${x.name}" aria-hidden="true">${x.g}</span>`:'<span class="off" aria-hidden="true">?</span>').join('')}</div>`;""",
    """  const shelf=shelfHTML();""")
rep("  if(b.id==='hGift'){openGiftSend(c);return;}", "  if(b.id==='hGift'){openGiftSend(c);return;}\n  if(b.dataset.cur){openCurio(b.dataset.cur);return;}")
rep("""  else if(b.id==='giftKeep')giftKeep();""",
    """  else if(b.id==='giftKeep')giftKeep();
  else if(b.id==='curFire'&&b.dataset.id){state.hearth.curio=b.dataset.id;save();const cu=CURIOS.find(x=>x.id===b.dataset.id);closeModal();hf.msg=`The ${cu.name.toLowerCase()} now sits by the fire.`;renderHearth();}""")
# sanitize the fire curio
rep("""  if(s.giftsSent!==undefined&&!(Number.isInteger(s.giftsSent)&&s.giftsSent>=0))s.giftsSent=0;""",
    """  if(s.giftsSent!==undefined&&!(Number.isInteger(s.giftsSent)&&s.giftsSent>=0))s.giftsSent=0;
  if(s.hearth&&s.hearth.curio!==undefined&&!(typeof s.hearth.curio==='string'&&CURIOS.some(x=>x.id===s.hearth.curio)))delete s.hearth.curio;""")

# ---- the Hearth scene: the curio sits beside the fire (behind the Forgelings, inside the firelight) ----
rep("  drawSprout(setpx,t);\n", "  drawSprout(setpx,t);\n  {const fc=heapOn?null:fireCurio(),px=fc&&cpix(fc);if(px)px.forEach(([x,y,c])=>setpx(39+x,55+y,c));}\n")

# ---- emoji out, sprites in ----
rep("""    <div style="font-size:64px;text-align:center;line-height:1.25" aria-hidden="true">${cu.g}</div>""",
    """    <div class="cbig">${cImg(cu.id,80,{cls:'cpop'})}</div>""")
rep("""<li><span class="g" aria-hidden="true">${cu.g}</span>""", """<li><span class="g" aria-hidden="true">${cImg(cu.id,20)}</span>""")
rep("""<span class="gl" aria-hidden="true">${x.g}</span>""", """<span class="gl" aria-hidden="true">${cImg(x.id,32)}</span>""")
rep("""    <p class="gcur" aria-hidden="true">${cu.g}</p>""",
    """    <div class="gcur" aria-hidden="true">${cImg('bundle',96,{cls:'gbun'})}${cImg(cu.id,96,{cls:'gitem'})}</div>""")
# a gift remembers who sent it
rep("const cur=state.curios[cu.id]||{n:0,cid:0,at:todayKey(),gift:1};", "const cur=state.curios[cu.id]||{n:0,cid:0,at:todayKey(),gift:1,from:g.n};")
rep(".gpick button .gl{font-size:24px;line-height:1}", ".gpick button .gl{line-height:0}")

# ---- version and What's New (keep the list short to save room) ----
rep('<title>Forgelings (prototype 0.29.0)</title>', '<title>Forgelings (prototype 0.30.0)</title>')
rep("const VERSION='prototype 0.29.0';", "const VERSION='prototype 0.30.0';")
rep('const SEEN_V=34;', 'const SEEN_V=35;')
rep("""<ul class="newlist"><li><b>Gifts for friends.</b>""",
    """<ul class="newlist"><li><b>Curios, hand drawn.</b> Every curio now has its own pixel art. The curio shelf at the Hearth has real shelves, one for each realm, with outlines of what is still out there. Tap a curio to see it up close, and set your favourite by the fire.</li>
    <li><b>Gifts for friends.</b>""")
_i=src.index('<ul class="newlist">'); _j=src.index('</ul>',_i)
_items=re.findall(r'\s*<li>.*?</li>',src[_i+len('<ul class="newlist">'):_j],re.S)
src=src[:_i]+'<ul class="newlist">'+''.join(_items[:8])+src[_j:]
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src.encode()))

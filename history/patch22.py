# Forge 0.22.0: aesthetic polish. A pixel card back and a paper card face for the daily card,
# the reveal and packs staged at night by the fire, Journal stamps and ribbon badges, and a quieter Binder filter.
# Reads base21.html, writes work.html.
import base64, urllib.parse
src = open('base21.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

# ---------------- pixel art, drawn here as crisp SVG so it scales cleanly ----------------
def svg_from(w, h, layers):
    """layers: list of (color, set of (x,y)). Rows are merged into runs to keep the SVG small."""
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" shape-rendering="crispEdges" preserveAspectRatio="none">']
    for col, pts in layers:
        rows = {}
        for (x, y) in pts:
            rows.setdefault(y, []).append(x)
        out.append(f'<g fill="{col}">')
        for y, xs in sorted(rows.items()):
            xs = sorted(set(xs)); s = xs[0]; prev = s
            for x in xs[1:] + [None]:
                if x is not None and x == prev + 1: prev = x; continue
                out.append(f'<rect x="{s}" y="{y}" width="{prev - s + 1}" height="1"/>')
                if x is not None: s = prev = x
        out.append('</g>')
    out.append('</svg>')
    return ''.join(out)
def uri(svg): return 'url("data:image/svg+xml,' + urllib.parse.quote(svg, safe=' =:/,;"<>') .replace('"', "'") + '")'

FLAME = [".........#........",
         "........#Y#.......",
         "........#Y#.......",
         ".......#YY#.......",
         "...#...#YYY#..#...",
         "..#O#.#YYWY#.#O#..",
         "..#O#.#YWWY#.#O#..",
         "..#OO#YYWWYY#OO#..",
         "..#ROOYYWWYYOOR#..",
         "..#ROOYYYYYYOOR#..",
         "...#ROOOYYOOOR#...",
         "...#RROOOOOORR#...",
         "....#RRROORRR#....",
         ".....##RRRR##.....",
         "...BBBBBBBBBBBB...",
         "..BbbbbbbbbbbbbB..",
         "...BBBBBBBBBBBB..."]
FC = {'#': '#6E2228', 'Y': '#FFD66A', 'W': '#FFF6CF', 'O': '#FF8A2E', 'R': '#E5441E', 'B': '#462E1E', 'b': '#7A5434'}

def card_back(W, H, fy):
    L = {}
    def add(c, x, y): L.setdefault(c, set()).add((x, y))
    BASE = '<rect width="%d" height="%d" fill="#4C3D90"/>' % (W, H)
    # lattice of small diamonds
    for y in range(3, H - 3, 6):
        for x in range(3 + (3 if (y // 6) % 2 else 0), W - 3, 6):
            for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)): add('#5D4EA6', x + dx, y + dy)
            add('#6B5CB6', x, y)
    # frame: dark outer, gold stitch, dark inner
    for x in range(W):
        for y in (0, 1, H - 2, H - 1): add('#2B2152', x, y)
    for y in range(H):
        for x in (0, 1, W - 2, W - 1): add('#2B2152', x, y)
    for x in range(3, W - 3):
        if x % 3 != 2: add('#E7B84F', x, 3); add('#E7B84F', x, H - 4)
    for y in range(3, H - 3):
        if y % 3 != 2: add('#E7B84F', 3, y); add('#E7B84F', W - 4, y)
    for (cx, cy) in ((3, 3), (W - 4, 3), (3, H - 4), (W - 4, H - 4)):
        add('#FFF2C2', cx, cy)
    # a soft glow behind the flame
    gx, gy = W // 2, fy + 9
    for y in range(H):
        for x in range(W):
            d = ((x - gx) ** 2 + ((y - gy) * 1.15) ** 2) ** .5
            if 7 < d < 12 and 4 < x < W - 5 and 4 < y < H - 5: add('#5E4796', x, y)
            elif d <= 7 and 4 < x < W - 5: add('#6E4E9C', x, y)
    ox = (W - len(FLAME[0])) // 2
    for j, row in enumerate(FLAME):
        for i, ch in enumerate(row):
            if ch != '.': add(FC[ch], ox + i, fy + j)
    order = ['#5E4796', '#6E4E9C', '#5D4EA6', '#6B5CB6', '#2B2152', '#E7B84F', '#FFF2C2'] + list(FC.values())
    sv = svg_from(W, H, [(c, L[c]) for c in order if c in L])
    return sv.replace('preserveAspectRatio="none">', 'preserveAspectRatio="none">' + BASE, 1)

BACK_TEXT = uri(card_back(40, 56, 9))     # flame high, room for words underneath
BACK_PLAIN = uri(card_back(40, 56, 18))   # flame centred, for the reveal cover

def paper():
    L = {'#FBF5E6': set(), '#F2E8D0': set(), '#EADDBF': set()}
    for y in range(16):
        for x in range(16):
            L['#FBF5E6'].add((x, y))
    for (x, y) in ((2, 3), (11, 1), (6, 9), (14, 12), (4, 14), (9, 6)): L['#F2E8D0'].add((x, y))
    for (x, y) in ((13, 5), (1, 10), (8, 13)): L['#EADDBF'].add((x, y))
    return svg_from(16, 16, list(L.items()))
PAPER = uri(paper())

rep(':root{', f':root{{--cbT:{BACK_TEXT};--cbP:{BACK_PLAIN};--paper:{PAPER};', 1)
rep('/* Nav */', f'''/* ---- 0.22: the daily card in pixels ---- */
.heroback{{background:var(--cbT) 0 0/100% 100% no-repeat !important;box-shadow:0 6px 0 rgba(46,42,71,.22) !important;align-content:end !important;padding-bottom:26px !important;text-shadow:0 2px 0 #2B2152}}
.heroback svg{{display:none}}
.vface.vback{{background:var(--cbT) 0 0/100% 100% no-repeat !important;justify-content:flex-end !important;padding-bottom:13% !important;border-radius:6px !important;text-shadow:0 2px 0 #2B2152}}
.vface.vback svg{{display:none}}
.cover{{background:var(--cbP) 0 0/100% 100% no-repeat !important;box-shadow:none !important}}
.cover svg{{display:none}}
.vface.vfront,.taskface{{background:var(--paper) 0 0/32px 32px repeat,#FBF5E6 !important;color:#2E2A47}}
.vface.vfront{{border:3px solid #2E2A47 !important;border-radius:6px !important;box-shadow:0 0 0 3px #FBF5E6 inset,0 10px 0 rgba(46,42,71,.22)}}
.vface.vback{{box-shadow:0 10px 0 rgba(46,42,71,.22)}}
.vband,.taskface .band{{position:relative;border-bottom:0 !important;background-image:linear-gradient(90deg,#2E2A47 50%,transparent 50%);background-size:6px 3px;background-repeat:repeat-x;background-position:0 100%;padding-bottom:16px !important}}
.vbody strong,.taskface strong{{font:600 15px var(--display);letter-spacing:.01em}}
.taskface{{border-width:3px !important;border-radius:6px !important}}
/* ---- 0.22: the reveal and packs, at night by the fire ---- */
.scrim.dark{{background:#0E0B24}}
.stageCv{{position:absolute;inset:0;width:100%;height:100%;image-rendering:pixelated;image-rendering:crisp-edges;image-rendering:pixelated;pointer-events:none;z-index:0}}
.scrim.dark .ov{{position:relative;z-index:1}}
/* Nav */''')

def flame_group():
    L={}
    for j,row in enumerate(FLAME):
        for i,ch in enumerate(row):
            if ch!='.': L.setdefault(FC[ch],set()).add((i,j))
    inner=svg_from(18,17,list(L.items())).split('>',1)[1].rsplit('</svg>',1)[0]
    return '<g transform="translate(53 60) scale(3)" shape-rendering="crispEdges">'+inner+'</g>'
rep('''<path d="M80 62l26 22l-26 46l-26 -46z" fill="#FFD36B" stroke="#fff" stroke-width="2"/><path d="M54 84h52M68 84l12 46M92 84l-12 46" stroke="#fff" stroke-width="2" opacity=".8"/>''', flame_group())


# ================= Journal: flame stamps for days you showed up, a moon for rest days =================
STAMP_FLAME = ["....#....",
               "...#Y#...",
               "...#Y#.#.",
               ".#.#YY##O",
               "#O#YYWY#O",
               "#OOYWWYOO",
               "#ROYYYYOR",
               ".#ROOOOR#",
               "..#RRRR#."]
STAMP_MOON = ["..####..",
              ".###....",
              "###.....",
              "###.....",
              "###.....",
              "###.....",
              ".###....",
              "..####.."]
def stamp_svg(grid, cmap):
    L={}
    for j,row in enumerate(grid):
        for i,ch in enumerate(row):
            if ch!='.': L.setdefault(cmap[ch],set()).add((i,j))
    return svg_from(len(grid[0]),len(grid),list(L.items())).replace('preserveAspectRatio="none"','')
FLAME_URI = uri(stamp_svg(STAMP_FLAME, {'#':'#8E2F2A','Y':'#FFD66A','W':'#FFF6CF','O':'#FF8A2E','R':'#E5441E'}))
MOON_URI = uri(stamp_svg(STAMP_MOON, {'#':'#8E86C9'}))
rep(':root{', f':root{{--stF:{FLAME_URI};--stM:{MOON_URI};', 1)
rep('--chip:#EFEAFA; --butter:#FFD36B; --scr:#A4471F;', '--chip:#EFEAFA; --butter:#FFD36B; --scr:#A4471F; --stamp:#FFF1D2; --stampEdge:#F1C76A;')
rep('--chip:#2D2851; --scr:#F0A472;', '--chip:#2D2851; --scr:#F0A472; --stamp:#3A2C2E; --stampEdge:#7A5A3A;', 2)
rep('/* Nav */', """#view-chronicle .cal span.c{position:relative;border-radius:6px;background:var(--surface);border:1.5px solid var(--line);place-items:start;padding:2px 0 0 4px;font-size:10px;line-height:1.2}
#view-chronicle .cal span.c.done{background:var(--stF) 55% 68%/58% auto no-repeat,var(--stamp);border-color:var(--stampEdge);color:var(--ink)}
#view-chronicle .cal span.c.rest{background:var(--stM) 58% 66%/52% auto no-repeat,var(--surface);border:1.5px dashed var(--line)}
#view-chronicle .cal span.c.skipped{background:transparent;border:1.5px solid var(--line)}
#view-chronicle .cal span.c.future{background:transparent;border:1.5px dashed var(--line)}
#view-chronicle .cal span.c.now{box-shadow:0 0 0 3px var(--butter)}
.calkey{display:flex;gap:14px;flex-wrap:wrap;margin:8px 0 2px;font-size:13px;color:var(--muted)}
.calkey i{display:inline-block;width:14px;height:14px;vertical-align:-2px;margin-right:5px;background-size:contain;background-repeat:no-repeat;background-position:center}
/* Nav */""")
rep("""<div class="cal">${head}${cells}</div>${didHTML(""", """<div class="cal">${head}${cells}</div><div class="calkey" aria-hidden="true"><span><i style="background-image:var(--stF)"></i>showed up</span><span><i style="background-image:var(--stM)"></i>rested</span></div>${didHTML(""")

# ================= Ribbons: pixel rosettes, and dots instead of progress bars =================
def rosette(earned):
    G=["..#####..",
       ".#CCCCC#.",
       "#CCHCCCC#",
       "#CHCCCCC#",
       "#CCCCCCC#",
       "#CCCCCCC#",
       ".#CCCCC#.",
       "..#####..",
       "..TT.TT..",
       ".TT...TT.",
       ".T.....T."]
    cm={'#':'#9A5A12','C':'#FFC43D','H':'#FFF2B8','T':'#D9475A'} if earned else {'#':'#B7AFD6','C':'#ECE8F8','H':'#FFFFFF','T':'#C9C2E4'}
    return uri(stamp_svg(G,cm))
rep(':root{', f':root{{--roOn:{rosette(True)};--roOff:{rosette(False)};', 1)
rep('/* Nav */', """.rib .ico{border-radius:0 !important;background:var(--roOff) center/contain no-repeat !important;width:34px !important;height:42px !important;font-size:0 !important}
.rib.on .ico{background:var(--roOn) center/contain no-repeat !important}
.rib .dots{display:flex;gap:4px;flex-wrap:wrap;margin-top:6px}
.rib .dots i{width:7px;height:7px;border-radius:2px;background:var(--chip);border:1px solid var(--line)}
.rib .dots i.on{background:var(--plum);border-color:var(--plum)}
.rib .soft{display:block;margin-top:4px;font-size:12px;color:var(--muted)}
/* Nav */""")
rep("""<div class="ico" aria-hidden="true">${on?'\\u2713':v+'/'+r.g}</div>""", """<div class="ico" role="img" aria-label="${on?'Earned':v+' of '+r.g}">${on?'\\u2713':v+'/'+r.g}</div>""")
rep("""${on?'':`<div class="pb" aria-hidden="true"><i style="width:${Math.round(v/r.g*100)}%"></i></div>`}""",
    """${on?'':r.g<=12?`<div class="dots" aria-hidden="true">${Array.from({length:r.g},(_,i)=>`<i class="${i<v?'on':''}"></i>`).join('')}</div>`:`<span class="soft">${v} of ${r.g} so far</span>`}""")

# ================= Binder: one quiet row, and a sheet for the filters =================
rep("""    <div class="filters" role="group" aria-label="Filter by type"><button class="fchip" data-ftype="all" aria-pressed="${bf.type==='all'}">All</button>${VECTORS.map((V,i)=>`<button class="fchip" data-ftype="${i}" aria-pressed="${String(bf.type)===String(i)}"><i style="background:${V.color}"></i>${V.name} ${counts[i]||0}</button>`).join('')}</div>
    <div class="row" style="margin:0 0 10px"><div class="chips" role="group" aria-label="Filter by mood" style="padding:0">${[['all','All'],['cute','Cute'],['dark','Dark']].map(a=>`<button class="chip" data-fmood="${a[0]}" aria-pressed="${bf.mood===a[0]}">${a[1]}</button>`).join('')}<button class="chip" id="fFav" aria-label="Favorites only" aria-pressed="${!!bf.fav}">\\u2605</button></div><button class="pill" id="btnSort">Sort: ${bf.sort==='new'?'Newest':'Rarest'}</button></div>""",
    """    <div class="row" style="margin:4px 0 10px"><button class="pill" id="btnFilter" aria-haspopup="dialog">Filter${filtN()?' \\u00B7 '+filtN():''}</button><button class="pill" id="btnSort">Sort: ${bf.sort==='new'?'Newest':'Rarest'}</button></div>
    ${filtN()?`<p class="muted small" style="margin:-4px 0 10px">Showing ${esc(filtText())}. <button class="ghost" id="fClear" style="padding:0 4px;min-height:44px">Show all</button></p>`:''}""")
rep('/* ================= Start ================= */', r"""const filtN=()=>(bf.type!=='all'?1:0)+(bf.mood!=='all'?1:0)+(bf.fav?1:0);
function filtText(){const p=[];if(bf.type!=='all'&&VECTORS[+bf.type])p.push(VECTORS[+bf.type].name);if(bf.mood!=='all')p.push(bf.mood==='dark'?'Dark':'Cute');if(bf.fav)p.push('favourites');return p.join(', ')+' only';}
function filterSheetHTML(){
  const counts={};state.cards.forEach(c=>counts[c.v]=(counts[c.v]||0)+1);
  return `<h2>Filter your binder</h2><div class="lbl2">Calling</div><div class="chips" role="group" aria-label="Filter by calling"><button class="fchip" data-ftype="all" aria-pressed="${bf.type==='all'}">All</button>${VECTORS.map((V,i)=>`<button class="fchip" data-ftype="${i}" aria-pressed="${String(bf.type)===String(i)}"><i style="background:${V.color}"></i>${V.name} ${counts[i]||0}</button>`).join('')}</div>
    <div class="lbl2">Mood</div><div class="chips" role="group" aria-label="Filter by mood">${[['all','All'],['cute','Cute'],['dark','Dark']].map(a=>`<button class="chip" data-fmood="${a[0]}" aria-pressed="${bf.mood===a[0]}">${a[1]}</button>`).join('')}<button class="chip" id="fFav" aria-pressed="${!!bf.fav}">\u2605 Favorites</button></div>
    <div class="stack"><button class="primary" data-close>Show ${binderCount()} ${binderCount()===1?'Forgeling':'Forgelings'}</button></div>`;
}
const binderCount=()=>state.cards.filter(c=>(bf.type==='all'||c.v===+bf.type)&&(bf.mood==='all'||(bf.mood==='dark')===c.dark)&&(!bf.fav||c.fav)).length;
function openFilter(){openSheet(filterSheetHTML());}
document.addEventListener('click',e=>{
  const b=e.target.closest&&e.target.closest('#modal button');if(!b||!modal.querySelector('#fFav'))return;
  let hit=false;
  if(b.dataset.ftype!==undefined){bf.type=b.dataset.ftype;hit=true;}else if(b.dataset.fmood){bf.mood=b.dataset.fmood;hit=true;}else if(b.id==='fFav'){bf.fav=!bf.fav;hit=true;}
  if(hit){bf.page=0;renderBinder();const d=modal.querySelector('[role=dialog]');if(d){const y=d.scrollTop;d.innerHTML=filterSheetHTML();d.scrollTop=y;nameDialog();}const f=modal.querySelector(b.id?'#'+b.id:b.dataset.ftype!==undefined?`[data-ftype="${b.dataset.ftype}"]`:`[data-fmood="${b.dataset.fmood}"]`);if(f)f.focus({preventScroll:true});}
});
/* ================= Start ================= */""")
rep("  if(b.dataset.ftype!==undefined){bf.type=b.dataset.ftype;bf.page=0;renderBinder();}", "  if(b.id==='btnFilter'){openFilter();return;}\n  if(b.id==='fClear'){bf.type='all';bf.mood='all';bf.fav=false;bf.page=0;renderBinder();return;}\n  if(b.dataset.ftype!==undefined){bf.type=b.dataset.ftype;bf.page=0;renderBinder();}")

STAGE_JS = r'''
/* ---- The stage: big moments (the reveal, packs, a card up close) happen at night by the fire.
   Stars overhead, warm light from a fire just below the screen, and a few embers rising. ---- */
let stageRAF=0,stageLast=0;
function drawStage(t){
  const cv=modal.querySelector('.stageCv');if(!cv){stageRAF=0;return false;}
  const asp=Math.max(1,innerHeight)/Math.max(1,innerWidth);let W=80,H=Math.round(80*asp);if(H<100){H=100;W=Math.min(320,Math.round(100/asp));}
  if(cv.width!==W||cv.height!==H){cv.width=W;cv.height=H;}
  const ctx=cv.getContext('2d'),img=ctx.createImageData(W,H),d=img.data,s0=[14,11,36],s1=[42,28,70],NB=8;
  for(let y=0;y<H;y++)for(let x=0;x<W;x++){const f=y/H*NB;let bi=Math.floor(f);if(f-bi>(BAY[(y&3)*4+(x&3)]+.5)/16)bi++;const k=Math.min(1,bi/NB),o=(y*W+x)*4;d[o]=lerp(s0[0],s1[0],k);d[o+1]=lerp(s0[1],s1[1],k);d[o+2]=lerp(s0[2],s1[2],k);d[o+3]=255;}
  const put=(x,y,q)=>{x=Math.floor(x);y=Math.floor(y);if(x<0||y<0||x>=W||y>=H)return;const o=(y*W+x)*4;d[o]=q[0];d[o+1]=q[1];d[o+2]=q[2];};
  const r=mulberry32(4711);
  for(let i=0,n=Math.round(W*H/150);i<n;i++){const x=r()*W,y=r()*H*.7,ph=r()*6.3,on=REDUCE?r()<.8:Math.sin(t/900+ph)>-.5;if(on)put(x,y,r()<.15?[255,236,190]:[186,180,232]);}
  /* firelight from below */
  const cx=W/2,cy=H+6;for(let y=Math.round(H*.45);y<H;y++)for(let x=0;x<W;x++){const dist=Math.hypot(x-cx,(y-cy)*1.25);if(dist<H*.62){let k=1-dist/(H*.62);k=k*k*(.55+(REDUCE?0:.05*Math.sin(t/120)));const o=(y*W+x)*4;d[o]=lerp(d[o],255,k);d[o+1]=lerp(d[o+1],140,k);d[o+2]=lerp(d[o+2],60,k);}}
  /* embers drifting up */
  if(!REDUCE)for(let i=0;i<9;i++){const sp=.012+(i%3)*.004,life=(t*sp/16+i*37)%(H*.6),x=cx+Math.sin(t/700+i*1.9)*(6+i*2.2)+((i*29)%31-15),y=H-life;put(x,y,life<H*.35?[255,190,90]:[255,120,60]);}
  ctx.putImageData(img,0,0);return true;
}
function stageLoop(ts){if(!modal.querySelector('.stageCv')){stageRAF=0;return;}if(ts-stageLast>80){stageLast=ts;drawStage(ts);}stageRAF=requestAnimationFrame(stageLoop);}
function stageOn(){
  const sc=modal.querySelector('.scrim.dark');if(!sc||sc.classList.contains('titlemode')||sc.querySelector('.stageCv'))return;
  const cv=document.createElement('canvas');cv.className='stageCv';cv.setAttribute('aria-hidden','true');sc.insertBefore(cv,sc.firstChild);
  drawStage(performance.now());if(!REDUCE&&!stageRAF)stageRAF=requestAnimationFrame(stageLoop);
}
window.addEventListener('resize',()=>{if(modal.querySelector('.stageCv'))drawStage(performance.now());});
'''
rep('/* ================= Start ================= */', STAGE_JS + '\n/* ================= Start ================= */')
rep("""  modal.innerHTML=`<div class="scrim dark" data-dismiss="${!!dismiss}"><div class="ov" role="dialog" aria-modal="true">${html}</div></div>`;modal.hidden=false;nameDialog();""",
    """  modal.innerHTML=`<div class="scrim dark" data-dismiss="${!!dismiss}"><div class="ov" role="dialog" aria-modal="true">${html}</div></div>`;modal.hidden=false;nameDialog();setTimeout(stageOn,0);""")

rep('<button class="vface vback" id="vBack" aria-label="Turn over today\'s card">', '<button class="vface vback" id="vBack">')

# ================= version =================
rep('<title>Forge (prototype 0.21.0)</title>', '<title>Forge (prototype 0.22.0)</title>')
rep("const VERSION='prototype 0.21.0';", "const VERSION='prototype 0.22.0';")
rep('const SEEN_V=25;', 'const SEEN_V=26;')
rep("""<ul class="newlist"><li><b>A warmer welcome.</b>""",
    """<ul class="newlist"><li><b>A new daily card.</b> Today\u2019s card has a pixel back with the campfire on it, and its face is printed on paper.</li>
    <li><b>Found by the fire.</b> New Forgelings and packs now open at night by a fire, with embers drifting up.</li>
    <li><b>Stamps and rosettes.</b> The Journal marks the days you showed up with a little flame and rest days with a moon. Ribbons are pixel rosettes now.</li>
    <li><b>A tidier binder.</b> Filters live behind one button.</li>
    <li><b>A warmer welcome.</b>""")

open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src))

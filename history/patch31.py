# Forgelings 0.31.0: the map, inked. Same map, same rules (no counts), a much richer sheet:
# - Parchment: warm paper (night paper in dark), fine grain, burnt edges, a double ruled border with corner marks.
# - Hand-inked lines: coastlines wobble slightly, the way a pen does (an SVG displacement filter).
# - Watercolour washes: realm colours pool and fade instead of sitting flat, with a soft pigment edge.
# - The sea: little ink waves in the open water between realms.
# - Trails: once two neighbouring realms are both known, a dotted trail joins them.
# - Fog: realms not yet found sit under soft cloud instead of an empty dashed line.
# - A compass rose and a ribbon for the title.
# Reads base301.html.
import re
src = open('base301.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

# ---- colours for the sheet ----
rep('''    --plum:#A596F2; --plum-ink:#17152A; --chip:#2D2851; --scr:#F0A472; --stamp:#3A2C2E; --stampEdge:#7A5A3A;
  }
}''', '''    --plum:#A596F2; --plum-ink:#17152A; --chip:#2D2851; --scr:#F0A472; --stamp:#3A2C2E; --stampEdge:#7A5A3A;
    --mpaper:#1F1B38; --mburn:rgba(0,0,0,.42); --mfog:#3D3768; --mgrain:#FFFFFF; --mrib:#2C2750; --mbleed:.4;
  }
}''')
rep(''':root[data-theme="dark"]{
  --bg:#17152A; --surface:#231F3D; --ink:#F1EEFB; --muted:#A9A3C9; --line:#3A345E;
  --plum:#A596F2; --plum-ink:#17152A; --chip:#2D2851; --scr:#F0A472; --stamp:#3A2C2E; --stampEdge:#7A5A3A;
}''', ''':root[data-theme="dark"]{
  --bg:#17152A; --surface:#231F3D; --ink:#F1EEFB; --muted:#A9A3C9; --line:#3A345E;
  --plum:#A596F2; --plum-ink:#17152A; --chip:#2D2851; --scr:#F0A472; --stamp:#3A2C2E; --stampEdge:#7A5A3A;
  --mpaper:#1F1B38; --mburn:rgba(0,0,0,.42); --mfog:#3D3768; --mgrain:#FFFFFF; --mrib:#2C2750; --mbleed:.4;
}
:root{--mpaper:#F8F0DE; --mburn:rgba(150,104,48,.24); --mfog:#FFFFFF; --mgrain:#7A5A34; --mrib:#EFE2C4; --mbleed:1}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--mpaper:#1F1B38; --mburn:rgba(0,0,0,.42); --mfog:#3D3768; --mgrain:#FFFFFF; --mrib:#2C2750; --mbleed:.4}}''')
rep('.mapwrap{background:var(--surface);', '.mapwrap{background:var(--mpaper);')
rep('.mp-sel{stroke:var(--plum)}', '''.mp-sel{stroke:var(--plum)}
.mp-paper{fill:var(--mpaper)}.mp-burn{stop-color:var(--mburn)}.mp-fog{fill:var(--mfog)}.mp-grain{fill:var(--mgrain)}.mp-rib{fill:var(--mrib)}.mp-inkf{fill:var(--ink)}.mp-bleed{opacity:var(--mbleed)}''')

# ---- geometry helpers: open sea, trails ----
SEA_JS = r'''/* ---- 0.31: the inked map. Open sea for waves, and trails between neighbouring realms. ---- */
function segD(x,y,a,b){const dx=b[0]-a[0],dy=b[1]-a[1],t=Math.max(0,Math.min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy||1)));return Math.hypot(x-a[0]-t*dx,y-a[1]-t*dy);}
function polyD(x,y,P){let m=1e9;for(let i=0,j=P.length-1;i<P.length;j=i++)m=Math.min(m,segD(x,y,P[j],P[i]));return inPoly(x,y,P)?-m:m;}
let SEA=null;
function seaPts(){
  if(SEA)return SEA;const out=[];
  for(let gy=58;gy<=392;gy+=19)for(let gx=16;gx<=326;gx+=23){
    const h=whash(gx*131+gy*7),x=gx+(h%9)-4,y=gy+((h>>4)%9)-4;
    if(MAPP.every(P=>polyD(x,y,P)>13)&&!(x>282&&y<52))out.push([x,y,h%3]);
  }
  return SEA=out;
}
const TRAILS=[[0,1],[0,2],[0,3],[1,3],[2,4],[0,4]];
function trailD(a,b){
  const A=MAPP[a],B=MAPP[b];let best=null;
  A.forEach(p=>B.forEach(q=>{const d=Math.hypot(p[0]-q[0],p[1]-q[1]);if(!best||d<best[0])best=[d,p,q];}));
  const [,p,q]=best,ca=mapMid(A),cb=mapMid(B),ux=p[0]-ca[0],uy=p[1]-ca[1],ul=Math.hypot(ux,uy)||1,vx=q[0]-cb[0],vy=q[1]-cb[1],vl=Math.hypot(vx,vy)||1;
  const s=[p[0]+ux/ul*4,p[1]+uy/ul*4],e=[q[0]+vx/vl*4,q[1]+vy/vl*4],mx=(s[0]+e[0])/2,my=(s[1]+e[1])/2,bend=((a+b)%2?1:-1)*Math.min(14,best[0]*.25),nx=-(e[1]-s[1]),ny=e[0]-s[0],nl=Math.hypot(nx,ny)||1;
  return `M${r1(s[0])} ${r1(s[1])}Q${r1(mx+nx/nl*bend)} ${r1(my+ny/nl*bend)} ${r1(e[0])} ${r1(e[1])}`;
}
function fogSVG(ti){
  const P=MAPP[ti],L=mapMid(P);let s='';
  P.forEach((p,i)=>{if(i%2)return;const h=whash(ti*97+i*13),x=L[0]+(p[0]-L[0])*.55,y=L[1]+(p[1]-L[1])*.55;s+=`<circle cx="${r1(x)}" cy="${r1(y)}" r="${14+h%10}"/>`;});
  s+=`<circle cx="${r1(L[0])}" cy="${r1(L[1])}" r="22"/>`;
  return `<g class="mp-fog" fill-opacity=".72" filter="url(#mpFog)">${s}</g>`;
}
const waveD=(x,y,k)=>k===0?`M${x-6} ${y}q3 -3 6 0t6 0`:k===1?`M${x-4} ${y}q2 -2.5 4 0t4 0`:`M${x-7} ${y}q3.5 -3 7 0t7 0M${x-3} ${y+4}q2 -2 4 0`;
'''
rep("function mapHTML(){", SEA_JS + "function mapHTML(){")

# ---- realms: watercolour wash + inked edge; fog over the unknown ----
rep('''    if(m.tier===0){g+=`<path d="${d}" class="mp-faint" fill="none" stroke-width="1.4" pathLength="100" stroke-dasharray="26 74" stroke-dashoffset="${-(whash(ti*53+9)%100)}" filter="url(#mpBlur)"/>''',
    '''    if(m.tier===0){g+=fogSVG(ti)+`<path d="${d}" class="mp-faint" fill="none" stroke-width="1" pathLength="100" stroke-dasharray="26 74" stroke-dashoffset="${-(whash(ti*53+9)%100)}" filter="url(#mpBlur)"/>''')
rep('''    g+=`<path d="${d}" fill="${acc}" fill-opacity="${[0,.12,.22,.32][m.tier]}" class="mp-st" stroke-width="${[0,1.1,1.5,1.9][m.tier]}" stroke-dasharray="${m.tier===1?'5 4':'none'}" stroke-opacity="${[0,.55,.8,1][m.tier]}"/>`;''',
    '''    g+=`<path d="${d}" fill="${acc}" fill-opacity="${[0,.2,.34,.46][m.tier]}" stroke="none" filter="url(#mpWash)"/><path d="${d}" fill="none" class="mp-bleed" stroke="${acc}" stroke-opacity="${[0,.35,.5,.6][m.tier]}" stroke-width="5" filter="url(#mpBleed)"/>`;
    g+=`<path d="${d}" fill="none" class="mp-st" stroke-width="${[0,1.1,1.5,1.9][m.tier]}" stroke-dasharray="${m.tier===1?'5 4':'none'}" stroke-opacity="${[0,.55,.8,1][m.tier]}" filter="url(#mpInk)"/>`;''')
# sea and trails go under everything else in the map group
rep('''  ms.forEach(m=>{
    const P=MAPP[m.ti],d=blobPath(P,m.ti+1,[3.4,2.3,1.3,.5][m.tier]),sel=ch.realm===m.ti;''',
    '''  const sea=`<path class="mp-st" fill="none" stroke-width="1" stroke-opacity=".38" d="${seaPts().map(([x,y,k])=>waveD(x,y,k)).join('')}"/>`;
  const trails=TRAILS.filter(([a,b])=>ms[a].tier>0&&ms[b].tier>0).map(([a,b])=>`<path class="mp-st" fill="none" stroke-width="1.2" stroke-dasharray="0.1 4.2" stroke-opacity=".75" d="${trailD(a,b)}"/>`).join('');
  g=sea+trails+g;
  ms.forEach(m=>{
    const P=MAPP[m.ti],d=blobPath(P,m.ti+1,[3.4,2.3,1.3,.5][m.tier]),sel=ch.realm===m.ti;''')

# ---- the sheet: paper, grain, burnt edges, border, ribbon, compass ----
rep('''    <defs><filter id="mpBlur" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="1"/></filter></defs>
    <rect x="3" y="3" width="334" height="424" rx="10" class="mp-st" fill="none" stroke-width="1.2" stroke-opacity=".35"/>
    <text x="16" y="24" class="mp-txt" font-size="14">The Forge, as it is remembered</text>
    <text x="16" y="38" class="mp-mut" font-size="10.5">In the ${esc(era.n)}</text>
    <path class="mp-st" fill="none" stroke-width="1.1" d="M312 14L312 42M298 28L326 28"/><text x="312" y="11" text-anchor="middle" class="mp-mut" font-size="9">N</text>''',
    '''    <defs><filter id="mpBlur" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="1"/></filter>
      <filter id="mpInk" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".045" numOctaves="2" seed="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="2.6" xChannelSelector="R" yChannelSelector="G"/></filter>
      <filter id="mpWash" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="3" seed="9" result="t"/><feColorMatrix in="t" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.1 1.38" result="m"/><feComposite in="SourceGraphic" in2="m" operator="in"/></filter>
      <filter id="mpBleed" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="1.6"/></filter>
      <filter id="mpFog" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="5"/></filter>
      <filter id="mpGrain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="1" seed="2" result="g"/><feColorMatrix in="g" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.4 1.25" result="a"/><feComposite in="SourceGraphic" in2="a" operator="in"/></filter>
      <radialGradient id="mpEdge" cx="50%" cy="48%" r="72%"><stop offset=".62" stop-opacity="0" class="mp-burn"/><stop offset="1" class="mp-burn"/></radialGradient></defs>
    <rect x="0" y="0" width="340" height="430" rx="16" class="mp-paper"/>
    <rect x="0" y="0" width="340" height="430" rx="16" class="mp-grain" opacity=".09" filter="url(#mpGrain)"/>
    <rect x="0" y="0" width="340" height="430" rx="16" fill="url(#mpEdge)"/>
    <rect x="5" y="5" width="330" height="420" rx="11" class="mp-st" fill="none" stroke-width="1.3" stroke-opacity=".5"/>
    <rect x="10" y="10" width="320" height="410" rx="7" class="mp-st" fill="none" stroke-width=".7" stroke-opacity=".32"/>
    <path class="mp-st" fill="none" stroke-width=".9" stroke-opacity=".45" d="M10 22q8 0 12 -12M330 22q-8 0 -12 -12M10 408q8 0 12 12M330 408q-8 0 -12 12"/>
    <path class="mp-rib" d="M12 14h214l-8 14l8 14h-214l8 -14z" opacity=".95"/><path class="mp-st" fill="none" stroke-width=".8" stroke-opacity=".4" d="M12 14h214l-8 14l8 14h-214l8 -14z"/>
    <text x="24" y="27" class="mp-txt" font-size="13.5">The Forge, as it is remembered</text>
    <text x="24" y="39" class="mp-mut" font-size="10">In the ${esc(era.n)}</text>
    <g transform="translate(305 34)"><circle r="15" class="mp-st" fill="none" stroke-width=".7" stroke-opacity=".45"/><path class="mp-inkf" fill-opacity=".85" d="M0 -17L3 -3L0 0zM17 0L3 3L0 0zM0 17L-3 3L0 0zM-17 0L-3 -3L0 0z"/><path class="mp-st" fill="none" stroke-width=".8" d="M0 -17L-3 -3L0 0M17 0L3 -3L0 0M0 17L3 3L0 0M-17 0L-3 3L0 0"/><path class="mp-st" fill="none" stroke-width=".6" stroke-opacity=".6" d="M7 -7L2 -2M7 7L2 2M-7 7L-2 2M-7 -7L-2 -2"/></g><text x="305" y="12" text-anchor="middle" class="mp-mut" font-size="9">N</text>''')
rep('''    <text x="170" y="420" text-anchor="middle" class="mp-mut" font-size="11">${esc(foot)}</text></svg>`;''',
    '''    <text x="170" y="414" text-anchor="middle" class="mp-mut" font-size="11">${esc(foot)}</text></svg>`;''')

rep('<title>Forgelings (prototype 0.30.1)</title>', '<title>Forgelings (prototype 0.31.0)</title>')
rep("const VERSION='prototype 0.30.1';", "const VERSION='prototype 0.31.0';")
rep('const SEEN_V=35;', 'const SEEN_V=36;')
rep("""<ul class="newlist"><li><b>Curios, hand drawn.</b>""",
    """<ul class="newlist"><li><b>The map, inked.</b> The map is now drawn on old paper, with hand-inked coasts, watercolour realms, waves in the open sea, trails between the realms you know, and fog over the ones you don’t.</li>
    <li><b>Curios, hand drawn.</b>""")
_i=src.index('<ul class="newlist">'); _j=src.index('</ul>',_i)
_items=re.findall(r'\s*<li>.*?</li>',src[_i+len('<ul class="newlist">'):_j],re.S)
src=src[:_i]+'<ul class="newlist">'+''.join(_items[:8])+src[_j:]
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src.encode()))

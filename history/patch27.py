# Forge 0.27.0: places on the map. Each realm has five named places. The first appears when you find your first
# Forgeling there; each wander there uncovers the next. Places are drawn on the Map as small landmarks joined by a dotted
# trail; a realm with all five is fully charted. Reads base26.html, writes work.html.
src = open('base26.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

rep('/* Nav */', '''.mp-gold{stroke:#C9962E}
:root[data-theme="dark"] .mp-gold{stroke:#E2B04A}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .mp-gold{stroke:#E2B04A}}
ul.places{list-style:none;margin:6px 0 0;padding:0;display:grid;gap:6px}
ul.places li{font-size:14px;line-height:1.35}
ul.places li.gone{color:var(--muted)}
ul.places li b{font-weight:700}
/* Nav */''')

PLACES_JS = r'''/* ---- 0.27: places on the map. The first place in a realm appears with your first Forgeling there; each wander there
   uncovers the next. They are drawn as small landmarks joined by a dotted trail. ---- */
const PLACES=[
 [{n:'The Slow Hill',k:'hill',x:'The first hill in Meadow. Someone is always sitting on it, admiring the view.'},
  {n:'Birdwait Oak',k:'tree',x:'Birds leave feathers in its branches as promises. The oak keeps every one.'},
  {n:'The Crooked Garden',k:'star',x:'Nothing here grows straight, and nothing here minds.'},
  {n:'Bramble Edge',k:'zig',x:'Where Meadow goes wild. The thorns keep untended things safe until you come back for them.'},
  {n:'Fernlow\'s Seat',k:'stone',x:'A flat stone where Fernlow sits. Time slows down a little near it.'}],
 [{n:'Leaprock',k:'star',x:'Where the Forge\'s first spark landed. The ground is still warm.'},
  {n:'Warmleaf Grove',k:'tree',x:'Red leaves that stay warm, and naps that last longer than planned.'},
  {n:'Skitter\'s Run',k:'zig',x:'A trail worn smooth by someone who never waits to be finished.'},
  {n:'The Holding Stone',k:'cave',x:'Down in Inferno. Heavy things rest here until someone is ready to lift them.'},
  {n:'Crystal Hollow',k:'gem',x:'Every crystal here was once a hard thing, finally done.'}],
 [{n:'First Wave Cove',k:'pool',x:'Where the water laughed for the first time. It still does, now and then.'},
  {n:'Pebble Shallows',k:'dots',x:'Round pebbles, warm water, and no hurry at all.'},
  {n:'Jollop\'s Point',k:'tower',x:'A rock where nobody keeps score. Jumping off is encouraged.'},
  {n:'The Questions Deep',k:'cave',x:'Down in the Abyss. Unasked questions drift here, glowing softly.'},
  {n:'Rainrise Bay',k:'arch',x:'Where answers rise as rain. Bring a pocket.'}],
 [{n:'The Unmelting Field',k:'star',x:'Snow that decided to stay. The air here makes thinking easy.'},
  {n:'Bell Peak',k:'bell',x:'A bell rings here once a year. Everyone comes. Nobody speaks.'},
  {n:'Quillen\'s Clearing',k:'pool',x:'A quiet clearing, trimmed of everything extra.'},
  {n:'Hollow Log Light',k:'cave',x:'In the Wraith whiteout, a small light kept burning so nobody feels alone.'},
  {n:'Moonrest',k:'arch',x:'Where the moon once rested. A sliver still glows on the snow.'}],
 [{n:'The First Workshop',k:'house',x:'Benches, half-made things, and a lamp that is always lit.'},
  {n:'Candle Row',k:'star',x:'Candles that light themselves when you want to see your work clearly.'},
  {n:'Tikka\'s Clocktower',k:'tower',x:'Every gear in it was fixed once, and has worked ever since.'},
  {n:'The Keyhole',k:'key',x:'Down in the Void. One small key, and one door that opens when you are ready.'},
  {n:'Red Thread Stair',k:'zig',x:'The way home from the Void, marked by a red thread and a small light.'}]];
const rKnownTi=ti=>state.cards.some(c=>c.theme===ti);
const placesFound=ti=>rKnownTi(ti)?Math.min(5,1+((state.explore&&state.explore[ti])||0)):0;
const chartedCount=()=>[0,1,2,3,4].filter(ti=>placesFound(ti)===5).length;
const PLACE_PTS={};
function placePts(ti){
  if(PLACE_PTS[ti])return PLACE_PTS[ti];
  const P=MAPP[ti],L=mapMid(P),xs=P.map(p=>p[0]),ys=P.map(p=>p[1]),x0=Math.min(...xs),x1=Math.max(...xs),y0=Math.min(...ys),y1=Math.max(...ys),gl=glyphPts(ti,MAXG[ti]);
  let out=[];
  for(const [edge,gd,pd,lw] of [[7,10,17,34],[6,8,14,30],[5,6,12,26],[4,4,10,20]]){
    out=[];
    for(let k=0;k<1500&&out.length<5;k++){
      const x=x0+whash(ti*4099+k*11+3)%1000/1000*(x1-x0),y=y0+whash(ti*7919+k*13+5)%1000/1000*(y1-y0);
      if(!inPoly(x,y,P)||![[edge,0],[-edge,0],[0,edge],[0,-edge]].every(o=>inPoly(x+o[0],y+o[1],P)))continue;
      if(Math.abs(x-L[0])<lw&&y>L[1]-13&&y<L[1]+17)continue;
      if(gl.some(q=>Math.hypot(q[0]-x,q[1]-y)<gd))continue;
      if(out.some(q=>Math.hypot(q[0]-x,q[1]-y)<pd))continue;
      out.push([Math.round(x),Math.round(y)]);
    }
    if(out.length===5)break;
  }
  while(out.length<5)out.push([Math.round(L[0]),Math.round(L[1]+22+out.length*4)]);
  out.sort((a,b)=>Math.atan2(a[1]-L[1],a[0]-L[0])-Math.atan2(b[1]-L[1],b[0]-L[0]));
  return PLACE_PTS[ti]=out;
}
function iconD(k,x,y){
  switch(k){
    case 'hill':return `M${x-5} ${y+3}Q${x} ${y-5} ${x+5} ${y+3}Z`;
    case 'tree':return `M${x} ${y-5}L${x+4} ${y+1}L${x-4} ${y+1}ZM${x} ${y+1}L${x} ${y+4}`;
    case 'star':return `M${x} ${y-5}L${x+1.3} ${y-1.3}L${x+5} ${y}L${x+1.3} ${y+1.3}L${x} ${y+5}L${x-1.3} ${y+1.3}L${x-5} ${y}L${x-1.3} ${y-1.3}Z`;
    case 'zig':return `M${x-5} ${y+2}L${x-2.5} ${y-3}L${x} ${y+2}L${x+2.5} ${y-3}L${x+5} ${y+2}`;
    case 'stone':return `M${x-4} ${y+2}Q${x-4} ${y-3} ${x} ${y-3}Q${x+4} ${y-3} ${x+4} ${y+2}Z`;
    case 'cave':return `M${x-5} ${y+3}Q${x-5} ${y-4} ${x} ${y-4}Q${x+5} ${y-4} ${x+5} ${y+3}M${x-2} ${y+3}Q${x-2} ${y-1} ${x} ${y-1}Q${x+2} ${y-1} ${x+2} ${y+3}`;
    case 'gem':return `M${x} ${y-5}L${x+4} ${y-1}L${x} ${y+5}L${x-4} ${y-1}ZM${x-4} ${y-1}L${x+4} ${y-1}`;
    case 'pool':return `M${x-5} ${y}Q${x-5} ${y-3} ${x} ${y-3}Q${x+5} ${y-3} ${x+5} ${y}Q${x+5} ${y+3} ${x} ${y+3}Q${x-5} ${y+3} ${x-5} ${y}Z`;
    case 'dots':return `M${x-4} ${y}h1M${x} ${y-2}h1M${x+3} ${y+1}h1M${x-1} ${y+3}h1`;
    case 'tower':return `M${x-2} ${y+4}L${x-2} ${y-3}L${x+2} ${y-3}L${x+2} ${y+4}ZM${x} ${y-3}L${x} ${y-6}L${x+3} ${y-5}L${x} ${y-4}`;
    case 'arch':return `M${x-5} ${y+3}L${x-5} ${y}Q${x-5} ${y-5} ${x} ${y-5}Q${x+5} ${y-5} ${x+5} ${y}L${x+5} ${y+3}`;
    case 'bell':return `M${x-4} ${y+3}Q${x-3} ${y-4} ${x} ${y-4}Q${x+3} ${y-4} ${x+4} ${y+3}ZM${x} ${y+3}L${x} ${y+5}`;
    case 'house':return `M${x-4} ${y+4}L${x-4} ${y-1}L${x} ${y-5}L${x+4} ${y-1}L${x+4} ${y+4}Z`;
    case 'key':return `M${x-1} ${y-4}Q${x-4} ${y-4} ${x-4} ${y-1.5}Q${x-4} ${y+1} ${x-1} ${y+1}Q${x+2} ${y+1} ${x+2} ${y-1.5}Q${x+2} ${y-4} ${x-1} ${y-4}ZM${x-1} ${y+1}L${x-1} ${y+5}L${x+1} ${y+5}`;
  }
  return '';
}
function placesSVG(ti){
  const n=placesFound(ti);if(!n)return '';const pts=placePts(ti),found=PLACES[ti].slice(0,n).map((p,i)=>[p,pts[i]]);
  let s='';
  if(n>1)s+=`<path class="mp-st" fill="none" stroke-width="1" stroke-dasharray="1.5 3" stroke-opacity=".7" d="M${found.map(f=>f[1][0]+' '+f[1][1]).join('L')}"/>`;
  s+=found.map(f=>`<path class="mp-st mp-place" fill="none" stroke-width="1.3" stroke-linejoin="round" stroke-linecap="round" transform="translate(${f[1][0]} ${f[1][1]}) scale(1.3)" d="${iconD(f[0].k,0,0)}"/>`).join('');
  return s;
}
function placesListHTML(ti){
  const n=placesFound(ti);if(!n)return '';
  return `<p class="muted small" style="margin:8px 0 0">Places on the map${n===5?'. Fully charted.':''}</p><ul class="places">${PLACES[ti].slice(0,n).map(p=>`<li><b>${esc(p.n)}.</b> <span class="world">${esc(p.x)}</span></li>`).join('')}${n<5?'<li class="gone">There is more to find here. Wander here to uncover it.</li>':''}</ul>`;
}
'''
rep('function mapState(){', PLACES_JS + 'function mapState(){')

# draw places on each known realm, under its name; a fully charted realm gets a gold mark under its name
rep("""    if(gl.length)g+=`<path class="mp-st" fill="none" stroke-width="1.1" stroke-opacity="${m.tier===1?.5:.75}" d="${gl.map(p=>glyphD(ti,p[0],p[1])).join('')}"/>`;""",
    """    if(gl.length)g+=`<path class="mp-st" fill="none" stroke-width="1.1" stroke-opacity="${m.tier===1?.5:.75}" d="${gl.map(p=>glyphD(ti,p[0],p[1])).join('')}"/>`;
    g+=placesSVG(ti);
""")
rep("""    if(m.tier===3)g+=`<path class="mp-st" fill="none" stroke-width="1" d="M${r1(L[0]-15)} ${r1(L[1]+10)}Q${r1(L[0])} ${r1(L[1]+14)} ${r1(L[0]+15)} ${r1(L[1]+10)}"/>`;""",
    """    const chd=placesFound(ti)===5;
    if(m.tier===3||chd)g+=`<path class="${chd?'mp-gold':'mp-st'}" fill="none" stroke-width="${chd?1.6:1}" d="M${r1(L[0]-15)} ${r1(L[1]+10)}Q${r1(L[0])} ${r1(L[1]+14)} ${r1(L[0]+15)} ${r1(L[1]+10)}"/>`;
    if(chd)g+=`<path class="mp-gold" fill="#E2B04A" stroke-width="1" d="M${r1(L[0])} ${r1(L[1]+9)}l3 3l-3 3l-3 -3z"/>`;""")
# the notes under the map say how many places are found
rep("""  let notes=ms.filter(m=>m.tier>0).map(m=>`<p class="small"><b>${esc(nameOf(m))}.</b> ${(dkOf(m)?dnames:names)[m.tier-1]}</p>`).join('');""",
    """  let notes=ms.filter(m=>m.tier>0).map(m=>{const pf=placesFound(m.ti);return `<p class="small"><b>${esc(nameOf(m))}.</b> ${(dkOf(m)?dnames:names)[m.tier-1]} ${['','One place drawn in so far.','A few places drawn in.','A few places drawn in.','Most of it drawn in.','Fully charted.'][pf]}</p>`;}).join('');""")
# the realm page lists its places
rep("""  if(loreOn()){const tp=talePages(ti);out+=""", """  out+=placesListHTML(ti);
  if(loreOn()){const tp=talePages(ti);out+=""")

# a wander uncovers the next place
rep("""  state.wstat.back++;state.wander=null;
  let done='';const rq=state.request,ra=rq?cardById(rq.cid):null;""",
    """  state.wstat.back++;state.wander=null;
  let place='';{const open=[0,1,2,3,4].filter(t=>rKnownTi(t)&&placesFound(t)<5),dto=to>=0?(open.includes(to)?to:-1):(open.length?open[Math.floor(r()*open.length)]:-1);
    if(dto>=0){if(!state.explore)state.explore={};state.explore[dto]=(state.explore[dto]||0)+1;const pf=placesFound(dto),pl=PLACES[dto][pf-1];
      place=`<div class="tale new"><b>A new place on your map: ${esc(pl.n)}</b><p class="world">${esc(pl.x)}</p><p class="small">${pf===5?`That is the last place in ${esc(THEMES[dto].name)}. The realm is fully charted.`:`Another place is drawn on your map of ${esc(THEMES[dto].name)}.`} See it on the Map tab.</p></div>`;}}
  let done='';const rq=state.request,ra=rq?cardById(rq.cid):null;""")
rep("""${isNew?talePageHTML(cu.id):''}${done}""", """${place}${isNew?talePageHTML(cu.id):''}${done}""")

# state
rep("own:{text:'',days:[]},backup:{at:'',ask:''}};}", "own:{text:'',days:[]},backup:{at:'',ask:''},explore:{}};}")
rep("  s.keepsR=Array.isArray(s.keepsR)?", """  {const e=s.explore&&typeof s.explore==='object'&&!Array.isArray(s.explore)?s.explore:{};const ok={};[0,1,2,3,4].forEach(t=>{const v=e[t];if(Number.isFinite(v)&&v>0)ok[t]=Math.min(4,Math.round(v));});s.explore=ok;}
  s.keepsR=Array.isArray(s.keepsR)?""")

# ribbons
rep("  {id:'tale1',name:'Tale Keeper',",
    "  {id:'chart1',name:'Cartographer',desc:'Find all five places in a realm.',g:1,f:()=>chartedCount()},\n  {id:'chart5',name:'Every Corner',desc:'Fully chart all five realms.',g:5,f:()=>chartedCount()},\n  {id:'tale1',name:'Tale Keeper',")

rep('<title>Forge (prototype 0.26.0)</title>', '<title>Forge (prototype 0.27.0)</title>')
rep("const VERSION='prototype 0.26.0';", "const VERSION='prototype 0.27.0';")
rep('const SEEN_V=30;', 'const SEEN_V=31;')
rep("""<ul class="newlist"><li><b>Old tales.</b>""",
    """<ul class="newlist"><li><b>Places on the map.</b> Each realm has five places to find. Your first Forgeling there reveals one, and every wander there uncovers another. Watch the Map fill in, one landmark at a time.</li>
    <li><b>Old tales.</b>""")
import re as _re
_i=src.index('<ul class="newlist">'); _j=src.index('</ul>',_i)
_items=_re.findall(r'\s*<li>.*?</li>',src[_i+len('<ul class="newlist">'):_j],_re.S)
src=src[:_i]+'<ul class="newlist">'+''.join(_items[:10])+src[_j:]
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src))

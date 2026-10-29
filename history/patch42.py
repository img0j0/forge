# Forgelings 0.42.0: the living map (Hunter chose A + B from the map design canvas, October 28).
# 1. Pixel landmarks: every place on both sides of the map (50) is drawn as a small pixel landmark in its realm's
#    colours, in place of the line icons. Each one is a 44-point tap target that opens a close-up: the landmark large,
#    its name and line, Send <name> to wander here, and its realm's page.
# 2. A living map: a canvas over the paper draws gentle realm weather (Meadow petals, Ember smoke and sparks, Tide
#    glints, Frost snow, Dusk fireflies; Shade realms on the back drift glowing motes), a glow on the place you found
#    today, and your wanderer walking the trail: out, a look around, and home again, placed by the wander's real time.
#    The loop draws about 12 times a second only while the Map is open; it stops on other tabs and when the app is
#    hidden. With Reduce Motion on, one still frame is drawn (the wanderer where it is, no weather).
# Reads base411.html.
src = open('base411.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

rep("const VERSION='prototype 0.41.1'", "const VERSION='prototype 0.42.0'")
rep("<title>Forgelings (prototype 0.41.1)</title>", "<title>Forgelings (prototype 0.42.0)</title>")
rep("const SEEN_V=46;", "const SEEN_V=47;")

# ---------- 1. pixel landmarks ----------
rep("""function placesSVG(ti){
  const n=placesFound(ti);if(!n)return '';const pts=placePts(ti),found=PLACES[ti].slice(0,n).map((p,i)=>[p,pts[i]]);
  let s='';
  if(n>1)s+=`<path class="mp-st" fill="none" stroke-width="1" stroke-dasharray="1.5 3" stroke-opacity=".7" d="M${found.map(f=>f[1][0]+' '+f[1][1]).join('L')}"/>`;
  s+=found.map(f=>`<path class="mp-st mp-place" fill="none" stroke-width="1.3" stroke-linejoin="round" stroke-linecap="round" transform="translate(${f[1][0]} ${f[1][1]}) scale(1.3)" d="${iconD(f[0].k,0,0)}"/>`).join('');
  return s;
}""",
"""/* ---- 0.42: pixel landmarks. Each place kind is a small pixel sprite, coloured for its realm (Shade twins darker,
   lit by their glow), drawn as one path per colour. ---- */
const LMSPR={
 hill:['....o....','...oggo..','..ogglgo.','.ogglggGo','ogglgggGo','oGGGGGGGo'],
 tree:['..ooooo..','.oglglgo.','oglggglgo','ogglgglGo','.oGGgGGo.','..ooWoo..','...oWo...','...oWo...'],
 star:['....o....','...oyo...','..oyYyo..','ooyYYYyoo','oyyYYYyyo','ooyYYYyoo','..oyYyo..','...oyo...','....o....'],
 zig:['o.....o..','ro...oro.','oGo.oGGo.','oGGoGGGGo','oGGGGrGGo','ooooooooo'],
 stone:['..ooooo..','.osssssSo','osssssSSo','oSSSSSSSo','.ooooooo.'],
 cave:['..ooooo..','.osssSSo.','osskkkSSo','oskkkkkSo','oskkkkkSo','ooooooooo'],
 gem:['....o....','...oco...','..occCo..','.occcCDo.','.ocCCCDo.','..oCCDo..','...oDo...','....o....'],
 pool:['..ooooo..','.obBBbbbo','obBbbbbbo','obbbbbBbo','.obbbbbo.','..ooooo..'],
 dots:['..o...o..','.oso.oso.','..o...o..','o...o....','so.oso...','o...o....'],
 tower:['...oyo...','..ossSo..','..osSSo..','..osSSo..','..osySo..','..osSSo..','.ossSSSo.','ooooooooo'],
 arch:['..ooooo..','.osssssSo','osSoooSSo','oso...oSo','oso...oSo','ooo...ooo'],
 bell:['....o....','...oao...','..oaaAo..','..oaYAo..','.oaaaaAo.','oaaaaaaAo','ooooaoooo','....o....'],
 house:['....o....','...oro...','..orrro..','.orrrrro.','owwwwwwWo','owyywoWWo','ooooooooo'],
 key:['..ooo....','.oaYao...','.oa.ao...','.oaaao...','..oao....','..oao....','..oaoao..','..oaaao..','..ooooo..']};
const LMBASE={o:'#2A2045',g:'#5FB86A',G:'#3E8A45',l:'#9FE08A',w:'#8A5A3A',W:'#5E3A22',y:'#FFD36B',Y:'#FFF3B0',s:'#B4B9C1',S:'#767B85',b:'#4F93C8',B:'#A6D8F2',
 r:'#D9475A',a:'#E3B341',A:'#B8862A',k:'#1B1530',c:'#E6DDFF',C:'#B9A6F0',D:'#7A5FC0'};
const LMTINT=[{},
 {g:'#E2703A',G:'#B4482A',l:'#FFB06A',s:'#A08478',S:'#6E564C'},
 {s:'#B9C8D2',S:'#7E8E9A',b:'#4FA9D9',B:'#BFE9F8'},
 {g:'#BFE6FF',G:'#7FB8E0',l:'#FFFFFF',s:'#D6E2EE',S:'#9AAAC0'},
 {r:'#9B7BD8',w:'#6A4FA8',W:'#4A3578',s:'#A99BC8',S:'#6E6290'}];
function lmPal(ti){
  const b=ti%5,p=Object.assign({},LMBASE,LMTINT[b]);if(ti<5)return p;
  const D=THEMES[b].dark;return Object.assign(p,{o:'#0B0816',g:D.bodies[0],G:D.bodies[1],l:D.accent,s:'#575168',S:'#363046',w:'#4A3A3A',W:'#2E2424',y:D.glow,Y:D.glow2,a:D.glow,A:D.accent,r:D.accent,b:b===2?'#1E5E78':'#2F3E55',B:D.glow,c:D.glow2,C:D.glow,D:D.accent});
}
const LMU=2.0;
function lmPaths(kind,ti,u,cx,cy){
  const rows=LMSPR[kind]||LMSPR.star,P=lmPal(ti),h=rows.length,w=9,x0=cx-w*u/2,y0=cy-h*u/2,by={};
  rows.forEach((r,j)=>{for(let i=0;i<r.length;i++){const ch=r[i];if(ch==='.'||!P[ch])continue;(by[ch]=by[ch]||[]).push(`M${r1(x0+i*u)} ${r1(y0+j*u)}h${u}v${u}h${-u}z`);}});
  return Object.keys(by).map(ch=>`<path fill="${P[ch]}" d="${by[ch].join('')}"/>`).join('');
}
function placesSVG(ti){
  const n=placesFound(ti);if(!n)return '';const pts=placePts(ti),found=PLACES[ti].slice(0,n).map((p,i)=>[p,pts[i]]);
  let s='';
  if(n>1)s+=`<path class="mp-st" fill="none" stroke-width="1" stroke-dasharray="1.5 3" stroke-opacity=".7" d="M${found.map(f=>f[1][0]+' '+f[1][1]).join('L')}"/>`;
  const L=mapMid(polyOf(ti)),lift=q=>(L[1]-q[1]>0&&L[1]-q[1]<22&&Math.abs(q[0]-L[0])<44)?5:0; /* a landmark just above the realm's name sits a little higher */
  s+=found.map(f=>`<g class="mp-place" shape-rendering="crispEdges">${lmPaths(f[0].k,ti,LMU,f[1][0],f[1][1]-lift(f[1]))}</g>`).join('');
  return s;
}
/* a 44-point target over each landmark, above the realm targets; opens the landmark's close-up */
function placeHits(tis){
  return tis.map(ti=>{const n=placesFound(ti);if(!n)return '';const pts=placePts(ti);
    return PLACES[ti].slice(0,n).map((p,k)=>`<circle class="mpplace" data-place="${ti}:${k}" cx="${pts[k][0]}" cy="${pts[k][1]}" r="26" role="button" tabindex="0" aria-label="${esc(p.n)}, ${esc(mapName(ti))}. Open its close-up" fill="transparent"/>`).join('');}).join('');
}
function openPlace(ti,k){
  const p=PLACES[ti]&&PLACES[ti][k];if(!p||placesFound(ti)<=k)return;
  const hc=slotCards(),hw=hc[Math.min(hf.sel,hc.length-1)],wc0=wCard();
  const big=`<svg class="lmbig" viewBox="0 0 90 90" width="132" height="132" role="img" aria-label="${esc(p.n)} in pixel art" shape-rendering="crispEdges">${lmPaths(p.k,ti,10,45,45)}</svg>`;
  const go=hw&&!(state.wander&&wc0)&&!state.hearth.sleep?`<button class="primary" data-wto="${ti}" data-close>Send ${esc(hw.nick||hw.name)} to wander here</button>`:'';
  openSheet(`<div class="cbig">${big}</div><p class="muted small center" style="margin:0">${esc(mapName(ti))}${ti>=5?' · the other side':''}</p><h2 class="center" style="margin-top:2px">${esc(p.n)}</h2>
    <p class="center world">${esc(p.x)}</p><div class="stack">${go}<button class="outline" data-realmopen="${ti}">Open ${esc(mapName(ti))}’s page</button></div>
    <div class="row" style="justify-content:center"><button class="ghost" data-close>Close</button></div>`);
}""")
# place targets after the realm targets, front and back
rep("""  if(ms[1].tier>0&&ms[2].tier>0)g+=`<path d="M204 253Q240 247 276 255" class="mp-st" fill="none" stroke-width="1.1" stroke-dasharray="1 4" stroke-opacity=".7"/>`;""",
    """  if(ms[1].tier>0&&ms[2].tier>0)g+=`<path d="M204 253Q240 247 276 255" class="mp-st" fill="none" stroke-width="1.1" stroke-dasharray="1 4" stroke-opacity=".7"/>`;
  g+=placeHits([0,1,2,3,4]);""")
rep("""    g+=`<path d="${d}" class="mphit" data-realm="${m.ti}" role="button" tabindex="0" aria-pressed="${sel}" aria-label="${m.tier>0?esc(THEMES[m.b].dark.name):'A dark corner across from '+THEMES[m.b].name}, ${sel?'close its page':'open its page'}" fill="transparent" stroke="none"/>`;
  });""", """    g+=`<path d="${d}" class="mphit" data-realm="${m.ti}" role="button" tabindex="0" aria-pressed="${sel}" aria-label="${m.tier>0?esc(THEMES[m.b].dark.name):'A dark corner across from '+THEMES[m.b].name}, ${sel?'close its page':'open its page'}" fill="transparent" stroke="none"/>`;
  });
  g+=placeHits([5,6,7,8,9]);""")
# the canvas for the living map, on both sides
rep("  return `${turnHTML()}<div class=\"mapwrap\">${svg}</div>${sp||", "  return `${turnHTML()}<div class=\"mapwrap\">${svg}<canvas class=\"mpfx\" aria-hidden=\"true\"></canvas></div>${sp||")
rep("  return `${turnHTML()}<div class=\"mapwrap mback\">${svg}</div>${sp||", "  return `${turnHTML()}<div class=\"mapwrap mback\">${svg}<canvas class=\"mpfx\" aria-hidden=\"true\"></canvas></div>${sp||")
# taps and keys on a landmark (before the realm handler, since a landmark sits inside its realm)
rep("""  const rh=e.target.closest('.mphit');""", """  const ph=e.target.closest('.mpplace');if(ph){const [a,k]=ph.dataset.place.split(':').map(Number);sfx('select');openPlace(a,k);return;}
  const rh=e.target.closest('.mphit');""")
rep("let bondUpNext=null;", """let bondUpNext=null;
document.addEventListener('click',e=>{const ro=e.target.closest&&e.target.closest('[data-realmopen]');if(!ro)return;const ti=+ro.dataset.realmopen;closeModal();tab='chronicle';ch.sub='map';ch.side=ti>=5?1:0;ch.realm=ti;render();});""")
rep(".mapcap p{margin:6px 0}", """.mapcap p{margin:6px 0}
.mapwrap{position:relative}.mpfx{position:absolute;pointer-events:none}
.mpplace{cursor:pointer;outline:none}.mpplace:focus-visible{stroke:var(--plum);stroke-width:1.6;stroke-dasharray:3 3}
.lmbig{image-rendering:pixelated;background:radial-gradient(circle,rgba(255,211,107,.22),transparent 68%);padding:8px}""")

# ---------- 2. the living map ----------
rep("function wakeLoops(){", """/* ---- 0.42: the living map. Drawn on a canvas over the paper, about 12 times a second, only while the Map is open. ---- */
let mapFxT=0,mapFxImg={},mapFxStill=0;
function mapFxCanvas(){if(tab!=='chronicle'||ch.sub!=='map')return null;const cv=document.querySelector('#view-chronicle .mpfx');return cv&&cv.isConnected?cv:null;}
function mapFxLoop(){
  mapFxT=0;const cv=mapFxCanvas();
  if(!cv||document.hidden){mapFxT=setTimeout(mapFxLoop,600);return;}
  if(REDUCE){if(mapFxStill!==cv){mapFxStill=cv;mapFxDraw(cv,0,true);}mapFxT=setTimeout(mapFxLoop,1000);return;}
  mapFxDraw(cv,performance.now(),false);mapFxT=setTimeout(mapFxLoop,80);
}
function mapFxSprite(c){const u=spriteURL(c);if(!u)return null;let im=mapFxImg[u];if(!im){im=new Image();im.src=u;mapFxImg[u]=im;}return im.complete?im:null;}
function mapFxDraw(cv,t,still){
  const svg=cv.parentNode.querySelector('svg.mapsvg');if(!svg)return;
  const R=svg.getBoundingClientRect(),W=cv.parentNode.getBoundingClientRect(),dpr=Math.min(2,window.devicePixelRatio||1);
  const w=Math.round(R.width),h=Math.round(R.height);if(!w||!h)return;
  if(cv.width!==Math.round(w*dpr)||cv.height!==Math.round(h*dpr)){cv.width=Math.round(w*dpr);cv.height=Math.round(h*dpr);cv.style.width=w+'px';cv.style.height=h+'px';}
  cv.style.left=(R.left-W.left)+'px';cv.style.top=(R.top-W.top)+'px';
  const x=cv.getContext('2d'),k=w/340*dpr;x.setTransform(1,0,0,1,0,0);x.clearRect(0,0,cv.width,cv.height);x.setTransform(k,0,0,k,0,8*k);x.imageSmoothingEnabled=false;
  const back=cv.parentNode.classList.contains('mback'),tis=back?[5,6,7,8,9]:[0,1,2,3,4],s=t/1000;
  const dot=(px,py,sz,col,a)=>{x.globalAlpha=Math.max(0,Math.min(1,a));x.fillStyle=col;x.fillRect(px-sz/2,py-sz/2,sz,sz);};
  if(!still)tis.forEach(ti=>{
    if(placesFound(ti)<1&&!(ti<5&&rKnownTi(ti)))return;const P=polyOf(ti),L=mapMid(P),b=ti%5;
    const xs=P.map(p=>p[0]),ys=P.map(p=>p[1]),x0=Math.min(...xs),x1=Math.max(...xs),y0=Math.min(...ys),y1=Math.max(...ys);
    for(let i=0;i<9;i++){const h1=whash(ti*131+i*17)%1000/1000,h2=whash(ti*977+i*29)%1000/1000,ph=(s/(4+h1*3)+h2)%1;
      let px=x0+h1*(x1-x0),py=y0+h2*(y1-y0);
      if(ti>=5){py-=ph*16;if(inPoly(px,py,P))dot(px,py,2,THEMES[b].dark.glow,Math.sin(ph*Math.PI));continue;}
      if(b===0){px+=ph*22;py+=Math.sin(ph*6+i)*3+ph*6;if(inPoly(px,py,P))dot(px,py,2,i%2?'#F29BB5':'#FFF3B0',Math.sin(ph*Math.PI));}
      else if(b===1){const sx=L[0]+(h1-.5)*30,sy=L[1]-6-ph*26;if(i<5)dot(sx+Math.sin(ph*5+i)*3,sy,2.2+ph*2,'#CDBFB4',(1-ph)*.55);else if(inPoly(px,py-ph*12,P))dot(px,py-ph*12,1.2,'#FFB067',Math.sin(ph*Math.PI));}
      else if(b===2){if(inPoly(px,py,P))dot(px,py,1.8,'#E8F4FF',Math.max(0,Math.sin(ph*Math.PI*2)));}
      else if(b===3){py+=ph*20-6;px+=Math.sin(ph*4+i)*2;if(inPoly(px,py,P))dot(px,py,1.8,'#FFFFFF',Math.sin(ph*Math.PI));}
      else{px+=Math.sin(s*.7+i)*4;py+=Math.cos(s*.9+i*1.3)*3;if(inPoly(px,py,P)){dot(px,py,3.6,'#FFD36B',.12+.1*Math.sin(s*2+i));dot(px,py,1.4,'#FFE9A8',.5+.45*Math.sin(s*2+i));}}
    }});
  x.globalAlpha=1;
  /* the place found today glows */
  const lp=state.lastPlace;if(lp&&lp.d===todayKey()&&tis.includes(lp.ti)&&placesFound(lp.ti)>lp.k){const q=placePts(lp.ti)[lp.k],ph=still?.3:(s%2.4)/2.4;
    x.globalAlpha=still?.8:(1-ph)*.9;x.strokeStyle='#FFD36B';x.lineWidth=1.2;x.beginPath();x.arc(q[0],q[1],8+ph*9,0,Math.PI*2);x.stroke();x.globalAlpha=1;}
  /* the wanderer on the trail */
  const wd=state.wander,c=wd&&cardById(wd.id);if(!c)return;
  let to=Number.isInteger(wd.realm)&&wd.realm>=0?wd.realm:-1;if(to<0){const ks=rKnown();if(!ks.length)return;to=ks[(wd.seed>>>0)%ks.length];}
  if((to>=5)!==back)return;
  const home=back?(shadeOpen(c.theme+5)?c.theme+5:to):c.theme,A=home===to?placePts(to)[0]:mapMid(polyOf(home)),B=mapMid(polyOf(to));
  const now=Date.now(),span=Math.max(1,wd.ready-wd.start),p=Math.max(0,Math.min(1,(now-wd.start)/span)),back2=p>=1;
  let f,dir=1;if(p<.45){f=p/.45;}else if(p<.55){f=1;}else{f=1-(p-.55)/.45;dir=-1;}
  const mx=(A[0]+B[0])/2+(B[1]-A[1])*.18,my=(A[1]+B[1])/2-(B[0]-A[0])*.18,q=1-f,px=q*q*A[0]+2*q*f*mx+f*f*B[0],py=q*q*A[1]+2*q*f*my+f*f*B[1];
  const im=mapFxSprite(c);if(!im)return;const sz=20,hop=still?0:(back2?Math.abs(Math.sin(s*5))*3:(Math.floor(s*4)%2));
  const wx=back2?A[0]:p>=.45&&p<.55?B[0]+Math.sin(s*1.5)*5:px,wy=back2?A[1]:p>=.45&&p<.55?B[1]+4:py;
  x.globalAlpha=.35;x.fillStyle='#000';x.beginPath();x.ellipse(wx,wy+2,6,2,0,0,Math.PI*2);x.fill();x.globalAlpha=1;
  x.save();x.translate(wx,wy-hop);if((B[0]-A[0])*dir<0){x.scale(-1,1);}x.drawImage(im,-sz/2,-sz,sz,sz);x.restore();
}
setTimeout(mapFxLoop,800);
function wakeLoops(){
  if(mapFxT){clearTimeout(mapFxT);mapFxT=0;mapFxStill=0;setTimeout(mapFxLoop,30);}""")
# remember the place found today (for the glow), and keep it valid
rep("state.disc=todayKey();place=`<div class=\"tale new\"><b>A new place on", "state.disc=todayKey();state.lastPlace={ti:dto,k:pf-1,d:todayKey()};place=`<div class=\"tale new\"><b>A new place on")
rep("if(s.wander)s.wander.realm=Number.isInteger(s.wander.realm)&&s.wander.realm>=0&&s.wander.realm<=9?s.wander.realm:-1;",
    "if(s.wander)s.wander.realm=Number.isInteger(s.wander.realm)&&s.wander.realm>=0&&s.wander.realm<=9?s.wander.realm:-1;\n  if(s.lastPlace!==undefined){const q=s.lastPlace;if(!q||typeof q!=='object'||!Number.isInteger(q.ti)||q.ti<0||q.ti>9||!Number.isInteger(q.k)||q.k<0||q.k>4||typeof q.d!=='string'||!/^\\d{4}-\\d{2}-\\d{2}$/.test(q.d))delete s.lastPlace;}")
rep("e.target.classList.contains('mphit')){e.preventDefault();", "(e.target.classList.contains('mphit')||e.target.classList.contains('mpplace'))){e.preventDefault();")
# the map caption mentions landmarks
rep("'<p class=\"muted small center\" style=\"margin:-4px 0 10px\">Tap a corner of the map to open its page.</p>'",
    "'<p class=\"muted small center\" style=\"margin:-4px 0 10px\">Tap a corner of the map to open its page, or a landmark to see it up close.</p>'")

# ---------- What's New ----------
rep("""    <ul class="newlist"><li><b>The other side.</b>""", """    <ul class="newlist"><li><b>A living map.</b> Every place on the map is now a little pixel landmark. Tap one to see it up close and send a Forgeling there. The realms are gently alive, with petals, smoke, glints, snow and fireflies, and while a Forgeling is out wandering you can watch it walk the trail, look around and come home.</li>
    <li><b>The other side.</b>""")
import re
src2 = re.sub(r"\n    <li><b>The Forge\.</b>.*?</li>", "", src, count=1, flags=re.S)
assert src2 != src; src = src2

open('work.html', 'w', encoding='utf8').write(src)
print('ok', len(src))

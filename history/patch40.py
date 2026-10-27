# Forgelings 0.40.0: Living Hearth. The Forgelings and their fire come alive:
#  - tap a Forgeling at the Hearth and it hops and says something (the fire still stirs when you tap elsewhere);
#  - on a card's close-up, tapping the art makes the creature itself hop inside its frame (the frame no longer jumps);
#  - after 10 pm everyone by the fire dozes, eyes shut, with drifting Zs; a tap wakes one for a few seconds;
#  - weather from the realm of whoever is sitting there: petals (Meadow), embers (Ember), rain (Tide), snow (Frost),
#    fireflies (Dusk), and glowing motes for each Shade;
#  - statues you have cast stand on little plinths at the edges of the scene.
# Reduced motion keeps the scene still as before. The Shade side moves to 0.41. Reads base39.html.
src = open('base39.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

# ---- state for taps, dozing and weather
rep("let hbg=null,hbgMode='',hImg=null,hfx=[];",
    "let hbg=null,hbgMode='',hImg=null,hfx=[],hPos=[],hWake={};\n"
    "/* 0.40: after 10 pm everyone by the fire dozes (a tap wakes one for a while) */\n"
    "const hLate=()=>{const h=new Date().getHours();return h>=22||h<6;};\n"
    "/* 0.40: weather from the realm of whoever is sitting by the fire: the most common realm, Shade if most are dark */\n"
    "function hWeather(cs){const t={};let dk=0,n=0;cs.forEach(c=>{t[c.theme]=(t[c.theme]||0)+1;dk+=c.dark?1:0;n++;});if(!n)return null;const ti=+Object.keys(t).sort((a,b)=>t[b]-t[a])[0];return {ti,dk:dk*2>n};}\n"
    "function drawWeather(setpx,W,t){if(!W)return;const ti=W.ti,dk=W.dk,G=hexRGB(dk?THEMES[ti].dark.glow:'#FFFFFF');\n"
    "  for(let k=0;k<18;k++){const s=(k*73)%128,sp=.6+((k*37)%10)/10,ph=(t/1000*sp*9+k*13);\n"
    "    if(ti===3&&!dk){const x=(s+Math.sin(t/900+k)*3+128)%128,y=ph%56;setpx(x,y,[255,255,255]);setpx(x,y+1,[196,212,236]);if(k%3===0){setpx(x+1,y,[255,255,255]);setpx(x+1,y+1,[196,212,236]);}}\n"
    "    else if(ti===2&&!dk){const y=(ph*2.2)%60,x=(s+y*.3)%128;for(let q=0;q<3;q++)setpx(x+q*.3,y+q,[96,156,214]);}\n"
    "    else if(ti===0&&!dk){if(k%3===2)continue;const x=(s+ph*.6)%128,y=(ph*.7+k*7)%50,q=k%4?[244,140,180]:[255,214,232];setpx(x,y,q);setpx(x+1,y,q);}\n"
    "    else if(ti===4&&!dk){if(k%3)continue;const on=Math.sin(t/430+k*2.1)>.1;if(on)setpx(s+Math.round(Math.sin(t/1700+k)*6),18+((k*11)%26)+Math.round(Math.cos(t/1300+k)*3),[255,224,138]);}\n"
    "    else if(ti===1&&!dk){if(k%2)continue;setpx(s+Math.sin(t/600+k)*2,52-(ph%50),[255,160,70]);}\n"
    "    else{if(k%2)continue;const up=ti!==3,y=up?52-(ph*.5%50):(ph*.5%52);if(Math.sin(t/500+k*1.7)>-.3)setpx(s+Math.sin(t/800+k)*3,y,G);}}}\n"
    "/* 0.40: statues stand on little plinths at the scene's edges, the two most recent */\n"
    "function drawStatues(setpx,t){const L=statues().slice(-2);L.forEach((c,j)=>{const g=prep(Object.assign({},c,{keep:c.statue.keep})),sp=g.sp[0]||(g.sp[0]=buildSprite(g.spec,0,0)),x0=j?111:1,y0=GYH-19;\n"
    "  for(let y=0;y<16;y++)for(let x=0;x<16;x++){const sl=sp[(2*y+1)*32+2*x+1]||sp[(2*y)*32+2*x];if(!sl)continue;setpx(x0+x,y0+y,g.pal[sl]);}\n"
    "  for(let x=-1;x<17;x++){setpx(x0+x,y0+16,[150,140,166]);setpx(x0+x,y0+17,[112,102,130]);setpx(x0+x,y0+18,[86,78,104]);}});}")
# ---- dozing, hops with an arc, and remembering where everyone stands
rep("    const still=(i===soloI&&soloV===8),bob=(slp||still)?0:Math.floor(to/520)%2,blink=slp?1:(still?((to%9000)<160?1:0):((to%3600)<140?1:0)),pulse=Math.floor(to/640)%2,si=bob*2+blink;",
    "    const dz=!slp&&hLate()&&!(hWake[c.id]&&t-hWake[c.id]<6000)&&!hfx.some(f=>f.i===i&&t-f.t0<1500);\n"
    "    const still=(i===soloI&&soloV===8),bob=(slp||still||dz)?0:Math.floor(to/520)%2,blink=(slp||dz)?1:(still?((to%9000)<160?1:0):((to%3600)<140?1:0)),pulse=Math.floor(to/640)%2,si=bob*2+blink;\n"
    "    hPos[i]=[p[0],p[1],c.id];")
rep("    let hop=0;hfx.forEach(f=>{if(f.i===i){const a=t-f.t0;if(a<420)hop=a<210?-2:-1;}});\n    if(slp)hop=Math.floor(t/1500+i)%2;else if(still)hop=Math.floor(t/3000)%2;",
    "    let hop=0;hfx.forEach(f=>{if(f.i===i){const a=t-f.t0;if(f.k==='hop'){if(a<640)hop=-Math.round(Math.sin(a/640*Math.PI)*6);}else if(a<420)hop=a<210?-2:-1;}});\n    if(slp||dz)hop=Math.floor(t/1500+i)%2;else if(still)hop=Math.floor(t/3000)%2;")
rep("    if(slp){const zt=((t/900)+i*.9)%3;", "    if(slp||dz){const zt=((t/900)+i*.9)%3;")
# weather behind everyone, statues on the hill
rep("  order.filter(i=>isSleep(i)).forEach(drawOne);",
    "  if(!heapOn)drawWeather(setpx,hWeather(cs.filter(c=>c.id!==outId)),t);\n  drawStatues(setpx,t);\n  hPos=[];\n  order.filter(i=>isSleep(i)).forEach(drawOne);")
# a hop has no badge above its head
rep("  hfx.forEach(f=>{const p=pos(f.i);if(!p)return;const a=t-f.t0,",
    "  hfx.forEach(f=>{if(f.k==='hop')return;const p=pos(f.i);if(!p)return;const a=t-f.t0,")
# ---- tapping a Forgeling at the Hearth
rep("  if(e.target.id==='hearthCv'){hearthPoke();if(state.hearth.sleep&&!sleepRun)startWake();return;}",
    "  if(e.target.id==='hearthCv'){if(!state.hearth.sleep&&hearthTap(e))return;hearthPoke();if(state.hearth.sleep&&!sleepRun)startWake();return;}")
rep("function fxAdd(i,k){hfx.push({i,k,t0:performance.now()});}",
    "function fxAdd(i,k){hfx.push({i,k,t0:performance.now()});}\n"
    "/* 0.40: a tap on a Forgeling makes it hop and say something; dozers wake for a few seconds */\n"
    "function hearthTap(e){const cv=e.target,r=cv.getBoundingClientRect();if(!r.width)return false;const x=(e.clientX-r.left)/r.width*HW,y=(e.clientY-r.top)/r.height*HH;\n"
    "  const hit=hPos.map((p,i)=>p&&x>=p[0]+5&&x<=p[0]+27&&y>=p[1]+4&&y<=p[1]+32?i:-1).filter(i=>i>=0).pop();if(hit===undefined)return false;\n"
    "  const c=cardById(hPos[hit][2]);if(!c)return false;const now=performance.now(),was=hLate()&&!(hWake[c.id]&&now-hWake[c.id]<6000);hWake[c.id]=now;fxAdd(hit,'hop');chime(0);\n"
    "  const n=c.nick||c.name,L=c.dark?SPEAK_DARK:SPEAK_CUTE;hf.msg=was?`${n} opens one eye, then hops up to say hello.`:L[rand(L.length)].replace(/\\{n\\}/g,n);const m=$('#hmsg');if(m)m.textContent=hf.msg;\n"
    "  if(REDUCE)drawHearth(now);return true;}")
# ---- the creature hops inside its card frame
rep("  const FS=R===3?FOIL3:R===4?FOIL4:null,OX=8,OY=4;",
    "  const ha=e.hopT?t-e.hopT:9e9,FS=R===3?FOIL3:R===4?FOIL4:null,OX=8,OY=4-(ha<620?Math.round(Math.sin(ha/620*Math.PI)*4):0);")
rep("  if(art){art.classList.remove('hop');void art.offsetWidth;art.classList.add('hop');}",
    "  {const cv=$('#stage .art canvas.pcv');if(cv&&cv._e){cv._e.hopT=performance.now();if(REDUCE)drawFrame(cv._e,cv,performance.now(),null);}}")
# What's new
rep("const SEEN_V=44;", "const SEEN_V=45;")
rep("""<ul class="newlist"><li><b>Voxel statues.</b>""",
    """<ul class="newlist"><li><b>A living Hearth.</b> Tap a Forgeling by the fire and it hops to say hello. After 10 pm everyone dozes, and a tap wakes one up. The weather follows whoever is sitting there: petals, embers, rain, snow or fireflies. Statues you have cast now stand at the edges of the scene. On a card, tap the art and the creature hops inside its frame.</li>
    <li><b>Voxel statues.</b>""")
_i=src.index('function openWhatsNew(){'); _j=src.index('</ul>',_i); _lis=src[_i:_j].split('<li>')
assert len(_lis)-1==9, len(_lis)-1
_k=src.rindex('<li>',_i,_j); _e=src.rindex('\n',_i,_k); src=src[:_e]+src[_j:]
rep('<title>Forgelings (prototype 0.39.0)</title>', '<title>Forgelings (prototype 0.40.0)</title>')
rep("const VERSION='prototype 0.39.0'", "const VERSION='prototype 0.40.0'")
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src.encode()))

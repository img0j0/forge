# 0.44: realm dioramas (Hunter approved the map canvas AA4V5DdFxJBDqQmZhhShtm, artboard "Meadow in 3D").
# A fully charted realm (all five places found) opens from its page on the Map as a small floating voxel island of its
# five places, drawn by the statue viewer. Turn left/right buttons, a place list that turns the island to face a place
# and lights it, the turntable chip. Built from the realm and its places alone; nothing new is stored.
import re,subprocess,sys
S=open('base431.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old)
    assert c==n,(c,n,old[:90])
    S=S.replace(old,new)

rep("const VERSION='prototype 0.43.1'","const VERSION='prototype 0.44.0'")
rep("<title>Forgelings (prototype 0.43.1)</title>","<title>Forgelings (prototype 0.44.0)</title>")
rep("SEEN_V=48","SEEN_V=49")

# ---- shader: a place can be lit (hl = place index + 1; 0 lights nothing, so statues draw exactly as before)
rep("uniform float T,holo,rise;uniform vec3 eye,gc;","uniform float T,holo,rise,hl;uniform vec3 eye,gc;")
rep("col=mix(col,vc*(1.25+.25*sin(T*3.+vw.x)),ve);gl_FragColor=vec4(col,1.);}';",
    "col=mix(col,vc*(1.25+.25*sin(T*3.+vw.x)),ve);if(hl>.5&&abs(vh-hl)<.5)col+=gc*(.26+.1*sin(T*3.));gl_FragColor=vec4(col,1.);}';")

# ---- statueView takes a ready-made scene (o.scene) instead of a card's figure and stand
rep("""const u32=gl.getExtension('OES_element_index_uint'),st=statueStand(c.theme,c.dark),fig=statueFigure(c,o.clay);if(o.clay)st.gc=[.78,.72,.9];""",
    """const u32=gl.getExtension('OES_element_index_uint'),sc=o.scene,st=sc||statueStand(c.theme,c.dark),fig=sc?new Map():statueFigure(c,o.clay);if(o.clay)st.gc=[.78,.72,.9];""")
rep("""const mFig=stvMesh([fig],0),mAll=stvMesh([fig,st.S],0);
  if((mFig.big||mAll.big)&&!u32)return null;""",
    """const mFig=sc?null:stvMesh([fig],0),mAll=sc?stvMesh([st.S],0):stvMesh([fig,st.S],0);
  if(((mFig&&mFig.big)||mAll.big)&&!u32)return null;""")
rep("""const gFig=up(mFig),gAll=up(mAll),pBuf""","""const gFig=mFig?up(mFig):null,gAll=up(mAll),pBuf""")
rep("""holo=o.clay?0:c.rarity===3?1:c.rarity===4?2:0;""","""holo=o.clay||sc?0:c.rarity===3?1:c.rarity===4?2:0;""")
rep("""const v={yaw:-.35,pitch:.28,zoom:1,""","""const v={yaw:sc?.5:-.35,pitch:sc?.36:.28,zoom:1,hl:0,goal:null,""")
rep("""if(v.rise<1)v.rise=Math.min(1,v.rise+dt/2.2);const T=REDUCE?0:t/1000;""",
    """if(v.rise<1)v.rise=Math.min(1,v.rise+dt/2.2);const T=REDUCE?0:t/1000;
    if(v.goal!=null){const d=Math.atan2(Math.sin(v.goal-v.yaw),Math.cos(v.goal-v.yaw));if(REDUCE||Math.abs(d)<.004){v.yaw+=d;v.goal=null;}else{v.yaw+=d*Math.min(1,dt*5);v.idle=0;}}""")
rep("""const as=cv.width/cv.height,dist=(as<.8?96:76)/v.zoom,ct=[0,v.base?12:fh/2,0],""",
    """const as=cv.width/cv.height,dist=(as<.8?96:76)*(sc?sc.dist:1)/v.zoom,ct=[0,sc?sc.cy:v.base?12:fh/2,0],""")
rep("""gl.uniform3fv(U('eye'),eye);gl.uniform3fv(U('gc'),st.gc);""","""gl.uniform3fv(U('eye'),eye);gl.uniform3fv(U('gc'),st.gc);gl.uniform1f(U('hl'),v.hl);""")

ISLE=r"""
/* ---- 0.44: realm dioramas. A fully charted realm opens as a small floating voxel island of its five places, drawn by
   the statue viewer. Everything comes from the realm and its places, so nothing is stored. ---- */
function isleScene(ti){
  const b=ti%5,dk=ti>=5,T=THEMES[b],P=dk?T.dark:T.cute,hx=h=>hexRGB(h).map(v=>v/255),S=new Map(),pts=[],spots=[];
  let a=(ti*131+17)|0;const rnd=()=>{a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};
  const put=(x,y,z,h,e,id)=>S.set(x+','+y+','+z,{c:typeof h==='string'?hx(h):h,f:null,e:e||0,h:id||0});
  const mix=(h,k)=>hx(h).map(v=>Math.min(1,v*k)),pick=A=>A[(rnd()*A.length)|0];
  const G=P.ground,glow=dk?P.glow:P.accent,top=[hx(G[0]),hx(G[1]),mix(G[0],.88)],side=[mix(G[1],.62),mix(G[1],.52),mix(G[0],.56)],rock=dk?[hx('#2A2438'),hx('#221D30'),hx('#302940')]:[hx('#8C7A68'),hx('#7A6A5A'),hx('#9A8774')];
  const R=22,crack=(x,z,r)=>(Math.abs(Math.sin(x*.45+z*.2)+Math.cos(z*.38-x*.15))<.2)&&r>7;
  for(let x=-R;x<=R;x++)for(let z=-R;z<=R;z++){const r=Math.hypot(x,z*1.1),edge=R-rnd()*2.2;if(r>edge)continue;
    const f=1-r/edge,dep=2+Math.round(Math.pow(f,.75)*15+rnd()*2.5);
    for(let y=-dep;y<0;y++){let c3=y===-1?pick(top):y>-4?pick(side):pick(rock),e=0;
      if(y===-1){if(b===1&&crack(x,z,r)&&rnd()<.85){c3=hx(rnd()<.5?glow:(dk?P.glow2:'#FF9F43'));e=1;}
        else if((dk||b===4)&&b!==1&&crack(x,z,r)&&rnd()<.5){c3=hx(glow);e=dk?.9:.6;}}
      put(x,y,z,c3,e);}}
  /* the five places sit in a ring; each place's blocks carry its number so it can be lit */
  const off=-Math.PI/2+.35;
  PLACES[ti].forEach((p,i)=>{const an=off+i*Math.PI*2/5,rr=i===0?11:13,ox=Math.round(Math.cos(an)*rr),oz=Math.round(Math.sin(an)*rr);spots.push([ox,oz]);
    const L=(x,y,z,c,e)=>put(ox+x,y,oz+z,c,e,i+1),ux=ox/(Math.hypot(ox,oz)||1),uz=oz/(Math.hypot(ox,oz)||1);
    const stone=dk?['#4A4458','#3A3548','#55506A']:['#A8A196','#B9B2A6','#958E83'],wood=dk?'#2A2018':'#7A5230',body=dk?P.bodies:T.cute.bodies;
    const leaf=dk?[G[0],G[1],mix(G[0],1.3)]:b===1?['#D9583B','#E8744A','#C9472E']:b===3?['#DCEFF7','#BFE6FF','#FFFFFF']:b===2?['#5FB878','#4FA36A']:[G[0],G[1],'#5FA85A'];
    const k=p.k;
    if(k==='hill'){let hh=0;for(let x=-5;x<=5;x++)for(let z=-5;z<=5;z++){const d=Math.hypot(x,z),h=Math.round(4.6*(1-d/5.6));for(let y=0;y<h;y++)L(x,y,z,y===h-1?pick(top):pick(side));if(!x&&!z)hh=h;}
      L(0,hh,0,body[1]);L(0,hh+1,0,body[1]);L(0,hh+2,0,mix(body[1],1.15));}
    else if(k==='tree'){for(let y=0;y<7;y++)L(0,y,0,wood);for(let x=-4;x<=4;x++)for(let y=-3;y<=3;y++)for(let z=-4;z<=4;z++)if(Math.hypot(x,y*1.25,z)<3.9&&rnd()<.93){const g=dk&&rnd()<.07;L(x,9+y,z,g?glow:pick(leaf),g?.9:0);}
      if(b===1&&dk)for(let q=0;q<6;q++)L(Math.round(Math.cos(q)*4),8,Math.round(Math.sin(q)*4),'#E8B93C',.5);}
    else if(k==='star'){for(let x=-3;x<=3;x++)for(let z=-3;z<=3;z++){if(Math.hypot(x,z)>3.4||(!x&&!z)||rnd()<.4)continue;const h=1+(rnd()<.4);for(let y=0;y<h;y++)L(x,y,z,y===h-1?pick(body):leaf[0],0);}
      for(let y=0;y<3;y++)L(0,y,0,stone[1]);L(0,3,0,glow,1);L(1,4,0,glow,.8);L(-1,4,0,glow,.8);L(0,4,1,glow,.8);L(0,4,-1,glow,.8);L(0,5,0,glow,1);}
    else if(k==='zig'){const path=dk?'#5A4A3A':'#C9A878';for(let t=-6;t<=6;t++){const x=Math.round(t*uz*-1+Math.sin(t*.9)*2*ux),z=Math.round(t*ux+Math.sin(t*.9)*2*uz);L(x,-1,z,path);
        if(t%2===0){const s=t%4===0?2:-2,bx=x+Math.round(s*ux),bz=z+Math.round(s*uz),th=dk?['#2A3A2A','#1E2B20']:['#3E6B3A','#2F5A30'];L(bx,0,bz,pick(th));if(rnd()<.6)L(bx,1,bz,pick(th));if(dk&&rnd()<.5)L(bx,2,bz,glow,.8);}}
      if(b===4)for(let t=-6;t<=6;t++)L(Math.round(t*uz*-1+Math.sin(t*.9)*2*ux),0,Math.round(t*ux+Math.sin(t*.9)*2*uz),'#D9475A',.25);}
    else if(k==='stone'){for(let x=-3;x<=3;x++)for(let z=-2;z<=2;z++){if(Math.abs(x)===3&&Math.abs(z)===2)continue;L(x,0,z,stone[0]);L(x,1,z,Math.abs(x)<3&&Math.abs(z)<2?stone[1]:stone[2]);}}
    else if(k==='cave'){for(let x=-5;x<=5;x++)for(let z=-5;z<=5;z++){const d=Math.hypot(x,z),h=Math.round(6*(1-d/5.8)),al=x*ux+z*uz,pp=-x*uz+z*ux;for(let y=0;y<h;y++){if(al>-.5&&Math.abs(pp)<1.6&&y<3)continue;L(x,y,z,y===h-1?pick(rock):pick(side));}}
      L(Math.round(-ux),0,Math.round(-uz),glow,1);L(Math.round(-ux),1,Math.round(-uz),glow,.8);}
    else if(k==='gem'){for(const [cx,cz,h] of [[0,0,8],[2,1,5],[-2,1,4],[1,-2,6],[-1,-2,3]])for(let y=0;y<h;y++){L(cx,y,cz,glow,y>h-3?1:.5);if(y<h-3&&rnd()<.5)L(cx+(rnd()<.5?1:-1),y,cz,mix(glow,.75),.3);}}
    else if(k==='pool'){const w=dk?(b===2?'#1D6F7A':'#1D3A6B'):b===3?'#9FD3F0':'#4FA9D9';for(let x=-5;x<=5;x++)for(let z=-5;z<=5;z++){const d=Math.hypot(x,z);if(d<3.6)L(x,-1,z,rnd()<.25?mix(w,1.15):w,dk?.45:.18);else if(d<4.6&&rnd()<.7)L(x,0,z,pick(stone));}}
    else if(k==='dots'){for(let q=0;q<12;q++){const an2=rnd()*6.283,r2=rnd()*4.5,x=Math.round(Math.cos(an2)*r2),z=Math.round(Math.sin(an2)*r2);L(x,0,z,dk&&q%3===0?glow:rnd()<.5?pick(stone):pick(body),dk&&q%3===0?.7:0);if(dk&&q%3===0)L(x,1,z,'#C4FFF8',.5);}}
    else if(k==='tower'){for(let y=0;y<11;y++)for(let x=-1;x<=1;x++)for(let z=-1;z<=1;z++)L(x,y,z,y===0?stone[0]:pick(stone));
      for(const [x,z] of [[2,0],[-2,0],[0,2],[0,-2]])L(x,8,z,dk?glow:'#FFE08A',.9);
      for(let y=11;y<14;y++){const w=13-y;for(let x=-w;x<=w;x++)for(let z=-w;z<=w;z++)L(x,y,z,dk?P.accent:b===2?'#FF8FA3':'#A8463A',dk?.3:0);}
      if(dk&&b===2)for(let y=14;y<22;y++)L(0,y,0,glow,.9);}
    else if(k==='arch'){for(const x of [-3,3])for(let y=0;y<6;y++){L(x,y,0,pick(stone));L(x,y,1,pick(stone));}for(let x=-3;x<=3;x++){L(x,6,0,stone[1]);L(x,6,1,stone[1]);if(Math.abs(x)<2){L(x,7,0,stone[2]);L(x,7,1,stone[2]);}}
      if(b===3)for(const [x,y] of [[-1,3],[0,4],[1,3]])L(x,y,0,dk?glow:'#FFF3C4',.9);if(b===2&&!dk)for(let x=-2;x<=2;x++)L(x,-1,0,'#4FA9D9',.2);}
    else if(k==='bell'){for(let x=-4;x<=4;x++)for(let z=-4;z<=4;z++){const d=Math.hypot(x,z),h=Math.round(5*(1-d/4.6));for(let y=0;y<h;y++)L(x,y,z,y===h-1?'#FFFFFF':dk?'#5A6480':'#DCE8FA');}
      for(const x of [-2,2])for(let y=5;y<9;y++)L(x,y,0,wood);for(let x=-2;x<=2;x++)L(x,9,0,wood);for(let x=-1;x<=0;x++)for(let y=6;y<8;y++)for(let z=0;z<=1;z++)L(x,y,z-0,'#E8B93C',.2);}
    else if(k==='house'){const wall=dk?'#3B2B1E':'#C99B6A',roof=dk?'#2A2140':'#A8463A';for(let x=-2;x<=2;x++)for(let z=-2;z<=2;z++)for(let y=0;y<4;y++){const edge2=Math.abs(x)===2||Math.abs(z)===2;if(!edge2)continue;const win=y>0&&y<3&&((Math.abs(x)===2&&!z)||(Math.abs(z)===2&&!x));L(x,y,z,win?'#FFE08A':wall,win?1:0);}
      for(let y=4;y<7;y++){const w=6-y;for(let x=-w-1;x<=w+1;x++)for(let z=-w;z<=w;z++)L(x,y,z,roof);}for(let y=5;y<9;y++)L(2,y,1,stone[0]);}
    else if(k==='key'){for(let x=-2;x<=2;x++)for(let y=0;y<7;y++){const hole=!x&&(y===2||y===3||y===4)||(Math.abs(x)===1&&y===4);if(hole)continue;L(Math.round(x*-uz),y,Math.round(x*ux),y===6||Math.abs(x)===2?stone[0]:pick(stone));}
      L(Math.round(ux*2),1,Math.round(uz*2),'#FFD36B',.7);L(Math.round(ux*2),2,Math.round(uz*2),'#FFD36B',.7);for(let y=2;y<5;y++)L(Math.round(-ux),y,Math.round(-uz),glow,1);}
  });
  /* grass, snow and little flowers between the places */
  for(let q=0;q<120;q++){const an=rnd()*6.283,r=rnd()*19,x=Math.round(Math.cos(an)*r),z=Math.round(Math.sin(an)*r);if(spots.some(([sx,sz])=>Math.hypot(x-sx,z-sz)<6)||S.has(x+',0,'+z)||!S.has(x+',-1,'+z))continue;
    const fl=rnd()<.3;put(x,0,z,fl?(dk?glow:pick(T.cute.bodies)):(b===3&&!dk?'#FFFFFF':pick(side)),fl&&dk?.8:0);}
  for(const [k,o] of S)if(o.e>.5&&rnd()<.18){const [x,y,z]=k.split(',').map(Number);pts.push(x+.5,y+1,z+.5,20,0);}
  for(let i=0;i<90;i++){const an=rnd()*6.283,r=5+rnd()*22;pts.push(Math.cos(an)*r,b===3?30:-2,Math.sin(an)*r,.55+rnd()*.6,.05+rnd()*.95);}
  const pc={0:dk?P.glow:'#FFB7D0',1:'#FFB347',2:dk?P.glow:'#D6F2FF',3:'#FFFFFF',4:dk?P.glow:'#FFE08A'}[b];
  return {S,pts,pc:hx(pc),gc:hx(glow),fall:b===3?1:0,spots,cy:-1,dist:1.02};
}
function openIsle(ti){
  if(!(ti>=0&&ti<=9)||placesFound(ti)<5)return;if(stv){stv.stop();stv=null;}
  const nm=mapName(ti),b=ti%5,dk=ti>=5,gc=dk?THEMES[b].dark.glow:THEMES[b].cute.accent,PL=PLACES[ti];
  openOverlay(`<div class="stview isle" style="--sg:${gc}"><p class="islek">Fully charted</p><p class="rv-title">${esc(nm)}</p><p class="stsub">${dk?'The other side of '+esc(THEMES[b].name)+'. ':''}Five places, all found. Turn it to look around.</p>
    <div class="stcan"><canvas id="stCv" tabindex="0" role="img" aria-label="${esc(nm)} as a small floating island of its five places: ${PL.map(p=>esc(p.n)).join(', ')}. Drag to turn it, pinch or scroll to zoom, arrow keys to turn."></canvas><p class="stno" id="stNo" hidden>This phone could not start 3D drawing, so ${esc(nm)} stays on the map for now.</p></div>
    <div class="row stbtns"><button class="chip" id="isL">Turn left</button><button class="chip" id="isR">Turn right</button><button class="chip" id="stTurn" aria-pressed="${!REDUCE}">Turntable</button></div>
    <ul class="islelist">${PL.map((p,i)=>`<li><button data-isp="${i}" aria-pressed="false"><b>${esc(p.n)}.</b> ${esc(p.x)}</button></li>`).join('')}</ul>
    <button class="ghost" id="ovClose">Close</button></div>`,true);
  ovMode='statue';stvId=null;
  const cv=$('#stCv'),sc=isleScene(ti);stv=statueView(cv,{rarity:0},{scene:sc});
  if(stv)stv.spots=sc.spots;else{cv.hidden=true;$('#stNo').hidden=false;['isL','isR','stTurn'].forEach(i=>{const x=$('#'+i);if(x)x.hidden=true;});}
  const f=$('#ovClose');if(f)f.focus({preventScroll:true});
}
function isleTurn(goal,hl){
  if(!stv)return;const v=stv.v;v.goal=goal;v.idle=0;
  if(hl!=null){v.hl=hl;if(v.turn){v.turn=false;const t=$('#stTurn');if(t)t.setAttribute('aria-pressed','false');}
    document.querySelectorAll('#modal [data-isp]').forEach(x=>x.setAttribute('aria-pressed',String(+x.dataset.isp+1===hl)));}
  stv.kick();
}
document.addEventListener('click',e=>{const x=e.target.closest&&e.target.closest('[data-isle]');if(x)openIsle(+x.dataset.isle);});
"""
rep("""function openStatue(id,o){""",ISLE.strip()+"\nfunction openStatue(id,o){")

# the realm pages: a button once all five places are found
rep("""  out+=placesListHTML(ti);
  if(loreOn()){const tp=talePages(ti);""","""  out+=placesListHTML(ti)+isleBtn(ti);
  if(loreOn()){const tp=talePages(ti);""")
rep("""  out+=placesListHTML(si);
  if(loreOn()){const tp=talePages(si);""","""  out+=placesListHTML(si)+isleBtn(si);
  if(loreOn()){const tp=talePages(si);""")
rep("""function placesListHTML(ti){""","""const isleBtn=ti=>placesFound(ti)===5?`<button class="chip isgo" data-isle="${ti}">See ${esc(mapName(ti))} in 3D</button>`:'';
function placesListHTML(ti){""")

# overlay buttons
rep("""  else if(b.id==='stPic'){const c=cardById(stvId);if(c)statuePicture(c);}""",
    """  else if(b.id==='stPic'){const c=cardById(stvId);if(c)statuePicture(c);}
  else if(b.id==='isL'||b.id==='isR'){if(stv)isleTurn((stv.v.goal!=null?stv.v.goal:stv.v.yaw)+(b.id==='isL'?1:-1)*Math.PI/4);}
  else if(b.dataset.isp!=null){if(stv&&stv.spots){const i=+b.dataset.isp,s=stv.spots[i];if(stv.v.hl===i+1)isleTurn(null,0);else isleTurn(Math.atan2(s[0],s[1]),i+1);}}""")

CSS=""".isle .stcan{height:min(44vh,420px)}
.islek{margin:0;font:700 11px/1.2 var(--body,inherit);letter-spacing:.12em;text-transform:uppercase;color:#FFD36B}
.isle .stsub{margin:-4px 0 0;color:#D2C9EE;font-weight:400;text-align:center}
.islelist{list-style:none;margin:0;padding:0;width:min(100%,560px);display:grid;gap:4px}
.islelist button{display:block;width:100%;min-height:44px;padding:8px 12px;border:0;background:#F7EEDA;color:#3A2E22;font:400 13px/1.4 var(--body,inherit);text-align:left;cursor:pointer}
.islelist button[aria-pressed="true"]{background:#FFE9A8;box-shadow:inset 4px 0 0 #8A5A00}
.isgo{display:block;margin:8px 0 0;min-height:44px}
"""
rep(""".stbtns{justify-content:center;gap:8px;flex-wrap:wrap}""",""".stbtns{justify-content:center;gap:8px;flex-wrap:wrap}
"""+CSS.strip())

# What's New: newest first, keep eight
rep("""<ul class="newlist"><li><b>Safer saving.</b>""","""<ul class="newlist"><li><b>Realms in 3D.</b> Find all five places in a realm, and its page on the Map opens it as a small floating island you can turn. Tap a place to turn it into view.</li><li><b>Safer saving.</b>""")
m=re.search(r'<li><b>Ink\.</b>.*?</li>',S);assert m;rep(m.group(0),"")

open('work.html','w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S)
open('/tmp/chk44.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk44.js'],capture_output=True,text=True)
print('node --check',r.returncode,r.stderr[:800])

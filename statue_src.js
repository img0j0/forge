/* ================= 0.39: Voxel Statues =================
   A Forgebound Forgeling can be cast as a 3D statue at the Forge for 6 embers. The statue is built on the phone from
   the creature's own sprite and palette (the keepsake it wore when cast, Holo/Legend foil frozen as on its card), set on
   a stand from its realm, and drawn by a small WebGL renderer: only faces that touch air, soft shadow in the corners,
   a warm and a cool rim light, a slow sheen for Holo and Legend. c.statue = {at:'YYYY-MM-DD', keep:'<keepsake id>'}. */
const STATUE_EMB=6;
const statueReady=c=>!!c&&!c.statue&&bondLevel(c)>=5;
const statues=()=>state.cards.filter(c=>c.statue);
let stv=null; /* the open viewer: {stop, shot} */
function statueSprite(c){
  const cc=Object.assign({},c,{keep:c.statue?c.statue.keep:(c.keep||'')}),spec=genSpec(cc),pl=makePal(spec,cc),g=buildSprite(spec,0,0),R=c.rarity,FS=R===3?FOIL3:R===4?FOIL4:null;
  const col=new Array(1024).fill(null),out=new Uint8Array(1024);
  for(let i=0;i<1024;i++){const sl=g[i];if(!sl)continue;let [r,gg,b]=pl.pal[sl];
    if((FS&&FS[sl])||(c.bond>=25&&sl===1)){const x=i%32+8,y=(i>>5)+4;
      if(R===3){const q=RAINBOW[Math.floor((((x+y)*.045)%1)*12)%12];r=lerp(r,q[0],.7);gg=lerp(gg,q[1],.7);b=lerp(b,q[2],.7);}
      else{const q=GOLD[Math.floor((((x+y)*.05)%1)*6)%6];r=lerp(r,q[0],.85);gg=lerp(gg,q[1],.85);b=lerp(b,q[2],.85);}}
    col[i]=[r/255,gg/255,b/255];out[i]=sl===1?1:0;}
  return {col,out};
}
/* pixels to blocks: depth from the distance to the silhouette edge; the outline is painted on the front and back faces
   only (its sides are body); small features (eyes, mouth, markings) sit one block proud of the face */
function statueFigure(c){
  const {col,out}=statueSprite(c),W=32,V=new Map(),dist=new Float32Array(1024).fill(99),key=a=>a.map(v=>Math.round(v*255)).join(',');
  for(let i=0;i<1024;i++){const x=i&31,y=i>>5;if(!col[i])dist[i]=0;else if(!x||!y||x===31||y===31)dist[i]=1;}
  for(let p=0;p<2;p++)for(let k=0;k<1024;k++){const i=p?1023-k:k,x=i&31,y=i>>5;if(!dist[i])continue;
    for(const [dx,dy,w] of [[-1,0,1],[1,0,1],[0,-1,1],[0,1,1],[-1,-1,1.4],[1,-1,1.4],[-1,1,1.4],[1,1,1.4]]){const X=x+dx,Y=y+dy,d=(X<0||Y<0||X>31||Y>31)?0:dist[Y*W+X];if(d+w<dist[i])dist[i]=d+w;}}
  const cnt={};col.forEach((c3,i)=>{if(c3&&!out[i]){const k=key(c3);cnt[k]=(cnt[k]||0)+1;}});
  const bk=Object.keys(cnt).sort((a,b)=>cnt[b]-cnt[a])[0],BODY=bk?bk.split(',').map(v=>v/255):[.4,.3,.25],RIM=BODY.map(v=>v*.78);
  const reg=new Int32Array(1024).fill(-1),rs=[];
  for(let i=0;i<1024;i++){if(!col[i]||reg[i]>=0)continue;const id=rs.length,k0=key(col[i]),st=[i];reg[i]=id;let n=0;
    while(st.length){const j=st.pop();n++;const x=j&31,y=j>>5;for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1]]){const X=x+dx,Y=y+dy;if(X<0||Y<0||X>31||Y>31)continue;const q=Y*W+X;if(reg[q]<0&&col[q]&&key(col[q])===k0){reg[q]=id;st.push(q);}}}rs.push(n);}
  const feat=i=>col[i]&&!out[i]&&key(col[i])!==bk&&rs[reg[i]]<=14&&dist[i]>=2;
  let foot=31;for(let i=1023;i>=0;i--)if(col[i]){foot=i>>5;break;}
  const put=(x,y,z,c3,f,h)=>V.set(x+','+y+','+z,{c:c3,f:f||null,e:0,h:h});
  for(let i=0;i<1024;i++){if(!col[i])continue;const x=i&31,y=i>>5,d=dist[i];
    const half=out[i]?Math.max(1,Math.min(4,Math.round(1+1.3*Math.sqrt(d)))):Math.max(1,Math.min(6,Math.round(1+1.55*Math.sqrt(d))));
    const X=x-16,Y=foot-y;
    for(let z=-half;z<half;z++){
      if(out[i]){put(X,Y,z,RIM,(z===half-1||z===-half)?col[i]:null,1);continue;}
      put(X,Y,z,feat(i)&&z<half-1?BODY:col[i],null,1);}
    if(feat(i))put(X,Y,half,col[i],null,0);}
  return V;
}
/* ten stands: each realm, bright and Shade. Everything comes from the realm's palette. */
function statueStand(ti,dk){
  const T=THEMES[ti],P=dk?T.dark:T.cute,hx=h=>hexRGB(h).map(v=>v/255),S=new Map(),pts=[];
  let a=(ti*97+(dk?7:3))|0;const rnd=()=>{a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};
  const put=(x,y,z,h,e)=>S.set(x+','+y+','+z,{c:typeof h==='string'?hx(h):h,f:null,e:e||0,h:0});
  const mix=(h,k)=>hx(h).map(v=>Math.min(1,v*k));
  const G=P.ground,top=[hx(G[0]),hx(G[1]),mix(G[0],.85)],side=[mix(G[1],.62),mix(G[1],.5),mix(G[0],.55)];
  const glow=dk?P.glow:P.accent,R=20;
  const crack=(x,z,r)=>(Math.abs(Math.sin(x*.45+z*.2)+Math.cos(z*.38-x*.15))<.22)&&r>9;
  for(let x=-R;x<=R;x++)for(let z=-R;z<=R;z++){const r=Math.hypot(x,z*1.15);if(r>R-rnd()*2.5)continue;const hgt=r<11?2:(rnd()<.35?3:rnd()<.5?1:2);
    for(let y=-hgt;y<0;y++){let c3=y===-1?top[(rnd()*3)|0]:side[(rnd()*3)|0],e=0;
      if(y===-1){if(ti===1&&crack(x,z,r)&&rnd()<.85){c3=hx(rnd()<.5?glow:(dk?P.glow2:'#FF9F43'));e=1;}
        else if(ti===2&&!dk&&r>12&&r<16&&z>0){c3=hx(rnd()<.5?'#4FA9D9':'#5FC4C0');e=.15;}
        else if((dk||ti===4)&&ti!==1&&crack(x,z,r)&&rnd()<.5){c3=hx(glow);e=dk?.9:.6;}}
      put(x,y,z,c3,e);}
    if(r>R-5&&rnd()<.16)put(x,0,z,side[(rnd()*3)|0]);
    if(r>8&&r<R-2&&rnd()<.05){if(ti===0)put(x,0,z,dk?P.glow:T.cute.bodies[(rnd()*5)|0],dk?.8:0);else if(ti===3&&!dk)put(x,0,z,'#FFFFFF');}}
  const cone=(ox,oz,hgt,r0,body,tip,e)=>{for(let y=0;y<hgt;y++){const rr=Math.max(1.4,r0-y*r0/hgt*.85);for(let x=-r0;x<=r0;x++)for(let z=-r0;z<=r0;z++){const d=Math.hypot(x,z);if(d>rr||(d<rr-1.6&&y<hgt-1))continue;const t=y>hgt-3;put(x+ox,y,z+oz,t?tip:body[(rnd()*body.length)|0],t?e:0);}}};
  if(ti===1){for(let y=0;y<18;y++){const rr=Math.max(1.6,7.5-y*.36);for(let x=-8;x<=8;x++)for(let z=-8;z<=8;z++){const d=Math.hypot(x,z);if(d>rr||(d<rr-1.6&&y<17))continue;
      const flow=(Math.abs(x-z*.4-Math.sin(y*.55)*1.2)<1.1&&z>-1)||(y>15&&d<2.6);put(x+15,y,z-16,flow?hx(rnd()<.5?glow:'#FFB347'):side[(rnd()*3)|0],flow?1:0);}}}
  else if(ti===0){for(let y=0;y<9;y++)put(14,y,-15,dk?'#2A2018':'#7A5230');for(let x=-5;x<=5;x++)for(let y=-4;y<=4;y++)for(let z=-5;z<=5;z++)if(Math.hypot(x,y*1.2,z)<5.2&&rnd()<.92)put(14+x,12+y,-15+z,dk?(rnd()<.06?P.glow:G[0]):(rnd()<.5?G[0]:G[1]),dk&&rnd()<.06?.9:0);}
  else if(ti===2){cone(15,-15,14,4,dk?[G[0],G[1]]:['#B9A27A','#9E8A62'],dk?P.glow:P.accent,dk?.9:.3);if(!dk)for(let y=0;y<6;y++)put(-14,y,-12,'#FF8FA3');}
  else if(ti===3){for(const [ox,oz,h] of [[14,-15,15],[18,-11,9],[10,-18,7]])for(let y=0;y<h;y++){const rr=Math.max(.6,2.2-y*2.2/h);for(let x=-2;x<=2;x++)for(let z=-2;z<=2;z++)if(Math.hypot(x,z)<=rr)put(ox+x,y,oz+z,dk?P.accent:'#BFE6FF',dk?.5:.15);}}
  else{for(let y=0;y<12;y++)put(14,y,-14,dk?'#1A1030':'#3B2B1E');for(let x=-1;x<=1;x++)for(let y=12;y<15;y++)for(let z=-1;z<=1;z++)put(14+x,y,-14+z,glow,1);}
  for(const [k,o] of S)if(o.e>.5&&rnd()<.22){const [x,y,z]=k.split(',').map(Number);pts.push(x+.5,y+1,z+.5,22,0);}
  for(let i=0;i<70;i++){const an=rnd()*6.283,r=6+rnd()*17;pts.push(Math.cos(an)*r,ti===3?26:0,Math.sin(an)*r,.55+rnd()*.6,.05+rnd()*.95);}
  const pc={0:dk?P.glow:'#FFB7D0',1:'#FFB347',2:dk?P.glow:'#D6F2FF',3:'#FFFFFF',4:dk?P.glow:'#FFE08A'}[ti];
  return {S,pts,pc:hx(pc),gc:hx(glow),fall:ti===3?1:0};
}
const STV_VS='attribute vec3 p,n,c;attribute float a,e,h;uniform mat4 M;varying vec3 vc,vn,vw;varying float va,ve,vh;void main(){vc=c;vn=n;va=a;ve=e;vh=h;vw=p;gl_Position=M*vec4(p,1.);}';
const STV_FS='precision mediump float;varying vec3 vc,vn,vw;varying float va,ve,vh;uniform float T,holo,rise;uniform vec3 eye,gc;vec3 hsv(float h){return clamp(abs(mod(h*6.+vec3(0,4,2),6.)-3.)-1.,0.,1.);}'
 +'void main(){if(vh>-1.&&vw.y>rise)discard;vec3 L=normalize(vec3(.45,.8,.55));float d=max(dot(vn,L),0.);vec3 col=vc*(.48+.85*d)*(.42+.58*va);vec3 V=normalize(eye-vw);float rim=pow(1.-max(dot(vn,V),0.),2.2);'
 +'col+=rim*(vn.x>0.?gc*.35:vec3(.55,.35,1.)*.28);col+=gc*.16*clamp(1.-vw.y/10.,0.,1.)*max(dot(vn,vec3(0,-.2,1)),0.);'
 +'if(holo>.5&&vh>.5){float s=pow(sin(vw.x*.35+vw.y*.25-T*1.6)*.5+.5,6.)*(.4+rim);col=mix(col,col+(holo>1.5?vec3(1.,.85,.4):hsv(fract(vw.x*.03+vw.y*.05-T*.15)))*.35,s);}'
 +'col=mix(col,vc*(1.25+.25*sin(T*3.+vw.x)),ve);gl_FragColor=vec4(col,1.);}';
const STV_PV='attribute vec3 p;attribute float s,k;uniform mat4 M;uniform float T,px,fall;varying float vk,vl;void main(){vec3 q=p;float life=fract(T*.06*(.6+k)+k*7.);vk=k;vl=life;if(k>0.){q.y+=(fall>.5?-life:life)*28.;q.x+=sin(T*.9+k*20.)*1.5;}gl_Position=M*vec4(q,1.);gl_PointSize=s*px/gl_Position.w;}';
const STV_PF='precision mediump float;varying float vk,vl;uniform vec3 pc,gc;void main(){vec2 d=gl_PointCoord-.5;if(vk>0.){if(max(abs(d.x),abs(d.y))>.5)discard;gl_FragColor=vec4(pc,(1.-vl)*smoothstep(0.,.15,vl));}else gl_FragColor=vec4(gc,smoothstep(.5,0.,length(d))*.22);}';
function stvMesh(sets,fig){
  const has=k=>sets.some(s=>s.has(k)),F=[[[1,0,0],[[1,0,0],[1,1,0],[1,1,1],[1,0,1]]],[[-1,0,0],[[0,0,1],[0,1,1],[0,1,0],[0,0,0]]],[[0,1,0],[[0,1,1],[1,1,1],[1,1,0],[0,1,0]]],[[0,-1,0],[[0,0,0],[1,0,0],[1,0,1],[0,0,1]]],[[0,0,1],[[1,0,1],[1,1,1],[0,1,1],[0,0,1]]],[[0,0,-1],[[0,0,0],[0,1,0],[1,1,0],[1,0,0]]]];
  const P=[],N=[],C=[],A=[],E=[],H=[],I=[];let v=0;
  sets.forEach((s,si)=>{for(const [k,o] of s){const [x,y,z]=k.split(',').map(Number);
    for(const [n,cs] of F){if(has((x+n[0])+','+(y+n[1])+','+(z+n[2])))continue;
      for(const q of cs){const t=[0,1,2].filter(i=>!n[i]),s1=[0,0,0],s2=[0,0,0];s1[t[0]]=q[t[0]]?1:-1;s2[t[1]]=q[t[1]]?1:-1;const bx=x+n[0],by=y+n[1],bz=z+n[2];
        const a1=has((bx+s1[0])+','+(by+s1[1])+','+(bz+s1[2])),a2=has((bx+s2[0])+','+(by+s2[1])+','+(bz+s2[2])),a3=has((bx+s1[0]+s2[0])+','+(by+s1[1]+s2[1])+','+(bz+s1[2]+s2[2]));
        P.push(x+q[0],y+q[1],z+q[2]);N.push(n[0],n[1],n[2]);const cc=o.f&&n[2]?o.f:o.c;C.push(cc[0],cc[1],cc[2]);A.push(((a1&&a2)?0:3-(a1+a2+a3))/3);E.push(o.e);H.push(si===fig?o.h:-2);}
      I.push(v,v+1,v+2,v,v+2,v+3);v+=4;}}});
  return {P:new Float32Array(P),N:new Float32Array(N),C:new Float32Array(C),A:new Float32Array(A),E:new Float32Array(E),H:new Float32Array(H),I:v>65535?new Uint32Array(I):new Uint16Array(I),count:I.length,big:v>65535};
}
function statueView(cv,c,o){
  o=o||{};const gl=cv.getContext('webgl',{antialias:true,alpha:true,preserveDrawingBuffer:true});if(!gl)return null;
  const u32=gl.getExtension('OES_element_index_uint'),st=statueStand(c.theme,c.dark),fig=statueFigure(c);
  let fh=0;for(const k of fig.keys()){const y=+k.split(',')[1];if(y+1>fh)fh=y+1;}
  const mFig=stvMesh([fig],0),mAll=stvMesh([fig,st.S],0);
  if((mFig.big||mAll.big)&&!u32)return null;
  const sh=(t,s)=>{const x=gl.createShader(t);gl.shaderSource(x,s);gl.compileShader(x);return x;},prog=(a,b)=>{const p=gl.createProgram();gl.attachShader(p,sh(gl.VERTEX_SHADER,a));gl.attachShader(p,sh(gl.FRAGMENT_SHADER,b));gl.linkProgram(p);return gl.getProgramParameter(p,gl.LINK_STATUS)?p:null;};
  const pr=prog(STV_VS,STV_FS),pp=prog(STV_PV,STV_PF);if(!pr||!pp)return null;
  const up=m=>{const r={count:m.count,big:m.big,b:{}};for(const [k,arr,sz] of [['p',m.P,3],['n',m.N,3],['c',m.C,3],['a',m.A,1],['e',m.E,1],['h',m.H,1]]){const b=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,b);gl.bufferData(gl.ARRAY_BUFFER,arr,gl.STATIC_DRAW);r.b[k]=[b,sz,gl.getAttribLocation(pr,k)];}r.ib=gl.createBuffer();gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,r.ib);gl.bufferData(gl.ELEMENT_ARRAY_BUFFER,m.I,gl.STATIC_DRAW);return r;};
  const gFig=up(mFig),gAll=up(mAll),pBuf=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,pBuf);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(st.pts),gl.STATIC_DRAW);const pN=st.pts.length/5;
  const U=n=>gl.getUniformLocation(pr,n),UP=n=>gl.getUniformLocation(pp,n),holo=c.rarity===3?1:c.rarity===4?2:0;
  const v={yaw:-.35,pitch:.28,zoom:1,turn:!REDUCE,base:true,idle:o.rise?-2.2:-1.5,rise:o.rise&&!REDUCE?0:1,raf:0,last:performance.now(),dead:false};
  const mul=(a,b)=>{const r=new Float32Array(16);for(let i=0;i<4;i++)for(let j=0;j<4;j++){let s=0;for(let k=0;k<4;k++)s+=a[k*4+j]*b[i*4+k];r[i*4+j]=s;}return r;};
  const persp=(f,as,n,fa)=>{const t=1/Math.tan(f/2);return new Float32Array([t/as,0,0,0,0,t,0,0,0,0,(fa+n)/(n-fa),-1,0,0,2*fa*n/(n-fa),0]);};
  const look=(e,ct)=>{const z=[e[0]-ct[0],e[1]-ct[1],e[2]-ct[2]],zl=Math.hypot(...z);for(let i=0;i<3;i++)z[i]/=zl;const x=[z[2],0,-z[0]],xl=Math.hypot(...x)||1;for(let i=0;i<3;i++)x[i]/=xl;const y=[z[1]*x[2]-z[2]*x[1],z[2]*x[0]-z[0]*x[2],z[0]*x[1]-z[1]*x[0]];
    return new Float32Array([x[0],y[0],z[0],0,x[1],y[1],z[1],0,x[2],y[2],z[2],0,-(x[0]*e[0]+x[1]*e[1]+x[2]*e[2]),-(y[0]*e[0]+y[1]*e[1]+y[2]*e[2]),-(z[0]*e[0]+z[1]*e[1]+z[2]*e[2]),1]);};
  const fit=()=>{const r=cv.getBoundingClientRect(),d=Math.min(devicePixelRatio||1,2),w=Math.max(1,r.width*d|0),h=Math.max(1,r.height*d|0);if(cv.width!==w||cv.height!==h){cv.width=w;cv.height=h;}};
  function draw(t){
    if(v.dead)return;fit();const dt=Math.min(.05,(t-v.last)/1000);v.last=t;v.idle+=dt;if(v.turn&&v.idle>1.2)v.yaw-=dt*.35;
    if(v.rise<1)v.rise=Math.min(1,v.rise+dt/2.2);const T=REDUCE?0:t/1000;
    gl.viewport(0,0,cv.width,cv.height);gl.clearColor(0,0,0,0);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);gl.enable(gl.DEPTH_TEST);gl.enable(gl.CULL_FACE);
    const as=cv.width/cv.height,dist=(as<.8?96:76)/v.zoom,ct=[0,v.base?12:fh/2,0],eye=[ct[0]+Math.sin(v.yaw)*Math.cos(v.pitch)*dist,ct[1]+Math.sin(v.pitch)*dist,ct[2]+Math.cos(v.yaw)*Math.cos(v.pitch)*dist];
    const M=mul(persp(.62,as,1,600),look(eye,ct)),m=v.base?gAll:gFig;
    gl.useProgram(pr);gl.uniformMatrix4fv(U('M'),false,M);gl.uniform1f(U('T'),T);gl.uniform1f(U('holo'),holo);gl.uniform1f(U('rise'),v.rise>=1?999:v.rise*(fh+1)-.5);gl.uniform3fv(U('eye'),eye);gl.uniform3fv(U('gc'),st.gc);
    for(const k in m.b){const [b,sz,l]=m.b[k];gl.bindBuffer(gl.ARRAY_BUFFER,b);gl.enableVertexAttribArray(l);gl.vertexAttribPointer(l,sz,gl.FLOAT,false,0,0);}
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,m.ib);gl.drawElements(gl.TRIANGLES,m.count,m.big?gl.UNSIGNED_INT:gl.UNSIGNED_SHORT,0);for(const k in m.b)gl.disableVertexAttribArray(m.b[k][2]);
    if(v.base){gl.useProgram(pp);gl.uniformMatrix4fv(UP('M'),false,M);gl.uniform1f(UP('T'),REDUCE?3:t/1000);gl.uniform1f(UP('px'),cv.height*.9);gl.uniform1f(UP('fall'),st.fall);gl.uniform3fv(UP('pc'),st.pc);gl.uniform3fv(UP('gc'),st.gc);
      gl.enable(gl.BLEND);gl.blendFunc(gl.SRC_ALPHA,gl.ONE);gl.depthMask(false);gl.bindBuffer(gl.ARRAY_BUFFER,pBuf);const la=gl.getAttribLocation(pp,'p'),ls=gl.getAttribLocation(pp,'s'),lk=gl.getAttribLocation(pp,'k');
      gl.enableVertexAttribArray(la);gl.vertexAttribPointer(la,3,gl.FLOAT,false,20,0);gl.enableVertexAttribArray(ls);gl.vertexAttribPointer(ls,1,gl.FLOAT,false,20,12);gl.enableVertexAttribArray(lk);gl.vertexAttribPointer(lk,1,gl.FLOAT,false,20,16);
      gl.drawArrays(gl.POINTS,0,pN);gl.disableVertexAttribArray(la);gl.disableVertexAttribArray(ls);gl.disableVertexAttribArray(lk);gl.depthMask(true);gl.disable(gl.BLEND);}
    v.raf=requestAnimationFrame(draw);}
  const ptr=new Map();let p0=0,z0=1;
  cv.addEventListener('pointerdown',e=>{try{cv.setPointerCapture(e.pointerId);}catch(x){}ptr.set(e.pointerId,[e.clientX,e.clientY]);v.idle=0;if(ptr.size===2){const [a,b]=[...ptr.values()];p0=Math.hypot(a[0]-b[0],a[1]-b[1]);z0=v.zoom;}});
  cv.addEventListener('pointermove',e=>{if(!ptr.has(e.pointerId))return;const q=ptr.get(e.pointerId);if(ptr.size===1){v.yaw-=(e.clientX-q[0])*.009;v.pitch=Math.max(-.15,Math.min(1.2,v.pitch+(e.clientY-q[1])*.006));}
    ptr.set(e.pointerId,[e.clientX,e.clientY]);if(ptr.size===2&&p0){const [a,b]=[...ptr.values()];v.zoom=Math.max(.55,Math.min(2.2,z0*Math.hypot(a[0]-b[0],a[1]-b[1])/p0));}v.idle=0;});
  const off=e=>{ptr.delete(e.pointerId);p0=0;};cv.addEventListener('pointerup',off);cv.addEventListener('pointercancel',off);
  cv.addEventListener('wheel',e=>{e.preventDefault();v.zoom=Math.max(.55,Math.min(2.2,v.zoom*Math.exp(-e.deltaY*.0012)));},{passive:false});
  cv.addEventListener('keydown',e=>{const k=e.key;if(k==='ArrowLeft')v.yaw+=.15;else if(k==='ArrowRight')v.yaw-=.15;else if(k==='ArrowUp')v.pitch=Math.min(1.2,v.pitch+.08);else if(k==='ArrowDown')v.pitch=Math.max(-.15,v.pitch-.08);else if(k==='+'||k==='=')v.zoom=Math.min(2.2,v.zoom*1.1);else if(k==='-')v.zoom=Math.max(.55,v.zoom/1.1);else return;e.preventDefault();v.idle=0;});
  v.raf=requestAnimationFrame(draw);
  return {v,stop(){v.dead=true;cancelAnimationFrame(v.raf);},frame(){draw(performance.now());cancelAnimationFrame(v.raf);v.raf=requestAnimationFrame(draw);}};
}
function openStatue(id,o){
  o=o||{};const c=cardById(id);if(!c||!c.statue)return;if(stv){stv.stop();stv=null;}
  const n=c.nick||c.name,R=RAR[c.rarity],gc=c.dark?THEMES[c.theme].dark.glow:THEMES[c.theme].cute.accent;
  ovMode='statue';
  openOverlay(`<div class="stview" style="--sg:${gc}"><p class="rv-title">${esc(n)}</p><p class="stsub">Statue · ${R.name} · ${esc(realmName(c))}</p>
    <div class="stcan"><canvas id="stCv" tabindex="0" role="img" aria-label="${esc(n)} as a 3D statue on a ${esc(realmName(c))} stand. Drag to turn it, pinch or scroll to zoom, arrow keys to turn."></canvas><p class="stno" id="stNo" hidden>This phone could not start 3D drawing, so here is ${esc(n)} as on the card.<img src="${spriteURL(c)}" alt="${esc(n)}"></p></div>
    <p class="rv-hint">${o.fresh?`Cast with ${esc(n)} today. It keeps the ${c.statue.keep?esc(keepName(c.statue.keep)).toLowerCase():'look'} it wore.`:`Cast ${esc(dateLabel(c.statue.at))}.`} Drag to turn, pinch to zoom.</p>
    <div class="row stbtns"><button class="chip" id="stTurn" aria-pressed="${!REDUCE}">Turntable</button><button class="chip" id="stBase" aria-pressed="true">Stand</button><button class="chip" id="stPic">Save picture</button></div>
    <button class="ghost" id="ovClose">Close</button></div>`,true);
  ovMode='statue';
  const cv=$('#stCv');stv=statueView(cv,c,{rise:o.fresh});
  if(!stv){cv.hidden=true;$('#stNo').hidden=false;['stTurn','stBase','stPic'].forEach(i=>{const b=$('#'+i);if(b)b.hidden=true;});}
  if(o.fresh)chime(3);const f=$('#ovClose');if(f)f.focus({preventScroll:true});
}
function keepName(k){const all=KEEPS.concat(KEEPR,FORGE_R.filter(r=>r.ti!==undefined).map(r=>({id:r.id,name:r.name})));const x=all.find(q=>q.id===k);return x?x.name:k;}
function statueCast(id){
  const c=cardById(id);if(!statueReady(c)||embers()<STATUE_EMB)return;
  const f=fgState();f.spent=(f.spent||0)+STATUE_EMB;c.statue={at:todayKey(),keep:c.keep||''};save();sfx('save');
  hf.msg=`The Forge cast ${c.nick||c.name} in stone.`;renderHearth();renderToday();renderBinder();openStatue(id,{fresh:true});
}
async function statuePicture(c){
  if(!stv)return;await shareFonts();stv.frame();const src=$('#stCv'),W=1080,H=1080,cv=document.createElement('canvas');cv.width=W;cv.height=H;const x=cv.getContext('2d');
  const gc=c.dark?THEMES[c.theme].dark.glow:THEMES[c.theme].cute.accent,g=x.createRadialGradient(W/2,H*.4,40,W/2,H*.42,W*.7);g.addColorStop(0,'#3A1E5C');g.addColorStop(.55,'#22143F');g.addColorStop(1,'#140F2E');x.fillStyle=g;x.fillRect(0,0,W,H);
  const s=Math.min(940/src.width,760/src.height);x.drawImage(src,(W-src.width*s)/2,40,src.width*s,src.height*s);
  const n=c.nick||c.name;x.textAlign='center';x.fillStyle='#FFF7EC';x.font='600 76px Fredoka, sans-serif';x.fillText(n,W/2,H-190);
  x.fillStyle=gc;x.font='700 32px "Nunito Sans", sans-serif';x.fillText(`Statue · ${RAR[c.rarity].name} · ${realmName(c)}`,W/2,H-138);
  x.fillStyle='#B9A9C9';x.font='400 26px "Nunito Sans", sans-serif';x.fillText(`Forgebound · cast ${dateLabel(c.statue.at)}`,W/2,H-96);
  x.fillStyle='#FFD36B';x.font='18px "Press Start 2P", monospace';x.fillText('FORGELINGS',W/2,H-44);
  const blob=await new Promise(r=>{try{cv.toBlob(r,'image/png');}catch(e){r(null);}});
  shareCv={c,cv,blob};const can=canShareFiles(),url=cv.toDataURL('image/png');if(stv){stv.stop();stv=null;}
  openOverlay(`<p class="rv-title">${esc(n)}'s statue</p><img class="shareimg" src="${url}" alt="A picture of ${esc(n)}'s statue on its ${esc(realmName(c))} stand">
    <p class="rv-hint">${can?'Send it to a friend, or save it to your photos.':'Save the picture, then send it however you like.'} It's made on this phone, and nothing is uploaded.</p>
    <div class="btnrow"><button class="primary" id="shDo">${can?'Share':'Save picture'}</button><button class="ghost" id="stBack" data-cid="${c.id}">Back</button></div>`,true);
  ovMode='share';const d=$('#shDo');if(d)d.focus({preventScroll:true});
}
function statueForgeHTML(){
  const fb=state.cards.filter(c=>bondLevel(c)>=5),e=embers();
  if(!fb.length)return `<h3 class="fgh">Statues</h3><p class="muted small">When a Forgeling becomes Forgebound (bond 5), the Forge can cast it as a 3D statue for ${STATUE_EMB} embers.</p>`;
  return `<h3 class="fgh">Statues</h3><ul class="furn forgel">${fb.map(c=>{const n=c.nick||c.name,ok=!!c.statue,can=!ok&&e>=STATUE_EMB;
    return `<li class="${ok?'on':can?'can':''}"><span class="fi" aria-hidden="true"><img class="cimg" src="${spriteURL(c)}" width="30" height="30" alt=""></span><span><b>${esc(n)}’s statue</b><small>Statue. ${esc(n)} in 3D on a ${esc(realmName(c))} stand.</small><small>${ok?`Cast ${esc(dateLabel(c.statue.at))}.`:`Needs ${STATUE_EMB} embers (you have ${e}).`}</small></span>${ok?`<button class="chip" data-statue="${c.id}">See it</button>`:can?`<button class="chip" data-scast="${c.id}">Cast it</button>`:''}</li>`;}).join('')}</ul>`;
}
function statueShelfHTML(){
  const s=statues();if(!s.length)return '';
  return `<div class="lbl2">Statues</div><div class="stshelf">${s.map(c=>`<button data-statue="${c.id}" aria-label="See ${esc(c.nick||c.name)}'s statue"><img src="${spriteURL(c)}" alt=""><span>${esc(c.nick||c.name)}</span></button>`).join('')}</div>`;
}

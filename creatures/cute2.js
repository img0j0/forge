/* 0.54: the second generation of bright Forgelings. New bodies (pear, drop, loaf, blob, noodle, mushroom), poses
   (arms up, waving, hugging, tucked away), faces (happy, sparkle, bean, wink, line; fang, o, wavy, flat, tongue)
   and small touches (two-tone ears and tail, a nose, a mask, cheek fluff, socks, a patch). Same 32x32 grid and
   palette slots as the first generation, so cards, the Hearth, statues and share pictures need nothing new. */
const CSH2={round:{cy:18,rx:10,ry:9},tall:{cy:16,rx:8,ry:11},wide:{cy:20,rx:12,ry:7},chonk:{cy:17,rx:11,ry:10},
  pear:{cy:18,rx:8,ry:8},drop:{cy:19,rx:9.5,ry:8},loaf:{cy:21,rx:12,ry:6.5},blob:{cy:17,rx:10,ry:9},noodle:{cy:16,rx:6.5,ry:11.5},mush:{cy:21,rx:9,ry:7}};
function cute2(g,S,oy,blink,FOOT,M,rm,FX){
  const sh=CSH2[S.shape],fl=S.flip,cy=sh.cy+oy,rx=sh.rx,ry=sh.ry;let top=cy-ry;
  const duo=S.duo?{b:6,s:13,h:7}:{};
  /* tail */
  const tailX=Math.min(16+rx-2,25),m=mask();
  if(S.tail==='curl')curve(m,[[tailX,cy+3],[tailX+7,cy+4],[tailX+6,cy-5]],3.4,2.2,fl);
  else if(S.tail==='fluffy')fillEll(m,Math.min(tailX+3,28),cy+2,3.6,3.6,fl);
  else if(S.tail==='leaf')fillPoly(m,[[tailX,cy+4],[Math.min(tailX+7,30),cy-1],[Math.min(tailX+5,29),cy+6]],fl);
  else if(S.tail==='stub')fillEll(m,Math.min(tailX+1,29),cy+4,2.4,2.4,fl);
  if(S.tail!=='none')commit(g,m,S.tail==='fluffy'||S.tail==='leaf'?(S.tail==='leaf'?{b:6,s:13,h:7}:{b:5,s:12,h:7}):duo);
  /* wings */
  if(S.wings){const w=mask();both(f=>fillEll(w,16-rx-2.5,cy-3,5,3.6,f));commit(g,w,{b:5,s:12,h:7});}
  /* ears (the mushroom wears its cap instead; the drop has a point) */
  if(S.shape==='drop'){const d=mask();fillPoly(d,[[16-rx*.62,cy-ry*.55],[16,top-5],[16+rx*.62,cy-ry*.55]]);fillEll(M,16,cy,rx,ry);commit(g,d,{});top-=4;}
  /* 0.56: tall ears and antennae sit lower on tall bodies, just enough that they fit the 40x40 frame with their
     outline (nothing cut) */
  const ears=(e,t)=>{let o=duo;
    if(S.ears==='pointy')both(f=>fillPoly(e,[[16-rx*.85,t+4],[16-rx*.7,t-6],[16-rx*.2,t+1]],f));
    else if(S.ears==='round')both(f=>fillEll(e,16-rx*.62,t+1.5,3.4,3.4,f));
    else if(S.ears==='bunny')both(f=>fillEll(e,16-rx*.38,t-3,2.6,6.5,f));
    else if(S.ears==='floppy')both(f=>fillEll(e,16-rx-.5,cy-ry*.25,2.6,5,f));
    else if(S.ears==='nubs'){both(f=>fillPoly(e,[[16-rx*.55,t+2],[16-rx*.45,t-3],[16-rx*.2,t+1]],f));o={b:6,s:13,h:null};}
    else if(S.ears==='antenna'){both(f=>curve(e,[[13,t+2],[11,t-4],[9,t-8]],2,2,f));both(f=>fillEll(e,9,t-9,2.1,2.1,f));}
    else if(S.ears==='tuft'){fillEll(e,16,t-2.5,1.8,4);both(f=>fillEll(e,12.5,t-1.5,1.6,3.2,f));o={b:6,s:13,h:null};}
    return o;};
  /* fitted once on the resting pose (bob 0), then moved with the body, so ears never stretch as it bobs; one free row under the frame's top */
    let et=top-oy;for(let k=0;k<9;k++){const t=mask();ears(t,et);let hi=N;for(let q=0;q<N*N;q++)if(t[q]){hi=Math.floor(q/N);break;}if(hi>=2)break;et+=1;}et+=oy;
  if(S.ears==='antenna'){const st=mask();both(f=>curve(st,[[13,et+2],[11,et-4],[9,et-8]],2,2,f));commit(g,st,duo);const bl=mask();both(f=>fillEll(bl,9,et-9,2.1,2.1,f));commit(g,bl,{b:6,s:13,h:null});}
  else{const e=mask(),eo=ears(e,et);if(S.ears!=='none')commit(g,e,eo);}
  /* feet (not bobbing); blobs and loaves sit on the ground */
  if(S.shape!=='blob'&&S.shape!=='loaf'){both(f=>fillEll(FOOT,16-Math.round(Math.max(rx,7)*.45),27.5,3.2,2.2,f));commit(g,FOOT,S.mark==='socks'?{b:7,s:15,h:null}:{});}
  /* body */
  fillEll(M,16,cy,rx,ry);
  if(S.shape==='pear')fillEll(M,16,cy+4,rx+2.6,ry-2.5);
  else if(S.shape==='loaf'){for(let y=Math.round(cy);y<=26;y++)for(let x=Math.ceil(16-rx);x<Math.floor(16+rx);x++)setp(M,x,y,false);}
  else if(S.shape==='blob'){for(let y=Math.round(cy);y<=25;y++)for(let x=Math.ceil(16-rx);x<Math.floor(16+rx);x++)setp(M,x,y,false);
    for(let x=Math.ceil(16-rx);x<Math.floor(16+rx);x++)if((x+Math.round(rm()*2))%4<2)setp(M,x,26,false);}
  commit(g,M,{});
  /* belly */
  if(S.mark!=='belly0'){const bx=16,by=cy+ry*.35+(S.shape==='pear'?2:0),brx=rx*.58,bry=ry*.52;
    const inB=(x,y)=>{const dx=(x+.5-bx)/brx,dy=(y+.5-by)/bry;return dx*dx+dy*dy<=1;};
    for(let y=-SPP;y<SPC+SPP;y++)for(let x=-SPP;x<SPC+SPP;x++){if(M[SPI(x,y)]&&inB(x,y)&&g[SPI(x,y)]!==1)g[SPI(x,y)]=(!inB(x+1,y)||!inB(x,y+1))?12:5;}}
  /* mushroom cap */
  if(S.shape==='mush'){const cm=mask(),cty=cy-ry+1;fillEll(cm,16,cty,12.5,7.5);for(let y=Math.ceil(cty+2);y<SPC+SPP;y++)for(let x=-SPP;x<SPC+SPP;x++)cm[SPI(x,y)]=0;commit(g,cm,{b:6,s:13,h:7});
    [[11,cty-3],[19,cty-4],[15,cty-1],[22,cty]].forEach(p=>{const X=Math.round(p[0]),Y=Math.round(p[1]);[[0,0],[1,0],[0,1],[1,1]].forEach(d=>{const i=SPI(X+d[0],Y+d[1]);if(g[i]===6||g[i]===13)g[i]=7;});});
    top=cty-7;}
  /* markings */
  if(S.mark==='spots'){for(let i=0;i<3;i++){const sx=16+Math.round((rm()-.5)*rx*1.3),sy=Math.floor(cy-ry+3+rm()*ry*.45);for(let a=0;a<2;a++)for(let b=0;b<2;b++){const X=sx+a,Y=sy+b;if(M[SPI(X,Y)]&&g[SPI(X,Y)]!==1&&g[SPI(X,Y)]!==5)g[SPI(X,Y)]=3;}}}
  else if(S.mark==='stripes'){[12,15,16,19].forEach(X=>{for(let Y=cy-ry+1;Y<=cy-ry+3;Y++){if(M[SPI(X,Y)]&&g[SPI(X,Y)]!==1)g[SPI(X,Y)]=3;}});}
  else if(S.mark==='patch'){const px=fl?19:11,py=Math.round(cy-ry*.35);for(let y=py-2;y<=py+2;y++)for(let x=px-2;x<=px+2;x++){const d=(x-px)*(x-px)+(y-py)*(y-py);const i=SPI(x,y);if(d<=5&&M[i]&&g[i]!==1&&g[i]!==5&&g[i]!==12)g[i]=6;}}
  /* cheek fluff */
  if(S.fluff){const fm=mask();both(f=>fillPoly(fm,[[16-rx+1,cy-1],[16-rx-3,cy+1],[16-rx+1,cy+3]],f));for(let i=0;i<N*N;i++)if(fm[i]&&!M[i]&&g[i]!==1)g[i]=0;commit(g,fm,{});}
  /* face: laid out first, fitted to this body (every face pixel has body on all four sides), so the arms can be
     placed clear of it; drawn last, so nothing covers it */
  const EYES={big:['ppp','wpp','ppp','ppw'],round:['wp','pp','pp'],dot:['wp','pp'],sleepy:['ppp'],
    happy:['.p.','p.p'],sparkle:['wpp.','pppp','pppw','.pp.'],bean:['p','p','p'],line:['pp.','..p'],wink:['wp','pp','pp']};
  const MO={smile:['p..p','.pp.'],cat:['p.pp.p','.pppp.'],open:['pppp','.cc.'],tiny:['pp'],
    fang:['p...p','.ppp.','.w...'],o:['.p.','p.p','.p.'],wavy:['p.p.p','.p.p.'],flat:['ppp'],tongue:['pppp','.pc.','..c.']}[S.mouth];
  const lay=(gp,eyes,eyeY,blush)=>{const EY=EYES[eyes],ew=EY[0].length,eh=EY.length,closed=blink&&!['sleepy','happy','line'].includes(eyes);
    const pat=closed?['p'.repeat(ew)]:EY,ey=closed?eyeY+eh-1:eyeY+(eyes==='sleepy'?1:0),moY=eyeY+eh+1+(S.nose?1:0);
    const draw=G=>{stamp(G,16-gp-ew,ey,pat,false);
      if(eyes==='wink')stamp(G,16+gp,eyeY+eh-1,['p'.repeat(ew)],false);else stamp(G,16+gp,ey,eyes==='line'?['.pp','p..']:pat,false);
      if(blush){stamp(G,16-gp-ew-1,eyeY+eh,['cc'],false);stamp(G,16+gp+ew-1,eyeY+eh,['cc'],false);}
      if(S.nose)stamp(G,15,eyeY+eh-1,['pp'],false);
      stamp(G,16-Math.floor(MO[0].length/2),moY,MO,false);};
    const FG=new Uint8Array(N*N);draw(FG);const FI=[];for(let i=0;i<N*N;i++)if(FG[i])FI.push(i);
    const B=p=>M[p]&&g[p]!==1,ok=FI.every(p=>B(p)&&B(p-1)&&B(p+1)&&B(p-N)&&B(p+N));
    return {ok,FG,FI,draw,eyeY,eh,moY};};
  let eY0=Math.round(cy-ry*.22)+(S.ey||0);
  if(S.shape==='mush')eY0=Math.max(eY0,Math.round(cy-ry+1)+4);
  let hw=0;while(hw<15&&M[SPI(16-hw-1,eY0)])hw++;
  const gp0=Math.max(2,Math.min(5,Math.round(rx*.3)+1+(S.ex||0),Math.floor(hw*.42)));
  let F=null;
  search:for(const eyes of [S.eyes,'round','dot'])for(const blush of S.blush?[true,false]:[false])for(let gp=gp0;gp>=1;gp--)for(const d of [0,1,-1,2,-2,3,4]){
    const t=lay(gp,eyes,eY0+d,blush);if(t.ok){F=t;break search;}}
  if(!F)F=lay(1,'dot',eY0,false);
  const {FG,FI,eyeY,moY}=F,face=F.draw,gp=Math.max(1,gp0);
  if(S.mask){for(let y=eyeY-1;y<=eyeY+2;y++)for(let x=-SPP;x<SPC+SPP;x++){const i=SPI(x,y);if(M[i]&&M[i-1]&&M[i+1]&&g[i]!==1&&g[i]!==6&&g[i]!==13)g[i]=3;}}
  /* arms: the chosen pose if it stays clear of the face (a pixel of body between), else a calmer one */
  /* each pose has a few placements (lower, further out); the first that keeps a pixel of body between the arm's
     outline and the face wins, else a calmer pose, else the arms stay tucked away */
  const hugY=Math.min(Math.max(cy+ry*.66,moY+3.5),25.5+oy);
  const OUT=[[-.5,2],[-1.5,3],[-.5,4.5],[-1.5,5.5]],UP=[[1.5,1,0],[1.5,3,-1],[.5,4,-1.5]];
  const out=(a,f,k)=>fillEll(a,16-rx+OUT[k][0],cy+OUT[k][1],2.1,3,f),
    up=(a,f,k)=>{const[x0,y0,dx]=UP[k];curve(a,[[16-rx+x0,cy+y0],[16-rx-2.5+dx,cy+y0-3],[16-rx-2+dx,cy+y0-8]],3.6,2.8,f);};
  const clear=a=>FI.every(i=>{const x=i%N,y=(i-x)/N;for(let dy=-2;dy<=2;dy++)for(let dx=-2;dx<=2;dx++){const X=x+dx,Y=y+dy;if(X>=0&&Y>=0&&X<N&&Y<N&&a[Y*N+X])return false;}return true;});
  const tries={out:OUT.map((_,k)=>a=>both(f=>out(a,f,k))),up:UP.map((_,k)=>a=>both(f=>up(a,f,k))),
    wave:UP.flatMap((_,k)=>OUT.map((_,j)=>a=>{up(a,fl,k);out(a,!fl,j);})),hug:[a=>both(f=>fillEll(a,16-rx*.34,hugY,2,1.5,f))]};
  const order={out:['out'],up:['up','out'],wave:['wave','up','out'],hug:['hug','out'],tuck:[]}[S.arms];
  let arms='tuck',a=mask();
  pick:for(const k of order)for(const fn of tries[k]){const m=mask();fn(m);if(clear(m)){arms=k;a=m;break pick;}}
  if(arms!=='tuck')commit(g,a,S.mark==='socks'?{b:7,s:15,h:null}:{});
  const PV=FI.map(i=>g[i]);face(g);FX.FI=FI;FX.FV=FI.map(i=>FG[i]);
  if(globalThis.__FDBG)globalThis.__FDBG.push({FI,FV:FI.map(i=>FG[i]),PV,M:Array.from(M),arms,want:S.arms,dark:0});
  /* crown */
  if(S.crown){const cm=mask();fillPoly(cm,[[12,top-1],[12,top-5],[14,top-3],[16,top-6],[18,top-3],[20,top-5],[20,top-1]]);commit(g,cm,{b:17,s:18,h:null});}
  /* the keepsake code places charms and scarves below eyeY+eh+1: report the face's real depth */
  return {top,eyeY,eh:moY+MO.length-eyeY-3,rx};
}
/* 0.54: three more Shade bodies for the second generation */
Object.assign(DSH,{
  imp:{top:8,poly:[[11,8],[21,8],[25,13],[25,21],[21,27],[11,27],[7,21],[7,13]],eyeY:13,gap:2,arm:[6,20],sp:[[8,12],[4,8],[10,10]]},
  slink:{top:11,poly:[[4,15],[11,11],[22,11],[29,16],[26,27],[6,27]],eyeY:16,gap:3,arm:[5,22],sp:[[6,15],[2,11],[9,13]]},
  tower:{top:3,poly:[[12,3],[20,3],[23,10],[22,27],[10,27],[9,10]],eyeY:8,gap:1,arm:[8,18],sp:[[10,9],[6,5],[12,7]]}
});

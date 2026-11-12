/* 0.54: the second generation of bright Forgelings. New bodies (pear, drop, loaf, blob, noodle, mushroom), poses
   (arms up, waving, hugging, tucked away), faces (happy, sparkle, bean, wink, line; fang, o, wavy, flat, tongue)
   and small touches (two-tone ears and tail, a nose, a mask, cheek fluff, socks, a patch). Same 32x32 grid and
   palette slots as the first generation, so cards, the Hearth, statues and share pictures need nothing new. */
const CSH2={round:{cy:18,rx:10,ry:9},tall:{cy:16,rx:8,ry:11},wide:{cy:20,rx:12,ry:7},chonk:{cy:17,rx:11,ry:10},
  pear:{cy:18,rx:8,ry:8},drop:{cy:19,rx:9.5,ry:8},loaf:{cy:21,rx:12,ry:6.5},blob:{cy:17,rx:10,ry:9},noodle:{cy:16,rx:6.5,ry:11.5},mush:{cy:21,rx:8,ry:6.5}};
function cute2(g,S,oy,blink,FOOT,M,rm){
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
  const e=mask();let eo=duo;
  if(S.shape==='drop'){const d=mask();fillPoly(d,[[16-rx*.62,cy-ry*.55],[16,top-5],[16+rx*.62,cy-ry*.55]]);fillEll(M,16,cy,rx,ry);commit(g,d,{});top-=4;}
  if(S.ears==='pointy')both(f=>fillPoly(e,[[16-rx*.85,top+4],[16-rx*.7,top-6],[16-rx*.2,top+1]],f));
  else if(S.ears==='round')both(f=>fillEll(e,16-rx*.62,top+1.5,3.4,3.4,f));
  else if(S.ears==='bunny')both(f=>fillEll(e,16-rx*.38,top-3,2.6,6.5,f));
  else if(S.ears==='floppy')both(f=>fillEll(e,16-rx-.5,cy-ry*.25,2.6,5,f));
  else if(S.ears==='nubs'){both(f=>fillPoly(e,[[16-rx*.55,top+2],[16-rx*.45,top-3],[16-rx*.2,top+1]],f));eo={b:6,s:13,h:null};}
  else if(S.ears==='antenna'){both(f=>curve(e,[[13,top+2],[11,top-4],[9,top-8]],2,2,f));}
  else if(S.ears==='tuft'){fillEll(e,16,top-2.5,1.8,4);both(f=>fillEll(e,12.5,top-1.5,1.6,3.2,f));eo={b:6,s:13,h:null};}
  if(S.ears!=='none')commit(g,e,eo);
  if(S.ears==='antenna'){const bl=mask();both(f=>fillEll(bl,9,top-9,2.1,2.1,f));commit(g,bl,{b:6,s:13,h:null});}
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
    for(let y=0;y<N;y++)for(let x=0;x<N;x++){if(M[y*N+x]&&inB(x,y)&&g[y*N+x]!==1)g[y*N+x]=(!inB(x+1,y)||!inB(x,y+1))?12:5;}}
  /* mushroom cap */
  if(S.shape==='mush'){const cm=mask(),cty=cy-ry+1;fillEll(cm,16,cty,12.5,7.5);for(let y=Math.ceil(cty+2);y<N;y++)for(let x=0;x<N;x++)cm[y*N+x]=0;commit(g,cm,{b:6,s:13,h:7});
    [[11,cty-3],[19,cty-4],[15,cty-1],[22,cty]].forEach(p=>{const X=Math.round(p[0]),Y=Math.round(p[1]);[[0,0],[1,0],[0,1],[1,1]].forEach(d=>{const i=(Y+d[1])*N+X+d[0];if(g[i]===6||g[i]===13)g[i]=7;});});
    top=cty-7;}
  /* markings */
  if(S.mark==='spots'){for(let i=0;i<3;i++){const sx=16+Math.round((rm()-.5)*rx*1.3),sy=Math.floor(cy-ry+3+rm()*ry*.45);for(let a=0;a<2;a++)for(let b=0;b<2;b++){const X=sx+a,Y=sy+b;if(M[Y*N+X]&&g[Y*N+X]!==1&&g[Y*N+X]!==5)g[Y*N+X]=3;}}}
  else if(S.mark==='stripes'){[12,15,16,19].forEach(X=>{for(let Y=cy-ry+1;Y<=cy-ry+3;Y++){if(M[Y*N+X]&&g[Y*N+X]!==1)g[Y*N+X]=3;}});}
  else if(S.mark==='patch'){const px=fl?19:11,py=Math.round(cy-ry*.35);for(let y=py-2;y<=py+2;y++)for(let x=px-2;x<=px+2;x++){const d=(x-px)*(x-px)+(y-py)*(y-py);const i=y*N+x;if(d<=5&&M[i]&&g[i]!==1&&g[i]!==5&&g[i]!==12)g[i]=6;}}
  /* cheek fluff */
  if(S.fluff){const fm=mask();both(f=>fillPoly(fm,[[16-rx+1,cy-1],[16-rx-3,cy+1],[16-rx+1,cy+3]],f));for(let i=0;i<N*N;i++)if(fm[i]&&!M[i]&&g[i]!==1)g[i]=0;commit(g,fm,{});}
  /* face */
  const gp=Math.max(2,Math.min(5,Math.round(rx*.3)+1+(S.ex||0)));const eyeY=Math.round(cy-ry*.22)+(S.shape==='mush'?2:0)+(S.ey||0);
  if(S.mask){for(let y=eyeY-1;y<=eyeY+2;y++)for(let x=16-gp-4;x<=16+gp+3;x++){const i=y*N+x;if(M[i]&&g[i]!==1&&g[i]!==6&&g[i]!==13)g[i]=3;}}
  const EYES={big:['ppp','wpp','ppp','ppw'],round:['wp','pp','pp'],dot:['wp','pp'],sleepy:['ppp'],
    happy:['.p.','p.p'],sparkle:['wpp.','pppp','pppw','.pp.'],bean:['p','p','p'],line:['pp.','..p'],wink:['wp','pp','pp']};
  const EY=EYES[S.eyes],ew=EY[0].length,eh=EY.length,closed=blink&&!['sleepy','happy','line'].includes(S.eyes);
  const pat=closed?['p'.repeat(ew)]:EY,ey=closed?eyeY+eh-1:eyeY+(S.eyes==='sleepy'?1:0);
  stamp(g,16-gp-ew,ey,pat,false);
  if(S.eyes==='wink')stamp(g,16+gp,eyeY+eh-1,['p'.repeat(ew)],false);else stamp(g,16+gp,ey,S.eyes==='line'?['.pp','p..']:pat,false);
  if(S.blush){stamp(g,16-gp-ew-2,eyeY+eh,['cc'],false);stamp(g,16+gp+ew,eyeY+eh,['cc'],false);}
  if(S.nose)stamp(g,15,eyeY+eh-1,['pp'],false);
  const MO={smile:['p..p','.pp.'],cat:['p.pp.p','.pppp.'],open:['pppp','.cc.'],tiny:['pp'],
    fang:['p...p','.ppp.','.w...'],o:['.p.','p.p','.p.'],wavy:['p.p.p','.p.p.'],flat:['ppp'],tongue:['pppp','.pc.','..c.']}[S.mouth];
  stamp(g,16-Math.floor(MO[0].length/2),eyeY+eh+1+(S.nose?1:0),MO,false);
  /* arms (in front of the body) */
  const a=mask();
  const out=f=>fillEll(a,16-rx-.5,cy+2,2.1,3,f),up=f=>curve(a,[[16-rx+1.5,cy+1],[16-rx-2.5,cy-2],[16-rx-2,cy-7]],3.6,2.8,f);
  if(S.arms==='out')both(out);
  else if(S.arms==='up')both(up);
  else if(S.arms==='wave'){up(fl);out(!fl);}
  else if(S.arms==='hug')both(f=>fillEll(a,16-rx*.34,Math.min(cy+ry*.66,25),2,1.5,f));
  if(S.arms!=='tuck')commit(g,a,S.mark==='socks'?{b:7,s:15,h:null}:{});
  /* crown */
  if(S.crown){const cm=mask();fillPoly(cm,[[12,top-1],[12,top-5],[14,top-3],[16,top-6],[18,top-3],[20,top-5],[20,top-1]]);commit(g,cm,{b:17,s:18,h:null});}
  return {top,eyeY,eh,rx};
}
/* 0.54: three more Shade bodies for the second generation */
Object.assign(DSH,{
  imp:{top:8,poly:[[11,8],[21,8],[25,13],[25,21],[21,27],[11,27],[7,21],[7,13]],eyeY:13,gap:2,arm:[6,20],sp:[[8,12],[4,8],[10,10]]},
  slink:{top:11,poly:[[4,15],[11,11],[22,11],[29,16],[26,27],[6,27]],eyeY:15,gap:3,arm:[5,22],sp:[[6,15],[2,11],[9,13]]},
  tower:{top:3,poly:[[12,3],[20,3],[23,10],[22,27],[10,27],[9,10]],eyeY:8,gap:1,arm:[8,18],sp:[[10,9],[6,5],[12,7]]}
});

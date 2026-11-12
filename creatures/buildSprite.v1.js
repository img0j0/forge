function buildSprite(S,bob,blink){
  const g=new Uint8Array(N*N),oy=bob,fl=S.flip,dk=S.dark;
  const rm=mulberry32(S.seed^0x51ed270b);
  const FOOT=mask(),M=mask();
  let cy,rx,ry,top,eyeY,gap,eh;
  if(!dk){
    const sh=CSH[S.shape];cy=sh.cy+oy;rx=sh.rx;ry=sh.ry;top=cy-ry;
    const tailX=Math.min(16+rx-2,25);
    /* tail */
    const m=mask();
    if(S.tail==='curl')curve(m,[[tailX,cy+3],[tailX+7,cy+4],[tailX+6,cy-5]],3.4,2.2,fl);
    else if(S.tail==='fluffy')fillEll(m,Math.min(tailX+3,28),cy+2,3.6,3.6,fl);
    else fillEll(m,Math.min(tailX+1,29),cy+4,2.4,2.4,fl);
    commit(g,m,S.tail==='fluffy'?{b:5,s:12,h:7}:{});
    /* wings */
    if(S.wings){const w=mask();both(f=>fillEll(w,16-rx-2.5,cy-3,5,3.6,f));commit(g,w,{b:5,s:12,h:7});}
    /* ears */
    const e=mask();let eo={};
    if(S.ears==='pointy')both(f=>fillPoly(e,[[16-rx*.85,top+4],[16-rx*.7,top-6],[16-rx*.2,top+1]],f));
    else if(S.ears==='round')both(f=>fillEll(e,16-rx*.62,top+1.5,3.4,3.4,f));
    else if(S.ears==='bunny')both(f=>fillEll(e,16-rx*.38,top-3,2.6,6.5,f));
    else if(S.ears==='floppy')both(f=>fillEll(e,16-rx-.5,cy-ry*.25,2.6,5,f));
    else if(S.ears==='nubs'){both(f=>fillPoly(e,[[16-rx*.55,top+2],[16-rx*.45,top-3],[16-rx*.2,top+1]],f));eo={b:6,s:13,h:null};}
    else if(S.ears==='antenna'){both(f=>curve(e,[[13,top+2],[11,top-4],[9,top-8]],2,2,f));}
    else if(S.ears==='tuft'){fillEll(e,16,top-2.5,1.8,4);both(f=>fillEll(e,12.5,top-1.5,1.6,3.2,f));eo={b:6,s:13,h:null};}
    commit(g,e,eo);
    if(S.ears==='antenna'){const bl=mask();both(f=>fillEll(bl,9,top-9,2.1,2.1,f));commit(g,bl,{b:6,s:13,h:null});}
    /* feet (not bobbing) */
    both(f=>fillEll(FOOT,16-Math.round(rx*.45),27.5,3.2,2.2,f));commit(g,FOOT,{});
    /* body */
    fillEll(M,16,cy,rx,ry);commit(g,M,{});
    /* belly */
    const bx=16,by=cy+ry*.35,brx=rx*.58,bry=ry*.52;
    const inB=(x,y)=>{const dx=(x+.5-bx)/brx,dy=(y+.5-by)/bry;return dx*dx+dy*dy<=1;};
    for(let y=0;y<N;y++)for(let x=0;x<N;x++){if(M[y*N+x]&&inB(x,y)&&g[y*N+x]!==1)g[y*N+x]=(!inB(x+1,y)||!inB(x,y+1))?12:5;}
    /* markings */
    if(S.mark==='spots'){for(let i=0;i<3;i++){const sx=16+Math.round((rm()-.5)*rx*1.3),sy=Math.floor(top+3+rm()*ry*.45);for(let a=0;a<2;a++)for(let b=0;b<2;b++){const X=sx+a,Y=sy+b;if(M[Y*N+X]&&g[Y*N+X]!==1&&g[Y*N+X]!==5)g[Y*N+X]=3;}}}
    else if(S.mark==='stripes'){[12,15,16,19].forEach(X=>{for(let Y=top+1;Y<=top+3;Y++){if(M[Y*N+X]&&g[Y*N+X]!==1)g[Y*N+X]=3;}});}
    /* arms */
    const a=mask();both(f=>fillEll(a,16-rx-.5,cy+2,2.1,3,f));commit(g,a,{});
    /* face */
    const gp=Math.max(2,Math.min(5,Math.round(rx*.3)+1));eyeY=Math.round(cy-ry*.22);
    const EY={big:['ppp','wpp','ppp','ppw'],round:['wp','pp','pp'],dot:['wp','pp'],sleepy:['ppp']}[S.eyes];
    const ew=EY[0].length;eh=EY.length;
    const pat=blink&&S.eyes!=='sleepy'?[ 'p'.repeat(ew) ]:EY;
    const ey=blink&&S.eyes!=='sleepy'?eyeY+eh-1:eyeY+(S.eyes==='sleepy'?1:0);
    stamp(g,16-gp-ew,ey,pat,false);stamp(g,16+gp,ey,pat,false);
    stamp(g,16-gp-ew-2,eyeY+eh,['cc'],false);stamp(g,16+gp+ew,eyeY+eh,['cc'],false);
    const MO={smile:['p..p','.pp.'],cat:['p.pp.p','.pppp.'],open:['pppp','.cc.'],tiny:['pp']}[S.mouth];
    stamp(g,16-MO[0].length/2,eyeY+eh+1,MO,false);
    /* crown */
    if(S.crown){const cm=mask();fillPoly(cm,[[12,top-1],[12,top-5],[14,top-3],[16,top-6],[18,top-3],[20,top-5],[20,top-1]]);commit(g,cm,{b:17,s:18,h:null});}
  }else{
    const sh=DSH[S.shape];top=sh.top+oy;eyeY=sh.eyeY+oy;gap=sh.gap;
    /* tail */
    const m=mask();
    if(S.tail==='spade'){curve(m,[[22,25+oy],[29,24+oy],[28,17+oy]],3.2,2,fl);}
    else if(S.tail==='scorpion'){curve(m,[[22,26+oy],[31,22+oy],[29,11+oy],[24,7+oy]],3.4,1.4,fl);}
    else curve(m,[[22,26+oy],[28,29+oy],[30,22+oy],[30,16+oy]],2.4,1.4,fl);
    commit(g,m,{});
    const tipPt=S.tail==='spade'?[28,17+oy]:S.tail==='scorpion'?[24,7+oy]:[30,16+oy];
    const tm=mask();fillEll(tm,tipPt[0],tipPt[1]-.5,S.tail==='spade'?2.8:1.6,S.tail==='spade'?2.8:1.6,fl);commit(g,tm,{b:6,s:13,h:null});
    /* wings */
    if(S.wings){const w=mask(),t=top;both(f=>fillPoly(w,[[12,t+7],[2,t-2],[1,t+6],[4,t+5],[3,t+11],[6,t+9],[6,t+16],[10,t+12],[12,t+14]],f));commit(g,w,{b:11,s:3,h:3});}
    /* horns */
    const hm=mask();
    if(S.horns==='up')both(f=>curve(hm,[[11,top+3],[8,top-2],[9,top-8]],3.4,1.2,f));
    else if(S.horns==='ram')both(f=>curve(hm,[[11,top+4],[4,top],[3,top+7]],3.6,1.4,f));
    else if(S.horns==='crown'){[[11,4],[16,6],[21,4]].forEach(p=>fillPoly(hm,[[p[0]-2.2,top+2],[p[0],top-p[1]+2],[p[0]+2.2,top+2]]));}
    commit(g,hm,{b:14,s:15,h:null});
    /* shoulder spines */
    if(S.spines){const sp=mask();both(f=>fillPoly(sp,sh.sp.map(p=>[p[0],p[1]+oy]),f));commit(g,sp,{b:14,s:15,h:null});}
    /* feet */
    both(f=>fillEll(FOOT,16-6,27.5,3.4,2,f));commit(g,FOOT,{});
    for(const X of [8,10,21,23])g[29*N+X]=14;
    /* body */
    fillPoly(M,sh.poly.map(p=>[p[0],p[1]+oy]));commit(g,M,{});
    /* chest */
    const cb=mask();fillEll(cb,16,top+(27-sh.top)*.62,4.2,5.2);
    for(let y=0;y<N;y++)for(let x=0;x<N;x++)if(cb[y*N+x]&&M[y*N+x]&&g[y*N+x]!==1)g[y*N+x]=5;
    /* markings */
    if(S.mark==='ribs'){for(let k=0;k<3;k++){const Y=Math.floor(top+(27-sh.top)*.5)+k*2;for(let X=14;X<=17;X++)if(M[Y*N+X]&&g[Y*N+X]===5)g[Y*N+X]=11;}}
    else if(S.mark==='cracks'){let X=11,Y=top+2;for(let k=0;k<9;k++){if(M[Y*N+X]&&g[Y*N+X]!==1)g[Y*N+X]=11;Y++;X+=(k%2?1:-1)*(rm()<.5?0:1)+(k%3===0?1:0);}}
    else if(S.mark==='runes'){[[15,top+11],[16,top+11],[15,top+12],[16,top+13],[15,top+14]].forEach(p=>{if(M[p[1]*N+p[0]])g[p[1]*N+p[0]]=6;});}
    /* arms and claws */
    const am=mask();both(f=>fillEll(am,sh.arm[0],sh.arm[1]+oy,2.6,4.8,f));commit(g,am,{});
    for(const sd of [0,1]){const ax=sd?N-1-Math.floor(sh.arm[0]):Math.floor(sh.arm[0]),by=Math.floor(sh.arm[1]+oy+4.8)+1;for(let i=-1;i<=1;i++){const X=ax+i,Y=by;if(X>=0&&X<N&&Y<N)g[Y*N+X]=14;}}
    /* face */
    const gx=gap,ey=eyeY;
    if(S.eyes==='glare'){const L=blink?['gggg']:['gg..','.ggG'],Rr=blink?['gggg']:['..gg','Ggg.'];eh=blink?1:2;stamp(g,16-gx-4,ey+(blink?1:0),L,false);stamp(g,16+gx,ey+(blink?1:0),Rr,false);}
    else if(S.eyes==='slit'){const L=blink?['ggg']:['gpg','gpg','gpg'];eh=blink?1:3;stamp(g,16-gx-3,ey+(blink?1:0),L,false);stamp(g,16+gx,ey+(blink?1:0),L,false);}
    else if(S.eyes==='hollow'){const L=blink?['www']:['www','wpw','www'];eh=blink?1:3;stamp(g,16-gx-3,ey+(blink?1:0),L,false);stamp(g,16+gx,ey+(blink?1:0),L,false);}
    else{const L=blink?['gggggg']:['.gggg.','ggppgg','.gggg.'];eh=blink?1:3;stamp(g,13,ey+(blink?1:0),L,false);}
    if(S.third&&!blink)stamp(g,15,ey-4,['gg','gG'],false);
    const MO={fangs:['pppppp','t.pp.t'],grin:['pppppppp','ptptptpt'],maw:['.pppppp.','pptpptpp','.pppppp.'],snarl:['pppp','tppt']}[S.mouth];
    stamp(g,16-MO[0].length/2,ey+eh+2,MO,false);
    /* halo for legends */
    if(S.crown){const hmk=mask();for(let y=0;y<N;y++)for(let x=0;x<N;x++){const dx=(x+.5-16)/6.5,dy=(y+.5-(top-3))/2;const d=dx*dx+dy*dy;if(d>=.62&&d<=1.1)setp(hmk,x,y,false);}
      for(let y=0;y<N;y++)for(let x=0;x<N;x++)if(hmk[y*N+x])g[y*N+x]=17;}
  }

  if(S.keep){
    const half=dk?7:rx,mouthY=eyeY+eh+(dk?2:1);
    if(S.keep==='hat'){const hm=mask();fillPoly(hm,[[12.5,top+2],[19.5,top+2],[16,top-6]]);commit(g,hm,{b:6,s:13,h:null});
      const pm=mask();fillEll(pm,16,top-6.6,1.7,1.7);commit(g,pm,{b:17,s:18,h:null});
      [[14,top+1],[17,top+1],[15,top-2],[16,top-2]].forEach(p=>{const i=p[1]*N+p[0];if(g[i]===6||g[i]===13)g[i]=7;});}
    else if(S.keep==='scarf'){const sy=mouthY+(dk?4:3);for(let dy=0;dy<2;dy++)for(let x=0;x<N;x++){const i=(sy+dy)*N+x;if(M[i]&&g[i]!==1)g[i]=dy?13:6;}
      const tm=mask();fillPoly(tm,[[17,sy+1],[20,sy+1],[20,sy+6],[17,sy+6]]);commit(g,tm,{b:6,s:13,h:null});}
    else if(S.keep==='flower'){const fx=16+Math.round(half*.62),fy=top+3;stamp(g,fx-1,fy-1,['.c.','cyc','.c.'],false);}
    else if(S.keep==='daisies'){[11,15,19].forEach(x=>stamp(g,x,top,['.c.','cyc','.c.'],false));}
    else if(S.keep==='charm'){const cy=mouthY+(dk?3:2);stamp(g,14,cy,['.o..o.','..oo..','.oyyo.','.oyao.','..oo..'],false);}
    else if(S.keep==='shells'){const sy=mouthY+(dk?4:3);for(let x=0;x<N;x++){const i=sy*N+x;if(M[i]&&g[i]!==1)g[i]=x%2?7:16;}}
    else if(S.keep==='cap'){const cm=mask();fillEll(cm,16,top+1.2,6.4,3.4);for(let y=Math.ceil(top+1.2);y<N;y++)for(let x=0;x<N;x++)cm[y*N+x]=0;commit(g,cm,{b:6,s:13,h:null});const bm=mask();fillEll(bm,16,top-2.6,1.6,1.4);commit(g,bm,{b:7,s:7,h:null});}
    else if(S.keep==='lantern'){const lx=16+half+2,ly=mouthY+1;stamp(g,Math.min(N-3,lx),ly,['.o.','ooo','yyy','yyy','yyy','ooo'],false);}
    else if(/^charm[0-4]$/.test(S.keep)){const L='ABCDE'[+S.keep[5]],cy=mouthY+(dk?2:1);stamp(g,13,cy,['o....o','.o..o.','..oo..','.oXXo.','oXXXXo','oXyXXo','.oXXo.','..oo..'].map(r=>r.replace(/X/g,L)),false);}
    else if(/^ward[0-4]$/.test(S.keep)){const L='FHIJK'[+S.keep[4]],cy=mouthY+(dk?2:1);stamp(g,13,cy,['o....o','.o..o.','..oo..','.oXXo.','oXXXXo','oXyyXo','oXXXXo','.oXXo.','..oo..'].map(r=>r.replace(/X/g,L)),false);}
  }
  return g;
}
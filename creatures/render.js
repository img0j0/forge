/* 0.55: finer rendering for every Forgeling (same shapes, faces and colours).
   commit(): round form shading. Light comes from the upper left; each pixel measures how far the part reaches
   toward the light and away from it, and gets highlight, base, a mid tone or shade by where it sits between the
   two (small parts keep the old rim rule). selout(): outlines take the colour of what they edge (a dark accent
   line round an accent part, gold round gold) and lines inside the silhouette, where parts overlap, soften to
   the part's own deep shade. */
const MIDOF={2:29,6:30,5:31};
function commit(g,m,o){
  const inm=(x,y)=>x>=0&&y>=0&&x<N&&y<N&&m[y*N+x]===1;
  const base=o.b||2,sh=o.s===undefined?3:o.s,hl=o.h===undefined?4:o.h,md=o.m!==undefined?o.m:(MIDOF[base]||0);
  const ray=(x,y,dx,dy)=>{let k=0;while(k<14&&inm(x+dx*(k+1),y+dy*(k+1)))k++;return k;};
  for(let y=0;y<N;y++)for(let x=0;x<N;x++){
    if(!inm(x,y))continue;let s=base;
    const L=(ray(x,y,-1,-1)+ray(x,y,0,-1)+ray(x,y,-1,0)*.5)/2.5,D=(ray(x,y,1,1)+ray(x,y,0,1)+ray(x,y,1,0)*.5)/2.5,T=L+D;
    if(T<3.2){
      if(sh&&(!inm(x+1,y)||!inm(x,y+1)||!inm(x+1,y+1)))s=sh;
      else if(hl&&!inm(x-1,y-1)&&inm(x+1,y)&&inm(x,y+1))s=hl;
    }else{const u=L/T;
      if(sh&&(u>.8||!inm(x+1,y+1)&&(!inm(x+1,y)||!inm(x,y+1))))s=sh;
      else if(md&&u>.52)s=md;
      else if(hl&&(u<.2||!inm(x-1,y-1)&&!inm(x-1,y)&&inm(x+1,y)&&inm(x,y+1)))s=hl;}
    g[y*N+x]=s;
  }
  if(o.out!==false)for(let y=0;y<N;y++)for(let x=0;x<N;x++){
    if(!inm(x,y)&&(inm(x-1,y)||inm(x+1,y)||inm(x,y-1)||inm(x,y+1)))g[y*N+x]=o.o||1;
  }
}
/* every outline slot: the near-black 1 and selout's 32-38. Forgebound gold, legendary foil and statue outlines use it */
const OL=s=>s===1||(s>=32&&s<=38);
const SELFAM=s=>s===6||s===13||s===30?1:s===14||s===15?2:s===17||s===18?3:s===7?4:0;
function selout(g){
  const src=g.slice(),OUTER=[1,32,33,34,1],LIT=[35,36,37,38,37],INNER=[35,36,37,38,37];
  for(let y=0;y<N;y++)for(let x=0;x<N;x++){const i=y*N+x;if(src[i]!==1)continue;
    let outer=false,lit=0;const cnt=[0,0,0,0,0];
    for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++){if(!dx&&!dy)continue;const X=x+dx,Y=y+dy;
      const v=X<0||Y<0||X>=N||Y>=N?0:src[Y*N+X];
      if(!v){if(!dx||!dy)outer=true;continue;}if(v===1)continue;cnt[SELFAM(v)]+=(!dx||!dy)?2:1;if(dx>=0&&dy>=0)lit++;else lit-=2;}
    let f=0;for(let k=1;k<5;k++)if(cnt[k]>cnt[f])f=k;
    if(!cnt[f])continue;
    g[i]=outer?(lit>=2&&y<N-6?LIT[f]:OUTER[f]):INNER[f];}
  return g;
}

function commit(g,m,o){
  const inm=(x,y)=>x>=0&&y>=0&&x<N&&y<N&&m[y*N+x]===1;
  const base=o.b||2,sh=o.s===undefined?3:o.s,hl=o.h===undefined?4:o.h;
  for(let y=0;y<N;y++)for(let x=0;x<N;x++){
    if(!inm(x,y))continue;let s=base;
    if(sh&&(!inm(x+1,y)||!inm(x,y+1)||!inm(x+1,y+1)))s=sh;
    else if(hl&&!inm(x-1,y-1)&&inm(x+1,y)&&inm(x,y+1))s=hl;
    g[y*N+x]=s;
  }
  if(o.out!==false)for(let y=0;y<N;y++)for(let x=0;x<N;x++){
    if(!inm(x,y)&&(inm(x-1,y)||inm(x+1,y)||inm(x,y-1)||inm(x,y+1)))g[y*N+x]=o.o||1;
  }
}
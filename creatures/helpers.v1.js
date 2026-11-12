const N=32;
const mask=()=>new Uint8Array(N*N);
function setp(m,x,y,fl){x=Math.floor(x);if(fl)x=N-1-x;y=Math.floor(y);if(x>=0&&y>=0&&x<N&&y<N)m[y*N+x]=1;}
function fillEll(m,cx,cy,rx,ry,fl){for(let y=Math.max(0,Math.floor(cy-ry));y<=Math.min(N-1,Math.ceil(cy+ry));y++)for(let x=0;x<N;x++){const dx=(x+.5-cx)/rx,dy=(y+.5-cy)/ry;if(dx*dx+dy*dy<=1)setp(m,x,y,fl);}}
function fillPoly(m,pts,fl){const n=pts.length;for(let y=0;y<N;y++)for(let x=0;x<N;x++){const px=x+.5,py=y+.5;let ins=false;for(let i=0,j=n-1;i<n;j=i++){const xi=pts[i][0],yi=pts[i][1],xj=pts[j][0],yj=pts[j][1];if(((yi>py)!==(yj>py))&&(px<(xj-xi)*(py-yi)/(yj-yi)+xi))ins=!ins;}if(ins)setp(m,x,y,fl);}}
function bez(pts,t){let p=pts.slice();while(p.length>1){const q=[];for(let i=0;i<p.length-1;i++)q.push([p[i][0]+(p[i+1][0]-p[i][0])*t,p[i][1]+(p[i+1][1]-p[i][1])*t]);p=q;}return p[0];}
function curve(m,pts,t0,t1,fl){for(let s=0;s<=48;s++){const t=s/48,p=bez(pts,t),th=t0+(t1-t0)*t,r=th/2;for(let y=Math.max(0,Math.floor(p[1]-r-1));y<=Math.min(N-1,Math.ceil(p[1]+r+1));y++)for(let x=0;x<N;x++){const dx=x+.5-p[0],dy=y+.5-p[1];if(dx*dx+dy*dy<=r*r+.15)setp(m,x,y,fl);}}}

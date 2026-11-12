/* 0.56: Forgelings are drawn on a 40x40 grid: the creature's own 32x32 coordinates with a 4-pixel margin all
   round (SPP), so ear tips, crowns, hats, wings and tails that reach past the old frame are drawn instead of cut.
   Shapes use creature coordinates (SPC=32 wide, mirrored about its middle); SPI(x,y) is a creature pixel's grid index.
   Every place that shows a sprite places the 40x40 grid 4 pixels up and left of where the 32x32 one went. */
const SPC=32,SPP=4,N=SPC+2*SPP,SPN=N;
const SPI=(x,y)=>(y+SPP)*N+x+SPP;
const mask=()=>new Uint8Array(N*N);
function setp(m,x,y,fl){x=Math.floor(x);if(fl)x=SPC-1-x;y=Math.floor(y);const X=x+SPP,Y=y+SPP;if(X>=0&&Y>=0&&X<N&&Y<N)m[Y*N+X]=1;}
function fillEll(m,cx,cy,rx,ry,fl){for(let y=Math.max(-SPP,Math.floor(cy-ry));y<=Math.min(SPC+SPP-1,Math.ceil(cy+ry));y++)for(let x=-SPP;x<SPC+SPP;x++){const dx=(x+.5-cx)/rx,dy=(y+.5-cy)/ry;if(dx*dx+dy*dy<=1)setp(m,x,y,fl);}}
function fillPoly(m,pts,fl){const n=pts.length;for(let y=-SPP;y<SPC+SPP;y++)for(let x=-SPP;x<SPC+SPP;x++){const px=x+.5,py=y+.5;let ins=false;for(let i=0,j=n-1;i<n;j=i++){const xi=pts[i][0],yi=pts[i][1],xj=pts[j][0],yj=pts[j][1];if(((yi>py)!==(yj>py))&&(px<(xj-xi)*(py-yi)/(yj-yi)+xi))ins=!ins;}if(ins)setp(m,x,y,fl);}}
function bez(pts,t){let p=pts.slice();while(p.length>1){const q=[];for(let i=0;i<p.length-1;i++)q.push([p[i][0]+(p[i+1][0]-p[i][0])*t,p[i][1]+(p[i+1][1]-p[i][1])*t]);p=q;}return p[0];}
function curve(m,pts,t0,t1,fl){for(let s=0;s<=48;s++){const t=s/48,p=bez(pts,t),th=t0+(t1-t0)*t,r=th/2;for(let y=Math.max(-SPP,Math.floor(p[1]-r-1));y<=Math.min(SPC+SPP-1,Math.ceil(p[1]+r+1));y++)for(let x=-SPP;x<SPC+SPP;x++){const dx=x+.5-p[0],dy=y+.5-p[1];if(dx*dx+dy*dy<=r*r+.15)setp(m,x,y,fl);}}}

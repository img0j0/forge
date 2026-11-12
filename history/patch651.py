# 0.65.1: sharper photo postcards (Hunter, November 12: "the postcard is just very blurry. Not sure if that is fixable").
#   New photo postcards are 96 x 72 (2.25 times the dots of 64 x 48), scaled down by halving (close to a box filter, so
#   no smearing), lightly sharpened before the shades are chosen, and dithered more gently (less speckle). About
#   2.6 KB each, so at most 400 are kept. Postcards made in 0.65.0 stay 64 x 48 (they are told apart by length);
#   "Change the photo" remakes one. The Forgelings' own drawn postcards are unchanged.
import re,subprocess,os
S=open('base65.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.65.0'","const VERSION='prototype 0.65.1'")
rep("<title>Forgelings (prototype 0.65.0)</title>","<title>Forgelings (prototype 0.65.1)</title>")

rep("const PC_W=64,PC_H=48,PC_MAX=500,PC_B64=4*Math.ceil(PC_W*PC_H*3/8/3);",
    "const PC_W=64,PC_H=48,PH_W=96,PH_H=72,PC_MAX=400,PC_B64=4*Math.ceil(PC_W*PC_H*3/8/3),PH_B64=4*Math.ceil(PH_W*PH_H*3/8/3);\nconst pcDims=p=>p.length===PH_B64?[PH_W,PH_H]:[PC_W,PC_H];")
rep("v.p.length===PC_B64&&","(v.p.length===PC_B64||v.p.length===PH_B64)&&")
rep("function pcUnpack(p){const s=atob(p),n=PC_W*PC_H,","function pcUnpack(p){const [w,h]=pcDims(p),s=atob(p),n=w*h,")
rep("function pcDraw(idx,r){const cv=document.createElement('canvas');cv.width=PC_W;cv.height=PC_H;const x=cv.getContext('2d'),im=x.createImageData(PC_W,PC_H),",
    "function pcDraw(idx,r,w,h){w=w||PC_W;h=h||PC_H;const cv=document.createElement('canvas');cv.width=w;cv.height=h;const x=cv.getContext('2d'),im=x.createImageData(w,h),")
rep("try{u=pcDraw(pcUnpack(p),r);}","try{const [w,h]=pcDims(p);u=pcDraw(pcUnpack(p),r,w,h);}")
# the photo: halving steps, a light unsharp mask on the brightness, gentler dither
m=re.search(r"function pcFromImage\(img\)\{[\s\S]*?\n  return idx;\}",S);assert m
S=S[:m.start()]+"""function pcFromImage(img){
  const iw=img.naturalWidth||img.width,ih=img.naturalHeight||img.height;if(!iw||!ih)return null;
  const W=PH_W,H=PH_H,s=Math.max(W/iw,H/ih),sw=W/s,sh=H/s;
  let k=8;while(k>1&&(sw<W*k||sh<H*k))k/=2;
  let cv=document.createElement('canvas');cv.width=W*k;cv.height=H*k;let x=cv.getContext('2d');x.imageSmoothingEnabled=true;x.imageSmoothingQuality='high';x.drawImage(img,(iw-sw)/2,(ih-sh)/2,sw,sh,0,0,W*k,H*k);
  while(k>1){k/=2;const c2=document.createElement('canvas');c2.width=W*k;c2.height=H*k;const x2=c2.getContext('2d');x2.imageSmoothingEnabled=true;x2.imageSmoothingQuality='high';x2.drawImage(cv,0,0,W*k,H*k);cv=c2;x=x2;}
  const d=x.getImageData(0,0,W,H).data,n=W*H,L0=new Float32Array(n);
  for(let i=0;i<n;i++)L0[i]=.2126*d[i*4]+.7152*d[i*4+1]+.0722*d[i*4+2];
  const at=(xx,y)=>L0[Math.min(H-1,Math.max(0,y))*W+Math.min(W-1,Math.max(0,xx))],L=new Float32Array(n);
  for(let y=0;y<H;y++)for(let xx=0;xx<W;xx++){let b=0;for(let j=-1;j<=1;j++)for(let i=-1;i<=1;i++)b+=at(xx+i,y+j)*(i?1:2)*(j?1:2);L[y*W+xx]=L0[y*W+xx]+.6*(L0[y*W+xx]-b/16);}
  const so=Array.from(L).sort((a,b)=>a-b),lo=so[Math.floor(n*.02)],hi=Math.max(lo+24,so[Math.floor(n*.98)]);
  const idx=new Uint8Array(n);
  for(let y=0;y<H;y++)for(let xx=0;xx<W;xx++){const i=y*W+xx,t=Math.min(1,Math.max(0,(L[i]-lo)/(hi-lo)));idx[i]=Math.max(0,Math.min(7,Math.round(t*7+(BAYER4[(y&3)*4+(xx&3)]/16-.47)*.55)));}
  return idx;}"""+S[m.end():]

out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk651.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk651.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)

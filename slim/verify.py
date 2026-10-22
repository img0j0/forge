import re, sys, json
sys.path.insert(0, 'slim'); from svgslim import slim, conv_svg
from playwright.sync_api import sync_playwright
s = open(sys.argv[1], encoding='utf8').read()
uris = re.findall(r"url\(\"data:image/svg\+xml,<svg.*?</svg>\"\)", s, re.S)
pairs = []
for u in uris:
    o, _, _ = slim(u)
    if o != u: pairs.append((u[5:-2], o[5:-2]))
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.set_content("<html><body></body></html>")
    res = pg.evaluate("""async(pairs)=>{
      const draw=src=>new Promise(r=>{const i=new Image();i.onload=()=>{const W=160,H=224,c=document.createElement('canvas');c.width=W;c.height=H;const x=c.getContext('2d');x.drawImage(i,0,0,W,H);r(Array.from(x.getImageData(0,0,W,H).data))};i.onerror=()=>r(null);i.src=src;});
      const out=[];for(const [a,b] of pairs){const A=await draw(a),B=await draw(b);if(!A||!B){out.push('load fail');continue;}let d=0,mx=0;for(let k=0;k<A.length;k++){const e=Math.abs(A[k]-B[k]);if(e>2)d++;mx=Math.max(mx,e);}out.push([d,mx]);}return out;}""", pairs)
    print(res); b.close()

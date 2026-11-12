# Identity check for the rendering upgrade: for 2,000 Forgelings of each generation (bright and Shade, every rarity,
# keepsakes, blink and bob), the silhouette (which pixels are drawn) and the face (eyes, glow, blush: slots 8, 9, 10,
# 16) must be exactly where the shipped build draws them. Only shading and outline colours may change.
import sys,os,subprocess
H=os.path.dirname(os.path.abspath(__file__)); subprocess.run(['python3',H+'/mk.py'],check=True)
s=open(H+'/../work.html').read(); i=s.find('function buildSprite('); j=s.find('\n}',i)+2
open('/tmp/cur.html','w').write(s[:j]+'\nwindow.__H={genSpec,buildSprite,makePal,N};'+s[j:])
from playwright.sync_api import sync_playwright
gen=int(sys.argv[1]) if len(sys.argv)>1 else 1
JS="""(gen)=>{const GN=__H.N||32,O=(GN-32)/2,crop=g=>{const o=[];for(let y=0;y<32;y++)for(let x=0;x<32;x++)o.push(g[(y+O)*GN+x+O]);return o;};const K=['','hat','scarf','flower','charm2','cap','lantern'];const out=[];for(let i=0;i<2000;i++){const c={id:i,seed:(9001+i*104729)>>>0,rarity:i%5,dark:i%2===1,theme:i%5,v:i%12,keep:K[i%K.length],bond:0,gen};
  const S=__H.genSpec(c);for(const[b,bl]of[[0,0],[1,1]]){const g=__H.buildSprite(S,b,bl);out.push(crop(g).map(v=>!v?'.':[8,9,10,16].includes(v)?v.toString(36):'#').join(''));}}return out;}"""
with sync_playwright() as p:
    b=p.chromium.launch(); r={}
    for f in ('/tmp/cur.html','/tmp/c54.html'):
        pg=b.new_page(); pg.goto('file://'+f); pg.wait_for_function('window.__H'); r[f]=pg.evaluate(JS,gen); pg.close()
    b.close()
a,bb=r['/tmp/cur.html'],r['/tmp/c54.html']; diff=[k for k in range(len(a)) if a[k]!=bb[k]]
print(f'generation {gen}: {len(a)} sprites, {len(diff)} differ in silhouette or face', 'IDENTICAL' if not diff else diff[:10])

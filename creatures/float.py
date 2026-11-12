# Head keepsakes (hat, cap, flower, daisies) must rest on the Forgeling: some column of the keepsake has the body or
# an ear directly beneath it. Checks 3,000 of each generation.
import sys,os,subprocess
H=os.path.dirname(os.path.abspath(__file__)); subprocess.run(['python3',H+'/mk.py'],check=True)
from playwright.sync_api import sync_playwright
JS="""(gen)=>{const GN=__H.N||32;const K=['hat','cap','flower','daisies'];const bad=[];let n=0;for(let i=0;i<3000;i++){const keep=K[i%4];
  const c={id:i,seed:(31337+i*7919)>>>0,rarity:i%5,dark:i%2===1,theme:i%5,v:i%12,keep,bond:0,gen};const c0=Object.assign({},c,{keep:''});
  const a=__H.buildSprite(__H.genSpec(c),0,0),b=__H.buildSprite(__H.genSpec(c0),0,0);n++;
  const kp=[];for(let p=0;p<GN*GN;p++)if(a[p]!==b[p]&&a[p]!==1&&b[p]===0)kp.push(p);if(!kp.length)continue;
  let ok=false;for(const p of kp){const x=p%GN,y=(p-x)/GN;for(let d=1;d<=2;d++){const q=(y+d)*GN+x;if(y+d<GN&&b[q]&&!kp.includes(q)){ok=true;break;}}if(ok)break;}
  if(!ok)bad.push({i,keep,dark:c.dark,shape:__H.genSpec(c).shape});}return {n,bad};}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto('file:///tmp/c54.html'); pg.wait_for_function('window.__H')
    for gen in (1,2):
        r=pg.evaluate(JS,gen); from collections import Counter
        print(f'generation {gen}: {r["n"]} with head keepsakes, {len(r["bad"])} floating', Counter((x['keep'],x['shape']) for x in r['bad']).most_common(8))
    b.close()

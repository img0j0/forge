# Nothing may be cut off by the 32x32 frame: no drawn pixel on row 0 or columns 0 and 31, and no part drawn past the
# top (a part reaching above row 0 shows as a flat cut). python3 clip.py [gen]
import sys,os,subprocess
H=os.path.dirname(os.path.abspath(__file__)); subprocess.run(['python3',H+'/mk.py'],check=True)
from playwright.sync_api import sync_playwright
from collections import Counter
JS="""(gen)=>{const GN=__H.N||32;const K=['','hat','cap','flower','daisies','scarf'];const bad=[];let n=0;for(let i=0;i<4000;i++){const c={id:i,seed:(2024+i*7919)>>>0,rarity:i%5,dark:i%3===2,theme:i%5,v:i%12,keep:K[i%K.length],bond:0,gen};
  const S=__H.genSpec(c);for(const bob of [0,1]){const g=__H.buildSprite(S,bob,0);n++;let w=[];
   const cut=v=>v&&!(v===1||(v>=32&&v<=38));for(let x=0;x<GN;x++)if(cut(g[x]))w.push('top');for(let y=0;y<GN;y++){if(cut(g[y*GN]))w.push('left');if(cut(g[y*GN+GN-1]))w.push('right');}
   if(w.length)bad.push({i,shape:S.shape,ears:S.ears||S.horns,keep:c.keep,crown:S.crown,wings:S.wings,tail:S.tail,why:[...new Set(w)].join('+'),dark:c.dark});}}return {n,bad};}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto('file:///tmp/c54.html'); pg.wait_for_function('window.__H')
    for gen in ([int(sys.argv[1])] if len(sys.argv)>1 else [1,2]):
        r=pg.evaluate(JS,gen)
        print(f'generation {gen}: {r["n"]} sprites, {len(r["bad"])} are cut off by the frame')
        print('   ',Counter((x['dark'],x['shape'],x['why']) for x in r['bad']).most_common(10))
        print('   ',Counter((x['ears'],x['keep'],bool(x['crown'])) for x in r['bad']).most_common(8))
    b.close()

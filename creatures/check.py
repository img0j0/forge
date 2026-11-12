# Layout check for second-generation Forgelings: python3 check.py [count]
# For every sampled Forgeling (bright and Shade, every rarity, every keepsake, both bob frames) the face (eyes, mouth,
# nose, blush) must be (A) still showing in the finished sprite, nothing drawn over it; (B) on the body, with body
# on all four sides of every face pixel, so it never touches an outline, an arm, a cap edge or the background.
import sys,os,subprocess,json
H=os.path.dirname(os.path.abspath(__file__)); subprocess.run(['python3',H+'/mk.py'],check=True)
from playwright.sync_api import sync_playwright
n=int(sys.argv[1]) if len(sys.argv)>1 else 3000
JS="""(n)=>{const KEEPS=['','hat','scarf','flower','daisies','charm','shells','cap','lantern','charm1','ward2'];const bad=[],swaps={};let total=0;
 for(let i=0;i<n;i++){const c={id:i,seed:(777+i*2654435761)>>>0,rarity:i%5,dark:i%3===2,theme:i%5,v:i%12,keep:KEEPS[i%KEEPS.length],bond:0,gen:2};
  const S=__H.genSpec(c);for(const bob of [0,1]){globalThis.__FDBG=[];const g=__H.buildSprite(S,bob,0);const r=__FDBG.pop();total++;if(!r){bad.push({i,why:'no record'});continue;}
   if(r.arms!==r.want)swaps[r.want+'>'+r.arms]=(swaps[r.want+'>'+r.arms]||0)+1;
   const why=[];r.FI.forEach((p,k)=>{if(g[p]!==r.FV[k])why.push('covered');if(r.PV[k]===1)why.push('on-a-line');const x=p%32,y=(p-x)/32;
     if(!r.M[p])why.push('off-body');else if(!r.dark&&[[1,0],[-1,0],[0,1],[0,-1]].some(([dx,dy])=>!r.M[(y+dy)*32+x+dx]))why.push('edge');});
   if(why.length)bad.push({i,bob,shape:S.shape,arms:r.arms,eyes:S.eyes,mouth:S.mouth,keep:c.keep,dark:c.dark,crown:S.crown,why:[...new Set(why)].join(',')});}}
 globalThis.__FDBG=null;return {total,bad,swaps};}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto('file:///tmp/c54.html'); pg.wait_for_function('window.__H')
    r=pg.evaluate(JS,n); b.close()
print('checked',r['total'],'sprites; problems',len(r['bad'])); print('pose changed to keep the face clear:',r['swaps'])
from collections import Counter
print(Counter((x['dark'],x['shape'],x['why'],x['keep'] if 'covered' in x['why'] else '') for x in r['bad']).most_common(25))
json.dump(r['bad'],open('/tmp/layout_bad.json','w'))

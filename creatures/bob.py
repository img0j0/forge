# Bobbing must move the whole Forgeling: above the feet, the bob frame is the rest frame one pixel lower (silhouette).
# python3 bob.py [html]  (default: the creature files)
import sys,os,subprocess
H=os.path.dirname(os.path.abspath(__file__)); subprocess.run(['python3',H+'/mk.py'],check=True)
f=sys.argv[1] if len(sys.argv)>1 else '/tmp/c54.html'
if f!='/tmp/c54.html':
    s=open(f).read(); i=s.find('function buildSprite('); j=s.find('\n}',i)+2; open('/tmp/bobx.html','w').write(s[:j]+'\nwindow.__H={genSpec,buildSprite,makePal,N};'+s[j:]); f='/tmp/bobx.html'
from playwright.sync_api import sync_playwright
from collections import Counter
JS="""()=>{const GN=__H.N||32,O=(GN-32)/2;const K=['','hat','cap','flower','daisies','scarf'];const bad=[];let n=0;
 for(const gen of [1,2])for(let i=0;i<3000;i++){const c={id:i,seed:(4711+i*7919)>>>0,rarity:i%5,dark:i%3===2,theme:i%5,v:i%12,keep:K[i%K.length],bond:0,gen};const S=__H.genSpec(c);
  const a=__H.buildSprite(S,0,0),b=__H.buildSprite(S,1,0);n++;let ok=true;
  for(let y=-O;y<22&&ok;y++)for(let x=-O;x<32+O;x++){const A=a[(y+O)*GN+x+O]?1:0,B=(y+1+O<GN)?(b[(y+1+O)*GN+x+O]?1:0):A;if(A!==B){ok=false;break;}}
  if(!ok)bad.push({gen,shape:S.shape,ears:S.ears||S.horns,keep:c.keep});}
 return {n,bad};}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto('file://'+f); pg.wait_for_function('window.__H'); r=pg.evaluate(JS); b.close()
print(f'{r["n"]} Forgelings, {len(r["bad"])} do not bob as one piece',Counter((x['gen'],x['shape'],x['ears'],x['keep']) for x in r['bad']).most_common(8))

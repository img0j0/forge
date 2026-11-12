# The first generation must not change: hash 1,200 old-generation sprites (cute and Shade, every rarity, blink and bob)
# with the 0.53 code and with the new code, and compare.
import sys,os,subprocess,hashlib
H=os.path.dirname(os.path.abspath(__file__)); subprocess.run(['python3',H+'/mk.py'],check=True)
import subprocess as sp
s=sp.run(['git','-C',H+'/..','show','c64b4f7:base53.html'],capture_output=True,text=True).stdout
i=s.find('function buildSprite('); j=s.find('\n}',i)+2
open('/tmp/c53.html','w').write(s[:j]+'\nwindow.__H={genSpec,buildSprite,makePal};'+s[j:])
sys.path.insert(0,'/home/claude/forge/qa')
from playwright.sync_api import sync_playwright
JS="""()=>{const out=[];for(let i=0;i<1200;i++){const c={id:i,seed:(12345+i*104729)>>>0,rarity:i%5,dark:i%2===1,theme:i%5,v:i%12,keep:['','hat','scarf','flower','charm2'][i%5],bond:0};
  const S=__H.genSpec(c);for(const[bb,bl]of[[0,0],[1,1]])out.push(Array.from(__H.buildSprite(S,bb,bl)).join(''));}return out.join('|');}"""
res={}
with sync_playwright() as p:
    b=p.chromium.launch()
    for f in ('/tmp/c53.html','/tmp/c54.html'):
        pg=b.new_page(); pg.goto('file://'+f); pg.wait_for_function('window.__H'); res[f]=hashlib.sha256(pg.evaluate(JS).encode()).hexdigest(); pg.close()
    b.close()
print(res); print('SAME' if len(set(res.values()))==1 else 'DIFFERENT')

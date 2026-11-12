# Which pixels get the holo rainbow (rarity 3: FOIL3 slots) before and after: python3 foil.py OUT.png
import sys,os,subprocess
H=os.path.dirname(os.path.abspath(__file__)); subprocess.run(['python3',H+'/mk.py'],check=True)
s=open(os.environ.get('BEFORE','/tmp/c541.html')).read(); i=s.find('function buildSprite('); j=s.find('\n}',i)+2
open('/tmp/cur.html','w').write(s[:j]+'\nwindow.__H={genSpec,buildSprite,makePal,N};'+s[j:])
from playwright.sync_api import sync_playwright
JS="""()=>{const GN=__H.N||32,O=(GN-32)/2;const Z=6,n=8,cv=document.createElement('canvas');cv.width=n*42*Z;cv.height=42*Z;const x=cv.getContext('2d');x.fillStyle='#222';x.fillRect(0,0,cv.width,cv.height);const F={4:1,6:1,9:1,10:1,17:1};
 for(let i=0;i<n;i++){const c={id:i,seed:(5150+i*7919)>>>0,rarity:3,dark:i%2===0,theme:1,v:i%12,keep:'',bond:0};const S=__H.genSpec(c),pl=__H.makePal(S,c).pal,g=__H.buildSprite(S,0,0);
  for(let k=0;k<GN*GN;k++){const sl=g[k];if(!sl)continue;const q=F[sl]?[255,60,200]:pl[sl];x.fillStyle=`rgb(${q[0]},${q[1]},${q[2]})`;x.fillRect(i*42*Z+5*Z+((k%GN)-O)*Z,5*Z+(Math.floor(k/GN)-O)*Z,Z,Z);}}return cv.toDataURL();}"""
imgs=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    for f in ('/tmp/cur.html','/tmp/c54.html'):
        pg=b.new_page(); pg.goto('file://'+f); pg.wait_for_function('window.__H'); imgs.append(pg.evaluate(JS)); pg.close()
    pg=b.new_page(viewport={'width':1700,'height':500}); pg.set_content(f"<body style='margin:0;background:#222'><img src='{imgs[0]}'><br><img src='{imgs[1]}'></body>"); pg.wait_for_timeout(300)
    pg.locator('body').screenshot(path=sys.argv[1]); b.close()

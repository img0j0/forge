# Before/after: python3 compare.py OUT.png [dark] [gen] — top row the shipped build, bottom row the creature files.
import sys,os,subprocess,base64
H=os.path.dirname(os.path.abspath(__file__)); subprocess.run(['python3',H+'/mk.py'],check=True)
s=open(os.environ.get('BEFORE',H+'/../work.html')).read(); i=s.find('function buildSprite('); j=s.find('\n}',i)+2
open('/tmp/cur.html','w').write(s[:j]+'\nwindow.__H={genSpec,buildSprite,makePal,N};'+s[j:])
from playwright.sync_api import sync_playwright
out=sys.argv[1];dark=len(sys.argv)>2 and sys.argv[2]=='1';gen=int(sys.argv[3]) if len(sys.argv)>3 else 1
JS="""([dark,gen])=>{const GN=__H.N||32,O=(GN-32)/2;const Z=6,n=8,cv=document.createElement('canvas');cv.width=n*42*Z;cv.height=42*Z;const x=cv.getContext('2d');x.fillStyle='#F3EAD3';x.fillRect(0,0,cv.width,cv.height);
 for(let i=0;i<n;i++){const c={id:i,seed:(4242+i*7919)>>>0,rarity:[0,1,2,3,4,1,2,0][i],dark,theme:i%5,v:i%12,keep:'',bond:0,gen};const S=__H.genSpec(c),pl=__H.makePal(S,c).pal,g=__H.buildSprite(S,0,0);
  for(let k=0;k<GN*GN;k++){const sl=g[k];if(!sl)continue;const q=pl[sl];x.fillStyle=`rgb(${q[0]},${q[1]},${q[2]})`;x.fillRect(i*42*Z+5*Z+((k%GN)-O)*Z,5*Z+(Math.floor(k/GN)-O)*Z,Z,Z);}}return cv.toDataURL();}"""
imgs=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    for f in ('/tmp/cur.html','/tmp/c54.html'):
        pg=b.new_page(); pg.goto('file://'+f); pg.wait_for_function('window.__H'); imgs.append(pg.evaluate(JS,[dark,gen])); pg.close()
    pg=b.new_page(viewport={'width':1700,'height':500}); pg.set_content(f"<body style='margin:0;background:#F3EAD3'><img src='{imgs[0]}'><br><img src='{imgs[1]}'></body>"); pg.wait_for_timeout(300)
    pg.locator('body').screenshot(path=out); b.close()

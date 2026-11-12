# Before/after for chosen Forgelings: python3 pick.py OUT.png '<JS filter on S and c>' gen [count]
import sys,os,subprocess
H=os.path.dirname(os.path.abspath(__file__)); subprocess.run(['python3',H+'/mk.py'],check=True)
s=open(os.environ.get('BEFORE','/tmp/c541.html')).read(); i=s.find('function buildSprite('); j=s.find('\n}',i)+2
open('/tmp/cur.html','w').write(s[:j]+'\nwindow.__H={genSpec,buildSprite,makePal,N};'+s[j:])
from playwright.sync_api import sync_playwright
flt,gen=sys.argv[2],int(sys.argv[3]);cnt=int(sys.argv[4]) if len(sys.argv)>4 else 8
JS="""([flt,gen,cnt])=>{const GN=__H.N||32,O=(GN-32)/2,Z=6,cv=document.createElement('canvas');cv.width=cnt*44*Z;cv.height=44*Z;const x=cv.getContext('2d');x.fillStyle='#F3EAD3';x.fillRect(0,0,cv.width,cv.height);
 const F=new Function('S','c','return '+flt);let n=0;for(let i=0;i<20000&&n<cnt;i++){const c={id:i,seed:(777+i*7919)>>>0,rarity:i%4,dark:i%2===1,theme:i%5,v:i%12,keep:'',bond:0,gen};const S=__H.genSpec(c);if(!F(S,c))continue;
  const pl=__H.makePal(S,c).pal,g=__H.buildSprite(S,0,0);x.strokeStyle='#C9B98F';x.strokeRect(n*44*Z+6*Z,6*Z,32*Z,32*Z);
  for(let k=0;k<GN*GN;k++){const sl=g[k];if(!sl)continue;const q=pl[sl];x.fillStyle=`rgb(${q[0]},${q[1]},${q[2]})`;x.fillRect(n*44*Z+6*Z+((k%GN)-O)*Z,6*Z+(Math.floor(k/GN)-O)*Z,Z,Z);}n++;}return cv.toDataURL();}"""
imgs=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    for f in ('/tmp/cur.html','/tmp/c54.html'):
        pg=b.new_page(); pg.goto('file://'+f); pg.wait_for_function('window.__H'); imgs.append(pg.evaluate(JS,[flt,gen,cnt])); pg.close()
    pg=b.new_page(viewport={'width':2200,'height':700}); pg.set_content(f"<body style='margin:0;background:#F3EAD3'><img src='{imgs[0]}'><br><img src='{imgs[1]}'></body>"); pg.wait_for_timeout(300)
    pg.locator('body').screenshot(path=sys.argv[1]); b.close()

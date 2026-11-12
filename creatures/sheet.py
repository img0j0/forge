# Contact sheet of Forgelings: python3 sheet.py OUT.png [gen] [dark] [count] [cols] [seed0]
import sys,os,subprocess
subprocess.run(['python3',os.path.join(os.path.dirname(os.path.abspath(__file__)),'mk.py')],check=True)
sys.path.insert(0,'/home/claude/forge/qa')
os.environ['FORGE_HTML']='file:///tmp/c54.html'
from lib import *
out=sys.argv[1];gen=int(sys.argv[2]) if len(sys.argv)>2 else 2;dark=sys.argv[3]=='1' if len(sys.argv)>3 else False
cnt=int(sys.argv[4]) if len(sys.argv)>4 else 48;cols=int(sys.argv[5]) if len(sys.argv)>5 else 8;s0=int(sys.argv[6]) if len(sys.argv)>6 else 1000
H=os.path.dirname(os.path.abspath(__file__))
code=open(H+'/cute2.js').read()+'\n'+open(H+'/genSpec.js').read()+'\n'+open(H+'/buildSprite.js').read()
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=newpage(b,1200,900)
    pg.goto(P); pg.wait_for_selector('#titleGo')

    pg.evaluate("k=>window.__K=k",os.environ.get('KEEPS','').split(',') if os.environ.get('KEEPS') else None)
    url=pg.evaluate("""([gen,dark,cnt,cols,s0])=>{const GN=__H.N||32,O=(GN-32)/2;const Z=4,cv=document.createElement('canvas');const rows=Math.ceil(cnt/cols);cv.width=cols*44*Z;cv.height=rows*44*Z;const x=cv.getContext('2d');x.fillStyle='#F3EAD3';x.fillRect(0,0,cv.width,cv.height);
      for(let i=0;i<cnt;i++){const c={id:i,seed:(s0+i*7919)>>>0,rarity:[0,0,1,1,2,3,4][i%7],dark,theme:i%5,v:i%12,keep:(window.__K||[''])[i%(window.__K||['']).length],bond:0,gen};
        const S=__H.genSpec(c),pl=__H.makePal(S,c).pal,g=__H.buildSprite(S,0,0);const ox=(i%cols)*44*Z+6*Z,oy=Math.floor(i/cols)*44*Z+6*Z;
        for(let k=0;k<GN*GN;k++){const sl=g[k];if(!sl)continue;const q=pl[sl];x.fillStyle=`rgb(${q[0]},${q[1]},${q[2]})`;x.fillRect(ox+((k%GN)-O)*Z,oy+(Math.floor(k/GN)-O)*Z,Z,Z);}
        x.fillStyle='#8a7';x.font='11px monospace';x.fillText((S.shape||'')+' '+(S.arms||'')+' '+(S.eyes||''),ox,oy+34*Z);}
      return cv.toDataURL();}""",[gen,dark,cnt,cols,s0])
    import base64; open(out,'wb').write(base64.b64decode(url.split(',')[1]))
    print(pg._errs[:3]); b.close()

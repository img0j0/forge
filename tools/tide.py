import sys,os,time,random; sys.path.insert(0,"/home/claude/qa-src/forge-qa/qa"); os.chdir("/home/claude/qa-src/forge-qa/qa")
os.environ["FORGE_HTML"]="file:///home/claude/forge/work.html"
from lib import *
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
BOT="""sigma=>{const g=()=>{let u=0,v=0;while(!u)u=Math.random();while(!v)v=Math.random();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v)};
 let busy=false,prev=null;const step=now=>{const s=document.getElementById('pgStone'),c=document.getElementById('pgCalm');if(!s||!c)return;
  const x=s.getBoundingClientRect().left+11,z=c.getBoundingClientRect(),cx=z.left+z.width/2;
  if(prev&&!busy){const v=(x-prev[0])/(now-prev[1]);if(Math.abs(v)>.02){const t=(cx-x)/v;if(t>60&&t<260){busy=true;setTimeout(()=>{const b=document.getElementById('pgSkip');if(b)b.click();setTimeout(()=>busy=false,250)},Math.max(0,t+g()*sigma));}}}
  prev=[x,now];requestAnimationFrame(step)};requestAnimationFrame(step)}"""
CFG={"new":dict(stats=[30,30,30],bond=0,dark=False),"strong":dict(stats=[85,85,85],bond=9,dark=False),"dark":dict(stats=[55,55,55],bond=9,dark=True)}
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=newpage(b,390,844); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); base=st(pg)
    for sigma in (60,90):
      for cname,cf in CFG.items():
        out=[]
        for r in range(3):
            s=build(base,[0,0,1,0,0]); s["seen"]=99; c=s["cards"][0]; c.update(cf); s["hearth"]["slots"]=[c["id"]]; s["hearth"]["visits"]={"date":s["date"],"used":3}; s["games"]={"best":{},"played":0,"curioDay":""}
            pg.evaluate("()=>{const b=document.getElementById('pgSit');if(b)b.click();const d=document.getElementById('pgDone');if(d)d.click()}"); pg.wait_for_timeout(200)
            setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg); tabto(pg,"hearth"); pg.tap("#hPlay"); pg.wait_for_timeout(250); pg.tap("#modal [data-game]"); pg.wait_for_timeout(250); pg.tap("#pgGo"); pg.evaluate(BOT,sigma)
            t0=time.time()
            while time.time()-t0<24 and not pg.locator("#pgAgain").count(): pg.wait_for_timeout(200)
            out.append(st(pg)["games"]["best"].get("tide",0))
        print("sigma",sigma,cname,out,flush=True)
    b.close()
